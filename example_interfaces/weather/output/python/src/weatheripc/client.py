"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the weather interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
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
from .method_codes import *
from .interface_types import *
import threading

from .connection import IBrokerConnection

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


class WeatherClient:

    def __init__(self, connection: IBrokerConnection, service_instance_id: str):
        """Constructor for a `WeatherClient` object."""
        self._logger = logging.getLogger("WeatherClient")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing WeatherClient")
        self._conn = connection
        self._conn.add_message_callback(self._receive_message)
        self._service_id = service_instance_id

        self._pending_method_responses: dict[str, Callable[..., None]] = {}

        self._property_location = None  # type: Optional[LocationProperty]
        self._property_location_mutex = threading.Lock()
        self._property_location_version = -1
        self._conn.subscribe("weather/{}/property/location/value".format(self._service_id), self._receive_location_property_update_message)
        self._changed_value_callbacks_for_location: list[LocationPropertyUpdatedCallbackType] = []
        self._property_current_temperature = None  # type: Optional[float]
        self._property_current_temperature_mutex = threading.Lock()
        self._property_current_temperature_version = -1
        self._conn.subscribe("weather/{}/property/currentTemperature/value".format(self._service_id), self._receive_current_temperature_property_update_message)
        self._changed_value_callbacks_for_current_temperature: list[CurrentTemperaturePropertyUpdatedCallbackType] = []
        self._property_current_condition = None  # type: Optional[CurrentConditionProperty]
        self._property_current_condition_mutex = threading.Lock()
        self._property_current_condition_version = -1
        self._conn.subscribe("weather/{}/property/currentCondition/value".format(self._service_id), self._receive_current_condition_property_update_message)
        self._changed_value_callbacks_for_current_condition: list[CurrentConditionPropertyUpdatedCallbackType] = []
        self._property_daily_forecast = None  # type: Optional[DailyForecastProperty]
        self._property_daily_forecast_mutex = threading.Lock()
        self._property_daily_forecast_version = -1
        self._conn.subscribe("weather/{}/property/dailyForecast/value".format(self._service_id), self._receive_daily_forecast_property_update_message)
        self._changed_value_callbacks_for_daily_forecast: list[DailyForecastPropertyUpdatedCallbackType] = []
        self._property_hourly_forecast = None  # type: Optional[HourlyForecastProperty]
        self._property_hourly_forecast_mutex = threading.Lock()
        self._property_hourly_forecast_version = -1
        self._conn.subscribe("weather/{}/property/hourlyForecast/value".format(self._service_id), self._receive_hourly_forecast_property_update_message)
        self._changed_value_callbacks_for_hourly_forecast: list[HourlyForecastPropertyUpdatedCallbackType] = []
        self._property_current_condition_refresh_interval = None  # type: Optional[int]
        self._property_current_condition_refresh_interval_mutex = threading.Lock()
        self._property_current_condition_refresh_interval_version = -1
        self._conn.subscribe("weather/{}/property/currentConditionRefreshInterval/value".format(self._service_id), self._receive_current_condition_refresh_interval_property_update_message)
        self._changed_value_callbacks_for_current_condition_refresh_interval: list[CurrentConditionRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_hourly_forecast_refresh_interval = None  # type: Optional[int]
        self._property_hourly_forecast_refresh_interval_mutex = threading.Lock()
        self._property_hourly_forecast_refresh_interval_version = -1
        self._conn.subscribe("weather/{}/property/hourlyForecastRefreshInterval/value".format(self._service_id), self._receive_hourly_forecast_refresh_interval_property_update_message)
        self._changed_value_callbacks_for_hourly_forecast_refresh_interval: list[HourlyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_daily_forecast_refresh_interval = None  # type: Optional[int]
        self._property_daily_forecast_refresh_interval_mutex = threading.Lock()
        self._property_daily_forecast_refresh_interval_version = -1
        self._conn.subscribe("weather/{}/property/dailyForecastRefreshInterval/value".format(self._service_id), self._receive_daily_forecast_refresh_interval_property_update_message)
        self._changed_value_callbacks_for_daily_forecast_refresh_interval: list[DailyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_current_time: list[CurrentTimeSignalCallbackType] = []
        self._conn.subscribe(f"client/{self._conn.client_id}/refresh_daily_forecast/response", self._receive_refresh_daily_forecast_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/refresh_hourly_forecast/response", self._receive_refresh_hourly_forecast_response_message)
        self._conn.subscribe(f"client/{self._conn.client_id}/refresh_current_conditions/response", self._receive_refresh_current_conditions_response_message)

    @property
    def location(self) -> Optional[LocationProperty]:
        """Property 'location' getter."""
        return self._property_location

    @location.setter
    def location(self, value: LocationProperty):
        """Serializes and publishes the 'location' property."""
        if not isinstance(value, LocationProperty):
            raise ValueError("The 'location' property must be a LocationProperty")
        serialized = value.model_dump_json(exclude_none=True, by_alias=True)
        self._logger.debug("Setting 'location' property to %s", serialized)
        self._conn.publish("weather/{}/property/location/setValue".format(self._service_id), serialized, qos=1)

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
    def current_temperature(self) -> Optional[float]:
        """Property 'current_temperature' getter."""
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
    def current_condition(self) -> Optional[CurrentConditionProperty]:
        """Property 'current_condition' getter."""
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
    def daily_forecast(self) -> Optional[DailyForecastProperty]:
        """Property 'daily_forecast' getter."""
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
    def hourly_forecast(self) -> Optional[HourlyForecastProperty]:
        """Property 'hourly_forecast' getter."""
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
    def current_condition_refresh_interval(self) -> Optional[int]:
        """Property 'current_condition_refresh_interval' getter."""
        return self._property_current_condition_refresh_interval

    @current_condition_refresh_interval.setter
    def current_condition_refresh_interval(self, value: int):
        """Serializes and publishes the 'current_condition_refresh_interval' property."""
        if not isinstance(value, int):
            raise ValueError("The 'current_condition_refresh_interval' property must be a int")
        serialized = json.dumps({"seconds": value.seconds})
        self._logger.debug("Setting 'current_condition_refresh_interval' property to %s", serialized)
        self._conn.publish("weather/{}/property/currentConditionRefreshInterval/setValue".format(self._service_id), serialized, qos=1)

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
    def hourly_forecast_refresh_interval(self) -> Optional[int]:
        """Property 'hourly_forecast_refresh_interval' getter."""
        return self._property_hourly_forecast_refresh_interval

    @hourly_forecast_refresh_interval.setter
    def hourly_forecast_refresh_interval(self, value: int):
        """Serializes and publishes the 'hourly_forecast_refresh_interval' property."""
        if not isinstance(value, int):
            raise ValueError("The 'hourly_forecast_refresh_interval' property must be a int")
        serialized = json.dumps({"seconds": value.seconds})
        self._logger.debug("Setting 'hourly_forecast_refresh_interval' property to %s", serialized)
        self._conn.publish("weather/{}/property/hourlyForecastRefreshInterval/setValue".format(self._service_id), serialized, qos=1)

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
    def daily_forecast_refresh_interval(self) -> Optional[int]:
        """Property 'daily_forecast_refresh_interval' getter."""
        return self._property_daily_forecast_refresh_interval

    @daily_forecast_refresh_interval.setter
    def daily_forecast_refresh_interval(self, value: int):
        """Serializes and publishes the 'daily_forecast_refresh_interval' property."""
        if not isinstance(value, int):
            raise ValueError("The 'daily_forecast_refresh_interval' property must be a int")
        serialized = json.dumps({"seconds": value.seconds})
        self._logger.debug("Setting 'daily_forecast_refresh_interval' property to %s", serialized)
        self._conn.publish("weather/{}/property/dailyForecastRefreshInterval/setValue".format(self._service_id), serialized, qos=1)

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

    def _receive_refresh_daily_forecast_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'refresh_daily_forecast' method response.
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

    def _receive_refresh_hourly_forecast_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'refresh_hourly_forecast' method response.
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

    def _receive_refresh_current_conditions_response_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'refresh_current_conditions' method response.
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

    def _receive_location_property_update_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        # Handle 'location' property change.
        if "ContentType" not in properties or properties["ContentType"] != "application/json":
            self._logger.warning("Received 'location' property change with non-JSON content type")
            return
        try:
            prop_obj = LocationProperty.model_validate_json(payload)
            with self._property_location_mutex:
                self._property_location = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_location_version:
                        self._property_location_version = int(ver)

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
            with self._property_current_temperature_mutex:
                self._property_current_temperature = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_current_temperature_version:
                        self._property_current_temperature_version = int(ver)

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
            with self._property_current_condition_mutex:
                self._property_current_condition = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_current_condition_version:
                        self._property_current_condition_version = int(ver)

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
            with self._property_daily_forecast_mutex:
                self._property_daily_forecast = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_daily_forecast_version:
                        self._property_daily_forecast_version = int(ver)

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
            with self._property_hourly_forecast_mutex:
                self._property_hourly_forecast = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_hourly_forecast_version:
                        self._property_hourly_forecast_version = int(ver)

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
            with self._property_current_condition_refresh_interval_mutex:
                self._property_current_condition_refresh_interval = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_current_condition_refresh_interval_version:
                        self._property_current_condition_refresh_interval_version = int(ver)

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
            with self._property_hourly_forecast_refresh_interval_mutex:
                self._property_hourly_forecast_refresh_interval = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_hourly_forecast_refresh_interval_version:
                        self._property_hourly_forecast_refresh_interval_version = int(ver)

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
            with self._property_daily_forecast_refresh_interval_mutex:
                self._property_daily_forecast_refresh_interval = prop_obj
                if ver := properties.get("PropertyVersion", False):
                    if int(ver) > self._property_daily_forecast_refresh_interval_version:
                        self._property_daily_forecast_refresh_interval_version = int(ver)

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
        self._conn.publish(
            "weather/{}/method/refreshDailyForecast".format(self._service_id),
            json_payload,
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/refresh_daily_forecast/response",
        )
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
        self._conn.publish(
            "weather/{}/method/refreshHourlyForecast".format(self._service_id),
            json_payload,
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/refresh_hourly_forecast/response",
        )
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
        self._conn.publish(
            "weather/{}/method/refreshCurrentConditions".format(self._service_id),
            json_payload,
            qos=2,
            retain=False,
            correlation_id=correlation_id,
            response_topic=f"client/{self._conn.client_id}/refresh_current_conditions/response",
        )
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
        self._signal_recv_callbacks_for_current_time.append(handler)

    def location_updated(self, handler: LocationPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_location.append(handler)

    def current_temperature_updated(self, handler: CurrentTemperaturePropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_current_temperature.append(handler)

    def current_condition_updated(self, handler: CurrentConditionPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_current_condition.append(handler)

    def daily_forecast_updated(self, handler: DailyForecastPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_daily_forecast.append(handler)

    def hourly_forecast_updated(self, handler: HourlyForecastPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_hourly_forecast.append(handler)

    def current_condition_refresh_interval_updated(self, handler: CurrentConditionRefreshIntervalPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_current_condition_refresh_interval.append(handler)

    def hourly_forecast_refresh_interval_updated(self, handler: HourlyForecastRefreshIntervalPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_hourly_forecast_refresh_interval.append(handler)

    def daily_forecast_refresh_interval_updated(self, handler: DailyForecastRefreshIntervalPropertyUpdatedCallbackType):
        """Used as a decorator for methods which handle updates to properties."""
        self._property_updated_callbacks_for_daily_forecast_refresh_interval.append(handler)

    def build(self, broker: IBrokerConnection, service_instance_id: str) -> WeatherClient:
        """Builds a new WeatherClient."""
        self._logger.debug("Building WeatherClient for service instance %s", service_instance_id)
        client = WeatherClient(broker, service_instance_id)

        for cb in self._signal_recv_callbacks_for_current_time:
            client.receive_current_time(cb)

        for cb in self._property_updated_callbacks_for_location:
            client.location_changed(cb)

        for cb in self._property_updated_callbacks_for_current_temperature:
            client.current_temperature_changed(cb)

        for cb in self._property_updated_callbacks_for_current_condition:
            client.current_condition_changed(cb)

        for cb in self._property_updated_callbacks_for_daily_forecast:
            client.daily_forecast_changed(cb)

        for cb in self._property_updated_callbacks_for_hourly_forecast:
            client.hourly_forecast_changed(cb)

        for cb in self._property_updated_callbacks_for_current_condition_refresh_interval:
            client.current_condition_refresh_interval_changed(cb)

        for cb in self._property_updated_callbacks_for_hourly_forecast_refresh_interval:
            client.hourly_forecast_refresh_interval_changed(cb)

        for cb in self._property_updated_callbacks_for_daily_forecast_refresh_interval:
            client.daily_forecast_refresh_interval_changed(cb)

        return client


class WeatherClientDiscoverer:

    def __init__(self, connection: IBrokerConnection, builder: Optional[WeatherClientBuilder] = None):
        """Creates a new WeatherClientDiscoverer."""
        self._conn = connection
        self._builder = builder
        self._logger = logging.getLogger("WeatherClientDiscoverer")
        self._logger.setLevel(logging.DEBUG)
        service_discovery_topic = "weather/{}/interface".format("+")
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

    def get_singleton_client(self) -> futures.Future[WeatherClient]:
        """Returns a WeatherClient for the single discovered service.
        Raises an exception if there is not exactly one discovered service.
        """
        fut = futures.Future()
        with self._mutex:
            if len(self._discovered_services) > 0:
                service_instance_id = next(iter(self._discovered_services))
                if self._builder is None:
                    fut.set_result(WeatherClient(self._conn, service_instance_id))
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
                            fut.set_result(WeatherClient(self._conn, service_info.instance))
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
