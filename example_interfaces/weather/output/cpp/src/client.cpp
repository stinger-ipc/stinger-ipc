

#include <vector>
#include <iostream>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <syslog.h>
#include <sstream>
#include <stinger/utils/iconnection.hpp>
#include <stinger/utils/uuid.hpp>
#include <stinger/utils/format.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "client.hpp"
#include "enums.hpp"
#include "discovery.hpp"

namespace stinger {

namespace gen {
namespace weather {

constexpr const char WeatherClient::NAME[];
constexpr const char WeatherClient::INTERFACE_VERSION[];

WeatherClient::WeatherClient(std::shared_ptr<stinger::utils::IConnection> broker, const InstanceInfo& instanceInfo):
    _broker(broker), _instanceId(instanceInfo.serviceId.value_or("error_service_id_not_found")), _instanceInfo(instanceInfo)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](const stinger::mqtt::Message& msg)
                                                               {
                                                                   _receiveMessage(msg);
                                                               });

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto currentTimeTopic = stinger::utils::format("{prefix}/weather/{service_id}/signal/current_time", topicParams);
    _currentTimeSignalSubscriptionId = _broker->Subscribe(currentTimeTopic, 2);
    { // Restrict scope
        auto refreshDailyForecastRequestTopic = stinger::utils::format("{prefix}/weather/{service_id}/method/refresh_daily_forecast/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(refreshDailyForecastRequestTopic, topicParams);
        _refreshDailyForecastMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto refreshHourlyForecastRequestTopic = stinger::utils::format("{prefix}/weather/{service_id}/method/refresh_hourly_forecast/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(refreshHourlyForecastRequestTopic, topicParams);
        _refreshHourlyForecastMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto refreshCurrentConditionsRequestTopic = stinger::utils::format("{prefix}/weather/{service_id}/method/refresh_current_conditions/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(refreshCurrentConditionsRequestTopic, topicParams);
        _refreshCurrentConditionsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    auto locationValueTopic = stinger::utils::format("{prefix}/weather/{service_id}/property/location/value", topicParams);
    _locationPropertySubscriptionId = _broker->Subscribe(locationValueTopic, 1);
    auto currentTemperatureValueTopic = stinger::utils::format("{prefix}/weather/{service_id}/property/current_temperature/value", topicParams);
    _currentTemperaturePropertySubscriptionId = _broker->Subscribe(currentTemperatureValueTopic, 1);
    auto currentConditionValueTopic = stinger::utils::format("{prefix}/weather/{service_id}/property/current_condition/value", topicParams);
    _currentConditionPropertySubscriptionId = _broker->Subscribe(currentConditionValueTopic, 1);
    auto dailyForecastValueTopic = stinger::utils::format("{prefix}/weather/{service_id}/property/daily_forecast/value", topicParams);
    _dailyForecastPropertySubscriptionId = _broker->Subscribe(dailyForecastValueTopic, 1);
    auto hourlyForecastValueTopic = stinger::utils::format("{prefix}/weather/{service_id}/property/hourly_forecast/value", topicParams);
    _hourlyForecastPropertySubscriptionId = _broker->Subscribe(hourlyForecastValueTopic, 1);
    auto currentConditionRefreshIntervalValueTopic = stinger::utils::format("{prefix}/weather/{service_id}/property/current_condition_refresh_interval/value", topicParams);
    _currentConditionRefreshIntervalPropertySubscriptionId = _broker->Subscribe(currentConditionRefreshIntervalValueTopic, 1);
    auto hourlyForecastRefreshIntervalValueTopic = stinger::utils::format("{prefix}/weather/{service_id}/property/hourly_forecast_refresh_interval/value", topicParams);
    _hourlyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe(hourlyForecastRefreshIntervalValueTopic, 1);
    auto dailyForecastRefreshIntervalValueTopic = stinger::utils::format("{prefix}/weather/{service_id}/property/daily_forecast_refresh_interval/value", topicParams);
    _dailyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe(dailyForecastRefreshIntervalValueTopic, 1);

    auto anyPropertyUpdateResponseTopic = stinger::utils::format("client/{client_id}/weather/property/+/update/response", topicParams);
    _anyPropertyUpdateResponseSubscriptionId = _broker->Subscribe(anyPropertyUpdateResponseTopic, 1);
}

WeatherClient::~WeatherClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void WeatherClient::_receiveMessage(const stinger::mqtt::Message& msg)
{
    const int noSubId = -1;
    int subscriptionId = msg.properties.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", msg.topic.c_str(), subscriptionId);
    if (subscriptionId == _currentTimeSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling current_time signal");
        rapidjson::Document doc;
        try {
            if (_currentTimeSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse current_time signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::string tempCurrentTime;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("current_time");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempCurrentTime = itr->value.GetString();

                    } else {
                        throw std::runtime_error("Received payload for 'current_time' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_currentTimeSignalCallbacksMutex);
                for (const auto& cb: _currentTimeSignalCallbacks) {
                    cb(tempCurrentTime);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _refreshDailyForecastMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for refresh_daily_forecast response");
        _handleRefreshDailyForecastResponse(msg);
    } else if (subscriptionId == _refreshHourlyForecastMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for refresh_hourly_forecast response");
        _handleRefreshHourlyForecastResponse(msg);
    } else if (subscriptionId == _refreshCurrentConditionsMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for refresh_current_conditions response");
        _handleRefreshCurrentConditionsResponse(msg);
    }
    if (subscriptionId == _locationPropertySubscriptionId) {
        _receiveLocationPropertyUpdate(msg);
    } else if (subscriptionId == _currentTemperaturePropertySubscriptionId) {
        _receiveCurrentTemperaturePropertyUpdate(msg);
    } else if (subscriptionId == _currentConditionPropertySubscriptionId) {
        _receiveCurrentConditionPropertyUpdate(msg);
    } else if (subscriptionId == _dailyForecastPropertySubscriptionId) {
        _receiveDailyForecastPropertyUpdate(msg);
    } else if (subscriptionId == _hourlyForecastPropertySubscriptionId) {
        _receiveHourlyForecastPropertyUpdate(msg);
    } else if (subscriptionId == _currentConditionRefreshIntervalPropertySubscriptionId) {
        _receiveCurrentConditionRefreshIntervalPropertyUpdate(msg);
    } else if (subscriptionId == _hourlyForecastRefreshIntervalPropertySubscriptionId) {
        _receiveHourlyForecastRefreshIntervalPropertyUpdate(msg);
    } else if (subscriptionId == _dailyForecastRefreshIntervalPropertySubscriptionId) {
        _receiveDailyForecastRefreshIntervalPropertyUpdate(msg);
    } else if (subscriptionId == _anyPropertyUpdateResponseSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for any property update response");
    }
}

void WeatherClient::registerCurrentTimeCallback(const std::function<void(std::string)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentTimeSignalCallbacksMutex);
    _currentTimeSignalCallbacks.push_back(cb);
}

std::future<void> WeatherClient::refreshDailyForecast()
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingRefreshDailyForecastMethodCalls[correlationData] = std::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/weather/method/refresh_daily_forecast/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/weather/{service_id}/method/refresh_daily_forecast/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingRefreshDailyForecastMethodCalls[correlationData].get_future();
}

void WeatherClient::_handleRefreshDailyForecastResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for refresh_daily_forecast");

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingRefreshDailyForecastMethodCalls.find(correlationData);
    if (promiseItr != _pendingRefreshDailyForecastMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method doesn't have any return values.
        promiseItr->second.set_value();
    }

    _broker->Log(LOG_DEBUG, "End of response handler for refresh_daily_forecast");
}

std::future<void> WeatherClient::refreshHourlyForecast()
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingRefreshHourlyForecastMethodCalls[correlationData] = std::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/weather/method/refresh_hourly_forecast/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/weather/{service_id}/method/refresh_hourly_forecast/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingRefreshHourlyForecastMethodCalls[correlationData].get_future();
}

void WeatherClient::_handleRefreshHourlyForecastResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for refresh_hourly_forecast");

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingRefreshHourlyForecastMethodCalls.find(correlationData);
    if (promiseItr != _pendingRefreshHourlyForecastMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method doesn't have any return values.
        promiseItr->second.set_value();
    }

    _broker->Log(LOG_DEBUG, "End of response handler for refresh_hourly_forecast");
}

std::future<void> WeatherClient::refreshCurrentConditions()
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingRefreshCurrentConditionsMethodCalls[correlationData] = std::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/weather/method/refresh_current_conditions/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/weather/{service_id}/method/refresh_current_conditions/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingRefreshCurrentConditionsMethodCalls[correlationData].get_future();
}

void WeatherClient::_handleRefreshCurrentConditionsResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for refresh_current_conditions");

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingRefreshCurrentConditionsMethodCalls.find(correlationData);
    if (promiseItr != _pendingRefreshCurrentConditionsMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method doesn't have any return values.
        promiseItr->second.set_value();
    }

    _broker->Log(LOG_DEBUG, "End of response handler for refresh_current_conditions");
}

void WeatherClient::_receiveLocationPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse location property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'location' property update payload is not an object");
    }
    LocationProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("latitude");
        if (itr != doc.MemberEnd() && itr->value.IsDouble()) {
            tempValue.latitude = itr->value.GetDouble();

        } else {
            throw std::runtime_error("Received payload for the 'latitude' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("longitude");
        if (itr != doc.MemberEnd() && itr->value.IsDouble()) {
            tempValue.longitude = itr->value.GetDouble();

        } else {
            throw std::runtime_error("Received payload for the 'longitude' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_locationPropertyMutex);
        _locationProperty = tempValue;
        _lastLocationPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_locationPropertyCallbacksMutex);
        for (const auto& cb: _locationPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.latitude, tempValue.longitude);
        }
    }
}

