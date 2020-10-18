import pytest

from pytest_splunk_env.splunk.helmut.manager.jobs import Jobs
from pytest_splunk_env.splunk.helmut.splunk.cloud import CloudSplunk
from pytest_splunk_env.splunk.helmut_lib.SearchUtil import SearchUtil
import logging
LOGGER = logging.getLogger(__name__)


class SplunkEnv():
    """[summary]
    """

    def __init__(self,
                 search_index,
                 search_retry,
                 search_interval,
                 name=None,
                 splunkd_scheme="https",
                 splunkd_host="127.0.0.1",
                 splunkd_port="8089",
                 web_scheme="http",
                 splunk_web="8000",
                 username=None,
                 password=None
                 ):

        LOGGER.info("Initializing SearchUtil for the Splunk instance.")
        self.cloud_splunk = CloudSplunk(
            splunkd_host=splunkd_host,
            splunkd_port=splunkd_port,
            username=username,
            password=password,
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

    def splunk_search():
        return self.search_util
