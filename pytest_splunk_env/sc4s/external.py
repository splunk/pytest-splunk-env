# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import logging
import os

import pytest
import splunklib.client as client

from .base import SC4SEnv

LOGGER = logging.getLogger(__name__)


class SC4SEnvExternal(SC4SEnv):
    def __init__(self, splunk, sc4s_host):

        super().__init__(splunk, sc4s_host)
