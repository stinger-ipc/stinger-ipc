

#include <vector>
#include <iostream>
#include <syslog.h>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "server.hpp"
#include "method_payloads.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"

constexpr const char WeatherServer::NAME[];
constexpr const char WeatherServer::INTERFACE_VERSION[];

WeatherServer::WeatherServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId): _broker(broker), _instanceId(instanceId), _advertisementThreadRunning(false)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _receiveMessage(topic, payload, mqttProps);
                                                               });

    _refreshDailyForecastMethodSubscriptionId = _broker->Subscribe((boost::format("weather/%1%/method/refreshDailyForecast") % _instanceId).str(), 2);
    _refreshHourlyForecastMethodSubscriptionId = _broker->Subscribe((boost::format("weather/%1%/method/refreshHourlyForecast") % _instanceId).str(), 2);
    _refreshCurrentConditionsMethodSubscriptionId = _broker->Subscribe((boost::format("weather/%1%/method/refreshCurrentConditions") % _instanceId).str(), 2);

    _locationPropertySubscriptionId = _broker->Subscribe((boost::format("weather/%1%/property/location/setValue") % _instanceId).str(), 1);
    _currentTemperaturePropertySubscriptionId = _broker->Subscribe((boost::format("weather/%1%/property/currentTemperature/setValue") % _instanceId).str(), 1);
    _currentConditionPropertySubscriptionId = _broker->Subscribe((boost::format("weather/%1%/property/currentCondition/setValue") % _instanceId).str(), 1);
    _dailyForecastPropertySubscriptionId = _broker->Subscribe((boost::format("weather/%1%/property/dailyForecast/setValue") % _instanceId).str(), 1);
    _hourlyForecastPropertySubscriptionId = _broker->Subscribe((boost::format("weather/%1%/property/hourlyForecast/setValue") % _instanceId).str(), 1);
    _currentConditionRefreshIntervalPropertySubscriptionId = _broker->Subscribe((boost::format("weather/%1%/property/currentConditionRefreshInterval/setValue") % _instanceId).str(), 1);
    _hourlyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe((boost::format("weather/%1%/property/hourlyForecastRefreshInterval/setValue") % _instanceId).str(), 1);
    _dailyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe((boost::format("weather/%1%/property/dailyForecastRefreshInterval/setValue") % _instanceId).str(), 1);

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&WeatherServer::_advertisementThreadLoop, this);
}

