

#include <vector>
#include <iostream>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <syslog.h>
#include <sstream>
#include "utils.hpp"
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "client.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"
#include "interface_exceptions.hpp"

constexpr const char SimpleClient::NAME[];
constexpr const char SimpleClient::INTERFACE_VERSION[];

SimpleClient::SimpleClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId):
    _broker(broker), _instanceId(instanceId)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _receiveMessage(topic, payload, mqttProps);
                                                               });
    _personEnteredSignalSubscriptionId = _broker->Subscribe((format("simple/%1%/signal/personEntered") % _instanceId).str(), 2);
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/tradeNumbers/methodResponse") % _broker->GetClientId();
        _tradeNumbersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    _schoolPropertySubscriptionId = _broker->Subscribe((format("simple/%1%/property/school/value") % _instanceId).str(), 1);
}

SimpleClient::~SimpleClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void SimpleClient::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", topic.c_str(), subscriptionId);
    if ((subscriptionId == _personEnteredSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("simple/%1%/signal/personEntered") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling person_entered signal");
        rapidjson::Document doc;
        try
        {
            if (_personEnteredSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse person_entered signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                Person tempPerson;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("person");
                    if (itr != doc.MemberEnd() && itr->value.IsObject())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'person_entered' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_personEnteredSignalCallbacksMutex);
                for (const auto& cb: _personEnteredSignalCallbacks)
                {
                    cb(tempPerson);
                }
            }
        }
        catch (const std::exception&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if ((subscriptionId == _tradeNumbersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/tradeNumbers/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for trade_numbers response");
        _handleTradeNumbersResponse(topic, payload, mqttProps);
    }
    if ((subscriptionId == _schoolPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("simple/%1%/property/school/value") % _instanceId).str()))
    {
        _receiveSchoolPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

void SimpleClient::registerPersonEnteredCallback(const std::function<void(Person)>& cb)
{
    std::lock_guard<std::mutex> lock(_personEnteredSignalCallbacksMutex);
    _personEnteredSignalCallbacks.push_back(cb);
}

std::future<int> SimpleClient::tradeNumbers(int yourNumber)
{
    auto correlationId = generate_uuid_string();
    _pendingTradeNumbersMethodCalls[correlationId] = std::promise<int>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("your_number", yourNumber, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/tradeNumbers/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("simple/%1%/method/tradeNumbers") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingTradeNumbersMethodCalls[correlationId].get_future();
}

void SimpleClient::_handleTradeNumbersResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for trade_numbers");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse trade_numbers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'trade_numbers' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingTradeNumbersMethodCalls.find(correlationId);
    if (promiseItr != _pendingTradeNumbersMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = TradeNumbersReturnValues::FromRapidJsonObject(doc).myNumber;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for trade_numbers");
}

void SimpleClient::_receiveSchoolPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse school property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'school' property update payload is not an object");
    }
    SchoolProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("name");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.name = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'name' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
        _schoolProperty = tempValue;
        _lastSchoolPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_schoolPropertyCallbacksMutex);
        for (const auto& cb: _schoolPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.name);
        }
    }
}

std::optional<std::string&> SimpleClient::getSchoolProperty()
{
    std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
    if (_schoolProperty)
    {
        return _schoolProperty->name;
    }
    return std::nullopt;
}

void SimpleClient::registerSchoolPropertyCallback(const std::function<void(std::string name)>& cb)
{
    std::lock_guard<std::mutex> lock(_schoolPropertyCallbacksMutex);
    _schoolPropertyCallbacks.push_back(cb);
}

std::future<bool> SimpleClient::updateSchoolProperty(std::string name) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(name.c_str(), name.size(), doc.GetAllocator());
        doc.AddMember("name", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("simple/%1%/property/school/setValue", buf.GetString(), 1, false, mqttProps);
}
