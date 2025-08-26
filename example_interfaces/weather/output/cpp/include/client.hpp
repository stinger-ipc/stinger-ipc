/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/


#pragma once

#include <cstdint>
#include <functional>
#include <map>
#include <memory>
#include <exception>
#include <mutex>
#include <rapidjson/document.h>
#include <boost/uuid/uuid.hpp>

#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "return_types.hpp"
#include "property_structs.hpp"

class WeatherClient {

public:
    // This is the name of the API.
    static constexpr const char NAME[] = "weather";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    // Constructor taking a connection object.
    WeatherClient(std::shared_ptr<IBrokerConnection> broker);

    virtual ~WeatherClient() = default;

    
    // Register a callback for the `current_time` signal.
    // The provided method will be called whenever a `current_time` is received.
    void registerCurrentTimeCallback(const std::function<void(const std::string&)>& cb);
    

    
    // Calls the `refresh_daily_forecast` method.
    // Returns a future.  When that future resolves, it will have the returned value.
    boost::future<void> refreshDailyForecast();
    
    // Calls the `refresh_hourly_forecast` method.
    // Returns a future.  When that future resolves, it will have the returned value.
    boost::future<void> refreshHourlyForecast();
    
    // Calls the `refresh_current_conditions` method.
    // Returns a future.  When that future resolves, it will have the returned value.
    boost::future<void> refreshCurrentConditions();
    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(const std::string& topic, const std::string& payload, const boost::optional<std::string> optCorrelationId, const boost::optional<MethodResultCode> optResultCode);
    std::map<boost::uuids::uuid, boost::promise<void>> _pendingRefreshDailyForecastMethodCalls;
    std::map<boost::uuids::uuid, boost::promise<void>> _pendingRefreshHourlyForecastMethodCalls;
    std::map<boost::uuids::uuid, boost::promise<void>> _pendingRefreshCurrentConditionsMethodCalls;
    
    std::function<void(const std::string&)> _currentTimeCallback;
    
    void _handleRefreshDailyForecastResponse(const std::string& topic, const std::string& payload, const std::string& optCorrelationId);
    void _handleRefreshHourlyForecastResponse(const std::string& topic, const std::string& payload, const std::string& optCorrelationId);
    void _handleRefreshCurrentConditionsResponse(const std::string& topic, const std::string& payload, const std::string& optCorrelationId);
};