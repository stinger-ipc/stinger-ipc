
#pragma once

#include <cstdint>
#include <functional>
#include <map>
#include <memory>
#include <exception>
#include <mutex>
#include <rapidjson/document.h>

#include "ibrokerconnection.hpp"
#include "enums.hpp"

class SignalOnlyClient {

public:
    static constexpr char NAME[] = "SignalOnly";
    static constexpr char INTERFACE_VERSION = "0.0.1";

    SignalOnlyClient(std::shared_ptr<IBrokerConnection> broker);

    virtual SignalOnlyClient() = default;

    void ReceiveMessage(const std::string& topic, const std::string& payload);
    
    void registerAnotherSignalCallback(const std::function<void(double, bool, const std::string&)>& cb);
    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    
    std::function<void(double, bool, const std::string&)> _anotherSignalCallback;
    
    
};