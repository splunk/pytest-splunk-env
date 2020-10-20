# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import pytest
import os
from .base import SC4SEnv
from .external import SC4SEnvExternal
import splunklib.client as client
import logging
LOGGER = logging.getLogger(__name__)


class SC4SEnvDockerCompose(SC4SEnvExternal):

    def __init__(self,
                 docker_services, splunk
                 ):

        # Env vars are used to pass config to splunk
        os.environ["SPLUNK_HEC_TOKEN"] = splunk.hec_token

        self.docker_services = docker_services
        self.docker_services.start("sc4s")

        super().__init__(
            splunk,
            sc4s_host="sc4s"
        )

    def port_for(self, service, port, udp=False):
        """Get the effective bind port for a service."""

        # Lookup in the cache.
        #cache = self.docker_services._services.get(service, {}).get(port, None)
        # if cache is not None:
        #    return cache
        if udp:
            output = self.docker_services._docker_compose.execute(
                'port', '--protocol=udp', service, str(port)
            )
        else:
            output = self.docker_services._docker_compose.execute(
                'port', service, str(port)
            )
        endpoint = output.strip()
        if not endpoint:
            raise ValueError(
                'Could not detect port for "%s:%d".' % (service, port)
            )

        # Usually, the IP address here is 0.0.0.0, so we don't use it.
        match = int(endpoint.split(':', 1)[1])

        # Store it in cache in case we request it multiple times.
        #self._services.setdefault(service, {})[port] = match

        return match

    def get_service(self, port, udp=False):
        real_ip = self.docker_services.docker_ip
        real_port = self.port_for("sc4s", port, udp)
        return real_ip, real_port
