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
        payload = {
            "dayOfMonth": dayOfMonth, 
            "dayOfWeek": dayOfWeek, 
        }
        self._conn.publish("Example/signal/todayIs", json.dumps(payload), qos=1, retain=False)

    

    

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep

    conn = MqttConnection('localhost', 1883)
    server = SignalOnlyServer(conn)

    server.emit_todayIs(2022, )
    

    sleep(4)

    server.emit_todayIs(dayOfMonth=2022, dayOfWeek=)
    