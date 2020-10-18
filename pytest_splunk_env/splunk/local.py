import pytest
from .base import SplunkEnv
from .external import SplunkEnvExternal
import logging
LOGGER = logging.getLogger(__name__)


class SplunkEnvLocal(SplunkEnvExternal):

    def __init__(self,
                 search_index,
                 search_retry,
                 search_interval,
                 username,
                 password,
                 ):
        super().__init__(
            search_index,
            search_retry,
            search_interval,
            splunkd_host="127.0.0.1",
            splunkd_port="8089",
            splunk_web="8000",
            username=username,
            password=password
        )
