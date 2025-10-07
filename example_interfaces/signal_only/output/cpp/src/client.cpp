

#include <vector>
#include <iostream>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <syslog.h>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "client.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"

constexpr const char SignalOnlyClient::NAME[];
constexpr const char SignalOnlyClient::INTERFACE_VERSION[];

SignalOnlyClient::SignalOnlyClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId)
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
    _anotherSignalSignalSubscriptionId = _broker->Subscribe((boost::format("signalOnly/%1%/signal/anotherSignal") % _instanceId).str(), 2);
    _barkSignalSubscriptionId = _broker->Subscribe((boost::format("signalOnly/%1%/signal/bark") % _instanceId).str(), 2);
    _maybeNumberSignalSubscriptionId = _broker->Subscribe((boost::format("signalOnly/%1%/signal/maybeNumber") % _instanceId).str(), 2);
    _maybeNameSignalSubscriptionId = _broker->Subscribe((boost::format("signalOnly/%1%/signal/maybeName") % _instanceId).str(), 2);
    _nowSignalSubscriptionId = _broker->Subscribe((boost::format("signalOnly/%1%/signal/now") % _instanceId).str(), 2);
}

SignalOnlyClient::~SignalOnlyClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void SignalOnlyClient::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);
    if ((subscriptionId == _anotherSignalSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "signalOnly/%1%/signal/anotherSignal")))
    {
        _broker->Log(LOG_INFO, "Handling anotherSignal signal");
        rapidjson::Document doc;
        try
        {
            if (_anotherSignalSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse anotherSignal signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                double tempOne;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("one");
                    if (itr != doc.MemberEnd() && itr->value.IsDouble())
                    {
                        tempOne = itr->value.GetDouble();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                bool tempTwo;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("two");
                    if (itr != doc.MemberEnd() && itr->value.IsBool())
                    {
                        tempTwo = itr->value.GetBool();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::string tempThree;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("three");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempThree = itr->value.GetString();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_anotherSignalSignalCallbacksMutex);
                for (const auto& cb: _anotherSignalSignalCallbacks)
                {
                    cb(tempOne, tempTwo, tempThree);
                }
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if ((subscriptionId == _barkSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "signalOnly/%1%/signal/bark")))
    {
        _broker->Log(LOG_INFO, "Handling bark signal");
        rapidjson::Document doc;
        try
        {
            if (_barkSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse bark signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::string tempWord;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("word");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempWord = itr->value.GetString();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_barkSignalCallbacksMutex);
                for (const auto& cb: _barkSignalCallbacks)
                {
                    cb(tempWord);
                }
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if ((subscriptionId == _maybeNumberSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "signalOnly/%1%/signal/maybeNumber")))
    {
        _broker->Log(LOG_INFO, "Handling maybe_number signal");
        rapidjson::Document doc;
        try
        {
            if (_maybeNumberSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse maybe_number signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                boost::optional<int> tempNumber;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("number");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempNumber = itr->value.GetInt();
                    }
                    else
                    {
                        tempNumber = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_maybeNumberSignalCallbacksMutex);
                for (const auto& cb: _maybeNumberSignalCallbacks)
                {
                    cb(tempNumber);
                }
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if ((subscriptionId == _maybeNameSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "signalOnly/%1%/signal/maybeName")))
    {
        _broker->Log(LOG_INFO, "Handling maybe_name signal");
        rapidjson::Document doc;
        try
        {
            if (_maybeNameSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse maybe_name signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                boost::optional<std::string> tempName;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("name");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempName = itr->value.GetString();
                    }
                    else
                    {
                        tempName = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_maybeNameSignalCallbacksMutex);
                for (const auto& cb: _maybeNameSignalCallbacks)
                {
                    cb(tempName);
                }
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if ((subscriptionId == _nowSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "signalOnly/%1%/signal/now")))
    {
        _broker->Log(LOG_INFO, "Handling now signal");
        rapidjson::Document doc;
        try
        {
            if (_nowSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse now signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::time_point<std::chrono::system_clock> tempTimestamp;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("timestamp");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail())
                        {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempTimestamp = std::chrono::system_clock::from_time_t(std::mktime(&tm));
                    }
                    else
                    {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_nowSignalCallbacksMutex);
                for (const auto& cb: _nowSignalCallbacks)
                {
                    cb(tempTimestamp);
                }
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
}

void SignalOnlyClient::registerAnotherSignalCallback(const std::function<void(double, bool, const std::string&)>& cb)
{
    std::lock_guard<std::mutex> lock(_anotherSignalSignalCallbacksMutex);
    _anotherSignalSignalCallbacks.push_back(cb);
}

void SignalOnlyClient::registerBarkCallback(const std::function<void(const std::string&)>& cb)
{
    std::lock_guard<std::mutex> lock(_barkSignalCallbacksMutex);
    _barkSignalCallbacks.push_back(cb);
}

void SignalOnlyClient::registerMaybeNumberCallback(const std::function<void(boost::optional<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_maybeNumberSignalCallbacksMutex);
    _maybeNumberSignalCallbacks.push_back(cb);
}

void SignalOnlyClient::registerMaybeNameCallback(const std::function<void(boost::optional<std::string>)>& cb)
{
    std::lock_guard<std::mutex> lock(_maybeNameSignalCallbacksMutex);
    _maybeNameSignalCallbacks.push_back(cb);
}

void SignalOnlyClient::registerNowCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb)
{
    std::lock_guard<std::mutex> lock(_nowSignalCallbacksMutex);
    _nowSignalCallbacks.push_back(cb);
}
