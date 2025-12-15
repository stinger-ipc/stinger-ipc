"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the weather interface.

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


from .property import WeatherInitialPropertyValues


T = TypeVar("T")


@dataclass
class PropertyControls(Generic[T]):
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


class WeatherServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str, initial_property_values: WeatherInitialPropertyValues):
        self._logger = logging.getLogger(f"WeatherServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing WeatherServer instance %s", instance_id)
        self._instance_id = instance_id
        self._service_advert_topic = "weather/{}/interface".format(self._instance_id)
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._property_location: PropertyControls[LocationProperty] = PropertyControls(value=initial_property_values.location, version=initial_property_values.location_version)
        self._property_location.subscription_id = self._conn.subscribe("weather/{}/property/location/setValue".format(self._instance_id), self._receive_location_update_request_message)

        self._property_current_temperature: PropertyControls[float] = PropertyControls(value=initial_property_values.current_temperature, version=initial_property_values.current_temperature_version)

        self._property_current_condition: PropertyControls[CurrentConditionProperty] = PropertyControls(
            value=initial_property_values.current_condition, version=initial_property_values.current_condition_version
        )

        self._property_daily_forecast: PropertyControls[DailyForecastProperty] = PropertyControls(value=initial_property_values.daily_forecast, version=initial_property_values.daily_forecast_version)

        self._property_hourly_forecast: PropertyControls[HourlyForecastProperty] = PropertyControls(
            value=initial_property_values.hourly_forecast, version=initial_property_values.hourly_forecast_version
        )

        self._property_current_condition_refresh_interval: PropertyControls[int] = PropertyControls(
            value=initial_property_values.current_condition_refresh_interval, version=initial_property_values.current_condition_refresh_interval_version
        )
        self._property_current_condition_refresh_interval.subscription_id = self._conn.subscribe(
            "weather/{}/property/currentConditionRefreshInterval/setValue".format(self._instance_id), self._receive_current_condition_refresh_interval_update_request_message
        )

        self._property_hourly_forecast_refresh_interval: PropertyControls[int] = PropertyControls(
            value=initial_property_values.hourly_forecast_refresh_interval, version=initial_property_values.hourly_forecast_refresh_interval_version
        )
        self._property_hourly_forecast_refresh_interval.subscription_id = self._conn.subscribe(
            "weather/{}/property/hourlyForecastRefreshInterval/setValue".format(self._instance_id), self._receive_hourly_forecast_refresh_interval_update_request_message
        )

        self._property_daily_forecast_refresh_interval: PropertyControls[int] = PropertyControls(
            value=initial_property_values.daily_forecast_refresh_interval, version=initial_property_values.daily_forecast_refresh_interval_version
        )
        self._property_daily_forecast_refresh_interval.subscription_id = self._conn.subscribe(
            "weather/{}/property/dailyForecastRefreshInterval/setValue".format(self._instance_id), self._receive_daily_forecast_refresh_interval_update_request_message
        )

        self._method_refresh_daily_forecast = MethodControls()
        self._method_refresh_daily_forecast.subscription_id = self._conn.subscribe("weather/{}/method/refreshDailyForecast".format(self._instance_id), self._process_refresh_daily_forecast_call)

        self._method_refresh_hourly_forecast = MethodControls()
        self._method_refresh_hourly_forecast.subscription_id = self._conn.subscribe("weather/{}/method/refreshHourlyForecast".format(self._instance_id), self._process_refresh_hourly_forecast_call)

        self._method_refresh_current_conditions = MethodControls()
        self._method_refresh_current_conditions.subscription_id = self._conn.subscribe(
            "weather/{}/method/refreshCurrentConditions".format(self._instance_id), self._process_refresh_current_conditions_call
        )

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

    def _publish_all_properties(self):
        with self._property_location.mutex:
            location_prop_obj = self._property_location.get_value()
            state_msg = Message.property_state_message("weather/{}/property/location/value".format(self._instance_id), location_prop_obj, self._property_location.version)
            self._conn.publish(state_msg)
        with self._property_current_temperature.mutex:
            current_temperature_prop_obj = CurrentTemperatureProperty(temperature_f=self._property_current_temperature.get_value())
            state_msg = Message.property_state_message(
                "weather/{}/property/currentTemperature/value".format(self._instance_id), current_temperature_prop_obj, self._property_current_temperature.version
            )
            self._conn.publish(state_msg)
        with self._property_current_condition.mutex:
            current_condition_prop_obj = self._property_current_condition.get_value()
            state_msg = Message.property_state_message("weather/{}/property/currentCondition/value".format(self._instance_id), current_condition_prop_obj, self._property_current_condition.version)
            self._conn.publish(state_msg)
        with self._property_daily_forecast.mutex:
            daily_forecast_prop_obj = self._property_daily_forecast.get_value()
            state_msg = Message.property_state_message("weather/{}/property/dailyForecast/value".format(self._instance_id), daily_forecast_prop_obj, self._property_daily_forecast.version)
            self._conn.publish(state_msg)
        with self._property_hourly_forecast.mutex:
            hourly_forecast_prop_obj = self._property_hourly_forecast.get_value()
            state_msg = Message.property_state_message("weather/{}/property/hourlyForecast/value".format(self._instance_id), hourly_forecast_prop_obj, self._property_hourly_forecast.version)
            self._conn.publish(state_msg)
        with self._property_current_condition_refresh_interval.mutex:
            current_condition_refresh_interval_prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())
            state_msg = Message.property_state_message(
                "weather/{}/property/currentConditionRefreshInterval/value".format(self._instance_id),
                current_condition_refresh_interval_prop_obj,
                self._property_current_condition_refresh_interval.version,
            )
            self._conn.publish(state_msg)
        with self._property_hourly_forecast_refresh_interval.mutex:
            hourly_forecast_refresh_interval_prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())
            state_msg = Message.property_state_message(
                "weather/{}/property/hourlyForecastRefreshInterval/value".format(self._instance_id), hourly_forecast_refresh_interval_prop_obj, self._property_hourly_forecast_refresh_interval.version
            )
            self._conn.publish(state_msg)
        with self._property_daily_forecast_refresh_interval.mutex:
            daily_forecast_refresh_interval_prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())
            state_msg = Message.property_state_message(
                "weather/{}/property/dailyForecastRefreshInterval/value".format(self._instance_id), daily_forecast_refresh_interval_prop_obj, self._property_daily_forecast_refresh_interval.version
            )
            self._conn.publish(state_msg)

    def _receive_location_update_request_message(self, message: Message):
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]

        existing_prop_obj = self._property_location.get_value()

        try:
            if int(prop_version) != int(self._property_location.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", message.topic, prop_version, self._property_location.version)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_location.version),
                        MethodReturnCode.OUT_OF_SYNC.value,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_location.version}",
                    )
                    self._conn.publish(prop_resp_msg)
                return

            try:
                prop_obj = LocationProperty.model_validate_json(message.payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", message.topic, e)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic, existing_prop_obj, str(self._property_location.version), MethodReturnCode.CLIENT_DESERIALIZATION_ERROR.value, correlation_id, str(e)
                    )
                    self._conn.publish(prop_resp_msg)
                return
            prop_value = prop_obj
            with self._property_location.mutex:
                self._property_location.version += 1
                self._property_location.set_value(prop_value)

                prop_obj = self._property_location.get_value()

                state_msg = Message.property_state_message("weather/{}/property/location/value".format(self._instance_id), prop_obj, self._property_location.version)
                self._conn.publish(state_msg)

            if response_topic is not None:

                prop_obj = self._property_location.get_value()

                self._logger.debug("Sending property update response for to %s", response_topic)
                prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_location.version), MethodReturnCode.SUCCESS.value, correlation_id)
                self._conn.publish(prop_resp_msg)
            else:
                self._logger.warning("No response topic provided for property update of %s", message.topic)

            for callback in self._property_location.callbacks:
                callback(
                    prop_value.latitude,
                    prop_value.longitude,
                )

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", message.topic, exc_info=e)
            if response_topic is not None:
                prop_obj = self._property_location.get_value()
                prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_location.version), MethodReturnCode.SERVER_ERROR.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)

    def _receive_current_condition_refresh_interval_update_request_message(self, message: Message):
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]

        existing_prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())

        try:
            if int(prop_version) != int(self._property_current_condition_refresh_interval.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", message.topic, prop_version, self._property_current_condition_refresh_interval.version)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_current_condition_refresh_interval.version),
                        MethodReturnCode.OUT_OF_SYNC.value,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_current_condition_refresh_interval.version}",
                    )
                    self._conn.publish(prop_resp_msg)
                return

            try:
                prop_obj = CurrentConditionRefreshIntervalProperty.model_validate_json(message.payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", message.topic, e)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic, existing_prop_obj, str(self._property_current_condition_refresh_interval.version), MethodReturnCode.CLIENT_DESERIALIZATION_ERROR.value, correlation_id, str(e)
                    )
                    self._conn.publish(prop_resp_msg)
                return
            prop_value = prop_obj.seconds
            with self._property_current_condition_refresh_interval.mutex:
                self._property_current_condition_refresh_interval.version += 1
                self._property_current_condition_refresh_interval.set_value(prop_value)

                prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())

                state_msg = Message.property_state_message(
                    "weather/{}/property/currentConditionRefreshInterval/value".format(self._instance_id), prop_obj, self._property_current_condition_refresh_interval.version
                )
                self._conn.publish(state_msg)

            if response_topic is not None:

                prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                prop_resp_msg = Message.property_response_message(
                    response_topic, prop_obj, str(self._property_current_condition_refresh_interval.version), MethodReturnCode.SUCCESS.value, correlation_id
                )
                self._conn.publish(prop_resp_msg)
            else:
                self._logger.warning("No response topic provided for property update of %s", message.topic)

            for callback in self._property_current_condition_refresh_interval.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", message.topic, exc_info=e)
            if response_topic is not None:
                prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())
                prop_resp_msg = Message.property_response_message(
                    response_topic, prop_obj, str(self._property_current_condition_refresh_interval.version), MethodReturnCode.SERVER_ERROR.value, correlation_id, str(e)
                )
                self._conn.publish(prop_resp_msg)

    def _receive_hourly_forecast_refresh_interval_update_request_message(self, message: Message):
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]

        existing_prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())

        try:
            if int(prop_version) != int(self._property_hourly_forecast_refresh_interval.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", message.topic, prop_version, self._property_hourly_forecast_refresh_interval.version)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_hourly_forecast_refresh_interval.version),
                        MethodReturnCode.OUT_OF_SYNC.value,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_hourly_forecast_refresh_interval.version}",
                    )
                    self._conn.publish(prop_resp_msg)
                return

            try:
                prop_obj = HourlyForecastRefreshIntervalProperty.model_validate_json(message.payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", message.topic, e)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic, existing_prop_obj, str(self._property_hourly_forecast_refresh_interval.version), MethodReturnCode.CLIENT_DESERIALIZATION_ERROR.value, correlation_id, str(e)
                    )
                    self._conn.publish(prop_resp_msg)
                return
            prop_value = prop_obj.seconds
            with self._property_hourly_forecast_refresh_interval.mutex:
                self._property_hourly_forecast_refresh_interval.version += 1
                self._property_hourly_forecast_refresh_interval.set_value(prop_value)

                prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())

                state_msg = Message.property_state_message(
                    "weather/{}/property/hourlyForecastRefreshInterval/value".format(self._instance_id), prop_obj, self._property_hourly_forecast_refresh_interval.version
                )
                self._conn.publish(state_msg)

            if response_topic is not None:

                prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                prop_resp_msg = Message.property_response_message(
                    response_topic, prop_obj, str(self._property_hourly_forecast_refresh_interval.version), MethodReturnCode.SUCCESS.value, correlation_id
                )
                self._conn.publish(prop_resp_msg)
            else:
                self._logger.warning("No response topic provided for property update of %s", message.topic)

            for callback in self._property_hourly_forecast_refresh_interval.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", message.topic, exc_info=e)
            if response_topic is not None:
                prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())
                prop_resp_msg = Message.property_response_message(
                    response_topic, prop_obj, str(self._property_hourly_forecast_refresh_interval.version), MethodReturnCode.SERVER_ERROR.value, correlation_id, str(e)
                )
                self._conn.publish(prop_resp_msg)

    def _receive_daily_forecast_refresh_interval_update_request_message(self, message: Message):
        user_properties = message.user_properties or dict()  # type: Dict[str, str]
        prop_version_str = user_properties.get("PropertyVersion", "-1")  # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data  # type: Optional[bytes]
        response_topic = message.response_topic  # type: Optional[str]

        existing_prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())

        try:
            if int(prop_version) != int(self._property_daily_forecast_refresh_interval.version):
                self._logger.warning("Received out-of-date update for %s (version %s, current version %s)", message.topic, prop_version, self._property_daily_forecast_refresh_interval.version)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic,
                        existing_prop_obj,
                        str(self._property_daily_forecast_refresh_interval.version),
                        MethodReturnCode.OUT_OF_SYNC.value,
                        correlation_id,
                        f"Request version {prop_version} does not match current version {self._property_daily_forecast_refresh_interval.version}",
                    )
                    self._conn.publish(prop_resp_msg)
                return

            try:
                prop_obj = DailyForecastRefreshIntervalProperty.model_validate_json(message.payload)
            except ValidationError as e:
                self._logger.error("Failed to validate payload for %s: %s", message.topic, e)
                if response_topic is not None:
                    prop_resp_msg = Message.property_response_message(
                        response_topic, existing_prop_obj, str(self._property_daily_forecast_refresh_interval.version), MethodReturnCode.CLIENT_DESERIALIZATION_ERROR.value, correlation_id, str(e)
                    )
                    self._conn.publish(prop_resp_msg)
                return
            prop_value = prop_obj.seconds
            with self._property_daily_forecast_refresh_interval.mutex:
                self._property_daily_forecast_refresh_interval.version += 1
                self._property_daily_forecast_refresh_interval.set_value(prop_value)

                prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())

                state_msg = Message.property_state_message(
                    "weather/{}/property/dailyForecastRefreshInterval/value".format(self._instance_id), prop_obj, self._property_daily_forecast_refresh_interval.version
                )
                self._conn.publish(state_msg)

            if response_topic is not None:

                prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())

                self._logger.debug("Sending property update response for to %s", response_topic)
                prop_resp_msg = Message.property_response_message(response_topic, prop_obj, str(self._property_daily_forecast_refresh_interval.version), MethodReturnCode.SUCCESS.value, correlation_id)
                self._conn.publish(prop_resp_msg)
            else:
                self._logger.warning("No response topic provided for property update of %s", message.topic)

            for callback in self._property_daily_forecast_refresh_interval.callbacks:
                callback(prop_value)

        except Exception as e:
            self._logger.exception("Exception while processing property update for %s", message.topic, exc_info=e)
            if response_topic is not None:
                prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())
                prop_resp_msg = Message.property_response_message(
                    response_topic, prop_obj, str(self._property_daily_forecast_refresh_interval.version), MethodReturnCode.SERVER_ERROR.value, correlation_id, str(e)
                )
                self._conn.publish(prop_resp_msg)

    def _receive_message(self, message: Message):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message: %s", message)

    def emit_current_time(self, current_time: str):
        """Server application code should call this method to emit the 'current_time' signal.

        CurrentTimeSignalPayload is a pydantic BaseModel which will validate the arguments.
        """

        assert isinstance(current_time, str), f"The 'current_time' argument must be of type str, but was {type(current_time)}"

        payload = CurrentTimeSignalPayload(
            current_time=current_time,
        )
        sig_msg = Message.signal_message("weather/{}/signal/currentTime".format(self._instance_id), payload)
        self._conn.publish(sig_msg)

    def handle_refresh_daily_forecast(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_daily_forecast' method calls."""
        if self._method_refresh_daily_forecast.callback is None and handler is not None:
            self._method_refresh_daily_forecast.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_daily_forecast_call(self, message: Message):
        """This processes a call to the 'refresh_daily_forecast' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = RefreshDailyForecastMethodRequest.model_validate_json(message.payload)
        correlation_id = message.correlation_data
        response_topic = message.response_topic
        self._logger.debug("Correlation data for 'refresh_daily_forecast' request: %s", correlation_id)
        if self._method_refresh_daily_forecast.callback is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    self._method_refresh_daily_forecast.callback(*method_args)

                    return_json = "{}"

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling refresh_daily_forecast: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling refresh_daily_forecast", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                else:
                    msg = Message.response_message(response_topic, return_json, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    def handle_refresh_hourly_forecast(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_hourly_forecast' method calls."""
        if self._method_refresh_hourly_forecast.callback is None and handler is not None:
            self._method_refresh_hourly_forecast.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_hourly_forecast_call(self, message: Message):
        """This processes a call to the 'refresh_hourly_forecast' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = RefreshHourlyForecastMethodRequest.model_validate_json(message.payload)
        correlation_id = message.correlation_data
        response_topic = message.response_topic
        self._logger.debug("Correlation data for 'refresh_hourly_forecast' request: %s", correlation_id)
        if self._method_refresh_hourly_forecast.callback is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    self._method_refresh_hourly_forecast.callback(*method_args)

                    return_json = "{}"

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling refresh_hourly_forecast: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling refresh_hourly_forecast", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                else:
                    msg = Message.response_message(response_topic, return_json, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    def handle_refresh_current_conditions(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_current_conditions' method calls."""
        if self._method_refresh_current_conditions.callback is None and handler is not None:
            self._method_refresh_current_conditions.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_current_conditions_call(self, message: Message):
        """This processes a call to the 'refresh_current_conditions' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = RefreshCurrentConditionsMethodRequest.model_validate_json(message.payload)
        correlation_id = message.correlation_data
        response_topic = message.response_topic
        self._logger.debug("Correlation data for 'refresh_current_conditions' request: %s", correlation_id)
        if self._method_refresh_current_conditions.callback is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    self._method_refresh_current_conditions.callback(*method_args)

                    return_json = "{}"

                except StingerMethodException as sme:
                    self._logger.warning("StingerMethodException while handling refresh_current_conditions: %s", sme)
                    return_code = sme.return_code
                    debug_msg = str(sme)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                except Exception as e:
                    self._logger.exception("Exception while handling refresh_current_conditions", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                    err_msg = Message.error_response_message(response_topic, return_code.value, correlation_id, debug_info=debug_msg)
                    self._conn.publish(err_msg)
                else:
                    msg = Message.response_message(response_topic, return_json, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    @property
    def location(self) -> LocationProperty:
        """This property returns the last received value for the 'location' property."""
        return self._property_location.get_value()

    @location.setter
    def location(self, value: LocationProperty):
        """This property sets (publishes) a new value structure for the 'location' property."""

        if not isinstance(value, LocationProperty):
            raise ValueError(f"The value must be LocationProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_location.value:
            with self._property_location.mutex:
                self._property_location.value = value
                self._property_location.version += 1
                state_msg = Message.property_state_message("weather/{}/property/location/value".format(self._instance_id), value, self._property_location.version)
                self._conn.publish(state_msg)
            for callback in self._property_location.callbacks:
                callback(value.latitude, value.longitude)

    def set_location(self, latitude: float, longitude: float):
        """This method sets (publishes) a new value for the 'location' property."""
        if not isinstance(latitude, float):
            raise ValueError(f"The 'latitude' value must be float.")
        if not isinstance(longitude, float):
            raise ValueError(f"The 'longitude' value must be float.")

        obj = LocationProperty(
            latitude=latitude,
            longitude=longitude,
        )

        # Use the property.setter to do that actual work.
        self.location = obj

    def on_location_updates(self, handler: Callable[[float, float], None]):
        """This method registers a callback to be called whenever a new 'location' property update is received."""
        if handler is not None:

            def wrapper(value: LocationProperty):
                handler(value.latitude, value.longitude)

            self._property_location.callbacks.append(handler)

    @property
    def current_temperature(self) -> Optional[float]:
        """This property returns the last received value for the 'current_temperature' property."""
        return self._property_current_temperature.get_value()

    @current_temperature.setter
    def current_temperature(self, temperature_f: float):
        """This property sets (publishes) a new value for the 'current_temperature' property."""

        if not isinstance(temperature_f, float):
            raise ValueError(f"The value must be float .")

        prop_obj = CurrentTemperatureProperty(temperature_f=temperature_f)
        payload = prop_obj.model_dump_json(by_alias=True)

        with self._property_current_temperature.mutex:
            if temperature_f != self._property_current_temperature.value:
                self._property_current_temperature.value = temperature_f
                self._property_current_temperature.version += 1
                state_msg = Message.property_state_message("weather/{}/property/currentTemperature/value".format(self._instance_id), prop_obj, self._property_current_temperature.version)
                self._conn.publish(state_msg)
        for callback in self._property_current_temperature.callbacks:
            callback(prop_obj.temperature_f)

    def set_current_temperature(self, temperature_f: float):
        """This method sets (publishes) a new value for the 'current_temperature' property."""
        if not isinstance(temperature_f, float):
            raise ValueError(f"The 'temperature_f' value must be float.")

        obj = temperature_f

        # Use the property.setter to do that actual work.
        self.current_temperature = obj

    def on_current_temperature_updates(self, handler: Callable[[float], None]):
        """This method registers a callback to be called whenever a new 'current_temperature' property update is received."""
        if handler is not None:

            def wrapper(value: CurrentTemperatureProperty):
                handler(value.temperature_f)

            self._property_current_temperature.callbacks.append(handler)

    @property
    def current_condition(self) -> CurrentConditionProperty:
        """This property returns the last received value for the 'current_condition' property."""
        return self._property_current_condition.get_value()

    @current_condition.setter
    def current_condition(self, value: CurrentConditionProperty):
        """This property sets (publishes) a new value structure for the 'current_condition' property."""

        if not isinstance(value, CurrentConditionProperty):
            raise ValueError(f"The value must be CurrentConditionProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_current_condition.value:
            with self._property_current_condition.mutex:
                self._property_current_condition.value = value
                self._property_current_condition.version += 1
                state_msg = Message.property_state_message("weather/{}/property/currentCondition/value".format(self._instance_id), value, self._property_current_condition.version)
                self._conn.publish(state_msg)
            for callback in self._property_current_condition.callbacks:
                callback(value.condition, value.description)

    def set_current_condition(self, condition: WeatherCondition, description: str):
        """This method sets (publishes) a new value for the 'current_condition' property."""
        if not isinstance(condition, WeatherCondition):
            raise ValueError(f"The 'condition' value must be WeatherCondition.")
        if not isinstance(description, str):
            raise ValueError(f"The 'description' value must be str.")

        obj = CurrentConditionProperty(
            condition=condition,
            description=description,
        )

        # Use the property.setter to do that actual work.
        self.current_condition = obj

    def on_current_condition_updates(self, handler: Callable[[WeatherCondition, str], None]):
        """This method registers a callback to be called whenever a new 'current_condition' property update is received."""
        if handler is not None:

            def wrapper(value: CurrentConditionProperty):
                handler(value.condition, value.description)

            self._property_current_condition.callbacks.append(handler)

    @property
    def daily_forecast(self) -> DailyForecastProperty:
        """This property returns the last received value for the 'daily_forecast' property."""
        return self._property_daily_forecast.get_value()

    @daily_forecast.setter
    def daily_forecast(self, value: DailyForecastProperty):
        """This property sets (publishes) a new value structure for the 'daily_forecast' property."""

        if not isinstance(value, DailyForecastProperty):
            raise ValueError(f"The value must be DailyForecastProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_daily_forecast.value:
            with self._property_daily_forecast.mutex:
                self._property_daily_forecast.value = value
                self._property_daily_forecast.version += 1
                state_msg = Message.property_state_message("weather/{}/property/dailyForecast/value".format(self._instance_id), value, self._property_daily_forecast.version)
                self._conn.publish(state_msg)
            for callback in self._property_daily_forecast.callbacks:
                callback(value.monday, value.tuesday, value.wednesday)

    def set_daily_forecast(self, monday: ForecastForDay, tuesday: ForecastForDay, wednesday: ForecastForDay):
        """This method sets (publishes) a new value for the 'daily_forecast' property."""
        if not isinstance(monday, ForecastForDay):
            raise ValueError(f"The 'monday' value must be ForecastForDay.")
        if not isinstance(tuesday, ForecastForDay):
            raise ValueError(f"The 'tuesday' value must be ForecastForDay.")
        if not isinstance(wednesday, ForecastForDay):
            raise ValueError(f"The 'wednesday' value must be ForecastForDay.")

        obj = DailyForecastProperty(
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
        )

        # Use the property.setter to do that actual work.
        self.daily_forecast = obj

    def on_daily_forecast_updates(self, handler: Callable[[ForecastForDay, ForecastForDay, ForecastForDay], None]):
        """This method registers a callback to be called whenever a new 'daily_forecast' property update is received."""
        if handler is not None:

            def wrapper(value: DailyForecastProperty):
                handler(value.monday, value.tuesday, value.wednesday)

            self._property_daily_forecast.callbacks.append(handler)

    @property
    def hourly_forecast(self) -> HourlyForecastProperty:
        """This property returns the last received value for the 'hourly_forecast' property."""
        return self._property_hourly_forecast.get_value()

    @hourly_forecast.setter
    def hourly_forecast(self, value: HourlyForecastProperty):
        """This property sets (publishes) a new value structure for the 'hourly_forecast' property."""

        if not isinstance(value, HourlyForecastProperty):
            raise ValueError(f"The value must be HourlyForecastProperty.")

        payload = value.model_dump_json(by_alias=True)

        if value != self._property_hourly_forecast.value:
            with self._property_hourly_forecast.mutex:
                self._property_hourly_forecast.value = value
                self._property_hourly_forecast.version += 1
                state_msg = Message.property_state_message("weather/{}/property/hourlyForecast/value".format(self._instance_id), value, self._property_hourly_forecast.version)
                self._conn.publish(state_msg)
            for callback in self._property_hourly_forecast.callbacks:
                callback(value.hour_0, value.hour_1, value.hour_2, value.hour_3)

    def set_hourly_forecast(self, hour_0: ForecastForHour, hour_1: ForecastForHour, hour_2: ForecastForHour, hour_3: ForecastForHour):
        """This method sets (publishes) a new value for the 'hourly_forecast' property."""
        if not isinstance(hour_0, ForecastForHour):
            raise ValueError(f"The 'hour_0' value must be ForecastForHour.")
        if not isinstance(hour_1, ForecastForHour):
            raise ValueError(f"The 'hour_1' value must be ForecastForHour.")
        if not isinstance(hour_2, ForecastForHour):
            raise ValueError(f"The 'hour_2' value must be ForecastForHour.")
        if not isinstance(hour_3, ForecastForHour):
            raise ValueError(f"The 'hour_3' value must be ForecastForHour.")

        obj = HourlyForecastProperty(
            hour_0=hour_0,
            hour_1=hour_1,
            hour_2=hour_2,
            hour_3=hour_3,
        )

        # Use the property.setter to do that actual work.
        self.hourly_forecast = obj

    def on_hourly_forecast_updates(self, handler: Callable[[ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour], None]):
        """This method registers a callback to be called whenever a new 'hourly_forecast' property update is received."""
        if handler is not None:

            def wrapper(value: HourlyForecastProperty):
                handler(value.hour_0, value.hour_1, value.hour_2, value.hour_3)

            self._property_hourly_forecast.callbacks.append(handler)

    @property
    def current_condition_refresh_interval(self) -> Optional[int]:
        """This property returns the last received value for the 'current_condition_refresh_interval' property."""
        return self._property_current_condition_refresh_interval.get_value()

    @current_condition_refresh_interval.setter
    def current_condition_refresh_interval(self, seconds: int):
        """This property sets (publishes) a new value for the 'current_condition_refresh_interval' property."""

        if not isinstance(seconds, int):
            raise ValueError(f"The value must be int .")

        prop_obj = CurrentConditionRefreshIntervalProperty(seconds=seconds)
        payload = prop_obj.model_dump_json(by_alias=True)

        with self._property_current_condition_refresh_interval.mutex:
            if seconds != self._property_current_condition_refresh_interval.value:
                self._property_current_condition_refresh_interval.value = seconds
                self._property_current_condition_refresh_interval.version += 1
                state_msg = Message.property_state_message(
                    "weather/{}/property/currentConditionRefreshInterval/value".format(self._instance_id), prop_obj, self._property_current_condition_refresh_interval.version
                )
                self._conn.publish(state_msg)
        for callback in self._property_current_condition_refresh_interval.callbacks:
            callback(prop_obj.seconds)

    def set_current_condition_refresh_interval(self, seconds: int):
        """This method sets (publishes) a new value for the 'current_condition_refresh_interval' property."""
        if not isinstance(seconds, int):
            raise ValueError(f"The 'seconds' value must be int.")

        obj = seconds

        # Use the property.setter to do that actual work.
        self.current_condition_refresh_interval = obj

    def on_current_condition_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'current_condition_refresh_interval' property update is received."""
        if handler is not None:

            def wrapper(value: CurrentConditionRefreshIntervalProperty):
                handler(value.seconds)

            self._property_current_condition_refresh_interval.callbacks.append(handler)

    @property
    def hourly_forecast_refresh_interval(self) -> Optional[int]:
        """This property returns the last received value for the 'hourly_forecast_refresh_interval' property."""
        return self._property_hourly_forecast_refresh_interval.get_value()

    @hourly_forecast_refresh_interval.setter
    def hourly_forecast_refresh_interval(self, seconds: int):
        """This property sets (publishes) a new value for the 'hourly_forecast_refresh_interval' property."""

        if not isinstance(seconds, int):
            raise ValueError(f"The value must be int .")

        prop_obj = HourlyForecastRefreshIntervalProperty(seconds=seconds)
        payload = prop_obj.model_dump_json(by_alias=True)

        with self._property_hourly_forecast_refresh_interval.mutex:
            if seconds != self._property_hourly_forecast_refresh_interval.value:
                self._property_hourly_forecast_refresh_interval.value = seconds
                self._property_hourly_forecast_refresh_interval.version += 1
                state_msg = Message.property_state_message(
                    "weather/{}/property/hourlyForecastRefreshInterval/value".format(self._instance_id), prop_obj, self._property_hourly_forecast_refresh_interval.version
                )
                self._conn.publish(state_msg)
        for callback in self._property_hourly_forecast_refresh_interval.callbacks:
            callback(prop_obj.seconds)

    def set_hourly_forecast_refresh_interval(self, seconds: int):
        """This method sets (publishes) a new value for the 'hourly_forecast_refresh_interval' property."""
        if not isinstance(seconds, int):
            raise ValueError(f"The 'seconds' value must be int.")

        obj = seconds

        # Use the property.setter to do that actual work.
        self.hourly_forecast_refresh_interval = obj

    def on_hourly_forecast_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'hourly_forecast_refresh_interval' property update is received."""
        if handler is not None:

            def wrapper(value: HourlyForecastRefreshIntervalProperty):
                handler(value.seconds)

            self._property_hourly_forecast_refresh_interval.callbacks.append(handler)

    @property
    def daily_forecast_refresh_interval(self) -> Optional[int]:
        """This property returns the last received value for the 'daily_forecast_refresh_interval' property."""
        return self._property_daily_forecast_refresh_interval.get_value()

    @daily_forecast_refresh_interval.setter
    def daily_forecast_refresh_interval(self, seconds: int):
        """This property sets (publishes) a new value for the 'daily_forecast_refresh_interval' property."""

        if not isinstance(seconds, int):
            raise ValueError(f"The value must be int .")

        prop_obj = DailyForecastRefreshIntervalProperty(seconds=seconds)
        payload = prop_obj.model_dump_json(by_alias=True)

        with self._property_daily_forecast_refresh_interval.mutex:
            if seconds != self._property_daily_forecast_refresh_interval.value:
                self._property_daily_forecast_refresh_interval.value = seconds
                self._property_daily_forecast_refresh_interval.version += 1
                state_msg = Message.property_state_message(
                    "weather/{}/property/dailyForecastRefreshInterval/value".format(self._instance_id), prop_obj, self._property_daily_forecast_refresh_interval.version
                )
                self._conn.publish(state_msg)
        for callback in self._property_daily_forecast_refresh_interval.callbacks:
            callback(prop_obj.seconds)

    def set_daily_forecast_refresh_interval(self, seconds: int):
        """This method sets (publishes) a new value for the 'daily_forecast_refresh_interval' property."""
        if not isinstance(seconds, int):
            raise ValueError(f"The 'seconds' value must be int.")

        obj = seconds

        # Use the property.setter to do that actual work.
        self.daily_forecast_refresh_interval = obj

    def on_daily_forecast_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'daily_forecast_refresh_interval' property update is received."""
        if handler is not None:

            def wrapper(value: DailyForecastRefreshIntervalProperty):
                handler(value.seconds)

            self._property_daily_forecast_refresh_interval.callbacks.append(handler)


class WeatherServerBuilder:
    """
    This is a builder for the WeatherServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):

        self._refresh_daily_forecast_method_handler: Optional[Callable[[None], None]] = None
        self._refresh_hourly_forecast_method_handler: Optional[Callable[[None], None]] = None
        self._refresh_current_conditions_method_handler: Optional[Callable[[None], None]] = None

        self._location_property_callbacks: List[Callable[[float, float], None]] = []
        self._current_temperature_property_callbacks: List[Callable[[float], None]] = []
        self._current_condition_property_callbacks: List[Callable[[WeatherCondition, str], None]] = []
        self._daily_forecast_property_callbacks: List[Callable[[ForecastForDay, ForecastForDay, ForecastForDay], None]] = []
        self._hourly_forecast_property_callbacks: List[Callable[[ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour], None]] = []
        self._current_condition_refresh_interval_property_callbacks: List[Callable[[int], None]] = []
        self._hourly_forecast_refresh_interval_property_callbacks: List[Callable[[int], None]] = []
        self._daily_forecast_refresh_interval_property_callbacks: List[Callable[[int], None]] = []

    def handle_refresh_daily_forecast(self, handler: Callable[[None], None]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._refresh_daily_forecast_method_handler is None and handler is not None:
            self._refresh_daily_forecast_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_refresh_hourly_forecast(self, handler: Callable[[None], None]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._refresh_hourly_forecast_method_handler is None and handler is not None:
            self._refresh_hourly_forecast_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def handle_refresh_current_conditions(self, handler: Callable[[None], None]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        if self._refresh_current_conditions_method_handler is None and handler is not None:
            self._refresh_current_conditions_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper

    def on_location_updates(self, handler: Callable[[float, float], None]):
        """This method registers a callback to be called whenever a new 'location' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._location_property_callbacks.append(wrapper)
        return wrapper

    def on_current_temperature_updates(self, handler: Callable[[float], None]):
        """This method registers a callback to be called whenever a new 'current_temperature' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._current_temperature_property_callbacks.append(wrapper)
        return wrapper

    def on_current_condition_updates(self, handler: Callable[[WeatherCondition, str], None]):
        """This method registers a callback to be called whenever a new 'current_condition' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._current_condition_property_callbacks.append(wrapper)
        return wrapper

    def on_daily_forecast_updates(self, handler: Callable[[ForecastForDay, ForecastForDay, ForecastForDay], None]):
        """This method registers a callback to be called whenever a new 'daily_forecast' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._daily_forecast_property_callbacks.append(wrapper)
        return wrapper

    def on_hourly_forecast_updates(self, handler: Callable[[ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour], None]):
        """This method registers a callback to be called whenever a new 'hourly_forecast' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._hourly_forecast_property_callbacks.append(wrapper)
        return wrapper

    def on_current_condition_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'current_condition_refresh_interval' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._current_condition_refresh_interval_property_callbacks.append(wrapper)
        return wrapper

    def on_hourly_forecast_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'hourly_forecast_refresh_interval' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._hourly_forecast_refresh_interval_property_callbacks.append(wrapper)
        return wrapper

    def on_daily_forecast_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'daily_forecast_refresh_interval' property update is received."""

        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._daily_forecast_refresh_interval_property_callbacks.append(wrapper)
        return wrapper

    def build(self, connection: IBrokerConnection, instance_id: str, initial_property_values: WeatherInitialPropertyValues, binding: Optional[Any] = None) -> WeatherServer:
        new_server = WeatherServer(connection, instance_id, initial_property_values)

        if self._refresh_daily_forecast_method_handler is not None:
            if binding:
                binding_cb = self._refresh_daily_forecast_method_handler.__get__(binding, binding.__class__)
                new_server.handle_refresh_daily_forecast(binding_cb)
            else:
                new_server.handle_refresh_daily_forecast(self._refresh_daily_forecast_method_handler)
        if self._refresh_hourly_forecast_method_handler is not None:
            if binding:
                binding_cb = self._refresh_hourly_forecast_method_handler.__get__(binding, binding.__class__)
                new_server.handle_refresh_hourly_forecast(binding_cb)
            else:
                new_server.handle_refresh_hourly_forecast(self._refresh_hourly_forecast_method_handler)
        if self._refresh_current_conditions_method_handler is not None:
            if binding:
                binding_cb = self._refresh_current_conditions_method_handler.__get__(binding, binding.__class__)
                new_server.handle_refresh_current_conditions(binding_cb)
            else:
                new_server.handle_refresh_current_conditions(self._refresh_current_conditions_method_handler)

        for callback in self._location_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_location_updates(binding_cb)
            else:
                new_server.on_location_updates(callback)

        for callback in self._current_temperature_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_current_temperature_updates(binding_cb)
            else:
                new_server.on_current_temperature_updates(callback)

        for callback in self._current_condition_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_current_condition_updates(binding_cb)
            else:
                new_server.on_current_condition_updates(callback)

        for callback in self._daily_forecast_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_daily_forecast_updates(binding_cb)
            else:
                new_server.on_daily_forecast_updates(callback)

        for callback in self._hourly_forecast_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_hourly_forecast_updates(binding_cb)
            else:
                new_server.on_hourly_forecast_updates(callback)

        for callback in self._current_condition_refresh_interval_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_current_condition_refresh_interval_updates(binding_cb)
            else:
                new_server.on_current_condition_refresh_interval_updates(callback)

        for callback in self._hourly_forecast_refresh_interval_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_hourly_forecast_refresh_interval_updates(binding_cb)
            else:
                new_server.on_hourly_forecast_refresh_interval_updates(callback)

        for callback in self._daily_forecast_refresh_interval_property_callbacks:
            if binding:
                binding_cb = callback.__get__(binding, binding.__class__)
                new_server.on_daily_forecast_refresh_interval_updates(binding_cb)
            else:
                new_server.on_daily_forecast_refresh_interval_updates(callback)

        return new_server
