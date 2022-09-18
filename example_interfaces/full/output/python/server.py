"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
"""

import json
import logging

logging.basicConfig(level=logging.DEBUG)

from typing import Callable, Dict, Any
from connection import BrokerConnection, MethodResultCode
import interface_types as stinger_types



class MethodResponseBuilder:

    def __init__(self, request: Dict[str, Any]):
        self._response = {}
        if "clientId" in request and isinstance(request["clientId"], str):
            self.client_id(request["clientId"])
        if "correlationId" in request and isinstance(request["correlationId"], str):
            self.correlation_id(request["correlationId"])

    @property
    def response(self):
        return self._response

    def is_valid(self) -> bool:
        return "clientId" in self._response and "result" in self._response

    def client_id(self, client_id: str):
        self._response["clientId"] = client_id
        return self

    def correlation_id(self, correlationId: str):
        self._response["correlationId"] = correlationId
        return self
    
    def result_code(self, result_code: MethodResultCode):
        self._response["result"] = result_code.value
        return self

    def return_value(self, return_value):
        self._response["returnValue"] = return_value
        return self


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
        if self._add_numbers_method_handler is None and handler is not None:
            self._add_numbers_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_add_numbers_call(self, topic, payload):
        if self._add_numbers_method_handler is not None:
            response_builder = MethodResponseBuilder(payload)
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
            
            try:
                return_value = self._add_numbers_method_handler(*method_args)
            except:
                response_builder.result_code(MethodResultCode.SERVER_ERROR)
            else:
                response_builder.result_code(MethodResultCode.SUCCESS)
            
            if True:
            
                
                response_builder.return_value(return_value)
                
            if response_builder.is_valid():
                response_topic = f"client/{payload['clientId']}/Example/method/addNumbers/response"
                self._conn.publish(response_topic, json.dumps(response_builder.response), qos=1, retain=False)
    

    

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