std::optional<LocationProperty> WeatherClient::getLocationProperty()
{
    std::lock_guard<std::mutex> lock(_locationPropertyMutex);
    if (_locationProperty) {
        return *_locationProperty;
    }
    return std::nullopt;
}

void WeatherClient::registerLocationPropertyCallback(const std::function<void(double latitude, double longitude)>& cb)
{
    std::lock_guard<std::mutex> lock(_locationPropertyCallbacksMutex);
    _locationPropertyCallbacks.push_back(cb);
}

std::future<bool> WeatherClient::updateLocationProperty(double latitude, double longitude) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("latitude", latitude, doc.GetAllocator());

    doc.AddMember("longitude", longitude, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/weather/{service_id}/property/location/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/weather/property/location/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastLocationPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void WeatherClient::_receiveCurrentTemperaturePropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse current_temperature property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'current_temperature' property update payload is not an object");
    }
    CurrentTemperatureProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("temperature_f");
        if (itr != doc.MemberEnd() && itr->value.IsDouble()) {
            tempValue.temperatureF = itr->value.GetDouble();

        } else {
            throw std::runtime_error("Received payload for the 'temperature_f' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
        _currentTemperatureProperty = tempValue;
        _lastCurrentTemperaturePropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyCallbacksMutex);
        for (const auto& cb: _currentTemperaturePropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.temperatureF);
        }
    }
}

