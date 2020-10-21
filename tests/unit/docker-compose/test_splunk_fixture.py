# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

from utils import *
import logging
import configparser


def pytest_generate_tests(metafunc):
    if "splunk_version" in metafunc.fixturenames:
        config = configparser.ConfigParser()
        config.read(
            'deps/build/addonfactory_test_matrix_splunk/splunk_matrix.conf')
        splunk_versions = []
        for v in config.sections():
            splunk_versions.append(config[v]['VERSION'])
        metafunc.parametrize("splunk_version", splunk_versions)


def test_splunk_fixture_compose(request, testdir, caplog, splunk_version):
    caplog.set_level(logging.INFO)
    setup_test_dir(testdir)
    testdir.makepyfile(
        f"""
        import pytest

        def test_splunk_no_params(splunk_setup):
            search = f"| search index=_internal version sourcetype=splunk_version VERSION={splunk_version}"
            result = splunk_setup.search_util.checkQueryCountIsGreaterThanZero(
                search, interval=1, retries=0
            )
            assert result
""")

    #result = testdir.runpytest("--splunk-type=docker-compose","--keepalive")
    result = testdir.runpytest(
        "--splunk-type=docker-compose", f"--splunk-version={splunk_version}")
    result.assert_outcomes(passed=1)


def test_splunk_fixture_compose_bad_splunk_version(request, testdir):

    setup_test_dir(testdir)
    testdir.makepyfile(
        """
        import pytest

        def test_splunk_no_params(splunk_setup):
            #this should always error
            assert False
            
""")

    #result = testdir.runpytest("--splunk-type=docker-compose","--keepalive")
    result = testdir.runpytest(
        "--splunk-type=docker-compose", "--splunk-version=600")
    result.assert_outcomes(passed=0, errors=1)
