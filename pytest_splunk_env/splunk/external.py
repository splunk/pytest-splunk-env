# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from .base import SplunkEnv
import logging
LOGGER = logging.getLogger(__name__)

class SplunkEnvExternal(SplunkEnv):

    def __init__(self,
                 search_index,
                 search_retry,
                 search_interval,
                 splunkd_host,
                 splunkd_port,
                 web_port,
                 username,
                 password,
                 hec_token
                 ):
        super().__init__(
            search_index,
            search_retry,
            search_interval,
            splunkd_host=splunkd_host,
            splunkd_port=splunkd_port,
            web_port="8000",
            username=username,
            password=password,
            hec_token=hec_token,
        )
