

#include <vector>
#include <iostream>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>

#include "server.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"

constexpr const char WeatherServer::NAME[];
constexpr const char WeatherServer::INTERFACE_VERSION[];

WeatherServer::WeatherServer(std::shared_ptr<IBrokerConnection> broker)
    : _broker(broker)
{
    _broker->AddMessageCallback([this](
                                        const std::string& topic,
                                        const std::string& payload,
                                        const MqttProperties& mqttProps
                                )
                                { _receiveMessage(topic, payload, mqttProps); });

    _refreshDailyForecastMethodSubscriptionId = _broker->Subscribe("weather/{}/method/refreshDailyForecast", 2);
    _refreshHourlyForecastMethodSubscriptionId = _broker->Subscribe("weather/{}/method/refreshHourlyForecast", 2);
    _refreshCurrentConditionsMethodSubscriptionId = _broker->Subscribe("weather/{}/method/refreshCurrentConditions", 2);

    _locationPropertySubscriptionId = _broker->Subscribe("weather/{}/property/location/setValue", 1);
    _currentTemperaturePropertySubscriptionId = _broker->Subscribe("weather/{}/property/currentTemperature/setValue", 1);
    _currentConditionPropertySubscriptionId = _broker->Subscribe("weather/{}/property/currentCondition/setValue", 1);
    _dailyForecastPropertySubscriptionId = _broker->Subscribe("weather/{}/property/dailyForecast/setValue", 1);
    _hourlyForecastPropertySubscriptionId = _broker->Subscribe("weather/{}/property/hourlyForecast/setValue", 1);
    _currentConditionRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/{}/property/currentConditionRefreshInterval/setValue", 1);
    _hourlyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/{}/property/hourlyForecastRefreshInterval/setValue", 1);
    _dailyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/{}/property/dailyForecastRefreshInterval/setValue", 1);
}

void WeatherServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    int subscriptionId = mqttProps.subscriptionId.value_or(-1);

    if ((subscriptionId == _refreshDailyForecastMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "weather/{}/method/refreshDailyForecast"))
    {
        std::cout << "Message matched topic weather/{}/method/refreshDailyForecast\n";
        rapidjson::Document doc;
        try
        {
            if (_refreshDailyForecastHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callRefreshDailyForecastHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _refreshHourlyForecastMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "weather/{}/method/refreshHourlyForecast"))
    {
        std::cout << "Message matched topic weather/{}/method/refreshHourlyForecast\n";
        rapidjson::Document doc;
        try
        {
            if (_refreshHourlyForecastHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callRefreshHourlyForecastHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _refreshCurrentConditionsMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "weather/{}/method/refreshCurrentConditions"))
    {
        std::cout << "Message matched topic weather/{}/method/refreshCurrentConditions\n";
        rapidjson::Document doc;
        try
        {
            if (_refreshCurrentConditionsHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callRefreshCurrentConditionsHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    if (subscriptionId == _locationPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/{}/property/location/setValue"))
    {
        std::cout << "Message matched topic weather/{}/property/location/setValue\n";
        _receiveLocationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentTemperaturePropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/{}/property/currentTemperature/setValue"))
    {
        std::cout << "Message matched topic weather/{}/property/currentTemperature/setValue\n";
        _receiveCurrentTemperaturePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentConditionPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/{}/property/currentCondition/setValue"))
    {
        std::cout << "Message matched topic weather/{}/property/currentCondition/setValue\n";
        _receiveCurrentConditionPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _dailyForecastPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/{}/property/dailyForecast/setValue"))
    {
        std::cout << "Message matched topic weather/{}/property/dailyForecast/setValue\n";
        _receiveDailyForecastPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _hourlyForecastPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/{}/property/hourlyForecast/setValue"))
    {
        std::cout << "Message matched topic weather/{}/property/hourlyForecast/setValue\n";
        _receiveHourlyForecastPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentConditionRefreshIntervalPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/{}/property/currentConditionRefreshInterval/setValue"))
    {
        std::cout << "Message matched topic weather/{}/property/currentConditionRefreshInterval/setValue\n";
        _receiveCurrentConditionRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _hourlyForecastRefreshIntervalPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/{}/property/hourlyForecastRefreshInterval/setValue"))
    {
        std::cout << "Message matched topic weather/{}/property/hourlyForecastRefreshInterval/setValue\n";
        _receiveHourlyForecastRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _dailyForecastRefreshIntervalPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/{}/property/dailyForecastRefreshInterval/setValue"))
    {
        std::cout << "Message matched topic weather/{}/property/dailyForecastRefreshInterval/setValue\n";
        _receiveDailyForecastRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

boost::future<bool> WeatherServer::emitCurrentTimeSignal(const std::string& current_time)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(current_time.c_str(), current_time.size(), doc.GetAllocator());
        doc.AddMember("current_time", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("weather/{}/signal/currentTime", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::registerRefreshDailyForecastHandler(std::function<void()> func)
{
    std::cout << "Registered method to handle weather/{}/method/refreshDailyForecast\n";
    _refreshDailyForecastHandler = func;
}

void WeatherServer::registerRefreshHourlyForecastHandler(std::function<void()> func)
{
    std::cout << "Registered method to handle weather/{}/method/refreshHourlyForecast\n";
    _refreshHourlyForecastHandler = func;
}

void WeatherServer::registerRefreshCurrentConditionsHandler(std::function<void()> func)
{
    std::cout << "Registered method to handle weather/{}/method/refreshCurrentConditions\n";
    _refreshCurrentConditionsHandler = func;
}

void WeatherServer::_callRefreshDailyForecastHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    std::cout << "Handling call to refresh_daily_forecast\n";
    if (_refreshDailyForecastHandler)
    {
        _refreshDailyForecastHandler();

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void WeatherServer::_callRefreshHourlyForecastHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    std::cout << "Handling call to refresh_hourly_forecast\n";
    if (_refreshHourlyForecastHandler)
    {
        _refreshHourlyForecastHandler();

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void WeatherServer::_callRefreshCurrentConditionsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    std::cout << "Handling call to refresh_current_conditions\n";
    if (_refreshCurrentConditionsHandler)
    {
        _refreshCurrentConditionsHandler();

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

boost::optional<LocationProperty> WeatherServer::getLocationProperty() const
{
    std::lock_guard<std::mutex> lock(_locationPropertyMutex);
    return _locationProperty;
}

void WeatherServer::registerLocationPropertyCallback(const std::function<void(double latitude, double longitude)>& cb)
{
    std::lock_guard<std::mutex> lock(_locationPropertyCallbacksMutex);
    _locationPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateLocationProperty(double latitude, double longitude)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_locationPropertyMutex);
        _locationProperty = LocationProperty{ latitude, longitude };
        _lastLocationPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_locationPropertyCallbacksMutex);
        for (const auto& cb: _locationPropertyCallbacks)
        {
            cb(latitude, longitude);
        }
    }
    republishLocationProperty();
}

void WeatherServer::republishLocationProperty() const
{
    std::lock_guard<std::mutex> lock(_locationPropertyMutex);
    rapidjson::Document doc;
    if (_locationProperty)
    {
        doc.SetObject();

        _locationProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastLocationPropertyVersion;
    _broker->Publish("weather/{}/property/location/value", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::_receiveLocationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse location property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received location payload is not an object or null");
    }

    // TODO: Check _lastLocationPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    LocationProperty tempValue = LocationProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_locationPropertyMutex);
        _locationProperty = tempValue;
        _lastLocationPropertyVersion++;
    }
    republishLocationProperty();
}

boost::optional<CurrentTemperatureProperty> WeatherServer::getCurrentTemperatureProperty() const
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
    return _currentTemperatureProperty;
}

void WeatherServer::registerCurrentTemperaturePropertyCallback(const std::function<void(double temperature_f)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyCallbacksMutex);
    _currentTemperaturePropertyCallbacks.push_back(cb);
}

void WeatherServer::updateCurrentTemperatureProperty(double temperature_f)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
        _currentTemperatureProperty = temperature_f;
        _lastCurrentTemperaturePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyCallbacksMutex);
        for (const auto& cb: _currentTemperaturePropertyCallbacks)
        {
            cb(temperature_f);
        }
    }
    republishCurrentTemperatureProperty();
}

void WeatherServer::republishCurrentTemperatureProperty() const
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
    rapidjson::Document doc;
    if (_currentTemperatureProperty)
    {
        doc.SetObject();

        doc.AddMember("temperature_f", *_currentTemperatureProperty, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastCurrentTemperaturePropertyVersion;
    _broker->Publish("weather/{}/property/currentTemperature/value", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::_receiveCurrentTemperaturePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse current_temperature property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received current_temperature payload is not an object or null");
    }

    // TODO: Check _lastCurrentTemperaturePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    double tempTemperatureF;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("temperature_f");
    if (itr != doc.MemberEnd() && itr->value.IsDouble())
    {
        tempTemperatureF = itr->value.GetDouble();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
        _currentTemperatureProperty = tempTemperatureF;
        _lastCurrentTemperaturePropertyVersion++;
    }
    republishCurrentTemperatureProperty();
}

boost::optional<CurrentConditionProperty> WeatherServer::getCurrentConditionProperty() const
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
    return _currentConditionProperty;
}

void WeatherServer::registerCurrentConditionPropertyCallback(const std::function<void(WeatherCondition condition, const std::string& description)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyCallbacksMutex);
    _currentConditionPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateCurrentConditionProperty(WeatherCondition condition, const std::string& description)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
        _currentConditionProperty = CurrentConditionProperty{ condition, description };
        _lastCurrentConditionPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionPropertyCallbacksMutex);
        for (const auto& cb: _currentConditionPropertyCallbacks)
        {
            cb(condition, description);
        }
    }
    republishCurrentConditionProperty();
}

void WeatherServer::republishCurrentConditionProperty() const
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
    rapidjson::Document doc;
    if (_currentConditionProperty)
    {
        doc.SetObject();

        _currentConditionProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastCurrentConditionPropertyVersion;
    _broker->Publish("weather/{}/property/currentCondition/value", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::_receiveCurrentConditionPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse current_condition property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received current_condition payload is not an object or null");
    }

    // TODO: Check _lastCurrentConditionPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    CurrentConditionProperty tempValue = CurrentConditionProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
        _currentConditionProperty = tempValue;
        _lastCurrentConditionPropertyVersion++;
    }
    republishCurrentConditionProperty();
}

boost::optional<DailyForecastProperty> WeatherServer::getDailyForecastProperty() const
{
    std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
    return _dailyForecastProperty;
}

void WeatherServer::registerDailyForecastPropertyCallback(const std::function<void(ForecastForDay monday, ForecastForDay tuesday, ForecastForDay wednesday)>& cb)
{
    std::lock_guard<std::mutex> lock(_dailyForecastPropertyCallbacksMutex);
    _dailyForecastPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateDailyForecastProperty(ForecastForDay monday, ForecastForDay tuesday, ForecastForDay wednesday)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
        _dailyForecastProperty = DailyForecastProperty{ monday, tuesday, wednesday };
        _lastDailyForecastPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastPropertyCallbacksMutex);
        for (const auto& cb: _dailyForecastPropertyCallbacks)
        {
            cb(monday, tuesday, wednesday);
        }
    }
    republishDailyForecastProperty();
}

void WeatherServer::republishDailyForecastProperty() const
{
    std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
    rapidjson::Document doc;
    if (_dailyForecastProperty)
    {
        doc.SetObject();

        _dailyForecastProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastDailyForecastPropertyVersion;
    _broker->Publish("weather/{}/property/dailyForecast/value", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::_receiveDailyForecastPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse daily_forecast property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received daily_forecast payload is not an object or null");
    }

    // TODO: Check _lastDailyForecastPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 3 values into struct.
    DailyForecastProperty tempValue = DailyForecastProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
        _dailyForecastProperty = tempValue;
        _lastDailyForecastPropertyVersion++;
    }
    republishDailyForecastProperty();
}

boost::optional<HourlyForecastProperty> WeatherServer::getHourlyForecastProperty() const
{
    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
    return _hourlyForecastProperty;
}

void WeatherServer::registerHourlyForecastPropertyCallback(const std::function<void(ForecastForHour hour_0, ForecastForHour hour_1, ForecastForHour hour_2, ForecastForHour hour_3)>& cb)
{
    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyCallbacksMutex);
    _hourlyForecastPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateHourlyForecastProperty(ForecastForHour hour_0, ForecastForHour hour_1, ForecastForHour hour_2, ForecastForHour hour_3)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
        _hourlyForecastProperty = HourlyForecastProperty{ hour_0, hour_1, hour_2, hour_3 };
        _lastHourlyForecastPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyCallbacksMutex);
        for (const auto& cb: _hourlyForecastPropertyCallbacks)
        {
            cb(hour_0, hour_1, hour_2, hour_3);
        }
    }
    republishHourlyForecastProperty();
}

void WeatherServer::republishHourlyForecastProperty() const
{
    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
    rapidjson::Document doc;
    if (_hourlyForecastProperty)
    {
        doc.SetObject();

        _hourlyForecastProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastHourlyForecastPropertyVersion;
    _broker->Publish("weather/{}/property/hourlyForecast/value", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::_receiveHourlyForecastPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse hourly_forecast property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received hourly_forecast payload is not an object or null");
    }

    // TODO: Check _lastHourlyForecastPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 4 values into struct.
    HourlyForecastProperty tempValue = HourlyForecastProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
        _hourlyForecastProperty = tempValue;
        _lastHourlyForecastPropertyVersion++;
    }
    republishHourlyForecastProperty();
}

boost::optional<CurrentConditionRefreshIntervalProperty> WeatherServer::getCurrentConditionRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
    return _currentConditionRefreshIntervalProperty;
}

void WeatherServer::registerCurrentConditionRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyCallbacksMutex);
    _currentConditionRefreshIntervalPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateCurrentConditionRefreshIntervalProperty(int seconds)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
        _currentConditionRefreshIntervalProperty = seconds;
        _lastCurrentConditionRefreshIntervalPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _currentConditionRefreshIntervalPropertyCallbacks)
        {
            cb(seconds);
        }
    }
    republishCurrentConditionRefreshIntervalProperty();
}

