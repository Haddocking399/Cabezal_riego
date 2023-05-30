from api.sprinkler_head_plc import SprinklerHeadPLC
from threading import Thread, Event
from .models import Pump, Sensors, Fertilizers, Breakers, Valves
import time
from django.utils import timezone

class Daemon:
    
    def __init__(self, update_time: float, connector: SprinklerHeadPLC):
        self._update_time = update_time
        self._connector = connector        
        self._reset()

        self._event = Event()
        self._thread = None

    @property
    def ph(self):
        return self._ph
    
    @property
    def pressure(self):
        return self._pressure
    
    @property
    def water_level(self):
        return self._water_level    
    
    @property
    def flow(self):
        return self._flow        
    
    @property
    def salinity(self):
        return self._salinity   
    
    @property
    def pump(self):
        return self._pump  
    
    @property
    def valves(self):
        valves = []
        for x in self._valves:
            valves.append(x)
        return valves   
    
    @property
    def breakers(self):
        breakers = []
        for x in self._breakers:
            breakers.append(x)
        return breakers    

    @property
    def fertilizers(self):
        fertilizers = []
        for x in self._fertilizers:
            fertilizers.append(x)
        return fertilizers             
    
    def get_valve(self, idx):
        return self._valves[idx]
    
    def set_valve(self, idx, state):
        self._valve_orders[idx] = state    
    
    def get_breaker(self, idx):
        return self._breakers[idx]    
    
    def get_fertilizer(self, idx):
        return self._fertilizers[idx]     

    def _reset(self):
        self._reset_sensors()
        self._reset_pump()
        self._reset_fertilizers()
        self._reset_breakers()        
        self._reset_valves()

    def _reset_sensors(self):
        self._ph = None
        self._pressure = None
        self._water_level = None
        self._flow = None
        self._salinity = None

    def _reset_pump(self):
        self._pump = False

    def _reset_fertilizers(self):
        self._fertilizers = [False, False, False]

    def _reset_breakers(self):        
        self._breakers = [False, False, False, False]

    def _reset_valves(self):        
        self._valves = [False, False, False, False, False, False, False, False]
        self._valve_orders = [None, None, None, None, None, None, None, None]

    def _update_sensors(self):
        if not self._connector.is_connected():
            self._reset_sensors()
            return

        self._ph = self._connector.get_ph() if self._connector.is_working_ph else None 
        self._pressure = self._connector.get_pressure() if self._connector.is_working_pressure else None
        self._water_level = self._connector.get_water_level() if self._connector.is_working_water_level else None
        self._flow = self._connector.get_flow() if self._connector.is_working_flow else None
        self._salinity = self._connector.get_salinity() if self._connector.is_working_salinity else None

        Sensors.objects.create(
            date = timezone.now(),
            ph = self.ph,
            water_level = self.water_level,
            pressure = self.pressure,
            flow = self.flow,
            salinity = self.salinity
        )
    
    def _update_valves(self):
        if not self._connector.is_connected():
            self._reset_valves()
            return

        for idx, x in enumerate(self._valves):
            if self._valve_orders[idx] != None:
                self._connector.set_valve_state(idx, self._valve_orders[idx])
                self._valve_orders[idx] = None

        must_write = False
        for idx, x in enumerate(self._valves):
            valve = self._connector.get_valve_state(idx)
            if valve != x:
                must_write = True
            self._valves[idx] = valve

        if must_write:
            print("Escribir BD")
    
    def _update_breakers(self):
        if not self._connector.is_connected():
            self._reset_breakers()
            return

        must_write = False
        for idx, x in enumerate(self._breakers):
            breaker = self._connector.get_breaker_state(idx)
            if breaker != x:
                must_write = True
            self._breakers[idx] = breaker
            
        if must_write:
            print("Escribir BD")
    
    def _update_fertilizers(self):
        if not self._connector.is_connected():
            self._reset_fertilizers()
            return

        must_write = False
        for idx, x in enumerate(self._fertilizers):
            fertilizer = self._connector.get_fertilizer_state(idx)
            if fertilizer != x:
                must_write = True
            self._fertilizers[idx] = fertilizer
            
        if must_write:
            print("Escribir BD")

    def _update_pump(self):
        if not self._connector.is_connected():
            self._reset_pump()
            return
        
        pump = self._connector.get_pump_state()
        if pump != self.pump:
            self._pump = pump
            Pump.objects.create(
                date = timezone.now(),
                state = pump            
            )

    def _update(self):
        # try:
        while not self._event.isSet():
            time.sleep(self._update_time)
            if self._connector.is_connected:
                self._update_pump()
                self._update_sensors()
                self._update_valves()
                self._update_breakers()
                self._update_fertilizers()
            else:
                self._reset()

        # except E

    def run(self):
        self._thread = Thread(target=self._update)
        self._thread.daemon = True
        self._thread.start()

    def close(self):
        self._connector.disconnect()
        self._event.set()
        self._thread.join()