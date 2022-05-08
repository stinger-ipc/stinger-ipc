
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


boost::future<bool> ExampleServer::emitTodayIsSignal(int dayOfMonth, DayOfTheWeek dayOfWeek) {
    rapidjson::Document doc;
    doc.SetObject();
    
    doc.AddMember("dayOfMonth", dayOfMonth, doc.GetAllocator());
    
    doc.AddMember("dayOfWeek", static_cast<int>(dayOfWeek), doc.GetAllocator());
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    return _broker->Publish("Example/signal/todayIs", buf.GetString(), 1, false);
}
