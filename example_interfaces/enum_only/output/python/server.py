"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the EnumOnly interface.
"""

import json
import logging

logging.basicConfig(level=logging.DEBUG)

from typing import Callable
from connection import BrokerConnection
import interface_types as stinger_types



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