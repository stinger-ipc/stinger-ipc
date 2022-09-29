"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Example interface.
"""

from typing import Dict, Callable, List, Any
from uuid import uuid4
from functools import partial
import json
import logging

import asyncio
import concurrent.futures as futures
from method_codes import *

from connection import BrokerConnection
import interface_types as stinger_types

logging.basicConfig(level=logging.DEBUG)

class ExampleClient(object):

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('ExampleClient')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing ExampleClient")
        self._client_id = str(uuid4())
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        self._pending_method_responses = {}
        
        self._signal_recv_callbacks_for_todayIs = []
        self._conn.subscribe(f"client/{self._client_id}/Example/method/addNumbers/response")
        self._conn.subscribe(f"client/{self._client_id}/Example/method/doSomething/response")
        

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
        # Handle todayIs
        if self._conn.is_topic_sub(topic, "Example/signal/todayIs"):
            allowed_args = ["dayOfMonth", "dayOfWeek", ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["dayOfMonth"] = int(kwargs["dayOfMonth"])
            kwargs["dayOfWeek"] = stinger_types.DayOfTheWeek(kwargs["dayOfWeek"])
            
            self._do_callbacks_for(self._signal_recv_callbacks_for_todayIs, **kwargs)
        
        # Handle addNumbers
        if self._conn.is_topic_sub(topic, f"client/{self._client_id}/Example/method/addNumbers/response"):
            response = json.loads(payload)
            if "correlationId" in response and response["correlationId"] in self._pending_method_responses:
                cb = self._pending_method_responses[response["correlationId"]]
                del self._pending_method_responses[response["correlationId"]]
                cb(response)
        
        # Handle doSomething
        if self._conn.is_topic_sub(topic, f"client/{self._client_id}/Example/method/doSomething/response"):
            response = json.loads(payload)
            if "correlationId" in response and response["correlationId"] in self._pending_method_responses:
                cb = self._pending_method_responses[response["correlationId"]]
                del self._pending_method_responses[response["correlationId"]]
                cb(response)
        

    
    def receive_todayIs(self, handler):
        """ Used as a decorator for methods which handle particular signals.
        """
        self._signal_recv_callbacks_for_todayIs.append(handler)
        if len(self._signal_recv_callbacks_for_todayIs) == 1:
            self._conn.subscribe("Example/signal/todayIs")
    

    
    def add_numbers(self, first: int, second: int) -> futures.Future:
        """ Calling this initiates a `addNumbers` IPC method call.
        """
        
        if not isinstance(first, int):
            raise ValueError("The 'first' argument wasn't a int")
        
        if not isinstance(second, int):
            raise ValueError("The 'second' argument wasn't a int")
        
        fut = futures.Future()
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_add_numbers_response, fut)
        payload = {
            "first": first,
            "second": second,
            "clientId": self._client_id,
            "correlationId": correlation_id,
        }
        self._conn.publish("Example/method/addNumbers", json.dumps(payload))
        return fut

    def _handle_add_numbers_response(self, fut: futures.Future, response_json: Dict[str, Any]):
        """ This called with the response to a `addNumbers` IPC method call.
        """
        self._logger.debug("Handling add_numbers response message %s", fut)
        try:
            if 'result' not in response_json:
                raise PayloadErrorStingerMethodException("The `result` key was not found in the response")
            if response_json['result'] != MethodResultCode.SUCCESS.value:
                self._logger.debug("Creating exception for %s", response_json)
                raise stinger_exception_factory(response_json['result'], response_json['debugResultMessage'] if 'debugResultMessage' in response_json else None)
            
            if "sum" in response_json:
                if not isinstance(response_json["sum"], int):
                    raise ValueError("Return value 'sum'' had wrong type")
                self._logger.debug("Setting future result")
                fut.set_result(response_json["sum"])
            else:
                raise Exception("Response message didn't have the return value")
            
        except Exception as e:
            self._logger.info("Exception while handling add_numbers", exc_info=e)
            fut.set_exception(e)
        if not fut.done():
            fut.set_exception(Exception("No return value set"))
    
    def do_something(self, aString: str) -> futures.Future:
        """ Calling this initiates a `doSomething` IPC method call.
        """
        
        if not isinstance(aString, str):
            raise ValueError("The 'aString' argument wasn't a str")
        
        fut = futures.Future()
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_do_something_response, fut)
        payload = {
            "aString": aString,
            "clientId": self._client_id,
            "correlationId": correlation_id,
        }
        self._conn.publish("Example/method/doSomething", json.dumps(payload))
        return fut

    def _handle_do_something_response(self, fut: futures.Future, response_json: Dict[str, Any]):
        """ This called with the response to a `doSomething` IPC method call.
        """
        self._logger.debug("Handling do_something response message %s", fut)
        try:
            if 'result' not in response_json:
                raise PayloadErrorStingerMethodException("The `result` key was not found in the response")
            if response_json['result'] != MethodResultCode.SUCCESS.value:
                self._logger.debug("Creating exception for %s", response_json)
                raise stinger_exception_factory(response_json['result'], response_json['debugResultMessage'] if 'debugResultMessage' in response_json else None)
            
            return_args = self._filter_for_args(response_json, ["label", "identifier", "day", ])
            return_args["label"] = str(return_args["label"])
            return_args["identifier"] = int(return_args["identifier"])
            return_args["day"] = stinger_types.DayOfTheWeek(return_args["day"])
            
            return_obj = stinger_types.DoSomethingReturnValue(**return_args)
            fut.set_result(return_obj)
            
        except Exception as e:
            self._logger.info("Exception while handling do_something", exc_info=e)
            fut.set_exception(e)
        if not fut.done():
            fut.set_exception(Exception("No return value set"))
    

if __name__ == '__main__':
    import signal

    from connection import LocalConnection
    conn = LocalConnection()
    client = ExampleClient(conn)
    
    @client.receive_todayIs
    def print_todayIs_receipt(dayOfMonth: int, dayOfWeek: stinger_types.DayOfTheWeek):
        """
        @param dayOfMonth int 
        @param dayOfWeek stinger_types.DayOfTheWeek 
        """
        print(f"Got a 'todayIs' signal: dayOfMonth={ dayOfMonth } dayOfWeek={ dayOfWeek } ")
    

    
    
    print("Making call to 'add_numbers'")
    future = client.add_numbers(first=42, second=42)
    print(future.result(5))
    
    print("Making call to 'do_something'")
    future = client.do_something(aString="apples")
    print(future.result(5))
    
    

    print("Ctrl-C will stop the program.")
    signal.pause()