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


AnotherSignalSignalCallbackType = Callable[[float, bool, str], None]


class SignalOnlyClient:

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('SignalOnlyClient')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SignalOnlyClient")
        self._client_id = str(uuid4())
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        self._signal_recv_callbacks_for_anotherSignal = [] # type: List[AnotherSignalSignalCallbackType]
        

    def _do_callbacks_for(self, callbacks: List[Callable[..., None]], **kwargs):
        """ Call each callback in the callback dictionary with the provided args.
        """
        for cb in callbacks:
            cb(**kwargs)

    @staticmethod
    def _filter_for_args(args: Dict[str, Any], allowed_args: List[str]) -> Dict[str, Any]:
        """ Given a dictionary, reduce the dictionary so that it only has keys in the allowed list.
        """
        filtered_args = {}
        for k, v in args.items():
            if k in allowed_args:
                filtered_args[k] = v
        return filtered_args

    def _receive_message(self, topic, payload, properties):
        """ New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.debug("Receiving message sent to %s", topic)
        # Handle 'anotherSignal' signal.
        if self._conn.is_topic_sub(topic, "SignalOnly/signal/anotherSignal"):
            if 'contentType' not in properties or properties['contentType'] != 'application/json':
                self._logger.warning("Received 'anotherSignal' signal with non-JSON content type")
                return
            allowed_args = ["one", "two", "three", ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["one"] = float(kwargs["one"])
            kwargs["two"] = bool(kwargs["two"])
            kwargs["three"] = str(kwargs["three"])
            
            self._do_callbacks_for(self._signal_recv_callbacks_for_anotherSignal, **kwargs)
        

    
    def receive_anotherSignal(self, handler):
        """ Used as a decorator for methods which handle particular signals.
        """
        self._signal_recv_callbacks_for_anotherSignal.append(handler)
        if len(self._signal_recv_callbacks_for_anotherSignal) == 1:
            self._conn.subscribe("SignalOnly/signal/anotherSignal")
    

    

class SignalOnlyClientBuilder:

    def __init__(self, broker: BrokerConnection):
        """ Creates a new SignalOnlyClientBuilder.
        """
        self._conn = broker
        self._logger = logging.getLogger('SignalOnlyClientBuilder')
        self._signal_recv_callbacks_for_anotherSignal = [] # type: List[AnotherSignalSignalCallbackType]
        
    def receive_anotherSignal(self, handler):
        """ Used as a decorator for methods which handle particular signals.
        """
        self._signal_recv_callbacks_for_anotherSignal.append(handler)
    

    def build(self) -> SignalOnlyClient:
        """ Builds a new SignalOnlyClient.
        """
        self._logger.debug("Building SignalOnlyClient")
        client = SignalOnlyClient(self._conn)
        
        def receive_anotherSignal(self, handler):
            """ Used as a decorator for methods which handle particular signals.
            """
            for cb in self._signal_recv_callbacks_for_anotherSignal:
                client.receive_anotherSignal(cb)
        
        return client


if __name__ == '__main__':
    import signal

    from connection import DefaultConnection
    conn = DefaultConnection('localhost', 1883)
    client_builder = SignalOnlyClientBuilder(conn)
    
    @client_builder.receive_anotherSignal
    def print_anotherSignal_receipt(one: float, two: bool, three: str):
        """
        @param one float 
        @param two bool 
        @param three str 
        """
        print(f"Got a 'anotherSignal' signal: one={ one } two={ two } three={ three } ")
    

    client = client_builder.build()
    

    print("Ctrl-C will stop the program.")
    signal.pause()