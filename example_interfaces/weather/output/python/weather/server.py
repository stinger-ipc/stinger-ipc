"""
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the weather interface.
"""

import json
import logging

logging.basicConfig(level=logging.DEBUG)

from typing import Callable, Dict, Any, Optional, List
from connection import BrokerConnection
from method_codes import *
import interface_types as stinger_types


class WeatherServer:

    def __init__(self, connection: BrokerConnection):
        self._logger = logging.getLogger("WeatherServer")
        self._logger.setLevel(logging.DEBUG)
        self._logger.debug("Initializing WeatherServer")
        self._conn = connection
        self._conn.set_message_callback(self._receive_message)
        self._conn.set_last_will(topic="weather/interface", payload=None, qos=1, retain=True)
        self._property_location = None
        self._conn.subscribe("weather/property/location/setValue")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_current_temperature = None
        self._conn.subscribe("weather/property/currentTemperature/setValue")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_current_condition = None
        self._conn.subscribe("weather/property/currentCondition/setValue")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_daily_forecast = None
        self._conn.subscribe("weather/property/dailyForecast/setValue")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_hourly_forecast = None
        self._conn.subscribe("weather/property/hourlyForecast/setValue")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_current_condition_refresh_interval = None
        self._conn.subscribe("weather/property/currentConditionRefreshInterval/setValue")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_hourly_forecast_refresh_interval = None
        self._conn.subscribe("weather/property/hourlyForecastRefreshInterval/setValue")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()
        self._property_daily_forecast_refresh_interval = None
        self._conn.subscribe("weather/property/dailyForecastRefreshInterval/setValue")
        self.changed_value_callback_for_ = None
        self._publish_interface_info()

        self._conn.subscribe("weather/method/refreshDailyForecast")

        self._conn.subscribe("weather/method/refreshHourlyForecast")

        self._conn.subscribe("weather/method/refreshCurrentConditions")
        self._refresh_daily_forecast_method_handler: Optional[Callable[[None], None]] = None
        self._refresh_hourly_forecast_method_handler: Optional[Callable[[None], None]] = None
        self._refresh_current_conditions_method_handler: Optional[Callable[[None], None]] = None

    def _receive_message(self, topic: str, payload: str, properties: Dict[str, Any]):
        """This is the callback that is called whenever any message is received on a subscribed topic."""
        self._logger.debug("Received message to %s", topic)
        if self._conn.is_topic_sub(topic, "weather/method/refreshDailyForecast"):
            try:
                payload_obj = json.loads(payload)
            except json.decoder.JSONDecodeError:
                self._logger.warning("Invalid JSON payload received at topic '%s'", topic)
            else:
                self._process_refresh_daily_forecast_call(topic, payload_obj, properties)
        elif self._conn.is_topic_sub(topic, "weather/method/refreshHourlyForecast"):
            try:
                payload_obj = json.loads(payload)
            except json.decoder.JSONDecodeError:
                self._logger.warning("Invalid JSON payload received at topic '%s'", topic)
            else:
                self._process_refresh_hourly_forecast_call(topic, payload_obj, properties)
        elif self._conn.is_topic_sub(topic, "weather/method/refreshCurrentConditions"):
            try:
                payload_obj = json.loads(payload)
            except json.decoder.JSONDecodeError:
                self._logger.warning("Invalid JSON payload received at topic '%s'", topic)
            else:
                self._process_refresh_current_conditions_call(topic, payload_obj, properties)

    def _publish_interface_info(self):
        self._conn.publish(
            "weather/interface",
            """{"name": "weather", "summary": "Current conditions, daily and hourly forecasts from the NWS API", "title": "NWS weather forecast", "version": "0.0.1"}""",
            qos=1,
            retain=True,
        )

    def emit_current_time(self, current_time: str):
        """Server application code should call this method to emit the 'current_time' signal."""
        if not isinstance(current_time, str):
            raise ValueError(f"The 'current_time' value must be str.")

        payload = {
            "current_time": str(current_time),
        }
        self._conn.publish("weather/signal/currentTime", json.dumps(payload), qos=1, retain=False)

    def handle_refresh_daily_forecast(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_daily_forecast' method calls."""
        if self._refresh_daily_forecast_method_handler is None and handler is not None:
            self._refresh_daily_forecast_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_daily_forecast_call(self, topic: str, payload: Dict[str, Any], properties: Dict[str, Any]):
        """This processes a call to the 'refresh_daily_forecast' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._refresh_daily_forecast_method_handler is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._refresh_daily_forecast_method_handler(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling refresh_daily_forecast", exc_info=e)
                    return_code = MethodResultCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodResultCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)

    def handle_refresh_hourly_forecast(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_hourly_forecast' method calls."""
        if self._refresh_hourly_forecast_method_handler is None and handler is not None:
            self._refresh_hourly_forecast_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_hourly_forecast_call(self, topic: str, payload: Dict[str, Any], properties: Dict[str, Any]):
        """This processes a call to the 'refresh_hourly_forecast' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._refresh_hourly_forecast_method_handler is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._refresh_hourly_forecast_method_handler(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling refresh_hourly_forecast", exc_info=e)
                    return_code = MethodResultCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodResultCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)

    def handle_refresh_current_conditions(self, handler: Callable[[None], None]):
        """This is a decorator to decorate a method that will handle the 'refresh_current_conditions' method calls."""
        if self._refresh_current_conditions_method_handler is None and handler is not None:
            self._refresh_current_conditions_method_handler = handler
        else:
            raise Exception("Method handler already set")

    def _process_refresh_current_conditions_call(self, topic: str, payload: Dict[str, Any], properties: Dict[str, Any]):
        """This processes a call to the 'refresh_current_conditions' method.  It deserializes the payload to find the method arguments,
        then calls the method handler with those arguments.  It then builds and serializes a response and publishes it to the response topic.
        """
        correlation_id = properties.get("CorrelationData")  # type: Optional[bytes]
        response_topic = properties.get("ResponseTopic")  # type: Optional[str]
        self._logger.info("Correlation Data %s", correlation_id)
        if self._refresh_current_conditions_method_handler is not None:
            method_args = []  # type: List[Any]

            if response_topic is not None:
                return_json = ""
                debug_msg = None  # type: Optional[str]
                try:
                    return_struct = self._refresh_current_conditions_method_handler(*method_args)
                    self._logger.debug("Return value is %s", return_struct)

                    if return_struct is not None:
                        return_json = return_struct.model_dump_json()

                except Exception as e:
                    self._logger.exception("Exception while handling refresh_current_conditions", exc_info=e)
                    return_code = MethodResultCode.SERVER_ERROR
                    debug_msg = str(e)
                else:
                    return_code = MethodResultCode.SUCCESS
                    debug_msg = None

                self._conn.publish(response_topic, return_json, qos=1, retain=False, correlation_id=correlation_id, return_value=return_code, debug_info=debug_msg)


class WeatherServerBuilder:
    """
    This is a builder for the WeatherServer.  It is used to create a server with the desired parameters.
    """

    def __init__(self, connection: BrokerConnection):
        self._conn = connection

        self._refresh_daily_forecast_method_handler: Optional[Callable[[None], None]] = None
        self._refresh_hourly_forecast_method_handler: Optional[Callable[[None], None]] = None
        self._refresh_current_conditions_method_handler: Optional[Callable[[None], None]] = None

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

    def build(self) -> WeatherServer:
        new_server = WeatherServer(self._conn)

        if self._refresh_daily_forecast_method_handler is not None:
            new_server.handle_refresh_daily_forecast(self._refresh_daily_forecast_method_handler)
        if self._refresh_hourly_forecast_method_handler is not None:
            new_server.handle_refresh_hourly_forecast(self._refresh_hourly_forecast_method_handler)
        if self._refresh_current_conditions_method_handler is not None:
            new_server.handle_refresh_current_conditions(self._refresh_current_conditions_method_handler)
        return new_server


if __name__ == "__main__":
    """
    This shows an example on how to run the code.  Ideally, your app should do something similar, but use the methods in
    a more meaningful way.
    """
    from time import sleep
    import signal

    from connection import DefaultConnection

    conn = DefaultConnection("localhost", 1883)
    server = WeatherServer(conn)

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
