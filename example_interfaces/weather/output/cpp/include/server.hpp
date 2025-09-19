/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/

#pragma once

#include <cstdint>
#include <functional>
#include <map>
#include <string>
#include <memory>
#include <exception>
#include <mutex>
#include <boost/optional.hpp>
#include <rapidjson/document.h>

#include "property_structs.hpp"

#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "return_types.hpp"

class WeatherServer
{
public:
    static constexpr const char NAME[] = "weather";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    WeatherServer(std::shared_ptr<IBrokerConnection> broker);

    virtual ~WeatherServer() = default;

    boost::future<bool> emitCurrentTimeSignal(const std::string&);

    void registerRefreshDailyForecastHandler(std::function<void()> func);

    void registerRefreshHourlyForecastHandler(std::function<void()> func);

    void registerRefreshCurrentConditionsHandler(std::function<void()> func);

    // ---location Property---

    // Gets the latest value of the `location` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<struct LocationProperty> getLocationProperty() const;

    // Add a callback that will be called whenever the `location` property is updated.
    // The provided method will be called whenever a new value for the `location` property is received.
    void registerLocationPropertyCallback(const std::function<void(double, double)>& cb);

    void updateLocationProperty(double, double);

    // ---current_temperature Property---

    // Gets the latest value of the `current_temperature` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<CurrentTemperatureProperty> getCurrentTemperatureProperty() const;

    // Add a callback that will be called whenever the `current_temperature` property is updated.
    // The provided method will be called whenever a new value for the `current_temperature` property is received.
    void registerCurrentTemperaturePropertyCallback(const std::function<void(double)>& cb);

    void updateCurrentTemperatureProperty(double);

    // ---current_condition Property---

    // Gets the latest value of the `current_condition` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<struct CurrentConditionProperty> getCurrentConditionProperty() const;

    // Add a callback that will be called whenever the `current_condition` property is updated.
    // The provided method will be called whenever a new value for the `current_condition` property is received.
    void registerCurrentConditionPropertyCallback(const std::function<void(WeatherCondition, const std::string&)>& cb);

    void updateCurrentConditionProperty(WeatherCondition, const std::string&);

    // ---daily_forecast Property---

    // Gets the latest value of the `daily_forecast` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<struct DailyForecastProperty> getDailyForecastProperty() const;

    // Add a callback that will be called whenever the `daily_forecast` property is updated.
    // The provided method will be called whenever a new value for the `daily_forecast` property is received.
    void registerDailyForecastPropertyCallback(const std::function<void(ForecastForDay, ForecastForDay, ForecastForDay)>& cb);

    void updateDailyForecastProperty(ForecastForDay, ForecastForDay, ForecastForDay);

    // ---hourly_forecast Property---

    // Gets the latest value of the `hourly_forecast` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<struct HourlyForecastProperty> getHourlyForecastProperty() const;

    // Add a callback that will be called whenever the `hourly_forecast` property is updated.
    // The provided method will be called whenever a new value for the `hourly_forecast` property is received.
    void registerHourlyForecastPropertyCallback(const std::function<void(ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour)>& cb);

    void updateHourlyForecastProperty(ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour);

    // ---current_condition_refresh_interval Property---

    // Gets the latest value of the `current_condition_refresh_interval` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<CurrentConditionRefreshIntervalProperty> getCurrentConditionRefreshIntervalProperty() const;

    // Add a callback that will be called whenever the `current_condition_refresh_interval` property is updated.
    // The provided method will be called whenever a new value for the `current_condition_refresh_interval` property is received.
    void registerCurrentConditionRefreshIntervalPropertyCallback(const std::function<void(int)>& cb);

    void updateCurrentConditionRefreshIntervalProperty(int);

    // ---hourly_forecast_refresh_interval Property---

    // Gets the latest value of the `hourly_forecast_refresh_interval` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<HourlyForecastRefreshIntervalProperty> getHourlyForecastRefreshIntervalProperty() const;