void WeatherServer::republishCurrentConditionRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
    rapidjson::Document doc;
    if (_currentConditionRefreshIntervalProperty)
    {
        doc.SetObject();

        doc.AddMember("seconds", *_currentConditionRefreshIntervalProperty, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastCurrentConditionRefreshIntervalPropertyVersion;
    _broker->Publish("weather/{}/property/currentConditionRefreshInterval/value", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::_receiveCurrentConditionRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse current_condition_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received current_condition_refresh_interval payload is not an object or null");
    }

    // TODO: Check _lastCurrentConditionRefreshIntervalPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    int tempSeconds;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempSeconds = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
        _currentConditionRefreshIntervalProperty = tempSeconds;
        _lastCurrentConditionRefreshIntervalPropertyVersion++;
    }
    republishCurrentConditionRefreshIntervalProperty();
}

boost::optional<HourlyForecastRefreshIntervalProperty> WeatherServer::getHourlyForecastRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
    return _hourlyForecastRefreshIntervalProperty;
}

void WeatherServer::registerHourlyForecastRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyCallbacksMutex);
    _hourlyForecastRefreshIntervalPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateHourlyForecastRefreshIntervalProperty(int seconds)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
        _hourlyForecastRefreshIntervalProperty = seconds;
        _lastHourlyForecastRefreshIntervalPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _hourlyForecastRefreshIntervalPropertyCallbacks)
        {
            cb(seconds);
        }
    }
    republishHourlyForecastRefreshIntervalProperty();
}

