
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
                                          "splunk_version")
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
    return SplunkEnvExternal(
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
