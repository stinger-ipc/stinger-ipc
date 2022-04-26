"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
"""

import json
from connection import MqttConnection
import interface_enums as iface_enums

class ExampleServer(object):

    def __init__(self, connection: MqttConnection):
        self._conn = connection
        
    
    def emit_todayIs(self, dayOfMonth: int, dayOfWeek: iface_enums.DayOfTheWeek):
        
        if not isinstance(dayOfMonth, int):
            raise ValueError(f"The 'dayOfMonth' value must be int.")
        if not isinstance(dayOfWeek, iface_enums.DayOfTheWeek):
            raise ValueError(f"The 'dayOfWeek' value must be iface_enums.DayOfTheWeek.")
        
        payload = {
            "dayOfMonth": int(dayOfMonth),
            "dayOfWeek": iface_enums.DayOfTheWeek(dayOfWeek).value,
        }
        self._conn.publish("Example/signal/todayIs", json.dumps(payload), qos=1, retain=False)

    

    

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    
    conn = DefaultConnection('localhost', 1883)
    server = ExampleServer(conn)

    server.emit_todayIs(1981, iface_enums.DayOfTheWeek.WEDNESDAY)
    

    sleep(4)

    server.emit_todayIs(dayOfMonth=2022, dayOfWeek=iface_enums.DayOfTheWeek.MONDAY)
    