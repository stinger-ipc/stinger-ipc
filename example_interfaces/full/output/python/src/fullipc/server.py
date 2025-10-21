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
from datetime import datetime, timedelta, UTC
import isodate

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel, ValidationError
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from .connection import IBrokerConnection
from .method_codes import *
from .interface_types import *


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
    value: T | None = None
    mutex = threading.Lock()
    version: int = -1
    subscription_id: Optional[int] = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)


@dataclass
class MethodControls:
    subscription_id: Optional[int] = None
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

        self._property_favorite_foods: PropertyControls[FavoriteFoodsProperty, str, int, Optional[str]] = PropertyControls()
        self._property_favorite_foods.subscription_id = self._conn.subscribe("full/{}/property/favoriteFoods/setValue".format(self._instance_id), self._receive_favorite_foods_update_request_message)

        self._property_lunch_menu: PropertyControls[LunchMenuProperty, Lunch, Lunch] = PropertyControls()
        self._property_lunch_menu.subscription_id = self._conn.subscribe("full/{}/property/lunchMenu/setValue".format(self._instance_id), self._receive_lunch_menu_update_request_message)

        self._property_family_name: PropertyControls[str, str] = PropertyControls()
        self._property_family_name.subscription_id = self._conn.subscribe("full/{}/property/familyName/setValue".format(self._instance_id), self._receive_family_name_update_request_message)

        self._property_last_breakfast_time: PropertyControls[datetime, datetime] = PropertyControls()
        self._property_last_breakfast_time.subscription_id = self._conn.subscribe(
            "full/{}/property/lastBreakfastTime/setValue".format(self._instance_id), self._receive_last_breakfast_time_update_request_message
        )

        self._property_breakfast_length: PropertyControls[timedelta, timedelta] = PropertyControls()
        self._property_breakfast_length.subscription_id = self._conn.subscribe(
            "full/{}/property/breakfastLength/setValue".format(self._instance_id), self._receive_breakfast_length_update_request_message
        )

        self._property_last_birthdays: PropertyControls[LastBirthdaysProperty, datetime, datetime, Optional[datetime], Optional[int]] = PropertyControls()
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

        self._method_forward_time = MethodControls()
        self._method_forward_time.subscription_id = self._conn.subscribe("full/{}/method/forwardTime".format(self._instance_id), self._process_forward_time_call)

        self._method_how_off_is_the_clock = MethodControls()
        self._method_how_off_is_the_clock.subscription_id = self._conn.subscribe("full/{}/method/howOffIsTheClock".format(self._instance_id), self._process_how_off_is_the_clock_call)

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
        data = InterfaceInfo(instance=self._instance_id, connection_topic=self._conn.online_topic, timestamp=datetime.now(UTC).isoformat())
        expiry = int(self._re_advertise_server_interval_seconds * 1.2)  # slightly longer than the re-advertise interval
        topic = "full/{}/interface".format(self._instance_id)
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json(by_alias=True))
        self._conn.publish_status(topic, data, expiry)

    def _send_reply_error_message(self, return_code: MethodReturnCode, request_properties: Dict[str, Any], debug_info: Optional[str] = None):
        correlation_id = request_properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = request_properties.get("ResponseTopic")  # type: Optional[str]
        if response_topic is not None:
            self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_info)

    def _receive_favorite_number_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = int(payload_obj["number"])
        with self._property_favorite_number.mutex:
            self._property_favorite_number.value = prop_value
            self._property_favorite_number.version += 1
        for callback in self._property_favorite_number.callbacks:
            callback(prop_value)

    def _receive_favorite_foods_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = FavoriteFoodsProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_favorite_foods.mutex:
            self._property_favorite_foods.value = prop_value
            self._property_favorite_foods.version += 1
        for callback in self._property_favorite_foods.callbacks:
            callback(prop_value.drink, prop_value.slices_of_pizza, prop_value.breakfast)

    def _receive_lunch_menu_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = LunchMenuProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
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
        prop_value = datetime(payload_obj["timestamp"])
        with self._property_last_breakfast_time.mutex:
            self._property_last_breakfast_time.value = prop_value
            self._property_last_breakfast_time.version += 1
        for callback in self._property_last_breakfast_time.callbacks:
            callback(prop_value)

    def _receive_breakfast_length_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = timedelta(payload_obj["length"])
        with self._property_breakfast_length.mutex:
            self._property_breakfast_length.value = prop_value
            self._property_breakfast_length.version += 1
        for callback in self._property_breakfast_length.callbacks:
            callback(prop_value)

    def _receive_last_birthdays_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        try:
            prop_value = LastBirthdaysProperty.model_validate_json(payload)
        except ValidationError as e:
            self._logger.error("Failed to validate payload for %s: %s", topic, e)
            self._send_reply_error_message(MethodReturnCode.DESERIALIZATION_ERROR, properties, str(e))
            return
        with self._property_last_birthdays.mutex:
            self._property_last_birthdays.value = prop_value
            self._property_last_birthdays.version += 1
        for callback in self._property_last_birthdays.callbacks:
            callback(prop_value.mom, prop_value.dad, prop_value.sister, prop_value.brothers_age)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message to %s", topic)

    def emit_today_is(self, day_of_month: int, day_of_week: Optional[DayOfTheWeek], timestamp: datetime, process_time: timedelta, memory_segment: bytes):
        """Server application code should call this method to emit the 'todayIs' signal.

        TodayIsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(day_of_month, int), f"The 'dayOfMonth' argument must be of type int, but was {type(day_of_month)}"

        assert isinstance(day_of_week, DayOfTheWeek) or day_of_week is None, f"The 'dayOfWeek' argument must be of type Optional[DayOfTheWeek], but was {type(day_of_week)}"

        assert isinstance(timestamp, datetime), f"The 'timestamp' argument must be of type datetime, but was {type(timestamp)}"

        assert isinstance(process_time, timedelta), f"The 'process_time' argument must be of type timedelta, but was {type(process_time)}"

        assert isinstance(memory_segment, bytes), f"The 'memory_segment' argument must be of type bytes, but was {type(memory_segment)}"

        payload = TodayIsSignalPayload(
            day_of_month=day_of_month,
            day_of_week=day_of_week if day_of_week is not None else None,
            timestamp=timestamp,
            process_time=process_time,
            memory_segment=memory_segment,
        )
        self._conn.publish("full/{}/signal/todayIs".format(self._instance_id), payload.model_dump_json(by_alias=True), qos=1, retain=False)

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
        payload = AddNumbersMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'addNumbers' request: %s", correlation_id)
        if self._method_add_numbers.callback is not None:
            method_args = [
                payload.first,
                payload.second,
                payload.third,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_add_numbers.callback(*method_args)

                    if not isinstance(return_values, int):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type int, but was {type(return_values)}")
                    ret_obj = AddNumbersMethodResponse(sum=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling addNumbers: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling addNumbers", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_do_something(self, handler: Callable[[str], DoSomethingMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'doSomething' method calls."""
        if self._method_do_something.callback is None and handler is not None:
            self._method_do_something.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_do_something_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'doSomething' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = DoSomethingMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'doSomething' request: %s", correlation_id)
        if self._method_do_something.callback is not None:
            method_args = [
                payload.a_string,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_do_something.callback(*method_args)

                    if not isinstance(return_values, DoSomethingMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type DoSomethingMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling doSomething: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
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
        payload = EchoMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'echo' request: %s", correlation_id)
        if self._method_echo.callback is not None:
            method_args = [
                payload.message,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_echo.callback(*method_args)

                    if not isinstance(return_values, str):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type str, but was {type(return_values)}")
                    ret_obj = EchoMethodResponse(message=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling echo: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling echo", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_what_time_is_it(self, handler: Callable[[datetime], datetime]):
        """This is a decorator to decorate a method that will handle the 'what_time_is_it' method calls."""
        if self._method_what_time_is_it.callback is None and handler is not None:
            self._method_what_time_is_it.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_what_time_is_it_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'what_time_is_it' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = WhatTimeIsItMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'what_time_is_it' request: %s", correlation_id)
        if self._method_what_time_is_it.callback is not None:
            method_args = [
                payload.the_first_time,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_what_time_is_it.callback(*method_args)

                    if not isinstance(return_values, datetime):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type datetime, but was {type(return_values)}")
                    ret_obj = WhatTimeIsItMethodResponse(timestamp=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling what_time_is_it: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling what_time_is_it", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_set_the_time(self, handler: Callable[[datetime, datetime], SetTheTimeMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'set_the_time' method calls."""
        if self._method_set_the_time.callback is None and handler is not None:
            self._method_set_the_time.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_set_the_time_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'set_the_time' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = SetTheTimeMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'set_the_time' request: %s", correlation_id)
        if self._method_set_the_time.callback is not None:
            method_args = [
                payload.the_first_time,
                payload.the_second_time,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_set_the_time.callback(*method_args)

                    if not isinstance(return_values, SetTheTimeMethodResponse):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type SetTheTimeMethodResponse, but was {type(return_values)}")
                    return_json = return_values.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling set_the_time: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling set_the_time", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_forward_time(self, handler: Callable[[timedelta], datetime]):
        """This is a decorator to decorate a method that will handle the 'forward_time' method calls."""
        if self._method_forward_time.callback is None and handler is not None:
            self._method_forward_time.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_forward_time_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'forward_time' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = ForwardTimeMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'forward_time' request: %s", correlation_id)
        if self._method_forward_time.callback is not None:
            method_args = [
                payload.adjustment,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_forward_time.callback(*method_args)

                    if not isinstance(return_values, datetime):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type datetime, but was {type(return_values)}")
                    ret_obj = ForwardTimeMethodResponse(new_time=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling forward_time: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling forward_time", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    def handle_how_off_is_the_clock(self, handler: Callable[[datetime], timedelta]):
        """This is a decorator to decorate a method that will handle the 'how_off_is_the_clock' method calls."""
        if self._method_how_off_is_the_clock.callback is None and handler is not None:
            self._method_how_off_is_the_clock.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_how_off_is_the_clock_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'how_off_is_the_clock' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = HowOffIsTheClockMethodRequest.model_validate_json(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.debug("Correlation data for 'how_off_is_the_clock' request: %s", correlation_id)
        if self._method_how_off_is_the_clock.callback is not None:
            method_args = [
                payload.actual_time,
            ]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_how_off_is_the_clock.callback(*method_args)

                    if not isinstance(return_values, timedelta):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type timedelta, but was {type(return_values)}")
                    ret_obj = HowOffIsTheClockMethodResponse(difference=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling how_off_is_the_clock: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling how_off_is_the_clock", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    self._conn.publish_error_response(response_topic, return_code, correlation_id, debug_info=debug_msg)
                else:
                    self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id)

    @property
    def favorite_number(self) -> Optional[int]:
        """This property returns the last received value for the 'favorite_number' property."""
        with self._property_favorite_number_mutex:
            return self._property_favorite_number

    @favorite_number.setter
    def favorite_number(self, number: int):
        """This property sets (publishes) a new value for the 'favorite_number' property."""

        if not isinstance(number, int):
            raise ValueError(f"The value must be int .")

        prop_obj = FavoriteNumberProperty(number=number)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_favorite_number.value is None or number != self._property_favorite_number.value.number:
            with self._property_favorite_number.mutex:
                self._property_favorite_number.value = prop_obj
                self._property_favorite_number.version += 1
            self._conn.publish("full/{}/property/favoriteNumber/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_favorite_number.callbacks:
                callback(prop_obj.number)

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
    def favorite_foods(self) -> Optional[FavoriteFoodsProperty]:
        """This property returns the last received value for the 'favorite_foods' property."""
        with self._property_favorite_foods_mutex:
            return self._property_favorite_foods

    @favorite_foods.setter
    def favorite_foods(self, value: FavoriteFoodsProperty):
        """This property sets (publishes) a new value for the 'favorite_foods' property."""

        if not isinstance(value, FavoriteFoodsProperty):
            raise ValueError(f"The value must be FavoriteFoodsProperty.")

        payload = value.model_dump_json(by_alias=True)

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

        obj = interface_types.FavoriteFoodsProperty(
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
    def lunch_menu(self) -> Optional[LunchMenuProperty]:
        """This property returns the last received value for the 'lunch_menu' property."""
        with self._property_lunch_menu_mutex:
            return self._property_lunch_menu

    @lunch_menu.setter
    def lunch_menu(self, value: LunchMenuProperty):
        """This property sets (publishes) a new value for the 'lunch_menu' property."""

        if not isinstance(value, LunchMenuProperty):
            raise ValueError(f"The value must be LunchMenuProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_lunch_menu.value:
            with self._property_lunch_menu.mutex:
                self._property_lunch_menu.value = value
                self._property_lunch_menu.version += 1
            self._conn.publish("full/{}/property/lunchMenu/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_lunch_menu.callbacks:
                callback(value.monday, value.tuesday)

    def set_lunch_menu(self, monday: Lunch, tuesday: Lunch):
        """This method sets (publishes) a new value for the 'lunch_menu' property."""
        if not isinstance(monday, Lunch):
            raise ValueError(f"The 'monday' value must be Lunch.")
        if not isinstance(tuesday, Lunch):
            raise ValueError(f"The 'tuesday' value must be Lunch.")

        obj = interface_types.LunchMenuProperty(
            monday=monday,
            tuesday=tuesday,
        )

        # Use the property.setter to do that actual work.
        self.lunch_menu = obj

    def on_lunch_menu_updates(self, handler: Callable[[Lunch, Lunch], None]):
        """This method registers a callback to be called whenever a new 'lunch_menu' property update is received."""
        if handler is not None:
            self._property_lunch_menu.callbacks.append(handler)

    @property
    def family_name(self) -> Optional[str]:
        """This property returns the last received value for the 'family_name' property."""
        with self._property_family_name_mutex:
            return self._property_family_name

    @family_name.setter
    def family_name(self, family_name: str):
        """This property sets (publishes) a new value for the 'family_name' property."""

        if not isinstance(family_name, str):
            raise ValueError(f"The value must be str .")

        prop_obj = FamilyNameProperty(family_name=family_name)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_family_name.value is None or family_name != self._property_family_name.value.family_name:
            with self._property_family_name.mutex:
                self._property_family_name.value = prop_obj
                self._property_family_name.version += 1
            self._conn.publish("full/{}/property/familyName/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_family_name.callbacks:
                callback(prop_obj.family_name)

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
    def last_breakfast_time(self) -> Optional[datetime]:
        """This property returns the last received value for the 'last_breakfast_time' property."""
        with self._property_last_breakfast_time_mutex:
            return self._property_last_breakfast_time

    @last_breakfast_time.setter
    def last_breakfast_time(self, timestamp: datetime):
        """This property sets (publishes) a new value for the 'last_breakfast_time' property."""

        if not isinstance(timestamp, datetime):
            raise ValueError(f"The value must be datetime .")

        prop_obj = LastBreakfastTimeProperty(timestamp=timestamp)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_last_breakfast_time.value is None or timestamp != self._property_last_breakfast_time.value.timestamp:
            with self._property_last_breakfast_time.mutex:
                self._property_last_breakfast_time.value = prop_obj
                self._property_last_breakfast_time.version += 1
            self._conn.publish("full/{}/property/lastBreakfastTime/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_last_breakfast_time.callbacks:
                callback(prop_obj.timestamp)

    def set_last_breakfast_time(self, timestamp: datetime):
        """This method sets (publishes) a new value for the 'last_breakfast_time' property."""
        if not isinstance(timestamp, datetime):
            raise ValueError(f"The 'timestamp' value must be datetime.")

        obj = timestamp

        # Use the property.setter to do that actual work.
        self.last_breakfast_time = obj

    def on_last_breakfast_time_updates(self, handler: Callable[[datetime], None]):
        """This method registers a callback to be called whenever a new 'last_breakfast_time' property update is received."""
        if handler is not None:
            self._property_last_breakfast_time.callbacks.append(handler)

    @property
    def breakfast_length(self) -> Optional[timedelta]:
        """This property returns the last received value for the 'breakfast_length' property."""
        with self._property_breakfast_length_mutex:
            return self._property_breakfast_length

    @breakfast_length.setter
    def breakfast_length(self, length: timedelta):
        """This property sets (publishes) a new value for the 'breakfast_length' property."""

        if not isinstance(length, timedelta):
            raise ValueError(f"The value must be timedelta .")

        prop_obj = BreakfastLengthProperty(length=length)
        payload = prop_obj.model_dump_json(by_alias=True)

        if self._property_breakfast_length.value is None or length != self._property_breakfast_length.value.length:
            with self._property_breakfast_length.mutex:
                self._property_breakfast_length.value = prop_obj
                self._property_breakfast_length.version += 1
            self._conn.publish("full/{}/property/breakfastLength/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_breakfast_length.callbacks:
                callback(prop_obj.length)

    def set_breakfast_length(self, length: timedelta):
        """This method sets (publishes) a new value for the 'breakfast_length' property."""
        if not isinstance(length, timedelta):
            raise ValueError(f"The 'length' value must be timedelta.")

        obj = length

        # Use the property.setter to do that actual work.
        self.breakfast_length = obj

    def on_breakfast_length_updates(self, handler: Callable[[timedelta], None]):
        """This method registers a callback to be called whenever a new 'breakfast_length' property update is received."""
        if handler is not None:
            self._property_breakfast_length.callbacks.append(handler)

    @property
    def last_birthdays(self) -> Optional[LastBirthdaysProperty]:
        """This property returns the last received value for the 'last_birthdays' property."""
        with self._property_last_birthdays_mutex:
            return self._property_last_birthdays

    @last_birthdays.setter
    def last_birthdays(self, value: LastBirthdaysProperty):
        """This property sets (publishes) a new value for the 'last_birthdays' property."""

        if not isinstance(value, LastBirthdaysProperty):
            raise ValueError(f"The value must be LastBirthdaysProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_last_birthdays.value:
            with self._property_last_birthdays.mutex:
                self._property_last_birthdays.value = value
                self._property_last_birthdays.version += 1
            self._conn.publish("full/{}/property/lastBirthdays/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_last_birthdays.callbacks:
                callback(value.mom, value.dad, value.sister, value.brothers_age)

    def set_last_birthdays(self, mom: datetime, dad: datetime, sister: Optional[datetime], brothers_age: Optional[int]):
        """This method sets (publishes) a new value for the 'last_birthdays' property."""
        if not isinstance(mom, datetime):
            raise ValueError(f"The 'mom' value must be datetime.")
        if not isinstance(dad, datetime):
            raise ValueError(f"The 'dad' value must be datetime.")
        if not isinstance(sister, datetime) and sister is not None:
            raise ValueError(f"The 'sister' value must be Optional[datetime].")
        if not isinstance(brothers_age, int) and brothers_age is not None:
            raise ValueError(f"The 'brothers_age' value must be Optional[int].")

        obj = interface_types.LastBirthdaysProperty(
            mom=mom,
            dad=dad,
            sister=sister,
            brothers_age=brothers_age,
        )

        # Use the property.setter to do that actual work.
        self.last_birthdays = obj

    def on_last_birthdays_updates(self, handler: Callable[[datetime, datetime, Optional[datetime], Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'last_birthdays' property update is received."""
        if handler is not None:
            self._property_last_birthdays.callbacks.append(handler)


class FullServerBuilder:
    """
    This is a builder for the FullServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):

        self._add_numbers_method_handler: Optional[Callable[[int, int, Optional[int]], int]] = None
        self._do_something_method_handler: Optional[Callable[[str], DoSomethingMethodResponse]] = None
        self._echo_method_handler: Optional[Callable[[str], str]] = None
        self._what_time_is_it_method_handler: Optional[Callable[[datetime], datetime]] = None
        self._set_the_time_method_handler: Optional[Callable[[datetime, datetime], SetTheTimeMethodResponse]] = None
        self._forward_time_method_handler: Optional[Callable[[timedelta], datetime]] = None
        self._how_off_is_the_clock_method_handler: Optional[Callable[[datetime], timedelta]] = None

        self._favorite_number_property_callbacks: List[Callable[[int], None]] = []
        self._favorite_foods_property_callbacks: List[Callable[[str, int, Optional[str]], None]] = []
        self._lunch_menu_property_callbacks: List[Callable[[Lunch, Lunch], None]] = []
        self._family_name_property_callbacks: List[Callable[[str], None]] = []
        self._last_breakfast_time_property_callbacks: List[Callable[[datetime], None]] = []
        self._breakfast_length_property_callbacks: List[Callable[[timedelta], None]] = []
        self._last_birthdays_property_callbacks: List[Callable[[datetime, datetime, Optional[datetime], Optional[int]], None]] = []

    def handle_add_numbers(self, handler: Callable[[int, int, Optional[int]], int]):
        if self._add_numbers_method_handler is None and handler is not None:
            self._add_numbers_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_do_something(self, handler: Callable[[str], DoSomethingMethodResponse]):
        if self._do_something_method_handler is None and handler is not None:
            self._do_something_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_echo(self, handler: Callable[[str], str]):
        if self._echo_method_handler is None and handler is not None:
            self._echo_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_what_time_is_it(self, handler: Callable[[datetime], datetime]):
        if self._what_time_is_it_method_handler is None and handler is not None:
            self._what_time_is_it_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_set_the_time(self, handler: Callable[[datetime, datetime], SetTheTimeMethodResponse]):
        if self._set_the_time_method_handler is None and handler is not None:
            self._set_the_time_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_forward_time(self, handler: Callable[[timedelta], datetime]):
        if self._forward_time_method_handler is None and handler is not None:
            self._forward_time_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_how_off_is_the_clock(self, handler: Callable[[datetime], timedelta]):
        if self._how_off_is_the_clock_method_handler is None and handler is not None:
            self._how_off_is_the_clock_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def on_favorite_number_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'favorite_number' property update is received."""
        self._favorite_number_property_callbacks.append(handler)

    def on_favorite_foods_updates(self, handler: Callable[[str, int, Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'favorite_foods' property update is received."""
        self._favorite_foods_property_callbacks.append(handler)

    def on_lunch_menu_updates(self, handler: Callable[[Lunch, Lunch], None]):
        """This method registers a callback to be called whenever a new 'lunch_menu' property update is received."""
        self._lunch_menu_property_callbacks.append(handler)

    def on_family_name_updates(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'family_name' property update is received."""
        self._family_name_property_callbacks.append(handler)

    def on_last_breakfast_time_updates(self, handler: Callable[[datetime], None]):
        """This method registers a callback to be called whenever a new 'last_breakfast_time' property update is received."""
        self._last_breakfast_time_property_callbacks.append(handler)

    def on_breakfast_length_updates(self, handler: Callable[[timedelta], None]):
        """This method registers a callback to be called whenever a new 'breakfast_length' property update is received."""
        self._breakfast_length_property_callbacks.append(handler)

    def on_last_birthdays_updates(self, handler: Callable[[datetime, datetime, Optional[datetime], Optional[int]], None]):
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
        if self._forward_time_method_handler is not None:
            new_server.handle_forward_time(self._forward_time_method_handler)
        if self._how_off_is_the_clock_method_handler is not None:
            new_server.handle_how_off_is_the_clock(self._how_off_is_the_clock_method_handler)

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

        for callback in self._breakfast_length_property_callbacks:
            new_server.on_breakfast_length_updates(callback)

        for callback in self._last_birthdays_property_callbacks:
            new_server.on_last_birthdays_updates(callback)

        return new_server
