import os, shutil
import pytest
from .utils.setupparser import get_enabled_setups, get_setup_env
from .utils import dss

from dsclient import DebugServer, DebugSession

SETUP_FILE = os.path.join(os.path.dirname(__file__), "setup.cfg")

# parametrize tenv fixture with each test setup
def pytest_generate_tests(metafunc):
    if "tenv" in metafunc.fixturenames:
        enabled_setups = get_enabled_setups(SETUP_FILE)
        tenv_list = [get_setup_env(SETUP_FILE, envname) for envname in enabled_setups]
        metafunc.parametrize("tenv", tenv_list, scope="class")


@pytest.fixture(autouse=True, scope="class")
def test_env_setup(request, tenv):
    os.makedirs(tenv["tmp"])

    def teardown():
        shutil.rmtree(tenv["tmp"])

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def pid_and_port(request, tenv):
    """Launches DS server and returns process handle and port number"""
    p, port = dss.launch_server(tenv["ccs-exe"], tenv["workspace"])

    def teardown():
        p.terminate()

    request.addfinalizer(teardown)

    return (p, port)


@pytest.fixture(scope="function")
def debug_server(request, tenv):
    """An instantiated DebugServer object"""
    p, port = dss.launch_server(tenv["ccs-exe"], tenv["workspace"])
    DS = DebugServer(port=port)

    def teardown():
        p.terminate()

    request.addfinalizer(teardown)

    return DS


@pytest.fixture(scope="function")
def debug_session(request, debug_server, tenv):
    """An instantiated DebugSession object"""
    session_name = tenv["session"]

    debug_server.set_config(tenv["ccxml-path"])
    ds = debug_server.open_session(session_name)

    def teardown():
        ds.stop()

    request.addfinalizer(teardown)

    return ds
