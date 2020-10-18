import pytest
import pathlib


def setup_test_dir(testdir):
    shutil.copytree(
        os.path.join(testdir.request.config.invocation_dir, "deps"),
        os.path.join(testdir.tmpdir, "deps"),
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


def test_splunk_fixture(request,testdir):

    testdir.makepyfile(
        """
        import pytest

        def test_splunk_no_params(request,splunk):
            assert True
""")
    setup_test_dir(testdir)
    result = testdir.runpytest("--splunk-type=docker-compose")
    # we should have two passed tests and one failed (unarametrized one)
    result.assert_outcomes(passed=1)
