"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
"""

from typing import Dict, Callable, List, Any
from uuid import uuid4
from functools import partial
import json
import logging

from connection import BrokerConnection


logging.basicConfig(level=logging.DEBUG)

class SignalOnlyClient(object):

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('SignalOnlyClient')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SignalOnlyClient")
        self._client_id = str(uuid4())
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        self._signal_recv_callbacks_for_anotherSignal = []
        

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
        self._logger.debug("Receiving message sent to %s", topic)
        if self._conn.is_topic_sub(topic, "SignalOnly/signal/anotherSignal"):
            allowed_args = ["one", "two", "three", ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)

            # Ensure received payload values have correct type.
            kwargs["one"] = float(kwargs["one"])
            kwargs["two"] = bool(kwargs["two"])
            kwargs["three"] = str(kwargs["three"])
            
            self._do_callbacks_for(self._signal_recv_callbacks_for_anotherSignal, **kwargs)
        
        

    
    def receive_anotherSignal(self, handler):
        self._signal_recv_callbacks_for_anotherSignal.append(handler)
        if len(self._signal_recv_callbacks_for_anotherSignal) == 1:
            self._conn.subscribe("SignalOnly/signal/anotherSignal")
    

    

if __name__ == '__main__':
    import signal

    from connection import DefaultConnection
    conn = DefaultConnection('localhost', 1883)
    client = SignalOnlyClient(conn)
    
    @client.receive_anotherSignal
    def print_anotherSignal_receipt(one: float, two: bool, three: str):
        """
        @param one float 
        @param two bool 
        @param three str 
        """
        print(f"Got a 'anotherSignal' signal: one={ one } two={ two } three={ three } ")
    

    

    print("Ctrl-C will stop the program.")
    signal.pause()