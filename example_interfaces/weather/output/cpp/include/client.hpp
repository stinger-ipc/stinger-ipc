/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once

#include <cstdint>
#include <functional>
#include <map>
#include <memory>
#include <exception>
#include <mutex>
#include <chrono>
#include <rapidjson/document.h>
#include "utils.hpp"
#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "method_payloads.hpp"
#include "signal_payloads.hpp"

#include "property_structs.hpp"

class WeatherClient
{
public:
    // This is the name of the API.
    static constexpr const char NAME[] = "weather";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.1.2";

    // Constructor taking a connection object.
    WeatherClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId);

    virtual ~WeatherClient();
    // ------------------ SIGNALS --------------------

    // Register a callback for the `current_time` signal.
    // The provided method will be called whenever a `current_time` is received.
    void registerCurrentTimeCallback(const std::function<void(std::string)>& cb);

    // ------------------- METHODS --------------------

    // Calls the `refresh_daily_forecast` method.
    // Returns a future.  When that future resolves, it will have the returned value. None
    std::future<void> refreshDailyForecast();

    // Calls the `refresh_hourly_forecast` method.
    // Returns a future.  When that future resolves, it will have the returned value. None
    std::future<void> refreshHourlyForecast();

    // Calls the `refresh_current_conditions` method.
    // Returns a future.  When that future resolves, it will have the returned value. None
    std::future<void> refreshCurrentConditions();

    // ---------------- PROPERTIES ------------------

    // ---location Property---

    // Gets the latest value of the `location` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<LocationProperty> getLocationProperty();

    // Add a callback that will be called whenever the `location` property is updated.
    // The provided method will be called whenever a new value for the `location` property is received.
    void registerLocationPropertyCallback(const std::function<void(double, double)>& cb);

    std::future<bool> updateLocationProperty(double, double) const;

    // ---current_temperature Property---

    // Gets the latest value of the `current_temperature` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<double> getCurrentTemperatureProperty();

    // Add a callback that will be called whenever the `current_temperature` property is updated.
    // The provided method will be called whenever a new value for the `current_temperature` property is received.
    void registerCurrentTemperaturePropertyCallback(const std::function<void(double)>& cb);

    // ---current_condition Property---

    // Gets the latest value of the `current_condition` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<CurrentConditionProperty> getCurrentConditionProperty();

    // Add a callback that will be called whenever the `current_condition` property is updated.
    // The provided method will be called whenever a new value for the `current_condition` property is received.
    void registerCurrentConditionPropertyCallback(const std::function<void(WeatherCondition, std::string)>& cb);

    // ---daily_forecast Property---

    // Gets the latest value of the `daily_forecast` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<DailyForecastProperty> getDailyForecastProperty();

    // Add a callback that will be called whenever the `daily_forecast` property is updated.
    // The provided method will be called whenever a new value for the `daily_forecast` property is received.
    void registerDailyForecastPropertyCallback(const std::function<void(ForecastForDay, ForecastForDay, ForecastForDay)>& cb);

    // ---hourly_forecast Property---

    // Gets the latest value of the `hourly_forecast` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<HourlyForecastProperty> getHourlyForecastProperty();

    // Add a callback that will be called whenever the `hourly_forecast` property is updated.
    // The provided method will be called whenever a new value for the `hourly_forecast` property is received.
    void registerHourlyForecastPropertyCallback(const std::function<void(ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour)>& cb);

    // ---current_condition_refresh_interval Property---

    // Gets the latest value of the `current_condition_refresh_interval` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<int> getCurrentConditionRefreshIntervalProperty();

    // Add a callback that will be called whenever the `current_condition_refresh_interval` property is updated.
    // The provided method will be called whenever a new value for the `current_condition_refresh_interval` property is received.
    void registerCurrentConditionRefreshIntervalPropertyCallback(const std::function<void(int)>& cb);

    std::future<bool> updateCurrentConditionRefreshIntervalProperty(int) const;

    // ---hourly_forecast_refresh_interval Property---

    // Gets the latest value of the `hourly_forecast_refresh_interval` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<int> getHourlyForecastRefreshIntervalProperty();

    // Add a callback that will be called whenever the `hourly_forecast_refresh_interval` property is updated.
    // The provided method will be called whenever a new value for the `hourly_forecast_refresh_interval` property is received.
    void registerHourlyForecastRefreshIntervalPropertyCallback(const std::function<void(int)>& cb);

    std::future<bool> updateHourlyForecastRefreshIntervalProperty(int) const;

    // ---daily_forecast_refresh_interval Property---

    // Gets the latest value of the `daily_forecast_refresh_interval` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<int> getDailyForecastRefreshIntervalProperty();

    // Add a callback that will be called whenever the `daily_forecast_refresh_interval` property is updated.
    // The provided method will be called whenever a new value for the `daily_forecast_refresh_interval` property is received.
    void registerDailyForecastRefreshIntervalPropertyCallback(const std::function<void(int)>& cb);

    std::future<bool> updateDailyForecastRefreshIntervalProperty(int) const;

