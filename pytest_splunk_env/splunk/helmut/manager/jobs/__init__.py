# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

"""
@author: Nicklas Ansman-Giertz
@contact: U{ngiertz@splunk.com<mailto:ngiertz@splunk.com>}
@since: 2011-11-23
"""
from abc import abstractmethod

from pytest_splunk_env.splunk.helmut.manager import Manager
from pytest_splunk_env.splunk.helmut.misc.collection import Collection
from pytest_splunk_env.splunk.helmut.misc.manager_utils import (
    create_wrapper_from_connector_mapping,
)

PATH_PERFIX = "/servicesNS/nobody/system/search/jobs/"
EVENTS = "/events"
RESULTS = "/results"
SUMMARY = "/summary"
CONTROL = "/control"
RESULTS_PREVIEW = "/results_preview"
TIMELINE = "/timeline"
SEARCHLOG = "/search.log"


class Jobs(Manager, Collection):
    """
    Jobs is the manager that handles searches.
    It does not handle pausing, resuming, etc of individual searches, it just
    spawns and lists searches.
    """

    def __init__(self, connector):
        Manager.__init__(self, connector)
        Collection.__init__(self)

    def __new__(cls, connector):
        mappings = _CONNECTOR_TO_WRAPPER_MAPPINGS
        return create_wrapper_from_connector_mapping(cls, connector, mappings)

    @abstractmethod
    def create(self, query, **kwargs):
        pass

    @abstractmethod
    def __getitem__(self, sid):
        pass


class JobNotFound(RuntimeError):
    def __init__(self, sid):
        self.sid = sid
        super().__init__(self._error_message)

    @property
    def _error_message(self):
        return f"Could not find a job with SID {self.sid}"


# We need this at the bottom to avoid cyclic imports

from pytest_splunk_env.splunk.helmut.connector.rest import RESTConnector
from pytest_splunk_env.splunk.helmut.connector.sdk import SDKConnector
from pytest_splunk_env.splunk.helmut.manager.jobs.rest import RESTJobsWrapper
from pytest_splunk_env.splunk.helmut.manager.jobs.sdk import SDKJobsWrapper

_CONNECTOR_TO_WRAPPER_MAPPINGS = {
    SDKConnector: SDKJobsWrapper,
    RESTConnector: RESTJobsWrapper,
}
