# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

"""
Module for handling generic connections with a Splunk instance.

@author: Nicklas Ansman-Giertz
@contact: U{ngiertz@splunk.com<mailto:ngiertz@splunk.com>}
@since: 2011-11-21
"""

__all__ = ["sdk", "rest"]

from .rest import RESTConnector
from .sdk import SDKConnector
