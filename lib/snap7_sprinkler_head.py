import snap7
from snap7.util import *
from lib.sprinkler_head_plc import SprinklerHeadPLC


class Snap7SprinklerHead(SprinklerHeadPLC):

    def __init__(self, db_number: int = 11):
        self._client = snap7.client.Client()
        self._db_number = db_number

    def _read(self, offset: int, size: int) -> bytearray:
        return self._client.db_read(self._db_number, offset, size)

    def _write(self, offset: int, data: bytearray):
        self._client.db_write(self._db_number, offset, data)

    def connect(self, address: str, rack: int, slot: int, port: int = 102) -> bool:
        error = self._client.connect(address, rack, slot, port)
        if error:
            print(self._client.error_text(error))
            return False
        return True

    def disconnect(self) -> bool:
        error = self._client.disconnect()
        if error:
            print(self._client.error_text(error))
            return False
        return True

    def is_connected(self) -> bool:
        return self._client.get_connected()

    def is_filter_clogged(self) -> bool:
        return get_bool(self._read(37, 1), 0, 0)

    def is_working_ph(self) -> bool:
        return get_bool(self._read(36, 1), 0, 4)

    def is_working_water_level(self) -> bool:
        return get_bool(self._read(36, 1), 0, 5)

    def is_working_salinity(self) -> bool:
        return get_bool(self._read(36, 1), 0, 6)

    def is_working_pressure(self) -> bool:
        return get_bool(self._read(36, 1), 0, 7)

    def is_working_flow(self) -> bool:
        return False

    def get_ph(self) -> float:
        return get_real(self._read(0, 4), 0)

    def get_salinity(self) -> float:
        return get_real(self._read(4, 4), 0)

    def get_pressure(self) -> float:
        return get_real(self._read(8, 4), 0)

    def get_water_level(self) -> float:
        return get_real(self._read(12, 4), 0)

    def get_flow(self) -> float:
        return 0

    def get_fertilizer_state(self, index: int) -> bool:
        if not (0 <= index <= 2):
            raise Exception("Invalid index")

        return get_bool(self._read(37, 1), 0, index + 1)

    def get_fertilizer_running_milliseconds(self, index: int) -> int:
        if not (0 <= index <= 2):
            raise Exception("Invalid index")

        return get_dint(self._read(24 + index * 4, 4), 0)

    def get_breaker_state(self, index: int) -> bool:
        if not (0 <= index <= 3):
            raise Exception("Invalid index")

        return get_bool(self._read(36, 1), 0, index)

    def get_breaker_off_count(self, index: int) -> int:
        if not (0 <= index <= 3):
            raise Exception("Invalid index")

        return get_int(self._read(16 + index * 4, 4), 0)

    def get_pump_state(self) -> bool:
        return get_bool(self._read(38, 1), 0, 4)

    def get_valve_state(self, index: int) -> bool:
        if not (0 <= index <= 7):
            raise Exception("Invalid index")

        index = index + 4
        offset = 38 if index > 7 else 37

        return get_bool(self._read(offset, 1), 0, index % 8)

    def set_valve_state(self, index: int, state: bool):
        if not (0 <= index <= 7):
            raise Exception("Invalid index")

        index = index + 4
        offset = 38 if index > 7 else 37
        index = index % 8

        byte = self._read(offset, 1)
        data = bytearray(1)
        for i in range(8):
            if i != index:
                set_bool(data, 0, i, get_bool(byte, 0, i))
            else:
                set_bool(data, 0, index, state)

        self._write(offset, data)
