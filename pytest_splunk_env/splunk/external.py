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
                 s2s_scheme=None,
                 s2s_host="127.0.0.1",
                 s2s_port=9997,
                 s2s_validate=False,
                 hec_scheme="https",
                 hec_host="127.0.0.1",
                 hec_port="8088",
                 hec_validate=False,
                 hec_token=None
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
            s2s_scheme=hec_scheme,
            s2s_host=s2s_host,
            s2s_port=s2s_port,
            s2s_validate=s2s_validate,
            hec_scheme=hec_scheme,
            hec_host=hec_host,
            hec_port=hec_port,
            hec_validate=False,
            
            hec_token=hec_token,
        )
