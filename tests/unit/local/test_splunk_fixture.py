import pytest
import pathlib

def test_splunk_fixture_local(request,testdir):

    testdir.makepyfile(
        """
        import pytest

        def test_splunk_no_params(splunk):
            assert True
""")
    result = testdir.runpytest("--splunk-type=local")
    result.assert_outcomes(passed=1)
