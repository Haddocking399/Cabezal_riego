from api.sprinkler_head_plc import SprinklerHeadPLC
import random
import time

class MockSprinklerHeadPLC(SprinklerHeadPLC):

  def __init__(self):
    self._connected = False
    self._ph = 1
    self._water_level = 1
    self._salinity = 1
    self._pressure = 1
    self._flow = 1
    self._pump = True
    self._time = time.time()

  def connect(self, address: str, rack: int, slot: int, tcpport: int = 102) -> bool:
    self._connected = True
    return True

  def disconnect(self) -> bool:
    self._connected = False
    return True

  def is_connected(self) -> bool:
    return self._connected

  def is_filter_clogged(self) -> bool:
    return False

  def is_working_ph(self) -> bool:
    return True

  def is_working_water_level(self) -> bool:
    return True

  def is_working_salinity(self) -> bool:
    return True

  def is_working_pressure(self) -> bool:
    return True

  def is_working_flow(self) -> bool:
    return True
  
  def _random(self, value) -> float:
    r = random.random()
    return value + r if value < 1 or random.random() > 0.5 else value - r  

  def get_ph(self) -> float:    
    self._ph = self._random(self._ph)
    return self._ph 

  def get_water_level(self) -> float:
    self._water_level = self._random(self._water_level)
    return self._water_level

  def get_salinity(self) -> float:
    self._salinity = self._random(self._salinity)
    return self._salinity

  def get_pressure(self) -> float:
    self._pressure = self._random(self._pressure)
    return self._pressure

  def get_flow(self) -> float:
    self._flow = self._random(self._flow)
    return self._flow

  def get_fertilizer_state(self, index: int) -> bool:
    return True

  def get_fertilizer_running_milliseconds(self, index: int) -> int:
    return time.time() - self._time

  def get_breaker_state(self, index: int) -> bool:
    return True

  def get_breaker_off_count(self, index: int) -> int:
    return 0

  def get_pump_state(self) -> bool:
    dif = int((time.time() - self._time)/60)
    return True if dif % 2 == 0 else False

  def get_valve_state(self, index: int) -> bool:
    return True

  def set_valve_state(self, index: int, state: bool):
    return