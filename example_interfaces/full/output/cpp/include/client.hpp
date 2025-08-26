/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
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

class FullClient {

public:
    // This is the name of the API.
    static constexpr const char NAME[] = "Full";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    // Constructor taking a connection object.
    FullClient(std::shared_ptr<IBrokerConnection> broker);

    virtual ~FullClient() = default;

    
    // Register a callback for the `todayIs` signal.
    // The provided method will be called whenever a `todayIs` is received.
    void registerTodayIsCallback(const std::function<void(int, boost::optional<DayOfTheWeek>)>& cb);
    

    
    // Calls the `addNumbers` method.
    // Returns a future.  When that future resolves, it will have the returned value.
    boost::future<int> addNumbers(int first, int second, boost::optional<int> third);
    
    // Calls the `doSomething` method.
    // Returns a future.  When that future resolves, it will have the returned value.
    boost::future<DoSomethingReturnValue> doSomething(const std::string& aString);
    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(const std::string& topic, const std::string& payload, const boost::optional<std::string> optCorrelationId, const boost::optional<MethodResultCode> optResultCode);
    std::map<boost::uuids::uuid, boost::promise<int>> _pendingAddNumbersMethodCalls;
    std::map<boost::uuids::uuid, boost::promise<DoSomethingReturnValue>> _pendingDoSomethingMethodCalls;
    
    std::function<void(int, boost::optional<DayOfTheWeek>)> _todayIsCallback;
    
    void _handleAddNumbersResponse(const std::string& topic, const std::string& payload, const std::string& optCorrelationId);
    void _handleDoSomethingResponse(const std::string& topic, const std::string& payload, const std::string& optCorrelationId);
};