from abc import abstractmethod
from abc import ABCMeta


class SprinklerHeadPLC(metaclass=ABCMeta):

    @abstractmethod
    def connect(self, address: str, rack: int, slot: int, port: int = 102) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def is_filter_clogged(self) -> bool:
        pass

    @abstractmethod
    def is_working_ph(self) -> bool:
        pass

    @abstractmethod
    def is_working_water_level(self) -> bool:
        pass

    @abstractmethod
    def is_working_salinity(self) -> bool:
        pass

    @abstractmethod
    def is_working_pressure(self) -> bool:
        pass

    @abstractmethod
    def is_working_flow(self) -> bool:
        pass

    @abstractmethod
    def get_ph(self) -> float:
        pass

    @abstractmethod
    def get_water_level(self) -> float:
        pass

    @abstractmethod
    def get_salinity(self) -> float:
        pass

    @abstractmethod
    def get_pressure(self) -> float:
        pass

    @abstractmethod
    def get_flow(self) -> float:
        pass

    @abstractmethod
    def get_fertilizer_state(self, index: int) -> bool:
        pass

    @abstractmethod
    def get_fertilizer_running_milliseconds(self, index: int) -> int:
        pass

    @abstractmethod
    def get_breaker_state(self, index: int) -> bool:
        pass

    @abstractmethod
    def get_breaker_off_count(self, index: int) -> int:
        pass

    @abstractmethod
    def get_pump_state(self) -> bool:
        pass

    @abstractmethod
    def get_valve_state(self, index: int) -> bool:
        pass

    @abstractmethod
    def set_valve_state(self, index: int, state: bool):
        pass


"""
PH_BD | 0.0
SAL_BD | 4.0
PRES_BD | 8.0
LV_BD | 12.0
N_DIS1_BD | 16.0
N_DIS2_BD | 18.0
N_DIS3_BD | 20.0
N_DIS4_BD | 22.0
T_FER_DB_1 | 24.0
T_FER_DB_2 | 28.0
T_FER_DB_3 | 32.0
DIS1_BD | 36.0
DIS2_BD | 36.1
DIS3_BD | 36.2
DIS4_BD | 36.3
SENSOR_PH | 36.4
SENSOR_LV | 36.5
SENSOR_CON | 36.6
SENSOR_PRES | 36.7
PREOS_ESTADO | 37.0
BD_YM1 | 37.1
BD_YM2 | 37.2
BD_YM3 | 37.3
BD_YM4 | 37.4
BD_YM5 | 37.5
BD_YM6 | 37.6
BD_YM7 | 37.7
BD_YM8 | 38.0
BD_YM9 | 38.1
BD_YM10 | 38.2
BD_YM11 | 38.3
BOMBA_ESTADO | 38.4
MODO_MANUAL | 38.5
MODO_AUTO | 38.6
"""
