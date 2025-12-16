"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

import json
import logging
import threading
from time import sleep
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
import isodate
import functools
from concurrent.futures import Future

logging.basicConfig(level=logging.DEBUG)
from pydantic import BaseModel, ValidationError
from typing import Callable, Dict, Any, Optional, List, Generic, TypeVar
from pyqttier.interface import IBrokerConnection
from pyqttier.message import Message
from .method_codes import *
from .interface_types import *


from .property import FullInitialPropertyValues


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
    """
    Controls for a server property.  Generic[T] must be a single value or a pydantic BaseModel for multi-argument properties.
    """

    value: T
    mutex = threading.RLock()
    version: int = -1
    subscription_id: Optional[int] = None
    callbacks: List[Callable[[T], None]] = field(default_factory=list)

    def get_value(self) -> T:
        with self.mutex:
            return self.value

    def set_value(self, new_value: T) -> T:
        with self.mutex:
            self.value = new_value
            return self.value


@dataclass
class MethodControls:
    subscription_id: Optional[int] = None
    callback: Optional[Callable] = None


class FullServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str, initial_property_values: FullInitialPropertyValues):
        self._logger = logging.getLogger(f"FullServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing FullServer instance %s", instance_id)
        self._instance_id = instance_id
        self._service_advert_topic = "full/{}/interface".format(self._instance_id)
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._property_favorite_number: PropertyControls[int] = PropertyControls(value=initial_property_values.favorite_number, version=initial_property_values.favorite_number_version)
        self._property_favorite_number.subscription_id = self._conn.subscribe(
            "full/{}/property/favoriteNumber/setValue".format(self._instance_id), self._receive_favorite_number_update_request_message
        )

        self._property_favorite_foods: PropertyControls[FavoriteFoodsProperty] = PropertyControls(value=initial_property_values.favorite_foods, version=initial_property_values.favorite_foods_version)
        self._property_favorite_foods.subscription_id = self._conn.subscribe("full/{}/property/favoriteFoods/setValue".format(self._instance_id), self._receive_favorite_foods_update_request_message)

        self._property_lunch_menu: PropertyControls[LunchMenuProperty] = PropertyControls(value=initial_property_values.lunch_menu, version=initial_property_values.lunch_menu_version)

        self._property_family_name: PropertyControls[str] = PropertyControls(value=initial_property_values.family_name, version=initial_property_values.family_name_version)
        self._property_family_name.subscription_id = self._conn.subscribe("full/{}/property/familyName/setValue".format(self._instance_id), self._receive_family_name_update_request_message)

        self._property_last_breakfast_time: PropertyControls[datetime] = PropertyControls(
            value=initial_property_values.last_breakfast_time, version=initial_property_values.last_breakfast_time_version
        )
        self._property_last_breakfast_time.subscription_id = self._conn.subscribe(
            "full/{}/property/lastBreakfastTime/setValue".format(self._instance_id), self._receive_last_breakfast_time_update_request_message
        )

        self._property_last_birthdays: PropertyControls[LastBirthdaysProperty] = PropertyControls(value=initial_property_values.last_birthdays, version=initial_property_values.last_birthdays_version)
        self._property_last_birthdays.subscription_id = self._conn.subscribe("full/{}/property/lastBirthdays/setValue".format(self._instance_id), self._receive_last_birthdays_update_request_message)

        self._method_add_numbers = MethodControls()
        self._method_add_numbers.subscription_id = self._conn.subscribe("full/{}/method/addNumbers".format(self._instance_id), self._process_add_numbers_call)

        self._method_do_something = MethodControls()
        self._method_do_something.subscription_id = self._conn.subscribe("full/{}/method/doSomething".format(self._instance_id), self._process_do_something_call)

        self._method_what_time_is_it = MethodControls()
        self._method_what_time_is_it.subscription_id = self._conn.subscribe("full/{}/method/whatTimeIsIt".format(self._instance_id), self._process_what_time_is_it_call)

        self._method_hold_temperature = MethodControls()
        self._method_hold_temperature.subscription_id = self._conn.subscribe("full/{}/method/holdTemperature".format(self._instance_id), self._process_hold_temperature_call)

        self._publish_all_properties()
        self._logger.debug("Starting interface advertisement thread")
        self._advertise_thread = threading.Thread(target=self._loop_publishing_interface_info, daemon=True)
        self._advertise_thread.start()

    def __del__(self):
        self.shutdown()

    def shutdown(self, timeout: float = 5.0):
        """Gracefully shutdown the server and stop the advertisement thread."""
        if not self._running:
            return
        self._running = False
        self._conn.unpublish_retained(self._service_advert_topic)
        if hasattr(self, "_advertise_thread") and self._advertise_thread.is_alive():
            self._advertise_thread.join(timeout=timeout)

    @property
    def instance_id(self) -> str:
        """The instance ID of this server instance."""
        return self._instance_id

    def _loop_publishing_interface_info(self):
        """We have a discovery topic separate from the MQTT client discovery topic.
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
        """Publishes the interface info message to the interface info topic with an expiry interval."""
        data = InterfaceInfo(instance=self._instance_id, connection_topic=(self._conn.online_topic or ""), timestamp=datetime.now(UTC).isoformat())
        expiry = int(self._re_advertise_server_interval_seconds * 1.2)  # slightly longer than the re-advertise interval
        topic = self._service_advert_topic
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json(by_alias=True))
        msg = Message.status_message(topic, data, expiry)
        self._conn.publish(msg)

    def publish_favorite_number_value(self, *_, **__):
        """Publishes the current value of the 'favorite_number' property.

        Accepts unused args and kwargs to make this a usable callback for application code.

        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.

        """
        with self._property_favorite_number.mutex:
            self._property_favorite_number.version += 1
            favorite_number_prop_obj = FavoriteNumberProperty(number=self._property_favorite_number.get_value())
            state_msg = Message.property_state_message("full/{}/property/favoriteNumber/value".format(self._instance_id), favorite_number_prop_obj, self._property_favorite_number.version)
            self._conn.publish(state_msg)

    def publish_favorite_foods_value(self, *_, **__):
        """Publishes the current value of the 'favorite_foods' property.

        Accepts unused args and kwargs to make this a usable callback for application code.

        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.

        """
        with self._property_favorite_foods.mutex:
            self._property_favorite_foods.version += 1
            favorite_foods_prop_obj = self._property_favorite_foods.get_value()
            state_msg = Message.property_state_message("full/{}/property/favoriteFoods/value".format(self._instance_id), favorite_foods_prop_obj, self._property_favorite_foods.version)
            self._conn.publish(state_msg)

    def publish_lunch_menu_value(self, *_, **__):
        """Publishes the current value of the 'lunch_menu' property.

        Accepts unused args and kwargs to make this a usable callback for application code.

        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.

        """
        with self._property_lunch_menu.mutex:
            self._property_lunch_menu.version += 1
            lunch_menu_prop_obj = self._property_lunch_menu.get_value()
            state_msg = Message.property_state_message("full/{}/property/lunchMenu/value".format(self._instance_id), lunch_menu_prop_obj, self._property_lunch_menu.version)
            self._conn.publish(state_msg)

    def publish_family_name_value(self, *_, **__):
        """Publishes the current value of the 'family_name' property.

        Accepts unused args and kwargs to make this a usable callback for application code.

        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.

        """
        with self._property_family_name.mutex:
            self._property_family_name.version += 1
            family_name_prop_obj = FamilyNameProperty(family_name=self._property_family_name.get_value())
            state_msg = Message.property_state_message("full/{}/property/familyName/value".format(self._instance_id), family_name_prop_obj, self._property_family_name.version)
            self._conn.publish(state_msg)

    def publish_last_breakfast_time_value(self, *_, **__):
        """Publishes the current value of the 'last_breakfast_time' property.

        Accepts unused args and kwargs to make this a usable callback for application code.

        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.

        """
        with self._property_last_breakfast_time.mutex:
            self._property_last_breakfast_time.version += 1
            last_breakfast_time_prop_obj = LastBreakfastTimeProperty(timestamp=self._property_last_breakfast_time.get_value())
            state_msg = Message.property_state_message("full/{}/property/lastBreakfastTime/value".format(self._instance_id), last_breakfast_time_prop_obj, self._property_last_breakfast_time.version)
            self._conn.publish(state_msg)

    def publish_last_birthdays_value(self, *_, **__):
        """Publishes the current value of the 'last_birthdays' property.

        Accepts unused args and kwargs to make this a usable callback for application code.

        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.

        """
        with self._property_last_birthdays.mutex:
            self._property_last_birthdays.version += 1
            last_birthdays_prop_obj = self._property_last_birthdays.get_value()
            state_msg = Message.property_state_message("full/{}/property/lastBirthdays/value".format(self._instance_id), last_birthdays_prop_obj, self._property_last_birthdays.version)
            self._conn.publish(state_msg)

    def _publish_all_properties(self):
        """Publishes the current value of all properties."""
        self.publish_favorite_number_value()
        self.publish_favorite_foods_value()
        self.publish_lunch_menu_value()
        self.publish_family_name_value()
        self.publish_last_breakfast_time_value()
        self.publish_last_birthdays_value()

    def _receive_favorite_number_update_request_message(self, message: Message):
        """When the MQTT client receives a message to the `full/{}/property/favoriteNumber/setValue` topic
        in order to update the `favorite_number` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]
        existing_prop_obj = FavoriteNumberProperty(number=self._property_favorite_number.get_value())
        try:
            if int(prop_version) != int(self._property_favorite_number.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_favorite_number.version}' of the 'favorite_number' property")

            prop_obj = FavoriteNumberProperty.model_validate_json(message.payload)

            prop_value = prop_obj.number
            with self._property_favorite_number.mutex:
                self._property_favorite_number.version += 1
                self._property_favorite_number.set_value(prop_value)

                prop_obj = FavoriteNumberProperty(number=self._property_favorite_number.get_value())

                state_msg = Message.property_state_message("full/{}/property/favoriteNumber/value".format(self._instance_id), prop_obj, self._property_favorite_number.version)
                self._conn.publish(state_msg)

                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_favorite_number.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            for callback in self._property_favorite_number.callbacks:
                # Callbacks in this list are wrapped so that we can always pass the structure and if needed the arguments
                # are extracted there for the actual callback.
                callback(prop_obj)

        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = FavoriteNumberProperty(number=self._property_favorite_number.get_value())
                return_code = e.return_code if isinstance(e, StingerMethodException) else MethodReturnCode.SERVER_ERROR
                prop_resp_msg = Message.property_response_message(response_topic, existing_prop_obj, str(self._property_favorite_number.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)

    def _receive_favorite_foods_update_request_message(self, message: Message):
        """When the MQTT client receives a message to the `full/{}/property/favoriteFoods/setValue` topic
        in order to update the `favorite_foods` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]
        existing_prop_obj = self._property_favorite_foods.get_value()
        try:
            if int(prop_version) != int(self._property_favorite_foods.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_favorite_foods.version}' of the 'favorite_foods' property")

            prop_obj = FavoriteFoodsProperty.model_validate_json(message.payload)

            prop_value = prop_obj  # type: FavoriteFoodsProperty
            with self._property_favorite_foods.mutex:
                self._property_favorite_foods.version += 1
                self._property_favorite_foods.set_value(prop_value)

                prop_obj = self._property_favorite_foods.get_value()  # type: FavoriteFoodsProperty

                state_msg = Message.property_state_message("full/{}/property/favoriteFoods/value".format(self._instance_id), prop_obj, self._property_favorite_foods.version)
                self._conn.publish(state_msg)

                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_favorite_foods.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            for callback in self._property_favorite_foods.callbacks:
                # Callbacks in this list are wrapped so that we can always pass the structure and if needed the arguments
                # are extracted there for the actual callback.
                callback(prop_obj)

        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = self._property_favorite_foods.get_value()
                return_code = e.return_code if isinstance(e, StingerMethodException) else MethodReturnCode.SERVER_ERROR
                prop_resp_msg = Message.property_response_message(response_topic, existing_prop_obj, str(self._property_favorite_foods.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)

    def _receive_family_name_update_request_message(self, message: Message):
        """When the MQTT client receives a message to the `full/{}/property/familyName/setValue` topic
        in order to update the `family_name` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]
        existing_prop_obj = FamilyNameProperty(family_name=self._property_family_name.get_value())
        try:
            if int(prop_version) != int(self._property_family_name.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_family_name.version}' of the 'family_name' property")

            prop_obj = FamilyNameProperty.model_validate_json(message.payload)

            prop_value = prop_obj.family_name
            with self._property_family_name.mutex:
                self._property_family_name.version += 1
                self._property_family_name.set_value(prop_value)

                prop_obj = FamilyNameProperty(family_name=self._property_family_name.get_value())

                state_msg = Message.property_state_message("full/{}/property/familyName/value".format(self._instance_id), prop_obj, self._property_family_name.version)
                self._conn.publish(state_msg)

                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_family_name.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            for callback in self._property_family_name.callbacks:
                # Callbacks in this list are wrapped so that we can always pass the structure and if needed the arguments
                # are extracted there for the actual callback.
                callback(prop_obj)

        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = FamilyNameProperty(family_name=self._property_family_name.get_value())
                return_code = e.return_code if isinstance(e, StingerMethodException) else MethodReturnCode.SERVER_ERROR
                prop_resp_msg = Message.property_response_message(response_topic, existing_prop_obj, str(self._property_family_name.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)

    def _receive_last_breakfast_time_update_request_message(self, message: Message):
        """When the MQTT client receives a message to the `full/{}/property/lastBreakfastTime/setValue` topic
        in order to update the `last_breakfast_time` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]
        existing_prop_obj = LastBreakfastTimeProperty(timestamp=self._property_last_breakfast_time.get_value())
        try:
            if int(prop_version) != int(self._property_last_breakfast_time.version):
                raise OutOfSyncStingerMethodException(
                    f"Request version '{prop_version}'' does not match current version '{self._property_last_breakfast_time.version}' of the 'last_breakfast_time' property"
                )

            prop_obj = LastBreakfastTimeProperty.model_validate_json(message.payload)

            prop_value = prop_obj.timestamp
            with self._property_last_breakfast_time.mutex:
                self._property_last_breakfast_time.version += 1
                self._property_last_breakfast_time.set_value(prop_value)

                prop_obj = LastBreakfastTimeProperty(timestamp=self._property_last_breakfast_time.get_value())

                state_msg = Message.property_state_message("full/{}/property/lastBreakfastTime/value".format(self._instance_id), prop_obj, self._property_last_breakfast_time.version)
                self._conn.publish(state_msg)

                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_last_breakfast_time.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            for callback in self._property_last_breakfast_time.callbacks:
                # Callbacks in this list are wrapped so that we can always pass the structure and if needed the arguments
                # are extracted there for the actual callback.
                callback(prop_obj)

        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = LastBreakfastTimeProperty(timestamp=self._property_last_breakfast_time.get_value())
                return_code = e.return_code if isinstance(e, StingerMethodException) else MethodReturnCode.SERVER_ERROR
                prop_resp_msg = Message.property_response_message(response_topic, existing_prop_obj, str(self._property_last_breakfast_time.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)

    def _receive_last_birthdays_update_request_message(self, message: Message):
        """When the MQTT client receives a message to the `full/{}/property/lastBirthdays/setValue` topic
        in order to update the `last_birthdays` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]
        existing_prop_obj = self._property_last_birthdays.get_value()
        try:
            if int(prop_version) != int(self._property_last_birthdays.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_last_birthdays.version}' of the 'last_birthdays' property")

            prop_obj = LastBirthdaysProperty.model_validate_json(message.payload)

            prop_value = prop_obj  # type: LastBirthdaysProperty
            with self._property_last_birthdays.mutex:
                self._property_last_birthdays.version += 1
                self._property_last_birthdays.set_value(prop_value)

                prop_obj = self._property_last_birthdays.get_value()  # type: LastBirthdaysProperty

                state_msg = Message.property_state_message("full/{}/property/lastBirthdays/value".format(self._instance_id), prop_obj, self._property_last_birthdays.version)
                self._conn.publish(state_msg)

                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_last_birthdays.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            for callback in self._property_last_birthdays.callbacks:
                # Callbacks in this list are wrapped so that we can always pass the structure and if needed the arguments
                # are extracted there for the actual callback.
                callback(prop_obj)

        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = self._property_last_birthdays.get_value()
                return_code = e.return_code if isinstance(e, StingerMethodException) else MethodReturnCode.SERVER_ERROR
                prop_resp_msg = Message.property_response_message(response_topic, existing_prop_obj, str(self._property_last_birthdays.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)

    def _receive_message(self, message: Message):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message: %s", message)

    def emit_today_is(self, day_of_month: int, day_of_week: DayOfTheWeek):
        """Server application code should call this method to emit the 'todayIs' signal.

        TodayIsSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(day_of_month, int), f"The 'dayOfMonth' argument must be of type int, but was {type(day_of_month)}"

        assert isinstance(day_of_week, DayOfTheWeek), f"The 'dayOfWeek' argument must be of type DayOfTheWeek, but was {type(day_of_week)}"

        payload = TodayIsSignalPayload(
            day_of_month=day_of_month,
            day_of_week=day_of_week,
        )
        sig_msg = Message.signal_message("full/{}/signal/todayIs".format(self._instance_id), payload)
        self._conn.publish(sig_msg)

    def emit_random_word(self, word: str, time: datetime):
        """Server application code should call this method to emit the 'randomWord' signal.

        RandomWordSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(word, str), f"The 'word' argument must be of type str, but was {type(word)}"

        assert isinstance(time, datetime), f"The 'time' argument must be of type datetime, but was {type(time)}"

        payload = RandomWordSignalPayload(
            word=word,
            time=time,
        )
        sig_msg = Message.signal_message("full/{}/signal/randomWord".format(self._instance_id), payload)
        self._conn.publish(sig_msg)

    def handle_add_numbers(self, handler: Callable[[int, int, Optional[int]], int]):
        """This is a decorator to decorate a method that will handle the 'addNumbers' method calls."""
        if self._method_add_numbers.callback is None and handler is not None:
            self._method_add_numbers.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_add_numbers_call(self, message: Message):
        """This processes a call to the 'addNumbers' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = AddNumbersMethodRequest.model_validate_json(message.payload)
        correlation_id = message.correlation_data
        response_topic = message.response_topic
        self._logger.debug("Correlation data for 'addNumbers' request: %s", correlation_id)
        if self._method_add_numbers.callback is not None:
            method_args = [
                payload.first,
                payload.second,
                payload.third,
            ]  # type: List[Any]

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
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling addNumbers", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                else:
                    msg = Message.response_message(response_topic, return_json, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    def handle_do_something(self, handler: Callable[[str], DoSomethingMethodResponse]):
        """This is a decorator to decorate a method that will handle the 'doSomething' method calls."""
        if self._method_do_something.callback is None and handler is not None:
            self._method_do_something.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_do_something_call(self, message: Message):
        """This processes a call to the 'doSomething' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = DoSomethingMethodRequest.model_validate_json(message.payload)
        correlation_id = message.correlation_data
        response_topic = message.response_topic
        self._logger.debug("Correlation data for 'doSomething' request: %s", correlation_id)
        if self._method_do_something.callback is not None:
            method_args = [
                payload.task_to_do,
            ]  # type: List[Any]

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
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling doSomething", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                else:
                    msg = Message.response_message(response_topic, return_json, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    def handle_what_time_is_it(self, handler: Callable[[None], datetime]):
        """This is a decorator to decorate a method that will handle the 'what_time_is_it' method calls."""
        if self._method_what_time_is_it.callback is None and handler is not None:
            self._method_what_time_is_it.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_what_time_is_it_call(self, message: Message):
        """This processes a call to the 'what_time_is_it' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = WhatTimeIsItMethodRequest.model_validate_json(message.payload)
        correlation_id = message.correlation_data
        response_topic = message.response_topic
        self._logger.debug("Correlation data for 'what_time_is_it' request: %s", correlation_id)
        if self._method_what_time_is_it.callback is not None:
            method_args = []  # type: List[Any]

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
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling what_time_is_it", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                else:
                    msg = Message.response_message(response_topic, return_json, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    def handle_hold_temperature(self, handler: Callable[[float], bool]):
        """This is a decorator to decorate a method that will handle the 'hold_temperature' method calls."""
        if self._method_hold_temperature.callback is None and handler is not None:
            self._method_hold_temperature.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_hold_temperature_call(self, message: Message):
        """This processes a call to the 'hold_temperature' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = HoldTemperatureMethodRequest.model_validate_json(message.payload)
        correlation_id = message.correlation_data
        response_topic = message.response_topic
        self._logger.debug("Correlation data for 'hold_temperature' request: %s", correlation_id)
        if self._method_hold_temperature.callback is not None:
            method_args = [
                payload.temperature_celsius,
            ]  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_values = self._method_hold_temperature.callback(*method_args)

                    if not isinstance(return_values, bool):
                        raise ServerSerializationErrorStingerMethodException(f"The return value must be of type bool, but was {type(return_values)}")
                    ret_obj = HoldTemperatureMethodResponse(success=return_values)
                    return_json = ret_obj.model_dump_json(by_alias=True)

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling hold_temperature: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling hold_temperature", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                else:
                    msg = Message.response_message(response_topic, return_json, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    @property
    def favorite_number(self) -> Optional[int]:
        """This property returns the last received (int) value for the 'favorite_number' property."""
        return self._property_favorite_number.get_value()

    @favorite_number.setter
    def favorite_number(self, number: int):
        """This property sets (publishes) a new int value for the 'favorite_number' property."""
        if not isinstance(number, int):
            raise ValueError(f"The value must be int .")

        value_updated = False
        with self._property_favorite_number.mutex:
            if number != self._property_favorite_number.get_value():
                value_updated = True
                self._property_favorite_number.set_value(number)
                self._property_favorite_number.version += 1
                prop_obj = FavoriteNumberProperty(number=self._property_favorite_number.get_value())
                state_msg = Message.property_state_message("full/{}/property/favoriteNumber/value".format(self._instance_id), prop_obj, self._property_favorite_number.version)
                self._conn.publish(state_msg)

        if value_updated:
            for callback in self._property_favorite_number.callbacks:
                callback(prop_obj.number)

    def set_favorite_number(self, number: int):
        """This method sets (publishes) a new value for the 'favorite_number' property."""
        if not isinstance(number, int):
            raise ValueError(f"The 'number' value must be int.")

        obj = number

        # Use the property.setter to do that actual work.
        self.favorite_number = obj

    def on_favorite_number_updated(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'favorite_number' property update is received."""
        self._property_favorite_number.callbacks.append(handler)

    @property
    def favorite_foods(self) -> FavoriteFoodsProperty:
        """This property returns the last received value for the 'favorite_foods' property.
        The 'favorite_foods' property contains multiple values, so we operate on the full
        `FavoriteFoodsProperty` structure.

        """
        return self._property_favorite_foods.get_value()

    @favorite_foods.setter
    def favorite_foods(self, value: FavoriteFoodsProperty):
        """This property sets (publishes) a new value structure for the 'favorite_foods' property."""
        if not isinstance(value, FavoriteFoodsProperty):
            raise ValueError(f"The value must be FavoriteFoodsProperty.")

            value_updated = False
            with self._property_favorite_foods.mutex:
                if value != self._property_favorite_foods.get_value():
                    value_updated = True
                    self._property_favorite_foods.set_value(value)
                    self._property_favorite_foods.version += 1
                    state_msg = Message.property_state_message(
                        "full/{}/property/favoriteFoods/value".format(self._instance_id), self._property_favorite_foods.get_value(), self._property_favorite_foods.version
                    )
                    self._conn.publish(state_msg)

            if value_updated:
                for callback in self._property_favorite_foods.callbacks:
                    callback(self._property_favorite_foods.get_value())

    def set_favorite_foods(self, drink: str, slices_of_pizza: int, breakfast: Optional[str]):
        """This method sets (publishes) a new value for the 'favorite_foods' property."""
        if not isinstance(drink, str):
            raise ValueError(f"The 'drink' value must be str.")
        if not isinstance(slices_of_pizza, int):
            raise ValueError(f"The 'slices_of_pizza' value must be int.")
        if not isinstance(breakfast, str) and breakfast is not None:
            raise ValueError(f"The 'breakfast' value must be Optional[str].")

        obj = FavoriteFoodsProperty(
            drink=drink,
            slices_of_pizza=slices_of_pizza,
            breakfast=breakfast,
        )

        # Use the property.setter to do that actual work.
        self.favorite_foods = obj

    def on_favorite_foods_updated(self, handler: Callable[[str, int, Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'favorite_foods' property update is received."""

        def wrapper(value: FavoriteFoodsProperty):
            handler(
                value.drink,
                value.slices_of_pizza,
                value.breakfast,
            )

        self._property_favorite_foods.callbacks.append(wrapper)

    @property
    def lunch_menu(self) -> LunchMenuProperty:
        """This property returns the last received value for the 'lunch_menu' property.
        The 'lunch_menu' property contains multiple values, so we operate on the full
        `LunchMenuProperty` structure.

        """
        return self._property_lunch_menu.get_value()

    @lunch_menu.setter
    def lunch_menu(self, value: LunchMenuProperty):
        """This property sets (publishes) a new value structure for the 'lunch_menu' property."""
        if not isinstance(value, LunchMenuProperty):
            raise ValueError(f"The value must be LunchMenuProperty.")

            value_updated = False
            with self._property_lunch_menu.mutex:
                if value != self._property_lunch_menu.get_value():
                    value_updated = True
                    self._property_lunch_menu.set_value(value)
                    self._property_lunch_menu.version += 1
                    state_msg = Message.property_state_message("full/{}/property/lunchMenu/value".format(self._instance_id), self._property_lunch_menu.get_value(), self._property_lunch_menu.version)
                    self._conn.publish(state_msg)

            if value_updated:
                for callback in self._property_lunch_menu.callbacks:
                    callback(self._property_lunch_menu.get_value())

    def set_lunch_menu(self, monday: Lunch, tuesday: Lunch):
        """This method sets (publishes) a new value for the 'lunch_menu' property."""
        if not isinstance(monday, Lunch):
            raise ValueError(f"The 'monday' value must be Lunch.")
        if not isinstance(tuesday, Lunch):
            raise ValueError(f"The 'tuesday' value must be Lunch.")

        obj = LunchMenuProperty(
            monday=monday,
            tuesday=tuesday,
        )

        # Use the property.setter to do that actual work.
        self.lunch_menu = obj

    def on_lunch_menu_updated(self, handler: Callable[[Lunch, Lunch], None]):
        """This method registers a callback to be called whenever a new 'lunch_menu' property update is received."""

        def wrapper(value: LunchMenuProperty):
            handler(
                value.monday,
                value.tuesday,
            )

        self._property_lunch_menu.callbacks.append(wrapper)

    @property
    def family_name(self) -> Optional[str]:
        """This property returns the last received (str) value for the 'family_name' property."""
        return self._property_family_name.get_value()

    @family_name.setter
    def family_name(self, family_name: str):
        """This property sets (publishes) a new str value for the 'family_name' property."""
        if not isinstance(family_name, str):
            raise ValueError(f"The value must be str .")

        value_updated = False
        with self._property_family_name.mutex:
            if family_name != self._property_family_name.get_value():
                value_updated = True
                self._property_family_name.set_value(family_name)
                self._property_family_name.version += 1
                prop_obj = FamilyNameProperty(family_name=self._property_family_name.get_value())
                state_msg = Message.property_state_message("full/{}/property/familyName/value".format(self._instance_id), prop_obj, self._property_family_name.version)
                self._conn.publish(state_msg)

        if value_updated:
            for callback in self._property_family_name.callbacks:
                callback(prop_obj.family_name)

    def set_family_name(self, family_name: str):
        """This method sets (publishes) a new value for the 'family_name' property."""
        if not isinstance(family_name, str):
            raise ValueError(f"The 'family_name' value must be str.")

        obj = family_name

        # Use the property.setter to do that actual work.
        self.family_name = obj

    def on_family_name_updated(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'family_name' property update is received."""
        self._property_family_name.callbacks.append(handler)

    @property
    def last_breakfast_time(self) -> Optional[datetime]:
        """This property returns the last received (datetime) value for the 'last_breakfast_time' property."""
        return self._property_last_breakfast_time.get_value()

    @last_breakfast_time.setter
    def last_breakfast_time(self, timestamp: datetime):
        """This property sets (publishes) a new datetime value for the 'last_breakfast_time' property."""
        if not isinstance(timestamp, datetime):
            raise ValueError(f"The value must be datetime .")

        value_updated = False
        with self._property_last_breakfast_time.mutex:
            if timestamp != self._property_last_breakfast_time.get_value():
                value_updated = True
                self._property_last_breakfast_time.set_value(timestamp)
                self._property_last_breakfast_time.version += 1
                prop_obj = LastBreakfastTimeProperty(timestamp=self._property_last_breakfast_time.get_value())
                state_msg = Message.property_state_message("full/{}/property/lastBreakfastTime/value".format(self._instance_id), prop_obj, self._property_last_breakfast_time.version)
                self._conn.publish(state_msg)

        if value_updated:
            for callback in self._property_last_breakfast_time.callbacks:
                callback(prop_obj.timestamp)

    def set_last_breakfast_time(self, timestamp: datetime):
        """This method sets (publishes) a new value for the 'last_breakfast_time' property."""
        if not isinstance(timestamp, datetime):
            raise ValueError(f"The 'timestamp' value must be datetime.")

        obj = timestamp

        # Use the property.setter to do that actual work.
        self.last_breakfast_time = obj

    def on_last_breakfast_time_updated(self, handler: Callable[[datetime], None]):
        """This method registers a callback to be called whenever a new 'last_breakfast_time' property update is received."""
        self._property_last_breakfast_time.callbacks.append(handler)

    @property
    def last_birthdays(self) -> LastBirthdaysProperty:
        """This property returns the last received value for the 'last_birthdays' property.
        The 'last_birthdays' property contains multiple values, so we operate on the full
        `LastBirthdaysProperty` structure.

        """
        return self._property_last_birthdays.get_value()

    @last_birthdays.setter
    def last_birthdays(self, value: LastBirthdaysProperty):
        """This property sets (publishes) a new value structure for the 'last_birthdays' property."""
        if not isinstance(value, LastBirthdaysProperty):
            raise ValueError(f"The value must be LastBirthdaysProperty.")

            value_updated = False
            with self._property_last_birthdays.mutex:
                if value != self._property_last_birthdays.get_value():
                    value_updated = True
                    self._property_last_birthdays.set_value(value)
                    self._property_last_birthdays.version += 1
                    state_msg = Message.property_state_message(
                        "full/{}/property/lastBirthdays/value".format(self._instance_id), self._property_last_birthdays.get_value(), self._property_last_birthdays.version
                    )
                    self._conn.publish(state_msg)

            if value_updated:
                for callback in self._property_last_birthdays.callbacks:
                    callback(self._property_last_birthdays.get_value())

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

        obj = LastBirthdaysProperty(
            mom=mom,
            dad=dad,
            sister=sister,
            brothers_age=brothers_age,
        )

        # Use the property.setter to do that actual work.
        self.last_birthdays = obj

    def on_last_birthdays_updated(self, handler: Callable[[datetime, datetime, Optional[datetime], Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'last_birthdays' property update is received."""

        def wrapper(value: LastBirthdaysProperty):
            handler(
                value.mom,
                value.dad,
                value.sister,
                value.brothers_age,
            )

        self._property_last_birthdays.callbacks.append(wrapper)


class FullServerBuilder:
    """
    This is a builder for the FullServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):

        self._add_numbers_method_handler: Optional[Callable[[int, int, Optional[int]], int]] = None
        self._do_something_method_handler: Optional[Callable[[str], DoSomethingMethodResponse]] = None
        self._what_time_is_it_method_handler: Optional[Callable[[None], datetime]] = None
        self._hold_temperature_method_handler: Optional[Callable[[float], bool]] = None

        self._favorite_number_property_callbacks: List[Callable[[int], None]] = []
        self._favorite_foods_property_callbacks: List[Callable[[str, int, Optional[str]], None]] = []
        self._lunch_menu_property_callbacks: List[Callable[[Lunch, Lunch], None]] = []
        self._family_name_property_callbacks: List[Callable[[str], None]] = []
        self._last_breakfast_time_property_callbacks: List[Callable[[datetime], None]] = []
        self._last_birthdays_property_callbacks: List[Callable[[datetime, datetime, Optional[datetime], Optional[int]], None]] = []

    def handle_add_numbers(self, handler: Callable[[int, int, Optional[int]], int]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._add_numbers_method_handler is None and handler is not None:
            self._add_numbers_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_do_something(self, handler: Callable[[str], DoSomethingMethodResponse]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._do_something_method_handler is None and handler is not None:
            self._do_something_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_what_time_is_it(self, handler: Callable[[None], datetime]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._what_time_is_it_method_handler is None and handler is not None:
            self._what_time_is_it_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_hold_temperature(self, handler: Callable[[float], bool]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._hold_temperature_method_handler is None and handler is not None:
            self._hold_temperature_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def on_favorite_number_updated(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'favorite_number' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._favorite_number_property_callbacks.append(wrapper)
        return wrapper

    def on_favorite_foods_updated(self, handler: Callable[[str, int, Optional[str]], None]):
        """This method registers a callback to be called whenever a new 'favorite_foods' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._favorite_foods_property_callbacks.append(wrapper)
        return wrapper

    def on_lunch_menu_updated(self, handler: Callable[[Lunch, Lunch], None]):
        """This method registers a callback to be called whenever a new 'lunch_menu' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._lunch_menu_property_callbacks.append(wrapper)
        return wrapper

    def on_family_name_updated(self, handler: Callable[[str], None]):
        """This method registers a callback to be called whenever a new 'family_name' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._family_name_property_callbacks.append(wrapper)
        return wrapper

    def on_last_breakfast_time_updated(self, handler: Callable[[datetime], None]):
        """This method registers a callback to be called whenever a new 'last_breakfast_time' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._last_breakfast_time_property_callbacks.append(wrapper)
        return wrapper

    def on_last_birthdays_updated(self, handler: Callable[[datetime, datetime, Optional[datetime], Optional[int]], None]):
        """This method registers a callback to be called whenever a new 'last_birthdays' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._last_birthdays_property_callbacks.append(wrapper)
        return wrapper

    def build(self, connection: IBrokerConnection, instance_id: str, initial_property_values: FullInitialPropertyValues, binding: Optional[Any] = None) -> FullServer:
        new_server = FullServer(connection, instance_id, initial_property_values)

        if self._add_numbers_method_handler is not None:
            if binding:
                binding_cb = self._add_numbers_method_handler.__get__(binding, binding.__class__)
                new_server.handle_add_numbers(binding_cb)
            else:
                new_server.handle_add_numbers(self._add_numbers_method_handler)
        if self._do_something_method_handler is not None:
            if binding:
                binding_cb = self._do_something_method_handler.__get__(binding, binding.__class__)
                new_server.handle_do_something(binding_cb)
            else:
                new_server.handle_do_something(self._do_something_method_handler)
        if self._what_time_is_it_method_handler is not None:
            if binding:
                binding_cb = self._what_time_is_it_method_handler.__get__(binding, binding.__class__)
                new_server.handle_what_time_is_it(binding_cb)
            else:
                new_server.handle_what_time_is_it(self._what_time_is_it_method_handler)
        if self._hold_temperature_method_handler is not None:
            if binding:
                binding_cb = self._hold_temperature_method_handler.__get__(binding, binding.__class__)
                new_server.handle_hold_temperature(binding_cb)
            else:
                new_server.handle_hold_temperature(self._hold_temperature_method_handler)

        for callback in self._favorite_number_property_callbacks:
            if binding:
                new_server.on_favorite_number_updated(callback.__get__(binding, binding.__class__))
            else:
                new_server.on_favorite_number_updated(callback)

        for callback in self._favorite_foods_property_callbacks:
            if binding:
                new_server.on_favorite_foods_updated(callback.__get__(binding, binding.__class__))
            else:
                new_server.on_favorite_foods_updated(callback)

        for callback in self._lunch_menu_property_callbacks:
            if binding:
                new_server.on_lunch_menu_updated(callback.__get__(binding, binding.__class__))
            else:
                new_server.on_lunch_menu_updated(callback)

        for callback in self._family_name_property_callbacks:
            if binding:
                new_server.on_family_name_updated(callback.__get__(binding, binding.__class__))
            else:
                new_server.on_family_name_updated(callback)

        for callback in self._last_breakfast_time_property_callbacks:
            if binding:
                new_server.on_last_breakfast_time_updated(callback.__get__(binding, binding.__class__))
            else:
                new_server.on_last_breakfast_time_updated(callback)

        for callback in self._last_birthdays_property_callbacks:
            if binding:
                new_server.on_last_birthdays_updated(callback.__get__(binding, binding.__class__))
            else:
                new_server.on_last_birthdays_updated(callback)

        return new_server
