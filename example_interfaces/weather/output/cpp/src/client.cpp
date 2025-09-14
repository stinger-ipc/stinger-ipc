
#include <vector>
#include <iostream>
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

WeatherClient::WeatherClient(std::shared_ptr<IBrokerConnection> broker) : _broker(broker)
{
    _broker->AddMessageCallback([this](
            const std::string& topic, 
            const std::string& payload, 
            const boost::optional<std::string> optCorrelationId, 
            const boost::optional<std::string> unusedRespTopic, 
            const boost::optional<MethodResultCode> optResultCode,
            const boost::optional<int> optSubscriptionId,
            const boost::optional<int> optPropertyVersion)
    {
        _receiveMessage(topic, payload, optCorrelationId, optResultCode, optSubscriptionId, optPropertyVersion);
    });
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
    _locationPropertySubscriptionId = _broker->Subscribe("weather/property/location/setValue", 1);
    
    _currentTemperaturePropertySubscriptionId = _broker->Subscribe("weather/property/currentTemperature/setValue", 1);
    
    _currentConditionPropertySubscriptionId = _broker->Subscribe("weather/property/currentCondition/setValue", 1);
    
    _dailyForecastPropertySubscriptionId = _broker->Subscribe("weather/property/dailyForecast/setValue", 1);
    
    _hourlyForecastPropertySubscriptionId = _broker->Subscribe("weather/property/hourlyForecast/setValue", 1);
    
    _currentConditionRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/currentConditionRefreshInterval/setValue", 1);
    
    _hourlyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/hourlyForecastRefreshInterval/setValue", 1);
    
    _dailyForecastRefreshIntervalPropertySubscriptionId = _broker->Subscribe("weather/property/dailyForecastRefreshInterval/setValue", 1);
    
}

