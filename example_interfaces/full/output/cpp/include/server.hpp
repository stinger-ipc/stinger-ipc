
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

class ExampleServer {

public:
    static constexpr const char NAME[] = "Example";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    ExampleServer(std::shared_ptr<IBrokerConnection> broker);

    virtual ~ExampleServer() = default;

    void ReceiveMessage(const std::string& topic, const std::string& payload);
    
    boost::future<bool> emitTodayIsSignal(int, DayOfTheWeek);
    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    
};