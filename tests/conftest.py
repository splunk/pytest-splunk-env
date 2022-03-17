# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session")
def docker_compose_files(pytestconfig):
    """Get the docker-compose.yml absolute path.
    Override this fixture in your tests if you need a custom location.
    """
    return [os.path.join(str(pytestconfig.rootdir), "docker-compose.yml")]


def pytest_addoption(parser):
    """Add options for interaction with Splunk this allows the tool to work in two modes
    1) docker mode which is typically used by developers on their workstation
        manages a single instance of splunk
    2) external interacts with a single instance of splunk that is lifecycle managed
        by another process such as a ci/cd pipeline
    """

    group = parser.getgroup("splunk-env-testng")

    group.addoption(
        "--test-sc4s-host",
        action="store",
        dest="test_sc4s_host",
        default="127.0.0.1",
        help="Address of the sc4s Server",
    )
    group.addoption(
        "--test-splunk-host",
        action="store",
        dest="test_splunk_host",
        default="127.0.0.1",
        help=(
            "Address of the Splunk Server where search queries will be executed. Do not provide "
            "http scheme in the host. default is 127.0.0.1"
        ),
    )
