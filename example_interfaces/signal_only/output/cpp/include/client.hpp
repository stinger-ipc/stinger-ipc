/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
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


class SignalOnlyClient {

public:
    // This is the name of the API.
    static constexpr const char NAME[] = "SignalOnly";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    // Constructor taking a connection object.
    SignalOnlyClient(std::shared_ptr<IBrokerConnection> broker);

    virtual ~SignalOnlyClient() = default;

    
    // Register a callback for the `anotherSignal` signal.
    // The provided method will be called whenever a `anotherSignal` is received.
    void registerAnotherSignalCallback(const std::function<void(double, bool, const std::string&)>& cb);
    

    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(const std::string& topic, const std::string& payload, const boost::optional<std::string> optCorrelationId, const boost::optional<MethodResultCode> optResultCode);
    
    std::function<void(double, bool, const std::string&)> _anotherSignalCallback;
    
};