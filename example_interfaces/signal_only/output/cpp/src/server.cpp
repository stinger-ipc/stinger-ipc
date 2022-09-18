
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
        _receiveMessage(topic, payload);
    });
}

void SignalOnlyServer::_receiveMessage(const std::string& topic, const std::string& payload)
{
    
}


boost::future<bool> SignalOnlyServer::emitAnotherSignalSignal(double one, bool two, const std::string& three)
{
    rapidjson::Document doc;
    doc.SetObject();
    
    doc.AddMember("one", one, doc.GetAllocator());
    
    doc.AddMember("two", two, doc.GetAllocator());
    
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(three.c_str(), three.size(), doc.GetAllocator());
        doc.AddMember("three", tempStringValue, doc.GetAllocator());
    }
    
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    return _broker->Publish("SignalOnly/signal/anotherSignal", buf.GetString(), 1, false);
}




