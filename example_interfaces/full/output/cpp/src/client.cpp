

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
namespace full {

constexpr const char FullClient::NAME[];
constexpr const char FullClient::INTERFACE_VERSION[];

FullClient::FullClient(std::shared_ptr<stinger::utils::IConnection> broker, const InstanceInfo& instanceInfo):
    _broker(broker), _instanceId(instanceInfo.serviceId.value_or("error_service_id_not_found")), _instanceInfo(instanceInfo)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](const stinger::utils::MqttMessage& msg)
                                                               {
                                                                   _receiveMessage(msg);
                                                               });

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicArgs["interface_name"] = NAME;
    topicArgs["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto todayIsTopic = stinger::utils::format("{prefix}/Full/{service_id}/signal/todayIs", topicArgs);
    _todayIsSignalSubscriptionId = _broker->Subscribe(todayIsTopic, 2);
    auto randomWordTopic = stinger::utils::format("{prefix}/Full/{service_id}/signal/randomWord", topicArgs);
    _randomWordSignalSubscriptionId = _broker->Subscribe(randomWordTopic, 2);
    { // Restrict scope
        auto addNumbersRequestTopic = stinger::utils::format("{prefix}/Full/{service_id}/method/addNumbers/request", topicArgs);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(addNumbersRequestTopic, topicArgs);
        _addNumbersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto doSomethingRequestTopic = stinger::utils::format("{prefix}/Full/{service_id}/method/doSomething/request", topicArgs);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(doSomethingRequestTopic, topicArgs);
        _doSomethingMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto whatTimeIsItRequestTopic = stinger::utils::format("{prefix}/Full/{service_id}/method/what_time_is_it/request", topicArgs);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(whatTimeIsItRequestTopic, topicArgs);
        _whatTimeIsItMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto holdTemperatureRequestTopic = stinger::utils::format("{prefix}/Full/{service_id}/method/hold_temperature/request", topicArgs);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(holdTemperatureRequestTopic, topicArgs);
        _holdTemperatureMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    auto favoriteNumberValueTopic = stinger::utils::format("{prefix}/Full/{service_id}/property/favorite_number/value", topicArgs);
    _favoriteNumberPropertySubscriptionId = _broker->Subscribe(favoriteNumberValueTopic, 1);
    auto favoriteFoodsValueTopic = stinger::utils::format("{prefix}/Full/{service_id}/property/favorite_foods/value", topicArgs);
    _favoriteFoodsPropertySubscriptionId = _broker->Subscribe(favoriteFoodsValueTopic, 1);
    auto lunchMenuValueTopic = stinger::utils::format("{prefix}/Full/{service_id}/property/lunch_menu/value", topicArgs);
    _lunchMenuPropertySubscriptionId = _broker->Subscribe(lunchMenuValueTopic, 1);
    auto familyNameValueTopic = stinger::utils::format("{prefix}/Full/{service_id}/property/family_name/value", topicArgs);
    _familyNamePropertySubscriptionId = _broker->Subscribe(familyNameValueTopic, 1);
    auto lastBreakfastTimeValueTopic = stinger::utils::format("{prefix}/Full/{service_id}/property/last_breakfast_time/value", topicArgs);
    _lastBreakfastTimePropertySubscriptionId = _broker->Subscribe(lastBreakfastTimeValueTopic, 1);
    auto lastBirthdaysValueTopic = stinger::utils::format("{prefix}/Full/{service_id}/property/last_birthdays/value", topicArgs);
    _lastBirthdaysPropertySubscriptionId = _broker->Subscribe(lastBirthdaysValueTopic, 1);
}

FullClient::~FullClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void FullClient::_receiveMessage(const stinger::utils::MqttMessage& msg)
{
    const int noSubId = -1;
    int subscriptionId = msg.mqttProps.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", msg.topic.c_str(), subscriptionId);
    if (subscriptionId == _todayIsSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling todayIs signal");
        rapidjson::Document doc;
        try {
            if (_todayIsSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse todayIs signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                int tempDayOfMonth;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dayOfMonth");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempDayOfMonth = itr->value.GetInt();

                    } else {
                        throw std::runtime_error("Received payload for 'todayIs' doesn't have required value/type");
                    }
                }

                DayOfTheWeek tempDayOfWeek;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dayOfWeek");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempDayOfWeek = static_cast<DayOfTheWeek>(itr->value.GetInt());

                    } else {
                        throw std::runtime_error("Received payload for 'todayIs' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_todayIsSignalCallbacksMutex);
                for (const auto& cb: _todayIsSignalCallbacks) {
                    cb(tempDayOfMonth, tempDayOfWeek);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _randomWordSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling randomWord signal");
        rapidjson::Document doc;
        try {
            if (_randomWordSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse randomWord signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::string tempWord;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("word");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempWord = itr->value.GetString();

                    } else {
                        throw std::runtime_error("Received payload for 'randomWord' doesn't have required value/type");
                    }
                }

                std::chrono::time_point<std::chrono::system_clock> tempTime;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("time");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail()) {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempTime = std::chrono::system_clock::from_time_t(std::mktime(&tm));

                    } else {
                        throw std::runtime_error("Received payload for 'randomWord' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_randomWordSignalCallbacksMutex);
                for (const auto& cb: _randomWordSignalCallbacks) {
                    cb(tempWord, tempTime);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _addNumbersMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for addNumbers response");
        _handleAddNumbersResponse(topic, payload, mqttProps);
    } else if (subscriptionId == _doSomethingMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for doSomething response");
        _handleDoSomethingResponse(topic, payload, mqttProps);
    } else if (subscriptionId == _whatTimeIsItMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for what_time_is_it response");
        _handleWhatTimeIsItResponse(topic, payload, mqttProps);
    } else if (subscriptionId == _holdTemperatureMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for hold_temperature response");
        _handleHoldTemperatureResponse(topic, payload, mqttProps);
    }
    if ((subscriptionId == _favoriteNumberPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("<bound method Property.value_topic of <stingeripc.components.Property object at 0x738693f6b770>>") % _instanceId).str())) {
        _receiveFavoriteNumberPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    } else if ((subscriptionId == _favoriteFoodsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("<bound method Property.value_topic of <stingeripc.components.Property object at 0x738695a78c50>>") % _instanceId).str())) {
        _receiveFavoriteFoodsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    } else if ((subscriptionId == _lunchMenuPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("<bound method Property.value_topic of <stingeripc.components.Property object at 0x738693fa8410>>") % _instanceId).str())) {
        _receiveLunchMenuPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    } else if ((subscriptionId == _familyNamePropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("<bound method Property.value_topic of <stingeripc.components.Property object at 0x738693fa8920>>") % _instanceId).str())) {
        _receiveFamilyNamePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    } else if ((subscriptionId == _lastBreakfastTimePropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("<bound method Property.value_topic of <stingeripc.components.Property object at 0x738693fa8950>>") % _instanceId).str())) {
        _receiveLastBreakfastTimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    } else if ((subscriptionId == _lastBirthdaysPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("<bound method Property.value_topic of <stingeripc.components.Property object at 0x738693fa8ce0>>") % _instanceId).str())) {
        _receiveLastBirthdaysPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

void FullClient::registerTodayIsCallback(const std::function<void(int, DayOfTheWeek)>& cb)
{
    std::lock_guard<std::mutex> lock(_todayIsSignalCallbacksMutex);
    _todayIsSignalCallbacks.push_back(cb);
}

void FullClient::registerRandomWordCallback(const std::function<void(std::string, std::chrono::time_point<std::chrono::system_clock>)>& cb)
{
    std::lock_guard<std::mutex> lock(_randomWordSignalCallbacksMutex);
    _randomWordSignalCallbacks.push_back(cb);
}

std::future<int> FullClient::addNumbers(int first, int second, std::optional<int> third)
{
    std::vector<std::byte> correlationId = generate_uuid_bytes();
    _pendingAddNumbersMethodCalls[correlationId] = std::promise<int>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", first, doc.GetAllocator());

    doc.AddMember("second", second, doc.GetAllocator());

    if (third)
        doc.AddMember("third", *third, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicArgs["interface_name"] = NAME;
    topicArgs["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/Full/responses", topicArgs);
    auto requestTopic = stinger::utils::format("{prefix}/Full/{service_id}/method/addNumbers/request", topicArgs);
    auto msg = stinger::utils::MqttMessage::MethodRequest(requestTopic, buf.GetString(), correlationId, responseTopic);

    _broker->Publish(msg);

    return _pendingAddNumbersMethodCalls[correlationId].get_future();
}

void FullClient::_handleAddNumbersResponse(
        const std::string& topic,
        const std::string& payload,
        const stinger::utils::MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for addNumbers");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse addNumbers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'addNumbers' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingAddNumbersMethodCalls.find(correlationId);
    if (promiseItr != _pendingAddNumbersMethodCalls.end()) {
        if (mqttProps.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(mqttProps.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(mqttProps.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = AddNumbersReturnValues::FromRapidJsonObject(doc).sum;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for addNumbers");
}

std::future<DoSomethingReturnValues> FullClient::doSomething(std::string taskToDo)
{
    std::vector<std::byte> correlationId = generate_uuid_bytes();
    _pendingDoSomethingMethodCalls[correlationId] = std::promise<DoSomethingReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(taskToDo.c_str(), taskToDo.size(), doc.GetAllocator());
        doc.AddMember("task_to_do", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicArgs["interface_name"] = NAME;
    topicArgs["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/Full/responses", topicArgs);
    auto requestTopic = stinger::utils::format("{prefix}/Full/{service_id}/method/doSomething/request", topicArgs);
    auto msg = stinger::utils::MqttMessage::MethodRequest(requestTopic, buf.GetString(), correlationId, responseTopic);

    _broker->Publish(msg);

    return _pendingDoSomethingMethodCalls[correlationId].get_future();
}

void FullClient::_handleDoSomethingResponse(
        const std::string& topic,
        const std::string& payload,
        const stinger::utils::MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for doSomething");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse doSomething signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'doSomething' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingDoSomethingMethodCalls.find(correlationId);
    if (promiseItr != _pendingDoSomethingMethodCalls.end()) {
        if (mqttProps.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(mqttProps.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(mqttProps.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = DoSomethingReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for doSomething");
}

std::future<std::chrono::time_point<std::chrono::system_clock>> FullClient::whatTimeIsIt()
{
    std::vector<std::byte> correlationId = generate_uuid_bytes();
    _pendingWhatTimeIsItMethodCalls[correlationId] = std::promise<std::chrono::time_point<std::chrono::system_clock>>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicArgs["interface_name"] = NAME;
    topicArgs["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/Full/responses", topicArgs);
    auto requestTopic = stinger::utils::format("{prefix}/Full/{service_id}/method/what_time_is_it/request", topicArgs);
    auto msg = stinger::utils::MqttMessage::MethodRequest(requestTopic, buf.GetString(), correlationId, responseTopic);

    _broker->Publish(msg);

    return _pendingWhatTimeIsItMethodCalls[correlationId].get_future();
}

void FullClient::_handleWhatTimeIsItResponse(
        const std::string& topic,
        const std::string& payload,
        const stinger::utils::MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for what_time_is_it");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse what_time_is_it signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'what_time_is_it' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingWhatTimeIsItMethodCalls.find(correlationId);
    if (promiseItr != _pendingWhatTimeIsItMethodCalls.end()) {
        if (mqttProps.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(mqttProps.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(mqttProps.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = WhatTimeIsItReturnValues::FromRapidJsonObject(doc).timestamp;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for what_time_is_it");
}

std::future<bool> FullClient::holdTemperature(double temperatureCelsius)
{
    std::vector<std::byte> correlationId = generate_uuid_bytes();
    _pendingHoldTemperatureMethodCalls[correlationId] = std::promise<bool>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("temperature_celsius", temperatureCelsius, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicArgs["interface_name"] = NAME;
    topicArgs["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/Full/responses", topicArgs);
    auto requestTopic = stinger::utils::format("{prefix}/Full/{service_id}/method/hold_temperature/request", topicArgs);
    auto msg = stinger::utils::MqttMessage::MethodRequest(requestTopic, buf.GetString(), correlationId, responseTopic);

    _broker->Publish(msg);

    return _pendingHoldTemperatureMethodCalls[correlationId].get_future();
}

void FullClient::_handleHoldTemperatureResponse(
        const std::string& topic,
        const std::string& payload,
        const stinger::utils::MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for hold_temperature");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse hold_temperature signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'hold_temperature' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingHoldTemperatureMethodCalls.find(correlationId);
    if (promiseItr != _pendingHoldTemperatureMethodCalls.end()) {
        if (mqttProps.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(mqttProps.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(mqttProps.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = HoldTemperatureReturnValues::FromRapidJsonObject(doc).success;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for hold_temperature");
}

void FullClient::_receiveFavoriteNumberPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse favorite_number property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'favorite_number' property update payload is not an object");
    }
    FavoriteNumberProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("number");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.number = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'number' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
        _favoriteNumberProperty = tempValue;
        _lastFavoriteNumberPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteNumberPropertyCallbacksMutex);
        for (const auto& cb: _favoriteNumberPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.number);
        }
    }
}

std::optional<int> FullClient::getFavoriteNumberProperty()
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
    if (_favoriteNumberProperty) {
        return _favoriteNumberProperty->number;
    }
    return std::nullopt;
}

void FullClient::registerFavoriteNumberPropertyCallback(const std::function<void(int number)>& cb)
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyCallbacksMutex);
    _favoriteNumberPropertyCallbacks.push_back(cb);
}

std::future<bool> FullClient::updateFavoriteNumberProperty(int number) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("number", number, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish("<bound method Property.update_topic of <stingeripc.components.Property object at 0x738693f6b770>>", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveFavoriteFoodsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse favorite_foods property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'favorite_foods' property update payload is not an object");
    }
    FavoriteFoodsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("drink");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.drink = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'drink' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("slices_of_pizza");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.slicesOfPizza = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'slices_of_pizza' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("breakfast");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.breakfast = itr->value.GetString();

        } else {
            tempValue.breakfast = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
        _favoriteFoodsProperty = tempValue;
        _lastFavoriteFoodsPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyCallbacksMutex);
        for (const auto& cb: _favoriteFoodsPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.drink, tempValue.slicesOfPizza, tempValue.breakfast);
        }
    }
}

std::optional<FavoriteFoodsProperty> FullClient::getFavoriteFoodsProperty()
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
    if (_favoriteFoodsProperty) {
        return *_favoriteFoodsProperty;
    }
    return std::nullopt;
}

void FullClient::registerFavoriteFoodsPropertyCallback(const std::function<void(std::string drink, int slicesOfPizza, std::optional<std::string> breakfast)>& cb)
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyCallbacksMutex);
    _favoriteFoodsPropertyCallbacks.push_back(cb);
}

std::future<bool> FullClient::updateFavoriteFoodsProperty(std::string drink, int slicesOfPizza, std::optional<std::string> breakfast) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(drink.c_str(), drink.size(), doc.GetAllocator());
        doc.AddMember("drink", tempStringValue, doc.GetAllocator());
    }

    doc.AddMember("slices_of_pizza", slicesOfPizza, doc.GetAllocator());

    if (breakfast) {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(breakfast->c_str(), breakfast->size(), doc.GetAllocator());
        doc.AddMember("breakfast", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish("<bound method Property.update_topic of <stingeripc.components.Property object at 0x738695a78c50>>", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLunchMenuPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse lunch_menu property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'lunch_menu' property update payload is not an object");
    }
    LunchMenuProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("monday");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.monday = Lunch::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'monday' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("tuesday");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.tuesday = Lunch::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'tuesday' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
        _lunchMenuProperty = tempValue;
        _lastLunchMenuPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lunchMenuPropertyCallbacksMutex);
        for (const auto& cb: _lunchMenuPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.monday, tempValue.tuesday);
        }
    }
}

std::optional<LunchMenuProperty> FullClient::getLunchMenuProperty()
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
    if (_lunchMenuProperty) {
        return *_lunchMenuProperty;
    }
    return std::nullopt;
}

void FullClient::registerLunchMenuPropertyCallback(const std::function<void(Lunch monday, Lunch tuesday)>& cb)
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyCallbacksMutex);
    _lunchMenuPropertyCallbacks.push_back(cb);
}

