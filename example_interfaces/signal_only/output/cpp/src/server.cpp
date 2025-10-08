

#include <vector>
#include <iostream>
#include <syslog.h>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "server.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"

constexpr const char SignalOnlyServer::NAME[];
constexpr const char SignalOnlyServer::INTERFACE_VERSION[];

SignalOnlyServer::SignalOnlyServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId)
    : _broker(broker)
    , _instanceId(instanceId)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _receiveMessage(topic, payload, mqttProps);
                                                               });
}

SignalOnlyServer::~SignalOnlyServer()
{
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void SignalOnlyServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);
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
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("signalOnly/%1%/signal/anotherSignal") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> SignalOnlyServer::emitBarkSignal(const std::string& word)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(word.c_str(), word.size(), doc.GetAllocator());
        doc.AddMember("word", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("signalOnly/%1%/signal/bark") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> SignalOnlyServer::emitMaybeNumberSignal(boost::optional<int> number)
{
    rapidjson::Document doc;
    doc.SetObject();
    if (number)
        doc.AddMember("number", *number, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("signalOnly/%1%/signal/maybeNumber") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> SignalOnlyServer::emitMaybeNameSignal(boost::optional<std::string> name)
{
    rapidjson::Document doc;
    doc.SetObject();
    if (name)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(name->c_str(), name->size(), doc.GetAllocator());
        doc.AddMember("name", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("signalOnly/%1%/signal/maybeName") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> SignalOnlyServer::emitNowSignal(std::chrono::time_point<std::chrono::system_clock> timestamp)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), doc.GetAllocator());
        doc.AddMember("timestamp", tempTimestampStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("signalOnly/%1%/signal/now") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}
