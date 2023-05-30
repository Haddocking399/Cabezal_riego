from django.apps import AppConfig
import os  
import signal  
import sys  
from environs import Env
env = Env()

daemon = None

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from api.daemon import Daemon
        global daemon
        if env.bool('DEBUG', True):
            from api.mock_sprinkler_head_plc import MockSprinklerHeadPLC        
            connector = MockSprinklerHeadPLC() 
        else:
            from api.snap7_sprinkler_head_plc import Snap7SprinklerHead
            connector = Snap7SprinklerHead()
        connector.connect(env('PLC_IP', '127.0.0.1'), env.int('PLC_RACK', 0), env.int('PLC_SLOT', 1))
        daemon = Daemon(env.int('PLC_UPDATE_TIME', 1), connector)
        daemon.run()
        signal.signal(signal.SIGINT, self.my_signal_handler) 
        #signal.signal(signal.SIGKILL, self.my_signal_handler)

    def my_signal_handler(self, *args):
        daemon.close()
        if os.environ.get('RUN_MAIN') == 'true':
            print('stopped'.upper())
        sys.exit(0)