void FullClient::_receiveFamilyNamePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse family_name property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'family_name' property update payload is not an object");
    }
    FamilyNameProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("family_name");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.familyName = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'family_name' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
        _familyNameProperty = tempValue;
        _lastFamilyNamePropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_familyNamePropertyCallbacksMutex);
        for (const auto& cb: _familyNamePropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.familyName);
        }
    }
}

std::optional<std::string> FullClient::getFamilyNameProperty()
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
    if (_familyNameProperty) {
        return _familyNameProperty->familyName;
    }
    return std::nullopt;
}

void FullClient::registerFamilyNamePropertyCallback(const std::function<void(std::string familyName)>& cb)
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyCallbacksMutex);
    _familyNamePropertyCallbacks.push_back(cb);
}

std::future<bool> FullClient::updateFamilyNameProperty(std::string familyName) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(familyName.c_str(), familyName.size(), doc.GetAllocator());
        doc.AddMember("family_name", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish("<bound method Property.update_topic of <stingeripc.components.Property object at 0x738693fa8920>>", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLastBreakfastTimePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse last_breakfast_time property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'last_breakfast_time' property update payload is not an object");
    }
    LastBreakfastTimeProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("timestamp");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempTimestampIsoString = itr->value.GetString();
            tempValue.timestamp = stinger::utils::parseIsoTimestamp(tempTimestampIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'timestamp' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
        _lastBreakfastTimeProperty = tempValue;
        _lastLastBreakfastTimePropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyCallbacksMutex);
        for (const auto& cb: _lastBreakfastTimePropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.timestamp);
        }
    }
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> FullClient::getLastBreakfastTimeProperty()
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
    if (_lastBreakfastTimeProperty) {
        return _lastBreakfastTimeProperty->timestamp;
    }
    return std::nullopt;
}

