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
                 hec_token
                 ):
        super().__init__(
            search_index,
            search_retry,
            search_interval,
            splunkd_host="127.0.0.1",
            splunkd_port="8089",
            web_port="8000",
            username=username,
            password=password,
            hec_token=hec_token
        )
