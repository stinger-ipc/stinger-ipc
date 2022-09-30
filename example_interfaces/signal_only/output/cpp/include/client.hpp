
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
    static constexpr const char NAME[] = "SignalOnly";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    SignalOnlyClient(std::shared_ptr<IBrokerConnection> broker);

    virtual ~SignalOnlyClient() = default;

    
    void registerAnotherSignalCallback(const std::function<void(double, bool, const std::string&)>& cb);
    

    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(const std::string& topic, const std::string& payload);
    
    std::function<void(double, bool, const std::string&)> _anotherSignalCallback;
    
    
};