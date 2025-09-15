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

#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "return_types.hpp"

class WeatherServer {

public:
    static constexpr const char NAME[] = "weather";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    WeatherServer(std::shared_ptr<IBrokerConnection> broker);

    virtual ~WeatherServer() = default;

    
    boost::future<bool> emitCurrentTimeSignal(const std::string&);
    

    
    void registerRefreshDailyForecastHandler(std::function<void()> func);
    
    void registerRefreshHourlyForecastHandler(std::function<void()> func);
    
    void registerRefreshCurrentConditionsHandler(std::function<void()> func);
    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(
            const std::string& topic, 
            const std::string& payload, 
            const MqttProperties& mqttProps
    );

    
    void _callRefreshDailyForecastHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<void()> _refreshDailyForecastHandler;
    
    void _callRefreshHourlyForecastHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<void()> _refreshHourlyForecastHandler;
    
    void _callRefreshCurrentConditionsHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<void()> _refreshCurrentConditionsHandler;
    

};