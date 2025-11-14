"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the weather interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
"""

from typing import Dict, Callable, List, Any, Optional
from uuid import uuid4
from functools import partial, wraps
import json
import logging
from datetime import datetime, timedelta, UTC
from isodate import parse_duration

import asyncio
import concurrent.futures as futures
from .method_codes import *
from .interface_types import *
import threading

from .connection import IBrokerConnection

from .property import WeatherInitialPropertyValues

from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)

CurrentTimeSignalCallbackType = Callable[[str], None]
RefreshDailyForecastMethodResponseCallbackType = Callable[[], None]
RefreshHourlyForecastMethodResponseCallbackType = Callable[[], None]
RefreshCurrentConditionsMethodResponseCallbackType = Callable[[], None]

LocationPropertyUpdatedCallbackType = Callable[[LocationProperty], None]
CurrentTemperaturePropertyUpdatedCallbackType = Callable[[float], None]
CurrentConditionPropertyUpdatedCallbackType = Callable[[CurrentConditionProperty], None]
DailyForecastPropertyUpdatedCallbackType = Callable[[DailyForecastProperty], None]
HourlyForecastPropertyUpdatedCallbackType = Callable[[HourlyForecastProperty], None]
CurrentConditionRefreshIntervalPropertyUpdatedCallbackType = Callable[[int], None]
HourlyForecastRefreshIntervalPropertyUpdatedCallbackType = Callable[[int], None]
DailyForecastRefreshIntervalPropertyUpdatedCallbackType = Callable[[int], None]


class DiscoveredInstance(BaseModel):
    instance_id: str
    initial_property_values: WeatherInitialPropertyValues


class WeatherClient:

    def __init__(self, connection: IBrokerConnection, instance_info: DiscoveredInstance):
        """Constructor for a `WeatherClient` object."""
        self._logger = logging.getLogger("WeatherClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing WeatherClient")
        self._conn = connection
        self._conn.add_message_callback(self._receive_message)
        self._service_id = instance_info.instance_id

        self._pending_method_responses: dict[str, Callable[..., None]] = {}

        self._property_location = instance_info.initial_property_values.location  # type: LocationProperty
        self._property_location_mutex = threading.Lock()
        self._property_location_version = instance_info.initial_property_values.location_version
        self._conn.subscribe("weather/{}/property/location/value".format(self._service_id), self._receive_location_property_update_message)
        self._changed_value_callbacks_for_location: list[LocationPropertyUpdatedCallbackType] = []
        self._property_current_temperature = instance_info.initial_property_values.current_temperature  # type: float
        self._property_current_temperature_mutex = threading.Lock()
        self._property_current_temperature_version = instance_info.initial_property_values.current_temperature_version
        self._conn.subscribe("weather/{}/property/currentTemperature/value".format(self._service_id), self._receive_current_temperature_property_update_message)
        self._changed_value_callbacks_for_current_temperature: list[CurrentTemperaturePropertyUpdatedCallbackType] = []
        self._property_current_condition = instance_info.initial_property_values.current_condition  # type: CurrentConditionProperty
        self._property_current_condition_mutex = threading.Lock()
        self._property_current_condition_version = instance_info.initial_property_values.current_condition_version
        self._conn.subscribe("weather/{}/property/currentCondition/value".format(self._service_id), self._receive_current_condition_property_update_message)
        self._changed_value_callbacks_for_current_condition: list[CurrentConditionPropertyUpdatedCallbackType] = []
        self._property_daily_forecast = instance_info.initial_property_values.daily_forecast  # type: DailyForecastProperty
        self._property_daily_forecast_mutex = threading.Lock()
        self._property_daily_forecast_version = instance_info.initial_property_values.daily_forecast_version
        self._conn.subscribe("weather/{}/property/dailyForecast/value".format(self._service_id), self._receive_daily_forecast_property_update_message)
        self._changed_value_callbacks_for_daily_forecast: list[DailyForecastPropertyUpdatedCallbackType] = []
        self._property_hourly_forecast = instance_info.initial_property_values.hourly_forecast  # type: HourlyForecastProperty
        self._property_hourly_forecast_mutex = threading.Lock()
        self._property_hourly_forecast_version = instance_info.initial_property_values.hourly_forecast_version
        self._conn.subscribe("weather/{}/property/hourlyForecast/value".format(self._service_id), self._receive_hourly_forecast_property_update_message)
        self._changed_value_callbacks_for_hourly_forecast: list[HourlyForecastPropertyUpdatedCallbackType] = []
        self._property_current_condition_refresh_interval = instance_info.initial_property_values.current_condition_refresh_interval  # type: int
        self._property_current_condition_refresh_interval_mutex = threading.Lock()
        self._property_current_condition_refresh_interval_version = instance_info.initial_property_values.current_condition_refresh_interval_version
        self._conn.subscribe("weather/{}/property/currentConditionRefreshInterval/value".format(self._service_id), self._receive_current_condition_refresh_interval_property_update_message)
        self._changed_value_callbacks_for_current_condition_refresh_interval: list[CurrentConditionRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_hourly_forecast_refresh_interval = instance_info.initial_property_values.hourly_forecast_refresh_interval  # type: int
        self._property_hourly_forecast_refresh_interval_mutex = threading.Lock()
        self._property_hourly_forecast_refresh_interval_version = instance_info.initial_property_values.hourly_forecast_refresh_interval_version
        self._conn.subscribe("weather/{}/property/hourlyForecastRefreshInterval/value".format(self._service_id), self._receive_hourly_forecast_refresh_interval_property_update_message)
        self._changed_value_callbacks_for_hourly_forecast_refresh_interval: list[HourlyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_daily_forecast_refresh_interval = instance_info.initial_property_values.daily_forecast_refresh_interval  # type: int
        self._property_daily_forecast_refresh_interval_mutex = threading.Lock()
        self._property_daily_forecast_refresh_interval_version = instance_info.initial_property_values.daily_forecast_refresh_interval_version
        self._conn.subscribe("weather/{}/property/dailyForecastRefreshInterval/value".format(self._service_id), self._receive_daily_forecast_refresh_interval_property_update_message)
        self._changed_value_callbacks_for_daily_forecast_refresh_interval: list[DailyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_current_time: list[CurrentTimeSignalCallbackType] = []
        self._conn.subscribe(f"client/{self._conn.client_id}/weather/methodResponse", self._receive_any_method_response_message)

        self._property_response_topic = f"client/{self._conn.client_id}/weather/propertyUpdateResponse"
        self._conn.subscribe(self._property_response_topic, self._receive_any_property_response_message)

    @property
    def location(self) -> LocationProperty:
        """Property 'location' getter."""
        with self._property_location_mutex:
            return self._property_location

    @location.setter
    def location(self, value: LocationProperty):
        """Serializes and publishes the 'location' property."""
        if not isinstance(value, LocationProperty):
            raise ValueError("The 'location' property must be a LocationProperty")
        property_obj = value
        self._logger.debug("Setting 'location' property to %s", property_obj)
        with self._property_location_mutex:
            self._conn.publish_property_update_request(
                "weather/{}/property/location/setValue".format(self._service_id), property_obj, str(self._property_location_version), self._property_response_topic
            )

    def location_changed(self, handler: LocationPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'location' property changes.
        Can be used as a decorator.
        """
        with self._property_location_mutex:
            self._changed_value_callbacks_for_location.append(handler)
            if call_immediately and self._property_location is not None:
                handler(self._property_location)
        return handler

    @property
    def current_temperature(self) -> float:
        """Property 'current_temperature' getter."""
        with self._property_current_temperature_mutex:
            return self._property_current_temperature

    def current_temperature_changed(self, handler: CurrentTemperaturePropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'current_temperature' property changes.
        Can be used as a decorator.
        """
        with self._property_current_temperature_mutex:
            self._changed_value_callbacks_for_current_temperature.append(handler)
            if call_immediately and self._property_current_temperature is not None:
                handler(self._property_current_temperature)
        return handler

    @property
    def current_condition(self) -> CurrentConditionProperty:
        """Property 'current_condition' getter."""
        with self._property_current_condition_mutex:
            return self._property_current_condition

    def current_condition_changed(self, handler: CurrentConditionPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'current_condition' property changes.
        Can be used as a decorator.
        """
        with self._property_current_condition_mutex:
            self._changed_value_callbacks_for_current_condition.append(handler)
            if call_immediately and self._property_current_condition is not None:
                handler(self._property_current_condition)
        return handler

    @property
    def daily_forecast(self) -> DailyForecastProperty:
        """Property 'daily_forecast' getter."""
        with self._property_daily_forecast_mutex:
            return self._property_daily_forecast

    def daily_forecast_changed(self, handler: DailyForecastPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'daily_forecast' property changes.
        Can be used as a decorator.
        """
        with self._property_daily_forecast_mutex:
            self._changed_value_callbacks_for_daily_forecast.append(handler)
            if call_immediately and self._property_daily_forecast is not None:
                handler(self._property_daily_forecast)
        return handler

    @property
    def hourly_forecast(self) -> HourlyForecastProperty:
        """Property 'hourly_forecast' getter."""
        with self._property_hourly_forecast_mutex:
            return self._property_hourly_forecast

    def hourly_forecast_changed(self, handler: HourlyForecastPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'hourly_forecast' property changes.
        Can be used as a decorator.
        """
        with self._property_hourly_forecast_mutex:
            self._changed_value_callbacks_for_hourly_forecast.append(handler)
            if call_immediately and self._property_hourly_forecast is not None:
                handler(self._property_hourly_forecast)
        return handler

    @property
    def current_condition_refresh_interval(self) -> int:
        """Property 'current_condition_refresh_interval' getter."""
        with self._property_current_condition_refresh_interval_mutex:
            return self._property_current_condition_refresh_interval

    @current_condition_refresh_interval.setter
    def current_condition_refresh_interval(self, value: int):
        """Serializes and publishes the 'current_condition_refresh_interval' property."""
        if not isinstance(value, int):
            raise ValueError("The 'current_condition_refresh_interval' property must be a int")
        property_obj = CurrentConditionRefreshIntervalProperty(seconds=value)
        self._logger.debug("Setting 'current_condition_refresh_interval' property to %s", property_obj)
        with self._property_current_condition_refresh_interval_mutex:
            self._conn.publish_property_update_request(
                "weather/{}/property/currentConditionRefreshInterval/setValue".format(self._service_id),
                property_obj,
                str(self._property_current_condition_refresh_interval_version),
                self._property_response_topic,
            )

    def current_condition_refresh_interval_changed(self, handler: CurrentConditionRefreshIntervalPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'current_condition_refresh_interval' property changes.
        Can be used as a decorator.
        """
        with self._property_current_condition_refresh_interval_mutex:
            self._changed_value_callbacks_for_current_condition_refresh_interval.append(handler)
            if call_immediately and self._property_current_condition_refresh_interval is not None:
                handler(self._property_current_condition_refresh_interval)
        return handler

    @property
    def hourly_forecast_refresh_interval(self) -> int:
        """Property 'hourly_forecast_refresh_interval' getter."""
        with self._property_hourly_forecast_refresh_interval_mutex:
            return self._property_hourly_forecast_refresh_interval

    @hourly_forecast_refresh_interval.setter
    def hourly_forecast_refresh_interval(self, value: int):
        """Serializes and publishes the 'hourly_forecast_refresh_interval' property."""
        if not isinstance(value, int):
            raise ValueError("The 'hourly_forecast_refresh_interval' property must be a int")
        property_obj = HourlyForecastRefreshIntervalProperty(seconds=value)
        self._logger.debug("Setting 'hourly_forecast_refresh_interval' property to %s", property_obj)
        with self._property_hourly_forecast_refresh_interval_mutex:
            self._conn.publish_property_update_request(
                "weather/{}/property/hourlyForecastRefreshInterval/setValue".format(self._service_id),
                property_obj,
                str(self._property_hourly_forecast_refresh_interval_version),
                self._property_response_topic,
            )

    def hourly_forecast_refresh_interval_changed(self, handler: HourlyForecastRefreshIntervalPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'hourly_forecast_refresh_interval' property changes.
        Can be used as a decorator.
        """
        with self._property_hourly_forecast_refresh_interval_mutex:
            self._changed_value_callbacks_for_hourly_forecast_refresh_interval.append(handler)
            if call_immediately and self._property_hourly_forecast_refresh_interval is not None:
                handler(self._property_hourly_forecast_refresh_interval)
        return handler

    @property
    def daily_forecast_refresh_interval(self) -> int:
        """Property 'daily_forecast_refresh_interval' getter."""
        with self._property_daily_forecast_refresh_interval_mutex:
            return self._property_daily_forecast_refresh_interval

    @daily_forecast_refresh_interval.setter
    def daily_forecast_refresh_interval(self, value: int):
        """Serializes and publishes the 'daily_forecast_refresh_interval' property."""
        if not isinstance(value, int):
            raise ValueError("The 'daily_forecast_refresh_interval' property must be a int")
        property_obj = DailyForecastRefreshIntervalProperty(seconds=value)
        self._logger.debug("Setting 'daily_forecast_refresh_interval' property to %s", property_obj)
        with self._property_daily_forecast_refresh_interval_mutex:
            self._conn.publish_property_update_request(
                "weather/{}/property/dailyForecastRefreshInterval/setValue".format(self._service_id),
                property_obj,
                str(self._property_daily_forecast_refresh_interval_version),
                self._property_response_topic,
            )

    def daily_forecast_refresh_interval_changed(self, handler: DailyForecastRefreshIntervalPropertyUpdatedCallbackType, call_immediately: bool = False):
        """Sets a callback to be called when the 'daily_forecast_refresh_interval' property changes.
        Can be used as a decorator.
        """
        with self._property_daily_forecast_refresh_interval_mutex:
            self._changed_value_callbacks_for_daily_forecast_refresh_interval.append(handler)
            if call_immediately and self._property_daily_forecast_refresh_interval is not None:
                handler(self._property_daily_forecast_refresh_interval)
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

    def _receive_current_time_signal_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'current_time' signal with non-JSON content type")
            return

        model = CurrentTimeSignalPayload.model_validate_json(payload)
        kwargs = model.model_dump()

        self._do_callbacks_for(self._signal_recv_callbacks_for_current_time, **kwargs)

    def _receive_any_method_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle '' method response.
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

    def _receive_any_property_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        user_properties = properties.get("UserProperty", {})
        return_code = user_properties.get("ReturnCode")
        if return_code is not None and int(return_code) != MethodReturnCode.SUCCESS.value:
            debug_info = user_properties.get("DebugInfo", "")
            self._logger.warning("Received error return value %s from property update: %s", return_code, debug_info)

    def _receive_location_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'location' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'location' property change with non-JSON content type")
            return
        try:
            prop_obj = LocationProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_location_mutex:
                self._property_location = prop_obj
                self._property_location_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_location, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'location' property change: %s", exc_info=e)

    def _receive_current_temperature_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'current_temperature' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'current_temperature' property change with non-JSON content type")
            return
        try:
            prop_obj = CurrentTemperatureProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_current_temperature_mutex:
                self._property_current_temperature = prop_obj
                self._property_current_temperature_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_current_temperature, value=prop_obj.temperature_f)

        except Exception as e:
            self._logger.exception("Error processing 'current_temperature' property change: %s", exc_info=e)

    def _receive_current_condition_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'current_condition' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'current_condition' property change with non-JSON content type")
            return
        try:
            prop_obj = CurrentConditionProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_current_condition_mutex:
                self._property_current_condition = prop_obj
                self._property_current_condition_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_current_condition, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'current_condition' property change: %s", exc_info=e)

    def _receive_daily_forecast_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'daily_forecast' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'daily_forecast' property change with non-JSON content type")
            return
        try:
            prop_obj = DailyForecastProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_daily_forecast_mutex:
                self._property_daily_forecast = prop_obj
                self._property_daily_forecast_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_daily_forecast, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'daily_forecast' property change: %s", exc_info=e)

    def _receive_hourly_forecast_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'hourly_forecast' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'hourly_forecast' property change with non-JSON content type")
            return
        try:
            prop_obj = HourlyForecastProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_hourly_forecast_mutex:
                self._property_hourly_forecast = prop_obj
                self._property_hourly_forecast_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_hourly_forecast, value=prop_obj)

        except Exception as e:
            self._logger.exception("Error processing 'hourly_forecast' property change: %s", exc_info=e)

    def _receive_current_condition_refresh_interval_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'current_condition_refresh_interval' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'current_condition_refresh_interval' property change with non-JSON content type")
            return
        try:
            prop_obj = CurrentConditionRefreshIntervalProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_current_condition_refresh_interval_mutex:
                self._property_current_condition_refresh_interval = prop_obj
                self._property_current_condition_refresh_interval_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_current_condition_refresh_interval, value=prop_obj.seconds)

        except Exception as e:
            self._logger.exception("Error processing 'current_condition_refresh_interval' property change: %s", exc_info=e)

    def _receive_hourly_forecast_refresh_interval_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'hourly_forecast_refresh_interval' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'hourly_forecast_refresh_interval' property change with non-JSON content type")
            return
        try:
            prop_obj = HourlyForecastRefreshIntervalProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_hourly_forecast_refresh_interval_mutex:
                self._property_hourly_forecast_refresh_interval = prop_obj
                self._property_hourly_forecast_refresh_interval_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_hourly_forecast_refresh_interval, value=prop_obj.seconds)

        except Exception as e:
            self._logger.exception("Error processing 'hourly_forecast_refresh_interval' property change: %s", exc_info=e)

    def _receive_daily_forecast_refresh_interval_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'daily_forecast_refresh_interval' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'daily_forecast_refresh_interval' property change with non-JSON content type")
            return
        try:
            prop_obj = DailyForecastRefreshIntervalProperty.model_validate_json(payload)
            user_properties = properties.get("UserProperty", {})
            property_version = int(user_properties.get("PropertyVersion", -1))
            with self._property_daily_forecast_refresh_interval_mutex:
                self._property_daily_forecast_refresh_interval = prop_obj
                self._property_daily_forecast_refresh_interval_version = property_version

                self._do_callbacks_for(self._changed_value_callbacks_for_daily_forecast_refresh_interval, value=prop_obj.seconds)

        except Exception as e:
            self._logger.exception("Error processing 'daily_forecast_refresh_interval' property change: %s", exc_info=e)

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """New MQTT messages are passed to this method, which, based on the topic,
        calls the appropriate handler method for the message.
        """
        self._logger.warning("Receiving message sent to %s, but without a handler", topic)

    def receive_current_time(self, handler: CurrentTimeSignalCallbackType):
        """Used as a decorator for methods which handle particular signals."""
        self._signal_recv_callbacks_for_current_time.append(handler)
        if len(self._signal_recv_callbacks_for_current_time) == 1:
            self._conn.subscribe("weather/{}/signal/currentTime".format(self._service_id), self._receive_current_time_signal_message)
        return handler

    def refresh_daily_forecast(
        self,
    ) -> futures.Future:
        """Calling this initiates a `refresh_daily_forecast` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_refresh_daily_forecast_response, fut)
        payload = RefreshDailyForecastMethodRequest()
        json_payload = payload.model_dump_json(by_alias=True)
        self._logger.debug("Calling 'refresh_daily_forecast' method with payload %s", json_payload)
        response_topic = f"client/{self._conn.client_id}/weather/methodResponse"
        self._conn.publish("weather/{}/method/refreshDailyForecast".format(self._service_id), json_payload, qos=2, retain=False, correlation_id=correlation_id, response_topic=response_topic)
        return fut

    def _handle_refresh_daily_forecast_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `refresh_daily_forecast` IPC method call."""
        self._logger.debug("Handling refresh_daily_forecast response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'refresh_daily_forecast' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = RefreshDailyForecastMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'refresh_daily_forecast' method: {e}"))

        if not fut.done():
            fut.set_result(None)
            return
        else:
            self._logger.warning("Future for 'refresh_daily_forecast' method was already done!")

    def refresh_hourly_forecast(
        self,
    ) -> futures.Future:
        """Calling this initiates a `refresh_hourly_forecast` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_refresh_hourly_forecast_response, fut)
        payload = RefreshHourlyForecastMethodRequest()
        json_payload = payload.model_dump_json(by_alias=True)
        self._logger.debug("Calling 'refresh_hourly_forecast' method with payload %s", json_payload)
        response_topic = f"client/{self._conn.client_id}/weather/methodResponse"
        self._conn.publish("weather/{}/method/refreshHourlyForecast".format(self._service_id), json_payload, qos=2, retain=False, correlation_id=correlation_id, response_topic=response_topic)
        return fut

    def _handle_refresh_hourly_forecast_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `refresh_hourly_forecast` IPC method call."""
        self._logger.debug("Handling refresh_hourly_forecast response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'refresh_hourly_forecast' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = RefreshHourlyForecastMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'refresh_hourly_forecast' method: {e}"))

        if not fut.done():
            fut.set_result(None)
            return
        else:
            self._logger.warning("Future for 'refresh_hourly_forecast' method was already done!")

    def refresh_current_conditions(
        self,
    ) -> futures.Future:
        """Calling this initiates a `refresh_current_conditions` IPC method call."""
        fut = futures.Future()  # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_refresh_current_conditions_response, fut)
        payload = RefreshCurrentConditionsMethodRequest()
        json_payload = payload.model_dump_json(by_alias=True)
        self._logger.debug("Calling 'refresh_current_conditions' method with payload %s", json_payload)
        response_topic = f"client/{self._conn.client_id}/weather/methodResponse"
        self._conn.publish("weather/{}/method/refreshCurrentConditions".format(self._service_id), json_payload, qos=2, retain=False, correlation_id=correlation_id, response_topic=response_topic)
        return fut

    def _handle_refresh_current_conditions_response(self, fut: futures.Future, response_json_text: str, return_value: MethodReturnCode, debug_message: Optional[str] = None):
        """This called with the response to a `refresh_current_conditions` IPC method call."""
        self._logger.debug("Handling refresh_current_conditions response message %s", fut)

        if return_value != MethodReturnCode.SUCCESS.value:
            self._logger.warning("Received error return value %s from 'refresh_current_conditions' method: %s", return_value, debug_message)
            fut.set_exception(stinger_exception_factory(return_value, debug_message))
            return

        try:
            resp_model = RefreshCurrentConditionsMethodResponse.model_validate_json(response_json_text)
        except Exception as e:
            fut.set_exception(ClientDeserializationErrorStingerMethodException(f"Failed to deserialize response to 'refresh_current_conditions' method: {e}"))

        if not fut.done():
            fut.set_result(None)
            return
        else:
            self._logger.warning("Future for 'refresh_current_conditions' method was already done!")


