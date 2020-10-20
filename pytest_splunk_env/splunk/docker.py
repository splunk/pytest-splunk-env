# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from .base import SplunkEnv
import logging
LOGGER = logging.getLogger(__name__)


class splunk_docker(SplunkEnv):
    this = "that"
