from typing import Dict, Callable, List, Any
import json

class SignalOnlyClient(object):

    def __init__(self, connection):
        self._conn = connection
        
        self._signal_recv_callbacks_for_theSignal = {}
        self._signal_recv_callbacks_for_anotherSignal = {}
        
        self._conn.subscribe("SignalOnly/signal/theSignal", self._receive_message)
        self._conn.subscribe("SignalOnly/signal/anotherSignal", self._receive_message)
        

    def _do_callbacks_for(self, callbacks: Dict[str, Callable], **kwargs):
        for cb in callbacks.values():
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
        
    