void WeatherClient::_receiveMessage(
        const std::string& topic, 
        const std::string& payload, 
        const boost::optional<std::string> optCorrelationId, 
        const boost::optional<MethodResultCode> optResultCode,
        const boost::optional<int> optSubscriptionId,
        const boost::optional<int> optPropertyVersion)
{
    if ((optSubscriptionId && (*optSubscriptionId == _currentTimeSignalSubscriptionId)) || _broker->TopicMatchesSubscription(topic, "weather/signal/currentTime"))
    {
        //Log("Handling current_time signal");
        rapidjson::Document doc;
        try {
            if (_currentTimeSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse current_time signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                
                std::string tempcurrent_time;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("current_time");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        
                        tempcurrent_time = itr->value.GetString();
                        
                    } else {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    
                    }
                }
                
                for (const auto& cb : _currentTimeSignalCallbacks)
                {
                    cb(tempcurrent_time);
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
    if (_broker->TopicMatchesSubscription(topic, "client/+/weather/method/refreshDailyForecast/response") && optCorrelationId)
    {
        std::cout << "Matched topic for refresh_daily_forecast response" << std::endl;
        _handleRefreshDailyForecastResponse(topic, payload, *optCorrelationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/weather/method/refreshHourlyForecast/response") && optCorrelationId)
    {
        std::cout << "Matched topic for refresh_hourly_forecast response" << std::endl;
        _handleRefreshHourlyForecastResponse(topic, payload, *optCorrelationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/weather/method/refreshCurrentConditions/response") && optCorrelationId)
    {
        std::cout << "Matched topic for refresh_current_conditions response" << std::endl;
        _handleRefreshCurrentConditionsResponse(topic, payload, *optCorrelationId);
    }
    if ((optSubscriptionId && (*optSubscriptionId == _locationPropertySubscriptionId)) || topic == "weather/property/location/setValue")
    {
        _receiveLocationPropertyUpdate(topic, payload, optPropertyVersion);
    }
    else if ((optSubscriptionId && (*optSubscriptionId == _currentTemperaturePropertySubscriptionId)) || topic == "weather/property/currentTemperature/setValue")
    {
        _receiveCurrentTemperaturePropertyUpdate(topic, payload, optPropertyVersion);
    }
    else if ((optSubscriptionId && (*optSubscriptionId == _currentConditionPropertySubscriptionId)) || topic == "weather/property/currentCondition/setValue")
    {
        _receiveCurrentConditionPropertyUpdate(topic, payload, optPropertyVersion);
    }
    else if ((optSubscriptionId && (*optSubscriptionId == _dailyForecastPropertySubscriptionId)) || topic == "weather/property/dailyForecast/setValue")
    {
        _receiveDailyForecastPropertyUpdate(topic, payload, optPropertyVersion);
    }
    else if ((optSubscriptionId && (*optSubscriptionId == _hourlyForecastPropertySubscriptionId)) || topic == "weather/property/hourlyForecast/setValue")
    {
        _receiveHourlyForecastPropertyUpdate(topic, payload, optPropertyVersion);
    }
    else if ((optSubscriptionId && (*optSubscriptionId == _currentConditionRefreshIntervalPropertySubscriptionId)) || topic == "weather/property/currentConditionRefreshInterval/setValue")
    {
        _receiveCurrentConditionRefreshIntervalPropertyUpdate(topic, payload, optPropertyVersion);
    }
    else if ((optSubscriptionId && (*optSubscriptionId == _hourlyForecastRefreshIntervalPropertySubscriptionId)) || topic == "weather/property/hourlyForecastRefreshInterval/setValue")
    {
        _receiveHourlyForecastRefreshIntervalPropertyUpdate(topic, payload, optPropertyVersion);
    }
    else if ((optSubscriptionId && (*optSubscriptionId == _dailyForecastRefreshIntervalPropertySubscriptionId)) || topic == "weather/property/dailyForecastRefreshInterval/setValue")
    {
        _receiveDailyForecastRefreshIntervalPropertyUpdate(topic, payload, optPropertyVersion);
    }
}
void WeatherClient::registerCurrentTimeCallback(const std::function<void(const std::string&)>& cb)
{
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
    _broker->Publish("weather/method/refreshDailyForecast", buf.GetString(), 2, false, correlationIdStr, responseTopicStringStream.str(), MethodResultCode::SUCCESS);

    return _pendingRefreshDailyForecastMethodCalls[correlationId].get_future();
}

void WeatherClient::_handleRefreshDailyForecastResponse(
        const std::string& topic, 
        const std::string& payload, 
        const std::string &correlationId) 
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse refresh_daily_forecast signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload is not an object");
    }

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
    _broker->Publish("weather/method/refreshHourlyForecast", buf.GetString(), 2, false, correlationIdStr, responseTopicStringStream.str(), MethodResultCode::SUCCESS);

    return _pendingRefreshHourlyForecastMethodCalls[correlationId].get_future();
}

void WeatherClient::_handleRefreshHourlyForecastResponse(
        const std::string& topic, 
        const std::string& payload, 
        const std::string &correlationId) 
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse refresh_hourly_forecast signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload is not an object");
    }

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
    _broker->Publish("weather/method/refreshCurrentConditions", buf.GetString(), 2, false, correlationIdStr, responseTopicStringStream.str(), MethodResultCode::SUCCESS);

    return _pendingRefreshCurrentConditionsMethodCalls[correlationId].get_future();
}

void WeatherClient::_handleRefreshCurrentConditionsResponse(
        const std::string& topic, 
        const std::string& payload, 
        const std::string &correlationId) 
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse refresh_current_conditions signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload is not an object");
    }

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

    if (!doc.IsObject()) {
        throw std::runtime_error("Received location payload is not an object");
    }
    LocationProperty tempValue;
    
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("latitude");
        if (itr != doc.MemberEnd() && itr->value.IsDouble()) {
            
            tempValue.latitude = itr->value.GetDouble();

        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("longitude");
        if (itr != doc.MemberEnd() && itr->value.IsDouble()) {
            
            tempValue.longitude = itr->value.GetDouble();

        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }

    std::lock_guard<std::mutex> lock(_locationPropertyMutex);
    _locationProperty = tempValue;
    _lastLocationPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;

    // Notify all registered callbacks.
    for (const auto& cb : _locationPropertyCallbacks)
    {
        cb(*_locationProperty);
    }
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

    if (!doc.IsObject()) {
        throw std::runtime_error("Received current_temperature payload is not an object");
    }
    CurrentTemperatureProperty tempValue;
    
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("temperature_f");
    if (itr != doc.MemberEnd() && itr->value.IsDouble()) {
        
    tempValue = itr->value.GetDouble();

    } else {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    std::lock_guard<std::mutex> lock(_currentTemperaturePropertyMutex);
    _currentTemperatureProperty = tempValue;
    _lastCurrentTemperaturePropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;

    // Notify all registered callbacks.
    for (const auto& cb : _currentTemperaturePropertyCallbacks)
    {
        cb(*_currentTemperatureProperty);
    }
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

    if (!doc.IsObject()) {
        throw std::runtime_error("Received current_condition payload is not an object");
    }
    CurrentConditionProperty tempValue;
    
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("condition");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            
            tempValue.condition = static_cast<WeatherCondition>(itr->value.GetInt());

        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("description");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            
            tempValue.description = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }

    std::lock_guard<std::mutex> lock(_currentConditionPropertyMutex);
    _currentConditionProperty = tempValue;
    _lastCurrentConditionPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;

    // Notify all registered callbacks.
    for (const auto& cb : _currentConditionPropertyCallbacks)
    {
        cb(*_currentConditionProperty);
    }
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

    if (!doc.IsObject()) {
        throw std::runtime_error("Received daily_forecast payload is not an object");
    }
    DailyForecastProperty tempValue;
    
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("monday");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            
            tempValue.monday = ForecastForDay::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("tuesday");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            
            tempValue.tuesday = ForecastForDay::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("wednesday");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            
            tempValue.wednesday = ForecastForDay::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }

    std::lock_guard<std::mutex> lock(_dailyForecastPropertyMutex);
    _dailyForecastProperty = tempValue;
    _lastDailyForecastPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;

    // Notify all registered callbacks.
    for (const auto& cb : _dailyForecastPropertyCallbacks)
    {
        cb(*_dailyForecastProperty);
    }
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

    if (!doc.IsObject()) {
        throw std::runtime_error("Received hourly_forecast payload is not an object");
    }
    HourlyForecastProperty tempValue;
    
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_0");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            
            tempValue.hour_0 = ForecastForHour::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_1");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            
            tempValue.hour_1 = ForecastForHour::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_2");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            
            tempValue.hour_2 = ForecastForHour::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("hour_3");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            
            tempValue.hour_3 = ForecastForHour::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }

    std::lock_guard<std::mutex> lock(_hourlyForecastPropertyMutex);
    _hourlyForecastProperty = tempValue;
    _lastHourlyForecastPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;

    // Notify all registered callbacks.
    for (const auto& cb : _hourlyForecastPropertyCallbacks)
    {
        cb(*_hourlyForecastProperty);
    }
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

    if (!doc.IsObject()) {
        throw std::runtime_error("Received current_condition_refresh_interval payload is not an object");
    }
    CurrentConditionRefreshIntervalProperty tempValue;
    
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
        
    tempValue = itr->value.GetInt();

    } else {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    std::lock_guard<std::mutex> lock(_currentConditionRefreshIntervalPropertyMutex);
    _currentConditionRefreshIntervalProperty = tempValue;
    _lastCurrentConditionRefreshIntervalPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;

    // Notify all registered callbacks.
    for (const auto& cb : _currentConditionRefreshIntervalPropertyCallbacks)
    {
        cb(*_currentConditionRefreshIntervalProperty);
    }
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

    if (!doc.IsObject()) {
        throw std::runtime_error("Received hourly_forecast_refresh_interval payload is not an object");
    }
    HourlyForecastRefreshIntervalProperty tempValue;
    
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
        
    tempValue = itr->value.GetInt();

    } else {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    std::lock_guard<std::mutex> lock(_hourlyForecastRefreshIntervalPropertyMutex);
    _hourlyForecastRefreshIntervalProperty = tempValue;
    _lastHourlyForecastRefreshIntervalPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;

    // Notify all registered callbacks.
    for (const auto& cb : _hourlyForecastRefreshIntervalPropertyCallbacks)
    {
        cb(*_hourlyForecastRefreshIntervalProperty);
    }
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

    if (!doc.IsObject()) {
        throw std::runtime_error("Received daily_forecast_refresh_interval payload is not an object");
    }
    DailyForecastRefreshIntervalProperty tempValue;
    
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seconds");
    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
        
    tempValue = itr->value.GetInt();

    } else {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    std::lock_guard<std::mutex> lock(_dailyForecastRefreshIntervalPropertyMutex);
    _dailyForecastRefreshIntervalProperty = tempValue;
    _lastDailyForecastRefreshIntervalPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;

    // Notify all registered callbacks.
    for (const auto& cb : _dailyForecastRefreshIntervalPropertyCallbacks)
    {
        cb(*_dailyForecastRefreshIntervalProperty);
    }
}
 