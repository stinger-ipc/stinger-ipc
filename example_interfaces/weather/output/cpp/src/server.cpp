


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

WeatherServer::WeatherServer(std::shared_ptr<IBrokerConnection> broker) : _broker(broker) {
    _broker->AddMessageCallback([this](
            const std::string& topic, 
            const std::string& payload, 
            const MqttProperties& mqttProps)
    {
        _receiveMessage(topic, payload, mqttProps);
    });
    
    _broker->Subscribe("weather/method/refreshDailyForecast", 2);
    
    _broker->Subscribe("weather/method/refreshHourlyForecast", 2);
    
    _broker->Subscribe("weather/method/refreshCurrentConditions", 2);
    
}

void WeatherServer::_receiveMessage(
        const std::string& topic, 
        const std::string& payload, 
        const MqttProperties& mqttProps)
{
    
    if (_broker->TopicMatchesSubscription(topic, "weather/method/refreshDailyForecast"))
    {
        std::cout << "Message matched topic weather/method/refreshDailyForecast\n";
        rapidjson::Document doc;
        try {
            if (_refreshDailyForecastHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
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
    
    if (_broker->TopicMatchesSubscription(topic, "weather/method/refreshHourlyForecast"))
    {
        std::cout << "Message matched topic weather/method/refreshHourlyForecast\n";
        rapidjson::Document doc;
        try {
            if (_refreshHourlyForecastHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
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
    
    if (_broker->TopicMatchesSubscription(topic, "weather/method/refreshCurrentConditions"))
    {
        std::cout << "Message matched topic weather/method/refreshCurrentConditions\n";
        rapidjson::Document doc;
        try {
            if (_refreshCurrentConditionsHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
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
        const boost::optional<std::string> optResponseTopic) const
{
    std::cout << "Handling call to refresh_daily_forecast\n";
    if (_refreshDailyForecastHandler) {
        

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
        const boost::optional<std::string> optResponseTopic) const
{
    std::cout << "Handling call to refresh_hourly_forecast\n";
    if (_refreshHourlyForecastHandler) {
        

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
        const boost::optional<std::string> optResponseTopic) const
{
    std::cout << "Handling call to refresh_current_conditions\n";
    if (_refreshCurrentConditionsHandler) {
        

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
