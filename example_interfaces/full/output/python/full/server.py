"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Full interface.
"""

import json
import logging

logging.basicConfig(level=logging.DEBUG)

from typing import Callable, Dict, Any, Optional, List
from connection import BrokerConnection
from method_codes import *
import interface_types as stinger_types


class FullServer:

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger('FullServer')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing FullServer")
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        self._conn.set_last_will(topic="Full/interface", payload=None, qos=1, retain=True)
        self._property_favorite_number = None
        self._conn.subscribe("Full/property/favorite_number/set_value")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_favorite_foods = None
        self._conn.subscribe("Full/property/favorite_foods/set_value")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_lunch_menu = None
        self._conn.subscribe("Full/property/lunch_menu/set_value")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        
        self._conn.subscribe("Full/method/addNumbers")
        
        self._conn.subscribe("Full/method/doSomething")
        self._add_numbers_method_handler: Optional[Callable[[int, int, int | None], int]] = None
        self._do_something_method_handler: Optional[Callable[[str], ]] = None
        
    
    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """ This is the callback that is called whenever any message is received on a subscribed topic.
        """
        self._logger.debug("Received message to %s", topic)
        if self._conn.is_topic_sub(topic, "Full/method/addNumbers"):
            try:
                payload_obj = json.loads(payload)
            except json.decoder.JSONDecodeError:
                self._logger.warning("Invalid JSON payload received at topic '%s'", topic)
            else:
                self._process_add_numbers_call(topic, payload_obj, properties)
        elif self._conn.is_topic_sub(topic, "Full/method/doSomething"):
            try:
                payload_obj = json.loads(payload)
            except json.decoder.JSONDecodeError:
                self._logger.warning("Invalid JSON payload received at topic '%s'", topic)
            else:
                self._process_do_something_call(topic, payload_obj, properties)
        

    def _publish_interface_info(self):
        self._conn.publish("Full/interface", '''{"name": "Full", "summary": "Example StingerAPI interface which demonstrates most features.", "title": "Fully Featured Example Interface", "version": "0.0.1"}''', qos=1, retain=True)

    def emit_todayIs(self, dayOfMonth: int, dayOfWeek: stinger_types.DayOfTheWeek | None):
        """ Server application code should call this method to emit the 'todayIs' signal.
        """
        if not isinstance(dayOfMonth, int):
            raise ValueError(f"The 'dayOfMonth' value must be int.")
        if not isinstance(dayOfWeek, stinger_types.DayOfTheWeek) and dayOfWeek is not None:
            raise ValueError(f"The 'dayOfWeek' value must be stinger_types.DayOfTheWeek | None.")
        
        payload = {
            "dayOfMonth": int(dayOfMonth),
            "dayOfWeek": stinger_types.DayOfTheWeek(dayOfWeek).value if dayOfWeek is not None else None,
        }
        self._conn.publish("Full/signal/todayIs", json.dumps(payload), qos=1, retain=False)

    

    
    def handle_add_numbers(self, handler: Callable[[int, int, int | None], int]):
        """ This is a decorator to decorate a method that will handle the 'addNumbers' method calls.
        """
        if self._add_numbers_method_handler is None and handler is not None:
            self._add_numbers_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_add_numbers_call(self, topic: str, payload: Dict[str, Any], properties: Dict[str, Any]):
        """ This processes a call to the 'addNumbers' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        correlation_id = properties.get('CorrelationData') # type: Optional[bytes]
        response_topic = properties.get('ResponseTopic') # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._add_numbers_method_handler is not None:
            method_args = [] # type: List[Any]
            if "first" in payload:
                if not isinstance(payload["first"], int):
                    self._logger.warning("The 'first' property in the payload to '%s' wasn't the correct type.  It should have been int.", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["first"])
            else:
                
                self._logger.warning("The 'first' property in the payload to '%s' wasn't present", topic)
                # TODO: return an error via MQTT
                return
                
            if "second" in payload:
                if not isinstance(payload["second"], int):
                    self._logger.warning("The 'second' property in the payload to '%s' wasn't the correct type.  It should have been int.", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["second"])
            else:
                
                self._logger.warning("The 'second' property in the payload to '%s' wasn't present", topic)
                # TODO: return an error via MQTT
                return
                
            if "third" in payload:
                if not isinstance(payload["third"], int | None) or third is None:
                    self._logger.warning("The 'third' property in the payload to '%s' wasn't the correct type.  It should have been int | None.", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["third"])
            else:
                
                method_args.append(None)
                
            
            
            if response_topic is not None:
                return_json = ""
                debug_msg = None # type: Optional[str]
                try:
                    return_struct = self._add_numbers_method_handler(*method_args)
                    self._logger.debug("Return value is %s", return_struct)
                    
                    if return_struct is not None:
                        return_json = json.dumps({
                            "sum": return_struct
                        })
                except Exception as e:
                    self._logger.exception("Exception while handling addNumbers", exc_info=e)
                    return_code = MethodResultCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodResultCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, 
                    correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)
    
    def handle_do_something(self, handler: Callable[[str], ]):
        """ This is a decorator to decorate a method that will handle the 'doSomething' method calls.
        """
        if self._do_something_method_handler is None and handler is not None:
            self._do_something_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_do_something_call(self, topic: str, payload: Dict[str, Any], properties: Dict[str, Any]):
        """ This processes a call to the 'doSomething' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        correlation_id = properties.get('CorrelationData') # type: Optional[bytes]
        response_topic = properties.get('ResponseTopic') # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._do_something_method_handler is not None:
            method_args = [] # type: List[Any]
            if "aString" in payload:
                if not isinstance(payload["aString"], str):
                    self._logger.warning("The 'aString' property in the payload to '%s' wasn't the correct type.  It should have been str.", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["aString"])
            else:
                
                self._logger.warning("The 'aString' property in the payload to '%s' wasn't present", topic)
                # TODO: return an error via MQTT
                return
                
            
            
            if response_topic is not None:
                return_json = ""
                debug_msg = None # type: Optional[str]
                try:
                    return_struct = self._do_something_method_handler(*method_args)
                    self._logger.debug("Return value is %s", return_struct)
                    
                    if return_struct is not None:
                        return_json = json.dumps({
                            "doSomething": return_struct.model_dump_json()
                        })
                        
                except Exception as e:
                    self._logger.exception("Exception while handling doSomething", exc_info=e)
                    return_code = MethodResultCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodResultCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, 
                    correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)
    


class FullServerBuilder:
    """
    This is a builder for the FullServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self, connection: BrokerConnection):
        self._conn = connection
        
        self._add_numbers_method_handler: Optional[Callable[[int, int, int | None], int]] = None
        self._do_something_method_handler: Optional[Callable[[str], ]] = None
    
    def handle_add_numbers(self, handler: Callable[[int, int, int | None], int]):
        if self._add_numbers_method_handler is None and handler is not None:
            self._add_numbers_method_handler = handler
        else:
            raise Exception("Method handler already set")
    
    def handle_do_something(self, handler: Callable[[str], ]):
        if self._do_something_method_handler is None and handler is not None:
            self._do_something_method_handler = handler
        else:
            raise Exception("Method handler already set")
    
    def build(self) -> FullServer:
        new_server = FullServer(self._conn)
        
        if self._add_numbers_method_handler is not None:
            new_server.handle_add_numbers(self._add_numbers_method_handler)
        if self._do_something_method_handler is not None:
            new_server.handle_do_something(self._do_something_method_handler)
        return new_server

if __name__ == '__main__':
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal
    
    from connection import LocalConnection

    conn = LocalConnection()
    server = FullServer(conn)

    
    @server.handle_add_numbers
    def add_numbers(first: int, second: int, third: int | None) -> int:
        print(f"Running add_numbers'({first}, {second}, {third})'")
        return 42
    
    @server.handle_do_something
    def do_something(aString: str) -> :
        print(f"Running do_something'({aString})'")
        return ['"apples"', 42, 'stinger_types.DayOfTheWeek.MONDAY']
    

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_todayIs(42, stinger_types.DayOfTheWeek.MONDAY)
            
            sleep(4)
            server.emit_todayIs(dayOfMonth=42, dayOfWeek=stinger_types.DayOfTheWeek.MONDAY)
            
            sleep(6)
        except KeyboardInterrupt:
            break


    signal.pause()