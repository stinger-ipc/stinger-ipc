

#include <vector>
#include <iostream>
#include <chrono>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>

#include "client.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"

constexpr const char WeatherClient::NAME[];
constexpr const char WeatherClient::INTERFACE_VERSION[];

WeatherClient::WeatherClient(std::shared_ptr<IBrokerConnection> broker)
    : _broker(broker)
{
    _broker->AddMessageCallback([this](
                                        const std::string& topic,
                                        const std::string& payload,
                                        const MqttProperties& mqttProps
                                )
                                { _receiveMessage(topic, payload, mqttProps); });
    _currentTimeSignalSubscriptionId = _broker->Subscribe("weather/signal/currentTime", 2);
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/weather/method/refreshDailyForecast/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/weather/method/refreshHourlyForecast/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/weather/method/refreshCurrentConditions/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    _locationPropertySubscriptionId = _broker->Subscribe("weather/property/location/value", 1);
    _currentTemperaturePropertySubscriptionId = _broker->Subscribe("weather/property/currentTemperature/value", 1);
    _currentConditionPropertySubscriptionId = _broker->Subscribe("weather/property/currentCondition/value", 1);
    _dailyForecastPropertySubscriptionId = _broker->Subscribe("weather/property/dailyForecast/value", 1);
    _hourlyForecastPropertySubscriptionId = _broker->Subscribe("weather/property/hourlyForecast/value", 1);
    _currentConditionRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/currentConditionRefreshInterval/value", 1);
    _hourlyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/hourlyForecastRefreshInterval/value", 1);
    _dailyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/dailyForecastRefreshInterval/value", 1);
}

void WeatherClient::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _currentTimeSignalSubscriptionId)) || _broker->TopicMatchesSubscription(topic, "weather/signal/currentTime"))
    {
        //Log("Handling current_time signal");
        rapidjson::Document doc;
        try
        {
            if (_currentTimeSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse current_time signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
                }

                std::string tempCurrentTime;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("current_time");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempCurrentTime = itr->value.GetString();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_currentTimeSignalCallbacksMutex);
                for (const auto& cb: _currentTimeSignalCallbacks)
                {
                    cb(tempCurrentTime);
                }
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (_broker->TopicMatchesSubscription(topic, "client/+/weather/method/refreshDailyForecast/response") && mqttProps.correlationId)
    {
        std::cout << "Matched topic for refresh_daily_forecast response" << std::endl;
        _handleRefreshDailyForecastResponse(topic, payload, *mqttProps.correlationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/weather/method/refreshHourlyForecast/response") && mqttProps.correlationId)
    {
        std::cout << "Matched topic for refresh_hourly_forecast response" << std::endl;
        _handleRefreshHourlyForecastResponse(topic, payload, *mqttProps.correlationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/weather/method/refreshCurrentConditions/response") && mqttProps.correlationId)
    {
        std::cout << "Matched topic for refresh_current_conditions response" << std::endl;
        _handleRefreshCurrentConditionsResponse(topic, payload, *mqttProps.correlationId);
    }
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _locationPropertySubscriptionId)) || topic == "weather/property/location/value")
    {
        _receiveLocationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _currentTemperaturePropertySubscriptionId)) || topic == "weather/property/currentTemperature/value")
    {
        _receiveCurrentTemperaturePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _currentConditionPropertySubscriptionId)) || topic == "weather/property/currentCondition/value")
    {
        _receiveCurrentConditionPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _dailyForecastPropertySubscriptionId)) || topic == "weather/property/dailyForecast/value")
    {
        _receiveDailyForecastPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _hourlyForecastPropertySubscriptionId)) || topic == "weather/property/hourlyForecast/value")
    {
        _receiveHourlyForecastPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _currentConditionRefreshIntervalPropertySubscriptionId)) || topic == "weather/property/currentConditionRefreshInterval/value")
    {
        _receiveCurrentConditionRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _hourlyForecastRefreshIntervalPropertySubscriptionId)) || topic == "weather/property/hourlyForecastRefreshInterval/value")
    {
        _receiveHourlyForecastRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _dailyForecastRefreshIntervalPropertySubscriptionId)) || topic == "weather/property/dailyForecastRefreshInterval/value")
    {
        _receiveDailyForecastRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

void WeatherClient::registerCurrentTimeCallback(const std::function<void(const std::string&)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentTimeSignalCallbacksMutex);
    _currentTimeSignalCallbacks.push_back(cb);
}

boost::future<void> WeatherClient::refreshDailyForecast()
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingRefreshDailyForecastMethodCalls[correlationId] = boost::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/weather/method/refreshDailyForecast/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish("weather/method/refreshDailyForecast", buf.GetString(), 2, false, mqttProps);

    return _pendingRefreshDailyForecastMethodCalls[correlationId].get_future();
}

