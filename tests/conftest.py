# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import pytest
import os
pytest_plugins = ["pytester"]


@pytest.fixture(scope='session')
def docker_compose_files(pytestconfig):
    """Get the docker-compose.yml absolute path.
    Override this fixture in your tests if you need a custom location.
    """
    return [
        os.path.join(str(pytestconfig.rootdir), 'docker-compose.yml')
    ]
