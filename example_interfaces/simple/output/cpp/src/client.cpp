

#include <vector>
#include <iostream>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <syslog.h>
#include <sstream>
#include <stinger/utils/iconnection.hpp>
#include <stinger/utils/uuid.hpp>
#include <stinger/utils/format.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "client.hpp"
#include "enums.hpp"
#include "discovery.hpp"

namespace stinger {

namespace gen {
namespace simple {

constexpr const char SimpleClient::NAME[];
constexpr const char SimpleClient::INTERFACE_VERSION[];

SimpleClient::SimpleClient(std::shared_ptr<stinger::utils::IConnection> broker, const InstanceInfo& instanceInfo):
    _broker(broker), _instanceId(instanceInfo.serviceId.value_or("error_service_id_not_found")), _instanceInfo(instanceInfo)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](const stinger::mqtt::Message& msg)
                                                               {
                                                                   _receiveMessage(msg);
                                                               });

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto personEnteredTopic = stinger::utils::format("{prefix}/Simple/{service_id}/signal/person_entered", topicParams);
    _personEnteredSignalSubscriptionId = _broker->Subscribe(personEnteredTopic, 2);
    { // Restrict scope
        auto tradeNumbersRequestTopic = stinger::utils::format("{prefix}/Simple/{service_id}/method/trade_numbers/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(tradeNumbersRequestTopic, topicParams);
        _tradeNumbersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    auto schoolValueTopic = stinger::utils::format("{prefix}/Simple/{service_id}/property/school/value", topicParams);
    _schoolPropertySubscriptionId = _broker->Subscribe(schoolValueTopic, 1);

    auto anyPropertyUpdateResponseTopic = stinger::utils::format("client/{client_id}/Simple/property/+/update/response", topicParams);
    _anyPropertyUpdateResponseSubscriptionId = _broker->Subscribe(anyPropertyUpdateResponseTopic, 1);
}

SimpleClient::~SimpleClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void SimpleClient::_receiveMessage(const stinger::mqtt::Message& msg)
{
    const int noSubId = -1;
    int subscriptionId = msg.properties.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", msg.topic.c_str(), subscriptionId);
    if (subscriptionId == _personEnteredSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling person_entered signal");
        rapidjson::Document doc;
        try {
            if (_personEnteredSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse person_entered signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                Person tempPerson;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("person");
                    if (itr != doc.MemberEnd() && itr->value.IsObject()) {
                    } else {
                        throw std::runtime_error("Received payload for 'person_entered' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_personEnteredSignalCallbacksMutex);
                for (const auto& cb: _personEnteredSignalCallbacks) {
                    cb(tempPerson);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _tradeNumbersMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for trade_numbers response");
        _handleTradeNumbersResponse(msg);
    }
    if (subscriptionId == _schoolPropertySubscriptionId) {
        _receiveSchoolPropertyUpdate(msg);
    } else if (subscriptionId == _anyPropertyUpdateResponseSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for any property update response");
    }
}

void SimpleClient::registerPersonEnteredCallback(const std::function<void(Person)>& cb)
{
    std::lock_guard<std::mutex> lock(_personEnteredSignalCallbacksMutex);
    _personEnteredSignalCallbacks.push_back(cb);
}

std::future<int> SimpleClient::tradeNumbers(int yourNumber)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingTradeNumbersMethodCalls[correlationData] = std::promise<int>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("your_number", yourNumber, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/Simple/method/trade_numbers/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/Simple/{service_id}/method/trade_numbers/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingTradeNumbersMethodCalls[correlationData].get_future();
}

void SimpleClient::_handleTradeNumbersResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for trade_numbers");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse trade_numbers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'trade_numbers' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingTradeNumbersMethodCalls.find(correlationData);
    if (promiseItr != _pendingTradeNumbersMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = TradeNumbersReturnValues::FromRapidJsonObject(doc).myNumber;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for trade_numbers");
}

void SimpleClient::_receiveSchoolPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse school property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'school' property update payload is not an object");
    }
    SchoolProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("name");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.name = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'name' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
        _schoolProperty = tempValue;
        _lastSchoolPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_schoolPropertyCallbacksMutex);
        for (const auto& cb: _schoolPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.name);
        }
    }
}

std::optional<std::string> SimpleClient::getSchoolProperty()
{
    std::lock_guard<std::mutex> lock(_schoolPropertyMutex);
    if (_schoolProperty) {
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

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/Simple/{service_id}/property/school/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/Simple/property/school/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastSchoolPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

} // namespace simple

} // namespace gen

} // namespace stinger