void WeatherClient::_handleRefreshDailyForecastResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingRefreshDailyForecastMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingRefreshDailyForecastMethodCalls.end())
    {
        // There are no values in the response.
        promiseItr->second.set_value();
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

boost::future<void> WeatherClient::refreshHourlyForecast()
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingRefreshHourlyForecastMethodCalls[correlationId] = boost::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/weather/method/refreshHourlyForecast/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish("weather/method/refreshHourlyForecast", buf.GetString(), 2, false, mqttProps);

    return _pendingRefreshHourlyForecastMethodCalls[correlationId].get_future();
}

void WeatherClient::_handleRefreshHourlyForecastResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingRefreshHourlyForecastMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingRefreshHourlyForecastMethodCalls.end())
    {
        // There are no values in the response.
        promiseItr->second.set_value();
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

boost::future<void> WeatherClient::refreshCurrentConditions()
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingRefreshCurrentConditionsMethodCalls[correlationId] = boost::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/weather/method/refreshCurrentConditions/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish("weather/method/refreshCurrentConditions", buf.GetString(), 2, false, mqttProps);

    return _pendingRefreshCurrentConditionsMethodCalls[correlationId].get_future();
}

void WeatherClient::_handleRefreshCurrentConditionsResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingRefreshCurrentConditionsMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingRefreshCurrentConditionsMethodCalls.end())
    {
        // There are no values in the response.
        promiseItr->second.set_value();
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

void WeatherClient::_receiveLocationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse location property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received location payload is not an object");
    }
    LocationProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("latitude");
        if (itr != doc.MemberEnd() && itr->value.IsDouble())
        {
            tempValue.latitude = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("longitude");
        if (itr != doc.MemberEnd() && itr->value.IsDouble())
        {
            tempValue.longitude = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_locationPropertyMutex);
        _locationProperty = tempValue;
        _lastLocationPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_locationPropertyCallbacksMutex);
        for (const auto& cb: _locationPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue.latitude, tempValue.longitude);
        }
    }
}

boost::optional<LocationProperty> WeatherClient::getLocationProperty() const
{
    std::lock_guard<std::mutex> lock(_locationPropertyMutex);
    return _locationProperty;
}

void WeatherClient::registerLocationPropertyCallback(const std::function<void(double latitude, double longitude)>& cb)
{
    std::lock_guard<std::mutex> lock(_locationPropertyCallbacksMutex);
    _locationPropertyCallbacks.push_back(cb);
}

boost::future<bool> WeatherClient::updateLocationProperty(double latitude, double longitude) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("latitude", latitude, doc.GetAllocator());

    doc.AddMember("longitude", longitude, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("weather/property/location/setValue", buf.GetString(), 1, false, mqttProps);
}

void WeatherClient::_receiveCurrentTemperaturePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse current_temperature property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received current_temperature payload is not an object");
    }
    CurrentTemperatureProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("temperature_f");
    if (itr != doc.MemberEnd() && itr->value.IsDouble())
    {
        tempValue = itr->value.GetDouble();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
        _currentTemperatureProperty = tempValue;
        _lastCurrentTemperaturePropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyCallbacksMutex);
        for (const auto& cb: _currentTemperaturePropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue);
        }
    }
}

boost::optional<CurrentTemperatureProperty> WeatherClient::getCurrentTemperatureProperty() const
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
    return _currentTemperatureProperty;
}

void WeatherClient::registerCurrentTemperaturePropertyCallback(const std::function<void(double temperature_f)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyCallbacksMutex);
    _currentTemperaturePropertyCallbacks.push_back(cb);
}

void WeatherClient::_receiveCurrentConditionPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse current_condition property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received current_condition payload is not an object");
    }
    CurrentConditionProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("condition");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.condition = static_cast<WeatherCondition>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("description");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.description = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
        _currentConditionProperty = tempValue;
        _lastCurrentConditionPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionPropertyCallbacksMutex);
        for (const auto& cb: _currentConditionPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue.condition, tempValue.description);
        }
    }
}

boost::optional<CurrentConditionProperty> WeatherClient::getCurrentConditionProperty() const
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
    return _currentConditionProperty;
}

void WeatherClient::registerCurrentConditionPropertyCallback(const std::function<void(WeatherCondition condition, const std::string& description)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyCallbacksMutex);
    _currentConditionPropertyCallbacks.push_back(cb);
}

