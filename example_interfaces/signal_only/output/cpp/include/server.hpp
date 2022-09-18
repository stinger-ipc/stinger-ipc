
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

class SignalOnlyServer {

public:
    static constexpr const char NAME[] = "SignalOnly";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    SignalOnlyServer(std::shared_ptr<IBrokerConnection> broker);

    virtual ~SignalOnlyServer() = default;

    
    boost::future<bool> emitAnotherSignalSignal(double, bool, const std::string&);
    

    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(const std::string& topic, const std::string& payload);

    

};