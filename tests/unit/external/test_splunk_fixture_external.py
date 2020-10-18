import pytest
import pathlib

def test_splunk_fixture(request,testdir):

    testdir.makepyfile(
        """
        import pytest

        def test_splunk_no_params(splunk):
            assert True
""")
    result = testdir.runpytest("--splunk-type=external")
    # we should have two passed tests and one failed (unarametrized one)
    result.assert_outcomes(passed=1)
