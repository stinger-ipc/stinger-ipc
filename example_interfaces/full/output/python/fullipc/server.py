"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Full interface.
"""

import json
import logging
import threading
from time import sleep
from dataclasses import dataclass, field
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from connection import IBrokerConnection
from method_codes import *
from interface_types import InterfaceInfo
import interface_types as stinger_types


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
    value: T | None = None
    mutex = threading.Lock()
    version: int = -1
    subscription_id: int | None = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)


@dataclass
class MethodControls:
    subscription_id: int | None = None
    callback: Optional[Callable] = None


class FullServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str):
        self._logger = logging.getLogger(f"FullServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing FullServer instance %s", instance_id)
        self._instance_id = instance_id
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._property_favorite_number: PropertyControls[int, int] = PropertyControls()
        self._property_favorite_number.subscription_id = self._conn.subscribe(
            "full/{}/property/favoriteNumber/setValue".format(self._instance_id), self._receive_favorite_number_update_request_message
        )

        self._property_favorite_foods: PropertyControls[stinger_types.FavoriteFoodsProperty, str, int, Optional[str]] = PropertyControls()
        self._property_favorite_foods.subscription_id = self._conn.subscribe("full/{}/property/favoriteFoods/setValue".format(self._instance_id), self._receive_favorite_foods_update_request_message)

        self._property_lunch_menu: PropertyControls[stinger_types.LunchMenuProperty, stinger_types.Lunch, stinger_types.Lunch] = PropertyControls()
        self._property_lunch_menu.subscription_id = self._conn.subscribe("full/{}/property/lunchMenu/setValue".format(self._instance_id), self._receive_lunch_menu_update_request_message)

        self._property_family_name: PropertyControls[str, str] = PropertyControls()
        self._property_family_name.subscription_id = self._conn.subscribe("full/{}/property/familyName/setValue".format(self._instance_id), self._receive_family_name_update_request_message)

        self._property_last_breakfast_time: PropertyControls[datetime.datetime, datetime.datetime] = PropertyControls()
        self._property_last_breakfast_time.subscription_id = self._conn.subscribe(
            "full/{}/property/lastBreakfastTime/setValue".format(self._instance_id), self._receive_last_breakfast_time_update_request_message
        )

        self._property_last_birthdays: PropertyControls[stinger_types.LastBirthdaysProperty, datetime.datetime, datetime.datetime, datetime.datetime] = PropertyControls()
        self._property_last_birthdays.subscription_id = self._conn.subscribe("full/{}/property/lastBirthdays/setValue".format(self._instance_id), self._receive_last_birthdays_update_request_message)

        self._method_add_numbers = MethodControls()
        self._method_add_numbers.subscription_id = self._conn.subscribe("full/{}/method/addNumbers".format(self._instance_id), self._process_add_numbers_call)

        self._method_do_something = MethodControls()
        self._method_do_something.subscription_id = self._conn.subscribe("full/{}/method/doSomething".format(self._instance_id), self._process_do_something_call)

        self._method_echo = MethodControls()
        self._method_echo.subscription_id = self._conn.subscribe("full/{}/method/echo".format(self._instance_id), self._process_echo_call)

        self._method_what_time_is_it = MethodControls()
        self._method_what_time_is_it.subscription_id = self._conn.subscribe("full/{}/method/whatTimeIsIt".format(self._instance_id), self._process_what_time_is_it_call)

        self._method_set_the_time = MethodControls()
        self._method_set_the_time.subscription_id = self._conn.subscribe("full/{}/method/setTheTime".format(self._instance_id), self._process_set_the_time_call)

        self._advertise_thread = threading.Thread(target=self.loop_publishing_interface_info)
        self._advertise_thread.start()

    def __del__(self):
        self._running = False
        self._conn.unpublish_retained(self._conn.online_topic)
        self._advertise_thread.join()

    def loop_publishing_interface_info(self):
        while self._conn.is_connected() and self._running:
            self._publish_interface_info()
            sleep(self._re_advertise_server_interval_seconds)

    def _publish_interface_info(self):
        data = InterfaceInfo(instance=self._instance_id, connection_topic=self._conn.online_topic, timestamp=datetime.utcnow().isoformat())
        expiry = int(self._re_advertise_server_interval_seconds * 1.2)  # slightly longer than the re-advertise interval
        topic = "full/{}/interface".format(self._instance_id)
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json())
        self._conn.publish_status(topic, data, expiry)

    def _receive_favorite_number_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = int(payload_obj["number"])
        with self._property_favorite_number.mutex:
            self._property_favorite_number.value = prop_value
            self._property_favorite_number.version += 1
        for callback in self._property_favorite_number.callbacks:
            callback(prop_value)

    def _receive_favorite_foods_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        prop_value = stinger_types.FavoriteFoodsProperty.model_validate_json(payload)
        with self._property_favorite_foods.mutex:
            self._property_favorite_foods.value = prop_value
            self._property_favorite_foods.version += 1
        for callback in self._property_favorite_foods.callbacks:
            callback(prop_value.drink, prop_value.slices_of_pizza, prop_value.breakfast)

    def _receive_lunch_menu_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        prop_value = stinger_types.LunchMenuProperty.model_validate_json(payload)
        with self._property_lunch_menu.mutex:
            self._property_lunch_menu.value = prop_value
            self._property_lunch_menu.version += 1
        for callback in self._property_lunch_menu.callbacks:
            callback(prop_value.monday, prop_value.tuesday)

    def _receive_family_name_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = str(payload_obj["family_name"])
        with self._property_family_name.mutex:
            self._property_family_name.value = prop_value
            self._property_family_name.version += 1
        for callback in self._property_family_name.callbacks:
            callback(prop_value)

    def _receive_last_breakfast_time_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = datetime.datetime(payload_obj["timestamp"])
        with self._property_last_breakfast_time.mutex:
            self._property_last_breakfast_time.value = prop_value
            self._property_last_breakfast_time.version += 1
        for callback in self._property_last_breakfast_time.callbacks:
            callback(prop_value)

    def _receive_last_birthdays_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        prop_value = stinger_types.LastBirthdaysProperty.model_validate_json(payload)
        with self._property_last_birthdays.mutex:
            self._property_last_birthdays.value = prop_value
            self._property_last_birthdays.version += 1
        for callback in self._property_last_birthdays.callbacks:
            callback(prop_value.mom, prop_value.dad, prop_value.sister)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message to %s", topic)

    def emit_todayIs(self, dayOfMonth: int, dayOfWeek: Optional[stinger_types.DayOfTheWeek]):
        """Server application code should call this method to emit the 'todayIs' signal."""
        if not isinstance(dayOfMonth, int):
            raise ValueError(f"The 'dayOfMonth' value must be int.")
        if not isinstance(dayOfWeek, stinger_types.DayOfTheWeek) and dayOfWeek is not None:
            raise ValueError(f"The 'dayOfWeek' value must be Optional[stinger_types.DayOfTheWeek].")

        payload = {
            "dayOfMonth": int(dayOfMonth),
            "dayOfWeek": stinger_types.DayOfTheWeek(dayOfWeek).value if dayOfWeek is not None else None,
        }
        self._conn.publish("full/{}/signal/todayIs".format(self._instance_id), json.dumps(payload), qos=1, retain=False)

    def handle_add_numbers(self, handler: Callable[[int, int, Optional[int]], int]):
        """This is a decorator to decorate a method that will handle the 'addNumbers' method calls."""
        if self._method_add_numbers.callback is None and handler is not None:
            self._method_add_numbers.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_add_numbers_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'addNumbers' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = json.loads(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._method_add_numbers.callback is not None:
            method_args = []  # type: List[Any]
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
                if not isinstance(payload["third"], int) or payload["third"] is None:
                    self._logger.warning("The 'third' property in the payload to '%s' wasn't the correct type.  It should have been Optional[int].", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["third"])
            else:

                method_args.append(None)

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._method_add_numbers.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"sum": return_struct})
                except Exception as e:
                    self._logger.exception("Exception while handling addNumbers", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_do_something(self, handler: Callable[[str], stinger_types.DoSomethingReturnValue]):
        """This is a decorator to decorate a method that will handle the 'doSomething' method calls."""
        if self._method_do_something.callback is None and handler is not None:
            self._method_do_something.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_do_something_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'doSomething' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = json.loads(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._method_do_something.callback is not None:
            method_args = []  # type: List[Any]
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
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._method_do_something.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling doSomething", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_echo(self, handler: Callable[[str], str]):
        """This is a decorator to decorate a method that will handle the 'echo' method calls."""
        if self._method_echo.callback is None and handler is not None:
            self._method_echo.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_echo_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'echo' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = json.loads(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._method_echo.callback is not None:
            method_args = []  # type: List[Any]
            if "message" in payload:
                if not isinstance(payload["message"], str):
                    self._logger.warning("The 'message' property in the payload to '%s' wasn't the correct type.  It should have been str.", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["message"])
            else:

                self._logger.warning("The 'message' property in the payload to '%s' wasn't present", topic)
                # TODO: return an error via MQTT
                return

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._method_echo.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"message": return_struct})
                except Exception as e:
                    self._logger.exception("Exception while handling echo", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_what_time_is_it(self, handler: Callable[[datetime.datetime], datetime.datetime]):
        """This is a decorator to decorate a method that will handle the 'what_time_is_it' method calls."""
        if self._method_what_time_is_it.callback is None and handler is not None:
            self._method_what_time_is_it.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_what_time_is_it_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'what_time_is_it' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = json.loads(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._method_what_time_is_it.callback is not None:
            method_args = []  # type: List[Any]
            if "the_first_time" in payload:
                if not isinstance(payload["the_first_time"], datetime.datetime):
                    self._logger.warning("The 'the_first_time' property in the payload to '%s' wasn't the correct type.  It should have been datetime.datetime.", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["the_first_time"])
            else:

                self._logger.warning("The 'the_first_time' property in the payload to '%s' wasn't present", topic)
                # TODO: return an error via MQTT
                return

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._method_what_time_is_it.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling what_time_is_it", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodReturnCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)

    def handle_set_the_time(self, handler: Callable[[datetime.datetime, datetime.datetime], stinger_types.SetTheTimeReturnValue]):
        """This is a decorator to decorate a method that will handle the 'set_the_time' method calls."""
        if self._method_set_the_time.callback is None and handler is not None:
            self._method_set_the_time.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_set_the_time_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'set_the_time' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = json.loads(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._method_set_the_time.callback is not None:
            method_args = []  # type: List[Any]
            if "the_first_time" in payload:
                if not isinstance(payload["the_first_time"], datetime.datetime):
                    self._logger.warning("The 'the_first_time' property in the payload to '%s' wasn't the correct type.  It should have been datetime.datetime.", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["the_first_time"])
            else:

                self._logger.warning("The 'the_first_time' property in the payload to '%s' wasn't present", topic)
                # TODO: return an error via MQTT
                return

            if "the_second_time" in payload:
                if not isinstance(payload["the_second_time"], datetime.datetime):
                    self._logger.warning("The 'the_second_time' property in the payload to '%s' wasn't the correct type.  It should have been datetime.datetime.", topic)
                    # TODO: return an error via MQTT
                    return
                else:
                    method_args.append(payload["the_second_time"])
            else:

                self._logger.warning("The 'the_second_time' property in the payload to '%s' wasn't present", topic)
                # TODO: return an error via MQTT
                return

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._method_set_the_time.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = json.dumps({"set_the_time": return_struct.model_dump_json()})

                except Exception as e:
                    self._logger.exception("Exception while handling set_the_time", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodReturnCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)

    @property
    def favorite_number(self) -> int | None:
        """This property returns the last received value for the 'favorite_number' property."""
        with self._property_favorite_number_mutex:
            return self._property_favorite_number

    @favorite_number.setter
    def favorite_number(self, number: int):
        """This property sets (publishes) a new value for the 'favorite_number' property."""
        if not isinstance(number, int):
            raise ValueError(f"The value must be int.")

        payload = json.dumps({"number": number})

        if number != self._property_favorite_number.value:
            with self._property_favorite_number.mutex:
                self._property_favorite_number.value = number
                self._property_favorite_number.version += 1
            self._conn.publish("full/{}/property/favoriteNumber/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_favorite_number.callbacks:
                callback(number)

    def set_favorite_number(self, number: int):
        """This method sets (publishes) a new value for the 'favorite_number' property."""
        if not isinstance(number, int):
            raise ValueError(f"The 'number' value must be int.")

        obj = number

        # Use the property.setter to do that actual work.
        self.favorite_number = obj

    def on_favorite_number_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'favorite_number' property update is received."""
        if handler is not None:
            self._property_favorite_number.callbacks.append(handler)

    @property
    def favorite_foods(self) -> stinger_types.FavoriteFoodsProperty | None:
        """This property returns the last received value for the 'favorite_foods' property."""
        with self._property_favorite_foods_mutex:
            return self._property_favorite_foods

    @favorite_foods.setter
    def favorite_foods(self, value: stinger_types.FavoriteFoodsProperty):
        """This property sets (publishes) a new value for the 'favorite_foods' property."""
        if not isinstance(value, stinger_types.FavoriteFoodsProperty):
            raise ValueError(f"The value must be stinger_types.FavoriteFoodsProperty.")

        payload = value.model_dump_json()

        if value != self._property_favorite_foods.value:
            with self._property_favorite_foods.mutex:
                self._property_favorite_foods.value = value
                self._property_favorite_foods.version += 1
            self._conn.publish("full/{}/property/favoriteFoods/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_favorite_foods.callbacks:
                callback(value.drink, value.slices_of_pizza, value.breakfast)

    def set_favorite_foods(self, drink: str, slices_of_pizza: int, breakfast: Optional[str]):
        """This method sets (publishes) a new value for the 'favorite_foods' property."""
        if not isinstance(drink, str):
            raise ValueError(f"The 'drink' value must be str.")
        if not isinstance(slices_of_pizza, int):
            raise ValueError(f"The 'slices_of_pizza' value must be int.")
        if not isinstance(breakfast, str) and breakfast is not None:
            raise ValueError(f"The 'breakfast' value must be Optional[str].")

        obj = stinger_types.FavoriteFoodsProperty(
            drink=drink,
            slices_of_pizza=slices_of_pizza,
            breakfast=breakfast,
        )

        # Use the property.setter to do that actual work.
        self.favorite_foods = obj

    def on_favorite_foods_updates(self, handler: Callable[[str, int, Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'favorite_foods' property update is received."""
        if handler is not None:
            self._property_favorite_foods.callbacks.append(handler)

    @property
    def lunch_menu(self) -> stinger_types.LunchMenuProperty | None:
        """This property returns the last received value for the 'lunch_menu' property."""
        with self._property_lunch_menu_mutex:
            return self._property_lunch_menu

    @lunch_menu.setter
    def lunch_menu(self, value: stinger_types.LunchMenuProperty):
        """This property sets (publishes) a new value for the 'lunch_menu' property."""
        if not isinstance(value, stinger_types.LunchMenuProperty):
            raise ValueError(f"The value must be stinger_types.LunchMenuProperty.")

        payload = value.model_dump_json()

        if value != self._property_lunch_menu.value:
            with self._property_lunch_menu.mutex:
                self._property_lunch_menu.value = value
                self._property_lunch_menu.version += 1
            self._conn.publish("full/{}/property/lunchMenu/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_lunch_menu.callbacks:
                callback(value.monday, value.tuesday)

    def set_lunch_menu(self, monday: stinger_types.Lunch, tuesday: stinger_types.Lunch):
        """This method sets (publishes) a new value for the 'lunch_menu' property."""
        if not isinstance(monday, stinger_types.Lunch):
            raise ValueError(f"The 'monday' value must be stinger_types.Lunch.")
        if not isinstance(tuesday, stinger_types.Lunch):
            raise ValueError(f"The 'tuesday' value must be stinger_types.Lunch.")

        obj = stinger_types.LunchMenuProperty(
            monday=monday,
            tuesday=tuesday,
        )

        # Use the property.setter to do that actual work.
        self.lunch_menu = obj

    def on_lunch_menu_updates(self, handler: Callable[[stinger_types.Lunch, stinger_types.Lunch], None]):
        """This method registers a callback to be called whenever a new 'lunch_menu' property update is received."""
        if handler is not None:
            self._property_lunch_menu.callbacks.append(handler)

    @property
    def family_name(self) -> str | None:
        """This property returns the last received value for the 'family_name' property."""
        with self._property_family_name_mutex:
            return self._property_family_name

    @family_name.setter
    def family_name(self, family_name: str):
        """This property sets (publishes) a new value for the 'family_name' property."""
        if not isinstance(family_name, str):
            raise ValueError(f"The value must be str.")

        payload = json.dumps({"family_name": family_name})

        if family_name != self._property_family_name.value:
            with self._property_family_name.mutex:
                self._property_family_name.value = family_name
                self._property_family_name.version += 1
            self._conn.publish("full/{}/property/familyName/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_family_name.callbacks:
                callback(family_name)

    def set_family_name(self, family_name: str):
        """This method sets (publishes) a new value for the 'family_name' property."""
        if not isinstance(family_name, str):
            raise ValueError(f"The 'family_name' value must be str.")

        obj = family_name

        # Use the property.setter to do that actual work.
        self.family_name = obj

    def on_family_name_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'family_name' property update is received."""
        if handler is not None:
            self._property_family_name.callbacks.append(handler)

    @property
    def last_breakfast_time(self) -> datetime.datetime | None:
        """This property returns the last received value for the 'last_breakfast_time' property."""
        with self._property_last_breakfast_time_mutex:
            return self._property_last_breakfast_time

    @last_breakfast_time.setter
    def last_breakfast_time(self, timestamp: datetime.datetime):
        """This property sets (publishes) a new value for the 'last_breakfast_time' property."""
        if not isinstance(timestamp, datetime.datetime):
            raise ValueError(f"The value must be datetime.datetime.")

        payload = json.dumps({"timestamp": timestamp})

        if timestamp != self._property_last_breakfast_time.value:
            with self._property_last_breakfast_time.mutex:
                self._property_last_breakfast_time.value = timestamp
                self._property_last_breakfast_time.version += 1
            self._conn.publish("full/{}/property/lastBreakfastTime/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_last_breakfast_time.callbacks:
                callback(timestamp)

    def set_last_breakfast_time(self, timestamp: datetime.datetime):
        """This method sets (publishes) a new value for the 'last_breakfast_time' property."""
        if not isinstance(timestamp, datetime.datetime):
            raise ValueError(f"The 'timestamp' value must be datetime.datetime.")

        obj = timestamp

        # Use the property.setter to do that actual work.
        self.last_breakfast_time = obj

    def on_last_breakfast_time_updates(self, handler: Callable[[datetime.datetime], None]):
        """This method registers a callback to be called whenever a new 'last_breakfast_time' property update is received."""
        if handler is not None:
            self._property_last_breakfast_time.callbacks.append(handler)

    @property
    def last_birthdays(self) -> stinger_types.LastBirthdaysProperty | None:
        """This property returns the last received value for the 'last_birthdays' property."""
        with self._property_last_birthdays_mutex:
            return self._property_last_birthdays

    @last_birthdays.setter
    def last_birthdays(self, value: stinger_types.LastBirthdaysProperty):
        """This property sets (publishes) a new value for the 'last_birthdays' property."""
        if not isinstance(value, stinger_types.LastBirthdaysProperty):
            raise ValueError(f"The value must be stinger_types.LastBirthdaysProperty.")

        payload = value.model_dump_json()

        if value != self._property_last_birthdays.value:
            with self._property_last_birthdays.mutex:
                self._property_last_birthdays.value = value
                self._property_last_birthdays.version += 1
            self._conn.publish("full/{}/property/lastBirthdays/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_last_birthdays.callbacks:
                callback(value.mom, value.dad, value.sister)

    def set_last_birthdays(self, mom: datetime.datetime, dad: datetime.datetime, sister: datetime.datetime):
        """This method sets (publishes) a new value for the 'last_birthdays' property."""
        if not isinstance(mom, datetime.datetime):
            raise ValueError(f"The 'mom' value must be datetime.datetime.")
        if not isinstance(dad, datetime.datetime):
            raise ValueError(f"The 'dad' value must be datetime.datetime.")
        if not isinstance(sister, datetime.datetime) and sister is not None:
            raise ValueError(f"The 'sister' value must be datetime.datetime.")

        obj = stinger_types.LastBirthdaysProperty(
            mom=mom,
            dad=dad,
            sister=sister,
        )

        # Use the property.setter to do that actual work.
        self.last_birthdays = obj

    def on_last_birthdays_updates(self, handler: Callable[[datetime.datetime, datetime.datetime, datetime.datetime], None]):
        """This method registers a callback to be called whenever a new 'last_birthdays' property update is received."""
        if handler is not None:
            self._property_last_birthdays.callbacks.append(handler)


class FullServerBuilder:
    """
    This is a builder for the FullServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):

        self._add_numbers_method_handler: Optional[Callable[[int, int, Optional[int]], int]] = None
        self._do_something_method_handler: Optional[Callable[[str], stinger_types.DoSomethingReturnValue]] = None
        self._echo_method_handler: Optional[Callable[[str], str]] = None
        self._what_time_is_it_method_handler: Optional[Callable[[datetime.datetime], datetime.datetime]] = None
        self._set_the_time_method_handler: Optional[Callable[[datetime.datetime, datetime.datetime], stinger_types.SetTheTimeReturnValue]] = None

        self._favorite_number_property_callbacks: List[Callable[[int], None]] = []
        self._favorite_foods_property_callbacks: List[Callable[[str, int, Optional[str]], None]] = []
        self._lunch_menu_property_callbacks: List[Callable[[stinger_types.Lunch, stinger_types.Lunch], None]] = []
        self._family_name_property_callbacks: List[Callable[[str], None]] = []
        self._last_breakfast_time_property_callbacks: List[Callable[[datetime.datetime], None]] = []
        self._last_birthdays_property_callbacks: List[Callable[[datetime.datetime, datetime.datetime, datetime.datetime], None]] = []

    def handle_add_numbers(self, handler: Callable[[int, int, Optional[int]], int]):
        if self._add_numbers_method_handler is None and handler is not None:
            self._add_numbers_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_do_something(self, handler: Callable[[str], stinger_types.DoSomethingReturnValue]):
        if self._do_something_method_handler is None and handler is not None:
            self._do_something_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_echo(self, handler: Callable[[str], str]):
        if self._echo_method_handler is None and handler is not None:
            self._echo_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_what_time_is_it(self, handler: Callable[[datetime.datetime], datetime.datetime]):
        if self._what_time_is_it_method_handler is None and handler is not None:
            self._what_time_is_it_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_set_the_time(self, handler: Callable[[datetime.datetime, datetime.datetime], stinger_types.SetTheTimeReturnValue]):
        if self._set_the_time_method_handler is None and handler is not None:
            self._set_the_time_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def on_favorite_number_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'favorite_number' property update is received."""
        self._favorite_number_property_callbacks.append(handler)

    def on_favorite_foods_updates(self, handler: Callable[[str, int, Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'favorite_foods' property update is received."""
        self._favorite_foods_property_callbacks.append(handler)

    def on_lunch_menu_updates(self, handler: Callable[[stinger_types.Lunch, stinger_types.Lunch], None]):
        """This method registers a callback to be called whenever a new 'lunch_menu' property update is received."""
        self._lunch_menu_property_callbacks.append(handler)

    def on_family_name_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'family_name' property update is received."""
        self._family_name_property_callbacks.append(handler)

    def on_last_breakfast_time_updates(self, handler: Callable[[datetime.datetime], None]):
        """This method registers a callback to be called whenever a new 'last_breakfast_time' property update is received."""
        self._last_breakfast_time_property_callbacks.append(handler)

    def on_last_birthdays_updates(self, handler: Callable[[datetime.datetime, datetime.datetime, datetime.datetime], None]):
        """This method registers a callback to be called whenever a new 'last_birthdays' property update is received."""
        self._last_birthdays_property_callbacks.append(handler)

    def build(self, connection: IBrokerConnection) -> FullServer:
        new_server = FullServer(connection)

        if self._add_numbers_method_handler is not None:
            new_server.handle_add_numbers(self._add_numbers_method_handler)
        if self._do_something_method_handler is not None:
            new_server.handle_do_something(self._do_something_method_handler)
        if self._echo_method_handler is not None:
            new_server.handle_echo(self._echo_method_handler)
        if self._what_time_is_it_method_handler is not None:
            new_server.handle_what_time_is_it(self._what_time_is_it_method_handler)
        if self._set_the_time_method_handler is not None:
            new_server.handle_set_the_time(self._set_the_time_method_handler)

        for callback in self._favorite_number_property_callbacks:
            new_server.on_favorite_number_updates(callback)

        for callback in self._favorite_foods_property_callbacks:
            new_server.on_favorite_foods_updates(callback)

        for callback in self._lunch_menu_property_callbacks:
            new_server.on_lunch_menu_updates(callback)

        for callback in self._family_name_property_callbacks:
            new_server.on_family_name_updates(callback)

        for callback in self._last_breakfast_time_property_callbacks:
            new_server.on_last_breakfast_time_updates(callback)

        for callback in self._last_birthdays_property_callbacks:
            new_server.on_last_birthdays_updates(callback)

        return new_server


if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal
    from connection import MqttBrokerConnection, MqttTransport, MqttTransportType

    transport = MqttTransport(MqttTransportType.TCP, "localhost", 1883)
    conn = MqttBrokerConnection(transport)
    server = FullServer(conn, "demo")

    server.favorite_number = 42

    server.favorite_foods = stinger_types.FavoriteFoodsProperty(
        drink="apples",
        slices_of_pizza=42,
        breakfast="apples",
    )

    server.lunch_menu = stinger_types.LunchMenuProperty(
        monday=stinger_types.Lunch(drink=True, sandwich="apples", crackers=3.14, day=stinger_types.DayOfTheWeek.MONDAY, order_number=42),
        tuesday=stinger_types.Lunch(drink=True, sandwich="apples", crackers=3.14, day=stinger_types.DayOfTheWeek.MONDAY, order_number=42),
    )

    server.family_name = "apples"

    server.last_breakfast_time = datetime.datetime.now()

    server.last_birthdays = stinger_types.LastBirthdaysProperty(
        mom=datetime.datetime.now(),
        dad=datetime.datetime.now(),
        sister=datetime.datetime.now(),
    )

    @server.handle_add_numbers
    def add_numbers(first: int, second: int, third: Optional[int]) -> int:
        """This is an example handler for the 'addNumbers' method."""
        print(f"Running add_numbers'({first}, {second}, {third})'")
        return 42

    @server.handle_do_something
    def do_something(aString: str) -> stinger_types.DoSomethingReturnValue:
        """This is an example handler for the 'doSomething' method."""
        print(f"Running do_something'({aString})'")
        return stinger_types.DoSomethingReturnValue(label="apples", identifier=42, day=stinger_types.DayOfTheWeek.MONDAY)

    @server.handle_echo
    def echo(message: str) -> str:
        """This is an example handler for the 'echo' method."""
        print(f"Running echo'({message})'")
        return "apples"

    @server.handle_what_time_is_it
    def what_time_is_it(the_first_time: datetime.datetime) -> datetime.datetime:
        """This is an example handler for the 'what_time_is_it' method."""
        print(f"Running what_time_is_it'({the_first_time})'")
        return datetime.datetime.now()

    @server.handle_set_the_time
    def set_the_time(the_first_time: datetime.datetime, the_second_time: datetime.datetime) -> stinger_types.SetTheTimeReturnValue:
        """This is an example handler for the 'set_the_time' method."""
        print(f"Running set_the_time'({the_first_time}, {the_second_time})'")
        return ["datetime.datetime.now()", '"apples"']

    @server.on_favorite_number_updates
    def on_favorite_number_update(number: int):
        print(f"Received update for 'favorite_number' property: { number= }")

    @server.on_favorite_foods_updates
    def on_favorite_foods_update(drink: str, slices_of_pizza: int, breakfast: Optional[str]):
        print(f"Received update for 'favorite_foods' property: { drink= }, { slices_of_pizza= }, { breakfast= }")

    @server.on_lunch_menu_updates
    def on_lunch_menu_update(monday: stinger_types.Lunch, tuesday: stinger_types.Lunch):
        print(f"Received update for 'lunch_menu' property: { monday= }, { tuesday= }")

    @server.on_family_name_updates
    def on_family_name_update(family_name: str):
        print(f"Received update for 'family_name' property: { family_name= }")

    @server.on_last_breakfast_time_updates
    def on_last_breakfast_time_update(timestamp: datetime.datetime):
        print(f"Received update for 'last_breakfast_time' property: { timestamp= }")

    @server.on_last_birthdays_updates
    def on_last_birthdays_update(mom: datetime.datetime, dad: datetime.datetime, sister: datetime.datetime):
        print(f"Received update for 'last_birthdays' property: { mom= }, { dad= }, { sister= }")

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