std::optional<double> WeatherClient::getCurrentTemperatureProperty()
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
    if (_currentTemperatureProperty) {
        return _currentTemperatureProperty->temperatureF;
    }
    return std::nullopt;
}

void WeatherClient::registerCurrentTemperaturePropertyCallback(const std::function<void(double temperatureF)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyCallbacksMutex);
    _currentTemperaturePropertyCallbacks.push_back(cb);
}

void WeatherClient::_receiveCurrentConditionPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse current_condition property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'current_condition' property update payload is not an object");
    }
    CurrentConditionProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("condition");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.condition = static_cast<WeatherCondition>(itr->value.GetInt());

        } else {
            throw std::runtime_error("Received payload for the 'condition' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("description");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.description = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'description' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
        _currentConditionProperty = tempValue;
        _lastCurrentConditionPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionPropertyCallbacksMutex);
        for (const auto& cb: _currentConditionPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.condition, tempValue.description);
        }
    }
}

std::optional<CurrentConditionProperty> WeatherClient::getCurrentConditionProperty()
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
    if (_currentConditionProperty) {
        return *_currentConditionProperty;
    }
    return std::nullopt;
}

void WeatherClient::registerCurrentConditionPropertyCallback(const std::function<void(WeatherCondition condition, std::string description)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyCallbacksMutex);
    _currentConditionPropertyCallbacks.push_back(cb);
}

void WeatherClient::_receiveDailyForecastPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse daily_forecast property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'daily_forecast' property update payload is not an object");
    }
    DailyForecastProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("monday");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.monday = ForecastForDay::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'monday' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("tuesday");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.tuesday = ForecastForDay::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'tuesday' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("wednesday");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.wednesday = ForecastForDay::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'wednesday' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
        _dailyForecastProperty = tempValue;
        _lastDailyForecastPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastPropertyCallbacksMutex);
        for (const auto& cb: _dailyForecastPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.monday, tempValue.tuesday, tempValue.wednesday);
        }
    }
}

std::optional<DailyForecastProperty> WeatherClient::getDailyForecastProperty()
{
    std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
    if (_dailyForecastProperty) {
        return *_dailyForecastProperty;
    }
    return std::nullopt;
}

void WeatherClient::registerDailyForecastPropertyCallback(const std::function<void(ForecastForDay monday, ForecastForDay tuesday, ForecastForDay wednesday)>& cb)
{
    std::lock_guard<std::mutex> lock(_dailyForecastPropertyCallbacksMutex);
    _dailyForecastPropertyCallbacks.push_back(cb);
}

