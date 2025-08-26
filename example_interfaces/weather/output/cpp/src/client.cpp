
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
    _broker->AddMessageCallback([this](const std::string& topic, const std::string& payload, const boost::optional<std::string> optCorrelationId, const boost::optional<std::string> unusedRespTopic, const boost::optional<MethodResultCode> optResultCode)
    {
        _receiveMessage(topic, payload, optCorrelationId, optResultCode);
    });
    _broker->Subscribe("weather/signal/currentTime", 1);
    
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
}

void WeatherClient::_receiveMessage(
        const std::string& topic, 
        const std::string& payload, 
        const boost::optional<std::string> optCorrelationId, 
        const boost::optional<MethodResultCode> optResultCode)
{
    if (_broker->TopicMatchesSubscription(topic, "weather/signal/currentTime"))
    {
        //Log("Handling current_time signal");
        rapidjson::Document doc;
        try {
            if (_currentTimeCallback)
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
                

                _currentTimeCallback(tempcurrent_time);
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
}
void WeatherClient::registerCurrentTimeCallback(const std::function<void(const std::string&)>& cb)
{
    _currentTimeCallback = cb;
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
