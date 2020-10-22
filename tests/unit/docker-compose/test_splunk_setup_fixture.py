# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

from utils import *
import logging
import configparser
from splunklib import binding


def test_splunk_setup_fixture_compose(request, testdir, caplog, splunk_version):
    caplog.set_level(logging.INFO)
    setup_test_dir(testdir)

    testdir.makepyfile(
        f"""
        import pytest

        from splunklib import binding, client, results
        import time
        import os

        class TASetup(object):
            def __init__(self, splunk):
                self.splunk = splunk

            def wait_for_lookup(self, lookup):
                search = f" | inputlookup {{lookup}}"
                result = self.splunk.search_util.checkQueryCountIsGreaterThanZero(
                    search, interval=1, retries=90
                )
                if not result:
                    raise Exception()

            def enable_savedsearch(self, addon_name, savedsearch):
                splunk_binding = binding.connect(
                    username=self.splunk.username,
                    password=self.splunk.password,
                    host=self.splunk.splunkd_host,
                    port=self.splunk.splunkd_port,
                )
                splunk_binding.post(
                    f"/servicesNS/nobody/{{addon_name}}/saved/searches/{{savedsearch}}/enable"
                    , data=''
                )



        @pytest.fixture(scope="session")
        def splunk_setup(splunk):
            ta_setup = TASetup(splunk)
            ta_setup.enable_savedsearch("TA_SavedSearch", "ta_saved_search_one")
            ta_setup.wait_for_lookup("ta_saved_search_lookup")
            return splunk


        def test_splunk_no_params(splunk_setup):
            search = f"| search index=_internal version sourcetype=splunk_version VERSION={splunk_version}"
            result = splunk_setup.search_util.checkQueryCountIsGreaterThanZero(
                search, interval=1, retries=0
            )
            assert result
""")

    #result = testdir.runpytest("--splunk-type=docker-compose","--keepalive")
    result = testdir.runpytest(
        "--splunk-type=docker-compose",
        f"--splunk-version={splunk_version}",
        "--splunk-app=tests/addons/TA_SavedSearch",
        
        )
    result.assert_outcomes(passed=1)