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

class SC4SEnv():
    def __init__(self,
                 splunk,
                 sc4s_host
                 ):

        
        self.splunk = splunk
        self.sc4s_host = sc4s_host
        self.check_ready()

    def check_ready(self):
        search = f"| search index=main sourcetype=\"sc4s:events\" | tail 10"
        LOGGER.info(f"Search: {search}")
        result = self.splunk.search_util.checkQueryCountIsGreaterThanZero(
            search, interval=1, retries=60
        )
        LOGGER.info(f"result: {result}")
        if not result:
            raise Exception()
        
    def get_service(self,port,proto):
        return self.sc4s_host, port