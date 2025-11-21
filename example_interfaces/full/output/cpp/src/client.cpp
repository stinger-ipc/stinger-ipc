

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

constexpr const char FullClient::NAME[];
constexpr const char FullClient::INTERFACE_VERSION[];

FullClient::FullClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId):
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
    _todayIsSignalSubscriptionId = _broker->Subscribe((format("full/%1%/signal/todayIs") % _instanceId).str(), 2);
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/addNumbers/methodResponse") % _broker->GetClientId();
        _addNumbersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/doSomething/methodResponse") % _broker->GetClientId();
        _doSomethingMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/echo/methodResponse") % _broker->GetClientId();
        _echoMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/whatTimeIsIt/methodResponse") % _broker->GetClientId();
        _whatTimeIsItMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/setTheTime/methodResponse") % _broker->GetClientId();
        _setTheTimeMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/forwardTime/methodResponse") % _broker->GetClientId();
        _forwardTimeMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/howOffIsTheClock/methodResponse") % _broker->GetClientId();
        _howOffIsTheClockMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    _favoriteNumberPropertySubscriptionId = _broker->Subscribe((format("full/%1%/property/favoriteNumber/value") % _instanceId).str(), 1);
    _favoriteFoodsPropertySubscriptionId = _broker->Subscribe((format("full/%1%/property/favoriteFoods/value") % _instanceId).str(), 1);
    _lunchMenuPropertySubscriptionId = _broker->Subscribe((format("full/%1%/property/lunchMenu/value") % _instanceId).str(), 1);
    _familyNamePropertySubscriptionId = _broker->Subscribe((format("full/%1%/property/familyName/value") % _instanceId).str(), 1);
    _lastBreakfastTimePropertySubscriptionId = _broker->Subscribe((format("full/%1%/property/lastBreakfastTime/value") % _instanceId).str(), 1);
    _breakfastLengthPropertySubscriptionId = _broker->Subscribe((format("full/%1%/property/breakfastLength/value") % _instanceId).str(), 1);
    _lastBirthdaysPropertySubscriptionId = _broker->Subscribe((format("full/%1%/property/lastBirthdays/value") % _instanceId).str(), 1);
}

