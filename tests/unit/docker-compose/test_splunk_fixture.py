import pytest
import pathlib
import os
import shutil



def setup_test_dir(testdir):
    shutil.copytree(
        os.path.join(testdir.request.config.invocation_dir, "deps"),
        os.path.join(testdir.tmpdir, "deps"),
    )

    shutil.copytree(
        os.path.join(testdir.request.config.invocation_dir, "tests/addons"),
        os.path.join(testdir.tmpdir, "tests/addons"),
    )

    shutil.copy(
        os.path.join(testdir.request.config.invocation_dir, "tests/conftest.py"),
        os.path.join(testdir.tmpdir, ""),
    )

    shutil.copy(
        os.path.join(testdir.request.config.invocation_dir, "Dockerfile.splunk"),
        testdir.tmpdir,
    )
    shutil.copy(
        os.path.join(testdir.request.config.invocation_dir, "Dockerfile.tests"),
        testdir.tmpdir,
    )

    shutil.copy(
        os.path.join(testdir.request.config.invocation_dir, "docker-compose.yml"),
        testdir.tmpdir,
    )

def test_splunk_fixture_compose(request,testdir):

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
