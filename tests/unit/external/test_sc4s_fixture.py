# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

from utils import *
import logging


def test_sc4s_fixture_compose(request, testdir, caplog):
    caplog.set_level(logging.INFO)
    setup_test_dir(testdir)
    testdir.makepyfile(
        """
        import pytest

        def test_sc4s_no_params(splunk_setup, sc4s):
            assert True

        def test_sc4s_mapped_port(splunk_setup, sc4s):
            ip,tcp = sc4s.get_service(514)
            assert  tcp != "514"
            ip,udp = sc4s.get_service(514,True)
            assert  udp != "514"
            assert tcp != udp
""")

    result = testdir.runpytest(
        "--splunk-type=external",
        f'--splunk-host={request.config.getoption("test_splunk_host")}',
        "--sc4s-type=external",
        f'--sc4s-host={request.config.getoption("test_sc4s_host")}'
       )
    result.assert_outcomes(passed=2)
