
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
#include "return_types.hpp"

class ExampleClient {

public:
    static constexpr const char NAME[] = "Example";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    ExampleClient(std::shared_ptr<IBrokerConnection> broker);

    virtual ~ExampleClient() = default;

    
    void registerTodayIsCallback(const std::function<void(int, DayOfTheWeek)>& cb);
    

    
    boost::future<int> addNumbers(int first, int second) const;
    
    boost::future<DoSomethingReturnValue> doSomething(const std::string& aString) const;
    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(const std::string& topic, const std::string& payload);
    
    std::function<void(int, DayOfTheWeek)> _todayIsCallback;
    
    
};