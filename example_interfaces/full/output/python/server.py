"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
"""

import json
from typing import Callable
from connection import BrokerConnection
import interface_types as stinger_types

class ExampleServer(object):

    def __init__(self, connection: BrokerConnection):
        self._conn = connection
        self._conn.set_last_will(topic="Example/interface", payload=None, qos=1, retain=True)
        self._add_numbers_method_handler = None
        
    
    def _publish_interface_info(self):
        self._conn.publish("Example/interface", '''{"name": "Example", "summary": "Example StingerAPI interface which demonstrates most features.", "title": "Fully Featured Example Interface", "version": "0.0.1"}''', qos=1, retain=True)

    def emit_todayIs(self, dayOfMonth: int, dayOfWeek: stinger_types.DayOfTheWeek):
        
        if not isinstance(dayOfMonth, int):
            raise ValueError(f"The 'dayOfMonth' value must be int.")
        if not isinstance(dayOfWeek, stinger_types.DayOfTheWeek):
            raise ValueError(f"The 'dayOfWeek' value must be stinger_types.DayOfTheWeek.")
        
        payload = {
            "dayOfMonth": int(dayOfMonth),
            "dayOfWeek": stinger_types.DayOfTheWeek(dayOfWeek).value,
        }
        self._conn.publish("Example/signal/todayIs", json.dumps(payload), qos=1, retain=False)

    

    
    def handle_add_numbers(self, handler: Callable[[int, int], int]):
        do_subscribe = False
        if self._add_numbers_method_handler is None and handler is not None:
            do_subscribe = True
        self._add_numbers_method_handler = handler
        if do_subscribe:
            self._conn.subscribe("Example/method/addNumbers")

    def _process_add_numbers_call(self, topic, payload):
        if self._add_numbers_method_handler is not None:
            method_args = []
            for required_arg in []:
                if required_arg in payload:
                    method_args.append(payload[required_arg])
                else:
                    raise ValueError("Missing argument")
            return_value = self._add_numbers_method_handler(*method_args)
            if len(return_value) != 1:
                raise ValueError("Incorrect number of return arguments")
            
    

    

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    
    from connection import LocalConnection

    conn = LocalConnection()
    server = ExampleServer(conn)

    server.emit_todayIs(42, stinger_types.DayOfTheWeek.MONDAY)
    

    sleep(4)

    server.emit_todayIs(dayOfMonth=42, dayOfWeek=stinger_types.DayOfTheWeek.MONDAY)
    