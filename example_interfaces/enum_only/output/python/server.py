"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the EnumOnly interface.
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
        if "correlationId" in request and isinstance(request["correlationId"], str):
            self.correlation_id(request["correlationId"])

    @property
    def response(self):
        return self._response

    def is_valid(self) -> bool:
        return "correlationId" in self._response and "result" in self._response

    def correlation_id(self, correlationId: str):
        self._response["correlationId"] = correlationId
        return self
    
    def result_code(self, result_code: MethodResultCode):
        self._response["result"] = result_code.value
        return self

    def return_value(self, value_name: str, return_value):
        self._response[value_name] = return_value
        return self


class EnumOnlyServer(object):

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('EnumOnlyServer')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing EnumOnlyServer")
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        self._conn.set_last_will(topic="EnumOnly/interface", payload=None, qos=1, retain=True)
        
    
    def _receive_message(self, topic, payload):
        self._logger.debug("Received message to %s", topic)
        pass

    def _publish_interface_info(self):
        self._conn.publish("EnumOnly/interface", '''{"name": "EnumOnly", "summary": "", "title": "EnumOnly", "version": "0.0.1"}''', qos=1, retain=True)

    

    

    

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal
    
    from connection import DefaultConnection

    conn = DefaultConnection('localhost', 1883)
    server = EnumOnlyServer(conn)

    

    
    sleep(4)
    

    print("Ctrl-C will stop the program.")
    signal.pause()