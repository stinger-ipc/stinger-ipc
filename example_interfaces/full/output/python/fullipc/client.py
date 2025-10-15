"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
"""

from typing import Dict, Callable, List, Any, Optional
from uuid import uuid4
from functools import partial
import json
import logging
from datetime import datetime, timedelta, UTC
from isodate import parse_duration

import asyncio
import concurrent.futures as futures
from method_codes import *
from interface_types import *
import threading

from connection import IBrokerConnection
import interface_types as interface_types

logging.basicConfig(level=logging.DEBUG)

TodayIsSignalCallbackType = Callable[[int, Optional[interface_types.DayOfTheWeek], datetime, timedelta, bytes], None]
AddNumbersMethodResponseCallbackType = Callable[[int], None]
DoSomethingMethodResponseCallbackType = Callable[[interface_types.DoSomethingMethodResponse], None]
EchoMethodResponseCallbackType = Callable[[str], None]
WhatTimeIsItMethodResponseCallbackType = Callable[[datetime], None]
SetTheTimeMethodResponseCallbackType = Callable[[interface_types.SetTheTimeMethodResponse], None]
ForwardTimeMethodResponseCallbackType = Callable[[datetime], None]
HowOffIsTheClockMethodResponseCallbackType = Callable[[timedelta], None]

FavoriteNumberPropertyUpdatedCallbackType = Callable[[int], None]
FavoriteFoodsPropertyUpdatedCallbackType = Callable[[interface_types.FavoriteFoodsProperty], None]
LunchMenuPropertyUpdatedCallbackType = Callable[[interface_types.LunchMenuProperty], None]
FamilyNamePropertyUpdatedCallbackType = Callable[[str], None]
LastBreakfastTimePropertyUpdatedCallbackType = Callable[[datetime], None]
BreakfastLengthPropertyUpdatedCallbackType = Callable[[timedelta], None]
LastBirthdaysPropertyUpdatedCallbackType = Callable[[interface_types.LastBirthdaysProperty], None]


class FullClient:

    def __init__(self, connection: IBrokerConnection, service_instance_id: str):
        """Constructor for a `FullClient` object."""
        self._logger = logging.getLogger("FullClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing FullClient")
        self._conn = connection
        self._conn.add_message_callback(self._receive_message)
        self._service_id = service_instance_id

        self._pending_method_responses: dict[str, Callable[..., None]] = {}

        self._property_favorite_number = None  # type: Optional[int]
        self._property_favorite_number_mutex = threading.Lock()
        self._property_favorite_number_version = -1
        self._conn.subscribe("full/{}/property/favoriteNumber/value".format(self._service_id), self._receive_favorite_number_property_update_message)
        self._changed_value_callbacks_for_favorite_number: list[FavoriteNumberPropertyUpdatedCallbackType] = []
        self._property_favorite_foods = None  # type: Optional[interface_types.FavoriteFoodsProperty]
        self._property_favorite_foods_mutex = threading.Lock()
        self._property_favorite_foods_version = -1
        self._conn.subscribe("full/{}/property/favoriteFoods/value".format(self._service_id), self._receive_favorite_foods_property_update_message)
        self._changed_value_callbacks_for_favorite_foods: list[FavoriteFoodsPropertyUpdatedCallbackType] = []
        self._property_lunch_menu = None  # type: Optional[interface_types.LunchMenuProperty]
        self._property_lunch_menu_mutex = threading.Lock()
        self._property_lunch_menu_version = -1
        self._conn.subscribe("full/{}/property/lunchMenu/value".format(self._service_id), self._receive_lunch_menu_property_update_message)
        self._changed_value_callbacks_for_lunch_menu: list[LunchMenuPropertyUpdatedCallbackType] = []
        self._property_family_name = None  # type: Optional[str]
        self._property_family_name_mutex = threading.Lock()
        self._property_family_name_version = -1
        self._conn.subscribe("full/{}/property/familyName/value".format(self._service_id), self._receive_family_name_property_update_message)
        self._changed_value_callbacks_for_family_name: list[FamilyNamePropertyUpdatedCallbackType] = []
        self._property_last_breakfast_time = None  # type: Optional[datetime.datetime]
        self._property_last_breakfast_time_mutex = threading.Lock()
        self._property_last_breakfast_time_version = -1
        self._conn.subscribe("full/{}/property/lastBreakfastTime/value".format(self._service_id), self._receive_last_breakfast_time_property_update_message)
        self._changed_value_callbacks_for_last_breakfast_time: list[LastBreakfastTimePropertyUpdatedCallbackType] = []
        self._property_breakfast_length = None  # type: Optional[datetime.timedelta]
        self._property_breakfast_length_mutex = threading.Lock()
        self._property_breakfast_length_version = -1
        self._conn.subscribe("full/{}/property/breakfastLength/value".format(self._service_id), self._receive_breakfast_length_property_update_message)
        self._changed_value_callbacks_for_breakfast_length: list[BreakfastLengthPropertyUpdatedCallbackType] = []
        self._property_last_birthdays = None  # type: Optional[interface_types.LastBirthdaysProperty]
        self._property_last_birthdays_mutex = threading.Lock()
        self._property_last_birthdays_version = -1
        self._conn.subscribe("full/{}/property/lastBirthdays/value".format(self._service_id), self._receive_last_birthdays_property_update_message)
        self._changed_value_callbacks_for_last_birthdays: list[LastBirthdaysPropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_today_is: list[TodayIsSignalCallbackType] = []
        self._conn.subscribe(f"client/{self._conn.client_id}/addNumbers/response", self._receive_add_numbers_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/doSomething/response", self._receive_do_something_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/echo/response", self._receive_echo_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/what_time_is_it/response", self._receive_what_time_is_it_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/set_the_time/response", self._receive_set_the_time_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/forward_time/response", self._receive_forward_time_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/how_off_is_the_clock/response", self._receive_how_off_is_the_clock_response_message)

    @property
    def favorite_number(self) -> Optional[int]:
        """Property 'favorite_number' getter."""
        return self._property_favorite_number

    @favorite_number.setter
    def favorite_number(self, value: int):
        """Serializes and publishes the 'favorite_number' property."""
        if not isinstance(value, int):
            raise ValueError("The 'favorite_number' property must be a int")
        serialized = json.dumps({"number": value.number})
        self._logger.debug("Setting 'favorite_number' property to %s", serialized)
        self._conn.publish("full/{}/property/favoriteNumber/setValue".format(self._service_id), serialized, qos=1)

    def favorite_number_changed(self, handler: FavoriteNumberPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'favorite_number' property changes.
        Can be used as a decorator.
        """
        with self._property_favorite_number_mutex:
            self._changed_value_callbacks_for_favorite_number.append(handler)
            if call_immediately and self._property_favorite_number is not None:
                handler(self._property_favorite_number)
        return handler

    @property
    def favorite_foods(self) -> Optional[interface_types.FavoriteFoodsProperty]:
        """Property 'favorite_foods' getter."""
        return self._property_favorite_foods

    @favorite_foods.setter
    def favorite_foods(self, value: interface_types.FavoriteFoodsProperty):
        """Serializes and publishes the 'favorite_foods' property."""
        if not isinstance(value, FavoriteFoodsProperty):
            raise ValueError("The 'favorite_foods' property must be a interface_types.FavoriteFoodsProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'favorite_foods' property to %s", serialized)
        self._conn.publish("full/{}/property/favoriteFoods/setValue".format(self._service_id), serialized, qos=1)

    def favorite_foods_changed(self, handler: FavoriteFoodsPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'favorite_foods' property changes.
        Can be used as a decorator.
        """
        with self._property_favorite_foods_mutex:
            self._changed_value_callbacks_for_favorite_foods.append(handler)
            if call_immediately and self._property_favorite_foods is not None:
                handler(self._property_favorite_foods)
        return handler

    @property
    def lunch_menu(self) -> Optional[interface_types.LunchMenuProperty]:
        """Property 'lunch_menu' getter."""
        return self._property_lunch_menu

    @lunch_menu.setter
    def lunch_menu(self, value: interface_types.LunchMenuProperty):
        """Serializes and publishes the 'lunch_menu' property."""
        if not isinstance(value, LunchMenuProperty):
            raise ValueError("The 'lunch_menu' property must be a interface_types.LunchMenuProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'lunch_menu' property to %s", serialized)
        self._conn.publish("full/{}/property/lunchMenu/setValue".format(self._service_id), serialized, qos=1)

    def lunch_menu_changed(self, handler: LunchMenuPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'lunch_menu' property changes.
        Can be used as a decorator.
        """
        with self._property_lunch_menu_mutex:
            self._changed_value_callbacks_for_lunch_menu.append(handler)
            if call_immediately and self._property_lunch_menu is not None:
                handler(self._property_lunch_menu)
        return handler

    @property
    def family_name(self) -> Optional[str]:
        """Property 'family_name' getter."""
        return self._property_family_name

    @family_name.setter
    def family_name(self, value: str):
        """Serializes and publishes the 'family_name' property."""
        if not isinstance(value, str):
            raise ValueError("The 'family_name' property must be a str")
        serialized = json.dumps({"family_name": value.family_name})
        self._logger.debug("Setting 'family_name' property to %s", serialized)
        self._conn.publish("full/{}/property/familyName/setValue".format(self._service_id), serialized, qos=1)

    def family_name_changed(self, handler: FamilyNamePropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'family_name' property changes.
        Can be used as a decorator.
        """
        with self._property_family_name_mutex:
            self._changed_value_callbacks_for_family_name.append(handler)
            if call_immediately and self._property_family_name is not None:
                handler(self._property_family_name)
        return handler

    @property
    def last_breakfast_time(self) -> Optional[datetime]:
        """Property 'last_breakfast_time' getter."""
        return self._property_last_breakfast_time

    @last_breakfast_time.setter
    def last_breakfast_time(self, value: datetime):
        """Serializes and publishes the 'last_breakfast_time' property."""
        if not isinstance(value, datetime):
            raise ValueError("The 'last_breakfast_time' property must be a datetime.datetime")
        serialized = json.dumps({"timestamp": value.timestamp})
        self._logger.debug("Setting 'last_breakfast_time' property to %s", serialized)
        self._conn.publish("full/{}/property/lastBreakfastTime/setValue".format(self._service_id), serialized, qos=1)

    def last_breakfast_time_changed(self, handler: LastBreakfastTimePropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'last_breakfast_time' property changes.
        Can be used as a decorator.
        """
        with self._property_last_breakfast_time_mutex:
            self._changed_value_callbacks_for_last_breakfast_time.append(handler)
            if call_immediately and self._property_last_breakfast_time is not None:
                handler(self._property_last_breakfast_time)
        return handler

    @property
    def breakfast_length(self) -> Optional[timedelta]:
        """Property 'breakfast_length' getter."""
        return self._property_breakfast_length

    @breakfast_length.setter
    def breakfast_length(self, value: timedelta):
        """Serializes and publishes the 'breakfast_length' property."""
        if not isinstance(value, timedelta):
            raise ValueError("The 'breakfast_length' property must be a datetime.timedelta")
        serialized = json.dumps({"length": value.length})
        self._logger.debug("Setting 'breakfast_length' property to %s", serialized)
        self._conn.publish("full/{}/property/breakfastLength/setValue".format(self._service_id), serialized, qos=1)

    def breakfast_length_changed(self, handler: BreakfastLengthPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'breakfast_length' property changes.
        Can be used as a decorator.
        """
        with self._property_breakfast_length_mutex:
            self._changed_value_callbacks_for_breakfast_length.append(handler)
            if call_immediately and self._property_breakfast_length is not None:
                handler(self._property_breakfast_length)
        return handler

    @property
    def last_birthdays(self) -> Optional[interface_types.LastBirthdaysProperty]:
        """Property 'last_birthdays' getter."""
        return self._property_last_birthdays

    @last_birthdays.setter
    def last_birthdays(self, value: interface_types.LastBirthdaysProperty):
        """Serializes and publishes the 'last_birthdays' property."""
        if not isinstance(value, LastBirthdaysProperty):
            raise ValueError("The 'last_birthdays' property must be a interface_types.LastBirthdaysProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'last_birthdays' property to %s", serialized)
        self._conn.publish("full/{}/property/lastBirthdays/setValue".format(self._service_id), serialized, qos=1)

    def last_birthdays_changed(self, handler: LastBirthdaysPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'last_birthdays' property changes.
        Can be used as a decorator.
        """
        with self._property_last_birthdays_mutex:
            self._changed_value_callbacks_for_last_birthdays.append(handler)
            if call_immediately and self._property_last_birthdays is not None:
                handler(self._property_last_birthdays)
        return handler

    def _do_callbacks_for(self, callbacks: List[Callable[..., None]], **kwargs):
        """Call each callback in the callback dictionary with the provided args."""
        for cb in callbacks:
            cb(**kwargs)

    @staticmethod
    def _filter_for_args(args: Dict[str, Any], allowed_args: List[str]) -> Dict[str, Any]:
        """Given a dictionary, reduce the dictionary so that it only has keys in the allowed list."""
        filtered_args = {}
        for k, v in args.items():
            if k in allowed_args:
                filtered_args[k] = v
        return filtered_args

    def _receive_today_is_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'todayIs' signal with non-JSON content type")
            return

        model = TodayIsSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_today_is, **kwargs)

    def _receive_add_numbers_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'addNumbers' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_do_something_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'doSomething' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_echo_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'echo' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_what_time_is_it_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'what_time_is_it' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_set_the_time_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'set_the_time' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_forward_time_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'forward_time' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_how_off_is_the_clock_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'how_off_is_the_clock' method response.
        return_code = MethodReturnCode.SUCCESS
        debug_message = None
        if "UserProperty" in properties:
            user_properties = properties["UserProperty"]
            if "DebugInfo" in user_properties:
                self._logger.info("Received Debug Info to '%s': %s", topic, user_properties["DebugInfo"])
                debug_message = user_properties["DebugInfo"]
            if "ReturnCode" in user_properties:
                return_code = MethodReturnCode(int(user_properties["ReturnCode"]))
        if "CorrelationData" in properties:
            correlation_id = properties["CorrelationData"].decode()
            if correlation_id in self._pending_method_responses:
                cb = self._pending_method_responses[correlation_id]
                del self._pending_method_responses[correlation_id]
                cb(payload, return_code, debug_message)
            else:
                self._logger.warning("Correlation id %s was not in the list of pending method responses... %s", correlation_id, [k for k in self._pending_method_responses.keys()])
        else:
            self._logger.warning("No correlation data in properties sent to %s... %s", topic, [s for s in properties.keys()])

    def _receive_favorite_number_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'favorite_number' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'favorite_number' property change with non-JSON content type")
            return
        try:
            prop_obj = FavoriteNumberProperty.model_validate_json(payload)
            with self._property_favorite_number_mutex:
                self._property_favorite_number = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_favorite_number_version:
                        self._property_favorite_number_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_favorite_number, value=prop_obj.number)

        except Exception as e:
            self._logger.exception("Error processing 'favorite_number' property change: %s", exc_info=e)

    def _receive_favorite_foods_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'favorite_foods' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'favorite_foods' property change with non-JSON content type")
            return
        try:
            prop_obj = FavoriteFoodsProperty.model_validate_json(payload)
            with self._property_favorite_foods_mutex:
                self._property_favorite_foods = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_favorite_foods_version:
                        self._property_favorite_foods_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_favorite_foods, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'favorite_foods' property change: %s", exc_info=e)

    def _receive_lunch_menu_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'lunch_menu' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'lunch_menu' property change with non-JSON content type")
            return
        try:
            prop_obj = LunchMenuProperty.model_validate_json(payload)
            with self._property_lunch_menu_mutex:
                self._property_lunch_menu = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_lunch_menu_version:
                        self._property_lunch_menu_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_lunch_menu, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'lunch_menu' property change: %s", exc_info=e)

    def _receive_family_name_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'family_name' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'family_name' property change with non-JSON content type")
            return
        try:
            prop_obj = FamilyNameProperty.model_validate_json(payload)
            with self._property_family_name_mutex:
                self._property_family_name = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_family_name_version:
                        self._property_family_name_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_family_name, value=prop_obj.family_name)

        except Exception as e:
            self._logger.exception("Error processing 'family_name' property change: %s", exc_info=e)

    def _receive_last_breakfast_time_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'last_breakfast_time' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'last_breakfast_time' property change with non-JSON content type")
            return
        try:
            prop_obj = LastBreakfastTimeProperty.model_validate_json(payload)
            with self._property_last_breakfast_time_mutex:
                self._property_last_breakfast_time = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_last_breakfast_time_version:
                        self._property_last_breakfast_time_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_last_breakfast_time, value=prop_obj.timestamp)

        except Exception as e:
            self._logger.exception("Error processing 'last_breakfast_time' property change: %s", exc_info=e)

    def _receive_breakfast_length_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'breakfast_length' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'breakfast_length' property change with non-JSON content type")
            return
        try:
            prop_obj = BreakfastLengthProperty.model_validate_json(payload)
            with self._property_breakfast_length_mutex:
                self._property_breakfast_length = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_breakfast_length_version:
                        self._property_breakfast_length_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_breakfast_length, value=prop_obj.length)

        except Exception as e:
            self._logger.exception("Error processing 'breakfast_length' property change: %s", exc_info=e)

    def _receive_last_birthdays_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'last_birthdays' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'last_birthdays' property change with non-JSON content type")
            return
        try:
            prop_obj = LastBirthdaysProperty.model_validate_json(payload)
            with self._property_last_birthdays_mutex:
                self._property_last_birthdays = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_last_birthdays_version:
                        self._property_last_birthdays_version = int(ver)

                self._do_callbacks_for(self._changed_value_callbacks_for_last_birthdays, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'last_birthdays' property change: %s", exc_info=e)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.warning("Receiving message sent to %s, but without a handler", topic)

    def receive_today_is(self, handler: TodayIsSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_today_is.append(handler)
        if len(self._signal_recv_callbacks_for_today_is) == 1:
            self._conn.subscribe("full/{}/signal/todayIs".format(self._service_id), self._receive_today_is_signal_message)
        return handler

    def add_numbers(self, first: int, second: int, third: Optional[int]) -> futures.Future:
        """Calling this initiates a `addNumbers` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_add_numbers_response, fut)
        payload = AddNumbersMethodRequest(
            first=first,
            second=second,
            third=third,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'addNumbers' method with payload %s", json_payload)
        self._conn.publish(
            "full/{}/method/addNumbers".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/addNumbers/response",
        )
        return fut

    def _handle_add_numbers_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `addNumbers` IPC method call."""
        self._logger.debug("Handling add_numbers response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'addNumbers' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = AddNumbersMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'addNumbers' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.sum)
        else:
            self._logger.warning("Future for 'addNumbers' method was already done!")

    def do_something(self, a_string: str) -> futures.Future:
        """Calling this initiates a `doSomething` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_do_something_response, fut)
        payload = DoSomethingMethodRequest(
            aString=a_string,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'doSomething' method with payload %s", json_payload)
        self._conn.publish(
            "full/{}/method/doSomething".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/doSomething/response",
        )
        return fut

    def _handle_do_something_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `doSomething` IPC method call."""
        self._logger.debug("Handling do_something response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'doSomething' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = DoSomethingMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'doSomething' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'doSomething' method was already done!")

    def echo(self, message: str) -> futures.Future:
        """Calling this initiates a `echo` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_echo_response, fut)
        payload = EchoMethodRequest(
            message=message,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'echo' method with payload %s", json_payload)
        self._conn.publish(
            "full/{}/method/echo".format(self._service_id), payload.model_dump_json(), qos=2, retain=False, correlation_id=correlation_id, response_topic=f"client/{self._conn.client_id}/echo/response"
        )
        return fut

    def _handle_echo_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `echo` IPC method call."""
        self._logger.debug("Handling echo response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'echo' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = EchoMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'echo' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.message)
        else:
            self._logger.warning("Future for 'echo' method was already done!")

    def what_time_is_it(self, the_first_time: datetime) -> futures.Future:
        """Calling this initiates a `what_time_is_it` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_what_time_is_it_response, fut)
        payload = WhatTimeIsItMethodRequest(
            the_first_time=the_first_time,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'what_time_is_it' method with payload %s", json_payload)
        self._conn.publish(
            "full/{}/method/whatTimeIsIt".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/what_time_is_it/response",
        )
        return fut

    def _handle_what_time_is_it_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `what_time_is_it` IPC method call."""
        self._logger.debug("Handling what_time_is_it response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'what_time_is_it' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = WhatTimeIsItMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'what_time_is_it' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.timestamp)
        else:
            self._logger.warning("Future for 'what_time_is_it' method was already done!")

    def set_the_time(self, the_first_time: datetime, the_second_time: datetime) -> futures.Future:
        """Calling this initiates a `set_the_time` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_set_the_time_response, fut)
        payload = SetTheTimeMethodRequest(
            the_first_time=the_first_time,
            the_second_time=the_second_time,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'set_the_time' method with payload %s", json_payload)
        self._conn.publish(
            "full/{}/method/setTheTime".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/set_the_time/response",
        )
        return fut

    def _handle_set_the_time_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `set_the_time` IPC method call."""
        self._logger.debug("Handling set_the_time response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'set_the_time' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = SetTheTimeMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'set_the_time' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model)
        else:
            self._logger.warning("Future for 'set_the_time' method was already done!")

    def forward_time(self, adjustment: timedelta) -> futures.Future:
        """Calling this initiates a `forward_time` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_forward_time_response, fut)
        payload = ForwardTimeMethodRequest(
            adjustment=adjustment,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'forward_time' method with payload %s", json_payload)
        self._conn.publish(
            "full/{}/method/forwardTime".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/forward_time/response",
        )
        return fut

    def _handle_forward_time_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `forward_time` IPC method call."""
        self._logger.debug("Handling forward_time response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'forward_time' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = ForwardTimeMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'forward_time' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.new_time)
        else:
            self._logger.warning("Future for 'forward_time' method was already done!")

    def how_off_is_the_clock(self, actual_time: datetime) -> futures.Future:
        """Calling this initiates a `how_off_is_the_clock` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_how_off_is_the_clock_response, fut)
        payload = HowOffIsTheClockMethodRequest(
            actual_time=actual_time,
        )
        json_payload = payload.model_dump_json()
        self._logger.debug("Calling 'how_off_is_the_clock' method with payload %s", json_payload)
        self._conn.publish(
            "full/{}/method/howOffIsTheClock".format(self._service_id),
            payload.model_dump_json(),
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/how_off_is_the_clock/response",
        )
        return fut

    def _handle_how_off_is_the_clock_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `how_off_is_the_clock` IPC method call."""
        self._logger.debug("Handling how_off_is_the_clock response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'how_off_is_the_clock' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = HowOffIsTheClockMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'how_off_is_the_clock' method: {e}"))

        if not fut.done():
            fut.set_result(resp_model.difference)
        else:
            self._logger.warning("Future for 'how_off_is_the_clock' method was already done!")


class FullClientBuilder:
    """Using decorators from FullClient doesn't work if you are trying to create multiple instances of FullClient.
    Instead, use this builder to create a registry of callbacks, and then build clients using the registry.

    When ready to create a FullClient instance, call the `build(broker, service_instance_id)` method.
    """

    def __init__(self):
        """Creates a new FullClientBuilder."""
        self._logger = logging.getLogger("FullClientBuilder")
        self._signal_recv_callbacks_for_today_is = []  # type: List[TodayIsSignalCallbackType]
        self._property_updated_callbacks_for_favorite_number: list[FavoriteNumberPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_favorite_foods: list[FavoriteFoodsPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_lunch_menu: list[LunchMenuPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_family_name: list[FamilyNamePropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_last_breakfast_time: list[LastBreakfastTimePropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_breakfast_length: list[BreakfastLengthPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_last_birthdays: list[LastBirthdaysPropertyUpdatedCallbackType] = []

    def receive_today_is(self, handler):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_today_is.append(handler)

    def favorite_number_updated(self, handler: FavoriteNumberPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_favorite_number.append(handler)

    def favorite_foods_updated(self, handler: FavoriteFoodsPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_favorite_foods.append(handler)

    def lunch_menu_updated(self, handler: LunchMenuPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_lunch_menu.append(handler)

    def family_name_updated(self, handler: FamilyNamePropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_family_name.append(handler)

    def last_breakfast_time_updated(self, handler: LastBreakfastTimePropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_last_breakfast_time.append(handler)

    def breakfast_length_updated(self, handler: BreakfastLengthPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_breakfast_length.append(handler)

    def last_birthdays_updated(self, handler: LastBirthdaysPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_last_birthdays.append(handler)

    def build(self, broker: IBrokerConnection, service_instance_id: str) -> FullClient:
        """Builds a new FullClient."""
        self._logger.debug("Building FullClient for service instance %s", service_instance_id)
        client = FullClient(broker, service_instance_id)

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

        for cb in self._property_updated_callbacks_for_last_breakfast_time:
            client.last_breakfast_time_changed(cb)

        for cb in self._property_updated_callbacks_for_breakfast_length:
            client.breakfast_length_changed(cb)

        for cb in self._property_updated_callbacks_for_last_birthdays:
            client.last_birthdays_changed(cb)

        return client


class FullClientDiscoverer:

    def __init__(self, connection: IBrokerConnection, builder: Optional[FullClientBuilder] = None):
        """Creates a new FullClientDiscoverer."""
        self._conn = connection
        self._builder = builder
        self._logger = logging.getLogger("FullClientDiscoverer")
        self._logger.setLevel(logging.DEBUG)
        service_discovery_topic = "full/{}/interface".format("+")
        self._conn.subscribe(service_discovery_topic, self._process_service_discovery_message)
        self._mutex = threading.Lock()
        self._discovered_services: Dict[str, InterfaceInfo] = {}
        self._discovered_service_callbacks: List[Callable[[InterfaceInfo], None]] = []
        self._pending_futures: List[futures.Future] = []
        self._removed_service_callbacks: List[Callable[[str], None]] = []

    def add_discovered_service_callback(self, callback: Callable[[InterfaceInfo], None]):
        """Adds a callback to be called when a new service is discovered."""
        with self._mutex:
            self._discovered_service_callbacks.append(callback)

    def add_removed_service_callback(self, callback: Callable[[str], None]):
        """Adds a callback to be called when a service is removed."""
        with self._mutex:
            self._removed_service_callbacks.append(callback)

    def get_service_instance_ids(self) -> List[str]:
        """Returns a list of currently discovered service instance IDs."""
        with self._mutex:
            return list(self._discovered_services.keys())

    def get_singleton_client(self) -> futures.Future[FullClient]:
        """Returns a FullClient for the single discovered service.
        Raises an exception if there is not exactly one discovered service.
        """
        fut = futures.Future()
        with self._mutex:
            if len(self._discovered_services) > 0:
                service_instance_id = next(iter(self._discovered_services))
                if self._builder is None:
                    fut.set_result(FullClient(self._conn, service_instance_id))
                else:
                    new_client = self._builder.build(self._conn, service_instance_id)
                    fut.set_result(new_client)
            else:
                self._pending_futures.append(fut)
        return fut

    def _process_service_discovery_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """Processes a service discovery message."""
        self._logger.debug("Processing service discovery message on topic %s", topic)
        if len(payload) > 0:
            try:
                service_info = InterfaceInfo.model_validate_json(payload)
            except Exception as e:
                self._logger.warning("Failed to process service discovery message: %s", e)
            with self._mutex:
                self._discovered_services[service_info.instance] = service_info
                while self._pending_futures:
                    fut = self._pending_futures.pop(0)
                    if not fut.done():
                        if self._builder is not None:
                            fut.set_result(self._builder.build(self._conn, service_info.instance))
                        else:
                            fut.set_result(FullClient(self._conn, service_info.instance))
                if not service_info.instance in self._discovered_services:
                    self._logger.info("Discovered service: %s.instance", service_info.instance)
                    for cb in self._discovered_service_callbacks:
                        cb(service_info)
                else:
                    self._logger.debug("Updated info for service: %s", service_info.instance)
        else:  # Empty payload means the service is going away
            instance_id = topic.split("/")[-2]
            with self._mutex:
                if instance_id in self._discovered_services:
                    self._logger.info("Service %s is going away", instance_id)
                    del self._discovered_services[instance_id]
                    for cb in self._removed_service_callbacks:
                        cb(instance_id)


if __name__ == "__main__":
    import signal
    from time import sleep
    from connection import MqttBrokerConnection, MqttTransport, MqttTransportType

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport)

    client_builder = FullClientBuilder()

    @client_builder.receive_today_is
    def print_todayIs_receipt(dayOfMonth: int, dayOfWeek: Optional[interface_types.DayOfTheWeek], timestamp: datetime, process_time: timedelta, memory_segment: bytes):
        """
        @param dayOfMonth int
        @param dayOfWeek Optional[interface_types.DayOfTheWeek]
        @param timestamp datetime
        @param process_time timedelta
        @param memory_segment bytes
        """
        print(f"Got a 'todayIs' signal: dayOfMonth={ dayOfMonth } dayOfWeek={ dayOfWeek } timestamp={ timestamp } process_time={ process_time } memory_segment={ memory_segment } ")

    @client_builder.favorite_number_updated
    def print_new_favorite_number_value(value: int):
        """ """
        print(f"Property 'favorite_number' has been updated to: {value}")

    @client_builder.favorite_foods_updated
    def print_new_favorite_foods_value(value: interface_types.FavoriteFoodsProperty):
        """ """
        print(f"Property 'favorite_foods' has been updated to: {value}")

    @client_builder.lunch_menu_updated
    def print_new_lunch_menu_value(value: interface_types.LunchMenuProperty):
        """ """
        print(f"Property 'lunch_menu' has been updated to: {value}")

    @client_builder.family_name_updated
    def print_new_family_name_value(value: str):
        """ """
        print(f"Property 'family_name' has been updated to: {value}")

    @client_builder.last_breakfast_time_updated
    def print_new_last_breakfast_time_value(value: datetime):
        """ """
        print(f"Property 'last_breakfast_time' has been updated to: {value}")

    @client_builder.breakfast_length_updated
    def print_new_breakfast_length_value(value: timedelta):
        """ """
        print(f"Property 'breakfast_length' has been updated to: {value}")

    @client_builder.last_birthdays_updated
    def print_new_last_birthdays_value(value: interface_types.LastBirthdaysProperty):
        """ """
        print(f"Property 'last_birthdays' has been updated to: {value}")

    discovery = FullClientDiscoverer(conn, client_builder)
    fut_client = discovery.get_singleton_client()
    try:
        client = fut_client.result(10)
    except futures.TimeoutError:
        print("Timed out waiting for a service to appear")
        exit(1)

    sleep(2)

    print("Making call to 'add_numbers'")
    future_resp = client.add_numbers(first=42, second=42, third=42)
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'add_numbers' call")

    print("Making call to 'do_something'")
    future_resp = client.do_something(a_string="apples")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'do_something' call")

    print("Making call to 'echo'")
    future_resp = client.echo(message="apples")
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'echo' call")

    print("Making call to 'what_time_is_it'")
    future_resp = client.what_time_is_it(the_first_time=datetime.now())
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'what_time_is_it' call")

    print("Making call to 'set_the_time'")
    future_resp = client.set_the_time(the_first_time=datetime.now(), the_second_time=datetime.now())
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'set_the_time' call")

    print("Making call to 'forward_time'")
    future_resp = client.forward_time(adjustment=timedelta(seconds=3536))
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'forward_time' call")

    print("Making call to 'how_off_is_the_clock'")
    future_resp = client.how_off_is_the_clock(actual_time=datetime.now())
    try:
        print(f"RESULT:  {future_resp.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'how_off_is_the_clock' call")

    print("Ctrl-C will stop the program.")
    signal.pause()