void WeatherServer::republishHourlyForecastRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
    rapidjson::Document doc;
    if (_hourlyForecastRefreshIntervalProperty)
    {
        doc.SetObject();

        doc.AddMember("seconds", *_hourlyForecastRefreshIntervalProperty, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastHourlyForecastRefreshIntervalPropertyVersion;
    _broker->Publish("weather/{}/property/hourlyForecastRefreshInterval/value", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::_receiveHourlyForecastRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse hourly_forecast_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received hourly_forecast_refresh_interval payload is not an object or null");
    }

    // TODO: Check _lastHourlyForecastRefreshIntervalPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    int tempSeconds;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempSeconds = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
        _hourlyForecastRefreshIntervalProperty = tempSeconds;
        _lastHourlyForecastRefreshIntervalPropertyVersion++;
    }
    republishHourlyForecastRefreshIntervalProperty();
}

boost::optional<DailyForecastRefreshIntervalProperty> WeatherServer::getDailyForecastRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
    return _dailyForecastRefreshIntervalProperty;
}

void WeatherServer::registerDailyForecastRefreshIntervalPropertyCallback(const std::function<void(int seconds)>& cb)
{
    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyCallbacksMutex);
    _dailyForecastRefreshIntervalPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateDailyForecastRefreshIntervalProperty(int seconds)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
        _dailyForecastRefreshIntervalProperty = seconds;
        _lastDailyForecastRefreshIntervalPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyCallbacksMutex);
        for (const auto& cb: _dailyForecastRefreshIntervalPropertyCallbacks)
        {
            cb(seconds);
        }
    }
    republishDailyForecastRefreshIntervalProperty();
}

void WeatherServer::republishDailyForecastRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
    rapidjson::Document doc;
    if (_dailyForecastRefreshIntervalProperty)
    {
        doc.SetObject();

        doc.AddMember("seconds", *_dailyForecastRefreshIntervalProperty, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastDailyForecastRefreshIntervalPropertyVersion;
    _broker->Publish("weather/{}/property/dailyForecastRefreshInterval/value", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::_receiveDailyForecastRefreshIntervalPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse daily_forecast_refresh_interval property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received daily_forecast_refresh_interval payload is not an object or null");
    }

    // TODO: Check _lastDailyForecastRefreshIntervalPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    int tempSeconds;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempSeconds = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
        _dailyForecastRefreshIntervalProperty = tempSeconds;
        _lastDailyForecastRefreshIntervalPropertyVersion++;
    }
    republishDailyForecastRefreshIntervalProperty();
}
