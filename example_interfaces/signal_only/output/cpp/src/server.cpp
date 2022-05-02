
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


constexpr const char SignalOnlyServer::NAME[];
constexpr const char SignalOnlyServer::INTERFACE_VERSION[];

SignalOnlyServer::SignalOnlyServer(std::shared_ptr<IBrokerConnection> broker) : _broker(broker) {
    _broker->AddMessageCallback([this](const std::string& topic, const std::string& payload)
    {
        ReceiveMessage(topic, payload);
    });
}

void SignalOnlyServer::ReceiveMessage(const std::string& topic, const std::string& payload) {
  
}


void SignalOnlyServer::emitAnotherSignalSignal(double, bool, const std::string&) {
    std::string payload("");
    _broker->Publish("SignalOnly/signal/anotherSignal", payload, 1, false);
}
