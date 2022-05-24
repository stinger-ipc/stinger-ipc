"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Example interface.
"""

from typing import Dict, Callable, List, Any
import json
from connection import MqttConnection
import interface_enums as iface_enums

class ExampleClient(object):

    def __init__(self, connection: MqttConnection):
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        self._signal_recv_callbacks_for_todayIs = []
        

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
        if self._conn.is_topic_sub(topic, "Example/signal/todayIs"):
            allowed_args = ["dayOfMonth", "dayOfWeek", ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)

            # Ensure received payload values have correct type.
            kwargs["dayOfMonth"] = int(kwargs["dayOfMonth"])
            kwargs["dayOfWeek"] = iface_enums.DayOfTheWeek(kwargs["dayOfWeek"])
            
            self._do_callbacks_for(self._signal_recv_callbacks_for_todayIs, **kwargs)
        

    
    def receive_todayIs(self, handler):
        self._signal_recv_callbacks_for_todayIs.append(handler)
        if len(self._signal_recv_callbacks_for_todayIs) == 1:
            self._conn.subscribe("Example/signal/todayIs")
    

if __name__ == '__main__':
    import signal
    
    conn = LocalConnection()
    client = ExampleClient(conn)
    
    @client.receive_todayIs
    def print_todayIs_receipt(dayOfMonth: int, dayOfWeek: iface_enums.DayOfTheWeek):
        """
        @param dayOfMonth int 
        @param dayOfWeek iface_enums.DayOfTheWeek 
        """
        print(f"Got a 'todayIs' signal: dayOfMonth={ dayOfMonth } dayOfWeek={ dayOfWeek } ")
    
    
    print("Ctrl-C will stop the program.")
    signal.pause()