void FullClient::registerLastBreakfastTimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> timestamp)>& cb)
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyCallbacksMutex);
    _lastBreakfastTimePropertyCallbacks.push_back(cb);
}

std::future<bool> FullClient::updateLastBreakfastTimeProperty(std::chrono::time_point<std::chrono::system_clock> timestamp) const
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
    return _broker->Publish("<bound method Property.update_topic of <stingeripc.components.Property object at 0x738693fa8950>>", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLastBirthdaysPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse last_birthdays property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'last_birthdays' property update payload is not an object");
    }
    LastBirthdaysProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("mom");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempMomIsoString = itr->value.GetString();
            tempValue.mom = stinger::utils::parseIsoTimestamp(tempMomIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'mom' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dad");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempDadIsoString = itr->value.GetString();
            tempValue.dad = stinger::utils::parseIsoTimestamp(tempDadIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'dad' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("sister");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempSisterIsoString = itr->value.GetString();
            tempValue.sister = stinger::utils::parseIsoTimestamp(tempSisterIsoString);

        } else {
            tempValue.sister = std::nullopt;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("brothers_age");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.brothersAge = itr->value.GetInt();

        } else {
            tempValue.brothersAge = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
        _lastBirthdaysProperty = tempValue;
        _lastLastBirthdaysPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyCallbacksMutex);
        for (const auto& cb: _lastBirthdaysPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.mom, tempValue.dad, tempValue.sister, tempValue.brothersAge);
        }
    }
}

