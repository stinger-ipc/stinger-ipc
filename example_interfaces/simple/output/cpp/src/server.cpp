

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
#include "ibrokerconnection.hpp"

constexpr const char SimpleServer::NAME[];
constexpr const char SimpleServer::INTERFACE_VERSION[];

SimpleServer::SimpleServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId):
    _broker(broker), _instanceId(instanceId), _advertisementThreadRunning(false)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _receiveMessage(topic, payload, mqttProps);
                                                               });

    _tradeNumbersMethodSubscriptionId = _broker->Subscribe((format("simple/%1%/method/tradeNumbers") % _instanceId).str(), 2);

    _schoolPropertySubscriptionId = _broker->Subscribe((format("simple/%1%/property/school/setValue") % _instanceId).str(), 1);

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&SimpleServer::_advertisementThreadLoop, this);
}

SimpleServer::~SimpleServer()
{
    // Unregister the message callback from the broker.
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }

    // Stop the advertisement thread
    _advertisementThreadRunning = false;
    if (_advertisementThread.joinable())
    {
        _advertisementThread.join();
    }

    std::string topic = (format("simple/%1%/interface") % _instanceId).str();
    _broker->Publish(topic, "", 1, true, MqttProperties());

    _broker->Unsubscribe((format("simple/%1%/method/tradeNumbers") % _instanceId).str());

    _broker->Unsubscribe((format("simple/%1%/property/school/setValue") % _instanceId).str());
}

void SimpleServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);

    if ((subscriptionId == _tradeNumbersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("simple/%1%/method/tradeNumbers") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as trade_numbers method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_tradeNumbersHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callTradeNumbersHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const std::exception&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    if (subscriptionId == _schoolPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("simple/%1%/property/school/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as school property update.", topic.c_str());
        _receiveSchoolPropertyUpdate(topic, payload, mqttProps.propertyVersion);
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
    MqttProperties mqttProps;
    return _broker->Publish((format("simple/%1%/signal/personEntered") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void SimpleServer::registerTradeNumbersHandler(std::function<int(int)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle simple/+/method/tradeNumbers method requests.");
    _tradeNumbersHandler = func;
}

void SimpleServer::_callTradeNumbersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::string> optCorrelationId,
        const std::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to trade_numbers");
    if (!_tradeNumbersHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = TradeNumbersRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _tradeNumbersHandler(requestArgs.yourNumber);
    TradeNumbersReturnValues returnValues = { returnValue };

    if (optResponseTopic)
    {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);
        MqttProperties mqttProps;
        mqttProps.correlationId = optCorrelationId;
        mqttProps.returnCode = MethodReturnCode::SUCCESS;
        _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
    }
}

std::optional<std::string> SimpleServer::getSchoolProperty()
{
    std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
    if (_schoolProperty)
    {
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
        for (const auto& cb: _schoolPropertyCallbacks)
        {
            cb(name);
        }
    }
    republishSchoolProperty();
}

void SimpleServer::republishSchoolProperty() const
{
    std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
    rapidjson::Document doc;
    if (_schoolProperty)
    {
        doc.SetObject();
        _schoolProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastSchoolPropertyVersion;
    _broker->Publish((format("simple/%1%/property/school/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void SimpleServer::_receiveSchoolPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse school property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
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
    while (_advertisementThreadRunning)
    {
        // Get current timestamp
        auto now = std::chrono::system_clock::now();
        std::string timestamp = timePointToIsoString(now);

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

        // Convert to JSON string
        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        doc.Accept(writer);

        // Create MQTT properties with message expiry interval of 150 seconds
        MqttProperties mqttProps;
        mqttProps.messageExpiryInterval = 150;

        // Publish to simple/<instance_id>/interface
        std::string topic = (format("simple/%1%/interface") % _instanceId).str();
        _broker->Publish(topic, buf.GetString(), 1, true, mqttProps);

        _broker->Log(LOG_INFO, "Published service advertisement to %s", topic.c_str());

        // Wait for 120 seconds or until thread should stop
        // Use smaller sleep intervals to allow quick shutdown
        for (int i = 0; i < 120 && _advertisementThreadRunning; ++i)
        {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
}
