# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

"""
@author: Nicklas Ansman-Giertz
@contact: U{ngiertz@splunk.com<mailto:ngiertz@splunk.com>}
@since: 2011-11-23
"""
from abc import ABCMeta

from future.utils import with_metaclass

from pytest_splunk_env.splunk.helmut.log import Logging


class ItemFromManager(with_metaclass(ABCMeta, Logging)):
    def __init__(self, connector):
        self._connector = connector
        Logging.__init__(self)

    @property
    def connector(self):
        return self._connector