    // Add a callback that will be called whenever the `hourly_forecast_refresh_interval` property is updated.
    // The provided method will be called whenever a new value for the `hourly_forecast_refresh_interval` property is received.
    void registerHourlyForecastRefreshIntervalPropertyCallback(const std::function<void(int)>& cb);

    void updateHourlyForecastRefreshIntervalProperty(int);

    // ---daily_forecast_refresh_interval Property---

    // Gets the latest value of the `daily_forecast_refresh_interval` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<DailyForecastRefreshIntervalProperty> getDailyForecastRefreshIntervalProperty() const;

    // Add a callback that will be called whenever the `daily_forecast_refresh_interval` property is updated.
    // The provided method will be called whenever a new value for the `daily_forecast_refresh_interval` property is received.
    void registerDailyForecastRefreshIntervalPropertyCallback(const std::function<void(int)>& cb);

    void updateDailyForecastRefreshIntervalProperty(int);

private:
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const MqttProperties& mqttProps
    );

    void _callRefreshDailyForecastHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<void()> _refreshDailyForecastHandler;
    int _refreshDailyForecastMethodSubscriptionId;

    void _callRefreshHourlyForecastHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<void()> _refreshHourlyForecastHandler;
    int _refreshHourlyForecastMethodSubscriptionId;

    void _callRefreshCurrentConditionsHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<void()> _refreshCurrentConditionsHandler;
    int _refreshCurrentConditionsMethodSubscriptionId;

    // ---------------- PROPERTIES ------------------

    // ---location Property---

    // Current values for the `location` property.
    boost::optional<struct LocationProperty> _locationProperty;

    // This is the property version  of `location`.
    int _lastLocationPropertyVersion = -1;

    // Mutex for protecting access to the `location` property and its version.
    mutable std::mutex _locationPropertyMutex;

    // MQTT Subscription ID for `location` property update requests.
    int _locationPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `location` property.
    void _receiveLocationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `location` property.
    std::vector<std::function<void(double, double)>> _locationPropertyCallbacks;
    std::mutex _locationPropertyCallbacksMutex;

    // ---current_temperature Property---

    // Current value for the `current_temperature` property.
    boost::optional<CurrentTemperatureProperty> _currentTemperatureProperty;

    // This is the property version  of `current_temperature`.
    int _lastCurrentTemperaturePropertyVersion = -1;

    // Mutex for protecting access to the `current_temperature` property and its version.
    mutable std::mutex _currentTemperaturePropertyMutex;

    // MQTT Subscription ID for `current_temperature` property update requests.
    int _currentTemperaturePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `current_temperature` property.
    void _receiveCurrentTemperaturePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `current_temperature` property.
    std::vector<std::function<void(double)>> _currentTemperaturePropertyCallbacks;
    std::mutex _currentTemperaturePropertyCallbacksMutex;

    // ---current_condition Property---

    // Current values for the `current_condition` property.
    boost::optional<struct CurrentConditionProperty> _currentConditionProperty;

    // This is the property version  of `current_condition`.
    int _lastCurrentConditionPropertyVersion = -1;

    // Mutex for protecting access to the `current_condition` property and its version.
    mutable std::mutex _currentConditionPropertyMutex;

    // MQTT Subscription ID for `current_condition` property update requests.
    int _currentConditionPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `current_condition` property.
    void _receiveCurrentConditionPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `current_condition` property.
    std::vector<std::function<void(WeatherCondition, const std::string&)>> _currentConditionPropertyCallbacks;
    std::mutex _currentConditionPropertyCallbacksMutex;

    // ---daily_forecast Property---

    // Current values for the `daily_forecast` property.
    boost::optional<struct DailyForecastProperty> _dailyForecastProperty;

    // This is the property version  of `daily_forecast`.
    int _lastDailyForecastPropertyVersion = -1;

    // Mutex for protecting access to the `daily_forecast` property and its version.
    mutable std::mutex _dailyForecastPropertyMutex;

    // MQTT Subscription ID for `daily_forecast` property update requests.
    int _dailyForecastPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `daily_forecast` property.
    void _receiveDailyForecastPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `daily_forecast` property.
    std::vector<std::function<void(ForecastForDay, ForecastForDay, ForecastForDay)>> _dailyForecastPropertyCallbacks;
    std::mutex _dailyForecastPropertyCallbacksMutex;

    // ---hourly_forecast Property---

    // Current values for the `hourly_forecast` property.
    boost::optional<struct HourlyForecastProperty> _hourlyForecastProperty;

    // This is the property version  of `hourly_forecast`.
    int _lastHourlyForecastPropertyVersion = -1;

    // Mutex for protecting access to the `hourly_forecast` property and its version.
    mutable std::mutex _hourlyForecastPropertyMutex;

    // MQTT Subscription ID for `hourly_forecast` property update requests.
    int _hourlyForecastPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `hourly_forecast` property.
    void _receiveHourlyForecastPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `hourly_forecast` property.
    std::vector<std::function<void(ForecastForHour, ForecastForHour, ForecastForHour, ForecastForHour)>> _hourlyForecastPropertyCallbacks;
    std::mutex _hourlyForecastPropertyCallbacksMutex;

    // ---current_condition_refresh_interval Property---

    // Current value for the `current_condition_refresh_interval` property.
    boost::optional<CurrentConditionRefreshIntervalProperty> _currentConditionRefreshIntervalProperty;

    // This is the property version  of `current_condition_refresh_interval`.
    int _lastCurrentConditionRefreshIntervalPropertyVersion = -1;

    // Mutex for protecting access to the `current_condition_refresh_interval` property and its version.
    mutable std::mutex _currentConditionRefreshIntervalPropertyMutex;

    // MQTT Subscription ID for `current_condition_refresh_interval` property update requests.
    int _currentConditionRefreshIntervalPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `current_condition_refresh_interval` property.
    void _receiveCurrentConditionRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `current_condition_refresh_interval` property.
    std::vector<std::function<void(int)>> _currentConditionRefreshIntervalPropertyCallbacks;
    std::mutex _currentConditionRefreshIntervalPropertyCallbacksMutex;

    // ---hourly_forecast_refresh_interval Property---

    // Current value for the `hourly_forecast_refresh_interval` property.
    boost::optional<HourlyForecastRefreshIntervalProperty> _hourlyForecastRefreshIntervalProperty;

    // This is the property version  of `hourly_forecast_refresh_interval`.
    int _lastHourlyForecastRefreshIntervalPropertyVersion = -1;

    // Mutex for protecting access to the `hourly_forecast_refresh_interval` property and its version.
    mutable std::mutex _hourlyForecastRefreshIntervalPropertyMutex;

    // MQTT Subscription ID for `hourly_forecast_refresh_interval` property update requests.
    int _hourlyForecastRefreshIntervalPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `hourly_forecast_refresh_interval` property.
    void _receiveHourlyForecastRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `hourly_forecast_refresh_interval` property.
    std::vector<std::function<void(int)>> _hourlyForecastRefreshIntervalPropertyCallbacks;
    std::mutex _hourlyForecastRefreshIntervalPropertyCallbacksMutex;

    // ---daily_forecast_refresh_interval Property---

    // Current value for the `daily_forecast_refresh_interval` property.
    boost::optional<DailyForecastRefreshIntervalProperty> _dailyForecastRefreshIntervalProperty;

    // This is the property version  of `daily_forecast_refresh_interval`.
    int _lastDailyForecastRefreshIntervalPropertyVersion = -1;

    // Mutex for protecting access to the `daily_forecast_refresh_interval` property and its version.
    mutable std::mutex _dailyForecastRefreshIntervalPropertyMutex;

    // MQTT Subscription ID for `daily_forecast_refresh_interval` property update requests.
    int _dailyForecastRefreshIntervalPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `daily_forecast_refresh_interval` property.
    void _receiveDailyForecastRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `daily_forecast_refresh_interval` property.
    std::vector<std::function<void(int)>> _dailyForecastRefreshIntervalPropertyCallbacks;
    std::mutex _dailyForecastRefreshIntervalPropertyCallbacksMutex;
};