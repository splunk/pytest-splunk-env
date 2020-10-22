# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import logging
from filelock import FileLock
import os
import pytest

from .base import SplunkEnv
from .docker import splunk_docker
from .external import SplunkEnvExternal
from .local import SplunkEnvLocal
from .dockercompose import SplunkEnvDockerCompose
LOGGER = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add options for interaction with Splunk this allows the tool to work in two modes
    1) docker mode which is typically used by developers on their workstation
        manages a single instance of splunk
    2) external interacts with a single instance of splunk that is lifecycle managed
        by another process such as a ci/cd pipeline
    """

    group = parser.getgroup("splunk-env")

    group.addoption(
        "--splunk-app",
        action="store",
        dest="splunk_app",
        default="package",
        help=(
            "Path to Splunk app package. The package should have the "
            "configuration files in the default folder."
        ),
    )
    group.addoption(
        "--splunk-type",
        action="store",
        dest="splunk_type",
        default="external",
        help=(
            "Type of the Splunk instance. supports external & docker "
            "as a value. Default is external."
        ),
    )
    group.addoption(
        "--splunk-host",
        action="store",
        dest="splunk_host",
        default="127.0.0.1",
        help=(
            "Address of the Splunk Server where search queries will be executed. Do not provide "
            "http scheme in the host. default is 127.0.0.1"
        ),
    )
    group.addoption(
        "--splunk-forwarder-host",
        action="store",
        dest="splunk_forwarder_host",        
        help=(
            "Address of the Splunk Forwarder Server. Do not provide "
            "http scheme in the host."
        ),
    )
    group.addoption(
        "--splunk-hec-scheme",
        action="store",
        dest="splunk_hec_scheme",
        default="https",
        help="Splunk HTTP event collector port. default is https.",
    )
    group.addoption(
        "--splunk-hec-port",
        action="store",
        dest="splunk_hec",
        default="8088",
        help="Splunk HTTP event collector port. default is 8088.",
    )
    group.addoption(
        "--splunk-hec-token",
        action="store",
        dest="splunk_hec_token",
        default="9b741d03-43e9-4164-908b-e09102327d22",
        help='Splunk HTTP event collector token. default is "9b741d03-43e9-4164-908b-e09102327d22" If an external forwarder is used provide HEC token of forwarder.',
    )
    group.addoption(
        "--splunk-port",
        action="store",
        dest="splunkd_port",
        default="8089",
        help="Splunk Management port. default is 8089.",
    )
    group.addoption(
        "--splunk-s2s-port",
        action="store",
        dest="splunk_s2s",
        default="9997",
        help="Splunk s2s port. default is 9997.",
    )
    group.addoption(
        "--splunk-s2s-scheme",
        action="store",
        dest="splunk_s2s_scheme",
        default="tcp",
        help="Splunk s2s scheme. tls|tcp default is tcp.",
    )
    group.addoption(
        "--splunkweb-port",
        action="store",
        dest="splunk_web",
        default="8000",
        help="Splunk web port. default is 8000.",
    )
    group.addoption(
        "--splunk-user",
        action="store",
        dest="splunk_user",
        default="admin",
        help="Splunk login user. The user should have search capabilities.",
    )
    group.addoption(
        "--splunk-password",
        action="store",
        dest="splunk_password",
        default="Chang3d!",
        help="Password of the Splunk user",
    )
    group.addoption(
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
    group.addoption(
        "--search-index",
        action="store",
        dest="search_index",
        default="*",
        help="Splunk index of which the events will be searched while testing.",
    )
    group.addoption(
        "--search-retry",
        action="store",
        dest="search_retry",
        default=0,
        type=int,
        help="Number of retries to make if there are no events found while searching in the Splunk instance.",
    )
    group.addoption(
        "--search-interval",
        action="store",
        dest="search_interval",
        default=0,
        type=int,
        help="Time interval to wait before retrying the search query.",
    )

@pytest.fixture(scope="session")
def splunk(request):
    """
    This fixture based on the passed option will provide a real fixture
    for external or docker Splunk

    Returns:
        dict: Details of the splunk instance including host, port, username & password.
    """
    splunk_type = request.config.getoption("splunk_type")
    LOGGER.info("Get the Splunk instance of splunk_type=%s", splunk_type)

    if splunk_type == "external":
        fixture = "splunk_external"
    elif splunk_type == "local":
        fixture = "splunk_local"
    elif splunk_type == "docker":
        fixture = "splunk_docker"
    elif splunk_type == "docker-compose":
        fixture = "splunk_docker_compose"
    else:
        raise Exception
    request.fixturenames.append(fixture)
    splunk = request.getfixturevalue(fixture)

    yield splunk


@pytest.fixture(scope="session")
def splunk_docker_compose(
    request, docker_services, tmp_path_factory
):
    """

    Splunk docker depends on lovely-pytest-docker to create the docker instance
    of Splunk this may be changed in the future.
    docker-compose.yml in the project root must have
    a service "splunk" exposing port 8000 and 8089

    Returns:
        dict: Details of the splunk instance including host, port, username & password.
    """
    LOGGER.info("Starting docker_service=splunk")
    fn = os.path.join(tmp_path_factory.getbasetemp().parent,
                      "pytest_splunk_env_docker_compose.lock")

    with FileLock(str(fn)):
        return SplunkEnvDockerCompose(docker_services, search_index=request.config.getoption("search_index"),
                                      search_retry=request.config.getoption(
                                          "search_retry"),
                                      search_interval=request.config.getoption(
                                          "search_interval"),
                                      username=request.config.getoption(
                                          "splunk_user"),
                                      password=request.config.getoption(
                                          "splunk_password"),
                                      hec_token=request.config.getoption(
                                          "splunk_hec_token"),
                                      splunk_version=request.config.getoption(
                                          "splunk_version"),
                                      splunk_app=request.config.getoption(
                                          "splunk_app")
                                      )


@pytest.fixture(scope="session")
def splunk_docker(
    request, docker_services, docker_compose_files, tmp_path_factory, worker_id
):
    """
    Splunk docker depends on lovely-pytest-docker to create the docker instance
    of Splunk this may be changed in the future.
    docker-compose.yml in the project root must have
    a service "splunk" exposing port 8000 and 8089

    Returns:
        dict: Details of the splunk instance including host, port, username & password.
    """
    LOGGER.info("Starting docker=splunk")
    fn = os.path.join(tmp_path_factory.getbasetemp().parent,
                      "pytest_splunk_env_docker.lock")
    raise Exception


@pytest.fixture(scope="session")
def splunk_external(request):
    """
    This fixture provides the connection properties to Splunk based on the pytest args

    Returns:
        dict: Details of the splunk instance including host, port, username & password.
    """
    LOGGER.info("Checking Splunk")
    if not request.config.getoption("splunk_forwarder_host"):
        forwarder_host = request.config.getoption("splunk_host")
    else:
        forwarder_host = request.config.getoption("splunk_forwarder_host")

    return SplunkEnvExternal(
        search_index=request.config.getoption("search_index"),
        search_retry=request.config.getoption("search_retry"),
        search_interval=request.config.getoption("search_interval"),
        splunkd_host=request.config.getoption("splunk_host"),
        splunkd_port=request.config.getoption("splunkd_port"),
        web_port=request.config.getoption("splunk_web"),
        username=request.config.getoption("splunk_user"),
        password=request.config.getoption("splunk_password"),
        hec_scheme=request.config.getoption("splunk_hec_scheme"),
        hec_host=forwarder_host,
        hec_port=request.config.getoption("splunk_hec"),
        hec_validate=False,
        hec_token=request.config.getoption(
            "splunk_hec_token"),

    )


@pytest.fixture(scope="session")
def splunk_local(request):
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


@pytest.fixture(scope="session")
def splunk_setup(splunk):
    """
    Override this fixture in conftest.py, if any setup is required before the test session.
    splunk fixture can provide the details of the splunk instance in dict format.

    **Possible setups required**:

        1. Enable Saved-searches before running the tests
        2. Restart Splunk
        3. Configure inputs of an Add-on.

    **Example**::

        import pytest

        from splunklib import binding, client, results
        import time
        import os

        class TASetup(object):
            def __init__(self, splunk):
                self.splunk = splunk

            def wait_for_lookup(self, lookup):
                search = f" | inputlookup {{lookup}}"
                result = self.splunk.search_util.checkQueryCountIsGreaterThanZero(
                    search, interval=1, retries=90
                )
                if not result:
                    raise Exception()

            def enable_savedsearch(self, addon_name, savedsearch):
                splunk_binding = binding.connect(
                    username=self.splunk.username,
                    password=self.splunk.password,
                    host=self.splunk.splunkd_host,
                    port=self.splunk.splunkd_port,
                )
                splunk_binding.post(
                    f"/servicesNS/nobody/{{addon_name}}/saved/searches/{{savedsearch}}/enable"
                    , data=''
                )

        @pytest.fixture(scope="session")
        def splunk_setup(splunk):
            ta_setup = TASetup(splunk)
            ta_setup.enable_savedsearch("TA_SavedSearch", "ta_saved_search_one")
            ta_setup.wait_for_lookup("ta_saved_search_lookup")
            return splunk


        def test_splunk_no_params(splunk_setup):
            search = f"| search index=_internal version sourcetype=splunk_version VERSION={splunk_version}"
            result = splunk_setup.search_util.checkQueryCountIsGreaterThanZero(
                search, interval=1, retries=0
            )
            assert result

    """
    return splunk