FullClient::~FullClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void FullClient::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", topic.c_str(), subscriptionId);
    if ((subscriptionId == _todayIsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("full/%1%/signal/todayIs") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling todayIs signal");
        rapidjson::Document doc;
        try
        {
            if (_todayIsSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse todayIs signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                int tempDayOfMonth;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dayOfMonth");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempDayOfMonth = itr->value.GetInt();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'todayIs' doesn't have required value/type");
                    }
                }

                std::optional<DayOfTheWeek> tempDayOfWeek;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dayOfWeek");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempDayOfWeek = static_cast<DayOfTheWeek>(itr->value.GetInt());
                    }
                    else
                    {
                        tempDayOfWeek = std::nullopt;
                    }
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
                        throw std::runtime_error("Received payload for 'todayIs' doesn't have required value/type");
                    }
                }

                std::chrono::duration<double> tempProcessTime;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("process_time");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempProcessTime = parseIsoDuration(itr->value.GetString());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'todayIs' doesn't have required value/type");
                    }
                }

                std::vector<uint8_t> tempMemorySegment;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("memory_segment");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempMemorySegment = base64Decode(itr->value.GetString());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'todayIs' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_todayIsSignalCallbacksMutex);
                for (const auto& cb: _todayIsSignalCallbacks)
                {
                    cb(tempDayOfMonth, tempDayOfWeek, tempTimestamp, tempProcessTime, tempMemorySegment);
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
    if ((subscriptionId == _addNumbersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/addNumbers/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for addNumbers response");
        _handleAddNumbersResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _doSomethingMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/doSomething/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for doSomething response");
        _handleDoSomethingResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _echoMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/echo/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for echo response");
        _handleEchoResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _whatTimeIsItMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/whatTimeIsIt/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for what_time_is_it response");
        _handleWhatTimeIsItResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _setTheTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/setTheTime/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for set_the_time response");
        _handleSetTheTimeResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _forwardTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/forwardTime/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for forward_time response");
        _handleForwardTimeResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _howOffIsTheClockMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/howOffIsTheClock/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for how_off_is_the_clock response");
        _handleHowOffIsTheClockResponse(topic, payload, mqttProps);
    }
    if ((subscriptionId == _favoriteNumberPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("full/%1%/property/favoriteNumber/value") % _instanceId).str()))
    {
        _receiveFavoriteNumberPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _favoriteFoodsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("full/%1%/property/favoriteFoods/value") % _instanceId).str()))
    {
        _receiveFavoriteFoodsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _lunchMenuPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("full/%1%/property/lunchMenu/value") % _instanceId).str()))
    {
        _receiveLunchMenuPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _familyNamePropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("full/%1%/property/familyName/value") % _instanceId).str()))
    {
        _receiveFamilyNamePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _lastBreakfastTimePropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("full/%1%/property/lastBreakfastTime/value") % _instanceId).str()))
    {
        _receiveLastBreakfastTimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _breakfastLengthPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("full/%1%/property/breakfastLength/value") % _instanceId).str()))
    {
        _receiveBreakfastLengthPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _lastBirthdaysPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("full/%1%/property/lastBirthdays/value") % _instanceId).str()))
    {
        _receiveLastBirthdaysPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

void FullClient::registerTodayIsCallback(const std::function<void(int, std::optional<DayOfTheWeek>, std::chrono::time_point<std::chrono::system_clock>, std::chrono::duration<double>, std::vector<uint8_t>)>& cb)
{
    std::lock_guard<std::mutex> lock(_todayIsSignalCallbacksMutex);
    _todayIsSignalCallbacks.push_back(cb);
}

std::future<int> FullClient::addNumbers(int first, int second, std::optional<int> third)
{
    auto correlationId = generate_uuid_string();
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
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/addNumbers/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("full/%1%/method/addNumbers") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingAddNumbersMethodCalls[correlationId].get_future();
}

void FullClient::_handleAddNumbersResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for addNumbers");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse addNumbers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'addNumbers' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingAddNumbersMethodCalls.find(correlationId);
    if (promiseItr != _pendingAddNumbersMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = AddNumbersReturnValues::FromRapidJsonObject(doc).sum;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for addNumbers");
}

std::future<DoSomethingReturnValues> FullClient::doSomething(std::string aString)
{
    auto correlationId = generate_uuid_string();
    _pendingDoSomethingMethodCalls[correlationId] = std::promise<DoSomethingReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(aString.c_str(), aString.size(), doc.GetAllocator());
        doc.AddMember("aString", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/doSomething/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("full/%1%/method/doSomething") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingDoSomethingMethodCalls[correlationId].get_future();
}

void FullClient::_handleDoSomethingResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for doSomething");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse doSomething signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'doSomething' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingDoSomethingMethodCalls.find(correlationId);
    if (promiseItr != _pendingDoSomethingMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = DoSomethingReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for doSomething");
}

std::future<std::string> FullClient::echo(std::string message)
{
    auto correlationId = generate_uuid_string();
    _pendingEchoMethodCalls[correlationId] = std::promise<std::string>();

    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(message.c_str(), message.size(), doc.GetAllocator());
        doc.AddMember("message", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/echo/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("full/%1%/method/echo") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingEchoMethodCalls[correlationId].get_future();
}

void FullClient::_handleEchoResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for echo");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse echo signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'echo' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingEchoMethodCalls.find(correlationId);
    if (promiseItr != _pendingEchoMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = EchoReturnValues::FromRapidJsonObject(doc).message;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for echo");
}

std::future<std::chrono::time_point<std::chrono::system_clock>> FullClient::whatTimeIsIt(std::chrono::time_point<std::chrono::system_clock> theFirstTime)
{
    auto correlationId = generate_uuid_string();
    _pendingWhatTimeIsItMethodCalls[correlationId] = std::promise<std::chrono::time_point<std::chrono::system_clock>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTheFirstTimeStringValue;
        std::string theFirstTimeIsoString = timePointToIsoString(theFirstTime);
        tempTheFirstTimeStringValue.SetString(theFirstTimeIsoString.c_str(), theFirstTimeIsoString.size(), doc.GetAllocator());
        doc.AddMember("the_first_time", tempTheFirstTimeStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/whatTimeIsIt/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("full/%1%/method/whatTimeIsIt") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingWhatTimeIsItMethodCalls[correlationId].get_future();
}

void FullClient::_handleWhatTimeIsItResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for what_time_is_it");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse what_time_is_it signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'what_time_is_it' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingWhatTimeIsItMethodCalls.find(correlationId);
    if (promiseItr != _pendingWhatTimeIsItMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = WhatTimeIsItReturnValues::FromRapidJsonObject(doc).timestamp;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for what_time_is_it");
}

std::future<SetTheTimeReturnValues> FullClient::setTheTime(std::chrono::time_point<std::chrono::system_clock> theFirstTime, std::chrono::time_point<std::chrono::system_clock> theSecondTime)
{
    auto correlationId = generate_uuid_string();
    _pendingSetTheTimeMethodCalls[correlationId] = std::promise<SetTheTimeReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTheFirstTimeStringValue;
        std::string theFirstTimeIsoString = timePointToIsoString(theFirstTime);
        tempTheFirstTimeStringValue.SetString(theFirstTimeIsoString.c_str(), theFirstTimeIsoString.size(), doc.GetAllocator());
        doc.AddMember("the_first_time", tempTheFirstTimeStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTheSecondTimeStringValue;
        std::string theSecondTimeIsoString = timePointToIsoString(theSecondTime);
        tempTheSecondTimeStringValue.SetString(theSecondTimeIsoString.c_str(), theSecondTimeIsoString.size(), doc.GetAllocator());
        doc.AddMember("the_second_time", tempTheSecondTimeStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/setTheTime/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("full/%1%/method/setTheTime") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingSetTheTimeMethodCalls[correlationId].get_future();
}

void FullClient::_handleSetTheTimeResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for set_the_time");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse set_the_time signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'set_the_time' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingSetTheTimeMethodCalls.find(correlationId);
    if (promiseItr != _pendingSetTheTimeMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = SetTheTimeReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for set_the_time");
}

std::future<std::chrono::time_point<std::chrono::system_clock>> FullClient::forwardTime(std::chrono::duration<double> adjustment)
{
    auto correlationId = generate_uuid_string();
    _pendingForwardTimeMethodCalls[correlationId] = std::promise<std::chrono::time_point<std::chrono::system_clock>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempAdjustmentStringValue;
        std::string adjustmentIsoString = durationToIsoString(adjustment);
        tempAdjustmentStringValue.SetString(adjustmentIsoString.c_str(), adjustmentIsoString.size(), doc.GetAllocator());
        doc.AddMember("adjustment", tempAdjustmentStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/forwardTime/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("full/%1%/method/forwardTime") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingForwardTimeMethodCalls[correlationId].get_future();
}

void FullClient::_handleForwardTimeResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for forward_time");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse forward_time signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'forward_time' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingForwardTimeMethodCalls.find(correlationId);
    if (promiseItr != _pendingForwardTimeMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = ForwardTimeReturnValues::FromRapidJsonObject(doc).newTime;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for forward_time");
}

std::future<std::chrono::duration<double>> FullClient::howOffIsTheClock(std::chrono::time_point<std::chrono::system_clock> actualTime)
{
    auto correlationId = generate_uuid_string();
    _pendingHowOffIsTheClockMethodCalls[correlationId] = std::promise<std::chrono::duration<double>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempActualTimeStringValue;
        std::string actualTimeIsoString = timePointToIsoString(actualTime);
        tempActualTimeStringValue.SetString(actualTimeIsoString.c_str(), actualTimeIsoString.size(), doc.GetAllocator());
        doc.AddMember("actual_time", tempActualTimeStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/howOffIsTheClock/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("full/%1%/method/howOffIsTheClock") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingHowOffIsTheClockMethodCalls[correlationId].get_future();
}

void FullClient::_handleHowOffIsTheClockResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for how_off_is_the_clock");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse how_off_is_the_clock signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'how_off_is_the_clock' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingHowOffIsTheClockMethodCalls.find(correlationId);
    if (promiseItr != _pendingHowOffIsTheClockMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = HowOffIsTheClockReturnValues::FromRapidJsonObject(doc).difference;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for how_off_is_the_clock");
}

void FullClient::_receiveFavoriteNumberPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse favorite_number property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'favorite_number' property update payload is not an object");
    }
    FavoriteNumberProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("number");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.number = itr->value.GetInt();
        }
        else
        {
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
        for (const auto& cb: _favoriteNumberPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.number);
        }
    }
}

std::optional<int> FullClient::getFavoriteNumberProperty()
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
    if (_favoriteNumberProperty)
    {
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
    MqttProperties mqttProps;
    return _broker->Publish("full/%1%/property/favoriteNumber/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveFavoriteFoodsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse favorite_foods property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'favorite_foods' property update payload is not an object");
    }
    FavoriteFoodsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("drink");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.drink = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'drink' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("slices_of_pizza");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.slicesOfPizza = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'slices_of_pizza' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("breakfast");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.breakfast = itr->value.GetString();
        }
        else
        {
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
        for (const auto& cb: _favoriteFoodsPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.drink, tempValue.slicesOfPizza, tempValue.breakfast);
        }
    }
}

std::optional<FavoriteFoodsProperty> FullClient::getFavoriteFoodsProperty()
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
    if (_favoriteFoodsProperty)
    {
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

    if (breakfast)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(breakfast->c_str(), breakfast->size(), doc.GetAllocator());
        doc.AddMember("breakfast", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/%1%/property/favoriteFoods/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLunchMenuPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse lunch_menu property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'lunch_menu' property update payload is not an object");
    }
    LunchMenuProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("monday");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.monday = Lunch::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'monday' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("tuesday");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.tuesday = Lunch::FromRapidJsonObject(itr->value);
        }
        else
        {
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
        for (const auto& cb: _lunchMenuPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.monday, tempValue.tuesday);
        }
    }
}

