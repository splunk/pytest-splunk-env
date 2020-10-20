# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from .base import SplunkEnv
import logging
LOGGER = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add options for interaction with Splunk this allows the tool to work in two modes
    1) docker mode which is typically used by developers on their workstation
        manages a single instance of splunk
    2) external interacts with a single instance of splunk that is lifecycle managed
        by another process such as a ci/cd pipeline
    """

    group_external = parser.getgroup("splunk-env-external")
    group_external.addoption(
        "--splunk-host",
        action="store",
        dest="splunk_host",
        default="127.0.0.1",
        help=(
            "Address of the Splunk Server where search queries will be executed. Do not provide "
            "http scheme in the host. default is 127.0.0.1"
        ),
    )
    group_external.addoption(
        "--splunk-forwarder-host",
        action="store",
        dest="splunk_forwarder_host",
        help=(
            "Address of the Splunk Forwarder Server. Do not provide "
            "http scheme in the host."
        ),
    )
    group_external.addoption(
        "--splunk-hec-scheme",
        action="store",
        dest="splunk_hec_scheme",
        default="https",
        help="Splunk HTTP event collector port. default is https.",
    )
    group_external.addoption(
        "--splunk-hec-port",
        action="store",
        dest="splunk_hec",
        default="8088",
        help="Splunk HTTP event collector port. default is 8088.",
    )
    group_external.addoption(
        "--splunk-hec-token",
        action="store",
        dest="splunk_hec_token",
        default="9b741d03-43e9-4164-908b-e09102327d22",
        help='Splunk HTTP event collector token. default is "9b741d03-43e9-4164-908b-e09102327d22" If an external forwarder is used provide HEC token of forwarder.',
    )
    group_external.addoption(
        "--splunk-port",
        action="store",
        dest="splunkd_port",
        default="8089",
        help="Splunk Management port. default is 8089.",
    )
    group_external.addoption(
        "--splunk-s2s-port",
        action="store",
        dest="splunk_s2s",
        default="9997",
        help="Splunk s2s port. default is 9997.",
    )
    group_external.addoption(
        "--splunk-s2s-scheme",
        action="store",
        dest="splunk_s2s_scheme",
        default="tcp",
        help="Splunk s2s scheme. tls|tcp default is tcp.",
    )
    group_external.addoption(
        "--splunkweb-ext-port",
        action="store",
        dest="splunk_web",
        default="8000",
        help="Splunk web port. default is 8000.",
    )
    group_external.addoption(
        "--splunk-user",
        action="store",
        dest="splunk_user",
        default="admin",
        help="Splunk login user. The user should have search capabilities.",
    )
    group_external.addoption(
        "--splunk-password",
        action="store",
        dest="splunk_password",
        default="Chang3d!",
        help="Password of the Splunk user",
    )
    group_external.addoption(
        "--splunk-version",
        action="store",
        dest="splunk_version",
        default="latest",
        help=(
            "Splunk version to spin up with docker while splunk-type "
            " is set to docker. Examples, "
            " 1) latest: latest Splunk Enterprise tagged by the https://github.com/splunk/docker-splunk"
            " 2) 8.0.0: GA release of 8.0.0."
        ),
    )


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
