"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

import json
import logging
import threading
from time import sleep
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

import isodate
import functools
from concurrent.futures import Future
logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel, ValidationError
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from pyqttier.interface import IBrokerConnection
from stinger_python_utils.message_creator import MessageCreator
from stinger_python_utils.return_codes import *
from .interface_types import *



from .property import SimplePropertyAccess



T = TypeVar('T')

@dataclass
class PropertyControls(Generic[T]):
    """
    Controls for a server property.  Generic[T] must be a single value or a pydantic BaseModel for multi-argument properties.
    """
    mutex = threading.RLock()
    getter: Callable[[], T]
    setter: Callable[[T], None]
    version: int = -1

    def get_value(self) -> T:
        return self.getter()

    def set_value(self, new_value: T) -> None:
        self.setter(new_value)
    
 

class SimpleServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str, property_access: SimplePropertyAccess):
        self._logger = logging.getLogger(f'SimpleServer:{instance_id}')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing SimpleServer instance %s", instance_id)
        self._instance_id = instance_id
        self._service_advert_topic = "simple/{}/interface".format(self._instance_id)
        self._re_advertise_server_interval_seconds = 120 # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)
        self._property_school: PropertyControls[str] = PropertyControls(getter=property_access.school_getter, setter=property_access.school_setter)
        self._conn.subscribe("simple/{}/property/school/setValue".format(self._instance_id), self._receive_school_update_request_message)
        
        self._conn.subscribe("simple/{}/method/tradeNumbers".format(self._instance_id), self._process_trade_numbers_call)
        self._method_trade_numbers_handler = None # type: Optional[Callable[[int], int]]
        
        self._publish_all_properties()
        self._logger.debug("Starting interface advertisement thread")
        self._advertise_thread = threading.Thread(target=self._loop_publishing_interface_info, daemon=True)
        self._advertise_thread.start()

    def __del__(self):
        self.shutdown()

    def shutdown(self, timeout: float=5.0):
        """Gracefully shutdown the server and stop the advertisement thread."""
        if not self._running:
            return
        self._running = False
        self._conn.unpublish_retained(self._service_advert_topic)
        if hasattr(self, '_advertise_thread') and self._advertise_thread.is_alive():
            self._advertise_thread.join(timeout=timeout)

    @property
    def instance_id(self) -> str:
        """ The instance ID of this server instance. """
        return self._instance_id

    def _loop_publishing_interface_info(self):
        """ We have a discovery topic separate from the MQTT client discovery topic.
        We publish it periodically, but with a Message Expiry interval."""
        while self._running:
            if self._conn.is_connected():
                self.publish_interface_info()
                time_left = self._re_advertise_server_interval_seconds
                while self._running and time_left > 0:
                    sleep(4)
                    time_left -= 4
            else:
                sleep(2)
            
    def publish_interface_info(self):
        """ Publishes the interface info message to the interface info topic with an expiry interval. """
        data = InterfaceInfo(
            instance=self._instance_id,
            connection_topic=(self._conn.online_topic or ""),
        timestamp=datetime.now(UTC).isoformat()
        )
        expiry = int(self._re_advertise_server_interval_seconds * 1.2) # slightly longer than the re-advertise interval
        topic = self._service_advert_topic
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json(by_alias=True))
        msg = MessageCreator.status_message(topic, data, expiry)
        self._conn.publish(msg)

    
    def publish_school_value(self, *_, **__):
        """ Publishes the current value of the 'school' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        """
        with self._property_school.mutex:
            self._property_school.version += 1
            school_prop_obj = SchoolProperty(name=self._property_school.get_value())
            state_msg = MessageCreator.property_state_message("simple/{}/property/school/value".format(self._instance_id), school_prop_obj, self._property_school.version)
            self._conn.publish(state_msg)

    def _publish_all_properties(self):
        """ Publishes the current value of all properties.
        """
        self.publish_school_value()

    
    
    def _receive_school_update_request_message(self, message: Message):
        """ When the MQTT client receives a message to the `simple/{}/property/school/setValue` topic
        in order to update the `school` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict() # type: Dict[str, str]
        prop_version_str = user_properties.get('PropertyVersion', "-1") # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data # type: Optional[bytes]
        response_topic = message.response_topic # type: Optional[str]

        try:
            if int(prop_version) != int(self._property_school.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_school.version}' of the 'school' property")

            recv_prop_obj = SchoolProperty.model_validate_json(message.payload)

            prop_value = recv_prop_obj.name
            with self._property_school.mutex:
                self._property_school.version += 1
                self._property_school.set_value(prop_value)
                
                current_prop_obj = SchoolProperty(name=self._property_school.get_value())
                
                state_msg = MessageCreator.property_state_message("simple/{}/property/school/value".format(self._instance_id), current_prop_obj, self._property_school.version)
                self._conn.publish(state_msg)
            
                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = MessageCreator.property_response_message(response_topic, current_prop_obj, str(self._property_school.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            
        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = SchoolProperty(name=self._property_school.get_value())
                if isinstance(e, (json.JSONDecodeError, ValidationError)):
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                elif isinstance(e, StingerMethodException):
                    return_code = e.return_code
                else:
                    return_code = MethodReturnCode.SERVER_ERROR
                prop_resp_msg = MessageCreator.property_response_message(response_topic, prop_obj, str(self._property_school.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)
    
    

    def _receive_message(self, message: Message):
        """ This is the callback that is called whenever any message is received on a subscribed topic.
        """
        self._logger.warning("Received unexpected message: %s", message)

    def emit_person_entered(self, person: Person):
        """ Server application code should call this method to emit the 'person_entered' signal.

        PersonEnteredSignalPayload is a pydantic BaseModel which will validate the arguments.
        """
        
        assert isinstance(person, Person), f"The 'person' argument must be of type Person, but was {type(person)}"
        

        payload = PersonEnteredSignalPayload(
            person=person,
        )
        sig_msg = MessageCreator.signal_message("simple/{}/signal/personEntered".format(self._instance_id), payload)
        self._conn.publish(sig_msg)

    

    
    def handle_trade_numbers(self, handler: Callable[[int], int]):
        """ This is a decorator to decorate a method that will handle the 'trade_numbers' method calls.
        """
        if self._method_trade_numbers_handler is None and handler is not None:
            self._method_trade_numbers_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_trade_numbers_call(self, message: Message):
        """ This processes a call to the 'trade_numbers' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        try:
            payload = TradeNumbersMethodRequest.model_validate_json(message.payload)
        except (json.JSONDecodeError, ValidationError) as e:
            self._logger.warning("Deserialization error while handling trade_numbers: %s", e)
            correlation_id = message.correlation_data
            response_topic = message.response_topic
            return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
            if response_topic:
                err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                self._conn.publish(err_msg)
            return
        correlation_id = message.correlation_data
        response_topic = message.response_topic

        if self._method_trade_numbers_handler is not None:
            method_args = [payload.your_number, ] # type: List[Any]
            
            return_json = ""
            debug_msg = None # type: Optional[str]
            try:
                return_values = self._method_trade_numbers_handler(*method_args)
                
                
                if not isinstance(return_values, int):
                    raise ServerSerializationErrorStingerMethodException(f"The return value must be of type int, but was {type(return_values)}")
                ret_obj = TradeNumbersMethodResponse(my_number=return_values)
                return_data = ret_obj
                
            except (json.JSONDecodeError, ValidationError) as e:
                self._logger.warning("Deserialization error while handling trade_numbers: %s", e)
                if response_topic is not None:
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                    self._conn.publish(err_msg)
            except StingerMethodException as sme:
                self._logger.warning("StingerMethodException while handling trade_numbers: %s", sme)
                if response_topic is not None:
                    return_code = sme.return_code
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(sme))
                    self._conn.publish(err_msg)
            except Exception as e:
                self._logger.exception("Exception while handling trade_numbers", exc_info=e)
                if response_topic is not None:
                    return_code = MethodReturnCode.SERVER_ERROR
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                    self._conn.publish(err_msg)
            else:
                if response_topic is not None:
                    msg = MessageCreator.response_message(response_topic, return_data, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    
    
    
    @property
    def school(self) -> Optional[str]:
        """ This property returns the last received (str) value for the 'school' property.
        
        This calls back into the application code to get the current value of the property.
        """
        return self._property_school.get_value()

    @school.setter
    def school(self, name: str):
        """ This property sets (publishes) a new str value for the 'school' property.
        
        This call the setter callback into the application code to set the property value.
        """
        if (not isinstance(name, str)):
            raise ValueError(f"The value must be str .")

        value_updated = False
        with self._property_school.mutex:
            if name != self._property_school.get_value():
                value_updated = True
                self._property_school.set_value(name)
                self._property_school.version += 1
                prop_obj = SchoolProperty(name=self._property_school.get_value())
                state_msg = MessageCreator.property_state_message("simple/{}/property/school/value".format(self._instance_id), prop_obj, self._property_school.version)
                self._conn.publish(state_msg)
        

    def set_school(self, name: str):
        """ This method sets (publishes) a new value for the 'school' property.
        """
        if not isinstance(name, str):
            raise ValueError(f"The 'name' value must be str.")

        
        obj = name
        

        # Use the property.setter to do that actual work.
        self.school = obj

    def on_school_updated(self, handler: Callable[[str], None]):
        """ This method registers a callback to be called whenever a new 'school' property update is received.
        """
        self._property_school.callbacks.append(handler)
    

class SimpleServerBuilder:
    """
    This is a builder for the SimpleServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):
        
        
        self._trade_numbers_method_handler: Optional[Callable[[int], int]] = None
        
        self._school_property_callbacks: List[Callable[[str], None]] = []
    
    def handle_trade_numbers(self, handler: Callable[[int], int]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        if self._trade_numbers_method_handler is None and handler is not None:
            self._trade_numbers_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper
    
    
    def on_school_updated(self, handler: Callable[[str], None]):
        """ This method registers a callback to be called whenever a new 'school' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._school_property_callbacks.append(wrapper)
        return wrapper
    
    def build(self, connection: IBrokerConnection, instance_id: str, property_access: SimplePropertyAccess, binding: Optional[Any]=None) -> SimpleServer:
        new_server = SimpleServer(connection, instance_id, property_access)
        
        if self._trade_numbers_method_handler is not None:
            if binding:
                new_server.handle_trade_numbers(self._trade_numbers_method_handler.__get__(binding, binding.__class__))
            else:
                new_server.handle_trade_numbers(self._trade_numbers_method_handler)
        
        for school_callback in self._school_property_callbacks:
            if binding:
                new_server.on_school_updated(school_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_school_updated(school_callback)
        
        return new_server