void WeatherClient::_receiveHourlyForecastPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse hourly_forecast property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'hourly_forecast' property update payload is not an object");
    }
    HourlyForecastProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_0");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.hour0 = ForecastForHour::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'hour_0' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_1");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.hour1 = ForecastForHour::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'hour_1' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_2");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.hour2 = ForecastForHour::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'hour_2' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_3");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.hour3 = ForecastForHour::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'hour_3' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
        _hourlyForecastProperty = tempValue;
        _lastHourlyForecastPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyCallbacksMutex);
        for (const auto& cb: _hourlyForecastPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.hour0, tempValue.hour1, tempValue.hour2, tempValue.hour3);
        }
    }
}

std::optional<HourlyForecastProperty> WeatherClient::getHourlyForecastProperty()
{
    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
    if (_hourlyForecastProperty) {
        return *_hourlyForecastProperty;
    }
    return std::nullopt;
}

void WeatherClient::registerHourlyForecastPropertyCallback(const std::function<void(ForecastForHour hour0, ForecastForHour hour1, ForecastForHour hour2, ForecastForHour hour3)>& cb)
{
    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyCallbacksMutex);
    _hourlyForecastPropertyCallbacks.push_back(cb);
}

void WeatherClient::_receiveCurrentConditionRefreshIntervalPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse current_condition_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'current_condition_refresh_interval' property update payload is not an object");
    }
    CurrentConditionRefreshIntervalProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.seconds = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'seconds' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
        _currentConditionRefreshIntervalProperty = tempValue;
        _lastCurrentConditionRefreshIntervalPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _currentConditionRefreshIntervalPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.seconds);
        }
    }
}

std::optional<int> WeatherClient::getCurrentConditionRefreshIntervalProperty()
{
    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
    if (_currentConditionRefreshIntervalProperty) {
        return _currentConditionRefreshIntervalProperty->seconds;
    }
    return std::nullopt;
}

void WeatherClient::registerCurrentConditionRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyCallbacksMutex);
    _currentConditionRefreshIntervalPropertyCallbacks.push_back(cb);
}

std::future<bool> WeatherClient::updateCurrentConditionRefreshIntervalProperty(int seconds) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("seconds", seconds, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/weather/{service_id}/property/current_condition_refresh_interval/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/weather/property/current_condition_refresh_interval/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastCurrentConditionRefreshIntervalPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void WeatherClient::_receiveHourlyForecastRefreshIntervalPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse hourly_forecast_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'hourly_forecast_refresh_interval' property update payload is not an object");
    }
    HourlyForecastRefreshIntervalProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.seconds = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'seconds' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
        _hourlyForecastRefreshIntervalProperty = tempValue;
        _lastHourlyForecastRefreshIntervalPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _hourlyForecastRefreshIntervalPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.seconds);
        }
    }
}

std::optional<int> WeatherClient::getHourlyForecastRefreshIntervalProperty()
{
    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
    if (_hourlyForecastRefreshIntervalProperty) {
        return _hourlyForecastRefreshIntervalProperty->seconds;
    }
    return std::nullopt;
}

void WeatherClient::registerHourlyForecastRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyCallbacksMutex);
    _hourlyForecastRefreshIntervalPropertyCallbacks.push_back(cb);
}

std::future<bool> WeatherClient::updateHourlyForecastRefreshIntervalProperty(int seconds) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("seconds", seconds, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/weather/{service_id}/property/hourly_forecast_refresh_interval/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/weather/property/hourly_forecast_refresh_interval/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastHourlyForecastRefreshIntervalPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void WeatherClient::_receiveDailyForecastRefreshIntervalPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse daily_forecast_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'daily_forecast_refresh_interval' property update payload is not an object");
    }
    DailyForecastRefreshIntervalProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.seconds = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'seconds' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
        _dailyForecastRefreshIntervalProperty = tempValue;
        _lastDailyForecastRefreshIntervalPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _dailyForecastRefreshIntervalPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.seconds);
        }
    }
}

std::optional<int> WeatherClient::getDailyForecastRefreshIntervalProperty()
{
    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
    if (_dailyForecastRefreshIntervalProperty) {
        return _dailyForecastRefreshIntervalProperty->seconds;
    }
    return std::nullopt;
}

void WeatherClient::registerDailyForecastRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyCallbacksMutex);
    _dailyForecastRefreshIntervalPropertyCallbacks.push_back(cb);
}

std::future<bool> WeatherClient::updateDailyForecastRefreshIntervalProperty(int seconds) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("seconds", seconds, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/weather/{service_id}/property/daily_forecast_refresh_interval/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/weather/property/daily_forecast_refresh_interval/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastDailyForecastRefreshIntervalPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

} // namespace weather

} // namespace gen

} // namespace stinger