WeatherServer::~WeatherServer()
{
    // Unregister the message callback from the broker.
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }

    // Stop the advertisement thread
    _advertisementThreadRunning = false;
    if (_advertisementThread.joinable())
    {
        _advertisementThread.join();
    }

    std::string topic = (boost::format("weather/%1%/interface") % _instanceId).str();
    _broker->Publish(topic, "", 1, true, MqttProperties());

    _broker->Unsubscribe((boost::format("weather/%1%/method/refreshDailyForecast") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/method/refreshHourlyForecast") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/method/refreshCurrentConditions") % _instanceId).str());

    _broker->Unsubscribe((boost::format("weather/%1%/property/location/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/property/currentTemperature/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/property/currentCondition/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/property/dailyForecast/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/property/hourlyForecast/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/property/currentConditionRefreshInterval/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/property/hourlyForecastRefreshInterval/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("weather/%1%/property/dailyForecastRefreshInterval/setValue") % _instanceId).str());
}

void WeatherServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);

    if ((subscriptionId == _refreshDailyForecastMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/method/refreshDailyForecast") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as refresh_daily_forecast method request.", topic.c_str());
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

    else if ((subscriptionId == _refreshHourlyForecastMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/method/refreshHourlyForecast") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as refresh_hourly_forecast method request.", topic.c_str());
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

    else if ((subscriptionId == _refreshCurrentConditionsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/method/refreshCurrentConditions") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as refresh_current_conditions method request.", topic.c_str());
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

    if (subscriptionId == _locationPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/property/location/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as location property update.", topic.c_str());
        _receiveLocationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentTemperaturePropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/property/currentTemperature/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as current_temperature property update.", topic.c_str());
        _receiveCurrentTemperaturePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentConditionPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/property/currentCondition/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as current_condition property update.", topic.c_str());
        _receiveCurrentConditionPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _dailyForecastPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/property/dailyForecast/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as daily_forecast property update.", topic.c_str());
        _receiveDailyForecastPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _hourlyForecastPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/property/hourlyForecast/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as hourly_forecast property update.", topic.c_str());
        _receiveHourlyForecastPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _currentConditionRefreshIntervalPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/property/currentConditionRefreshInterval/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as current_condition_refresh_interval property update.", topic.c_str());
        _receiveCurrentConditionRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _hourlyForecastRefreshIntervalPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/property/hourlyForecastRefreshInterval/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as hourly_forecast_refresh_interval property update.", topic.c_str());
        _receiveHourlyForecastRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _dailyForecastRefreshIntervalPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("weather/%1%/property/dailyForecastRefreshInterval/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as daily_forecast_refresh_interval property update.", topic.c_str());
        _receiveDailyForecastRefreshIntervalPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

boost::future<bool> WeatherServer::emitCurrentTimeSignal(const std::string& currentTime)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(currentTime.c_str(), currentTime.size(), doc.GetAllocator());
        doc.AddMember("current_time", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("weather/%1%/signal/currentTime") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void WeatherServer::registerRefreshDailyForecastHandler(std::function<void()> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle weather/+/method/refreshDailyForecast method requests.");
    _refreshDailyForecastHandler = func;
}

void WeatherServer::registerRefreshHourlyForecastHandler(std::function<void()> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle weather/+/method/refreshHourlyForecast method requests.");
    _refreshHourlyForecastHandler = func;
}

void WeatherServer::registerRefreshCurrentConditionsHandler(std::function<void()> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle weather/+/method/refreshCurrentConditions method requests.");
    _refreshCurrentConditionsHandler = func;
}

void WeatherServer::_callRefreshDailyForecastHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to refresh_daily_forecast");
    if (!_refreshDailyForecastHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    // Method doesn't have any return values.
    _refreshDailyForecastHandler();
    auto returnValues = RefreshDailyForecastReturnValues();

    if (optResponseTopic)
    {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);
        MqttProperties mqttProps;
        mqttProps.correlationId = optCorrelationId;
        mqttProps.returnCode = MethodReturnCode::SUCCESS;
        _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
    }
}

void WeatherServer::_callRefreshHourlyForecastHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to refresh_hourly_forecast");
    if (!_refreshHourlyForecastHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    // Method doesn't have any return values.
    _refreshHourlyForecastHandler();
    auto returnValues = RefreshHourlyForecastReturnValues();

    if (optResponseTopic)
    {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);
        MqttProperties mqttProps;
        mqttProps.correlationId = optCorrelationId;
        mqttProps.returnCode = MethodReturnCode::SUCCESS;
        _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
    }
}

void WeatherServer::_callRefreshCurrentConditionsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to refresh_current_conditions");
    if (!_refreshCurrentConditionsHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    // Method doesn't have any return values.
    _refreshCurrentConditionsHandler();
    auto returnValues = RefreshCurrentConditionsReturnValues();

    if (optResponseTopic)
    {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);
        MqttProperties mqttProps;
        mqttProps.correlationId = optCorrelationId;
        mqttProps.returnCode = MethodReturnCode::SUCCESS;
        _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
    }
}

boost::optional<LocationProperty> WeatherServer::getLocationProperty() const
{
    std::lock_guard<std::mutex> lock(_locationPropertyMutex);
    if (_locationProperty)
    {
        return *_locationProperty;
    }
    return boost::none;
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
    _broker->Publish((boost::format("weather/%1%/property/location/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
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

boost::optional<double> WeatherServer::getCurrentTemperatureProperty() const
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
    if (_currentTemperatureProperty)
    {
        return _currentTemperatureProperty->temperatureF;
    }
    return boost::none;
}

void WeatherServer::registerCurrentTemperaturePropertyCallback(const std::function<void(double temperatureF)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyCallbacksMutex);
    _currentTemperaturePropertyCallbacks.push_back(cb);
}

void WeatherServer::updateCurrentTemperatureProperty(double temperatureF)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
        _currentTemperatureProperty = CurrentTemperatureProperty{ temperatureF };
        _lastCurrentTemperaturePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyCallbacksMutex);
        for (const auto& cb: _currentTemperaturePropertyCallbacks)
        {
            cb(temperatureF);
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
        _currentTemperatureProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
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
    _broker->Publish((boost::format("weather/%1%/property/currentTemperature/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
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

    // Deserialize 1 values into struct.
    CurrentTemperatureProperty tempValue = CurrentTemperatureProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
        _currentTemperatureProperty = tempValue;
        _lastCurrentTemperaturePropertyVersion++;
    }
    republishCurrentTemperatureProperty();
}

boost::optional<CurrentConditionProperty> WeatherServer::getCurrentConditionProperty() const
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
    if (_currentConditionProperty)
    {
        return *_currentConditionProperty;
    }
    return boost::none;
}

void WeatherServer::registerCurrentConditionPropertyCallback(const std::function<void(WeatherCondition condition, std::string description)>& cb)
{
    std::lock_guard<std::mutex> lock(_currentConditionPropertyCallbacksMutex);
    _currentConditionPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateCurrentConditionProperty(WeatherCondition condition, std::string description)
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
    _broker->Publish((boost::format("weather/%1%/property/currentCondition/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
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
    if (_dailyForecastProperty)
    {
        return *_dailyForecastProperty;
    }
    return boost::none;
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
    _broker->Publish((boost::format("weather/%1%/property/dailyForecast/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
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
    if (_hourlyForecastProperty)
    {
        return *_hourlyForecastProperty;
    }
    return boost::none;
}

void WeatherServer::registerHourlyForecastPropertyCallback(const std::function<void(ForecastForHour hour0, ForecastForHour hour1, ForecastForHour hour2, ForecastForHour hour3)>& cb)
{
    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyCallbacksMutex);
    _hourlyForecastPropertyCallbacks.push_back(cb);
}

void WeatherServer::updateHourlyForecastProperty(ForecastForHour hour0, ForecastForHour hour1, ForecastForHour hour2, ForecastForHour hour3)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
        _hourlyForecastProperty = HourlyForecastProperty{ hour0, hour1, hour2, hour3 };
        _lastHourlyForecastPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastPropertyCallbacksMutex);
        for (const auto& cb: _hourlyForecastPropertyCallbacks)
        {
            cb(hour0, hour1, hour2, hour3);
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
    _broker->Publish((boost::format("weather/%1%/property/hourlyForecast/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
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

boost::optional<int> WeatherServer::getCurrentConditionRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
    if (_currentConditionRefreshIntervalProperty)
    {
        return _currentConditionRefreshIntervalProperty->seconds;
    }
    return boost::none;
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
        _currentConditionRefreshIntervalProperty = CurrentConditionRefreshIntervalProperty{ seconds };
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
        _currentConditionRefreshIntervalProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
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
    _broker->Publish((boost::format("weather/%1%/property/currentConditionRefreshInterval/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
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

    // Deserialize 1 values into struct.
    CurrentConditionRefreshIntervalProperty tempValue = CurrentConditionRefreshIntervalProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
        _currentConditionRefreshIntervalProperty = tempValue;
        _lastCurrentConditionRefreshIntervalPropertyVersion++;
    }
    republishCurrentConditionRefreshIntervalProperty();
}

boost::optional<int> WeatherServer::getHourlyForecastRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
    if (_hourlyForecastRefreshIntervalProperty)
    {
        return _hourlyForecastRefreshIntervalProperty->seconds;
    }
    return boost::none;
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
        _hourlyForecastRefreshIntervalProperty = HourlyForecastRefreshIntervalProperty{ seconds };
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
        _hourlyForecastRefreshIntervalProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
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
    _broker->Publish((boost::format("weather/%1%/property/hourlyForecastRefreshInterval/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
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

    // Deserialize 1 values into struct.
    HourlyForecastRefreshIntervalProperty tempValue = HourlyForecastRefreshIntervalProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
        _hourlyForecastRefreshIntervalProperty = tempValue;
        _lastHourlyForecastRefreshIntervalPropertyVersion++;
    }
    republishHourlyForecastRefreshIntervalProperty();
}

boost::optional<int> WeatherServer::getDailyForecastRefreshIntervalProperty() const
{
    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
    if (_dailyForecastRefreshIntervalProperty)
    {
        return _dailyForecastRefreshIntervalProperty->seconds;
    }
    return boost::none;
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
        _dailyForecastRefreshIntervalProperty = DailyForecastRefreshIntervalProperty{ seconds };
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
        _dailyForecastRefreshIntervalProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
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
    _broker->Publish((boost::format("weather/%1%/property/dailyForecastRefreshInterval/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
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

    // Deserialize 1 values into struct.
    DailyForecastRefreshIntervalProperty tempValue = DailyForecastRefreshIntervalProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
        _dailyForecastRefreshIntervalProperty = tempValue;
        _lastDailyForecastRefreshIntervalPropertyVersion++;
    }
    republishDailyForecastRefreshIntervalProperty();
}

void WeatherServer::_advertisementThreadLoop()
{
    while (_advertisementThreadRunning)
    {
        // Get current timestamp
        auto now = std::chrono::system_clock::now();
        std::string timestamp = timePointToIsoString(now);

        // Build JSON message
        rapidjson::Document doc;
        doc.SetObject();
        rapidjson::Document::AllocatorType& allocator = doc.GetAllocator();

        doc.AddMember("interface_name", rapidjson::Value("weather", allocator), allocator);
        doc.AddMember("instance", rapidjson::Value(_instanceId.c_str(), allocator), allocator);
        doc.AddMember("title", rapidjson::Value("NWS weather forecast", allocator), allocator);
        doc.AddMember("version", rapidjson::Value("0.1.2", allocator), allocator);
        doc.AddMember("connection_topic", rapidjson::Value(_broker->GetOnlineTopic().c_str(), allocator), allocator);
        doc.AddMember("timestamp", rapidjson::Value(timestamp.c_str(), allocator), allocator);

        // Convert to JSON string
        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        doc.Accept(writer);

        // Create MQTT properties with message expiry interval of 150 seconds
        MqttProperties mqttProps;
        mqttProps.messageExpiryInterval = 150;

        // Publish to weather/<instance_id>/interface
        std::string topic = (boost::format("weather/%1%/interface") % _instanceId).str();
        _broker->Publish(topic, buf.GetString(), 1, true, mqttProps);

        _broker->Log(LOG_INFO, "Published service advertisement to %s", topic.c_str());

        // Wait for 120 seconds or until thread should stop
        // Use smaller sleep intervals to allow quick shutdown
        for (int i = 0; i < 120 && _advertisementThreadRunning; ++i)
        {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
}
