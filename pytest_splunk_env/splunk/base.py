import pytest

from pytest_splunk_env.splunk.helmut.manager.jobs import Jobs
from pytest_splunk_env.splunk.helmut.splunk.cloud import CloudSplunk
from pytest_splunk_env.splunk.helmut_lib.SearchUtil import SearchUtil
import requests
import splunklib.client as client
import logging
import time, timeit
import json

LOGGER = logging.getLogger(__name__)


class SplunkEnv():
    """[summary]
    """

    def __init__(self,
                 search_index,
                 search_retry,
                 search_interval,                 
                 name=None,
                 username="Admin",
                 password="changeme",
                 splunkd_scheme="https",
                 splunkd_host="127.0.0.1",
                 splunkd_port="8089",
                 web_scheme="http",
                 web_port="8000",
                 web_validate=False,
                 s2s_scheme=None,
                 s2s_host="127.0.0.1",
                 s2s_port=9997,
                 s2s_validate=False,
                 hec_scheme="https",
                 hec_host="127.0.0.1",
                 hec_port="8088",
                 hec_validate=False,
                 hec_token = None
                 
                 ):

        LOGGER.info(
            f"Docker container splunk info. host={splunkd_host}, port={splunkd_port}, port_web={web_port} port_hec={hec_port} port_s2s={s2s_port}",
        )

        self.splunkd_host = splunkd_host
        self.splunkd_scheme = splunkd_scheme
        self.splunkd_port = splunkd_port

        self.web_scheme = web_scheme
        self.web_port = web_port
        self.web_validate = web_validate

        self.s2s_scheme = s2s_scheme
        self.s2s_host = s2s_host
        self.s2s_port = s2s_port
        self.s2s_validate = s2s_validate

        self.hec_scheme = hec_scheme
        self.hec_host = hec_host
        self.hec_port = hec_port
        self.hec_validate = hec_validate
        self.hec_token = hec_token

        self.username = username
        self.password = password

        LOGGER.info("Wait for remote side to be responsive splunkd")
        self.wait_until_responsive(
            timeout=180.0, pause=0.5, check=lambda: self.is_responsive_splunk(),
        )
        LOGGER.info("Wait for remote side to be responsive hec")
        self.wait_until_responsive(
            timeout=30.0, pause=0.5, check=lambda: self.is_responsive_hec(),
        )
        
        LOGGER.info("Login to Splunk")        
        self.cloud_splunk = CloudSplunk(
            splunkd_host=self.splunkd_host,
            splunkd_port=self.splunkd_port,
            username=self.username,
            password=self.password,
        )
        self.conn = self.cloud_splunk.create_logged_in_connector()
        self.jobs = Jobs(self.conn)
        LOGGER.info("initialized SearchUtil for the Splunk instace.")
        self.search_util = SearchUtil(self.jobs, LOGGER)
        self.search_util.search_index = search_index
        self.search_util.search_retry = search_retry
        self.search_util.search_interval = search_interval

        search = f"| tstats count where index=_internal sourcetype=splunkd"
        LOGGER.info(f"Search: {search}")
        result = self.search_util.checkQueryCountIsGreaterThanZero(
            search, interval=self.search_util.search_interval, retries=self.search_util.search_retry
        )
        LOGGER.info(f"result: {result}")
        if not result:
            raise Exception()
        
        event = "this is a test"
        self.send_hec_event(event)
        search = f"| search index=_internal sourcetype=\"pytest-splunk-env:probe\" \"{event}\""
        LOGGER.info(f"Search: {search}")
        result = self.search_util.checkQueryCountIsGreaterThanZero(
            search, interval=1, retries=10
        )
        LOGGER.info(f"result: {result}")
        if not result:
            raise Exception()
        






    @staticmethod
    def wait_until_responsive(check, timeout, pause,
                              clock=timeit.default_timer):
        """Wait until a service is responsive."""

        ref = clock()
        now = ref
        while (now - ref) < timeout:
            if check():
                return
            time.sleep(pause)
            now = clock()

        raise Exception(
            'Timeout reached while waiting on service!'
        )


    def is_responsive_splunk(self):
        """
        Verify if the management port of Splunk is responsive or not

        Args:
            splunk (dict): details of the Splunk instance

        Returns:
            bool: True if Splunk is responsive. False otherwise
        """
        try:
            LOGGER.info(
                "Trying to connect Splunk instance...  splunk=%s", self.splunkd_host,
            )
            client.connect(
                username=self.username,
                password=self.password,
                host=self.splunkd_host,
                port=self.splunkd_port,
            )
            LOGGER.info("Connected to Splunk instance.")

            return True
        except Exception as e:
            LOGGER.debug(
                "Could not connect to Splunk Instance. Will try again. exception=%s", str(
                    e),
            )
            return False

    def is_responsive_hec(self):
        """
        Verify if the hec port of Splunk is responsive or not

        Args:
            splunk (dict): details of the Splunk instance

        Returns:
            bool: True if Splunk HEC is responsive. False otherwise
        """
        try:
            uri = f'{self.hec_scheme}://{self.hec_host}:{self.hec_port}/services/collector/health/1.0'
            LOGGER.info(
                f"Trying to connect Splunk HEC... uri={uri}",
            )
            session_headers = {
                "Authorization": f'Splunk {self.hec_token}'
            }
            response = requests.get(
                    uri,
                    verify=False,
                )
            LOGGER.debug("Status code: {}".format(response.status_code))
            if response.status_code in (200,201):
                LOGGER.info("Splunk HEC is responsive.")
                return True
            else:
                return False
        except Exception as e:
            LOGGER.debug(
                "Could not connect to Splunk HEC. Will try again. exception=%s", str(e),
            )
            return False

    def send_hec_event(self,event_content):
        """
        Used to send an event for to validate the stack

        Args:
            event: string value of the event
        
        """
        try:
            uri = f'{self.hec_scheme}://{self.hec_host}:{self.hec_port}/services/collector'
            LOGGER.info(
                f"Trying to connect Splunk HEC... uri={uri}",
            )
            session_headers = {
                "Authorization": f'Splunk {self.hec_token}',
                'Connection': 'close'
            }
            payload = { "sourcetype": "pytest-splunk-env:probe", "index": "_internal", "event": event_content }

            event = []
            event.append(json.dumps(payload))
            
            response = requests.post(
                    uri,
                    verify=False,
                    data=event[0],
                    headers=session_headers
                )
            LOGGER.debug("Status code: {}".format(response.status_code))
            if response.status_code in (200,201):
                LOGGER.info("Splunk HEC is responsive.")
                return True
            else:
                LOGGER.error(
                "Could not post to Splunk HEC. status code %s", str(response.status_code),
                )
                raise Exception
        except Exception as e:
            LOGGER.warning(
                "Could not connect to Splunk HEC. Will try again. exception=%s", str(e),
            )
            return False

    def splunk_search():
        return self.search_util
