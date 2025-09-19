

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

    _refreshDailyForecastMethodSubscriptionId = _broker->Subscribe("weather/method/refreshDailyForecast", 2);
    _refreshHourlyForecastMethodSubscriptionId = _broker->Subscribe("weather/method/refreshHourlyForecast", 2);
    _refreshCurrentConditionsMethodSubscriptionId = _broker->Subscribe("weather/method/refreshCurrentConditions", 2);

    _locationPropertySubscriptionId = _broker->Subscribe("weather/property/location/setValue", 1);

    _currentTemperaturePropertySubscriptionId = _broker->Subscribe("weather/property/currentTemperature/setValue", 1);

    _currentConditionPropertySubscriptionId = _broker->Subscribe("weather/property/currentCondition/setValue", 1);

    _dailyForecastPropertySubscriptionId = _broker->Subscribe("weather/property/dailyForecast/setValue", 1);

    _hourlyForecastPropertySubscriptionId = _broker->Subscribe("weather/property/hourlyForecast/setValue", 1);

    _currentConditionRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/currentConditionRefreshInterval/setValue", 1);

    _hourlyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/hourlyForecastRefreshInterval/setValue", 1);

    _dailyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/dailyForecastRefreshInterval/setValue", 1);
}

void WeatherServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    int subscriptionId = mqttProps.subscriptionId.value_or(-1);

    if ((subscriptionId == _refreshDailyForecastMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "weather/method/refreshDailyForecast"))
    {
        std::cout << "Message matched topic weather/method/refreshDailyForecast\n";
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

    else if ((subscriptionId == _refreshHourlyForecastMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "weather/method/refreshHourlyForecast"))
    {
        std::cout << "Message matched topic weather/method/refreshHourlyForecast\n";
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

    else if ((subscriptionId == _refreshCurrentConditionsMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "weather/method/refreshCurrentConditions"))
    {
        std::cout << "Message matched topic weather/method/refreshCurrentConditions\n";
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

    if (subscriptionId == _locationPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/property/location/setValue"))
    {
        std::cout << "Message matched topic weather/property/location/setValue\n";
        _receiveLocationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentTemperaturePropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/property/currentTemperature/setValue"))
    {
        std::cout << "Message matched topic weather/property/currentTemperature/setValue\n";
        _receiveCurrentTemperaturePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentConditionPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/property/currentCondition/setValue"))
    {
        std::cout << "Message matched topic weather/property/currentCondition/setValue\n";
        _receiveCurrentConditionPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _dailyForecastPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/property/dailyForecast/setValue"))
    {
        std::cout << "Message matched topic weather/property/dailyForecast/setValue\n";
        _receiveDailyForecastPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _hourlyForecastPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/property/hourlyForecast/setValue"))
    {
        std::cout << "Message matched topic weather/property/hourlyForecast/setValue\n";
        _receiveHourlyForecastPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentConditionRefreshIntervalPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/property/currentConditionRefreshInterval/setValue"))
    {
        std::cout << "Message matched topic weather/property/currentConditionRefreshInterval/setValue\n";
        _receiveCurrentConditionRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _hourlyForecastRefreshIntervalPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/property/hourlyForecastRefreshInterval/setValue"))
    {
        std::cout << "Message matched topic weather/property/hourlyForecastRefreshInterval/setValue\n";
        _receiveHourlyForecastRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _dailyForecastRefreshIntervalPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "weather/property/dailyForecastRefreshInterval/setValue"))
    {
        std::cout << "Message matched topic weather/property/dailyForecastRefreshInterval/setValue\n";
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
    return _broker->Publish("weather/signal/currentTime", buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::registerRefreshDailyForecastHandler(std::function<void()> func)
{
    std::cout << "Registered method to handle weather/method/refreshDailyForecast\n";
    _refreshDailyForecastHandler = func;
}

void WeatherServer::registerRefreshHourlyForecastHandler(std::function<void()> func)
{
    std::cout << "Registered method to handle weather/method/refreshHourlyForecast\n";
    _refreshHourlyForecastHandler = func;
}

void WeatherServer::registerRefreshCurrentConditionsHandler(std::function<void()> func)
{
    std::cout << "Registered method to handle weather/method/refreshCurrentConditions\n";
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
            mqttProps.resultCode = MethodResultCode::SUCCESS;
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
            mqttProps.resultCode = MethodResultCode::SUCCESS;
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
            mqttProps.resultCode = MethodResultCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

boost::optional<struct LocationProperty> WeatherServer::getLocationProperty() const
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
    _locationProperty = LocationProperty{ latitude, longitude };
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
    _currentTemperatureProperty = temperature_f;
}

boost::optional<struct CurrentConditionProperty> WeatherServer::getCurrentConditionProperty() const
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
    _currentConditionProperty = CurrentConditionProperty{ condition, description };
}

boost::optional<struct DailyForecastProperty> WeatherServer::getDailyForecastProperty() const
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
    _dailyForecastProperty = DailyForecastProperty{ monday, tuesday, wednesday };
}

boost::optional<struct HourlyForecastProperty> WeatherServer::getHourlyForecastProperty() const
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
    _hourlyForecastProperty = HourlyForecastProperty{ hour_0, hour_1, hour_2, hour_3 };
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
    _currentConditionRefreshIntervalProperty = seconds;
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
    _hourlyForecastRefreshIntervalProperty = seconds;
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
    _dailyForecastRefreshIntervalProperty = seconds;
}