std::optional<LunchMenuProperty> FullClient::getLunchMenuProperty()
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
    if (_lunchMenuProperty)
    {
        return *_lunchMenuProperty;
    }
    return std::nullopt;
}

void FullClient::registerLunchMenuPropertyCallback(const std::function<void(Lunch monday, Lunch tuesday)>& cb)
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyCallbacksMutex);
    _lunchMenuPropertyCallbacks.push_back(cb);
}

std::future<bool> FullClient::updateLunchMenuProperty(Lunch monday, Lunch tuesday) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        monday.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("monday", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        tuesday.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("tuesday", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/%1%/property/lunchMenu/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveFamilyNamePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse family_name property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'family_name' property update payload is not an object");
    }
    FamilyNameProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("family_name");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.familyName = itr->value.GetString();
        }
        else
        {
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
        for (const auto& cb: _familyNamePropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.familyName);
        }
    }
}

std::optional<std::string&> FullClient::getFamilyNameProperty()
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
    if (_familyNameProperty)
    {
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
    MqttProperties mqttProps;
    return _broker->Publish("full/%1%/property/familyName/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLastBreakfastTimePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse last_breakfast_time property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'last_breakfast_time' property update payload is not an object");
    }
    LastBreakfastTimeProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("timestamp");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempTimestampIsoString = itr->value.GetString();
            tempValue.timestamp = parseIsoTimestamp(tempTimestampIsoString);
        }
        else
        {
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
        for (const auto& cb: _lastBreakfastTimePropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.timestamp);
        }
    }
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> FullClient::getLastBreakfastTimeProperty()
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
    if (_lastBreakfastTimeProperty)
    {
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
        std::string timestampIsoString = timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), doc.GetAllocator());
        doc.AddMember("timestamp", tempTimestampStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/%1%/property/lastBreakfastTime/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveBreakfastLengthPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse breakfast_length property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'breakfast_length' property update payload is not an object");
    }
    BreakfastLengthProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("length");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempLengthIsoString = itr->value.GetString();
            tempValue.length = parseIsoDuration(tempLengthIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'length' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_breakfastLengthPropertyMutex);
        _breakfastLengthProperty = tempValue;
        _lastBreakfastLengthPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_breakfastLengthPropertyCallbacksMutex);
        for (const auto& cb: _breakfastLengthPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.length);
        }
    }
}

