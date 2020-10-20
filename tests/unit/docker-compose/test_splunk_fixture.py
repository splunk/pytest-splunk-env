from utils import *
import logging
def test_splunk_fixture_compose(request,testdir,caplog):
    caplog.set_level(logging.INFO)
    setup_test_dir(testdir)
    testdir.makepyfile(
        """
        import pytest

        def test_splunk_no_params(splunk):
            assert True
""")
    
    #result = testdir.runpytest("--splunk-type=docker-compose","--keepalive")
    result = testdir.runpytest("--splunk-type=docker-compose")
    result.assert_outcomes(passed=1)

def test_splunk_fixture_compose_7_3_7(request,testdir):
    
    setup_test_dir(testdir)
    testdir.makepyfile(
        """
        import pytest

        def test_splunk_no_params(splunk):
            assert True

        
""")
    
    #result = testdir.runpytest("--splunk-type=docker-compose","--keepalive")
    result = testdir.runpytest("--splunk-type=docker-compose","--splunk-version=7.3.7")
    result.assert_outcomes(passed=1)

def test_splunk_fixture_compose_6_0_0(request,testdir):
    
    setup_test_dir(testdir)
    testdir.makepyfile(
        """
        import pytest

        def test_splunk_no_params(splunk):
            assert True
""")
    
    #result = testdir.runpytest("--splunk-type=docker-compose","--keepalive")
    result = testdir.runpytest("--splunk-type=docker-compose","--splunk-version=600")
    result.assert_outcomes(passed=0,errors=1)
