"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the EnumOnly interface.
"""

import json
from connection import MqttConnection
import interface_enums as enum

class EnumOnlyServer(object):

    def __init__(self, connection: MqttConnection):
        self._conn = connection
        
    
    

    

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep

    conn = MqttConnection('localhost', 1883)
    server = SignalOnlyServer(conn)

    

    sleep(4)

    