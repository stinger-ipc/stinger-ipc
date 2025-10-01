"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
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

TodayIsSignalCallbackType = Callable[[int, stinger_types.DayOfTheWeek | None], None]
AddNumbersMethodResponseCallbackType = Callable[[int], None]
DoSomethingMethodResponseCallbackType = Callable[[], None]
EchoMethodResponseCallbackType = Callable[[str], None]

FavoriteNumberPropertyUpdatedCallbackType = Callable[[int], None]
FavoriteFoodsPropertyUpdatedCallbackType = Callable[[stinger_types.FavoriteFoodsProperty], None]
LunchMenuPropertyUpdatedCallbackType = Callable[[stinger_types.LunchMenuProperty], None]
FamilyNamePropertyUpdatedCallbackType = Callable[[str], None]


class FullClient:

    def __init__(self, connection: BrokerConnection):
        """ Constructor for a `FullClient` object.
        """
        self._logger = logging.getLogger('FullClient')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing FullClient")
        self._client_id = str(uuid4())
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        self._pending_method_responses: dict[str, Callable[..., None]] = {}
        
        self._property_favorite_number: int|None = None
        self._favorite_number_prop_subscription_id: int = self._conn.subscribe("full/{}/property/favoriteNumber/value")
        self._changed_value_callbacks_for_favorite_number: list[FavoriteNumberPropertyUpdatedCallbackType] = []
        self._property_favorite_foods: stinger_types.FavoriteFoodsProperty|None = None
        self._favorite_foods_prop_subscription_id: int = self._conn.subscribe("full/{}/property/favoriteFoods/value")
        self._changed_value_callbacks_for_favorite_foods: list[FavoriteFoodsPropertyUpdatedCallbackType] = []
        self._property_lunch_menu: stinger_types.LunchMenuProperty|None = None
        self._lunch_menu_prop_subscription_id: int = self._conn.subscribe("full/{}/property/lunchMenu/value")
        self._changed_value_callbacks_for_lunch_menu: list[LunchMenuPropertyUpdatedCallbackType] = []
        self._property_family_name: str|None = None
        self._family_name_prop_subscription_id: int = self._conn.subscribe("full/{}/property/familyName/value")
        self._changed_value_callbacks_for_family_name: list[FamilyNamePropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_today_is: list[TodayIsSignalCallbackType] = []
        self._addNumbers_method_call_subscription_id: int = self._conn.subscribe(f"client/{self._client_id}/full/{}/method/addNumbers/response")
        self._doSomething_method_call_subscription_id: int = self._conn.subscribe(f"client/{self._client_id}/full/{}/method/doSomething/response")
        self._echo_method_call_subscription_id: int = self._conn.subscribe(f"client/{self._client_id}/full/{}/method/echo/response")
        

    @property
    def favorite_number(self) -> int | None:
        """ Property 'favorite_number' getter.
        """
        return self._property_favorite_number
    
    @favorite_number.setter
    def favorite_number(self, value: int):
        """ Serializes and publishes the 'favorite_number' property.
        """
        if not isinstance(value, int):
            raise ValueError("The 'favorite_number' property must be a int")
        serialized = json.dumps({ "number": value.number })
        self._logger.debug("Setting 'favorite_number' property to %s", serialized)
        self._conn.publish("full/{}/property/favoriteNumber/setValue", serialized, qos=1)
    
    def favorite_number_changed(self, handler: FavoriteNumberPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'favorite_number' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_favorite_number.append(handler)
        if call_immediately and self._property_favorite_number is not None:
            handler(self._property_favorite_number)
        return handler

    @property
    def favorite_foods(self) -> stinger_types.FavoriteFoodsProperty | None:
        """ Property 'favorite_foods' getter.
        """
        return self._property_favorite_foods
    
    @favorite_foods.setter
    def favorite_foods(self, value: stinger_types.FavoriteFoodsProperty):
        """ Serializes and publishes the 'favorite_foods' property.
        """
        if not isinstance(value, stinger_types.FavoriteFoodsProperty):
            raise ValueError("The 'favorite_foods' property must be a stinger_types.FavoriteFoodsProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'favorite_foods' property to %s", serialized)
        self._conn.publish("full/{}/property/favoriteFoods/setValue", serialized, qos=1)
    
    def favorite_foods_changed(self, handler: FavoriteFoodsPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'favorite_foods' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_favorite_foods.append(handler)
        if call_immediately and self._property_favorite_foods is not None:
            handler(self._property_favorite_foods)
        return handler

    @property
    def lunch_menu(self) -> stinger_types.LunchMenuProperty | None:
        """ Property 'lunch_menu' getter.
        """
        return self._property_lunch_menu
    
    @lunch_menu.setter
    def lunch_menu(self, value: stinger_types.LunchMenuProperty):
        """ Serializes and publishes the 'lunch_menu' property.
        """
        if not isinstance(value, stinger_types.LunchMenuProperty):
            raise ValueError("The 'lunch_menu' property must be a stinger_types.LunchMenuProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'lunch_menu' property to %s", serialized)
        self._conn.publish("full/{}/property/lunchMenu/setValue", serialized, qos=1)
    
    def lunch_menu_changed(self, handler: LunchMenuPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'lunch_menu' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_lunch_menu.append(handler)
        if call_immediately and self._property_lunch_menu is not None:
            handler(self._property_lunch_menu)
        return handler

    @property
    def family_name(self) -> str | None:
        """ Property 'family_name' getter.
        """
        return self._property_family_name
    
    @family_name.setter
    def family_name(self, value: str):
        """ Serializes and publishes the 'family_name' property.
        """
        if not isinstance(value, str):
            raise ValueError("The 'family_name' property must be a str")
        serialized = json.dumps({ "family_name": value.family_name })
        self._logger.debug("Setting 'family_name' property to %s", serialized)
        self._conn.publish("full/{}/property/familyName/setValue", serialized, qos=1)
    
    def family_name_changed(self, handler: FamilyNamePropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'family_name' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_family_name.append(handler)
        if call_immediately and self._property_family_name is not None:
            handler(self._property_family_name)
        return handler

    

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

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """ New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.debug("Receiving message sent to %s", topic)
        # Handle 'todayIs' signal.
        if self._conn.is_topic_sub(topic, "full/{}/signal/todayIs"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'todayIs' signal with non-JSON content type")
                return
            allowed_args = ["dayOfMonth", "dayOfWeek", ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["dayOfMonth"] = int(kwargs["dayOfMonth"])
            kwargs["dayOfWeek"] = stinger_types.DayOfTheWeek(kwargs["dayOfWeek"]) if kwargs.get("dayOfWeek") else None 
            
            self._do_callbacks_for(self._signal_recv_callbacks_for_today_is, **kwargs)
        
        # Handle 'addNumbers' method response.
        if self._conn.is_topic_sub(topic, f"client/{self._client_id}/full/{}/method/addNumbers/response"):
            result_code = MethodReturnCode.SUCCESS
            if "UserProperty" in properties:
                user_properties = properties["UserProperty"]
                if "DebugInfo" in user_properties:
                    self._logger.info("Received Debug Info: %s", user_properties["DebugInfo"])
                if "ReturnValue" in user_properties:
                    result_code = MethodReturnCode(int(user_properties["ReturnValue"]))
            response = json.loads(payload)
            if "CorrelationData" in properties:
                correlation_id = properties["CorrelationData"].decode()
                if correlation_id in self._pending_method_responses:
                    cb = self._pending_method_responses[correlation_id]
                    del self._pending_method_responses[correlation_id]
                    cb(response, result_code)
                else:
                    self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
            else:
                self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])
        
        # Handle 'doSomething' method response.
        if self._conn.is_topic_sub(topic, f"client/{self._client_id}/full/{}/method/doSomething/response"):
            result_code = MethodReturnCode.SUCCESS
            if "UserProperty" in properties:
                user_properties = properties["UserProperty"]
                if "DebugInfo" in user_properties:
                    self._logger.info("Received Debug Info: %s", user_properties["DebugInfo"])
                if "ReturnValue" in user_properties:
                    result_code = MethodReturnCode(int(user_properties["ReturnValue"]))
            response = json.loads(payload)
            if "CorrelationData" in properties:
                correlation_id = properties["CorrelationData"].decode()
                if correlation_id in self._pending_method_responses:
                    cb = self._pending_method_responses[correlation_id]
                    del self._pending_method_responses[correlation_id]
                    cb(response, result_code)
                else:
                    self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
            else:
                self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])
        
        # Handle 'echo' method response.
        if self._conn.is_topic_sub(topic, f"client/{self._client_id}/full/{}/method/echo/response"):
            result_code = MethodReturnCode.SUCCESS
            if "UserProperty" in properties:
                user_properties = properties["UserProperty"]
                if "DebugInfo" in user_properties:
                    self._logger.info("Received Debug Info: %s", user_properties["DebugInfo"])
                if "ReturnValue" in user_properties:
                    result_code = MethodReturnCode(int(user_properties["ReturnValue"]))
            response = json.loads(payload)
            if "CorrelationData" in properties:
                correlation_id = properties["CorrelationData"].decode()
                if correlation_id in self._pending_method_responses:
                    cb = self._pending_method_responses[correlation_id]
                    del self._pending_method_responses[correlation_id]
                    cb(response, result_code)
                else:
                    self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
            else:
                self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])
        
        # Handle 'favorite_number' property change.
        if self._conn.is_topic_sub(topic, "full/{}/property/favoriteNumber/value"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'favorite_number' property change with non-JSON content type")
                return
            try:
                payload_obj = json.loads(payload)
                prop_value = int(payload_obj["number"])
                self._property_favorite_number = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_favorite_number, value=self._property_favorite_number)
            except Exception as e:
                self._logger.error("Error processing 'favorite_number' property change: %s", e)
        
        # Handle 'favorite_foods' property change.
        elif self._conn.is_topic_sub(topic, "full/{}/property/favoriteFoods/value"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'favorite_foods' property change with non-JSON content type")
                return
            try:
                prop_value = stinger_types.FavoriteFoodsProperty.model_validate_json(payload)
                self._property_favorite_foods = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_favorite_foods, value=self._property_favorite_foods)
            except Exception as e:
                self._logger.error("Error processing 'favorite_foods' property change: %s", e)
        
        # Handle 'lunch_menu' property change.
        elif self._conn.is_topic_sub(topic, "full/{}/property/lunchMenu/value"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'lunch_menu' property change with non-JSON content type")
                return
            try:
                prop_value = stinger_types.LunchMenuProperty.model_validate_json(payload)
                self._property_lunch_menu = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_lunch_menu, value=self._property_lunch_menu)
            except Exception as e:
                self._logger.error("Error processing 'lunch_menu' property change: %s", e)
        
        # Handle 'family_name' property change.
        elif self._conn.is_topic_sub(topic, "full/{}/property/familyName/value"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'family_name' property change with non-JSON content type")
                return
            try:
                payload_obj = json.loads(payload)
                prop_value = str(payload_obj["family_name"])
                self._property_family_name = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_family_name, value=self._property_family_name)
            except Exception as e:
                self._logger.error("Error processing 'family_name' property change: %s", e)
        

    
    def receive_today_is(self, handler: TodayIsSignalCallbackType):
        """ Used as a decorator for methods which handle particular signals.
        """
        self._signal_recv_callbacks_for_today_is.append(handler)
        if len(self._signal_recv_callbacks_for_today_is) == 1:
            self._conn.subscribe("full/{}/signal/todayIs")
        return handler
    

    
    def add_numbers(self, first: int, second: int, third: int | None) -> futures.Future:
        """ Calling this initiates a `addNumbers` IPC method call.
        """
        
        if not isinstance(first, int)and first is not None:
            raise ValueError("The 'first' argument wasn't a int")
        
        if not isinstance(second, int)and second is not None:
            raise ValueError("The 'second' argument wasn't a int")
        
        if not isinstance(third, int | None):
            raise ValueError("The 'third' argument wasn't a int | None")
        
        fut = futures.Future() # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_add_numbers_response, fut)
        payload = {
            "first": first,
            "second": second,
            "third": third,
        }
        self._conn.publish("full/{}/method/addNumbers", json.dumps(payload), qos=2, retain=False,
                           correlation_id=correlation_id, response_topic=f"client/{self._client_id}/full/{}/method/addNumbers/response")
        return fut

    def _handle_add_numbers_response(self, fut: futures.Future, response_json: Dict[str, Any], return_value: MethodReturnCode):
        """ This called with the response to a `addNumbers` IPC method call.
        """
        self._logger.debug("Handling add_numbers response message %s", fut)
        try:
            if return_value != MethodReturnCode.SUCCESS.value:
                raise stinger_exception_factory(return_value, response_json['debugResultMessage'] if 'debugResultMessage' in response_json else None)
            
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
        
        if not isinstance(aString, str)and aString is not None:
            raise ValueError("The 'aString' argument wasn't a str")
        
        fut = futures.Future() # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_do_something_response, fut)
        payload = {
            "aString": aString,
        }
        self._conn.publish("full/{}/method/doSomething", json.dumps(payload), qos=2, retain=False,
                           correlation_id=correlation_id, response_topic=f"client/{self._client_id}/full/{}/method/doSomething/response")
        return fut

    def _handle_do_something_response(self, fut: futures.Future, response_json: Dict[str, Any], return_value: MethodReturnCode):
        """ This called with the response to a `doSomething` IPC method call.
        """
        self._logger.debug("Handling do_something response message %s", fut)
        try:
            if return_value != MethodReturnCode.SUCCESS.value:
                raise stinger_exception_factory(return_value, response_json['debugResultMessage'] if 'debugResultMessage' in response_json else None)
            
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
    
    def echo(self, message: str) -> futures.Future:
        """ Calling this initiates a `echo` IPC method call.
        """
        
        if not isinstance(message, str)and message is not None:
            raise ValueError("The 'message' argument wasn't a str")
        
        fut = futures.Future() # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_echo_response, fut)
        payload = {
            "message": message,
        }
        self._conn.publish("full/{}/method/echo", json.dumps(payload), qos=2, retain=False,
                           correlation_id=correlation_id, response_topic=f"client/{self._client_id}/full/{}/method/echo/response")
        return fut

    def _handle_echo_response(self, fut: futures.Future, response_json: Dict[str, Any], return_value: MethodReturnCode):
        """ This called with the response to a `echo` IPC method call.
        """
        self._logger.debug("Handling echo response message %s", fut)
        try:
            if return_value != MethodReturnCode.SUCCESS.value:
                raise stinger_exception_factory(return_value, response_json['debugResultMessage'] if 'debugResultMessage' in response_json else None)
            
            if "message" in response_json:
                if not isinstance(response_json["message"], str):
                    raise ValueError("Return value 'message'' had wrong type")
                self._logger.debug("Setting future result")
                fut.set_result(response_json["message"])
            else:
                raise Exception("Response message didn't have the return value")
            
        except Exception as e:
            self._logger.info("Exception while handling echo", exc_info=e)
            fut.set_exception(e)
        if not fut.done():
            fut.set_exception(Exception("No return value set"))
    

class FullClientBuilder:

    def __init__(self, broker: BrokerConnection):
        """ Creates a new FullClientBuilder.
        """
        self._conn = broker
        self._logger = logging.getLogger('FullClientBuilder')
        self._signal_recv_callbacks_for_today_is = [] # type: List[TodayIsSignalCallbackType]
        self._property_updated_callbacks_for_favorite_number: list[FavoriteNumberPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_favorite_foods: list[FavoriteFoodsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_lunch_menu: list[LunchMenuPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_family_name: list[FamilyNamePropertyUpdatedCallbackType] = []
        
    def receive_today_is(self, handler):
        """ Used as a decorator for methods which handle particular signals.
        """
        self._signal_recv_callbacks_for_today_is.append(handler)
    

    
    def favorite_number_updated(self, handler: FavoriteNumberPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_favorite_number.append(handler)
    
    def favorite_foods_updated(self, handler: FavoriteFoodsPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_favorite_foods.append(handler)
    
    def lunch_menu_updated(self, handler: LunchMenuPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_lunch_menu.append(handler)
    
    def family_name_updated(self, handler: FamilyNamePropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_family_name.append(handler)
    

    def build(self) -> FullClient:
        """ Builds a new FullClient.
        """
        self._logger.debug("Building FullClient")
        client = FullClient(self._conn)
        
        for cb in self._signal_recv_callbacks_for_today_is:
            client.receive_today_is(cb)
        
        
        for cb in self._property_updated_callbacks_for_favorite_number:
            client.favorite_number_changed(cb)
        
        for cb in self._property_updated_callbacks_for_favorite_foods:
            client.favorite_foods_changed(cb)
        
        for cb in self._property_updated_callbacks_for_lunch_menu:
            client.lunch_menu_changed(cb)
        
        for cb in self._property_updated_callbacks_for_family_name:
            client.family_name_changed(cb)
        
        return client


if __name__ == '__main__':
    import signal


    conn = MqttBrokerConnection()
    client_builder = FullClientBuilder(conn)
    
    @client_builder.receive_today_is
    def print_todayIs_receipt(dayOfMonth: int, dayOfWeek: stinger_types.DayOfTheWeek | None):
        """
        @param dayOfMonth int 
        @param dayOfWeek stinger_types.DayOfTheWeek | None 
        """
        print(f"Got a 'todayIs' signal: dayOfMonth={ dayOfMonth } dayOfWeek={ dayOfWeek } ")
    
    
    @client_builder.favorite_number_updated
    def print_new_favorite_number_value(value: int):
        """
        """
        print(f"Property 'favorite_number' has been updated to: {value}")
    
    @client_builder.favorite_foods_updated
    def print_new_favorite_foods_value(value: stinger_types.FavoriteFoodsProperty):
        """
        """
        print(f"Property 'favorite_foods' has been updated to: {value}")
    
    @client_builder.lunch_menu_updated
    def print_new_lunch_menu_value(value: stinger_types.LunchMenuProperty):
        """
        """
        print(f"Property 'lunch_menu' has been updated to: {value}")
    
    @client_builder.family_name_updated
    def print_new_family_name_value(value: str):
        """
        """
        print(f"Property 'family_name' has been updated to: {value}")
    

    client = client_builder.build()
    
    print("Making call to 'add_numbers'")
    future = client.add_numbers(first=42, second=42, third=42)
    try:
        print(f"RESULT:  {future.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'add_numbers' call")
    
    print("Making call to 'do_something'")
    future = client.do_something(aString="apples")
    try:
        print(f"RESULT:  {future.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'do_something' call")
    
    print("Making call to 'echo'")
    future = client.echo(message="apples")
    try:
        print(f"RESULT:  {future.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'echo' call")
    
    

    print("Ctrl-C will stop the program.")
    signal.pause()