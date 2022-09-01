"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
"""

import json
import logging

logging.basicConfig(level=logging.DEBUG)

from typing import Callable
from connection import BrokerConnection
import interface_types as stinger_types



class ExampleServer(object):

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('ExampleServer')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing ExampleServer")
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        self._conn.set_last_will(topic="Example/interface", payload=None, qos=1, retain=True)
        
        self._conn.subscribe("Example/method/addNumbers")
        self._add_numbers_method_handler = None # type: Callable[[int, int], int]
        
    
    def _receive_message(self, topic, payload):
        self._logger.debug("Received message to %s", topic)
        if self._conn.is_topic_sub(topic, "Example/method/addNumbers"):
            try:
                payload_obj = json.loads(payload)
            except json.decoder.JSONDecodeError:
                self._logger.warning("Invalid JSON payload received at topic '%s'", topic)
            else:
                self._process_add_numbers_call(topic, payload_obj)
        

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

    def _process_add_numbers_call(self, topic, payload):
        if self._add_numbers_method_handler is not None:
            method_args = []
            if "first" in payload:
                if not isinstance(payload["first"], int):
                    self._logger.warning("The 'first' property in the payload to '%s' wasn't the correct type.  It should have been int.", topic)
                    return
                else:
                    method_args.append(payload["first"])
            else:
                self.logger.info("The 'first' property in the payload to '%s' wasn't present", topic)
            if "second" in payload:
                if not isinstance(payload["second"], int):
                    self._logger.warning("The 'second' property in the payload to '%s' wasn't the correct type.  It should have been int.", topic)
                    return
                else:
                    method_args.append(payload["second"])
            else:
                self.logger.info("The 'second' property in the payload to '%s' wasn't present", topic)
            
            return_value = self._add_numbers_method_handler(*method_args)
            
            if 'correlationId' and 'clientId' in payload:
                response = {
                    "correlationId": payload['correlationId']
                }
                
                response['returnValue'] = return_value
                
                response_topic = f"client/{payload['clientId']}/Example/method/addNumbers/response"
                self._conn.publish(response_topic, json.dumps(response), qos=1, retain=False)
    

    

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal
    
    from connection import LocalConnection

    conn = LocalConnection()
    server = ExampleServer(conn)

    
    @server.handle_add_numbers
    def add_numbers(first: int, second: int) -> int:
        print(f"Running add_numbers'({first}, {second})'")
        return 42
    

    server.emit_todayIs(42, stinger_types.DayOfTheWeek.MONDAY)
    
    sleep(4)
    server.emit_todayIs(dayOfMonth=42, dayOfWeek=stinger_types.DayOfTheWeek.MONDAY)
    

    print("Ctrl-C will stop the program.")
    signal.pause()