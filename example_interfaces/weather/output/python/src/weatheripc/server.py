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
from stinger_python_utils.message_creator import MessageCreator
from stinger_python_utils.return_codes import *
from .interface_types import *



from .property import WeatherInitialPropertyValues



T = TypeVar('T')

@dataclass
class PropertyControls(Generic[T]):
    """
    Controls for a server property.  Generic[T] must be a single value or a pydantic BaseModel for multi-argument properties.
    """
    value: T
    mutex = threading.RLock()
    version: int = -1
    callbacks: List[Callable[[T], None]] = field(default_factory=list)

    def get_value(self) -> T:
        with self.mutex:
            return self.value

    def set_value(self, new_value: T) -> T:
        with self.mutex:
            self.value = new_value
            return self.value
    
 

class WeatherServer:

    def __init__(self, connection: IBrokerConnection, instance_id: str, initial_property_values: WeatherInitialPropertyValues):
        self._logger = logging.getLogger(f'WeatherServer:{instance_id}')
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing WeatherServer instance %s", instance_id)
        self._instance_id = instance_id
        self._service_advert_topic = "weather/{}/interface".format(self._instance_id)
        self._re_advertise_server_interval_seconds = 120 # every two minutes
        self._conn = connection
        self._running = True
        self._conn.add_message_callback(self._receive_message)
        
        self._property_location: PropertyControls[LocationProperty] = PropertyControls(value=initial_property_values.location, version=initial_property_values.location_version)
        self._conn.subscribe("weather/{}/property/location/setValue".format(self._instance_id), self._receive_location_update_request_message)
        
        self._property_current_temperature: PropertyControls[float] = PropertyControls(value=initial_property_values.current_temperature, version=initial_property_values.current_temperature_version)
        
        self._property_current_condition: PropertyControls[CurrentConditionProperty] = PropertyControls(value=initial_property_values.current_condition, version=initial_property_values.current_condition_version)
        
        self._property_daily_forecast: PropertyControls[DailyForecastProperty] = PropertyControls(value=initial_property_values.daily_forecast, version=initial_property_values.daily_forecast_version)
        
        self._property_hourly_forecast: PropertyControls[HourlyForecastProperty] = PropertyControls(value=initial_property_values.hourly_forecast, version=initial_property_values.hourly_forecast_version)
        
        self._property_current_condition_refresh_interval: PropertyControls[int] = PropertyControls(value=initial_property_values.current_condition_refresh_interval, version=initial_property_values.current_condition_refresh_interval_version)
        self._conn.subscribe("weather/{}/property/currentConditionRefreshInterval/setValue".format(self._instance_id), self._receive_current_condition_refresh_interval_update_request_message)
        
        self._property_hourly_forecast_refresh_interval: PropertyControls[int] = PropertyControls(value=initial_property_values.hourly_forecast_refresh_interval, version=initial_property_values.hourly_forecast_refresh_interval_version)
        self._conn.subscribe("weather/{}/property/hourlyForecastRefreshInterval/setValue".format(self._instance_id), self._receive_hourly_forecast_refresh_interval_update_request_message)
        
        self._property_daily_forecast_refresh_interval: PropertyControls[int] = PropertyControls(value=initial_property_values.daily_forecast_refresh_interval, version=initial_property_values.daily_forecast_refresh_interval_version)
        self._conn.subscribe("weather/{}/property/dailyForecastRefreshInterval/setValue".format(self._instance_id), self._receive_daily_forecast_refresh_interval_update_request_message)
        
        self._conn.subscribe("weather/{}/method/refreshDailyForecast".format(self._instance_id), self._process_refresh_daily_forecast_call)
        self._method_refresh_daily_forecast_handler = None # type: Optional[Callable[[], None]]
        
        self._conn.subscribe("weather/{}/method/refreshHourlyForecast".format(self._instance_id), self._process_refresh_hourly_forecast_call)
        self._method_refresh_hourly_forecast_handler = None # type: Optional[Callable[[], None]]
        
        self._conn.subscribe("weather/{}/method/refreshCurrentConditions".format(self._instance_id), self._process_refresh_current_conditions_call)
        self._method_refresh_current_conditions_handler = None # type: Optional[Callable[[], None]]
        
        self._publish_all_properties()
        self._logger.debug("Starting interface advertisement thread")
        self._advertise_thread = threading.Thread(target=self._loop_publishing_interface_info, daemon=True)
        self._advertise_thread.start()

    def __del__(self):
        self.shutdown()

    def shutdown(self, timeout: float=5.0):
        """Gracefully shutdown the server and stop the advertisement thread."""
        if not self._running:
            return
        self._running = False
        self._conn.unpublish_retained(self._service_advert_topic)
        if hasattr(self, '_advertise_thread') and self._advertise_thread.is_alive():
            self._advertise_thread.join(timeout=timeout)

    @property
    def instance_id(self) -> str:
        """ The instance ID of this server instance. """
        return self._instance_id

    def _loop_publishing_interface_info(self):
        """ We have a discovery topic separate from the MQTT client discovery topic.
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
        """ Publishes the interface info message to the interface info topic with an expiry interval. """
        data = InterfaceInfo(
            instance=self._instance_id,
            connection_topic=(self._conn.online_topic or ""),
        timestamp=datetime.now(UTC).isoformat()
        )
        expiry = int(self._re_advertise_server_interval_seconds * 1.2) # slightly longer than the re-advertise interval
        topic = self._service_advert_topic
        self._logger.debug("Publishing interface info to %s: %s", topic, data.model_dump_json(by_alias=True))
        msg = MessageCreator.status_message(topic, data, expiry)
        self._conn.publish(msg)

    
    def publish_location_value(self, *_, **__):
        """ Publishes the current value of the 'location' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.
        
        """
        with self._property_location.mutex:
            self._property_location.version += 1
            location_prop_obj = self._property_location.get_value()
            state_msg = MessageCreator.property_state_message("weather/{}/property/location/value".format(self._instance_id), location_prop_obj, self._property_location.version)
            self._conn.publish(state_msg)
    def publish_current_temperature_value(self, *_, **__):
        """ Publishes the current value of the 'current_temperature' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.
        
        """
        with self._property_current_temperature.mutex:
            self._property_current_temperature.version += 1
            current_temperature_prop_obj = CurrentTemperatureProperty(temperature_f=self._property_current_temperature.get_value())
            state_msg = MessageCreator.property_state_message("weather/{}/property/currentTemperature/value".format(self._instance_id), current_temperature_prop_obj, self._property_current_temperature.version)
            self._conn.publish(state_msg)
    def publish_current_condition_value(self, *_, **__):
        """ Publishes the current value of the 'current_condition' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.
        
        """
        with self._property_current_condition.mutex:
            self._property_current_condition.version += 1
            current_condition_prop_obj = self._property_current_condition.get_value()
            state_msg = MessageCreator.property_state_message("weather/{}/property/currentCondition/value".format(self._instance_id), current_condition_prop_obj, self._property_current_condition.version)
            self._conn.publish(state_msg)
    def publish_daily_forecast_value(self, *_, **__):
        """ Publishes the current value of the 'daily_forecast' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.
        
        """
        with self._property_daily_forecast.mutex:
            self._property_daily_forecast.version += 1
            daily_forecast_prop_obj = self._property_daily_forecast.get_value()
            state_msg = MessageCreator.property_state_message("weather/{}/property/dailyForecast/value".format(self._instance_id), daily_forecast_prop_obj, self._property_daily_forecast.version)
            self._conn.publish(state_msg)
    def publish_hourly_forecast_value(self, *_, **__):
        """ Publishes the current value of the 'hourly_forecast' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.
        
        """
        with self._property_hourly_forecast.mutex:
            self._property_hourly_forecast.version += 1
            hourly_forecast_prop_obj = self._property_hourly_forecast.get_value()
            state_msg = MessageCreator.property_state_message("weather/{}/property/hourlyForecast/value".format(self._instance_id), hourly_forecast_prop_obj, self._property_hourly_forecast.version)
            self._conn.publish(state_msg)
    def publish_current_condition_refresh_interval_value(self, *_, **__):
        """ Publishes the current value of the 'current_condition_refresh_interval' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.
        
        """
        with self._property_current_condition_refresh_interval.mutex:
            self._property_current_condition_refresh_interval.version += 1
            current_condition_refresh_interval_prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())
            state_msg = MessageCreator.property_state_message("weather/{}/property/currentConditionRefreshInterval/value".format(self._instance_id), current_condition_refresh_interval_prop_obj, self._property_current_condition_refresh_interval.version)
            self._conn.publish(state_msg)
    def publish_hourly_forecast_refresh_interval_value(self, *_, **__):
        """ Publishes the current value of the 'hourly_forecast_refresh_interval' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.
        
        """
        with self._property_hourly_forecast_refresh_interval.mutex:
            self._property_hourly_forecast_refresh_interval.version += 1
            hourly_forecast_refresh_interval_prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())
            state_msg = MessageCreator.property_state_message("weather/{}/property/hourlyForecastRefreshInterval/value".format(self._instance_id), hourly_forecast_refresh_interval_prop_obj, self._property_hourly_forecast_refresh_interval.version)
            self._conn.publish(state_msg)
    def publish_daily_forecast_refresh_interval_value(self, *_, **__):
        """ Publishes the current value of the 'daily_forecast_refresh_interval' property.

        Accepts unused args and kwargs to make this a usable callback for application code.
        
        Since we won't automatically publish a property value unless it changes, this method is
        useful for unit tests where we want to force re-publishing the property value to check the
        published value in the unit test.
        
        """
        with self._property_daily_forecast_refresh_interval.mutex:
            self._property_daily_forecast_refresh_interval.version += 1
            daily_forecast_refresh_interval_prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())
            state_msg = MessageCreator.property_state_message("weather/{}/property/dailyForecastRefreshInterval/value".format(self._instance_id), daily_forecast_refresh_interval_prop_obj, self._property_daily_forecast_refresh_interval.version)
            self._conn.publish(state_msg)

    def _publish_all_properties(self):
        """ Publishes the current value of all properties.
        """
        self.publish_location_value()
        self.publish_current_temperature_value()
        self.publish_current_condition_value()
        self.publish_daily_forecast_value()
        self.publish_hourly_forecast_value()
        self.publish_current_condition_refresh_interval_value()
        self.publish_hourly_forecast_refresh_interval_value()
        self.publish_daily_forecast_refresh_interval_value()

    
    
    def _receive_location_update_request_message(self, message: Message):
        """ When the MQTT client receives a message to the `weather/{}/property/location/setValue` topic
        in order to update the `location` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict() # type: Dict[str, str]
        prop_version_str = user_properties.get('PropertyVersion', "-1") # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data # type: Optional[bytes]
        response_topic = message.response_topic # type: Optional[str]

        try:
            if int(prop_version) != int(self._property_location.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_location.version}' of the 'location' property")

            recv_prop_obj = LocationProperty.model_validate_json(message.payload)

            prop_value = recv_prop_obj # type: LocationProperty
            with self._property_location.mutex:
                self._property_location.version += 1
                self._property_location.set_value(prop_value)
                
                current_prop_obj = self._property_location.get_value() # type: LocationProperty
                
                state_msg = MessageCreator.property_state_message("weather/{}/property/location/value".format(self._instance_id), current_prop_obj, self._property_location.version)
                self._conn.publish(state_msg)
            
                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = MessageCreator.property_response_message(response_topic, current_prop_obj, str(self._property_location.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            
            for location_callback in self._property_location.callbacks:
                
                location_callback(current_prop_obj)
                
            
        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = self._property_location.get_value()
                if isinstance(e, (json.JSONDecodeError, ValidationError)):
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                elif isinstance(e, StingerMethodException):
                    return_code = e.return_code
                else:
                    return_code = MethodReturnCode.SERVER_ERROR
                prop_resp_msg = MessageCreator.property_response_message(response_topic, prop_obj, str(self._property_location.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)
    
    
    
    
    
    
    
    
    
    
    
    def _receive_current_condition_refresh_interval_update_request_message(self, message: Message):
        """ When the MQTT client receives a message to the `weather/{}/property/currentConditionRefreshInterval/setValue` topic
        in order to update the `current_condition_refresh_interval` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict() # type: Dict[str, str]
        prop_version_str = user_properties.get('PropertyVersion', "-1") # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data # type: Optional[bytes]
        response_topic = message.response_topic # type: Optional[str]

        try:
            if int(prop_version) != int(self._property_current_condition_refresh_interval.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_current_condition_refresh_interval.version}' of the 'current_condition_refresh_interval' property")

            recv_prop_obj = CurrentConditionRefreshIntervalProperty.model_validate_json(message.payload)

            prop_value = recv_prop_obj.seconds
            with self._property_current_condition_refresh_interval.mutex:
                self._property_current_condition_refresh_interval.version += 1
                self._property_current_condition_refresh_interval.set_value(prop_value)
                
                current_prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())
                
                state_msg = MessageCreator.property_state_message("weather/{}/property/currentConditionRefreshInterval/value".format(self._instance_id), current_prop_obj, self._property_current_condition_refresh_interval.version)
                self._conn.publish(state_msg)
            
                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = MessageCreator.property_response_message(response_topic, current_prop_obj, str(self._property_current_condition_refresh_interval.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            
            for current_condition_refresh_interval_callback in self._property_current_condition_refresh_interval.callbacks:
                
                current_condition_refresh_interval_callback(current_prop_obj.seconds)
                
            
        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())
                if isinstance(e, (json.JSONDecodeError, ValidationError)):
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                elif isinstance(e, StingerMethodException):
                    return_code = e.return_code
                else:
                    return_code = MethodReturnCode.SERVER_ERROR
                prop_resp_msg = MessageCreator.property_response_message(response_topic, prop_obj, str(self._property_current_condition_refresh_interval.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)
    
    
    
    def _receive_hourly_forecast_refresh_interval_update_request_message(self, message: Message):
        """ When the MQTT client receives a message to the `weather/{}/property/hourlyForecastRefreshInterval/setValue` topic
        in order to update the `hourly_forecast_refresh_interval` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict() # type: Dict[str, str]
        prop_version_str = user_properties.get('PropertyVersion', "-1") # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data # type: Optional[bytes]
        response_topic = message.response_topic # type: Optional[str]

        try:
            if int(prop_version) != int(self._property_hourly_forecast_refresh_interval.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_hourly_forecast_refresh_interval.version}' of the 'hourly_forecast_refresh_interval' property")

            recv_prop_obj = HourlyForecastRefreshIntervalProperty.model_validate_json(message.payload)

            prop_value = recv_prop_obj.seconds
            with self._property_hourly_forecast_refresh_interval.mutex:
                self._property_hourly_forecast_refresh_interval.version += 1
                self._property_hourly_forecast_refresh_interval.set_value(prop_value)
                
                current_prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())
                
                state_msg = MessageCreator.property_state_message("weather/{}/property/hourlyForecastRefreshInterval/value".format(self._instance_id), current_prop_obj, self._property_hourly_forecast_refresh_interval.version)
                self._conn.publish(state_msg)
            
                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = MessageCreator.property_response_message(response_topic, current_prop_obj, str(self._property_hourly_forecast_refresh_interval.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            
            for hourly_forecast_refresh_interval_callback in self._property_hourly_forecast_refresh_interval.callbacks:
                
                hourly_forecast_refresh_interval_callback(current_prop_obj.seconds)
                
            
        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())
                if isinstance(e, (json.JSONDecodeError, ValidationError)):
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                elif isinstance(e, StingerMethodException):
                    return_code = e.return_code
                else:
                    return_code = MethodReturnCode.SERVER_ERROR
                prop_resp_msg = MessageCreator.property_response_message(response_topic, prop_obj, str(self._property_hourly_forecast_refresh_interval.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)
    
    
    
    def _receive_daily_forecast_refresh_interval_update_request_message(self, message: Message):
        """ When the MQTT client receives a message to the `weather/{}/property/dailyForecastRefreshInterval/setValue` topic
        in order to update the `daily_forecast_refresh_interval` property, this method is called to process that message
        and update the value of the property.
        """
        user_properties = message.user_properties or dict() # type: Dict[str, str]
        prop_version_str = user_properties.get('PropertyVersion', "-1") # type: str
        prop_version = int(prop_version_str)
        correlation_id = message.correlation_data # type: Optional[bytes]
        response_topic = message.response_topic # type: Optional[str]

        try:
            if int(prop_version) != int(self._property_daily_forecast_refresh_interval.version):
                raise OutOfSyncStingerMethodException(f"Request version '{prop_version}'' does not match current version '{self._property_daily_forecast_refresh_interval.version}' of the 'daily_forecast_refresh_interval' property")

            recv_prop_obj = DailyForecastRefreshIntervalProperty.model_validate_json(message.payload)

            prop_value = recv_prop_obj.seconds
            with self._property_daily_forecast_refresh_interval.mutex:
                self._property_daily_forecast_refresh_interval.version += 1
                self._property_daily_forecast_refresh_interval.set_value(prop_value)
                
                current_prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())
                
                state_msg = MessageCreator.property_state_message("weather/{}/property/dailyForecastRefreshInterval/value".format(self._instance_id), current_prop_obj, self._property_daily_forecast_refresh_interval.version)
                self._conn.publish(state_msg)
            
                if response_topic is not None:
                    self._logger.debug("Sending property update response for to %s", response_topic)
                    prop_resp_msg = MessageCreator.property_response_message(response_topic, current_prop_obj, str(self._property_daily_forecast_refresh_interval.version), MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(prop_resp_msg)
                else:
                    self._logger.debug("No response topic provided for property update of %s", message.topic)

            
            for daily_forecast_refresh_interval_callback in self._property_daily_forecast_refresh_interval.callbacks:
                
                daily_forecast_refresh_interval_callback(current_prop_obj.seconds)
                
            
        except Exception as e:
            self._logger.exception("StingerMethodException while processing property update for %s: %s", message.topic, str(e))
            if response_topic is not None:
                prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())
                if isinstance(e, (json.JSONDecodeError, ValidationError)):
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                elif isinstance(e, StingerMethodException):
                    return_code = e.return_code
                else:
                    return_code = MethodReturnCode.SERVER_ERROR
                prop_resp_msg = MessageCreator.property_response_message(response_topic, prop_obj, str(self._property_daily_forecast_refresh_interval.version), return_code.value, correlation_id, str(e))
                self._conn.publish(prop_resp_msg)
    
    

    def _receive_message(self, message: Message):
        """ This is the callback that is called whenever any message is received on a subscribed topic.
        """
        self._logger.warning("Received unexpected message: %s", message)

    def emit_current_time(self, current_time: str):
        """ Server application code should call this method to emit the 'current_time' signal.

        CurrentTimeSignalPayload is a pydantic BaseModel which will validate the arguments.
        """
        
        assert isinstance(current_time, str), f"The 'current_time' argument must be of type str, but was {type(current_time)}"
        

        payload = CurrentTimeSignalPayload(
            current_time=current_time,
        )
        sig_msg = MessageCreator.signal_message("weather/{}/signal/currentTime".format(self._instance_id), payload)
        self._conn.publish(sig_msg)

    

    
    def handle_refresh_daily_forecast(self, handler: Callable[[], None]):
        """ This is a decorator to decorate a method that will handle the 'refresh_daily_forecast' method calls.
        """
        if self._method_refresh_daily_forecast_handler is None and handler is not None:
            self._method_refresh_daily_forecast_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_daily_forecast_call(self, message: Message):
        """ This processes a call to the 'refresh_daily_forecast' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        try:
            payload = RefreshDailyForecastMethodRequest.model_validate_json(message.payload)
        except (json.JSONDecodeError, ValidationError) as e:
            self._logger.warning("Deserialization error while handling refresh_daily_forecast: %s", e)
            correlation_id = message.correlation_data
            response_topic = message.response_topic
            return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
            if response_topic:
                err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                self._conn.publish(err_msg)
            return
        correlation_id = message.correlation_data
        response_topic = message.response_topic

        if self._method_refresh_daily_forecast_handler is not None:
            method_args = [] # type: List[Any]
            
            return_json = ""
            debug_msg = None # type: Optional[str]
            try:
                self._method_refresh_daily_forecast_handler(*method_args)
                
                
                return_data = "{}"
                
            except (json.JSONDecodeError, ValidationError) as e:
                self._logger.warning("Deserialization error while handling refresh_daily_forecast: %s", e)
                if response_topic is not None:
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                    self._conn.publish(err_msg)
            except StingerMethodException as sme:
                self._logger.warning("StingerMethodException while handling refresh_daily_forecast: %s", sme)
                if response_topic is not None:
                    return_code = sme.return_code
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(sme))
                    self._conn.publish(err_msg)
            except Exception as e:
                self._logger.exception("Exception while handling refresh_daily_forecast", exc_info=e)
                if response_topic is not None:
                    return_code = MethodReturnCode.SERVER_ERROR
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                    self._conn.publish(err_msg)
            else:
                if response_topic is not None:
                    msg = MessageCreator.response_message(response_topic, return_data, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    
    def handle_refresh_hourly_forecast(self, handler: Callable[[], None]):
        """ This is a decorator to decorate a method that will handle the 'refresh_hourly_forecast' method calls.
        """
        if self._method_refresh_hourly_forecast_handler is None and handler is not None:
            self._method_refresh_hourly_forecast_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_hourly_forecast_call(self, message: Message):
        """ This processes a call to the 'refresh_hourly_forecast' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        try:
            payload = RefreshHourlyForecastMethodRequest.model_validate_json(message.payload)
        except (json.JSONDecodeError, ValidationError) as e:
            self._logger.warning("Deserialization error while handling refresh_hourly_forecast: %s", e)
            correlation_id = message.correlation_data
            response_topic = message.response_topic
            return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
            if response_topic:
                err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                self._conn.publish(err_msg)
            return
        correlation_id = message.correlation_data
        response_topic = message.response_topic

        if self._method_refresh_hourly_forecast_handler is not None:
            method_args = [] # type: List[Any]
            
            return_json = ""
            debug_msg = None # type: Optional[str]
            try:
                self._method_refresh_hourly_forecast_handler(*method_args)
                
                
                return_data = "{}"
                
            except (json.JSONDecodeError, ValidationError) as e:
                self._logger.warning("Deserialization error while handling refresh_hourly_forecast: %s", e)
                if response_topic is not None:
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                    self._conn.publish(err_msg)
            except StingerMethodException as sme:
                self._logger.warning("StingerMethodException while handling refresh_hourly_forecast: %s", sme)
                if response_topic is not None:
                    return_code = sme.return_code
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(sme))
                    self._conn.publish(err_msg)
            except Exception as e:
                self._logger.exception("Exception while handling refresh_hourly_forecast", exc_info=e)
                if response_topic is not None:
                    return_code = MethodReturnCode.SERVER_ERROR
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                    self._conn.publish(err_msg)
            else:
                if response_topic is not None:
                    msg = MessageCreator.response_message(response_topic, return_data, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    
    def handle_refresh_current_conditions(self, handler: Callable[[], None]):
        """ This is a decorator to decorate a method that will handle the 'refresh_current_conditions' method calls.
        """
        if self._method_refresh_current_conditions_handler is None and handler is not None:
            self._method_refresh_current_conditions_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_current_conditions_call(self, message: Message):
        """ This processes a call to the 'refresh_current_conditions' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        try:
            payload = RefreshCurrentConditionsMethodRequest.model_validate_json(message.payload)
        except (json.JSONDecodeError, ValidationError) as e:
            self._logger.warning("Deserialization error while handling refresh_current_conditions: %s", e)
            correlation_id = message.correlation_data
            response_topic = message.response_topic
            return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
            if response_topic:
                err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                self._conn.publish(err_msg)
            return
        correlation_id = message.correlation_data
        response_topic = message.response_topic

        if self._method_refresh_current_conditions_handler is not None:
            method_args = [] # type: List[Any]
            
            return_json = ""
            debug_msg = None # type: Optional[str]
            try:
                self._method_refresh_current_conditions_handler(*method_args)
                
                
                return_data = "{}"
                
            except (json.JSONDecodeError, ValidationError) as e:
                self._logger.warning("Deserialization error while handling refresh_current_conditions: %s", e)
                if response_topic is not None:
                    return_code = MethodReturnCode.SERVER_DESERIALIZATION_ERROR
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                    self._conn.publish(err_msg)
            except StingerMethodException as sme:
                self._logger.warning("StingerMethodException while handling refresh_current_conditions: %s", sme)
                if response_topic is not None:
                    return_code = sme.return_code
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(sme))
                    self._conn.publish(err_msg)
            except Exception as e:
                self._logger.exception("Exception while handling refresh_current_conditions", exc_info=e)
                if response_topic is not None:
                    return_code = MethodReturnCode.SERVER_ERROR
                    err_msg = MessageCreator.error_response_message(response_topic, return_code.value, correlation_id, debug_info=str(e))
                    self._conn.publish(err_msg)
            else:
                if response_topic is not None:
                    msg = MessageCreator.response_message(response_topic, return_data, MethodReturnCode.SUCCESS.value, correlation_id)
                    self._conn.publish(msg)

    
    
     
    @property
    def location(self) -> LocationProperty:
        """ This property returns the last received value for the 'location' property.
        The 'location' property contains multiple values, so we operate on the full 
        `LocationProperty` structure.
        
        """
        return self._property_location.get_value()

    @location.setter
    def location(self, value: LocationProperty):
        """ This property sets (publishes) a new value structure for the 'location' property.
        
        """
        if not isinstance(value, LocationProperty):
            raise ValueError(f"The value must be LocationProperty.")

            value_updated = False
            with self._property_location.mutex:
                if value != self._property_location.get_value():
                    value_updated = True
                    self._property_location.set_value(value)
                    self._property_location.version += 1
                    state_msg = MessageCreator.property_state_message("weather/{}/property/location/value".format(self._instance_id), self._property_location.get_value(), self._property_location.version)
                    self._conn.publish(state_msg)
            
            if value_updated:
                for location_callback in self._property_location.callbacks:
                    location_callback(self._property_location.get_value())
            
    

    def set_location(self, latitude: float, longitude: float):
        """ This method sets (publishes) a new value for the 'location' property.
        """
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

    def on_location_updated(self, handler: Callable[[float, float], None]):
        """ This method registers a callback to be called whenever a new 'location' property update is received.
        """
        def wrapper(value: LocationProperty):
            handler(value.latitude, value.longitude, )
        self._property_location.callbacks.append(wrapper)
    
    
    @property
    def current_temperature(self) -> Optional[float]:
        """ This property returns the last received (float) value for the 'current_temperature' property.
        
        """
        return self._property_current_temperature.get_value()

    @current_temperature.setter
    def current_temperature(self, temperature_f: float):
        """ This property sets (publishes) a new float value for the 'current_temperature' property.
        
        """
        if (not isinstance(temperature_f, float)):
            raise ValueError(f"The value must be float .")

        value_updated = False
        with self._property_current_temperature.mutex:
            if temperature_f != self._property_current_temperature.get_value():
                value_updated = True
                self._property_current_temperature.set_value(temperature_f)
                self._property_current_temperature.version += 1
                prop_obj = CurrentTemperatureProperty(temperature_f=self._property_current_temperature.get_value())
                state_msg = MessageCreator.property_state_message("weather/{}/property/currentTemperature/value".format(self._instance_id), prop_obj, self._property_current_temperature.version)
                self._conn.publish(state_msg)
        
        if value_updated:
            for current_temperature_callback in self._property_current_temperature.callbacks:
                current_temperature_callback(prop_obj.temperature_f)
        

    def set_current_temperature(self, temperature_f: float):
        """ This method sets (publishes) a new value for the 'current_temperature' property.
        """
        if not isinstance(temperature_f, float):
            raise ValueError(f"The 'temperature_f' value must be float.")

        
        obj = temperature_f
        

        # Use the property.setter to do that actual work.
        self.current_temperature = obj

    def on_current_temperature_updated(self, handler: Callable[[float], None]):
        """ This method registers a callback to be called whenever a new 'current_temperature' property update is received.
        """
        self._property_current_temperature.callbacks.append(handler)
    
     
    @property
    def current_condition(self) -> CurrentConditionProperty:
        """ This property returns the last received value for the 'current_condition' property.
        The 'current_condition' property contains multiple values, so we operate on the full 
        `CurrentConditionProperty` structure.
        
        """
        return self._property_current_condition.get_value()

    @current_condition.setter
    def current_condition(self, value: CurrentConditionProperty):
        """ This property sets (publishes) a new value structure for the 'current_condition' property.
        
        """
        if not isinstance(value, CurrentConditionProperty):
            raise ValueError(f"The value must be CurrentConditionProperty.")

            value_updated = False
            with self._property_current_condition.mutex:
                if value != self._property_current_condition.get_value():
                    value_updated = True
                    self._property_current_condition.set_value(value)
                    self._property_current_condition.version += 1
                    state_msg = MessageCreator.property_state_message("weather/{}/property/currentCondition/value".format(self._instance_id), self._property_current_condition.get_value(), self._property_current_condition.version)
                    self._conn.publish(state_msg)
            
            if value_updated:
                for current_condition_callback in self._property_current_condition.callbacks:
                    current_condition_callback(self._property_current_condition.get_value())
            
    

    def set_current_condition(self, condition: WeatherCondition, description: str):
        """ This method sets (publishes) a new value for the 'current_condition' property.
        """
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

    def on_current_condition_updated(self, handler: Callable[[WeatherCondition, str], None]):
        """ This method registers a callback to be called whenever a new 'current_condition' property update is received.
        """
        def wrapper(value: CurrentConditionProperty):
            handler(value.condition, value.description, )
        self._property_current_condition.callbacks.append(wrapper)
    
     
    @property
    def daily_forecast(self) -> DailyForecastProperty:
        """ This property returns the last received value for the 'daily_forecast' property.
        The 'daily_forecast' property contains multiple values, so we operate on the full 
        `DailyForecastProperty` structure.
        
        """
        return self._property_daily_forecast.get_value()

    @daily_forecast.setter
    def daily_forecast(self, value: DailyForecastProperty):
        """ This property sets (publishes) a new value structure for the 'daily_forecast' property.
        
        """
        if not isinstance(value, DailyForecastProperty):
            raise ValueError(f"The value must be DailyForecastProperty.")

            value_updated = False
            with self._property_daily_forecast.mutex:
                if value != self._property_daily_forecast.get_value():
                    value_updated = True
                    self._property_daily_forecast.set_value(value)
                    self._property_daily_forecast.version += 1
                    state_msg = MessageCreator.property_state_message("weather/{}/property/dailyForecast/value".format(self._instance_id), self._property_daily_forecast.get_value(), self._property_daily_forecast.version)
                    self._conn.publish(state_msg)
            
            if value_updated:
                for daily_forecast_callback in self._property_daily_forecast.callbacks:
                    daily_forecast_callback(self._property_daily_forecast.get_value())
            
    

    def set_daily_forecast(self, monday: ForecastForDay, tuesday: ForecastForDay, wednesday: ForecastForDay):
        """ This method sets (publishes) a new value for the 'daily_forecast' property.
        """
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

    def on_daily_forecast_updated(self, handler: Callable[[ForecastForDay, ForecastForDay, ForecastForDay], None]):
        """ This method registers a callback to be called whenever a new 'daily_forecast' property update is received.
        """
        def wrapper(value: DailyForecastProperty):
            handler(value.monday, value.tuesday, value.wednesday, )
        self._property_daily_forecast.callbacks.append(wrapper)
    
     
    @property
    def hourly_forecast(self) -> HourlyForecastProperty:
        """ This property returns the last received value for the 'hourly_forecast' property.
        The 'hourly_forecast' property contains multiple values, so we operate on the full 
        `HourlyForecastProperty` structure.
        
        """
        return self._property_hourly_forecast.get_value()

    @hourly_forecast.setter
    def hourly_forecast(self, value: HourlyForecastProperty):
        """ This property sets (publishes) a new value structure for the 'hourly_forecast' property.
        
        """
        if not isinstance(value, HourlyForecastProperty):
            raise ValueError(f"The value must be HourlyForecastProperty.")

            value_updated = False
            with self._property_hourly_forecast.mutex:
                if value != self._property_hourly_forecast.get_value():
                    value_updated = True
                    self._property_hourly_forecast.set_value(value)
                    self._property_hourly_forecast.version += 1
                    state_msg = MessageCreator.property_state_message("weather/{}/property/hourlyForecast/value".format(self._instance_id), self._property_hourly_forecast.get_value(), self._property_hourly_forecast.version)
                    self._conn.publish(state_msg)
            
            if value_updated:
                for hourly_forecast_callback in self._property_hourly_forecast.callbacks:
                    hourly_forecast_callback(self._property_hourly_forecast.get_value())
            
    

    def set_hourly_forecast(self, hour_0: ForecastForHour, hour_1: ForecastForHour, hour_2: ForecastForHour, hour_3: ForecastForHour):
        """ This method sets (publishes) a new value for the 'hourly_forecast' property.
        """
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

    def on_hourly_forecast_updated(self, handler: Callable[[ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour], None]):
        """ This method registers a callback to be called whenever a new 'hourly_forecast' property update is received.
        """
        def wrapper(value: HourlyForecastProperty):
            handler(value.hour_0, value.hour_1, value.hour_2, value.hour_3, )
        self._property_hourly_forecast.callbacks.append(wrapper)
    
    
    @property
    def current_condition_refresh_interval(self) -> Optional[int]:
        """ This property returns the last received (int) value for the 'current_condition_refresh_interval' property.
        
        """
        return self._property_current_condition_refresh_interval.get_value()

    @current_condition_refresh_interval.setter
    def current_condition_refresh_interval(self, seconds: int):
        """ This property sets (publishes) a new int value for the 'current_condition_refresh_interval' property.
        
        """
        if (not isinstance(seconds, int)):
            raise ValueError(f"The value must be int .")

        value_updated = False
        with self._property_current_condition_refresh_interval.mutex:
            if seconds != self._property_current_condition_refresh_interval.get_value():
                value_updated = True
                self._property_current_condition_refresh_interval.set_value(seconds)
                self._property_current_condition_refresh_interval.version += 1
                prop_obj = CurrentConditionRefreshIntervalProperty(seconds=self._property_current_condition_refresh_interval.get_value())
                state_msg = MessageCreator.property_state_message("weather/{}/property/currentConditionRefreshInterval/value".format(self._instance_id), prop_obj, self._property_current_condition_refresh_interval.version)
                self._conn.publish(state_msg)
        
        if value_updated:
            for current_condition_refresh_interval_callback in self._property_current_condition_refresh_interval.callbacks:
                current_condition_refresh_interval_callback(prop_obj.seconds)
        

    def set_current_condition_refresh_interval(self, seconds: int):
        """ This method sets (publishes) a new value for the 'current_condition_refresh_interval' property.
        """
        if not isinstance(seconds, int):
            raise ValueError(f"The 'seconds' value must be int.")

        
        obj = seconds
        

        # Use the property.setter to do that actual work.
        self.current_condition_refresh_interval = obj

    def on_current_condition_refresh_interval_updated(self, handler: Callable[[int], None]):
        """ This method registers a callback to be called whenever a new 'current_condition_refresh_interval' property update is received.
        """
        self._property_current_condition_refresh_interval.callbacks.append(handler)
    
    
    @property
    def hourly_forecast_refresh_interval(self) -> Optional[int]:
        """ This property returns the last received (int) value for the 'hourly_forecast_refresh_interval' property.
        
        """
        return self._property_hourly_forecast_refresh_interval.get_value()

    @hourly_forecast_refresh_interval.setter
    def hourly_forecast_refresh_interval(self, seconds: int):
        """ This property sets (publishes) a new int value for the 'hourly_forecast_refresh_interval' property.
        
        """
        if (not isinstance(seconds, int)):
            raise ValueError(f"The value must be int .")

        value_updated = False
        with self._property_hourly_forecast_refresh_interval.mutex:
            if seconds != self._property_hourly_forecast_refresh_interval.get_value():
                value_updated = True
                self._property_hourly_forecast_refresh_interval.set_value(seconds)
                self._property_hourly_forecast_refresh_interval.version += 1
                prop_obj = HourlyForecastRefreshIntervalProperty(seconds=self._property_hourly_forecast_refresh_interval.get_value())
                state_msg = MessageCreator.property_state_message("weather/{}/property/hourlyForecastRefreshInterval/value".format(self._instance_id), prop_obj, self._property_hourly_forecast_refresh_interval.version)
                self._conn.publish(state_msg)
        
        if value_updated:
            for hourly_forecast_refresh_interval_callback in self._property_hourly_forecast_refresh_interval.callbacks:
                hourly_forecast_refresh_interval_callback(prop_obj.seconds)
        

    def set_hourly_forecast_refresh_interval(self, seconds: int):
        """ This method sets (publishes) a new value for the 'hourly_forecast_refresh_interval' property.
        """
        if not isinstance(seconds, int):
            raise ValueError(f"The 'seconds' value must be int.")

        
        obj = seconds
        

        # Use the property.setter to do that actual work.
        self.hourly_forecast_refresh_interval = obj

    def on_hourly_forecast_refresh_interval_updated(self, handler: Callable[[int], None]):
        """ This method registers a callback to be called whenever a new 'hourly_forecast_refresh_interval' property update is received.
        """
        self._property_hourly_forecast_refresh_interval.callbacks.append(handler)
    
    
    @property
    def daily_forecast_refresh_interval(self) -> Optional[int]:
        """ This property returns the last received (int) value for the 'daily_forecast_refresh_interval' property.
        
        """
        return self._property_daily_forecast_refresh_interval.get_value()

    @daily_forecast_refresh_interval.setter
    def daily_forecast_refresh_interval(self, seconds: int):
        """ This property sets (publishes) a new int value for the 'daily_forecast_refresh_interval' property.
        
        """
        if (not isinstance(seconds, int)):
            raise ValueError(f"The value must be int .")

        value_updated = False
        with self._property_daily_forecast_refresh_interval.mutex:
            if seconds != self._property_daily_forecast_refresh_interval.get_value():
                value_updated = True
                self._property_daily_forecast_refresh_interval.set_value(seconds)
                self._property_daily_forecast_refresh_interval.version += 1
                prop_obj = DailyForecastRefreshIntervalProperty(seconds=self._property_daily_forecast_refresh_interval.get_value())
                state_msg = MessageCreator.property_state_message("weather/{}/property/dailyForecastRefreshInterval/value".format(self._instance_id), prop_obj, self._property_daily_forecast_refresh_interval.version)
                self._conn.publish(state_msg)
        
        if value_updated:
            for daily_forecast_refresh_interval_callback in self._property_daily_forecast_refresh_interval.callbacks:
                daily_forecast_refresh_interval_callback(prop_obj.seconds)
        

    def set_daily_forecast_refresh_interval(self, seconds: int):
        """ This method sets (publishes) a new value for the 'daily_forecast_refresh_interval' property.
        """
        if not isinstance(seconds, int):
            raise ValueError(f"The 'seconds' value must be int.")

        
        obj = seconds
        

        # Use the property.setter to do that actual work.
        self.daily_forecast_refresh_interval = obj

    def on_daily_forecast_refresh_interval_updated(self, handler: Callable[[int], None]):
        """ This method registers a callback to be called whenever a new 'daily_forecast_refresh_interval' property update is received.
        """
        self._property_daily_forecast_refresh_interval.callbacks.append(handler)
    

class WeatherServerBuilder:
    """
    This is a builder for the WeatherServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self):
        
        
        self._refresh_daily_forecast_method_handler: Optional[Callable[[], None]] = None
        self._refresh_hourly_forecast_method_handler: Optional[Callable[[], None]] = None
        self._refresh_current_conditions_method_handler: Optional[Callable[[], None]] = None
        
        self._location_property_callbacks: List[Callable[[float, float], None]] = []
        self._current_temperature_property_callbacks: List[Callable[[float], None]] = []
        self._current_condition_property_callbacks: List[Callable[[WeatherCondition, str], None]] = []
        self._daily_forecast_property_callbacks: List[Callable[[ForecastForDay, ForecastForDay, ForecastForDay], None]] = []
        self._hourly_forecast_property_callbacks: List[Callable[[ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour], None]] = []
        self._current_condition_refresh_interval_property_callbacks: List[Callable[[int], None]] = []
        self._hourly_forecast_refresh_interval_property_callbacks: List[Callable[[int], None]] = []
        self._daily_forecast_refresh_interval_property_callbacks: List[Callable[[int], None]] = []
    
    def handle_refresh_daily_forecast(self, handler: Callable[[], None]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        if self._refresh_daily_forecast_method_handler is None and handler is not None:
            self._refresh_daily_forecast_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper
    
    def handle_refresh_hourly_forecast(self, handler: Callable[[], None]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        if self._refresh_hourly_forecast_method_handler is None and handler is not None:
            self._refresh_hourly_forecast_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper
    
    def handle_refresh_current_conditions(self, handler: Callable[[], None]):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        if self._refresh_current_conditions_method_handler is None and handler is not None:
            self._refresh_current_conditions_method_handler = wrapper
        else:
            raise Exception("Method handler already set")
        return wrapper
    
    
    def on_location_updated(self, handler: Callable[[float, float], None]):
        """ This method registers a callback to be called whenever a new 'location' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._location_property_callbacks.append(wrapper)
        return wrapper
    
    def on_current_temperature_updated(self, handler: Callable[[float], None]):
        """ This method registers a callback to be called whenever a new 'current_temperature' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._current_temperature_property_callbacks.append(wrapper)
        return wrapper
    
    def on_current_condition_updated(self, handler: Callable[[WeatherCondition, str], None]):
        """ This method registers a callback to be called whenever a new 'current_condition' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._current_condition_property_callbacks.append(wrapper)
        return wrapper
    
    def on_daily_forecast_updated(self, handler: Callable[[ForecastForDay, ForecastForDay, ForecastForDay], None]):
        """ This method registers a callback to be called whenever a new 'daily_forecast' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._daily_forecast_property_callbacks.append(wrapper)
        return wrapper
    
    def on_hourly_forecast_updated(self, handler: Callable[[ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour], None]):
        """ This method registers a callback to be called whenever a new 'hourly_forecast' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._hourly_forecast_property_callbacks.append(wrapper)
        return wrapper
    
    def on_current_condition_refresh_interval_updated(self, handler: Callable[[int], None]):
        """ This method registers a callback to be called whenever a new 'current_condition_refresh_interval' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._current_condition_refresh_interval_property_callbacks.append(wrapper)
        return wrapper
    
    def on_hourly_forecast_refresh_interval_updated(self, handler: Callable[[int], None]):
        """ This method registers a callback to be called whenever a new 'hourly_forecast_refresh_interval' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._hourly_forecast_refresh_interval_property_callbacks.append(wrapper)
        return wrapper
    
    def on_daily_forecast_refresh_interval_updated(self, handler: Callable[[int], None]):
        """ This method registers a callback to be called whenever a new 'daily_forecast_refresh_interval' property update is received.
        """
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        self._daily_forecast_refresh_interval_property_callbacks.append(wrapper)
        return wrapper
    
    def build(self, connection: IBrokerConnection, instance_id: str, initial_property_values: WeatherInitialPropertyValues, binding: Optional[Any]=None) -> WeatherServer:
        new_server = WeatherServer(connection, instance_id, initial_property_values)
        
        if self._refresh_daily_forecast_method_handler is not None:
            if binding:
                new_server.handle_refresh_daily_forecast(self._refresh_daily_forecast_method_handler.__get__(binding, binding.__class__))
            else:
                new_server.handle_refresh_daily_forecast(self._refresh_daily_forecast_method_handler)
        if self._refresh_hourly_forecast_method_handler is not None:
            if binding:
                new_server.handle_refresh_hourly_forecast(self._refresh_hourly_forecast_method_handler.__get__(binding, binding.__class__))
            else:
                new_server.handle_refresh_hourly_forecast(self._refresh_hourly_forecast_method_handler)
        if self._refresh_current_conditions_method_handler is not None:
            if binding:
                new_server.handle_refresh_current_conditions(self._refresh_current_conditions_method_handler.__get__(binding, binding.__class__))
            else:
                new_server.handle_refresh_current_conditions(self._refresh_current_conditions_method_handler)
        
        for location_callback in self._location_property_callbacks:
            if binding:
                new_server.on_location_updated(location_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_location_updated(location_callback)
        
        for current_temperature_callback in self._current_temperature_property_callbacks:
            if binding:
                new_server.on_current_temperature_updated(current_temperature_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_current_temperature_updated(current_temperature_callback)
        
        for current_condition_callback in self._current_condition_property_callbacks:
            if binding:
                new_server.on_current_condition_updated(current_condition_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_current_condition_updated(current_condition_callback)
        
        for daily_forecast_callback in self._daily_forecast_property_callbacks:
            if binding:
                new_server.on_daily_forecast_updated(daily_forecast_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_daily_forecast_updated(daily_forecast_callback)
        
        for hourly_forecast_callback in self._hourly_forecast_property_callbacks:
            if binding:
                new_server.on_hourly_forecast_updated(hourly_forecast_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_hourly_forecast_updated(hourly_forecast_callback)
        
        for current_condition_refresh_interval_callback in self._current_condition_refresh_interval_property_callbacks:
            if binding:
                new_server.on_current_condition_refresh_interval_updated(current_condition_refresh_interval_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_current_condition_refresh_interval_updated(current_condition_refresh_interval_callback)
        
        for hourly_forecast_refresh_interval_callback in self._hourly_forecast_refresh_interval_property_callbacks:
            if binding:
                new_server.on_hourly_forecast_refresh_interval_updated(hourly_forecast_refresh_interval_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_hourly_forecast_refresh_interval_updated(hourly_forecast_refresh_interval_callback)
        
        for daily_forecast_refresh_interval_callback in self._daily_forecast_refresh_interval_property_callbacks:
            if binding:
                new_server.on_daily_forecast_refresh_interval_updated(daily_forecast_refresh_interval_callback.__get__(binding, binding.__class__))
            else:
                new_server.on_daily_forecast_refresh_interval_updated(daily_forecast_refresh_interval_callback)
        
        return new_server
