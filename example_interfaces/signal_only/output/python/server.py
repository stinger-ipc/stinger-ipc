"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.
"""

import json
import logging

logging.basicConfig(level=logging.DEBUG)

from typing import Callable, Dict, Any, Optional
from .connection import BrokerConnection
from method_codes import *
from . import interface_types as stinger_types


class SignalOnlyServer:

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('SignalOnlyServer')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SignalOnlyServer")
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        self._conn.set_last_will(topic="SignalOnly/interface", payload=None, qos=1, retain=True)
        
    
    def _receive_message(self, topic: str, payload: str):
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

    

    

    

class SignalOnlyServerBuilder:
    """
    This is a builder for the SignalOnlyServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self, connection: BrokerConnection):
        self._conn = connection
        
    
    def build(self) -> SignalOnlyServer:
        new_server = SignalOnlyServer(self._conn)
        
        return new_server

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