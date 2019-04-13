import os
import time
import pytest
from dsclient import DebugServer, DebugSession


class Test_DebugServer:
    def test_DebugServer_instantiation(self, pid_and_port):
        """Tests instantiation of DebugServer object"""
        p, port = pid_and_port
        DS = DebugServer(port=port)

    def test_set_config(self, debug_server, tdevice):
        """Tests setting ccxml config file of DebugServer object"""
        debug_server.set_config(tdevice["ccxml-path"])

    def test_get_config_no_set(self, debug_server):
        """Tests setting ccxml config file of DebugServer object"""
        assert debug_server.get_config() is None

    def test_get_config_after_set(self, debug_server, tdevice):
        """Tests setting ccxml config file of DebugServer object"""
        debug_server.set_config(tdevice["ccxml-path"])
        assert debug_server.get_config() == tdevice["ccxml-path"]

    def test_basic_create_config(self, debug_server, tenv, tdevice):
        """Tests basic creation of ccxml file"""
        NAME = "BASIC.ccxml"
        CONNECTION = tdevice["connection"]
        DEVICE = tdevice["devicetype"]
        DIRECTORY = tenv["tmp"]
        resp = debug_server.create_config(
            NAME, connection=CONNECTION, device=DEVICE, directory=DIRECTORY
        )

        assert resp["name"] == NAME
        assert resp["directory"] == DIRECTORY
        assert os.path.exists(os.path.join(DIRECTORY, NAME))

    def test_fail_create_config_non_existant_directory(
        self, debug_server, tenv, tdevice
    ):
        """Tests basic creation of ccxml file"""
        NAME = "BASIC.ccxml"
        CONNECTION = tdevice["connection"]
        DEVICE = tdevice["devicetype"]
        DIRECTORY = os.path.join(tenv["workspace"], "NONEXISTANTDIR")
        with pytest.raises(Exception):
            resp = debug_server.create_config(
                NAME, connection=CONNECTION, device=DEVICE, directory=DIRECTORY
            )

    def test_get_list_of_cpus(self, debug_server, tdevice):
        """Tests listing of CPU names"""
        debug_server.set_config(tdevice["ccxml-path"])

        cpus = debug_server.get_list_of_CPUs()
        assert type(cpus) is list
        assert len(cpus) > 0

    def test_get_list_of_devices(self, debug_server, tdevice):
        """Tests listing of device names"""
        debug_server.set_config(tdevice["ccxml-path"])

        devices = debug_server.get_list_of_devices()
        assert type(devices) is list
        assert len(devices) > 0

    def test_get_list_of_connections(self, debug_server, tdevice):
        """Tests listing of connection names"""
        debug_server.set_config(tdevice["ccxml-path"])

        connections = debug_server.get_list_of_connections()
        assert type(connections) is list
        assert len(connections) > 0

    def test_get_list_of_configurations(self, debug_server, tdevice):
        """Tests listing of configurations files"""
        debug_server.set_config(tdevice["ccxml-path"])

        configurations = debug_server.get_list_of_configurations()
        assert type(configurations) is list
        # assert len(configurations) > 0

    def test_open_session(self, debug_server, tdevice):
        """Tests creation of DebugServer"""
        session_name = tdevice["session"]
        debug_server.set_config(tdevice["ccxml-path"])

        debug_session = debug_server.open_session(session_name)
        assert type(debug_session) == DebugSession

    def test_fail_open_existing_session(self, debug_server, tdevice):
        """Tests fails when trying to open existing session"""
        session_name = tdevice["session"]
        debug_server.set_config(tdevice["ccxml-path"])

        debug_session = debug_server.open_session(session_name)
        with pytest.raises(Exception):
            debug_session = debug_server.open_session(session_name)

    def test_get_list_of_open_sessions(self, debug_server, tdevice):
        """Tests getting dict of existing sessions"""
        session_name = tdevice["session"]
        debug_server.set_config(tdevice["ccxml-path"])

        debug_session = debug_server.open_session(session_name)
        session_list = debug_server.get_list_of_sessions()

        assert session_name in list(session_list.keys())
        assert session_list[session_name] is debug_session

    def test_get_list_of_open_sessions_with_no_open_sessions(
        self, debug_server, tdevice
    ):
        """Tests getting dict of existing sessions on a DebugServer with no open
        sessions"""
        debug_server.set_config(tdevice["ccxml-path"])

        session_list = debug_server.get_list_of_sessions()

        assert len(list(session_list.keys())) == 0

    def test_terminate_session(self, debug_server, tdevice):
        """Tests terminating a DebugSession"""
        session_name = tdevice["session"]
        debug_server.set_config(tdevice["ccxml-path"])

        debug_session = debug_server.open_session(session_name)
        debug_server.terminate_session(session_name)

    def test_attach_ccs(self, debug_server, tdevice):
        """Tests terminating a DebugSession"""
        session_name = tdevice["session"]
        debug_server.set_config(tdevice["ccxml-path"])

        debug_session = debug_server.open_session(session_name)
        debug_server.attach_ccs()
        time.sleep(10)
        debug_server.terminate_session(session_name)
