

#include <vector>
#include <iostream>
#include <syslog.h>

#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "server.hpp"
#include "method_payloads.hpp"
#include "enums.hpp"
#include <stinger/utils/iconnection.hpp>
#include <stinger/utils/format.hpp>

namespace stinger {

namespace gen {
namespace signal_only {

constexpr const char SignalOnlyServer::NAME[];
constexpr const char SignalOnlyServer::INTERFACE_VERSION[];

SignalOnlyServer::SignalOnlyServer(std::shared_ptr<stinger::utils::IConnection> broker, const std::string& instanceId, const std::string& prefix):
    _broker(broker), _instanceId(instanceId), _advertisementThreadRunning(false), _prefixTopicParam(prefix),

{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const stinger::utils::MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _receiveMessage(topic, payload, mqttProps);
                                                               });

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["prefix"] = _prefixTopicParam;

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&SignalOnlyServer::_advertisementThreadLoop, this);
}

SignalOnlyServer::~SignalOnlyServer()
{
    // Unregister the message callback from the broker.
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }

    // Stop the advertisement thread
    _advertisementThreadRunning = false;
    if (_advertisementThread.joinable()) {
        _advertisementThread.join();
    }

    std::string topic = (format("<bound method StingerSpec.interface_info_topic of <stingeripc.components.StingerSpec object at 0x7fa113d84e60>>") % _instanceId).str();
    _broker->Publish(topic, "", 1, true, stinger::utils::MqttProperties());
}

void SignalOnlyServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const stinger::utils::MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);
}

std::future<bool> SignalOnlyServer::emitAnotherSignalSignal(double one, bool two, std::string three)
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
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish((format("<bound method Signal.topic of <stingeripc.components.Signal object at 0x7fa113ed1d30>>") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

std::future<bool> SignalOnlyServer::emitBarkSignal(std::string word)
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
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish((format("<bound method Signal.topic of <stingeripc.components.Signal object at 0x7fa115065d00>>") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

std::future<bool> SignalOnlyServer::emitMaybeNumberSignal(std::optional<int> number)
{
    rapidjson::Document doc;
    doc.SetObject();
    if (number)
        doc.AddMember("number", *number, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish((format("<bound method Signal.topic of <stingeripc.components.Signal object at 0x7fa11324ef90>>") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

std::future<bool> SignalOnlyServer::emitMaybeNameSignal(std::optional<std::string> name)
{
    rapidjson::Document doc;
    doc.SetObject();
    if (name) {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(name->c_str(), name->size(), doc.GetAllocator());
        doc.AddMember("name", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish((format("<bound method Signal.topic of <stingeripc.components.Signal object at 0x7fa11324f440>>") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

std::future<bool> SignalOnlyServer::emitNowSignal(std::chrono::time_point<std::chrono::system_clock> timestamp)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = stinger::utils::timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), doc.GetAllocator());
        doc.AddMember("timestamp", tempTimestampStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish((format("<bound method Signal.topic of <stingeripc.components.Signal object at 0x7fa11324f5c0>>") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void SignalOnlyServer::_advertisementThreadLoop()
{
    while (_advertisementThreadRunning) {
        // Get current timestamp
        auto now = std::chrono::system_clock::now();
        std::string timestamp = stinger::utils::timePointToIsoString(now);

        // Build JSON message
        rapidjson::Document doc;
        doc.SetObject();
        rapidjson::Document::AllocatorType& allocator = doc.GetAllocator();

        doc.AddMember("interface_name", rapidjson::Value("SignalOnly", allocator), allocator);
        doc.AddMember("instance", rapidjson::Value(_instanceId.c_str(), allocator), allocator);
        doc.AddMember("title", rapidjson::Value("SignalOnly", allocator), allocator);
        doc.AddMember("version", rapidjson::Value("0.0.1", allocator), allocator);
        doc.AddMember("connection_topic", rapidjson::Value(_broker->GetOnlineTopic().c_str(), allocator), allocator);
        doc.AddMember("timestamp", rapidjson::Value(timestamp.c_str(), allocator), allocator);

        // Convert to JSON string
        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        doc.Accept(writer);

        // Create MQTT properties with message expiry interval of 150 seconds
        stinger::utils::MqttProperties mqttProps;
        mqttProps.messageExpiryInterval = 150;

        // Publish to <bound method StingerSpec.interface_info_topic of <stingeripc.components.StingerSpec object at 0x7fa113d84e60>>
        std::string topic = (format("<bound method StingerSpec.interface_info_topic of <stingeripc.components.StingerSpec object at 0x7fa113d84e60>>") % _instanceId).str();
        _broker->Publish(topic, buf.GetString(), 1, true, mqttProps);

        _broker->Log(LOG_INFO, "Published service advertisement to %s", topic.c_str());

        // Wait for 120 seconds or until thread should stop
        // Use smaller sleep intervals to allow quick shutdown
        for (int i = 0; i < 120 && _advertisementThreadRunning; ++i) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
}

} // namespace signal_only

} // namespace gen

} // namespace stinger
