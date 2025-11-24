

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

constexpr const char TestableClient::NAME[];
constexpr const char TestableClient::INTERFACE_VERSION[];

TestableClient::TestableClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId):
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
    _emptySignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/empty") % _instanceId).str(), 2);
    _singleIntSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleInt") % _instanceId).str(), 2);
    _singleOptionalIntSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleOptionalInt") % _instanceId).str(), 2);
    _threeIntegersSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/threeIntegers") % _instanceId).str(), 2);
    _singleStringSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleString") % _instanceId).str(), 2);
    _singleOptionalStringSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleOptionalString") % _instanceId).str(), 2);
    _threeStringsSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/threeStrings") % _instanceId).str(), 2);
    _singleEnumSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleEnum") % _instanceId).str(), 2);
    _singleOptionalEnumSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleOptionalEnum") % _instanceId).str(), 2);
    _threeEnumsSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/threeEnums") % _instanceId).str(), 2);
    _singleStructSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleStruct") % _instanceId).str(), 2);
    _singleOptionalStructSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleOptionalStruct") % _instanceId).str(), 2);
    _threeStructsSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/threeStructs") % _instanceId).str(), 2);
    _singleDateTimeSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleDateTime") % _instanceId).str(), 2);
    _singleOptionalDatetimeSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleOptionalDatetime") % _instanceId).str(), 2);
    _threeDateTimesSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/threeDateTimes") % _instanceId).str(), 2);
    _singleDurationSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleDuration") % _instanceId).str(), 2);
    _singleOptionalDurationSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleOptionalDuration") % _instanceId).str(), 2);
    _threeDurationsSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/threeDurations") % _instanceId).str(), 2);
    _singleBinarySignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleBinary") % _instanceId).str(), 2);
    _singleOptionalBinarySignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleOptionalBinary") % _instanceId).str(), 2);
    _threeBinariesSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/threeBinaries") % _instanceId).str(), 2);
    _singleArrayOfIntegersSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleArrayOfIntegers") % _instanceId).str(), 2);
    _singleOptionalArrayOfStringsSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/singleOptionalArrayOfStrings") % _instanceId).str(), 2);
    _arrayOfEveryTypeSignalSubscriptionId = _broker->Subscribe((format("testable/%1%/signal/arrayOfEveryType") % _instanceId).str(), 2);
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callWithNothing/methodResponse") % _broker->GetClientId();
        _callWithNothingMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOneInteger/methodResponse") % _broker->GetClientId();
        _callOneIntegerMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOptionalInteger/methodResponse") % _broker->GetClientId();
        _callOptionalIntegerMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callThreeIntegers/methodResponse") % _broker->GetClientId();
        _callThreeIntegersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOneString/methodResponse") % _broker->GetClientId();
        _callOneStringMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOptionalString/methodResponse") % _broker->GetClientId();
        _callOptionalStringMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callThreeStrings/methodResponse") % _broker->GetClientId();
        _callThreeStringsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOneEnum/methodResponse") % _broker->GetClientId();
        _callOneEnumMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOptionalEnum/methodResponse") % _broker->GetClientId();
        _callOptionalEnumMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callThreeEnums/methodResponse") % _broker->GetClientId();
        _callThreeEnumsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOneStruct/methodResponse") % _broker->GetClientId();
        _callOneStructMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOptionalStruct/methodResponse") % _broker->GetClientId();
        _callOptionalStructMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callThreeStructs/methodResponse") % _broker->GetClientId();
        _callThreeStructsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOneDateTime/methodResponse") % _broker->GetClientId();
        _callOneDateTimeMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOptionalDateTime/methodResponse") % _broker->GetClientId();
        _callOptionalDateTimeMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callThreeDateTimes/methodResponse") % _broker->GetClientId();
        _callThreeDateTimesMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOneDuration/methodResponse") % _broker->GetClientId();
        _callOneDurationMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOptionalDuration/methodResponse") % _broker->GetClientId();
        _callOptionalDurationMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callThreeDurations/methodResponse") % _broker->GetClientId();
        _callThreeDurationsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOneBinary/methodResponse") % _broker->GetClientId();
        _callOneBinaryMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOptionalBinary/methodResponse") % _broker->GetClientId();
        _callOptionalBinaryMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callThreeBinaries/methodResponse") % _broker->GetClientId();
        _callThreeBinariesMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOneListOfIntegers/methodResponse") % _broker->GetClientId();
        _callOneListOfIntegersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callOptionalListOfFloats/methodResponse") % _broker->GetClientId();
        _callOptionalListOfFloatsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << format("client/%1%/callTwoLists/methodResponse") % _broker->GetClientId();
        _callTwoListsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    _readWriteIntegerPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteInteger/value") % _instanceId).str(), 1);
    _readOnlyIntegerPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readOnlyInteger/value") % _instanceId).str(), 1);
    _readWriteOptionalIntegerPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteOptionalInteger/value") % _instanceId).str(), 1);
    _readWriteTwoIntegersPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteTwoIntegers/value") % _instanceId).str(), 1);
    _readOnlyStringPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readOnlyString/value") % _instanceId).str(), 1);
    _readWriteStringPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteString/value") % _instanceId).str(), 1);
    _readWriteOptionalStringPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteOptionalString/value") % _instanceId).str(), 1);
    _readWriteTwoStringsPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteTwoStrings/value") % _instanceId).str(), 1);
    _readWriteStructPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteStruct/value") % _instanceId).str(), 1);
    _readWriteOptionalStructPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteOptionalStruct/value") % _instanceId).str(), 1);
    _readWriteTwoStructsPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteTwoStructs/value") % _instanceId).str(), 1);
    _readOnlyEnumPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readOnlyEnum/value") % _instanceId).str(), 1);
    _readWriteEnumPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteEnum/value") % _instanceId).str(), 1);
    _readWriteOptionalEnumPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteOptionalEnum/value") % _instanceId).str(), 1);
    _readWriteTwoEnumsPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteTwoEnums/value") % _instanceId).str(), 1);
    _readWriteDatetimePropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteDatetime/value") % _instanceId).str(), 1);
    _readWriteOptionalDatetimePropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteOptionalDatetime/value") % _instanceId).str(), 1);
    _readWriteTwoDatetimesPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteTwoDatetimes/value") % _instanceId).str(), 1);
    _readWriteDurationPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteDuration/value") % _instanceId).str(), 1);
    _readWriteOptionalDurationPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteOptionalDuration/value") % _instanceId).str(), 1);
    _readWriteTwoDurationsPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteTwoDurations/value") % _instanceId).str(), 1);
    _readWriteBinaryPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteBinary/value") % _instanceId).str(), 1);
    _readWriteOptionalBinaryPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteOptionalBinary/value") % _instanceId).str(), 1);
    _readWriteTwoBinariesPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteTwoBinaries/value") % _instanceId).str(), 1);
    _readWriteListOfStringsPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteListOfStrings/value") % _instanceId).str(), 1);
    _readWriteListsPropertySubscriptionId = _broker->Subscribe((format("testable/%1%/property/readWriteLists/value") % _instanceId).str(), 1);
}

