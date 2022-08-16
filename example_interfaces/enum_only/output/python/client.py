"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the EnumOnly interface.
"""

from typing import Dict, Callable, List, Any
import json
from connection import MqttConnection
import interface_enums as iface_enums

class EnumOnlyClient(object):

    def __init__(self, connection: MqttConnection):
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        

    def _do_callbacks_for(self, callbacks: Dict[str, Callable], **kwargs):
        for cb in callbacks:
            cb(**kwargs)

    @staticmethod
    def _filter_for_args(args: Dict[str, Any], allowed_args: List[str]) -> Dict[str, Any]:
        filtered_args = {}
        for k, v in args.items():
            if k in allowed_args:
                filtered_args[k] = v
        return filtered_args

    def _receive_message(self, topic, payload):
        pass

    

if __name__ == '__main__':
    import signal
    
    conn = DefaultConnection('localhost', 1883)
    client = EnumOnlyClient(conn)
    
    
    print("Ctrl-C will stop the program.")
    signal.pause()