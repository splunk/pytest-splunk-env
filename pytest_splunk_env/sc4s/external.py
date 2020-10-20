

import pytest
import os
from .base import SC4SEnv
import splunklib.client as client
import logging
LOGGER = logging.getLogger(__name__)


class SC4SEnvExternal(SC4SEnv):

    def __init__(self,
                 splunk,
                 sc4s_host
                 ):

        super().__init__(
            splunk,
            sc4s_host
        )
