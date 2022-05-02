
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

class ExampleClient {

public:
    static constexpr const char NAME[] = "Example";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    ExampleClient(std::shared_ptr<IBrokerConnection> broker);

    virtual ~ExampleClient() = default;

    void ReceiveMessage(const std::string& topic, const std::string& payload);
    
    void registerTodayIsCallback(const std::function<void(int, DayOfTheWeek)>& cb);
    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    
    std::function<void(int, DayOfTheWeek)> _todayIsCallback;
    
    
};