"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the weather-forecast interface.
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

CurrentTimeSignalCallbackType = Callable[[str], None]
RefreshDailyForecastMethodResponseCallbackType = Callable[[], None]
RefreshHourlyForecastMethodResponseCallbackType = Callable[[], None]
RefreshCurrentConditionsMethodResponseCallbackType = Callable[[], None]

LocationPropertyUpdatedCallbackType = Callable[[stinger_types.LocationProperty], None]
CurrentTemperaturePropertyUpdatedCallbackType = Callable[[float], None]
CurrentConditionPropertyUpdatedCallbackType = Callable[[stinger_types.CurrentConditionProperty], None]
DailyForecastPropertyUpdatedCallbackType = Callable[[stinger_types.DailyForecastProperty], None]
HourlyForecastPropertyUpdatedCallbackType = Callable[[stinger_types.HourlyForecastProperty], None]
CurrentConditionRefreshIntervalPropertyUpdatedCallbackType = Callable[[int], None]
HourlyForecastRefreshIntervalPropertyUpdatedCallbackType = Callable[[int], None]
DailyForecastRefreshIntervalPropertyUpdatedCallbackType = Callable[[int], None]


class weather-forecastClient:

    def __init__(self, connection: BrokerConnection):
        """ Constructor for a `weather-forecastClient` object.
        """
        self._logger = logging.getLogger('weather-forecastClient')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing weather-forecastClient")
        self._client_id = str(uuid4())
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        
        self._pending_method_responses: dict[str, Callable[..., None]] = {}
        
        self._property_location: stinger_types.LocationProperty|None = None
        self._location_prop_subscription_id: int = self._conn.subscribe("weather-forecast/property/location")
        self._changed_value_callbacks_for_location: list[LocationPropertyUpdatedCallbackType] = []
        self._property_current_temperature: float|None = None
        self._current_temperature_prop_subscription_id: int = self._conn.subscribe("weather-forecast/property/current_temperature")
        self._changed_value_callbacks_for_current_temperature: list[CurrentTemperaturePropertyUpdatedCallbackType] = []
        self._property_current_condition: stinger_types.CurrentConditionProperty|None = None
        self._current_condition_prop_subscription_id: int = self._conn.subscribe("weather-forecast/property/current_condition")
        self._changed_value_callbacks_for_current_condition: list[CurrentConditionPropertyUpdatedCallbackType] = []
        self._property_daily_forecast: stinger_types.DailyForecastProperty|None = None
        self._daily_forecast_prop_subscription_id: int = self._conn.subscribe("weather-forecast/property/daily_forecast")
        self._changed_value_callbacks_for_daily_forecast: list[DailyForecastPropertyUpdatedCallbackType] = []
        self._property_hourly_forecast: stinger_types.HourlyForecastProperty|None = None
        self._hourly_forecast_prop_subscription_id: int = self._conn.subscribe("weather-forecast/property/hourly_forecast")
        self._changed_value_callbacks_for_hourly_forecast: list[HourlyForecastPropertyUpdatedCallbackType] = []
        self._property_current_condition_refresh_interval: int|None = None
        self._current_condition_refresh_interval_prop_subscription_id: int = self._conn.subscribe("weather-forecast/property/current_condition_refresh_interval")
        self._changed_value_callbacks_for_current_condition_refresh_interval: list[CurrentConditionRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_hourly_forecast_refresh_interval: int|None = None
        self._hourly_forecast_refresh_interval_prop_subscription_id: int = self._conn.subscribe("weather-forecast/property/hourly_forecast_refresh_interval")
        self._changed_value_callbacks_for_hourly_forecast_refresh_interval: list[HourlyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_daily_forecast_refresh_interval: int|None = None
        self._daily_forecast_refresh_interval_prop_subscription_id: int = self._conn.subscribe("weather-forecast/property/daily_forecast_refresh_interval")
        self._changed_value_callbacks_for_daily_forecast_refresh_interval: list[DailyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        self._signal_recv_callbacks_for_current_time: list[CurrentTimeSignalCallbackType] = []
        self._refresh_daily_forecast_method_call_subscription_id: int = self._conn.subscribe(f"client/{self._client_id}/weather-forecast/method/refresh_daily_forecast/response")
        self._refresh_hourly_forecast_method_call_subscription_id: int = self._conn.subscribe(f"client/{self._client_id}/weather-forecast/method/refresh_hourly_forecast/response")
        self._refresh_current_conditions_method_call_subscription_id: int = self._conn.subscribe(f"client/{self._client_id}/weather-forecast/method/refresh_current_conditions/response")
        

    @property
    def location(self) -> stinger_types.LocationProperty | None:
        """ Property 'location' getter.
        """
        return self._property_location
    
    @location.setter
    def location(self, value: stinger_types.LocationProperty):
        """ Serializes and publishes the 'location' property.
        """
        if not isinstance(value, stinger_types.LocationProperty):
            raise ValueError("The 'location' property must be a stinger_types.LocationProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'location' property to %s", serialized)
        self._conn.publish("weather-forecast/property/location/set_value", serialized, qos=1)
    
    def location_changed(self, handler: LocationPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'location' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_location.append(handler)
        if call_immediately and self._property_location is not None:
            handler(self._property_location)
        return handler

    @property
    def current_temperature(self) -> float | None:
        """ Property 'current_temperature' getter.
        """
        return self._property_current_temperature
    
    def current_temperature_changed(self, handler: CurrentTemperaturePropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'current_temperature' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_current_temperature.append(handler)
        if call_immediately and self._property_current_temperature is not None:
            handler(self._property_current_temperature)
        return handler

    @property
    def current_condition(self) -> stinger_types.CurrentConditionProperty | None:
        """ Property 'current_condition' getter.
        """
        return self._property_current_condition
    
    def current_condition_changed(self, handler: CurrentConditionPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'current_condition' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_current_condition.append(handler)
        if call_immediately and self._property_current_condition is not None:
            handler(self._property_current_condition)
        return handler

    @property
    def daily_forecast(self) -> stinger_types.DailyForecastProperty | None:
        """ Property 'daily_forecast' getter.
        """
        return self._property_daily_forecast
    
    @daily_forecast.setter
    def daily_forecast(self, value: stinger_types.DailyForecastProperty):
        """ Serializes and publishes the 'daily_forecast' property.
        """
        if not isinstance(value, stinger_types.DailyForecastProperty):
            raise ValueError("The 'daily_forecast' property must be a stinger_types.DailyForecastProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'daily_forecast' property to %s", serialized)
        self._conn.publish("weather-forecast/property/daily_forecast/set_value", serialized, qos=1)
    
    def daily_forecast_changed(self, handler: DailyForecastPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'daily_forecast' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_daily_forecast.append(handler)
        if call_immediately and self._property_daily_forecast is not None:
            handler(self._property_daily_forecast)
        return handler

    @property
    def hourly_forecast(self) -> stinger_types.HourlyForecastProperty | None:
        """ Property 'hourly_forecast' getter.
        """
        return self._property_hourly_forecast
    
    @hourly_forecast.setter
    def hourly_forecast(self, value: stinger_types.HourlyForecastProperty):
        """ Serializes and publishes the 'hourly_forecast' property.
        """
        if not isinstance(value, stinger_types.HourlyForecastProperty):
            raise ValueError("The 'hourly_forecast' property must be a stinger_types.HourlyForecastProperty")
        serialized = value.model_dump_json(exclude_none=True)
        self._logger.debug("Setting 'hourly_forecast' property to %s", serialized)
        self._conn.publish("weather-forecast/property/hourly_forecast/set_value", serialized, qos=1)
    
    def hourly_forecast_changed(self, handler: HourlyForecastPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'hourly_forecast' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_hourly_forecast.append(handler)
        if call_immediately and self._property_hourly_forecast is not None:
            handler(self._property_hourly_forecast)
        return handler

    @property
    def current_condition_refresh_interval(self) -> int | None:
        """ Property 'current_condition_refresh_interval' getter.
        """
        return self._property_current_condition_refresh_interval
    
    @current_condition_refresh_interval.setter
    def current_condition_refresh_interval(self, value: int):
        """ Serializes and publishes the 'current_condition_refresh_interval' property.
        """
        if not isinstance(value, int):
            raise ValueError("The 'current_condition_refresh_interval' property must be a int")
        serialized = json.dumps({ "seconds": value.seconds })
        self._logger.debug("Setting 'current_condition_refresh_interval' property to %s", serialized)
        self._conn.publish("weather-forecast/property/current_condition_refresh_interval/set_value", serialized, qos=1)
    
    def current_condition_refresh_interval_changed(self, handler: CurrentConditionRefreshIntervalPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'current_condition_refresh_interval' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_current_condition_refresh_interval.append(handler)
        if call_immediately and self._property_current_condition_refresh_interval is not None:
            handler(self._property_current_condition_refresh_interval)
        return handler

    @property
    def hourly_forecast_refresh_interval(self) -> int | None:
        """ Property 'hourly_forecast_refresh_interval' getter.
        """
        return self._property_hourly_forecast_refresh_interval
    
    @hourly_forecast_refresh_interval.setter
    def hourly_forecast_refresh_interval(self, value: int):
        """ Serializes and publishes the 'hourly_forecast_refresh_interval' property.
        """
        if not isinstance(value, int):
            raise ValueError("The 'hourly_forecast_refresh_interval' property must be a int")
        serialized = json.dumps({ "seconds": value.seconds })
        self._logger.debug("Setting 'hourly_forecast_refresh_interval' property to %s", serialized)
        self._conn.publish("weather-forecast/property/hourly_forecast_refresh_interval/set_value", serialized, qos=1)
    
    def hourly_forecast_refresh_interval_changed(self, handler: HourlyForecastRefreshIntervalPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'hourly_forecast_refresh_interval' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_hourly_forecast_refresh_interval.append(handler)
        if call_immediately and self._property_hourly_forecast_refresh_interval is not None:
            handler(self._property_hourly_forecast_refresh_interval)
        return handler

    @property
    def daily_forecast_refresh_interval(self) -> int | None:
        """ Property 'daily_forecast_refresh_interval' getter.
        """
        return self._property_daily_forecast_refresh_interval
    
    @daily_forecast_refresh_interval.setter
    def daily_forecast_refresh_interval(self, value: int):
        """ Serializes and publishes the 'daily_forecast_refresh_interval' property.
        """
        if not isinstance(value, int):
            raise ValueError("The 'daily_forecast_refresh_interval' property must be a int")
        serialized = json.dumps({ "seconds": value.seconds })
        self._logger.debug("Setting 'daily_forecast_refresh_interval' property to %s", serialized)
        self._conn.publish("weather-forecast/property/daily_forecast_refresh_interval/set_value", serialized, qos=1)
    
    def daily_forecast_refresh_interval_changed(self, handler: DailyForecastRefreshIntervalPropertyUpdatedCallbackType, call_immediately: bool=False):
        """ Sets a callback to be called when the 'daily_forecast_refresh_interval' property changes.
        Can be used as a decorator.
        """
        self._changed_value_callbacks_for_daily_forecast_refresh_interval.append(handler)
        if call_immediately and self._property_daily_forecast_refresh_interval is not None:
            handler(self._property_daily_forecast_refresh_interval)
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
        # Handle 'current_time' signal.
        if self._conn.is_topic_sub(topic, "weather-forecast/signal/current_time"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'current_time' signal with non-JSON content type")
                return
            allowed_args = ["current_time", ]
            kwargs = self._filter_for_args(json.loads(payload), allowed_args)
            kwargs["current_time"] = str(kwargs["current_time"])
            
            self._do_callbacks_for(self._signal_recv_callbacks_for_current_time, **kwargs)
        
        # Handle 'refresh_daily_forecast' method response.
        if self._conn.is_topic_sub(topic, f"client/{self._client_id}/weather-forecast/method/refresh_daily_forecast/response"):
            result_code = MethodResultCode.SUCCESS
            if "UserProperty" in properties:
                user_properties = properties["UserProperty"]
                if "DebugInfo" in user_properties:
                    self._logger.info("Received Debug Info: %s", user_properties["DebugInfo"])
                if "ReturnValue" in user_properties:
                    result_code = MethodResultCode(int(user_properties["ReturnValue"]))
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
        
        # Handle 'refresh_hourly_forecast' method response.
        if self._conn.is_topic_sub(topic, f"client/{self._client_id}/weather-forecast/method/refresh_hourly_forecast/response"):
            result_code = MethodResultCode.SUCCESS
            if "UserProperty" in properties:
                user_properties = properties["UserProperty"]
                if "DebugInfo" in user_properties:
                    self._logger.info("Received Debug Info: %s", user_properties["DebugInfo"])
                if "ReturnValue" in user_properties:
                    result_code = MethodResultCode(int(user_properties["ReturnValue"]))
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
        
        # Handle 'refresh_current_conditions' method response.
        if self._conn.is_topic_sub(topic, f"client/{self._client_id}/weather-forecast/method/refresh_current_conditions/response"):
            result_code = MethodResultCode.SUCCESS
            if "UserProperty" in properties:
                user_properties = properties["UserProperty"]
                if "DebugInfo" in user_properties:
                    self._logger.info("Received Debug Info: %s", user_properties["DebugInfo"])
                if "ReturnValue" in user_properties:
                    result_code = MethodResultCode(int(user_properties["ReturnValue"]))
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
        
        # Handle 'location' property change.
        if self._conn.is_topic_sub(topic, "weather-forecast/property/location"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'location' property change with non-JSON content type")
                return
            try:
                prop_value = stinger_types.LocationProperty.model_validate_json(payload)
                self._property_location = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_location, value=self._property_location)
            except Exception as e:
                self._logger.error("Error processing 'location' property change: %s", e)
        
        # Handle 'current_temperature' property change.
        elif self._conn.is_topic_sub(topic, "weather-forecast/property/current_temperature"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'current_temperature' property change with non-JSON content type")
                return
            try:
                payload_obj = json.loads(payload)
                prop_value = float(payload_obj["temperature_f"])
                self._property_current_temperature = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_current_temperature, value=self._property_current_temperature)
            except Exception as e:
                self._logger.error("Error processing 'current_temperature' property change: %s", e)
        
        # Handle 'current_condition' property change.
        elif self._conn.is_topic_sub(topic, "weather-forecast/property/current_condition"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'current_condition' property change with non-JSON content type")
                return
            try:
                prop_value = stinger_types.CurrentConditionProperty.model_validate_json(payload)
                self._property_current_condition = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_current_condition, value=self._property_current_condition)
            except Exception as e:
                self._logger.error("Error processing 'current_condition' property change: %s", e)
        
        # Handle 'daily_forecast' property change.
        elif self._conn.is_topic_sub(topic, "weather-forecast/property/daily_forecast"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'daily_forecast' property change with non-JSON content type")
                return
            try:
                prop_value = stinger_types.DailyForecastProperty.model_validate_json(payload)
                self._property_daily_forecast = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_daily_forecast, value=self._property_daily_forecast)
            except Exception as e:
                self._logger.error("Error processing 'daily_forecast' property change: %s", e)
        
        # Handle 'hourly_forecast' property change.
        elif self._conn.is_topic_sub(topic, "weather-forecast/property/hourly_forecast"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'hourly_forecast' property change with non-JSON content type")
                return
            try:
                prop_value = stinger_types.HourlyForecastProperty.model_validate_json(payload)
                self._property_hourly_forecast = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_hourly_forecast, value=self._property_hourly_forecast)
            except Exception as e:
                self._logger.error("Error processing 'hourly_forecast' property change: %s", e)
        
        # Handle 'current_condition_refresh_interval' property change.
        elif self._conn.is_topic_sub(topic, "weather-forecast/property/current_condition_refresh_interval"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'current_condition_refresh_interval' property change with non-JSON content type")
                return
            try:
                payload_obj = json.loads(payload)
                prop_value = int(payload_obj["seconds"])
                self._property_current_condition_refresh_interval = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_current_condition_refresh_interval, value=self._property_current_condition_refresh_interval)
            except Exception as e:
                self._logger.error("Error processing 'current_condition_refresh_interval' property change: %s", e)
        
        # Handle 'hourly_forecast_refresh_interval' property change.
        elif self._conn.is_topic_sub(topic, "weather-forecast/property/hourly_forecast_refresh_interval"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'hourly_forecast_refresh_interval' property change with non-JSON content type")
                return
            try:
                payload_obj = json.loads(payload)
                prop_value = int(payload_obj["seconds"])
                self._property_hourly_forecast_refresh_interval = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_hourly_forecast_refresh_interval, value=self._property_hourly_forecast_refresh_interval)
            except Exception as e:
                self._logger.error("Error processing 'hourly_forecast_refresh_interval' property change: %s", e)
        
        # Handle 'daily_forecast_refresh_interval' property change.
        elif self._conn.is_topic_sub(topic, "weather-forecast/property/daily_forecast_refresh_interval"):
            if 'ContentType' not in properties or properties['ContentType'] != 'application/json':
                self._logger.warning("Received 'daily_forecast_refresh_interval' property change with non-JSON content type")
                return
            try:
                payload_obj = json.loads(payload)
                prop_value = int(payload_obj["seconds"])
                self._property_daily_forecast_refresh_interval = prop_value
                self._do_callbacks_for(self._changed_value_callbacks_for_daily_forecast_refresh_interval, value=self._property_daily_forecast_refresh_interval)
            except Exception as e:
                self._logger.error("Error processing 'daily_forecast_refresh_interval' property change: %s", e)
        

    
    def receive_current_time(self, handler: CurrentTimeSignalCallbackType):
        """ Used as a decorator for methods which handle particular signals.
        """
        self._signal_recv_callbacks_for_current_time.append(handler)
        if len(self._signal_recv_callbacks_for_current_time) == 1:
            self._conn.subscribe("weather-forecast/signal/current_time")
        return handler
    

    
    def refresh_daily_forecast(self, ) -> futures.Future:
        """ Calling this initiates a `refresh_daily_forecast` IPC method call.
        """
        
        fut = futures.Future() # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_refresh_daily_forecast_response, fut)
        payload = {
        }
        self._conn.publish("weather-forecast/method/refresh_daily_forecast", json.dumps(payload), qos=2, retain=False,
                           correlation_id=correlation_id, response_topic=f"client/{self._client_id}/weather-forecast/method/refresh_daily_forecast/response")
        return fut

    def _handle_refresh_daily_forecast_response(self, fut: futures.Future, response_json: Dict[str, Any], return_value: MethodResultCode):
        """ This called with the response to a `refresh_daily_forecast` IPC method call.
        """
        self._logger.debug("Handling refresh_daily_forecast response message %s", fut)
        try:
            if return_value != MethodResultCode.SUCCESS.value:
                raise stinger_exception_factory(return_value, response_json['debugResultMessage'] if 'debugResultMessage' in response_json else None)
            
            fut.set_result(None)
            
        except Exception as e:
            self._logger.info("Exception while handling refresh_daily_forecast", exc_info=e)
            fut.set_exception(e)
        if not fut.done():
            fut.set_exception(Exception("No return value set"))
    
    def refresh_hourly_forecast(self, ) -> futures.Future:
        """ Calling this initiates a `refresh_hourly_forecast` IPC method call.
        """
        
        fut = futures.Future() # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_refresh_hourly_forecast_response, fut)
        payload = {
        }
        self._conn.publish("weather-forecast/method/refresh_hourly_forecast", json.dumps(payload), qos=2, retain=False,
                           correlation_id=correlation_id, response_topic=f"client/{self._client_id}/weather-forecast/method/refresh_hourly_forecast/response")
        return fut

    def _handle_refresh_hourly_forecast_response(self, fut: futures.Future, response_json: Dict[str, Any], return_value: MethodResultCode):
        """ This called with the response to a `refresh_hourly_forecast` IPC method call.
        """
        self._logger.debug("Handling refresh_hourly_forecast response message %s", fut)
        try:
            if return_value != MethodResultCode.SUCCESS.value:
                raise stinger_exception_factory(return_value, response_json['debugResultMessage'] if 'debugResultMessage' in response_json else None)
            
            fut.set_result(None)
            
        except Exception as e:
            self._logger.info("Exception while handling refresh_hourly_forecast", exc_info=e)
            fut.set_exception(e)
        if not fut.done():
            fut.set_exception(Exception("No return value set"))
    
    def refresh_current_conditions(self, ) -> futures.Future:
        """ Calling this initiates a `refresh_current_conditions` IPC method call.
        """
        
        fut = futures.Future() # type: futures.Future
        correlation_id = str(uuid4())
        self._pending_method_responses[correlation_id] = partial(self._handle_refresh_current_conditions_response, fut)
        payload = {
        }
        self._conn.publish("weather-forecast/method/refresh_current_conditions", json.dumps(payload), qos=2, retain=False,
                           correlation_id=correlation_id, response_topic=f"client/{self._client_id}/weather-forecast/method/refresh_current_conditions/response")
        return fut

    def _handle_refresh_current_conditions_response(self, fut: futures.Future, response_json: Dict[str, Any], return_value: MethodResultCode):
        """ This called with the response to a `refresh_current_conditions` IPC method call.
        """
        self._logger.debug("Handling refresh_current_conditions response message %s", fut)
        try:
            if return_value != MethodResultCode.SUCCESS.value:
                raise stinger_exception_factory(return_value, response_json['debugResultMessage'] if 'debugResultMessage' in response_json else None)
            
            fut.set_result(None)
            
        except Exception as e:
            self._logger.info("Exception while handling refresh_current_conditions", exc_info=e)
            fut.set_exception(e)
        if not fut.done():
            fut.set_exception(Exception("No return value set"))
    

class weather-forecastClientBuilder:

    def __init__(self, broker: BrokerConnection):
        """ Creates a new weather-forecastClientBuilder.
        """
        self._conn = broker
        self._logger = logging.getLogger('weather-forecastClientBuilder')
        self._signal_recv_callbacks_for_current_time = [] # type: List[CurrentTimeSignalCallbackType]
        self._property_updated_callbacks_for_location: list[LocationPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_current_temperature: list[CurrentTemperaturePropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_current_condition: list[CurrentConditionPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_daily_forecast: list[DailyForecastPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_hourly_forecast: list[HourlyForecastPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_current_condition_refresh_interval: list[CurrentConditionRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_hourly_forecast_refresh_interval: list[HourlyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        self._property_updated_callbacks_for_daily_forecast_refresh_interval: list[DailyForecastRefreshIntervalPropertyUpdatedCallbackType] = []
        
    def receive_current_time(self, handler):
        """ Used as a decorator for methods which handle particular signals.
        """
        self._signal_recv_callbacks_for_current_time.append(handler)
    

    
    def location_updated(self, handler: LocationPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_location.append(handler)
    
    def current_temperature_updated(self, handler: CurrentTemperaturePropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_current_temperature.append(handler)
    
    def current_condition_updated(self, handler: CurrentConditionPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_current_condition.append(handler)
    
    def daily_forecast_updated(self, handler: DailyForecastPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_daily_forecast.append(handler)
    
    def hourly_forecast_updated(self, handler: HourlyForecastPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_hourly_forecast.append(handler)
    
    def current_condition_refresh_interval_updated(self, handler: CurrentConditionRefreshIntervalPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_current_condition_refresh_interval.append(handler)
    
    def hourly_forecast_refresh_interval_updated(self, handler: HourlyForecastRefreshIntervalPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_hourly_forecast_refresh_interval.append(handler)
    
    def daily_forecast_refresh_interval_updated(self, handler: DailyForecastRefreshIntervalPropertyUpdatedCallbackType):
        """ Used as a decorator for methods which handle updates to properties.
        """
        self._property_updated_callbacks_for_daily_forecast_refresh_interval.append(handler)
    

    def build(self) -> weather-forecastClient:
        """ Builds a new weather-forecastClient.
        """
        self._logger.debug("Building weather-forecastClient")
        client = weather-forecastClient(self._conn)
        
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


if __name__ == '__main__':
    import signal

    from connection import DefaultConnection
    conn = DefaultConnection('localhost', 1883)
    client_builder = weather-forecastClientBuilder(conn)
    
    @client_builder.receive_current_time
    def print_current_time_receipt(current_time: str):
        """
        @param current_time str 
        """
        print(f"Got a 'current_time' signal: current_time={ current_time } ")
    
    
    @client_builder.location_updated
    def print_new_location_value(value: stinger_types.LocationProperty):
        """
        """
        print(f"Property 'location' has been updated to: {value}")
    
    @client_builder.current_temperature_updated
    def print_new_current_temperature_value(value: float):
        """
        """
        print(f"Property 'current_temperature' has been updated to: {value}")
    
    @client_builder.current_condition_updated
    def print_new_current_condition_value(value: stinger_types.CurrentConditionProperty):
        """
        """
        print(f"Property 'current_condition' has been updated to: {value}")
    
    @client_builder.daily_forecast_updated
    def print_new_daily_forecast_value(value: stinger_types.DailyForecastProperty):
        """
        """
        print(f"Property 'daily_forecast' has been updated to: {value}")
    
    @client_builder.hourly_forecast_updated
    def print_new_hourly_forecast_value(value: stinger_types.HourlyForecastProperty):
        """
        """
        print(f"Property 'hourly_forecast' has been updated to: {value}")
    
    @client_builder.current_condition_refresh_interval_updated
    def print_new_current_condition_refresh_interval_value(value: int):
        """
        """
        print(f"Property 'current_condition_refresh_interval' has been updated to: {value}")
    
    @client_builder.hourly_forecast_refresh_interval_updated
    def print_new_hourly_forecast_refresh_interval_value(value: int):
        """
        """
        print(f"Property 'hourly_forecast_refresh_interval' has been updated to: {value}")
    
    @client_builder.daily_forecast_refresh_interval_updated
    def print_new_daily_forecast_refresh_interval_value(value: int):
        """
        """
        print(f"Property 'daily_forecast_refresh_interval' has been updated to: {value}")
    

    client = client_builder.build()
    
    print("Making call to 'refresh_daily_forecast'")
    future = client.refresh_daily_forecast()
    try:
        print(f"RESULT:  {future.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'refresh_daily_forecast' call")
    
    print("Making call to 'refresh_hourly_forecast'")
    future = client.refresh_hourly_forecast()
    try:
        print(f"RESULT:  {future.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'refresh_hourly_forecast' call")
    
    print("Making call to 'refresh_current_conditions'")
    future = client.refresh_current_conditions()
    try:
        print(f"RESULT:  {future.result(5)}")
    except futures.TimeoutError:
        print(f"Timed out waiting for response to 'refresh_current_conditions' call")
    
    

    print("Ctrl-C will stop the program.")
    signal.pause()