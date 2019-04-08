import os
import pytest
from dsclient import DebugServer, DebugSession


class TestDebugSession(object):
    @pytest.mark.dependency(name="TestDebugSession::test_connect")
    def test_connect(self, debug_session):
        """Tests connecting to device"""
        debug_session.connect()

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_disconnect(self, debug_session):
        """Tests disconnecting from device"""
        debug_session.connect()

        debug_session.disconnect()

    def test_fail_disconnect_when_not_connected(self, debug_session):
        """Tests disconnecting from device"""
        with pytest.raises(Exception):
            debug_session.disconnect()

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_erase(self, debug_session):
        """Tests erasing device's flash"""
        debug_session.connect()

        debug_session.erase()

    def test_fail_erase_when_not_connected(self, debug_session):
        """Tests fails to erase device's flash when device is not connected"""
        with pytest.raises(Exception):
            debug_session.erase()

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_reset(self, debug_session):
        """Tests resetting device"""
        debug_session.connect()

        debug_session.reset()

    def test_fail_reset_when_not_connected(self, debug_session):
        """Tests fails to reset device when device is not connected"""
        with pytest.raises(Exception):
            debug_session.reset()

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_load(self, debug_session, tdevice):
        """Tests loading image into device's flash"""
        debug_session.connect()

        debug_session.load(tdevice["hex-image"])

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_load_binary(self, debug_session, tdevice):
        """Tests loading binary image into device's flash"""
        debug_session.connect()

        debug_session.load(tdevice["binary-image"], binary=True)

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    @pytest.mark.skip(reason="Need to find safe address to flash image at")
    def test_load_binary_at_address(self, debug_session, tdevice):
        """Tests loading binary image into device's flash"""
        debug_session.connect()

        debug_session.load(tdevice["binary-image"], binary=True, address=0x100)

    def test_fail_load_when_not_connected(self, debug_session, tdevice):
        """Tests fails to load image into device's flash when device is not connected"""
        with pytest.raises(Exception):
            debug_session.load(tdevice["hex-image"])

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_verify(self, debug_session, tdevice):
        """Tests verifying image in device's flash"""
        debug_session.connect()

        debug_session.verify(tdevice["hex-image"])

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    @pytest.mark.xfail
    def test_verify_binary(self, debug_session, tdevice):
        """Tests verifying binary image in device's flash"""
        debug_session.connect()

        debug_session.verify(tdevice["binary-image"], binary=True)

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    @pytest.mark.skip(reason="Need to find safe address to flash image at")
    def test_verify_binary_at_address(self, debug_session, tdevice):
        """Tests verifying binary image in device's flash"""
        debug_session.connect()

        debug_session.verify(tdevice["binary-image"], binary=True, address=0x100)

    def test_fail_verify_when_not_connected(self, debug_session, tdevice):
        """Tests fails to verify image in device's flash when device is not connected"""
        with pytest.raises(Exception):
            debug_session.verify(tdevice["hex-image"])

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_evaluate(self, debug_session, tdevice):
        """Tests evaluating an expression"""
        debug_session.connect()

        result = debug_session.evaluate(tdevice["expression"])

        assert type(result) == int

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_evaluate_with_symbols_file(self, debug_session, tdevice):
        """Tests evaluating an expression after loading symbols file"""
        debug_session.connect()

        result = debug_session.evaluate(tdevice["symbol"], file=tdevice["symbol-image"])

        assert type(result) == int

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_evaluate_with_invalid_expression(self, debug_session, tdevice):
        """Tests failing when evaluating an invalid expression"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.evaluate("&madeUpExpression", file=tdevice["symbol-image"])

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_read_data(self, debug_session, tdevice):
        """Tests reading data from device's memory"""
        debug_session.connect()

        result = debug_session.read_data(
            page=0, address=int(tdevice["address"], 16), num_bytes=4
        )

        assert type(result) == list
        assert len(result) == 4

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_read_data_invalid_address(self, debug_session):
        """Tests fails when reading data from invalid address in device's memory"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.read_data(page=0, address=0xFFFFFFFFF, num_bytes=4)

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_write_data(self, debug_session, tdevice):
        """Tests writing data to device's memory"""
        debug_session.connect()

        debug_session.write_data(
            data=[0xFF, 0xFF], page=0, address=int(tdevice["address"], 16)
        )

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_write_data_invalid_address(self, debug_session):
        """Tests fails when reading data from invalid address in device's memory"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.write_data(data=[0xFF, 0xFF], page=0, address=0x10000000)

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_read_register(self, debug_session):
        """Tests reading register value of device"""
        debug_session.connect()

        result = debug_session.read_register("PC")

        assert type(result) == int

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_read_register(self, debug_session):
        """Tests fails when reading value of invalid register"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.read_register("INVALIDREG")

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_write_register(self, debug_session):
        """Tests writing value to device's register"""
        debug_session.connect()

        result = debug_session.write_register("R1", 0xBEEF)

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_write_register(self, debug_session):
        """Tests fails when writing value to invalid register"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.write_register("INVALIDREG", 0xBEEF)

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_get_option(self, debug_session, tdevice):
        """Tests getting value of device option"""
        debug_session.connect()

        result = debug_session.get_option(tdevice["option"])
        assert result == False

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_get_option_invalid_id(self, debug_session):
        """Tests fails when getting value of an invalid option"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.get_option("InvalidOption")

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_set_option(self, debug_session, tdevice):
        """Tests setting value of device option"""
        debug_session.connect()

        debug_session.set_option(tdevice["option"], True)

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_set_option_invalid_id(self, debug_session):
        """Tests fails when setting value of an invalid option"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.set_option("InvalidOption", True)

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_set_option_invalid_value(self, debug_session, tdevice):
        """Tests fails when setting invalid value of an option"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.set_option(tdevice["option"], "ShouldBeBoolean")

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_perform_operation(self, debug_session, tdevice):
        """Tests performing a device operation"""
        debug_session.connect()

        debug_session.perform_operation(tdevice["opcode"])

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_fail_perform_operation_invalid_opcode(self, debug_session):
        """Tests fails when performing an invalid operation"""
        debug_session.connect()

        with pytest.raises(Exception):
            debug_session.perform_operation("InvalidOpCode")

    @pytest.mark.dependency(
        name="TestDebugSession::test_run_with_async",
        depends=["TestDebugSession::test_connect"],
    )
    def test_run_with_async(self, debug_session):
        """Tests running the target asynchronously"""
        debug_session.connect()

        debug_session.run(asynchronous=True)

    @pytest.mark.dependency(
        name="TestDebugSession::test_halt", depends=["TestDebugSession::test_connect"]
    )
    def test_halt(self, debug_session):
        """Tests halting the device"""
        debug_session.connect()

        debug_session.halt()

    @pytest.mark.dependency(depends=["TestDebugSession::test_connect"])
    def test_halt_and_wait(self, debug_session):
        """Tests halting the device and waiting until halted"""
        debug_session.connect()

        debug_session.halt(wait=True)

    @pytest.mark.dependency(
        depends=[
            "TestDebugSession::test_connect",
            "TestDebugSession::test_run_with_async",
            "TestDebugSession::test_halt",
        ]
    )
    def test_run_and_halt(self, debug_session):
        """Tests running the device and then halting it"""
        debug_session.connect()

        debug_session.run(asynchronous=True)

        debug_session.halt(wait=True)
