# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import logging
import os

import pytest
import splunklib.client as client

from .base import SplunkEnv
from .external import SplunkEnvExternal

LOGGER = logging.getLogger(__name__)


class SplunkEnvDockerCompose(SplunkEnv):
    def __init__(
        self,
        docker_services,
        search_index,
        search_retry,
        search_interval,
        username,
        password,
        hec_token,
        splunk_version,
    ):

        # Env vars are used to pass config to splunk
        os.environ["SPLUNK_HEC_TOKEN"] = hec_token
        os.environ["SPLUNK_USER"] = username
        os.environ["SPLUNK_PASSWORD"] = password
        os.environ["SPLUNK_VERSION"] = splunk_version

        self.docker_services = docker_services
        self.docker_services.start("splunk")

        super().__init__(
            search_index,
            search_retry,
            search_interval,
            splunkd_host=docker_services.docker_ip,
            splunkd_port=docker_services.port_for("splunk", 8089),
            web_port=docker_services.port_for("splunk", 8000),
            username=username,
            password=password,
            hec_host=docker_services.docker_ip,
            hec_port=docker_services.port_for("splunk", 8088),
            hec_token=hec_token,
        )
