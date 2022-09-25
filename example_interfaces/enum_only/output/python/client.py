"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the EnumOnly interface.
"""

from typing import Dict, Callable, List, Any
from uuid import uuid4
from functools import partial
import json
import logging

from connection import BrokerConnection
import interface_types as stinger_types

logging.basicConfig(level=logging.DEBUG)

class EnumOnlyClient(object):

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('EnumOnlyClient')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing EnumOnlyClient")
        self._client_id = str(uuid4())
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        

    def _do_callbacks_for(self, callbacks: Dict[str, Callable], **kwargs):
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

    def _receive_message(self, topic, payload):
        """ New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.debug("Receiving message sent to %s", topic)
        pass

    

    

if __name__ == '__main__':
    import signal

    from connection import DefaultConnection
    conn = DefaultConnection('localhost', 1883)
    client = EnumOnlyClient(conn)
    

    

    print("Ctrl-C will stop the program.")
    signal.pause()