class WeatherClientBuilder:
    """Using decorators from WeatherClient doesn't work if you are trying to create multiple instances of WeatherClient.
    Instead, use this builder to create a registry of callbacks, and then build clients using the registry.

    When ready to create a WeatherClient instance, call the `build(broker, service_instance_id)` method.
    """

    def __init__(self):
        """Creates a new WeatherClientBuilder."""
        self._logger = logging.getLogger("WeatherClientBuilder")
        self._signal_recv_callbacks_for_current_time = []  # type: List[CurrentTimeSignalCallbackType]
        self._property_updated_callbacks_for_location: list[LocationPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_current_temperature: list[CurrentTemperaturePropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_current_condition: list[CurrentConditionPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_daily_forecast: list[DailyForecastPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_hourly_forecast: list[HourlyForecastPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_current_condition_refresh_interval: list[CurrentConditionRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_hourly_forecast_refresh_interval: list[HourlyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_daily_forecast_refresh_interval: list[DailyForecastRefreshIntervalPropertyUpdatedCallbackType] = []

    def receive_current_time(self, handler):
        """Used as a decorator for methods which handle particular signals."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._signal_recv_callbacks_for_current_time.append(wrapper)
        return wrapper

    def location_updated(self, handler: LocationPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_location.append(wrapper)
        return wrapper

    def current_temperature_updated(self, handler: CurrentTemperaturePropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_current_temperature.append(wrapper)
        return wrapper

    def current_condition_updated(self, handler: CurrentConditionPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_current_condition.append(wrapper)
        return wrapper

    def daily_forecast_updated(self, handler: DailyForecastPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_daily_forecast.append(wrapper)
        return wrapper

    def hourly_forecast_updated(self, handler: HourlyForecastPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_hourly_forecast.append(wrapper)
        return wrapper

    def current_condition_refresh_interval_updated(self, handler: CurrentConditionRefreshIntervalPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_current_condition_refresh_interval.append(wrapper)
        return wrapper

    def hourly_forecast_refresh_interval_updated(self, handler: HourlyForecastRefreshIntervalPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_hourly_forecast_refresh_interval.append(wrapper)
        return wrapper

    def daily_forecast_refresh_interval_updated(self, handler: DailyForecastRefreshIntervalPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""

        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)

        self._property_updated_callbacks_for_daily_forecast_refresh_interval.append(wrapper)
        return wrapper

    def build(self, broker: IBrokerConnection, instance_info: DiscoveredInstance, binding: Optional[Any] = None) -> WeatherClient:
        """Builds a new WeatherClient."""
        self._logger.debug("Building WeatherClient for service instance %s", instance_info.instance_id)
        client = WeatherClient(broker, instance_info)

        for cb in self._signal_recv_callbacks_for_current_time:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.receive_current_time(bound_cb)
            else:
                client.receive_current_time(cb)

        for cb in self._property_updated_callbacks_for_location:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.location_changed(bound_cb)
            else:
                client.location_changed(cb)

        for cb in self._property_updated_callbacks_for_current_temperature:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.current_temperature_changed(bound_cb)
            else:
                client.current_temperature_changed(cb)

        for cb in self._property_updated_callbacks_for_current_condition:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.current_condition_changed(bound_cb)
            else:
                client.current_condition_changed(cb)

        for cb in self._property_updated_callbacks_for_daily_forecast:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.daily_forecast_changed(bound_cb)
            else:
                client.daily_forecast_changed(cb)

        for cb in self._property_updated_callbacks_for_hourly_forecast:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.hourly_forecast_changed(bound_cb)
            else:
                client.hourly_forecast_changed(cb)

        for cb in self._property_updated_callbacks_for_current_condition_refresh_interval:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.current_condition_refresh_interval_changed(bound_cb)
            else:
                client.current_condition_refresh_interval_changed(cb)

        for cb in self._property_updated_callbacks_for_hourly_forecast_refresh_interval:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.hourly_forecast_refresh_interval_changed(bound_cb)
            else:
                client.hourly_forecast_refresh_interval_changed(cb)

        for cb in self._property_updated_callbacks_for_daily_forecast_refresh_interval:
            if binding:
                bound_cb = cb.__get__(binding, binding.__class__)
                client.daily_forecast_refresh_interval_changed(bound_cb)
            else:
                client.daily_forecast_refresh_interval_changed(cb)

        return client


class WeatherClientDiscoverer:

    def __init__(self, connection: IBrokerConnection, builder: Optional[WeatherClientBuilder] = None, build_binding: Optional[Any] = None):
        """Creates a new WeatherClientDiscoverer."""
        self._conn = connection
        self._builder = builder
        self._build_binding = build_binding
        self._logger = logging.getLogger("WeatherClientDiscoverer")
        self._logger.setLevel(logging.DEBUG)
        service_discovery_topic = "weather/{}/interface".format("+")
        self._conn.subscribe(service_discovery_topic, self._process_service_discovery_message)
        self._conn.subscribe("weather/+/property/+/value", self._process_property_value_message)
        self._mutex = threading.Lock()
        self._pending_futures: List[futures.Future] = []
        self._removed_service_callbacks: List[Callable[[str], None]] = []

        # For partially discovered services
        self._discovered_interface_infos = dict()  # type: Dict[str, InterfaceInfo]
        self._discovered_properties = dict()  # type: Dict[str, Dict[str, Any]]

        # For fully discovered services
        self._discovered_services: Dict[str, DiscoveredInstance] = {}
        self._discovered_service_callbacks: List[Callable[[DiscoveredInstance], None]] = []

    def add_discovered_service_callback(self, callback: Callable[[DiscoveredInstance], None]):
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

    def get_discovery_info(self, instance_id: str) -> Optional[InterfaceInfo]:
        """Returns the InterfaceInfo for a discovered service instance ID, or None if not found."""
        with self._mutex:
            return self._discovered_services.get(instance_id, None)

    def get_singleton_client(self) -> futures.Future[WeatherClient]:
        """Returns a WeatherClient for the single discovered service.
        Raises an exception if there is not exactly one discovered service.
        """
        fut = futures.Future()  # type: futures.Future[WeatherClient]
        with self._mutex:
            if len(self._discovered_services) > 0:
                instance_info = next(iter(self._discovered_services))
                if self._builder is None:
                    fut.set_result(WeatherClient(self._conn, instance_info))
                else:
                    new_client = self._builder.build(self._conn, instance_info, self._build_binding)
                    fut.set_result(new_client)
            else:
                self._pending_futures.append(fut)
        return fut

    def _check_for_fully_discovered(self, instance_id: str):
        """Checks if all properties have been discovered for the given instance ID."""
        with self._mutex:
            if instance_id in self._discovered_properties and len(self._discovered_properties[instance_id]) == 16 and instance_id in self._discovered_interface_infos:

                entry = DiscoveredInstance(instance_id=instance_id, initial_property_values=WeatherInitialPropertyValues(**self._discovered_properties[instance_id]))

                self._discovered_services[instance_id] = entry
                while self._pending_futures:
                    fut = self._pending_futures.pop(0)
                    if not fut.done():
                        if self._builder is not None:
                            fut.set_result(self._builder.build(self._conn, entry, self._build_binding))
                        else:
                            fut.set_result(WeatherClient(self._conn, entry))
                if not instance_id in self._discovered_services:
                    self._logger.info("Discovered service: %s.instance", instance_id)
                    for cb in self._discovered_service_callbacks:
                        cb(entry)
                else:
                    self._logger.debug("Updated info for service: %s", instance_id)

    def _process_service_discovery_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """Processes a service discovery message."""
        self._logger.debug("Processing service discovery message on topic %s", topic)
        if len(payload) > 0:
            try:
                service_info = InterfaceInfo.model_validate_json(payload)
                with self._mutex:
                    self._discovered_interface_infos[service_info.instance] = service_info
            except Exception as e:
                self._logger.warning("Failed to process service discovery message: %s", e)
            self._check_for_fully_discovered(service_info.instance)

        else:  # Empty payload means the service is going away
            instance_id = topic.split("/")[-2]
            with self._mutex:
                if instance_id in self._discovered_services:
                    self._logger.info("Service %s is going away", instance_id)
                    if instance_id in self._discovered_services:
                        del self._discovered_services[instance_id]
                    if instance_id in self._discovered_interface_infos:
                        del self._discovered_interface_infos[instance_id]
                    if instance_id in self._discovered_properties:
                        del self._discovered_properties[instance_id]
                    for cb in self._removed_service_callbacks:
                        cb(instance_id)

    def _process_property_value_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """Processes a property value message for discovery purposes."""
        self._logger.debug("Processing property value message on topic %s", topic)
        instance_id = topic.split("/")[1]
        property_name = topic.split("/")[3]
        user_properties = properties.get("UserProperty", {})
        prop_version = user_properties.get("PropertyVersion", -1)
        try:
            prop_obj = json.loads(payload)
            with self._mutex:
                if instance_id not in self._discovered_properties:
                    self._discovered_properties[instance_id] = dict()

                if property_name == "location":

                    self._discovered_properties[instance_id]["location"] = prop_obj

                    self._discovered_properties[instance_id]["location_version"] = prop_version

                elif property_name == "currentTemperature":

                    self._discovered_properties[instance_id]["current_temperature"] = prop_obj.get("temperature_f")

                    self._discovered_properties[instance_id]["current_temperature_version"] = prop_version

                elif property_name == "currentCondition":

                    self._discovered_properties[instance_id]["current_condition"] = prop_obj

                    self._discovered_properties[instance_id]["current_condition_version"] = prop_version

                elif property_name == "dailyForecast":

                    self._discovered_properties[instance_id]["daily_forecast"] = prop_obj

                    self._discovered_properties[instance_id]["daily_forecast_version"] = prop_version

                elif property_name == "hourlyForecast":

                    self._discovered_properties[instance_id]["hourly_forecast"] = prop_obj

                    self._discovered_properties[instance_id]["hourly_forecast_version"] = prop_version

                elif property_name == "currentConditionRefreshInterval":

                    self._discovered_properties[instance_id]["current_condition_refresh_interval"] = prop_obj.get("seconds")

                    self._discovered_properties[instance_id]["current_condition_refresh_interval_version"] = prop_version

                elif property_name == "hourlyForecastRefreshInterval":

                    self._discovered_properties[instance_id]["hourly_forecast_refresh_interval"] = prop_obj.get("seconds")

                    self._discovered_properties[instance_id]["hourly_forecast_refresh_interval_version"] = prop_version

                elif property_name == "dailyForecastRefreshInterval":

                    self._discovered_properties[instance_id]["daily_forecast_refresh_interval"] = prop_obj.get("seconds")

                    self._discovered_properties[instance_id]["daily_forecast_refresh_interval_version"] = prop_version

            self._check_for_fully_discovered(instance_id)

        except Exception as e:
            self._logger.warning("Failed to process property value message: %s", e)