TestableClient::~TestableClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void TestableClient::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", topic.c_str(), subscriptionId);
    if ((subscriptionId == _emptySignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/empty") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling empty signal");
        rapidjson::Document doc;
        try
        {
            if (_emptySignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse empty signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::lock_guard<std::mutex> lock(_emptySignalCallbacksMutex);
                for (const auto& cb: _emptySignalCallbacks)
                {
                    cb();
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
    if ((subscriptionId == _singleIntSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleInt") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleInt signal");
        rapidjson::Document doc;
        try
        {
            if (_singleIntSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleInt signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                int tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempValue = itr->value.GetInt();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'singleInt' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleIntSignalCallbacksMutex);
                for (const auto& cb: _singleIntSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalIntSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleOptionalInt") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleOptionalInt signal");
        rapidjson::Document doc;
        try
        {
            if (_singleOptionalIntSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalInt signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<int> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempValue = itr->value.GetInt();
                    }
                    else
                    {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalIntSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalIntSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeIntegersSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/threeIntegers") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling threeIntegers signal");
        rapidjson::Document doc;
        try
        {
            if (_threeIntegersSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeIntegers signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                int tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempFirst = itr->value.GetInt();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeIntegers' doesn't have required value/type");
                    }
                }

                int tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempSecond = itr->value.GetInt();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeIntegers' doesn't have required value/type");
                    }
                }

                std::optional<int> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempThird = itr->value.GetInt();
                    }
                    else
                    {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeIntegersSignalCallbacksMutex);
                for (const auto& cb: _threeIntegersSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleStringSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleString") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleString signal");
        rapidjson::Document doc;
        try
        {
            if (_singleStringSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleString signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::string tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = itr->value.GetString();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'singleString' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleStringSignalCallbacksMutex);
                for (const auto& cb: _singleStringSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalStringSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleOptionalString") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleOptionalString signal");
        rapidjson::Document doc;
        try
        {
            if (_singleOptionalStringSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalString signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::string> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = itr->value.GetString();
                    }
                    else
                    {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalStringSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalStringSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeStringsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/threeStrings") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling threeStrings signal");
        rapidjson::Document doc;
        try
        {
            if (_threeStringsSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeStrings signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::string tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempFirst = itr->value.GetString();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeStrings' doesn't have required value/type");
                    }
                }

                std::string tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempSecond = itr->value.GetString();
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeStrings' doesn't have required value/type");
                    }
                }

                std::optional<std::string> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempThird = itr->value.GetString();
                    }
                    else
                    {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeStringsSignalCallbacksMutex);
                for (const auto& cb: _threeStringsSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleEnumSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleEnum") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleEnum signal");
        rapidjson::Document doc;
        try
        {
            if (_singleEnumSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleEnum signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                Numbers tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempValue = static_cast<Numbers>(itr->value.GetInt());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'singleEnum' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleEnumSignalCallbacksMutex);
                for (const auto& cb: _singleEnumSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalEnumSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleOptionalEnum") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleOptionalEnum signal");
        rapidjson::Document doc;
        try
        {
            if (_singleOptionalEnumSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalEnum signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<Numbers> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempValue = static_cast<Numbers>(itr->value.GetInt());
                    }
                    else
                    {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalEnumSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalEnumSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeEnumsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/threeEnums") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling threeEnums signal");
        rapidjson::Document doc;
        try
        {
            if (_threeEnumsSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeEnums signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                Numbers tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempFirst = static_cast<Numbers>(itr->value.GetInt());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeEnums' doesn't have required value/type");
                    }
                }

                Numbers tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempSecond = static_cast<Numbers>(itr->value.GetInt());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeEnums' doesn't have required value/type");
                    }
                }

                std::optional<Numbers> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempThird = static_cast<Numbers>(itr->value.GetInt());
                    }
                    else
                    {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeEnumsSignalCallbacksMutex);
                for (const auto& cb: _threeEnumsSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleStructSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleStruct") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleStruct signal");
        rapidjson::Document doc;
        try
        {
            if (_singleStructSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleStruct signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                AllTypes tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsObject())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'singleStruct' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleStructSignalCallbacksMutex);
                for (const auto& cb: _singleStructSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalStructSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleOptionalStruct") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleOptionalStruct signal");
        rapidjson::Document doc;
        try
        {
            if (_singleOptionalStructSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalStruct signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<AllTypes> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsObject())
                    {
                    }
                    else
                    {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalStructSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalStructSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeStructsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/threeStructs") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling threeStructs signal");
        rapidjson::Document doc;
        try
        {
            if (_threeStructsSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeStructs signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                AllTypes tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsObject())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeStructs' doesn't have required value/type");
                    }
                }

                AllTypes tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsObject())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeStructs' doesn't have required value/type");
                    }
                }

                std::optional<AllTypes> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsObject())
                    {
                    }
                    else
                    {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeStructsSignalCallbacksMutex);
                for (const auto& cb: _threeStructsSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleDateTimeSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleDateTime") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleDateTime signal");
        rapidjson::Document doc;
        try
        {
            if (_singleDateTimeSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleDateTime signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::time_point<std::chrono::system_clock> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail())
                        {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempValue = std::chrono::system_clock::from_time_t(std::mktime(&tm));
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'singleDateTime' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleDateTimeSignalCallbacksMutex);
                for (const auto& cb: _singleDateTimeSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalDatetimeSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleOptionalDatetime") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleOptionalDatetime signal");
        rapidjson::Document doc;
        try
        {
            if (_singleOptionalDatetimeSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalDatetime signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::chrono::time_point<std::chrono::system_clock>> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail())
                        {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempValue = std::chrono::system_clock::from_time_t(std::mktime(&tm));
                    }
                    else
                    {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalDatetimeSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalDatetimeSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeDateTimesSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/threeDateTimes") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling threeDateTimes signal");
        rapidjson::Document doc;
        try
        {
            if (_threeDateTimesSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeDateTimes signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::time_point<std::chrono::system_clock> tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail())
                        {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempFirst = std::chrono::system_clock::from_time_t(std::mktime(&tm));
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeDateTimes' doesn't have required value/type");
                    }
                }

                std::chrono::time_point<std::chrono::system_clock> tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail())
                        {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempSecond = std::chrono::system_clock::from_time_t(std::mktime(&tm));
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeDateTimes' doesn't have required value/type");
                    }
                }

                std::optional<std::chrono::time_point<std::chrono::system_clock>> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail())
                        {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempThird = std::chrono::system_clock::from_time_t(std::mktime(&tm));
                    }
                    else
                    {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeDateTimesSignalCallbacksMutex);
                for (const auto& cb: _threeDateTimesSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleDurationSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleDuration") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleDuration signal");
        rapidjson::Document doc;
        try
        {
            if (_singleDurationSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleDuration signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::duration<double> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = parseIsoDuration(itr->value.GetString());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'singleDuration' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleDurationSignalCallbacksMutex);
                for (const auto& cb: _singleDurationSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalDurationSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleOptionalDuration") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleOptionalDuration signal");
        rapidjson::Document doc;
        try
        {
            if (_singleOptionalDurationSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalDuration signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::chrono::duration<double>> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = parseIsoDuration(itr->value.GetString());
                    }
                    else
                    {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalDurationSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalDurationSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeDurationsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/threeDurations") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling threeDurations signal");
        rapidjson::Document doc;
        try
        {
            if (_threeDurationsSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeDurations signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::duration<double> tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempFirst = parseIsoDuration(itr->value.GetString());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeDurations' doesn't have required value/type");
                    }
                }

                std::chrono::duration<double> tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempSecond = parseIsoDuration(itr->value.GetString());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeDurations' doesn't have required value/type");
                    }
                }

                std::optional<std::chrono::duration<double>> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempThird = parseIsoDuration(itr->value.GetString());
                    }
                    else
                    {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeDurationsSignalCallbacksMutex);
                for (const auto& cb: _threeDurationsSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleBinarySignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleBinary") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleBinary signal");
        rapidjson::Document doc;
        try
        {
            if (_singleBinarySignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleBinary signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::vector<uint8_t> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = base64Decode(itr->value.GetString());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'singleBinary' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleBinarySignalCallbacksMutex);
                for (const auto& cb: _singleBinarySignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalBinarySignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleOptionalBinary") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleOptionalBinary signal");
        rapidjson::Document doc;
        try
        {
            if (_singleOptionalBinarySignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalBinary signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::vector<uint8_t>> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = base64Decode(itr->value.GetString());
                    }
                    else
                    {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalBinarySignalCallbacksMutex);
                for (const auto& cb: _singleOptionalBinarySignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeBinariesSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/threeBinaries") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling threeBinaries signal");
        rapidjson::Document doc;
        try
        {
            if (_threeBinariesSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeBinaries signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::vector<uint8_t> tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempFirst = base64Decode(itr->value.GetString());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeBinaries' doesn't have required value/type");
                    }
                }

                std::vector<uint8_t> tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempSecond = base64Decode(itr->value.GetString());
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'threeBinaries' doesn't have required value/type");
                    }
                }

                std::optional<std::vector<uint8_t>> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempThird = base64Decode(itr->value.GetString());
                    }
                    else
                    {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeBinariesSignalCallbacksMutex);
                for (const auto& cb: _threeBinariesSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleArrayOfIntegersSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleArrayOfIntegers") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleArrayOfIntegers signal");
        rapidjson::Document doc;
        try
        {
            if (_singleArrayOfIntegersSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleArrayOfIntegers signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::vector<int> tempValues;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("values");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'singleArrayOfIntegers' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleArrayOfIntegersSignalCallbacksMutex);
                for (const auto& cb: _singleArrayOfIntegersSignalCallbacks)
                {
                    cb(tempValues);
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
    if ((subscriptionId == _singleOptionalArrayOfStringsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/singleOptionalArrayOfStrings") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling singleOptionalArrayOfStrings signal");
        rapidjson::Document doc;
        try
        {
            if (_singleOptionalArrayOfStringsSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalArrayOfStrings signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::vector<std::string>> tempValues;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("values");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        tempValues = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalArrayOfStringsSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalArrayOfStringsSignalCallbacks)
                {
                    cb(tempValues);
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
    if ((subscriptionId == _arrayOfEveryTypeSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (format("testable/%1%/signal/arrayOfEveryType") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Handling arrayOfEveryType signal");
        rapidjson::Document doc;
        try
        {
            if (_arrayOfEveryTypeSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    _broker->Log(LOG_WARNING, "Could not JSON parse arrayOfEveryType signal payload.");
                    return;
                }

                if (!doc.IsObject())
                {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::vector<int> tempFirstOfIntegers;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first_of_integers");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<double> tempSecondOfFloats;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second_of_floats");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<std::string> tempThirdOfStrings;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third_of_strings");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<Numbers> tempFourthOfEnums;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("fourth_of_enums");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<Entry> tempFifthOfStructs;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("fifth_of_structs");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<std::chrono::time_point<std::chrono::system_clock>> tempSixthOfDatetimes;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("sixth_of_datetimes");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<std::chrono::duration<double>> tempSeventhOfDurations;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seventh_of_durations");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<std::vector<uint8_t>> tempEighthOfBinaries;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("eighth_of_binaries");
                    if (itr != doc.MemberEnd() && itr->value.IsArray())
                    {
                    }
                    else
                    {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_arrayOfEveryTypeSignalCallbacksMutex);
                for (const auto& cb: _arrayOfEveryTypeSignalCallbacks)
                {
                    cb(tempFirstOfIntegers, tempSecondOfFloats, tempThirdOfStrings, tempFourthOfEnums, tempFifthOfStructs, tempSixthOfDatetimes, tempSeventhOfDurations, tempEighthOfBinaries);
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
    if ((subscriptionId == _callWithNothingMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callWithNothing/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callWithNothing response");
        _handleCallWithNothingResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOneIntegerMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneInteger/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneInteger response");
        _handleCallOneIntegerResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOptionalIntegerMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalInteger/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalInteger response");
        _handleCallOptionalIntegerResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callThreeIntegersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeIntegers/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeIntegers response");
        _handleCallThreeIntegersResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOneStringMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneString/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneString response");
        _handleCallOneStringResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOptionalStringMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalString/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalString response");
        _handleCallOptionalStringResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callThreeStringsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeStrings/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeStrings response");
        _handleCallThreeStringsResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOneEnumMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneEnum/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneEnum response");
        _handleCallOneEnumResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOptionalEnumMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalEnum/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalEnum response");
        _handleCallOptionalEnumResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callThreeEnumsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeEnums/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeEnums response");
        _handleCallThreeEnumsResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOneStructMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneStruct/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneStruct response");
        _handleCallOneStructResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOptionalStructMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalStruct/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalStruct response");
        _handleCallOptionalStructResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callThreeStructsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeStructs/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeStructs response");
        _handleCallThreeStructsResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOneDateTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneDateTime/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneDateTime response");
        _handleCallOneDateTimeResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOptionalDateTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalDateTime/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalDateTime response");
        _handleCallOptionalDateTimeResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callThreeDateTimesMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeDateTimes/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeDateTimes response");
        _handleCallThreeDateTimesResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOneDurationMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneDuration/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneDuration response");
        _handleCallOneDurationResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOptionalDurationMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalDuration/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalDuration response");
        _handleCallOptionalDurationResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callThreeDurationsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeDurations/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeDurations response");
        _handleCallThreeDurationsResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOneBinaryMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneBinary/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneBinary response");
        _handleCallOneBinaryResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOptionalBinaryMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalBinary/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalBinary response");
        _handleCallOptionalBinaryResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callThreeBinariesMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeBinaries/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeBinaries response");
        _handleCallThreeBinariesResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOneListOfIntegersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneListOfIntegers/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneListOfIntegers response");
        _handleCallOneListOfIntegersResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callOptionalListOfFloatsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalListOfFloats/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalListOfFloats response");
        _handleCallOptionalListOfFloatsResponse(topic, payload, mqttProps);
    }
    else if ((subscriptionId == _callTwoListsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callTwoLists/methodResponse") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callTwoLists response");
        _handleCallTwoListsResponse(topic, payload, mqttProps);
    }
    if ((subscriptionId == _readWriteIntegerPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteInteger/value") % _instanceId).str()))
    {
        _receiveReadWriteIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readOnlyIntegerPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readOnlyInteger/value") % _instanceId).str()))
    {
        _receiveReadOnlyIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalIntegerPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteOptionalInteger/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoIntegersPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteTwoIntegers/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoIntegersPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readOnlyStringPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readOnlyString/value") % _instanceId).str()))
    {
        _receiveReadOnlyStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteStringPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteString/value") % _instanceId).str()))
    {
        _receiveReadWriteStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalStringPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteOptionalString/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoStringsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteTwoStrings/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoStringsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteStructPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteStruct/value") % _instanceId).str()))
    {
        _receiveReadWriteStructPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalStructPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteOptionalStruct/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalStructPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoStructsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteTwoStructs/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoStructsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readOnlyEnumPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readOnlyEnum/value") % _instanceId).str()))
    {
        _receiveReadOnlyEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteEnumPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteEnum/value") % _instanceId).str()))
    {
        _receiveReadWriteEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalEnumPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteOptionalEnum/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoEnumsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteTwoEnums/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoEnumsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteDatetimePropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteDatetime/value") % _instanceId).str()))
    {
        _receiveReadWriteDatetimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalDatetimePropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteOptionalDatetime/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalDatetimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoDatetimesPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteTwoDatetimes/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoDatetimesPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteDurationPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteDuration/value") % _instanceId).str()))
    {
        _receiveReadWriteDurationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalDurationPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteOptionalDuration/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalDurationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoDurationsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteTwoDurations/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoDurationsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteBinaryPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteBinary/value") % _instanceId).str()))
    {
        _receiveReadWriteBinaryPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalBinaryPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteOptionalBinary/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalBinaryPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoBinariesPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteTwoBinaries/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoBinariesPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteListOfStringsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteListOfStrings/value") % _instanceId).str()))
    {
        _receiveReadWriteListOfStringsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteListsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (format("testable/%1%/property/readWriteLists/value") % _instanceId).str()))
    {
        _receiveReadWriteListsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

void TestableClient::registerEmptyCallback(const std::function<void()>& cb)
{
    std::lock_guard<std::mutex> lock(_emptySignalCallbacksMutex);
    _emptySignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleIntCallback(const std::function<void(int)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleIntSignalCallbacksMutex);
    _singleIntSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalIntCallback(const std::function<void(std::optional<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalIntSignalCallbacksMutex);
    _singleOptionalIntSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeIntegersCallback(const std::function<void(int, int, std::optional<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeIntegersSignalCallbacksMutex);
    _threeIntegersSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleStringCallback(const std::function<void(std::string)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleStringSignalCallbacksMutex);
    _singleStringSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalStringCallback(const std::function<void(std::optional<std::string>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalStringSignalCallbacksMutex);
    _singleOptionalStringSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeStringsCallback(const std::function<void(std::string, std::string, std::optional<std::string>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeStringsSignalCallbacksMutex);
    _threeStringsSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleEnumCallback(const std::function<void(Numbers)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleEnumSignalCallbacksMutex);
    _singleEnumSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalEnumCallback(const std::function<void(std::optional<Numbers>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalEnumSignalCallbacksMutex);
    _singleOptionalEnumSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeEnumsCallback(const std::function<void(Numbers, Numbers, std::optional<Numbers>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeEnumsSignalCallbacksMutex);
    _threeEnumsSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleStructCallback(const std::function<void(AllTypes)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleStructSignalCallbacksMutex);
    _singleStructSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalStructCallback(const std::function<void(std::optional<AllTypes>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalStructSignalCallbacksMutex);
    _singleOptionalStructSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeStructsCallback(const std::function<void(AllTypes, AllTypes, std::optional<AllTypes>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeStructsSignalCallbacksMutex);
    _threeStructsSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleDateTimeCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleDateTimeSignalCallbacksMutex);
    _singleDateTimeSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalDatetimeCallback(const std::function<void(std::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalDatetimeSignalCallbacksMutex);
    _singleOptionalDatetimeSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeDateTimesCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeDateTimesSignalCallbacksMutex);
    _threeDateTimesSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleDurationCallback(const std::function<void(std::chrono::duration<double>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleDurationSignalCallbacksMutex);
    _singleDurationSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalDurationCallback(const std::function<void(std::optional<std::chrono::duration<double>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalDurationSignalCallbacksMutex);
    _singleOptionalDurationSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeDurationsCallback(const std::function<void(std::chrono::duration<double>, std::chrono::duration<double>, std::optional<std::chrono::duration<double>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeDurationsSignalCallbacksMutex);
    _threeDurationsSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleBinaryCallback(const std::function<void(std::vector<uint8_t>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleBinarySignalCallbacksMutex);
    _singleBinarySignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalBinaryCallback(const std::function<void(std::optional<std::vector<uint8_t>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalBinarySignalCallbacksMutex);
    _singleOptionalBinarySignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeBinariesCallback(const std::function<void(std::vector<uint8_t>, std::vector<uint8_t>, std::optional<std::vector<uint8_t>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeBinariesSignalCallbacksMutex);
    _threeBinariesSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleArrayOfIntegersCallback(const std::function<void(std::vector<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleArrayOfIntegersSignalCallbacksMutex);
    _singleArrayOfIntegersSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalArrayOfStringsCallback(const std::function<void(std::optional<std::vector<std::string>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalArrayOfStringsSignalCallbacksMutex);
    _singleOptionalArrayOfStringsSignalCallbacks.push_back(cb);
}

void TestableClient::registerArrayOfEveryTypeCallback(const std::function<void(std::vector<int>, std::vector<double>, std::vector<std::string>, std::vector<Numbers>, std::vector<Entry>, std::vector<std::chrono::time_point<std::chrono::system_clock>>, std::vector<std::chrono::duration<double>>, std::vector<std::vector<uint8_t>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_arrayOfEveryTypeSignalCallbacksMutex);
    _arrayOfEveryTypeSignalCallbacks.push_back(cb);
}

std::future<void> TestableClient::callWithNothing()
{
    auto correlationId = generate_uuid_string();
    _pendingCallWithNothingMethodCalls[correlationId] = std::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callWithNothing/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callWithNothing") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallWithNothingMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallWithNothingResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callWithNothing");

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallWithNothingMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallWithNothingMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method doesn't have any return values.
        promiseItr->second.set_value();
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callWithNothing");
}

std::future<int> TestableClient::callOneInteger(int input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOneIntegerMethodCalls[correlationId] = std::promise<int>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", input1, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOneInteger/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOneInteger") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneIntegerMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOneIntegerResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneInteger");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOneInteger signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOneInteger' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOneIntegerMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOneIntegerMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneIntegerReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneInteger");
}

std::future<std::optional<int>> TestableClient::callOptionalInteger(std::optional<int> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOptionalIntegerMethodCalls[correlationId] = std::promise<std::optional<int>>();

    rapidjson::Document doc;
    doc.SetObject();

    if (input1)
        doc.AddMember("input1", *input1, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOptionalInteger/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOptionalInteger") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalIntegerMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOptionalIntegerResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalInteger");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOptionalInteger signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOptionalInteger' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOptionalIntegerMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOptionalIntegerMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalIntegerReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalInteger");
}

std::future<CallThreeIntegersReturnValues> TestableClient::callThreeIntegers(int input1, int input2, std::optional<int> input3)
{
    auto correlationId = generate_uuid_string();
    _pendingCallThreeIntegersMethodCalls[correlationId] = std::promise<CallThreeIntegersReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", input1, doc.GetAllocator());

    doc.AddMember("input2", input2, doc.GetAllocator());

    if (input3)
        doc.AddMember("input3", *input3, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callThreeIntegers/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callThreeIntegers") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeIntegersMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallThreeIntegersResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeIntegers");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callThreeIntegers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callThreeIntegers' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallThreeIntegersMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallThreeIntegersMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeIntegersReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeIntegers");
}

std::future<std::string> TestableClient::callOneString(std::string input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOneStringMethodCalls[correlationId] = std::promise<std::string>();

    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1.c_str(), input1.size(), doc.GetAllocator());
        doc.AddMember("input1", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOneString/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOneString") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneStringMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOneStringResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneString");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOneString signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOneString' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOneStringMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOneStringMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneStringReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneString");
}

std::future<std::optional<std::string>> TestableClient::callOptionalString(std::optional<std::string> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOptionalStringMethodCalls[correlationId] = std::promise<std::optional<std::string>>();

    rapidjson::Document doc;
    doc.SetObject();

    if (input1)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1->c_str(), input1->size(), doc.GetAllocator());
        doc.AddMember("input1", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOptionalString/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOptionalString") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalStringMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOptionalStringResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalString");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOptionalString signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOptionalString' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOptionalStringMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOptionalStringMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalStringReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalString");
}

std::future<CallThreeStringsReturnValues> TestableClient::callThreeStrings(std::string input1, std::optional<std::string> input2, std::string input3)
{
    auto correlationId = generate_uuid_string();
    _pendingCallThreeStringsMethodCalls[correlationId] = std::promise<CallThreeStringsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1.c_str(), input1.size(), doc.GetAllocator());
        doc.AddMember("input1", tempStringValue, doc.GetAllocator());
    }

    if (input2)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input2->c_str(), input2->size(), doc.GetAllocator());
        doc.AddMember("input2", tempStringValue, doc.GetAllocator());
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input3.c_str(), input3.size(), doc.GetAllocator());
        doc.AddMember("input3", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callThreeStrings/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callThreeStrings") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeStringsMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallThreeStringsResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeStrings");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callThreeStrings signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callThreeStrings' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallThreeStringsMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallThreeStringsMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeStringsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeStrings");
}

std::future<Numbers> TestableClient::callOneEnum(Numbers input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOneEnumMethodCalls[correlationId] = std::promise<Numbers>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(input1), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOneEnum/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOneEnum") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneEnumMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOneEnumResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneEnum");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOneEnum signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOneEnum' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOneEnumMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOneEnumMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneEnumReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneEnum");
}

std::future<std::optional<Numbers>> TestableClient::callOptionalEnum(std::optional<Numbers> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOptionalEnumMethodCalls[correlationId] = std::promise<std::optional<Numbers>>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(*input1), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOptionalEnum/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOptionalEnum") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalEnumMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOptionalEnumResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalEnum");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOptionalEnum signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOptionalEnum' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOptionalEnumMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOptionalEnumMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalEnumReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalEnum");
}

std::future<CallThreeEnumsReturnValues> TestableClient::callThreeEnums(Numbers input1, Numbers input2, std::optional<Numbers> input3)
{
    auto correlationId = generate_uuid_string();
    _pendingCallThreeEnumsMethodCalls[correlationId] = std::promise<CallThreeEnumsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(input1), doc.GetAllocator());

    doc.AddMember("input2", static_cast<int>(input2), doc.GetAllocator());

    doc.AddMember("input3", static_cast<int>(*input3), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callThreeEnums/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callThreeEnums") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeEnumsMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallThreeEnumsResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeEnums");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callThreeEnums signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callThreeEnums' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallThreeEnumsMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallThreeEnumsMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeEnumsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeEnums");
}

std::future<AllTypes> TestableClient::callOneStruct(AllTypes input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOneStructMethodCalls[correlationId] = std::promise<AllTypes>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input1.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("input1", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOneStruct/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOneStruct") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneStructMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOneStructResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneStruct");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOneStruct signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOneStruct' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOneStructMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOneStructMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneStructReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneStruct");
}

std::future<std::optional<AllTypes>> TestableClient::callOptionalStruct(std::optional<AllTypes> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOptionalStructMethodCalls[correlationId] = std::promise<std::optional<AllTypes>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (input1)
        {
            tempStructValue.SetObject();
            input1->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        }
        else
        {
            tempStructValue.SetNull();
        }
        doc.AddMember("input1", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOptionalStruct/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOptionalStruct") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalStructMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOptionalStructResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalStruct");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOptionalStruct signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOptionalStruct' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOptionalStructMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOptionalStructMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalStructReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalStruct");
}

std::future<CallThreeStructsReturnValues> TestableClient::callThreeStructs(std::optional<AllTypes> input1, AllTypes input2, AllTypes input3)
{
    auto correlationId = generate_uuid_string();
    _pendingCallThreeStructsMethodCalls[correlationId] = std::promise<CallThreeStructsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (input1)
        {
            tempStructValue.SetObject();
            input1->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        }
        else
        {
            tempStructValue.SetNull();
        }
        doc.AddMember("input1", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input2.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("input2", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input3.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("input3", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callThreeStructs/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callThreeStructs") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeStructsMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallThreeStructsResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeStructs");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callThreeStructs signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callThreeStructs' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallThreeStructsMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallThreeStructsMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeStructsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeStructs");
}

std::future<std::chrono::time_point<std::chrono::system_clock>> TestableClient::callOneDateTime(std::chrono::time_point<std::chrono::system_clock> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOneDateTimeMethodCalls[correlationId] = std::promise<std::chrono::time_point<std::chrono::system_clock>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOneDateTime/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOneDateTime") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneDateTimeMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOneDateTimeResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneDateTime");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOneDateTime signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOneDateTime' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOneDateTimeMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOneDateTimeMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneDateTimeReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneDateTime");
}

std::future<std::optional<std::chrono::time_point<std::chrono::system_clock>>> TestableClient::callOptionalDateTime(std::optional<std::chrono::time_point<std::chrono::system_clock>> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOptionalDateTimeMethodCalls[correlationId] = std::promise<std::optional<std::chrono::time_point<std::chrono::system_clock>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(*input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOptionalDateTime/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOptionalDateTime") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalDateTimeMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOptionalDateTimeResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalDateTime");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOptionalDateTime signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOptionalDateTime' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOptionalDateTimeMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOptionalDateTimeMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalDateTimeReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalDateTime");
}

std::future<CallThreeDateTimesReturnValues> TestableClient::callThreeDateTimes(std::chrono::time_point<std::chrono::system_clock> input1, std::chrono::time_point<std::chrono::system_clock> input2, std::optional<std::chrono::time_point<std::chrono::system_clock>> input3)
{
    auto correlationId = generate_uuid_string();
    _pendingCallThreeDateTimesMethodCalls[correlationId] = std::promise<CallThreeDateTimesReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput2StringValue;
        std::string input2IsoString = timePointToIsoString(input2);
        tempInput2StringValue.SetString(input2IsoString.c_str(), input2IsoString.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput3StringValue;
        std::string input3IsoString = timePointToIsoString(*input3);
        tempInput3StringValue.SetString(input3IsoString.c_str(), input3IsoString.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callThreeDateTimes/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callThreeDateTimes") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeDateTimesMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallThreeDateTimesResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeDateTimes");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callThreeDateTimes signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callThreeDateTimes' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallThreeDateTimesMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallThreeDateTimesMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeDateTimesReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeDateTimes");
}

std::future<std::chrono::duration<double>> TestableClient::callOneDuration(std::chrono::duration<double> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOneDurationMethodCalls[correlationId] = std::promise<std::chrono::duration<double>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOneDuration/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOneDuration") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneDurationMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOneDurationResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneDuration");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOneDuration signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOneDuration' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOneDurationMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOneDurationMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneDurationReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneDuration");
}

std::future<std::optional<std::chrono::duration<double>>> TestableClient::callOptionalDuration(std::optional<std::chrono::duration<double>> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOptionalDurationMethodCalls[correlationId] = std::promise<std::optional<std::chrono::duration<double>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(*input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOptionalDuration/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOptionalDuration") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalDurationMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOptionalDurationResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalDuration");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOptionalDuration signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOptionalDuration' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOptionalDurationMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOptionalDurationMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalDurationReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalDuration");
}

std::future<CallThreeDurationsReturnValues> TestableClient::callThreeDurations(std::chrono::duration<double> input1, std::chrono::duration<double> input2, std::optional<std::chrono::duration<double>> input3)
{
    auto correlationId = generate_uuid_string();
    _pendingCallThreeDurationsMethodCalls[correlationId] = std::promise<CallThreeDurationsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput2StringValue;
        std::string input2IsoString = durationToIsoString(input2);
        tempInput2StringValue.SetString(input2IsoString.c_str(), input2IsoString.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput3StringValue;
        std::string input3IsoString = durationToIsoString(*input3);
        tempInput3StringValue.SetString(input3IsoString.c_str(), input3IsoString.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callThreeDurations/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callThreeDurations") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeDurationsMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallThreeDurationsResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeDurations");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callThreeDurations signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callThreeDurations' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallThreeDurationsMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallThreeDurationsMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeDurationsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeDurations");
}

std::future<std::vector<uint8_t>> TestableClient::callOneBinary(std::vector<uint8_t> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOneBinaryMethodCalls[correlationId] = std::promise<std::vector<uint8_t>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOneBinary/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOneBinary") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneBinaryMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOneBinaryResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneBinary");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOneBinary signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOneBinary' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOneBinaryMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOneBinaryMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneBinaryReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneBinary");
}

std::future<std::optional<std::vector<uint8_t>>> TestableClient::callOptionalBinary(std::optional<std::vector<uint8_t>> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOptionalBinaryMethodCalls[correlationId] = std::promise<std::optional<std::vector<uint8_t>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(*input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOptionalBinary/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOptionalBinary") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalBinaryMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOptionalBinaryResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalBinary");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOptionalBinary signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOptionalBinary' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOptionalBinaryMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOptionalBinaryMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalBinaryReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalBinary");
}

std::future<CallThreeBinariesReturnValues> TestableClient::callThreeBinaries(std::vector<uint8_t> input1, std::vector<uint8_t> input2, std::optional<std::vector<uint8_t>> input3)
{
    auto correlationId = generate_uuid_string();
    _pendingCallThreeBinariesMethodCalls[correlationId] = std::promise<CallThreeBinariesReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput2StringValue;
        std::string input2B64String = base64Encode(input2);
        tempInput2StringValue.SetString(input2B64String.c_str(), input2B64String.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput3StringValue;
        std::string input3B64String = base64Encode(*input3);
        tempInput3StringValue.SetString(input3B64String.c_str(), input3B64String.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callThreeBinaries/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callThreeBinaries") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeBinariesMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallThreeBinariesResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeBinaries");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callThreeBinaries signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callThreeBinaries' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallThreeBinariesMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallThreeBinariesMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeBinariesReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeBinaries");
}

std::future<std::vector<int>> TestableClient::callOneListOfIntegers(std::vector<int> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOneListOfIntegersMethodCalls[correlationId] = std::promise<std::vector<int>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: input1)
        {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("input1", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOneListOfIntegers/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOneListOfIntegers") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneListOfIntegersMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOneListOfIntegersResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneListOfIntegers");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOneListOfIntegers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOneListOfIntegers' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOneListOfIntegersMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOneListOfIntegersMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneListOfIntegersReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneListOfIntegers");
}

std::future<std::optional<std::vector<double>>> TestableClient::callOptionalListOfFloats(std::optional<std::vector<double>> input1)
{
    auto correlationId = generate_uuid_string();
    _pendingCallOptionalListOfFloatsMethodCalls[correlationId] = std::promise<std::optional<std::vector<double>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *input1)
        {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("input1", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callOptionalListOfFloats/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callOptionalListOfFloats") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalListOfFloatsMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallOptionalListOfFloatsResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalListOfFloats");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callOptionalListOfFloats signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callOptionalListOfFloats' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallOptionalListOfFloatsMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallOptionalListOfFloatsMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalListOfFloatsReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalListOfFloats");
}

std::future<CallTwoListsReturnValues> TestableClient::callTwoLists(std::vector<Numbers> input1, std::optional<std::vector<std::string>> input2)
{
    auto correlationId = generate_uuid_string();
    _pendingCallTwoListsMethodCalls[correlationId] = std::promise<CallTwoListsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: input1)
        {
            tempArrayValue.PushBack(static_cast<int>(item), doc.GetAllocator());
        }
        doc.AddMember("input1", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *input2)
        {
            rapidjson::Value tempInput2StringValue;
            tempInput2StringValue.SetString(item.c_str(), item.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempInput2StringValue, doc.GetAllocator());
        }
        doc.AddMember("input2", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << format("client/%1%/callTwoLists/methodResponse") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationId;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((format("testable/%1%/method/callTwoLists") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallTwoListsMethodCalls[correlationId].get_future();
}

void TestableClient::_handleCallTwoListsResponse(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callTwoLists");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse callTwoLists signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload for 'callTwoLists' response is not an object");
    }

    auto correlationId = mqttProps.correlationId.value_or(std::string());
    auto promiseItr = _pendingCallTwoListsMethodCalls.find(correlationId);
    if (promiseItr != _pendingCallTwoListsMethodCalls.end())
    {
        if (mqttProps.returnCode && (*(mqttProps.returnCode) != MethodReturnCode::SUCCESS))
        {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(mqttProps.returnCode.value_or(MethodReturnCode::UNKNOWN_ERROR), mqttProps.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallTwoListsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callTwoLists");
}

void TestableClient::_receiveReadWriteIntegerPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_integer' property update payload is not an object");
    }
    ReadWriteIntegerProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.value = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
        _readWriteIntegerProperty = tempValue;
        _lastReadWriteIntegerPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readWriteIntegerPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<int> TestableClient::getReadWriteIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    if (_readWriteIntegerProperty)
    {
        return _readWriteIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
    _readWriteIntegerPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteIntegerProperty(int value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteInteger/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadOnlyIntegerPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_only_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_only_integer' property update payload is not an object");
    }
    ReadOnlyIntegerProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.value = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
        _readOnlyIntegerProperty = tempValue;
        _lastReadOnlyIntegerPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyIntegerPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<int> TestableClient::getReadOnlyIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    if (_readOnlyIntegerProperty)
    {
        return _readOnlyIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadOnlyIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
    _readOnlyIntegerPropertyCallbacks.push_back(cb);
}

void TestableClient::_receiveReadWriteOptionalIntegerPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_optional_integer' property update payload is not an object");
    }
    ReadWriteOptionalIntegerProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.value = itr->value.GetInt();
        }
        else
        {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
        _readWriteOptionalIntegerProperty = tempValue;
        _lastReadWriteOptionalIntegerPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalIntegerPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<int> TestableClient::getReadWriteOptionalIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    if (_readWriteOptionalIntegerProperty)
    {
        return _readWriteOptionalIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalIntegerPropertyCallback(const std::function<void(std::optional<int> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
    _readWriteOptionalIntegerPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalIntegerProperty(std::optional<int> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    if (value)
        doc.AddMember("value", *value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteOptionalInteger/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteTwoIntegersPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_integers property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_two_integers' property update payload is not an object");
    }
    ReadWriteTwoIntegersProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.first = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.second = itr->value.GetInt();
        }
        else
        {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
        _readWriteTwoIntegersProperty = tempValue;
        _lastReadWriteTwoIntegersPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoIntegersPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoIntegersProperty> TestableClient::getReadWriteTwoIntegersProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
    if (_readWriteTwoIntegersProperty)
    {
        return *_readWriteTwoIntegersProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoIntegersPropertyCallback(const std::function<void(int first, std::optional<int> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
    _readWriteTwoIntegersPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoIntegersProperty(int first, std::optional<int> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", first, doc.GetAllocator());

    if (second)
        doc.AddMember("second", *second, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteTwoIntegers/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadOnlyStringPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_only_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_only_string' property update payload is not an object");
    }
    ReadOnlyStringProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.value = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
        _readOnlyStringProperty = tempValue;
        _lastReadOnlyStringPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyStringPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::string> TestableClient::getReadOnlyStringProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    if (_readOnlyStringProperty)
    {
        return _readOnlyStringProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadOnlyStringPropertyCallback(const std::function<void(std::string value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
    _readOnlyStringPropertyCallbacks.push_back(cb);
}

void TestableClient::_receiveReadWriteStringPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_string' property update payload is not an object");
    }
    ReadWriteStringProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.value = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
        _readWriteStringProperty = tempValue;
        _lastReadWriteStringPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
        for (const auto& cb: _readWriteStringPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::string> TestableClient::getReadWriteStringProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    if (_readWriteStringProperty)
    {
        return _readWriteStringProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteStringPropertyCallback(const std::function<void(std::string value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
    _readWriteStringPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteStringProperty(std::string value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value.c_str(), value.size(), doc.GetAllocator());
        doc.AddMember("value", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteString/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteOptionalStringPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_optional_string' property update payload is not an object");
    }
    ReadWriteOptionalStringProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.value = itr->value.GetString();
        }
        else
        {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
        _readWriteOptionalStringProperty = tempValue;
        _lastReadWriteOptionalStringPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalStringPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::string> TestableClient::getReadWriteOptionalStringProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    if (_readWriteOptionalStringProperty)
    {
        return _readWriteOptionalStringProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalStringPropertyCallback(const std::function<void(std::optional<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
    _readWriteOptionalStringPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalStringProperty(std::optional<std::string> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    if (value)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value->c_str(), value->size(), doc.GetAllocator());
        doc.AddMember("value", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteOptionalString/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteTwoStringsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_strings property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_two_strings' property update payload is not an object");
    }
    ReadWriteTwoStringsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.first = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            tempValue.second = itr->value.GetString();
        }
        else
        {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
        _readWriteTwoStringsProperty = tempValue;
        _lastReadWriteTwoStringsPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoStringsPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoStringsProperty> TestableClient::getReadWriteTwoStringsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
    if (_readWriteTwoStringsProperty)
    {
        return *_readWriteTwoStringsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoStringsPropertyCallback(const std::function<void(std::string first, std::optional<std::string> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
    _readWriteTwoStringsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoStringsProperty(std::string first, std::optional<std::string> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(first.c_str(), first.size(), doc.GetAllocator());
        doc.AddMember("first", tempStringValue, doc.GetAllocator());
    }

    if (second)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(second->c_str(), second->size(), doc.GetAllocator());
        doc.AddMember("second", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteTwoStrings/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteStructPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_struct property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_struct' property update payload is not an object");
    }
    ReadWriteStructProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.value = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
        _readWriteStructProperty = tempValue;
        _lastReadWriteStructPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
        for (const auto& cb: _readWriteStructPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<AllTypes> TestableClient::getReadWriteStructProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    if (_readWriteStructProperty)
    {
        return _readWriteStructProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteStructPropertyCallback(const std::function<void(AllTypes value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
    _readWriteStructPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteStructProperty(AllTypes value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        value.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("value", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteStruct/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteOptionalStructPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_struct property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_optional_struct' property update payload is not an object");
    }
    ReadWriteOptionalStructProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.value = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
        _readWriteOptionalStructProperty = tempValue;
        _lastReadWriteOptionalStructPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalStructPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<AllTypes> TestableClient::getReadWriteOptionalStructProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    if (_readWriteOptionalStructProperty)
    {
        return _readWriteOptionalStructProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalStructPropertyCallback(const std::function<void(std::optional<AllTypes> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
    _readWriteOptionalStructPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalStructProperty(std::optional<AllTypes> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (value)
        {
            tempStructValue.SetObject();
            value->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        }
        else
        {
            tempStructValue.SetNull();
        }
        doc.AddMember("value", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteOptionalStruct/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteTwoStructsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_structs property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_two_structs' property update payload is not an object");
    }
    ReadWriteTwoStructsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.first = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsObject())
        {
            tempValue.second = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
        _readWriteTwoStructsProperty = tempValue;
        _lastReadWriteTwoStructsPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoStructsPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoStructsProperty> TestableClient::getReadWriteTwoStructsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
    if (_readWriteTwoStructsProperty)
    {
        return *_readWriteTwoStructsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoStructsPropertyCallback(const std::function<void(AllTypes first, std::optional<AllTypes> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
    _readWriteTwoStructsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoStructsProperty(AllTypes first, std::optional<AllTypes> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        first.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("first", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (second)
        {
            tempStructValue.SetObject();
            second->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        }
        else
        {
            tempStructValue.SetNull();
        }
        doc.AddMember("second", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteTwoStructs/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadOnlyEnumPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_only_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_only_enum' property update payload is not an object");
    }
    ReadOnlyEnumProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.value = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
        _readOnlyEnumProperty = tempValue;
        _lastReadOnlyEnumPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyEnumPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<Numbers> TestableClient::getReadOnlyEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    if (_readOnlyEnumProperty)
    {
        return _readOnlyEnumProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadOnlyEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
    _readOnlyEnumPropertyCallbacks.push_back(cb);
}

void TestableClient::_receiveReadWriteEnumPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_enum' property update payload is not an object");
    }
    ReadWriteEnumProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.value = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
        _readWriteEnumProperty = tempValue;
        _lastReadWriteEnumPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
        for (const auto& cb: _readWriteEnumPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<Numbers> TestableClient::getReadWriteEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    if (_readWriteEnumProperty)
    {
        return _readWriteEnumProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
    _readWriteEnumPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteEnumProperty(Numbers value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteEnum/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteOptionalEnumPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_optional_enum' property update payload is not an object");
    }
    ReadWriteOptionalEnumProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.value = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
        _readWriteOptionalEnumProperty = tempValue;
        _lastReadWriteOptionalEnumPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalEnumPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<Numbers> TestableClient::getReadWriteOptionalEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    if (_readWriteOptionalEnumProperty)
    {
        return _readWriteOptionalEnumProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalEnumPropertyCallback(const std::function<void(std::optional<Numbers> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
    _readWriteOptionalEnumPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalEnumProperty(std::optional<Numbers> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(*value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteOptionalEnum/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteTwoEnumsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_enums property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_two_enums' property update payload is not an object");
    }
    ReadWriteTwoEnumsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.first = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.second = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
        _readWriteTwoEnumsProperty = tempValue;
        _lastReadWriteTwoEnumsPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoEnumsPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoEnumsProperty> TestableClient::getReadWriteTwoEnumsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
    if (_readWriteTwoEnumsProperty)
    {
        return *_readWriteTwoEnumsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoEnumsPropertyCallback(const std::function<void(Numbers first, std::optional<Numbers> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
    _readWriteTwoEnumsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoEnumsProperty(Numbers first, std::optional<Numbers> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", static_cast<int>(first), doc.GetAllocator());

    doc.AddMember("second", static_cast<int>(*second), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteTwoEnums/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteDatetimePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_datetime property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_datetime' property update payload is not an object");
    }
    ReadWriteDatetimeProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            tempValue.value = parseIsoTimestamp(tempValueIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
        _readWriteDatetimeProperty = tempValue;
        _lastReadWriteDatetimePropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
        for (const auto& cb: _readWriteDatetimePropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> TestableClient::getReadWriteDatetimeProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    if (_readWriteDatetimeProperty)
    {
        return _readWriteDatetimeProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteDatetimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
    _readWriteDatetimePropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteDatetimeProperty(std::chrono::time_point<std::chrono::system_clock> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = timePointToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteDatetime/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteOptionalDatetimePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_datetime property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_optional_datetime' property update payload is not an object");
    }
    ReadWriteOptionalDatetimeProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            tempValue.value = parseIsoTimestamp(tempValueIsoString);
        }
        else
        {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
        _readWriteOptionalDatetimeProperty = tempValue;
        _lastReadWriteOptionalDatetimePropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalDatetimePropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> TestableClient::getReadWriteOptionalDatetimeProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    if (_readWriteOptionalDatetimeProperty)
    {
        return _readWriteOptionalDatetimeProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalDatetimePropertyCallback(const std::function<void(std::optional<std::chrono::time_point<std::chrono::system_clock>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
    _readWriteOptionalDatetimePropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalDatetimeProperty(std::optional<std::chrono::time_point<std::chrono::system_clock>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = timePointToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteOptionalDatetime/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteTwoDatetimesPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_datetimes property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_two_datetimes' property update payload is not an object");
    }
    ReadWriteTwoDatetimesProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstIsoString = itr->value.GetString();
            tempValue.first = parseIsoTimestamp(tempFirstIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempSecondIsoString = itr->value.GetString();
            tempValue.second = parseIsoTimestamp(tempSecondIsoString);
        }
        else
        {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
        _readWriteTwoDatetimesProperty = tempValue;
        _lastReadWriteTwoDatetimesPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoDatetimesPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoDatetimesProperty> TestableClient::getReadWriteTwoDatetimesProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
    if (_readWriteTwoDatetimesProperty)
    {
        return *_readWriteTwoDatetimesProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoDatetimesPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> first, std::optional<std::chrono::time_point<std::chrono::system_clock>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
    _readWriteTwoDatetimesPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoDatetimesProperty(std::chrono::time_point<std::chrono::system_clock> first, std::optional<std::chrono::time_point<std::chrono::system_clock>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = timePointToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = timePointToIsoString(*second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteTwoDatetimes/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteDurationPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_duration property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_duration' property update payload is not an object");
    }
    ReadWriteDurationProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            tempValue.value = parseIsoDuration(tempValueIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
        _readWriteDurationProperty = tempValue;
        _lastReadWriteDurationPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
        for (const auto& cb: _readWriteDurationPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::chrono::duration<double>> TestableClient::getReadWriteDurationProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    if (_readWriteDurationProperty)
    {
        return _readWriteDurationProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteDurationPropertyCallback(const std::function<void(std::chrono::duration<double> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
    _readWriteDurationPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteDurationProperty(std::chrono::duration<double> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = durationToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteDuration/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteOptionalDurationPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_duration property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_optional_duration' property update payload is not an object");
    }
    ReadWriteOptionalDurationProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            tempValue.value = parseIsoDuration(tempValueIsoString);
        }
        else
        {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
        _readWriteOptionalDurationProperty = tempValue;
        _lastReadWriteOptionalDurationPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalDurationPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::chrono::duration<double>> TestableClient::getReadWriteOptionalDurationProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    if (_readWriteOptionalDurationProperty)
    {
        return _readWriteOptionalDurationProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalDurationPropertyCallback(const std::function<void(std::optional<std::chrono::duration<double>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
    _readWriteOptionalDurationPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalDurationProperty(std::optional<std::chrono::duration<double>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = durationToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteOptionalDuration/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteTwoDurationsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_durations property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_two_durations' property update payload is not an object");
    }
    ReadWriteTwoDurationsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstIsoString = itr->value.GetString();
            tempValue.first = parseIsoDuration(tempFirstIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempSecondIsoString = itr->value.GetString();
            tempValue.second = parseIsoDuration(tempSecondIsoString);
        }
        else
        {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
        _readWriteTwoDurationsProperty = tempValue;
        _lastReadWriteTwoDurationsPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoDurationsPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoDurationsProperty> TestableClient::getReadWriteTwoDurationsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
    if (_readWriteTwoDurationsProperty)
    {
        return *_readWriteTwoDurationsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoDurationsPropertyCallback(const std::function<void(std::chrono::duration<double> first, std::optional<std::chrono::duration<double>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
    _readWriteTwoDurationsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoDurationsProperty(std::chrono::duration<double> first, std::optional<std::chrono::duration<double>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = durationToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = durationToIsoString(*second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteTwoDurations/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteBinaryPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_binary property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_binary' property update payload is not an object");
    }
    ReadWriteBinaryProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempValueB64String = itr->value.GetString();
            tempValue.value = base64Decode(tempValueB64String);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
        _readWriteBinaryProperty = tempValue;
        _lastReadWriteBinaryPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
        for (const auto& cb: _readWriteBinaryPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::vector<uint8_t>> TestableClient::getReadWriteBinaryProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    if (_readWriteBinaryProperty)
    {
        return _readWriteBinaryProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteBinaryPropertyCallback(const std::function<void(std::vector<uint8_t> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
    _readWriteBinaryPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteBinaryProperty(std::vector<uint8_t> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = base64Encode(value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteBinary/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteOptionalBinaryPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_binary property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_optional_binary' property update payload is not an object");
    }
    ReadWriteOptionalBinaryProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempValueB64String = itr->value.GetString();
            tempValue.value = base64Decode(tempValueB64String);
        }
        else
        {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
        _readWriteOptionalBinaryProperty = tempValue;
        _lastReadWriteOptionalBinaryPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalBinaryPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::vector<uint8_t>> TestableClient::getReadWriteOptionalBinaryProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    if (_readWriteOptionalBinaryProperty)
    {
        return _readWriteOptionalBinaryProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalBinaryPropertyCallback(const std::function<void(std::optional<std::vector<uint8_t>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
    _readWriteOptionalBinaryPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalBinaryProperty(std::optional<std::vector<uint8_t>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = base64Encode(*value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteOptionalBinary/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteTwoBinariesPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_binaries property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_two_binaries' property update payload is not an object");
    }
    ReadWriteTwoBinariesProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstB64String = itr->value.GetString();
            tempValue.first = base64Decode(tempFirstB64String);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
            auto tempSecondB64String = itr->value.GetString();
            tempValue.second = base64Decode(tempSecondB64String);
        }
        else
        {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
        _readWriteTwoBinariesProperty = tempValue;
        _lastReadWriteTwoBinariesPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoBinariesPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoBinariesProperty> TestableClient::getReadWriteTwoBinariesProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
    if (_readWriteTwoBinariesProperty)
    {
        return *_readWriteTwoBinariesProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoBinariesPropertyCallback(const std::function<void(std::vector<uint8_t> first, std::optional<std::vector<uint8_t>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
    _readWriteTwoBinariesPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoBinariesProperty(std::vector<uint8_t> first, std::optional<std::vector<uint8_t>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempFirstStringValue;
        std::string firstB64String = base64Encode(first);
        tempFirstStringValue.SetString(firstB64String.c_str(), firstB64String.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempSecondStringValue;
        std::string secondB64String = base64Encode(*second);
        tempSecondStringValue.SetString(secondB64String.c_str(), secondB64String.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteTwoBinaries/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteListOfStringsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_list_of_strings property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_list_of_strings' property update payload is not an object");
    }
    ReadWriteListOfStringsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::string> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        tempArray.push_back(item.GetString());
                    }
                }
                tempValue.value = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
        _readWriteListOfStringsProperty = tempValue;
        _lastReadWriteListOfStringsPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteListOfStringsPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::vector<std::string>> TestableClient::getReadWriteListOfStringsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
    if (_readWriteListOfStringsProperty)
    {
        return _readWriteListOfStringsProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteListOfStringsPropertyCallback(const std::function<void(std::vector<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyCallbacksMutex);
    _readWriteListOfStringsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteListOfStringsProperty(std::vector<std::string> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: value)
        {
            rapidjson::Value tempValueStringValue;
            tempValueStringValue.SetString(item.c_str(), item.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempValueStringValue, doc.GetAllocator());
        }
        doc.AddMember("value", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteListOfStrings/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestableClient::_receiveReadWriteListsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_lists property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject())
    {
        throw std::runtime_error("Received 'read_write_lists' property update payload is not an object");
    }
    ReadWriteListsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("the_list");
        if (itr != doc.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<Numbers> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsInt())
                    {
                        tempArray.push_back(static_cast<Numbers>(item.GetInt()));
                    }
                }
                tempValue.theList = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'the_list' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("optionalList");
        if (itr != doc.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::chrono::time_point<std::chrono::system_clock>> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        {
                            std::string tempIsoString = item.GetString();
                            tempArray.push_back(parseIsoTimestamp(tempIsoString));
                        }
                    }
                }
                tempValue.optionalList = std::move(tempArray);
            }
        }
        else
        {
            tempValue.optionalList = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
        _readWriteListsProperty = tempValue;
        _lastReadWriteListsPropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteListsPropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.theList, tempValue.optionalList);
        }
    }
}

std::optional<ReadWriteListsProperty> TestableClient::getReadWriteListsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
    if (_readWriteListsProperty)
    {
        return *_readWriteListsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteListsPropertyCallback(const std::function<void(std::vector<Numbers> theList, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyCallbacksMutex);
    _readWriteListsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteListsProperty(std::vector<Numbers> theList, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: theList)
        {
            tempArrayValue.PushBack(static_cast<int>(item), doc.GetAllocator());
        }
        doc.AddMember("the_list", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalList)
        {
            rapidjson::Value tempOptionalListStringValue;
            std::string itemIsoString = timePointToIsoString(item);
            tempOptionalListStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempOptionalListStringValue, doc.GetAllocator());
        }
        doc.AddMember("optionalList", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testable/%1%/property/readWriteLists/setValue", buf.GetString(), 1, false, mqttProps);
}
