
#include <vector>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>

#include "server.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"


constexpr const char ExampleServer::NAME[];
constexpr const char ExampleServer::INTERFACE_VERSION[];

ExampleServer::ExampleServer(std::shared_ptr<IBrokerConnection> broker) : _broker(broker) {
    _broker->AddMessageCallback([this](const std::string& topic, const std::string& payload)
    {
        ReceiveMessage(topic, payload);
    });
}

void ExampleServer::ReceiveMessage(const std::string& topic, const std::string& payload) {
  
}


void ExampleServer::emitTodayIsSignal(int, DayOfTheWeek) {
    std::string payload("");
    _broker->Publish("Example/signal/todayIs", payload, 1, false);
}
