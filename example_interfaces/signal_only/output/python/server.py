"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.
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

class SignalOnlyServer(object):

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('SignalOnlyServer')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SignalOnlyServer")
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        self._conn.set_last_will(topic="SignalOnly/interface", payload=None, qos=1, retain=True)
        
    
    def _receive_message(self, topic, payload):
        self._logger.debug("Received message to %s", topic)
        pass

    def _publish_interface_info(self):
        self._conn.publish("SignalOnly/interface", '''{"name": "SignalOnly", "summary": "", "title": "SignalOnly", "version": "0.0.1"}''', qos=1, retain=True)

    def emit_anotherSignal(self, one: float, two: bool, three: str):
        
        if not isinstance(one, float):
            raise ValueError(f"The 'one' value must be float.")
        if not isinstance(two, bool):
            raise ValueError(f"The 'two' value must be bool.")
        if not isinstance(three, str):
            raise ValueError(f"The 'three' value must be str.")
        
        payload = {
            "one": float(one),
            "two": bool(two),
            "three": str(three),
        }
        self._conn.publish("SignalOnly/signal/anotherSignal", json.dumps(payload), qos=1, retain=False)

    

    

    

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal
    
    from connection import DefaultConnection

    conn = DefaultConnection('localhost', 1883)
    server = SignalOnlyServer(conn)

    

    server.emit_anotherSignal(3.14, True, "apples")
    
    sleep(4)
    server.emit_anotherSignal(one=3.14, two=True, three="apples")
    

    print("Ctrl-C will stop the program.")
    signal.pause()