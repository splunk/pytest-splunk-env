# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0


from future import standard_library

standard_library.install_aliases()
import logging
import threading
import urllib.error
import urllib.parse
import urllib.request

from pytest_splunk_env.splunk.helmut.connector.base import Connector

LOGGER = logging.getLogger("rest util log")


class RestUtils(threading.Thread):
    def invoke_restAPI(
        self,
        splunk,
        appname="",
        arguments={"output_mode": "json"},
        request_type="GET",
        acl=None,
        splunk_user="",
        splunk_pwd="",
        request_url="/servicesNS/nobody/system/apps/local",
    ):
        LOGGER.info("Creating edit a saved search")
        if splunk_user == "":
            splunk_user = splunk.username
        if splunk_pwd == "":
            splunk_pwd = splunk.password

        if request_type == "POST":
            request_args = arguments

        if request_type == "UPDATE":
            request_type = "POST"
            request_url = request_url + "/" + appname
            request_args = arguments

        if request_type == "GET" or request_type == "DELETE":
            request_url = request_url + "/" + appname
            request_args = {"output_mode": "json"}
            response, content = self.make_http_request(
                splunk, request_type, request_url, request_args, splunk_user, splunk_pwd
            )

        response, content = self.make_http_request(
            splunk, request_type, request_url, request_args, splunk_user, splunk_pwd
        )

        if acl != None:
            acl_req_url = request_url + "/" + appname + "/acl"
            res, cont = self.make_http_request(
                splunk, request_type, acl_req_url, acl, splunk_user, splunk_pwd
            )

        return response, content

    def make_http_request(
        self,
        splunk,
        request_type,
        request_url,
        request_args="",
        splunk_user="",
        splunk_pwd="",
    ):
        """
        This is a REST helper that will generate a http request
        using request_type - GET/POST/...
        request_url and request_args
        """
        if splunk_user == "":
            splunk_user = splunk.username
        if splunk_pwd == "":
            splunk_pwd = splunk.password
        restconn = splunk.create_logged_in_connector(
            contype=Connector.REST, username=splunk_user, password=splunk_pwd
        )
        try:
            response, content = restconn.make_request(
                request_type, request_url, request_args
            )
            return response, content

        except urllib.error.HTTPError as err:
            print(
                "Http error code is ({}): {} : {}".format(
                    err.code, err.errno, err.strerror
                )
            )
        finally:
            restconn.logout()