private:
    // Pointer to the broker connection.
    std::shared_ptr<IBrokerConnection> _broker;

    // Service Instance ID that this client is connected to.
    std::string _instanceId;

    CallbackHandleType _brokerMessageCallbackHandle = 0;

    // Internal method for receiving messages from the broker.
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const MqttProperties& mqttProps
    );

    // ------------------ SIGNALS --------------------

    // List of callbacks to be called whenever the `current_time` signal is received.
    std::vector<std::function<void(std::string)>> _currentTimeSignalCallbacks;
    std::mutex _currentTimeSignalCallbacksMutex;

    // MQTT Subscription ID for `current_time` signal receptions.
    int _currentTimeSignalSubscriptionId = -1;

    // ------------------- METHODS --------------------
    // Holds promises for pending `refresh_daily_forecast` method calls.
    std::map<std::string, std::promise<void>> _pendingRefreshDailyForecastMethodCalls;
    int _refreshDailyForecastMethodSubscriptionId = -1;
    // This is called internally to process responses to `refresh_daily_forecast` method calls.
    void _handleRefreshDailyForecastResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `refresh_hourly_forecast` method calls.
    std::map<std::string, std::promise<void>> _pendingRefreshHourlyForecastMethodCalls;
    int _refreshHourlyForecastMethodSubscriptionId = -1;
    // This is called internally to process responses to `refresh_hourly_forecast` method calls.
    void _handleRefreshHourlyForecastResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `refresh_current_conditions` method calls.
    std::map<std::string, std::promise<void>> _pendingRefreshCurrentConditionsMethodCalls;
    int _refreshCurrentConditionsMethodSubscriptionId = -1;
    // This is called internally to process responses to `refresh_current_conditions` method calls.
    void _handleRefreshCurrentConditionsResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // ---------------- PROPERTIES ------------------

    // ---location Property---

    // Last received values for the `location` property.
    std::optional<LocationProperty> _locationProperty;

    // This is the property version of the last received `location` property update.
    int _lastLocationPropertyVersion = -1;

    // Mutex for protecting access to the `location` property and its version.
    mutable std::mutex _locationPropertyMutex;

    // MQTT Subscription ID for `location` property updates.
    int _locationPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `location` property.
    void _receiveLocationPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `location` property.
    std::vector<std::function<void(double, double)>> _locationPropertyCallbacks;
    std::mutex _locationPropertyCallbacksMutex;

    // ---current_temperature Property---

    // Last received value for the `current_temperature` property.
    std::optional<CurrentTemperatureProperty> _currentTemperatureProperty;

    // This is the property version of the last received `current_temperature` property update.
    int _lastCurrentTemperaturePropertyVersion = -1;

    // Mutex for protecting access to the `current_temperature` property and its version.
    mutable std::mutex _currentTemperaturePropertyMutex;

    // MQTT Subscription ID for `current_temperature` property updates.
    int _currentTemperaturePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `current_temperature` property.
    void _receiveCurrentTemperaturePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `current_temperature` property.
    std::vector<std::function<void(double)>> _currentTemperaturePropertyCallbacks;
    std::mutex _currentTemperaturePropertyCallbacksMutex;

    // ---current_condition Property---

    // Last received values for the `current_condition` property.
    std::optional<CurrentConditionProperty> _currentConditionProperty;

    // This is the property version of the last received `current_condition` property update.
    int _lastCurrentConditionPropertyVersion = -1;

    // Mutex for protecting access to the `current_condition` property and its version.
    mutable std::mutex _currentConditionPropertyMutex;

    // MQTT Subscription ID for `current_condition` property updates.
    int _currentConditionPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `current_condition` property.
    void _receiveCurrentConditionPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `current_condition` property.
    std::vector<std::function<void(WeatherCondition, std::string)>> _currentConditionPropertyCallbacks;
    std::mutex _currentConditionPropertyCallbacksMutex;

    // ---daily_forecast Property---

    // Last received values for the `daily_forecast` property.
    std::optional<DailyForecastProperty> _dailyForecastProperty;

    // This is the property version of the last received `daily_forecast` property update.
    int _lastDailyForecastPropertyVersion = -1;

    // Mutex for protecting access to the `daily_forecast` property and its version.
    mutable std::mutex _dailyForecastPropertyMutex;

    // MQTT Subscription ID for `daily_forecast` property updates.
    int _dailyForecastPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `daily_forecast` property.
    void _receiveDailyForecastPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `daily_forecast` property.
    std::vector<std::function<void(ForecastForDay, ForecastForDay, ForecastForDay)>> _dailyForecastPropertyCallbacks;
    std::mutex _dailyForecastPropertyCallbacksMutex;

    // ---hourly_forecast Property---

    // Last received values for the `hourly_forecast` property.
    std::optional<HourlyForecastProperty> _hourlyForecastProperty;

    // This is the property version of the last received `hourly_forecast` property update.
    int _lastHourlyForecastPropertyVersion = -1;

    // Mutex for protecting access to the `hourly_forecast` property and its version.
    mutable std::mutex _hourlyForecastPropertyMutex;

    // MQTT Subscription ID for `hourly_forecast` property updates.
    int _hourlyForecastPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `hourly_forecast` property.
    void _receiveHourlyForecastPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `hourly_forecast` property.
    std::vector<std::function<void(ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour)>> _hourlyForecastPropertyCallbacks;
    std::mutex _hourlyForecastPropertyCallbacksMutex;

    // ---current_condition_refresh_interval Property---

    // Last received value for the `current_condition_refresh_interval` property.
    std::optional<CurrentConditionRefreshIntervalProperty> _currentConditionRefreshIntervalProperty;

    // This is the property version of the last received `current_condition_refresh_interval` property update.
    int _lastCurrentConditionRefreshIntervalPropertyVersion = -1;

    // Mutex for protecting access to the `current_condition_refresh_interval` property and its version.
    mutable std::mutex _currentConditionRefreshIntervalPropertyMutex;

    // MQTT Subscription ID for `current_condition_refresh_interval` property updates.
    int _currentConditionRefreshIntervalPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `current_condition_refresh_interval` property.
    void _receiveCurrentConditionRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `current_condition_refresh_interval` property.
    std::vector<std::function<void(int)>> _currentConditionRefreshIntervalPropertyCallbacks;
    std::mutex _currentConditionRefreshIntervalPropertyCallbacksMutex;

    // ---hourly_forecast_refresh_interval Property---

    // Last received value for the `hourly_forecast_refresh_interval` property.
    std::optional<HourlyForecastRefreshIntervalProperty> _hourlyForecastRefreshIntervalProperty;

    // This is the property version of the last received `hourly_forecast_refresh_interval` property update.
    int _lastHourlyForecastRefreshIntervalPropertyVersion = -1;

    // Mutex for protecting access to the `hourly_forecast_refresh_interval` property and its version.
    mutable std::mutex _hourlyForecastRefreshIntervalPropertyMutex;

    // MQTT Subscription ID for `hourly_forecast_refresh_interval` property updates.
    int _hourlyForecastRefreshIntervalPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `hourly_forecast_refresh_interval` property.
    void _receiveHourlyForecastRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `hourly_forecast_refresh_interval` property.
    std::vector<std::function<void(int)>> _hourlyForecastRefreshIntervalPropertyCallbacks;
    std::mutex _hourlyForecastRefreshIntervalPropertyCallbacksMutex;

    // ---daily_forecast_refresh_interval Property---

    // Last received value for the `daily_forecast_refresh_interval` property.
    std::optional<DailyForecastRefreshIntervalProperty> _dailyForecastRefreshIntervalProperty;

    // This is the property version of the last received `daily_forecast_refresh_interval` property update.
    int _lastDailyForecastRefreshIntervalPropertyVersion = -1;

    // Mutex for protecting access to the `daily_forecast_refresh_interval` property and its version.
    mutable std::mutex _dailyForecastRefreshIntervalPropertyMutex;

    // MQTT Subscription ID for `daily_forecast_refresh_interval` property updates.
    int _dailyForecastRefreshIntervalPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `daily_forecast_refresh_interval` property.
    void _receiveDailyForecastRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `daily_forecast_refresh_interval` property.
    std::vector<std::function<void(int)>> _dailyForecastRefreshIntervalPropertyCallbacks;
    std::mutex _dailyForecastRefreshIntervalPropertyCallbacksMutex;
};