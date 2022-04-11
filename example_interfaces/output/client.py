"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
"""

from typing import Dict, Callable, List, Any
import json
from .connection import MqttConnection

class SignalOnlyClient(object):

    def __init__(self, connection: MqttConnection):
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        self._signal_recv_callbacks_for_theSignal = []
        self._signal_recv_callbacks_for_anotherSignal = []
        
        self._conn.subscribe("SignalOnly/signal/theSignal", self._receive_message)
        self._conn.subscribe("SignalOnly/signal/anotherSignal", self._receive_message)
        

    def _do_callbacks_for(self, callbacks: Dict[str, Callable], **kwargs):
        for cb in callbacks:
            cb(**kwargs)

    @staticmethod
    def _filter_for_args(args: Dict[str, Any], allowed_args: List[str]) -> Dict[str, Any]:
        filtered_args = {}
        for k, v in args:
            if k in allowed_args:
                filtered_args[k] = v
        return filtered_args

    def _receive_message(self, topic, payload):
        if self._conn.is_topic_sub(topic, "SignalOnly/signal/theSignal"):
            allowed_args = []
            kwargs = self._filter_for_args(json.loads(payload), filtered_args)
            self._do_callbacks_for(self._signal_recv_callbacks_for_theSignal, **kwargs)
        elif self._conn.is_topic_sub(topic, "SignalOnly/signal/anotherSignal"):
            allowed_args = ["one", "two", "three", ]
            kwargs = self._filter_for_args(json.loads(payload), filtered_args)
            self._do_callbacks_for(self._signal_recv_callbacks_for_anotherSignal, **kwargs)
        

    
    def receive_theSignal(self, handler):
        self._signal_recv_callbacks_for_theSignal.append(handler)
    
    def receive_anotherSignal(self, handler):
        self._signal_recv_callbacks_for_anotherSignal.append(handler)
    

if __name__ == '__main__':
    conn = MqttConnection('localhost', 1883):
    client = SignalOnlyClient(conn)

    
    @client.receive_theSignal
    def print_theSignal_receipt(self, payload):
        print(f"Got a 'theSignal' signal: ")
    
    @client.receive_anotherSignal
    def print_anotherSignal_receipt(self, payload):
        print(f"Got a 'anotherSignal' signal: ")
    