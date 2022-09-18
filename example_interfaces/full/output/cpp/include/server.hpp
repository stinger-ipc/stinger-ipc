
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

    
    boost::future<bool> emitTodayIsSignal(int, DayOfTheWeek);
    

    
    void registerAddNumbersHandler(std::function<int(int, int)> func);
    
private: 
    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(const std::string& topic, const std::string& payload);

    
    void _calladdNumbersHandler(const std::string& topic, const rapidjson::Document& doc);
    std::function<int(int, int)> _addNumbersHandler;
    

};