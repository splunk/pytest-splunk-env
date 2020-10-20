# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import logging
from filelock import FileLock
import os
import pytest

from .base import SC4SEnv
#from .docker import splunk_docker
from .external import SC4SEnvExternal
#from .local import SC4SEnvLocal
from .dockercompose import SC4SEnvDockerCompose
LOGGER = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add options for interaction with Splunk this allows the tool to work in two modes
    1) docker mode which is typically used by developers on their workstation
        manages a single instance of splunk
    2) external interacts with a single instance of splunk that is lifecycle managed
        by another process such as a ci/cd pipeline
    """

    group = parser.getgroup("splunk-env-sc4s")

    group.addoption(
        "--sc4s-host",
        action="store",
        dest="sc4s_host",
        default="127.0.0.1",
        help="Address of the sc4s Server",
    )

    group.addoption(
        "--sc4s-port",
        action="store",
        dest="sc4s_port",
        default="514",
        help="SC4S Port. default is 514",
    )

    group.addoption(
        "--sc4s-type",
        action="store",
        dest="sc4s_type",
        default="external",
        help="SC4S Type external|local|docker-compose Note: if splunk-type is docker-compose sc4s must match",
    )


@pytest.fixture(scope="session")
def sc4s(request):
    """
    This fixture based on the passed option will provide a real fixture
    for external or docker s4cs

    Returns:
        sc4s: Details of the sc4s
    """
    sc4s_type = request.config.getoption("sc4s_type")
    LOGGER.info("Get the Splunk instance of sc4s_type=%s", sc4s_type)

    if sc4s_type == "external":
        fixture = "sc4s_external"
    elif sc4s_type == "local":
        fixture = "sc4s_local"
    elif sc4s_type == "docker":
        fixture = "sc4s_docker"
    elif sc4s_type == "docker-compose":
        fixture = "sc4s_docker_compose"
    else:
        raise Exception
    request.fixturenames.append(fixture)
    sc4s = request.getfixturevalue(fixture)

    yield sc4s


@pytest.fixture(scope="session")
def sc4s_docker_compose(
    request, docker_services, splunk, tmp_path_factory
):
    """

    sc4s docker depends on lovely-pytest-docker to create the docker instance
    of Splunk this may be changed in the future.
    docker-compose.yml in the project root must have
    a service "sc4s" exposing multiple ports

    Returns:
        class: Details of the sc4s instance including host, port, username & password.
    """
    LOGGER.info("Starting docker_service=sc4s")
    fn = os.path.join(tmp_path_factory.getbasetemp().parent,
                      "pytest_splunk_env_docker_compose.lock")

    with FileLock(str(fn)):
        return SC4SEnvDockerCompose(
            docker_services,
            splunk
        )


@pytest.fixture(scope="session")
def sc4s_docker(
    request, docker_services, docker_compose_files, splunk, tmp_path_factory, worker_id
):
    """
    Splunk docker depends on lovely-pytest-docker to create the docker instance
    of Splunk this may be changed in the future.
    docker-compose.yml in the project root must have
    a service "splunk" exposing port 8000 and 8089

    Returns:
        dict: Details of the splunk instance including host, port, username & password.
    """
    LOGGER.info("Starting docker=sc4s")
    fn = os.path.join(tmp_path_factory.getbasetemp().parent,
                      "pytest_splunk_env_docker.lock")
    raise Exception


@pytest.fixture(scope="session")
def sc4s_external(request, splunk):
    """
    This fixture provides the connection properties to Splunk based on the pytest args

    Returns:
        dict: Details of the splunk instance including host, port, username & password.
    """
    LOGGER.info("Checking Splunk")
    return EnvExternal(
        search_index=request.config.getoption("search_index"),
        search_retry=request.config.getoption("search_retry"),
        search_interval=request.config.getoption("search_interval"),
        splunkd_host=request.config.getoption("splunk_host"),
        splunkd_port=request.config.getoption("splunkd_port"),
        web_port=request.config.getoption("splunk_web"),
        username=request.config.getoption("splunk_user"),
        password=request.config.getoption("splunk_password"),
        hec_token=request.config.getoption(
            "splunk_hec_token"),

    )


@pytest.fixture(scope="session")
def sc4s_local(request):
    """
    This fixture provides the connection properties to Splunk based on the pytest args

    Returns:
        dict: Details of the splunk instance including host, port, username & password.
    """
    LOGGER.info("Checking Splunk")
    return SplunkEnvLocal(
        search_index=request.config.getoption("search_index"),
        search_retry=request.config.getoption("search_retry"),
        search_interval=request.config.getoption("search_interval"),
        username=request.config.getoption("splunk_user"),
        password=request.config.getoption("splunk_password"),
        hec_token=request.config.getoption(
            "splunk_hec_token"),

    )
