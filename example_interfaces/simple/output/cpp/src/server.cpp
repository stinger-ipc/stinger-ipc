
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
#include <stinger/error/return_codes.hpp>

namespace stinger {

namespace gen {
namespace simple {

constexpr const char SimpleServer::NAME[];
constexpr const char SimpleServer::INTERFACE_VERSION[];

SimpleServer::SimpleServer(std::shared_ptr<stinger::utils::IConnection> broker, const std::string& instanceId, const std::string& prefix):
    _broker(broker), _instanceId(instanceId), _advertisementThreadRunning(false), _prefixTopicParam(prefix)

{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const stinger::mqtt::Message& msg
                                                               )
                                                               {
                                                                   _receiveMessage(msg);
                                                               });

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["prefix"] = _prefixTopicParam;

    _tradeNumbersMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Simple/{service_id}/method/trade_numbers/request", topicArgs), 2);

    _schoolPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Simple/{service_id}/property/school/update", topicArgs), 1);

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&SimpleServer::_advertisementThreadLoop, this);
}

SimpleServer::~SimpleServer()
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["prefix"] = _prefixTopicParam;

    std::string topic = stinger::utils::format("{prefix}/Simple/{service_id}/interface", topicArgs);
    auto msg = stinger::mqtt::Message::ServiceOffline(topic);
    _broker->Publish(msg);

    _broker->Unsubscribe(stinger::utils::format("{prefix}/Simple/{service_id}/method/trade_numbers/request", topicArgs));

    _broker->Unsubscribe(stinger::utils::format("{prefix}/Simple/{service_id}/property/school/update", topicArgs));
}

void SimpleServer::_receiveMessage(const stinger::mqtt::Message& msg)
{
    const int noSubId = -1;
    int subscriptionId = msg.properties.subscriptionId.value_or(noSubId);

    if (subscriptionId == _tradeNumbersMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as trade_numbers method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_tradeNumbersHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callTradeNumbersHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    if (subscriptionId == _schoolPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as school property update.", msg.topic.c_str());
        _receiveSchoolPropertyUpdate(msg);
    }
}

std::future<bool> SimpleServer::emitPersonEnteredSignal(Person person)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        person.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("person", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "person_entered";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/Simple/{service_id}/signal/person_entered", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

void SimpleServer::registerTradeNumbersHandler(std::function<int(int)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _tradeNumbersHandler = func;
}

void SimpleServer::_callTradeNumbersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to trade_numbers");
    if (!_tradeNumbersHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = TradeNumbersRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _tradeNumbersHandler(requestArgs.yourNumber);
    TradeNumbersReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

std::optional<std::string> SimpleServer::getSchoolProperty()
{
    std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
    if (_schoolProperty) {
        return _schoolProperty->name;
    }
    return std::nullopt;
}

void SimpleServer::registerSchoolPropertyCallback(const std::function<void(std::string name)>& cb)
{
    std::lock_guard<std::mutex> lock(_schoolPropertyCallbacksMutex);
    _schoolPropertyCallbacks.push_back(cb);
}

void SimpleServer::updateSchoolProperty(std::string name)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
        _schoolProperty = SchoolProperty{ name };
        _lastSchoolPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_schoolPropertyCallbacksMutex);
        for (const auto& cb: _schoolPropertyCallbacks) {
            cb(name);
        }
    }
    republishSchoolProperty();
}

void SimpleServer::republishSchoolProperty() const
{
    std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
    rapidjson::Document doc;
    if (_schoolProperty) {
        doc.SetObject();
        _schoolProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "school";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/Simple/{service_id}/property/school/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastSchoolPropertyVersion);
    _broker->Publish(msg);
}

void SimpleServer::_receiveSchoolPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse school property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received school payload is not an object or null");
    }

    // TODO: Check _lastSchoolPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    SchoolProperty tempValue = SchoolProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
        _schoolProperty = tempValue;
        _lastSchoolPropertyVersion++;
    }
    republishSchoolProperty();
}

void SimpleServer::_advertisementThreadLoop()
{
    while (_advertisementThreadRunning) {
        // Get current timestamp
        auto now = std::chrono::system_clock::now();
        std::string timestamp = stinger::utils::timePointToIsoString(now);

        // Build JSON message
        rapidjson::Document doc;
        doc.SetObject();
        rapidjson::Document::AllocatorType& allocator = doc.GetAllocator();

        doc.AddMember("interface_name", rapidjson::Value("Simple", allocator), allocator);
        doc.AddMember("instance", rapidjson::Value(_instanceId.c_str(), allocator), allocator);
        doc.AddMember("title", rapidjson::Value("Simple Example Interface", allocator), allocator);
        doc.AddMember("version", rapidjson::Value("0.0.1", allocator), allocator);
        doc.AddMember("connection_topic", rapidjson::Value(_broker->GetOnlineTopic().c_str(), allocator), allocator);
        doc.AddMember("timestamp", rapidjson::Value(timestamp.c_str(), allocator), allocator);

        doc.AddMember("prefix", rapidjson::Value(_prefixTopicParam.c_str(), allocator), allocator);

        // Convert to JSON string
        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        doc.Accept(writer);

        std::map<std::string, std::string> topicArgs;
        topicArgs["service_id"] = _instanceId;
        topicArgs["interface_name"] = NAME;
        topicArgs["client_id"] = _broker->GetClientId();
        topicArgs["prefix"] = _prefixTopicParam;

        // Publish to "{prefix}/Simple/{service_id}/interface"
        std::string topic = stinger::utils::format("{prefix}/Simple/{service_id}/interface", topicArgs);
        auto msg = stinger::mqtt::Message::ServiceOnline(topic, buf.GetString(), 120);
        _broker->Publish(msg);

        _broker->Log(LOG_INFO, "Published service advertisement to %s", topic.c_str());

        // Wait for 120 seconds or until thread should stop
        // Use smaller sleep intervals to allow quick shutdown
        for (int i = 0; i < 120 && _advertisementThreadRunning; ++i) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
}

} // namespace simple

} // namespace gen

} // namespace stinger
