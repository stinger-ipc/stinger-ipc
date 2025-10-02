"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the weather interface.
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


class WeatherServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str):
        self._logger = logging.getLogger(f"WeatherServer:{instance_id}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing WeatherServer instance %s", instance_id)
        self._instance_id = instance_id
        self._re_advertise_server_interval_seconds = 120  # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)

        self._property_location: PropertyControls[stinger_types.LocationProperty, float, float] = PropertyControls()
        self._property_location.subscription_id = self._conn.subscribe("weather/{}/property/location/setValue".format(self._instance_id), self._receive_location_update_request_message)

        self._property_current_temperature: PropertyControls[float, float] = PropertyControls()
        self._property_current_temperature.subscription_id = self._conn.subscribe(
            "weather/{}/property/currentTemperature/setValue".format(self._instance_id), self._receive_current_temperature_update_request_message
        )

        self._property_current_condition: PropertyControls[stinger_types.CurrentConditionProperty, stinger_types.WeatherCondition, str] = PropertyControls()
        self._property_current_condition.subscription_id = self._conn.subscribe(
            "weather/{}/property/currentCondition/setValue".format(self._instance_id), self._receive_current_condition_update_request_message
        )

        self._property_daily_forecast: PropertyControls[stinger_types.DailyForecastProperty, stinger_types.ForecastForDay, stinger_types.ForecastForDay, stinger_types.ForecastForDay] = (
            PropertyControls()
        )
        self._property_daily_forecast.subscription_id = self._conn.subscribe(
            "weather/{}/property/dailyForecast/setValue".format(self._instance_id), self._receive_daily_forecast_update_request_message
        )

        self._property_hourly_forecast: PropertyControls[
            stinger_types.HourlyForecastProperty, stinger_types.ForecastForHour, stinger_types.ForecastForHour, stinger_types.ForecastForHour, stinger_types.ForecastForHour
        ] = PropertyControls()
        self._property_hourly_forecast.subscription_id = self._conn.subscribe(
            "weather/{}/property/hourlyForecast/setValue".format(self._instance_id), self._receive_hourly_forecast_update_request_message
        )

        self._property_current_condition_refresh_interval: PropertyControls[int, int] = PropertyControls()
        self._property_current_condition_refresh_interval.subscription_id = self._conn.subscribe(
            "weather/{}/property/currentConditionRefreshInterval/setValue".format(self._instance_id), self._receive_current_condition_refresh_interval_update_request_message
        )

        self._property_hourly_forecast_refresh_interval: PropertyControls[int, int] = PropertyControls()
        self._property_hourly_forecast_refresh_interval.subscription_id = self._conn.subscribe(
            "weather/{}/property/hourlyForecastRefreshInterval/setValue".format(self._instance_id), self._receive_hourly_forecast_refresh_interval_update_request_message
        )

        self._property_daily_forecast_refresh_interval: PropertyControls[int, int] = PropertyControls()
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
        topic = "weather/{}/interface".format(self._instance_id)
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json())
        self._conn.publish_status(topic, data, expiry)

    def _receive_location_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        prop_value = stinger_types.LocationProperty.model_validate_json(payload)
        with self._property_location.mutex:
            self._property_location.value = prop_value
            self._property_location.version += 1
        for callback in self._property_location.callbacks:
            callback(prop_value.latitude, prop_value.longitude)

    def _receive_current_temperature_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = float(payload_obj["temperature_f"])
        with self._property_current_temperature.mutex:
            self._property_current_temperature.value = prop_value
            self._property_current_temperature.version += 1
        for callback in self._property_current_temperature.callbacks:
            callback(prop_value)

    def _receive_current_condition_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        prop_value = stinger_types.CurrentConditionProperty.model_validate_json(payload)
        with self._property_current_condition.mutex:
            self._property_current_condition.value = prop_value
            self._property_current_condition.version += 1
        for callback in self._property_current_condition.callbacks:
            callback(prop_value.condition, prop_value.description)

    def _receive_daily_forecast_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        prop_value = stinger_types.DailyForecastProperty.model_validate_json(payload)
        with self._property_daily_forecast.mutex:
            self._property_daily_forecast.value = prop_value
            self._property_daily_forecast.version += 1
        for callback in self._property_daily_forecast.callbacks:
            callback(prop_value.monday, prop_value.tuesday, prop_value.wednesday)

    def _receive_hourly_forecast_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        prop_value = stinger_types.HourlyForecastProperty.model_validate_json(payload)
        with self._property_hourly_forecast.mutex:
            self._property_hourly_forecast.value = prop_value
            self._property_hourly_forecast.version += 1
        for callback in self._property_hourly_forecast.callbacks:
            callback(prop_value.hour_0, prop_value.hour_1, prop_value.hour_2, prop_value.hour_3)

    def _receive_current_condition_refresh_interval_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = int(payload_obj["seconds"])
        with self._property_current_condition_refresh_interval.mutex:
            self._property_current_condition_refresh_interval.value = prop_value
            self._property_current_condition_refresh_interval.version += 1
        for callback in self._property_current_condition_refresh_interval.callbacks:
            callback(prop_value)

    def _receive_hourly_forecast_refresh_interval_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = int(payload_obj["seconds"])
        with self._property_hourly_forecast_refresh_interval.mutex:
            self._property_hourly_forecast_refresh_interval.value = prop_value
            self._property_hourly_forecast_refresh_interval.version += 1
        for callback in self._property_hourly_forecast_refresh_interval.callbacks:
            callback(prop_value)

    def _receive_daily_forecast_refresh_interval_update_request_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        payload_obj = json.loads(payload)
        prop_value = int(payload_obj["seconds"])
        with self._property_daily_forecast_refresh_interval.mutex:
            self._property_daily_forecast_refresh_interval.value = prop_value
            self._property_daily_forecast_refresh_interval.version += 1
        for callback in self._property_daily_forecast_refresh_interval.callbacks:
            callback(prop_value)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.warning("Received unexpected message to %s", topic)

    def emit_current_time(self, current_time: str):
        """Server application code should call this method to emit the 'current_time' signal."""
        if not isinstance(current_time, str):
            raise ValueError(f"The 'current_time' value must be str.")

        payload = {
            "current_time": str(current_time),
        }
        self._conn.publish("weather/{}/signal/currentTime".format(self._instance_id), json.dumps(payload), qos=1, retain=False)

    def handle_refresh_daily_forecast(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_daily_forecast' method calls."""
        if self._method_refresh_daily_forecast.callback is None and handler is not None:
            self._method_refresh_daily_forecast.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_daily_forecast_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'refresh_daily_forecast' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = json.loads(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._method_refresh_daily_forecast.callback is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._method_refresh_daily_forecast.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling refresh_daily_forecast", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodReturnCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)

    def handle_refresh_hourly_forecast(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_hourly_forecast' method calls."""
        if self._method_refresh_hourly_forecast.callback is None and handler is not None:
            self._method_refresh_hourly_forecast.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_hourly_forecast_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'refresh_hourly_forecast' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = json.loads(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._method_refresh_hourly_forecast.callback is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._method_refresh_hourly_forecast.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling refresh_hourly_forecast", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodReturnCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)

    def handle_refresh_current_conditions(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_current_conditions' method calls."""
        if self._method_refresh_current_conditions.callback is None and handler is not None:
            self._method_refresh_current_conditions.callback = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_current_conditions_call(self, topic: str, payload_str: str, properties: Dict[str, Any]):
        """This processes a call to the 'refresh_current_conditions' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        payload = json.loads(payload_str)
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._method_refresh_current_conditions.callback is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._method_refresh_current_conditions.callback(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling refresh_current_conditions", exc_info=e)
                    return_code = MethodReturnCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodReturnCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)

    @property
    def location(self) -> stinger_types.LocationProperty | None:
        """This property returns the last received value for the 'location' property."""
        with self._property_location_mutex:
            return self._property_location

    @location.setter
    def location(self, value: stinger_types.LocationProperty):
        """This property sets (publishes) a new value for the 'location' property."""
        if not isinstance(value, stinger_types.LocationProperty):
            raise ValueError(f"The value must be stinger_types.LocationProperty.")

        payload = value.model_dump_json()

        if value != self._property_location.value:
            with self._property_location.mutex:
                self._property_location.value = value
                self._property_location.version += 1
            self._conn.publish("weather/{}/property/location/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_location.callbacks:
                callback(value.latitude, value.longitude)

    def set_location(self, latitude: float, longitude: float):
        """This method sets (publishes) a new value for the 'location' property."""
        if not isinstance(latitude, float):
            raise ValueError(f"The 'latitude' value must be float.")
        if not isinstance(longitude, float):
            raise ValueError(f"The 'longitude' value must be float.")

        obj = stinger_types.LocationProperty(
            latitude=latitude,
            longitude=longitude,
        )

        # Use the property.setter to do that actual work.
        self.location = obj

    def on_location_updates(self, handler: Callable[[float, float], None]):
        """This method registers a callback to be called whenever a new 'location' property update is received."""
        if handler is not None:
            self._property_location.callbacks.append(handler)

    @property
    def current_temperature(self) -> float | None:
        """This property returns the last received value for the 'current_temperature' property."""
        with self._property_current_temperature_mutex:
            return self._property_current_temperature

    @current_temperature.setter
    def current_temperature(self, temperature_f: float):
        """This property sets (publishes) a new value for the 'current_temperature' property."""
        if not isinstance(temperature_f, float):
            raise ValueError(f"The value must be float.")

        payload = json.dumps({"temperature_f": temperature_f})

        if temperature_f != self._property_current_temperature.value:
            with self._property_current_temperature.mutex:
                self._property_current_temperature.value = temperature_f
                self._property_current_temperature.version += 1
            self._conn.publish("weather/{}/property/currentTemperature/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_current_temperature.callbacks:
                callback(temperature_f)

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
            self._property_current_temperature.callbacks.append(handler)

    @property
    def current_condition(self) -> stinger_types.CurrentConditionProperty | None:
        """This property returns the last received value for the 'current_condition' property."""
        with self._property_current_condition_mutex:
            return self._property_current_condition

    @current_condition.setter
    def current_condition(self, value: stinger_types.CurrentConditionProperty):
        """This property sets (publishes) a new value for the 'current_condition' property."""
        if not isinstance(value, stinger_types.CurrentConditionProperty):
            raise ValueError(f"The value must be stinger_types.CurrentConditionProperty.")

        payload = value.model_dump_json()

        if value != self._property_current_condition.value:
            with self._property_current_condition.mutex:
                self._property_current_condition.value = value
                self._property_current_condition.version += 1
            self._conn.publish("weather/{}/property/currentCondition/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_current_condition.callbacks:
                callback(value.condition, value.description)

    def set_current_condition(self, condition: stinger_types.WeatherCondition, description: str):
        """This method sets (publishes) a new value for the 'current_condition' property."""
        if not isinstance(condition, stinger_types.WeatherCondition):
            raise ValueError(f"The 'condition' value must be stinger_types.WeatherCondition.")
        if not isinstance(description, str):
            raise ValueError(f"The 'description' value must be str.")

        obj = stinger_types.CurrentConditionProperty(
            condition=condition,
            description=description,
        )

        # Use the property.setter to do that actual work.
        self.current_condition = obj

    def on_current_condition_updates(self, handler: Callable[[stinger_types.WeatherCondition, str], None]):
        """This method registers a callback to be called whenever a new 'current_condition' property update is received."""
        if handler is not None:
            self._property_current_condition.callbacks.append(handler)

    @property
    def daily_forecast(self) -> stinger_types.DailyForecastProperty | None:
        """This property returns the last received value for the 'daily_forecast' property."""
        with self._property_daily_forecast_mutex:
            return self._property_daily_forecast

    @daily_forecast.setter
    def daily_forecast(self, value: stinger_types.DailyForecastProperty):
        """This property sets (publishes) a new value for the 'daily_forecast' property."""
        if not isinstance(value, stinger_types.DailyForecastProperty):
            raise ValueError(f"The value must be stinger_types.DailyForecastProperty.")

        payload = value.model_dump_json()

        if value != self._property_daily_forecast.value:
            with self._property_daily_forecast.mutex:
                self._property_daily_forecast.value = value
                self._property_daily_forecast.version += 1
            self._conn.publish("weather/{}/property/dailyForecast/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_daily_forecast.callbacks:
                callback(value.monday, value.tuesday, value.wednesday)

    def set_daily_forecast(self, monday: stinger_types.ForecastForDay, tuesday: stinger_types.ForecastForDay, wednesday: stinger_types.ForecastForDay):
        """This method sets (publishes) a new value for the 'daily_forecast' property."""
        if not isinstance(monday, stinger_types.ForecastForDay):
            raise ValueError(f"The 'monday' value must be stinger_types.ForecastForDay.")
        if not isinstance(tuesday, stinger_types.ForecastForDay):
            raise ValueError(f"The 'tuesday' value must be stinger_types.ForecastForDay.")
        if not isinstance(wednesday, stinger_types.ForecastForDay):
            raise ValueError(f"The 'wednesday' value must be stinger_types.ForecastForDay.")

        obj = stinger_types.DailyForecastProperty(
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
        )

        # Use the property.setter to do that actual work.
        self.daily_forecast = obj

    def on_daily_forecast_updates(self, handler: Callable[[stinger_types.ForecastForDay, stinger_types.ForecastForDay, stinger_types.ForecastForDay], None]):
        """This method registers a callback to be called whenever a new 'daily_forecast' property update is received."""
        if handler is not None:
            self._property_daily_forecast.callbacks.append(handler)

    @property
    def hourly_forecast(self) -> stinger_types.HourlyForecastProperty | None:
        """This property returns the last received value for the 'hourly_forecast' property."""
        with self._property_hourly_forecast_mutex:
            return self._property_hourly_forecast

    @hourly_forecast.setter
    def hourly_forecast(self, value: stinger_types.HourlyForecastProperty):
        """This property sets (publishes) a new value for the 'hourly_forecast' property."""
        if not isinstance(value, stinger_types.HourlyForecastProperty):
            raise ValueError(f"The value must be stinger_types.HourlyForecastProperty.")

        payload = value.model_dump_json()

        if value != self._property_hourly_forecast.value:
            with self._property_hourly_forecast.mutex:
                self._property_hourly_forecast.value = value
                self._property_hourly_forecast.version += 1
            self._conn.publish("weather/{}/property/hourlyForecast/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_hourly_forecast.callbacks:
                callback(value.hour_0, value.hour_1, value.hour_2, value.hour_3)

    def set_hourly_forecast(self, hour_0: stinger_types.ForecastForHour, hour_1: stinger_types.ForecastForHour, hour_2: stinger_types.ForecastForHour, hour_3: stinger_types.ForecastForHour):
        """This method sets (publishes) a new value for the 'hourly_forecast' property."""
        if not isinstance(hour_0, stinger_types.ForecastForHour):
            raise ValueError(f"The 'hour_0' value must be stinger_types.ForecastForHour.")
        if not isinstance(hour_1, stinger_types.ForecastForHour):
            raise ValueError(f"The 'hour_1' value must be stinger_types.ForecastForHour.")
        if not isinstance(hour_2, stinger_types.ForecastForHour):
            raise ValueError(f"The 'hour_2' value must be stinger_types.ForecastForHour.")
        if not isinstance(hour_3, stinger_types.ForecastForHour):
            raise ValueError(f"The 'hour_3' value must be stinger_types.ForecastForHour.")

        obj = stinger_types.HourlyForecastProperty(
            hour_0=hour_0,
            hour_1=hour_1,
            hour_2=hour_2,
            hour_3=hour_3,
        )

        # Use the property.setter to do that actual work.
        self.hourly_forecast = obj

    def on_hourly_forecast_updates(self, handler: Callable[[stinger_types.ForecastForHour, stinger_types.ForecastForHour, stinger_types.ForecastForHour, stinger_types.ForecastForHour], None]):
        """This method registers a callback to be called whenever a new 'hourly_forecast' property update is received."""
        if handler is not None:
            self._property_hourly_forecast.callbacks.append(handler)

    @property
    def current_condition_refresh_interval(self) -> int | None:
        """This property returns the last received value for the 'current_condition_refresh_interval' property."""
        with self._property_current_condition_refresh_interval_mutex:
            return self._property_current_condition_refresh_interval

    @current_condition_refresh_interval.setter
    def current_condition_refresh_interval(self, seconds: int):
        """This property sets (publishes) a new value for the 'current_condition_refresh_interval' property."""
        if not isinstance(seconds, int):
            raise ValueError(f"The value must be int.")

        payload = json.dumps({"seconds": seconds})

        if seconds != self._property_current_condition_refresh_interval.value:
            with self._property_current_condition_refresh_interval.mutex:
                self._property_current_condition_refresh_interval.value = seconds
                self._property_current_condition_refresh_interval.version += 1
            self._conn.publish("weather/{}/property/currentConditionRefreshInterval/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_current_condition_refresh_interval.callbacks:
                callback(seconds)

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
            self._property_current_condition_refresh_interval.callbacks.append(handler)

    @property
    def hourly_forecast_refresh_interval(self) -> int | None:
        """This property returns the last received value for the 'hourly_forecast_refresh_interval' property."""
        with self._property_hourly_forecast_refresh_interval_mutex:
            return self._property_hourly_forecast_refresh_interval

    @hourly_forecast_refresh_interval.setter
    def hourly_forecast_refresh_interval(self, seconds: int):
        """This property sets (publishes) a new value for the 'hourly_forecast_refresh_interval' property."""
        if not isinstance(seconds, int):
            raise ValueError(f"The value must be int.")

        payload = json.dumps({"seconds": seconds})

        if seconds != self._property_hourly_forecast_refresh_interval.value:
            with self._property_hourly_forecast_refresh_interval.mutex:
                self._property_hourly_forecast_refresh_interval.value = seconds
                self._property_hourly_forecast_refresh_interval.version += 1
            self._conn.publish("weather/{}/property/hourlyForecastRefreshInterval/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_hourly_forecast_refresh_interval.callbacks:
                callback(seconds)

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
            self._property_hourly_forecast_refresh_interval.callbacks.append(handler)

    @property
    def daily_forecast_refresh_interval(self) -> int | None:
        """This property returns the last received value for the 'daily_forecast_refresh_interval' property."""
        with self._property_daily_forecast_refresh_interval_mutex:
            return self._property_daily_forecast_refresh_interval

    @daily_forecast_refresh_interval.setter
    def daily_forecast_refresh_interval(self, seconds: int):
        """This property sets (publishes) a new value for the 'daily_forecast_refresh_interval' property."""
        if not isinstance(seconds, int):
            raise ValueError(f"The value must be int.")

        payload = json.dumps({"seconds": seconds})

        if seconds != self._property_daily_forecast_refresh_interval.value:
            with self._property_daily_forecast_refresh_interval.mutex:
                self._property_daily_forecast_refresh_interval.value = seconds
                self._property_daily_forecast_refresh_interval.version += 1
            self._conn.publish("weather/{}/property/dailyForecastRefreshInterval/value".format(self._instance_id), payload, qos=1, retain=True)
            for callback in self._property_daily_forecast_refresh_interval.callbacks:
                callback(seconds)

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
            self._property_daily_forecast_refresh_interval.callbacks.append(handler)


class WeatherServerBuilder:
    """
    This is a builder for the WeatherServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self, connection: IBrokerConnection):
        self._conn = connection

        self._refresh_daily_forecast_method_handler: Optional[Callable[[None], None]] = None
        self._refresh_hourly_forecast_method_handler: Optional[Callable[[None], None]] = None
        self._refresh_current_conditions_method_handler: Optional[Callable[[None], None]] = None

        self._location_property_callbacks: List[Callable[[float, float], None]] = []
        self._current_temperature_property_callbacks: List[Callable[[float], None]] = []
        self._current_condition_property_callbacks: List[Callable[[stinger_types.WeatherCondition, str], None]] = []
        self._daily_forecast_property_callbacks: List[Callable[[stinger_types.ForecastForDay, stinger_types.ForecastForDay, stinger_types.ForecastForDay], None]] = []
        self._hourly_forecast_property_callbacks: List[Callable[[stinger_types.ForecastForHour, stinger_types.ForecastForHour, stinger_types.ForecastForHour, stinger_types.ForecastForHour], None]] = (
            []
        )
        self._current_condition_refresh_interval_property_callbacks: List[Callable[[int], None]] = []
        self._hourly_forecast_refresh_interval_property_callbacks: List[Callable[[int], None]] = []
        self._daily_forecast_refresh_interval_property_callbacks: List[Callable[[int], None]] = []

    def handle_refresh_daily_forecast(self, handler: Callable[[None], None]):
        if self._refresh_daily_forecast_method_handler is None and handler is not None:
            self._refresh_daily_forecast_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_refresh_hourly_forecast(self, handler: Callable[[None], None]):
        if self._refresh_hourly_forecast_method_handler is None and handler is not None:
            self._refresh_hourly_forecast_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def handle_refresh_current_conditions(self, handler: Callable[[None], None]):
        if self._refresh_current_conditions_method_handler is None and handler is not None:
            self._refresh_current_conditions_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def on_location_updates(self, handler: Callable[[float, float], None]):
        """This method registers a callback to be called whenever a new 'location' property update is received."""
        self._location_property_callbacks.append(handler)

    def on_current_temperature_updates(self, handler: Callable[[float], None]):
        """This method registers a callback to be called whenever a new 'current_temperature' property update is received."""
        self._current_temperature_property_callbacks.append(handler)

    def on_current_condition_updates(self, handler: Callable[[stinger_types.WeatherCondition, str], None]):
        """This method registers a callback to be called whenever a new 'current_condition' property update is received."""
        self._current_condition_property_callbacks.append(handler)

    def on_daily_forecast_updates(self, handler: Callable[[stinger_types.ForecastForDay, stinger_types.ForecastForDay, stinger_types.ForecastForDay], None]):
        """This method registers a callback to be called whenever a new 'daily_forecast' property update is received."""
        self._daily_forecast_property_callbacks.append(handler)

    def on_hourly_forecast_updates(self, handler: Callable[[stinger_types.ForecastForHour, stinger_types.ForecastForHour, stinger_types.ForecastForHour, stinger_types.ForecastForHour], None]):
        """This method registers a callback to be called whenever a new 'hourly_forecast' property update is received."""
        self._hourly_forecast_property_callbacks.append(handler)

    def on_current_condition_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'current_condition_refresh_interval' property update is received."""
        self._current_condition_refresh_interval_property_callbacks.append(handler)

    def on_hourly_forecast_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'hourly_forecast_refresh_interval' property update is received."""
        self._hourly_forecast_refresh_interval_property_callbacks.append(handler)

    def on_daily_forecast_refresh_interval_updates(self, handler: Callable[[int], None]):
        """This method registers a callback to be called whenever a new 'daily_forecast_refresh_interval' property update is received."""
        self._daily_forecast_refresh_interval_property_callbacks.append(handler)

    def build(self) -> WeatherServer:
        new_server = WeatherServer(self._conn)

        if self._refresh_daily_forecast_method_handler is not None:
            new_server.handle_refresh_daily_forecast(self._refresh_daily_forecast_method_handler)
        if self._refresh_hourly_forecast_method_handler is not None:
            new_server.handle_refresh_hourly_forecast(self._refresh_hourly_forecast_method_handler)
        if self._refresh_current_conditions_method_handler is not None:
            new_server.handle_refresh_current_conditions(self._refresh_current_conditions_method_handler)

        for callback in self._location_property_callbacks:
            new_server.on_location_updates(callback)

        for callback in self._current_temperature_property_callbacks:
            new_server.on_current_temperature_updates(callback)

        for callback in self._current_condition_property_callbacks:
            new_server.on_current_condition_updates(callback)

        for callback in self._daily_forecast_property_callbacks:
            new_server.on_daily_forecast_updates(callback)

        for callback in self._hourly_forecast_property_callbacks:
            new_server.on_hourly_forecast_updates(callback)

        for callback in self._current_condition_refresh_interval_property_callbacks:
            new_server.on_current_condition_refresh_interval_updates(callback)

        for callback in self._hourly_forecast_refresh_interval_property_callbacks:
            new_server.on_hourly_forecast_refresh_interval_updates(callback)

        for callback in self._daily_forecast_refresh_interval_property_callbacks:
            new_server.on_daily_forecast_refresh_interval_updates(callback)

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
    service_id = "1"
    conn = MqttBrokerConnection(transport)
    server = WeatherServer(conn, service_id)

    server.location = stinger_types.LocationProperty(
        latitude=3.14,
        longitude=3.14,
    )

    server.current_temperature = 3.14

    server.current_condition = stinger_types.CurrentConditionProperty(
        condition=stinger_types.WeatherCondition.SUNNY,
        description="apples",
    )

    server.daily_forecast = stinger_types.DailyForecastProperty(
        monday=stinger_types.ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=stinger_types.WeatherCondition.SUNNY, start_time="apples", end_time="apples"),
        tuesday=stinger_types.ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=stinger_types.WeatherCondition.SUNNY, start_time="apples", end_time="apples"),
        wednesday=stinger_types.ForecastForDay(high_temperature=3.14, low_temperature=3.14, condition=stinger_types.WeatherCondition.SUNNY, start_time="apples", end_time="apples"),
    )

    server.hourly_forecast = stinger_types.HourlyForecastProperty(
        hour_0=stinger_types.ForecastForHour(temperature=3.14, starttime="apples", condition=stinger_types.WeatherCondition.SUNNY),
        hour_1=stinger_types.ForecastForHour(temperature=3.14, starttime="apples", condition=stinger_types.WeatherCondition.SUNNY),
        hour_2=stinger_types.ForecastForHour(temperature=3.14, starttime="apples", condition=stinger_types.WeatherCondition.SUNNY),
        hour_3=stinger_types.ForecastForHour(temperature=3.14, starttime="apples", condition=stinger_types.WeatherCondition.SUNNY),
    )

    server.current_condition_refresh_interval = 42

    server.hourly_forecast_refresh_interval = 42

    server.daily_forecast_refresh_interval = 42

    @server.handle_refresh_daily_forecast
    def refresh_daily_forecast() -> None:
        """This is an example handler for the 'refresh_daily_forecast' method."""
        print(f"Running refresh_daily_forecast'()'")
        return None

    @server.handle_refresh_hourly_forecast
    def refresh_hourly_forecast() -> None:
        """This is an example handler for the 'refresh_hourly_forecast' method."""
        print(f"Running refresh_hourly_forecast'()'")
        return None

    @server.handle_refresh_current_conditions
    def refresh_current_conditions() -> None:
        """This is an example handler for the 'refresh_current_conditions' method."""
        print(f"Running refresh_current_conditions'()'")
        return None

    @server.on_location_updates
    def on_location_update(latitude: float, longitude: float):
        print(f"Received update for 'location' property: { latitude= }, { longitude= }")

    @server.on_current_temperature_updates
    def on_current_temperature_update(temperature_f: float):
        print(f"Received update for 'current_temperature' property: { temperature_f= }")

    @server.on_current_condition_updates
    def on_current_condition_update(condition: stinger_types.WeatherCondition, description: str):
        print(f"Received update for 'current_condition' property: { condition= }, { description= }")

    @server.on_daily_forecast_updates
    def on_daily_forecast_update(monday: stinger_types.ForecastForDay, tuesday: stinger_types.ForecastForDay, wednesday: stinger_types.ForecastForDay):
        print(f"Received update for 'daily_forecast' property: { monday= }, { tuesday= }, { wednesday= }")

    @server.on_hourly_forecast_updates
    def on_hourly_forecast_update(hour_0: stinger_types.ForecastForHour, hour_1: stinger_types.ForecastForHour, hour_2: stinger_types.ForecastForHour, hour_3: stinger_types.ForecastForHour):
        print(f"Received update for 'hourly_forecast' property: { hour_0= }, { hour_1= }, { hour_2= }, { hour_3= }")

    @server.on_current_condition_refresh_interval_updates
    def on_current_condition_refresh_interval_update(seconds: int):
        print(f"Received update for 'current_condition_refresh_interval' property: { seconds= }")

    @server.on_hourly_forecast_refresh_interval_updates
    def on_hourly_forecast_refresh_interval_update(seconds: int):
        print(f"Received update for 'hourly_forecast_refresh_interval' property: { seconds= }")

    @server.on_daily_forecast_refresh_interval_updates
    def on_daily_forecast_refresh_interval_update(seconds: int):
        print(f"Received update for 'daily_forecast_refresh_interval' property: { seconds= }")

    print("Ctrl-C will stop the program.")

    while True:
        try:
            server.emit_current_time("apples")

            sleep(4)
            server.emit_current_time(current_time="apples")

            sleep(6)
        except KeyboardInterrupt:
            break

    signal.pause()