void WeatherClient::_receiveDailyForecastPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse daily_forecast property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received daily_forecast payload is not an object");
    }
    DailyForecastProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("monday");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.monday = ForecastForDay::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("tuesday");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.tuesday = ForecastForDay::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("wednesday");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.wednesday = ForecastForDay::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
        _dailyForecastProperty = tempValue;
        _lastDailyForecastPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastPropertyCallbacksMutex);
        for (const auto& cb: _dailyForecastPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue.monday, tempValue.tuesday, tempValue.wednesday);
        }
    }
}

boost::optional<DailyForecastProperty> WeatherClient::getDailyForecastProperty() const
{
    std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
    return _dailyForecastProperty;
}

void WeatherClient::registerDailyForecastPropertyCallback(const std::function<void(ForecastForDay monday, ForecastForDay tuesday, ForecastForDay wednesday)>& cb)
{
    std::lock_guard<std::mutex> lock(_dailyForecastPropertyCallbacksMutex);
    _dailyForecastPropertyCallbacks.push_back(cb);
}

void WeatherClient::_receiveHourlyForecastPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse hourly_forecast property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received hourly_forecast payload is not an object");
    }
    HourlyForecastProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_0");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.hour_0 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_1");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.hour_1 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_2");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.hour_2 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_3");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.hour_3 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
        _hourlyForecastProperty = tempValue;
        _lastHourlyForecastPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyCallbacksMutex);
        for (const auto& cb: _hourlyForecastPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue.hour_0, tempValue.hour_1, tempValue.hour_2, tempValue.hour_3);
        }
    }
}

boost::optional<HourlyForecastProperty> WeatherClient::getHourlyForecastProperty() const
{
    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
    return _hourlyForecastProperty;
}

void WeatherClient::registerHourlyForecastPropertyCallback(const std::function<void(ForecastForHour hour_0, ForecastForHour hour_1, ForecastForHour hour_2, ForecastForHour hour_3)>& cb)
{
    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyCallbacksMutex);
    _hourlyForecastPropertyCallbacks.push_back(cb);
}

void WeatherClient::_receiveCurrentConditionRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse current_condition_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received current_condition_refresh_interval payload is not an object");
    }
    CurrentConditionRefreshIntervalProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
        _currentConditionRefreshIntervalProperty = tempValue;
        _lastCurrentConditionRefreshIntervalPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _currentConditionRefreshIntervalPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue);
        }
    }
}

boost::optional<CurrentConditionRefreshIntervalProperty> WeatherClient::getCurrentConditionRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
    return _currentConditionRefreshIntervalProperty;
}

void WeatherClient::registerCurrentConditionRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyCallbacksMutex);
    _currentConditionRefreshIntervalPropertyCallbacks.push_back(cb);
}

boost::future<bool> WeatherClient::updateCurrentConditionRefreshIntervalProperty(int seconds) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("seconds", seconds, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("weather/property/currentConditionRefreshInterval/setValue", buf.GetString(), 1, false, mqttProps);
}

void WeatherClient::_receiveHourlyForecastRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse hourly_forecast_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received hourly_forecast_refresh_interval payload is not an object");
    }
    HourlyForecastRefreshIntervalProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
        _hourlyForecastRefreshIntervalProperty = tempValue;
        _lastHourlyForecastRefreshIntervalPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _hourlyForecastRefreshIntervalPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue);
        }
    }
}

boost::optional<HourlyForecastRefreshIntervalProperty> WeatherClient::getHourlyForecastRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
    return _hourlyForecastRefreshIntervalProperty;
}

void WeatherClient::registerHourlyForecastRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyCallbacksMutex);
    _hourlyForecastRefreshIntervalPropertyCallbacks.push_back(cb);
}

boost::future<bool> WeatherClient::updateHourlyForecastRefreshIntervalProperty(int seconds) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("seconds", seconds, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("weather/property/hourlyForecastRefreshInterval/setValue", buf.GetString(), 1, false, mqttProps);
}

void WeatherClient::_receiveDailyForecastRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse daily_forecast_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received daily_forecast_refresh_interval payload is not an object");
    }
    DailyForecastRefreshIntervalProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
        _dailyForecastRefreshIntervalProperty = tempValue;
        _lastDailyForecastRefreshIntervalPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _dailyForecastRefreshIntervalPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue);
        }
    }
}

boost::optional<DailyForecastRefreshIntervalProperty> WeatherClient::getDailyForecastRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
    return _dailyForecastRefreshIntervalProperty;
}

void WeatherClient::registerDailyForecastRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyCallbacksMutex);
    _dailyForecastRefreshIntervalPropertyCallbacks.push_back(cb);
}

boost::future<bool> WeatherClient::updateDailyForecastRefreshIntervalProperty(int seconds) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("seconds", seconds, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("weather/property/dailyForecastRefreshInterval/setValue", buf.GetString(), 1, false, mqttProps);
}
