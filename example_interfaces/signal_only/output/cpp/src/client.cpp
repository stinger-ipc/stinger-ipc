

#include <vector>
#include <iostream>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <ctime>
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

SignalOnlyClient::SignalOnlyClient(std::shared_ptr<IBrokerConnection> broker)
    : _broker(broker)
{
    _broker->AddMessageCallback([this](
                                        const std::string& topic,
                                        const std::string& payload,
                                        const MqttProperties& mqttProps
                                )
                                { _receiveMessage(topic, payload, mqttProps); });
    _anotherSignalSignalSubscriptionId = _broker->Subscribe("signalOnly/signal/anotherSignal", 2);
    _barkSignalSubscriptionId = _broker->Subscribe("signalOnly/signal/bark", 2);
    _maybeNumberSignalSubscriptionId = _broker->Subscribe("signalOnly/signal/maybeNumber", 2);
    _maybeNameSignalSubscriptionId = _broker->Subscribe("signalOnly/signal/maybeName", 2);
    _nowSignalSubscriptionId = _broker->Subscribe("signalOnly/signal/now", 2);
}

void SignalOnlyClient::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _anotherSignalSignalSubscriptionId)) || _broker->TopicMatchesSubscription(topic, "signalOnly/signal/anotherSignal"))
    {
        //Log("Handling anotherSignal signal");
        rapidjson::Document doc;
        try
        {
            if (_anotherSignalSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse anotherSignal signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
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
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _barkSignalSubscriptionId)) || _broker->TopicMatchesSubscription(topic, "signalOnly/signal/bark"))
    {
        //Log("Handling bark signal");
        rapidjson::Document doc;
        try
        {
            if (_barkSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse bark signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
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
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _maybeNumberSignalSubscriptionId)) || _broker->TopicMatchesSubscription(topic, "signalOnly/signal/maybeNumber"))
    {
        //Log("Handling maybe_number signal");
        rapidjson::Document doc;
        try
        {
            if (_maybeNumberSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse maybe_number signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
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
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _maybeNameSignalSubscriptionId)) || _broker->TopicMatchesSubscription(topic, "signalOnly/signal/maybeName"))
    {
        //Log("Handling maybe_name signal");
        rapidjson::Document doc;
        try
        {
            if (_maybeNameSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse maybe_name signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
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
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _nowSignalSubscriptionId)) || _broker->TopicMatchesSubscription(topic, "signalOnly/signal/now"))
    {
        //Log("Handling now signal");
        rapidjson::Document doc;
        try
        {
            if (_nowSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse now signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
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