std::optional<std::chrono::duration<double>> FullClient::getBreakfastLengthProperty()
{
    std::lock_guard<std::mutex> lock(_breakfastLengthPropertyMutex);
    if (_breakfastLengthProperty)
    {
        return _breakfastLengthProperty->length;
    }
    return std::nullopt;
}

void FullClient::registerBreakfastLengthPropertyCallback(const std::function<void(std::chrono::duration<double> length)>& cb)
{
    std::lock_guard<std::mutex> lock(_breakfastLengthPropertyCallbacksMutex);
    _breakfastLengthPropertyCallbacks.push_back(cb);
}

std::future<bool> FullClient::updateBreakfastLengthProperty(std::chrono::duration<double> length) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempLengthStringValue;
        std::string lengthIsoString = durationToIsoString(length);
        tempLengthStringValue.SetString(lengthIsoString.c_str(), lengthIsoString.size(), doc.GetAllocator());
        doc.AddMember("length", tempLengthStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/%1%/property/breakfastLength/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLastBirthdaysPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse last_birthdays property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'last_birthdays' property update payload is not an object");
    }
    LastBirthdaysProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("mom");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempMomIsoString = itr->value.GetString();
            tempValue.mom = parseIsoTimestamp(tempMomIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'mom' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dad");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempDadIsoString = itr->value.GetString();
            tempValue.dad = parseIsoTimestamp(tempDadIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'dad' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("sister");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempSisterIsoString = itr->value.GetString();
            tempValue.sister = parseIsoTimestamp(tempSisterIsoString);
        }
        else
        {
            tempValue.sister = std::nullopt;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("brothers_age");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.brothersAge = itr->value.GetInt();
        }
        else
        {
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
        for (const auto& cb: _lastBirthdaysPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.mom, tempValue.dad, tempValue.sister, tempValue.brothersAge);
        }
    }
}

std::optional<LastBirthdaysProperty> FullClient::getLastBirthdaysProperty()
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
    if (_lastBirthdaysProperty)
    {
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
        std::string momIsoString = timePointToIsoString(mom);
        tempMomStringValue.SetString(momIsoString.c_str(), momIsoString.size(), doc.GetAllocator());
        doc.AddMember("mom", tempMomStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempDadStringValue;
        std::string dadIsoString = timePointToIsoString(dad);
        tempDadStringValue.SetString(dadIsoString.c_str(), dadIsoString.size(), doc.GetAllocator());
        doc.AddMember("dad", tempDadStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempSisterStringValue;
        std::string sisterIsoString = timePointToIsoString(*sister);
        tempSisterStringValue.SetString(sisterIsoString.c_str(), sisterIsoString.size(), doc.GetAllocator());
        doc.AddMember("sister", tempSisterStringValue, doc.GetAllocator());
    }

    if (brothersAge)
        doc.AddMember("brothers_age", *brothersAge, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/%1%/property/lastBirthdays/setValue", buf.GetString(), 1, false, mqttProps);
}
