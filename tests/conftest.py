import os, shutil
import pytest
import json
from .utils import dss


from dsclient import DebugServer, DebugSession

SETUP_FILE = os.path.join(os.path.dirname(__file__), "setup.json")

# parametrize tenv fixture with each test setup
def pytest_generate_tests(metafunc):
    with open(SETUP_FILE, 'r') as f:
        tsetup = json.load(f)
    if "tdevice" in metafunc.fixturenames:
        tdevices = [ tsetup[dev] for dev in tsetup['devices'] ]
        metafunc.parametrize("tdevice", tdevices, scope="class")

@pytest.fixture(scope="class")
def tenv(request):
    """Fixture for accessing paths set in setup.json file"""
    with open(SETUP_FILE, 'r') as f:
        tsetup = json.load(f)

    return tsetup['paths']


@pytest.fixture(autouse=True, scope="class")
def test_env_setup(request, tenv):
    os.makedirs(tenv["tmp"])

    def teardown():
        shutil.rmtree(tenv["tmp"])

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def pid_and_port(request, tenv):
    """Launches DS server and returns process handle and port number"""
    p, port = dss.launch_server(tenv["ccs"], tenv["workspace"])

    def teardown():
        p.terminate()

    request.addfinalizer(teardown)

    return (p, port)


@pytest.fixture(scope="function")
def debug_server(request, tenv):
    """An instantiated DebugServer object"""
    p, port = dss.launch_server(tenv["ccs"], tenv["workspace"])
    DS = DebugServer(port=port)

    def teardown():
        p.terminate()

    request.addfinalizer(teardown)

    return DS


@pytest.fixture(scope="function")
def debug_session(request, debug_server, tenv, tdevice):
    """An instantiated DebugSession object"""
    session_name = tdevice["session"]

    debug_server.set_config(tdevice["ccxml-path"])
    ds = debug_server.open_session(session_name)

    def teardown():
        ds.stop()

    request.addfinalizer(teardown)

    return ds
