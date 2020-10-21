# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

import pytest
import pathlib
import logging

def test_splunk_fixture_external(request, caplog,testdir):
    caplog.set_level(logging.INFO)    
    testdir.makepyfile(
        """
        import pytest

        def test_splunk_no_params(splunk_setup):
            assert True
""")
    result = testdir.runpytest(
        "--splunk-type=external",
        "--splunk-host=splunk",
        "--sc4s-type=external",
        "--sc4s-host=sc4s"
        )
    # we should have two passed tests and one failed (unarametrized one)
    result.assert_outcomes(passed=1)
