

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
namespace signal_only {

constexpr const char SignalOnlyClient::NAME[];
constexpr const char SignalOnlyClient::INTERFACE_VERSION[];

SignalOnlyClient::SignalOnlyClient(std::shared_ptr<stinger::utils::IConnection> broker, const InstanceInfo& instanceInfo):
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

    auto anotherSignalTopic = stinger::utils::format("{prefix}/SignalOnly/{service_id}/signal/anotherSignal", topicArgs);
    _anotherSignalSignalSubscriptionId = _broker->Subscribe(anotherSignalTopic, 2);
    auto barkTopic = stinger::utils::format("{prefix}/SignalOnly/{service_id}/signal/bark", topicArgs);
    _barkSignalSubscriptionId = _broker->Subscribe(barkTopic, 2);
    auto maybeNumberTopic = stinger::utils::format("{prefix}/SignalOnly/{service_id}/signal/maybe_number", topicArgs);
    _maybeNumberSignalSubscriptionId = _broker->Subscribe(maybeNumberTopic, 2);
    auto maybeNameTopic = stinger::utils::format("{prefix}/SignalOnly/{service_id}/signal/maybe_name", topicArgs);
    _maybeNameSignalSubscriptionId = _broker->Subscribe(maybeNameTopic, 2);
    auto nowTopic = stinger::utils::format("{prefix}/SignalOnly/{service_id}/signal/now", topicArgs);
    _nowSignalSubscriptionId = _broker->Subscribe(nowTopic, 2);
}

SignalOnlyClient::~SignalOnlyClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void SignalOnlyClient::_receiveMessage(const stinger::utils::MqttMessage& msg)
{
    const int noSubId = -1;
    int subscriptionId = msg.mqttProps.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", msg.topic.c_str(), subscriptionId);
    if (subscriptionId == _anotherSignalSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling anotherSignal signal");
        rapidjson::Document doc;
        try {
            if (_anotherSignalSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse anotherSignal signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                double tempOne;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("one");
                    if (itr != doc.MemberEnd() && itr->value.IsDouble()) {
                        tempOne = itr->value.GetDouble();

                    } else {
                        throw std::runtime_error("Received payload for 'anotherSignal' doesn't have required value/type");
                    }
                }

                bool tempTwo;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("two");
                    if (itr != doc.MemberEnd() && itr->value.IsBool()) {
                        tempTwo = itr->value.GetBool();

                    } else {
                        throw std::runtime_error("Received payload for 'anotherSignal' doesn't have required value/type");
                    }
                }

                std::string tempThree;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("three");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempThree = itr->value.GetString();

                    } else {
                        throw std::runtime_error("Received payload for 'anotherSignal' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_anotherSignalSignalCallbacksMutex);
                for (const auto& cb: _anotherSignalSignalCallbacks) {
                    cb(tempOne, tempTwo, tempThree);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _barkSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling bark signal");
        rapidjson::Document doc;
        try {
            if (_barkSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse bark signal payload.");
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
                        throw std::runtime_error("Received payload for 'bark' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_barkSignalCallbacksMutex);
                for (const auto& cb: _barkSignalCallbacks) {
                    cb(tempWord);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _maybeNumberSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling maybe_number signal");
        rapidjson::Document doc;
        try {
            if (_maybeNumberSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse maybe_number signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<int> tempNumber;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("number");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempNumber = itr->value.GetInt();

                    } else {
                        tempNumber = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_maybeNumberSignalCallbacksMutex);
                for (const auto& cb: _maybeNumberSignalCallbacks) {
                    cb(tempNumber);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _maybeNameSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling maybe_name signal");
        rapidjson::Document doc;
        try {
            if (_maybeNameSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse maybe_name signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::string> tempName;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("name");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempName = itr->value.GetString();

                    } else {
                        tempName = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_maybeNameSignalCallbacksMutex);
                for (const auto& cb: _maybeNameSignalCallbacks) {
                    cb(tempName);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _nowSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling now signal");
        rapidjson::Document doc;
        try {
            if (_nowSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse now signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::time_point<std::chrono::system_clock> tempTimestamp;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("timestamp");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail()) {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempTimestamp = std::chrono::system_clock::from_time_t(std::mktime(&tm));

                    } else {
                        throw std::runtime_error("Received payload for 'now' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_nowSignalCallbacksMutex);
                for (const auto& cb: _nowSignalCallbacks) {
                    cb(tempTimestamp);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
}

void SignalOnlyClient::registerAnotherSignalCallback(const std::function<void(double, bool, std::string)>& cb)
{
    std::lock_guard<std::mutex> lock(_anotherSignalSignalCallbacksMutex);
    _anotherSignalSignalCallbacks.push_back(cb);
}

void SignalOnlyClient::registerBarkCallback(const std::function<void(std::string)>& cb)
{
    std::lock_guard<std::mutex> lock(_barkSignalCallbacksMutex);
    _barkSignalCallbacks.push_back(cb);
}

void SignalOnlyClient::registerMaybeNumberCallback(const std::function<void(std::optional<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_maybeNumberSignalCallbacksMutex);
    _maybeNumberSignalCallbacks.push_back(cb);
}

void SignalOnlyClient::registerMaybeNameCallback(const std::function<void(std::optional<std::string>)>& cb)
{
    std::lock_guard<std::mutex> lock(_maybeNameSignalCallbacksMutex);
    _maybeNameSignalCallbacks.push_back(cb);
}

void SignalOnlyClient::registerNowCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb)
{
    std::lock_guard<std::mutex> lock(_nowSignalCallbacksMutex);
    _nowSignalCallbacks.push_back(cb);
}

} // namespace signal_only

} // namespace gen

} // namespace stinger
