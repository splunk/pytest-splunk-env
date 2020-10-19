

import pytest
from .base import SplunkEnv
from .external import SplunkEnvExternal
import logging
LOGGER = logging.getLogger(__name__)


class SplunkEnvDockerCompose(SplunkEnv):

    def __init__(self,
                docker_services,
                 search_index,
                 search_retry,
                 search_interval,
                 username,
                 password,
                 ):       

        docker_services.start("splunk")

        splunk_info = {
            "host": docker_services.docker_ip,
            "port": docker_services.port_for("splunk", 8089),
            "port_hec": docker_services.port_for("splunk", 8088),
            "port_s2s": docker_services.port_for("splunk", 9997),
            "port_web": docker_services.port_for("splunk", 8000),
            "username": request.config.getoption("splunk_user"),
            "password": request.config.getoption("splunk_password"),
        }

        #splunk_info["forwarder_host"] = splunk_info.get("host")

        LOGGER.info(
            "Docker container splunk info. host=%s, port=%s, port_web=%s port_hec=%s port_s2s=%s",
            docker_services.docker_ip,
            docker_services.port_for("splunk", 8089),
            docker_services.port_for("splunk", 8088),
            docker_services.port_for("splunk", 8000),
            docker_services.port_for("splunk", 9997),
        )

        docker_services.wait_until_responsive(
            timeout=180.0, pause=0.5, check=lambda: self.is_responsive_splunk(splunk_info),
        )

        super().__init__(
            search_index,
            search_retry,
            search_interval,
            splunkd_host="splunk",
            splunkd_port="8089",
            splunk_web="8000",
            username=username,
            password=password
        )
