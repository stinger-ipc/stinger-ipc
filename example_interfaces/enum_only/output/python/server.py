"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the EnumOnly interface.
"""

import json
from connection import BrokerConnection
import interface_enums as iface_enums

class EnumOnlyServer(object):

    def __init__(self, connection: BrokerConnection):
        self._conn = connection
        self._conn.set_last_will("EnumOnly/interface", payload=None, qos=1, retain=True)
        
    
    def _publish_interface_info(self):
        self._conn.publish("EnumOnly/interface", '''{"name": "EnumOnly", "summary": "", "title": "EnumOnly", "version": "0.0.1"}''', qos=1, retain=True)

    

    

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    
    from connection import DefaultConnection

    conn = DefaultConnection('localhost', 1883)
    server = EnumOnlyServer(conn)

    

    sleep(4)

    