std::optional<LastBirthdaysProperty> FullClient::getLastBirthdaysProperty()
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
    if (_lastBirthdaysProperty) {
        return *_lastBirthdaysProperty;
    }
    return std::nullopt;
}

void FullClient::registerLastBirthdaysPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, std::optional<std::chrono::time_point<std::chrono::system_clock>> sister, std::optional<int> brothersAge)>& cb)
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyCallbacksMutex);
    _lastBirthdaysPropertyCallbacks.push_back(cb);
}

std::future<bool> FullClient::updateLastBirthdaysProperty(std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, std::optional<std::chrono::time_point<std::chrono::system_clock>> sister, std::optional<int> brothersAge) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempMomStringValue;
        std::string momIsoString = stinger::utils::timePointToIsoString(mom);
        tempMomStringValue.SetString(momIsoString.c_str(), momIsoString.size(), doc.GetAllocator());
        doc.AddMember("mom", tempMomStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempDadStringValue;
        std::string dadIsoString = stinger::utils::timePointToIsoString(dad);
        tempDadStringValue.SetString(dadIsoString.c_str(), dadIsoString.size(), doc.GetAllocator());
        doc.AddMember("dad", tempDadStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempSisterStringValue;
        std::string sisterIsoString = stinger::utils::timePointToIsoString(*sister);
        tempSisterStringValue.SetString(sisterIsoString.c_str(), sisterIsoString.size(), doc.GetAllocator());
        doc.AddMember("sister", tempSisterStringValue, doc.GetAllocator());
    }

    if (brothersAge)
        doc.AddMember("brothers_age", *brothersAge, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    stinger::utils::MqttProperties mqttProps;
    return _broker->Publish("<bound method Property.update_topic of <stingeripc.components.Property object at 0x738693fa8ce0>>", buf.GetString(), 1, false, mqttProps);
}

} // namespace full

} // namespace gen

} // namespace stinger
