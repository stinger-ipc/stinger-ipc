

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

constexpr const char TestAbleClient::NAME[];
constexpr const char TestAbleClient::INTERFACE_VERSION[];

TestAbleClient::TestAbleClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId):
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
    _emptySignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/empty") % _instanceId).str(), 2);
    _singleIntSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleInt") % _instanceId).str(), 2);
    _singleOptionalIntSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleOptionalInt") % _instanceId).str(), 2);
    _threeIntegersSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/threeIntegers") % _instanceId).str(), 2);
    _singleStringSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleString") % _instanceId).str(), 2);
    _singleOptionalStringSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleOptionalString") % _instanceId).str(), 2);
    _threeStringsSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/threeStrings") % _instanceId).str(), 2);
    _singleEnumSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleEnum") % _instanceId).str(), 2);
    _singleOptionalEnumSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleOptionalEnum") % _instanceId).str(), 2);
    _threeEnumsSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/threeEnums") % _instanceId).str(), 2);
    _singleStructSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleStruct") % _instanceId).str(), 2);
    _singleOptionalStructSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleOptionalStruct") % _instanceId).str(), 2);
    _threeStructsSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/threeStructs") % _instanceId).str(), 2);
    _singleDateTimeSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleDateTime") % _instanceId).str(), 2);
    _singleOptionalDatetimeSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleOptionalDatetime") % _instanceId).str(), 2);
    _threeDateTimesSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/threeDateTimes") % _instanceId).str(), 2);
    _singleDurationSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleDuration") % _instanceId).str(), 2);
    _singleOptionalDurationSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleOptionalDuration") % _instanceId).str(), 2);
    _threeDurationsSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/threeDurations") % _instanceId).str(), 2);
    _singleBinarySignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleBinary") % _instanceId).str(), 2);
    _singleOptionalBinarySignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/singleOptionalBinary") % _instanceId).str(), 2);
    _threeBinariesSignalSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/signal/threeBinaries") % _instanceId).str(), 2);
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callWithNothing/response") % _broker->GetClientId();
        _callWithNothingMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOneInteger/response") % _broker->GetClientId();
        _callOneIntegerMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOptionalInteger/response") % _broker->GetClientId();
        _callOptionalIntegerMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callThreeIntegers/response") % _broker->GetClientId();
        _callThreeIntegersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOneString/response") % _broker->GetClientId();
        _callOneStringMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOptionalString/response") % _broker->GetClientId();
        _callOptionalStringMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callThreeStrings/response") % _broker->GetClientId();
        _callThreeStringsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOneEnum/response") % _broker->GetClientId();
        _callOneEnumMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOptionalEnum/response") % _broker->GetClientId();
        _callOptionalEnumMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callThreeEnums/response") % _broker->GetClientId();
        _callThreeEnumsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOneStruct/response") % _broker->GetClientId();
        _callOneStructMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOptionalStruct/response") % _broker->GetClientId();
        _callOptionalStructMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callThreeStructs/response") % _broker->GetClientId();
        _callThreeStructsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOneDateTime/response") % _broker->GetClientId();
        _callOneDateTimeMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOptionalDateTime/response") % _broker->GetClientId();
        _callOptionalDateTimeMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callThreeDateTimes/response") % _broker->GetClientId();
        _callThreeDateTimesMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOneDuration/response") % _broker->GetClientId();
        _callOneDurationMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOptionalDuration/response") % _broker->GetClientId();
        _callOptionalDurationMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callThreeDurations/response") % _broker->GetClientId();
        _callThreeDurationsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOneBinary/response") % _broker->GetClientId();
        _callOneBinaryMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callOptionalBinary/response") % _broker->GetClientId();
        _callOptionalBinaryMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/callThreeBinaries/response") % _broker->GetClientId();
        _callThreeBinariesMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    _readWriteIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteInteger/value") % _instanceId).str(), 1);
    _readOnlyIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readOnlyInteger/value") % _instanceId).str(), 1);
    _readWriteOptionalIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalInteger/value") % _instanceId).str(), 1);
    _readWriteTwoIntegersPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoIntegers/value") % _instanceId).str(), 1);
    _readOnlyStringPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readOnlyString/value") % _instanceId).str(), 1);
    _readWriteStringPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteString/value") % _instanceId).str(), 1);
    _readWriteOptionalStringPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalString/value") % _instanceId).str(), 1);
    _readWriteTwoStringsPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoStrings/value") % _instanceId).str(), 1);
    _readWriteStructPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteStruct/value") % _instanceId).str(), 1);
    _readWriteOptionalStructPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalStruct/value") % _instanceId).str(), 1);
    _readWriteTwoStructsPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoStructs/value") % _instanceId).str(), 1);
    _readOnlyEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readOnlyEnum/value") % _instanceId).str(), 1);
    _readWriteEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteEnum/value") % _instanceId).str(), 1);
    _readWriteOptionalEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalEnum/value") % _instanceId).str(), 1);
    _readWriteTwoEnumsPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoEnums/value") % _instanceId).str(), 1);
    _readWriteDatetimePropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteDatetime/value") % _instanceId).str(), 1);
    _readWriteOptionalDatetimePropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalDatetime/value") % _instanceId).str(), 1);
    _readWriteTwoDatetimesPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoDatetimes/value") % _instanceId).str(), 1);
    _readWriteDurationPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteDuration/value") % _instanceId).str(), 1);
    _readWriteOptionalDurationPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalDuration/value") % _instanceId).str(), 1);
    _readWriteTwoDurationsPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoDurations/value") % _instanceId).str(), 1);
    _readWriteBinaryPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteBinary/value") % _instanceId).str(), 1);
    _readWriteOptionalBinaryPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalBinary/value") % _instanceId).str(), 1);
    _readWriteTwoBinariesPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoBinaries/value") % _instanceId).str(), 1);
}

TestAbleClient::~TestAbleClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void TestAbleClient::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", topic.c_str(), subscriptionId);
    if ((subscriptionId == _emptySignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/empty") % _instanceId).str())))
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
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if ((subscriptionId == _singleIntSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleInt") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleIntSignalCallbacksMutex);
                for (const auto& cb: _singleIntSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalIntSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleOptionalInt") % _instanceId).str())))
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

                boost::optional<int> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempValue = itr->value.GetInt();
                    }
                    else
                    {
                        tempValue = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalIntSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalIntSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeIntegersSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/threeIntegers") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                boost::optional<int> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempThird = itr->value.GetInt();
                    }
                    else
                    {
                        tempThird = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeIntegersSignalCallbacksMutex);
                for (const auto& cb: _threeIntegersSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleStringSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleString") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleStringSignalCallbacksMutex);
                for (const auto& cb: _singleStringSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalStringSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleOptionalString") % _instanceId).str())))
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

                boost::optional<std::string> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = itr->value.GetString();
                    }
                    else
                    {
                        tempValue = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalStringSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalStringSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeStringsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/threeStrings") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                boost::optional<std::string> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempThird = itr->value.GetString();
                    }
                    else
                    {
                        tempThird = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeStringsSignalCallbacksMutex);
                for (const auto& cb: _threeStringsSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleEnumSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleEnum") % _instanceId).str())))
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

                boost::optional<Numbers> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempValue = static_cast<Numbers>(itr->value.GetInt());
                    }
                    else
                    {
                        tempValue = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleEnumSignalCallbacksMutex);
                for (const auto& cb: _singleEnumSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalEnumSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleOptionalEnum") % _instanceId).str())))
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

                boost::optional<Numbers> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempValue = static_cast<Numbers>(itr->value.GetInt());
                    }
                    else
                    {
                        tempValue = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalEnumSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalEnumSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeEnumsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/threeEnums") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                boost::optional<Numbers> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempThird = static_cast<Numbers>(itr->value.GetInt());
                    }
                    else
                    {
                        tempThird = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeEnumsSignalCallbacksMutex);
                for (const auto& cb: _threeEnumsSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleStructSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleStruct") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleStructSignalCallbacksMutex);
                for (const auto& cb: _singleStructSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalStructSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleOptionalStruct") % _instanceId).str())))
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

                boost::optional<AllTypes> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsObject())
                    {
                    }
                    else
                    {
                        tempValue = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalStructSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalStructSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeStructsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/threeStructs") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                boost::optional<AllTypes> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsObject())
                    {
                    }
                    else
                    {
                        tempThird = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeStructsSignalCallbacksMutex);
                for (const auto& cb: _threeStructsSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleDateTimeSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleDateTime") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleDateTimeSignalCallbacksMutex);
                for (const auto& cb: _singleDateTimeSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalDatetimeSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleOptionalDatetime") % _instanceId).str())))
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

                boost::optional<std::chrono::time_point<std::chrono::system_clock>> tempValue;
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
                        tempValue = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalDatetimeSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalDatetimeSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeDateTimesSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/threeDateTimes") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                boost::optional<std::chrono::time_point<std::chrono::system_clock>> tempThird;
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
                        tempThird = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeDateTimesSignalCallbacksMutex);
                for (const auto& cb: _threeDateTimesSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleDurationSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleDuration") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleDurationSignalCallbacksMutex);
                for (const auto& cb: _singleDurationSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalDurationSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleOptionalDuration") % _instanceId).str())))
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

                boost::optional<std::chrono::duration<double>> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = parseIsoDuration(itr->value.GetString());
                    }
                    else
                    {
                        tempValue = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalDurationSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalDurationSignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeDurationsSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/threeDurations") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                boost::optional<std::chrono::duration<double>> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempThird = parseIsoDuration(itr->value.GetString());
                    }
                    else
                    {
                        tempThird = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeDurationsSignalCallbacksMutex);
                for (const auto& cb: _threeDurationsSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _singleBinarySignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleBinary") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleBinarySignalCallbacksMutex);
                for (const auto& cb: _singleBinarySignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _singleOptionalBinarySignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/singleOptionalBinary") % _instanceId).str())))
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

                boost::optional<std::vector<uint8_t>> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempValue = base64Decode(itr->value.GetString());
                    }
                    else
                    {
                        tempValue = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalBinarySignalCallbacksMutex);
                for (const auto& cb: _singleOptionalBinarySignalCallbacks)
                {
                    cb(tempValue);
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
    if ((subscriptionId == _threeBinariesSignalSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/signal/threeBinaries") % _instanceId).str())))
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                boost::optional<std::vector<uint8_t>> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString())
                    {
                        tempThird = base64Decode(itr->value.GetString());
                    }
                    else
                    {
                        tempThird = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeBinariesSignalCallbacksMutex);
                for (const auto& cb: _threeBinariesSignalCallbacks)
                {
                    cb(tempFirst, tempSecond, tempThird);
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
    if ((subscriptionId == _callWithNothingMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callWithNothing/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callWithNothing response");
        _handleCallWithNothingResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOneIntegerMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneInteger/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneInteger response");
        _handleCallOneIntegerResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOptionalIntegerMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalInteger/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalInteger response");
        _handleCallOptionalIntegerResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callThreeIntegersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeIntegers/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeIntegers response");
        _handleCallThreeIntegersResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOneStringMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneString/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneString response");
        _handleCallOneStringResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOptionalStringMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalString/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalString response");
        _handleCallOptionalStringResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callThreeStringsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeStrings/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeStrings response");
        _handleCallThreeStringsResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOneEnumMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneEnum/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneEnum response");
        _handleCallOneEnumResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOptionalEnumMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalEnum/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalEnum response");
        _handleCallOptionalEnumResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callThreeEnumsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeEnums/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeEnums response");
        _handleCallThreeEnumsResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOneStructMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneStruct/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneStruct response");
        _handleCallOneStructResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOptionalStructMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalStruct/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalStruct response");
        _handleCallOptionalStructResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callThreeStructsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeStructs/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeStructs response");
        _handleCallThreeStructsResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOneDateTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneDateTime/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneDateTime response");
        _handleCallOneDateTimeResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOptionalDateTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalDateTime/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalDateTime response");
        _handleCallOptionalDateTimeResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callThreeDateTimesMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeDateTimes/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeDateTimes response");
        _handleCallThreeDateTimesResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOneDurationMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneDuration/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneDuration response");
        _handleCallOneDurationResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOptionalDurationMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalDuration/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalDuration response");
        _handleCallOptionalDurationResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callThreeDurationsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeDurations/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeDurations response");
        _handleCallThreeDurationsResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOneBinaryMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOneBinary/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneBinary response");
        _handleCallOneBinaryResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callOptionalBinaryMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callOptionalBinary/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalBinary response");
        _handleCallOptionalBinaryResponse(topic, payload, *mqttProps.correlationId);
    }
    else if ((subscriptionId == _callThreeBinariesMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, "client/+/callThreeBinaries/response") && mqttProps.correlationId))
    {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeBinaries response");
        _handleCallThreeBinariesResponse(topic, payload, *mqttProps.correlationId);
    }
    if ((subscriptionId == _readWriteIntegerPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteInteger/value") % _instanceId).str()))
    {
        _receiveReadWriteIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readOnlyIntegerPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readOnlyInteger/value") % _instanceId).str()))
    {
        _receiveReadOnlyIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalIntegerPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteOptionalInteger/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoIntegersPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteTwoIntegers/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoIntegersPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readOnlyStringPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readOnlyString/value") % _instanceId).str()))
    {
        _receiveReadOnlyStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteStringPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteString/value") % _instanceId).str()))
    {
        _receiveReadWriteStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalStringPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteOptionalString/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoStringsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteTwoStrings/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoStringsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteStructPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteStruct/value") % _instanceId).str()))
    {
        _receiveReadWriteStructPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalStructPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteOptionalStruct/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalStructPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoStructsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteTwoStructs/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoStructsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readOnlyEnumPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readOnlyEnum/value") % _instanceId).str()))
    {
        _receiveReadOnlyEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteEnumPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteEnum/value") % _instanceId).str()))
    {
        _receiveReadWriteEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalEnumPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteOptionalEnum/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoEnumsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteTwoEnums/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoEnumsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteDatetimePropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteDatetime/value") % _instanceId).str()))
    {
        _receiveReadWriteDatetimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalDatetimePropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteOptionalDatetime/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalDatetimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoDatetimesPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteTwoDatetimes/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoDatetimesPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteDurationPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteDuration/value") % _instanceId).str()))
    {
        _receiveReadWriteDurationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalDurationPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteOptionalDuration/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalDurationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoDurationsPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteTwoDurations/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoDurationsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteBinaryPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteBinary/value") % _instanceId).str()))
    {
        _receiveReadWriteBinaryPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteOptionalBinaryPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteOptionalBinary/value") % _instanceId).str()))
    {
        _receiveReadWriteOptionalBinaryPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((subscriptionId == _readWriteTwoBinariesPropertySubscriptionId) || (subscriptionId == noSubId && topic == (boost::format("testAble/%1%/property/readWriteTwoBinaries/value") % _instanceId).str()))
    {
        _receiveReadWriteTwoBinariesPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

void TestAbleClient::registerEmptyCallback(const std::function<void()>& cb)
{
    std::lock_guard<std::mutex> lock(_emptySignalCallbacksMutex);
    _emptySignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleIntCallback(const std::function<void(int)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleIntSignalCallbacksMutex);
    _singleIntSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleOptionalIntCallback(const std::function<void(boost::optional<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalIntSignalCallbacksMutex);
    _singleOptionalIntSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerThreeIntegersCallback(const std::function<void(int, int, boost::optional<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeIntegersSignalCallbacksMutex);
    _threeIntegersSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleStringCallback(const std::function<void(std::string)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleStringSignalCallbacksMutex);
    _singleStringSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleOptionalStringCallback(const std::function<void(boost::optional<std::string>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalStringSignalCallbacksMutex);
    _singleOptionalStringSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerThreeStringsCallback(const std::function<void(std::string, std::string, boost::optional<std::string>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeStringsSignalCallbacksMutex);
    _threeStringsSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleEnumCallback(const std::function<void(boost::optional<Numbers>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleEnumSignalCallbacksMutex);
    _singleEnumSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleOptionalEnumCallback(const std::function<void(boost::optional<Numbers>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalEnumSignalCallbacksMutex);
    _singleOptionalEnumSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerThreeEnumsCallback(const std::function<void(Numbers, Numbers, boost::optional<Numbers>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeEnumsSignalCallbacksMutex);
    _threeEnumsSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleStructCallback(const std::function<void(AllTypes)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleStructSignalCallbacksMutex);
    _singleStructSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleOptionalStructCallback(const std::function<void(boost::optional<AllTypes>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalStructSignalCallbacksMutex);
    _singleOptionalStructSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerThreeStructsCallback(const std::function<void(AllTypes, AllTypes, boost::optional<AllTypes>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeStructsSignalCallbacksMutex);
    _threeStructsSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleDateTimeCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleDateTimeSignalCallbacksMutex);
    _singleDateTimeSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleOptionalDatetimeCallback(const std::function<void(boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalDatetimeSignalCallbacksMutex);
    _singleOptionalDatetimeSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerThreeDateTimesCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeDateTimesSignalCallbacksMutex);
    _threeDateTimesSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleDurationCallback(const std::function<void(std::chrono::duration<double>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleDurationSignalCallbacksMutex);
    _singleDurationSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleOptionalDurationCallback(const std::function<void(boost::optional<std::chrono::duration<double>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalDurationSignalCallbacksMutex);
    _singleOptionalDurationSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerThreeDurationsCallback(const std::function<void(std::chrono::duration<double>, std::chrono::duration<double>, boost::optional<std::chrono::duration<double>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeDurationsSignalCallbacksMutex);
    _threeDurationsSignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleBinaryCallback(const std::function<void(std::vector<uint8_t>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleBinarySignalCallbacksMutex);
    _singleBinarySignalCallbacks.push_back(cb);
}

void TestAbleClient::registerSingleOptionalBinaryCallback(const std::function<void(boost::optional<std::vector<uint8_t>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalBinarySignalCallbacksMutex);
    _singleOptionalBinarySignalCallbacks.push_back(cb);
}

void TestAbleClient::registerThreeBinariesCallback(const std::function<void(std::vector<uint8_t>, std::vector<uint8_t>, boost::optional<std::vector<uint8_t>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeBinariesSignalCallbacksMutex);
    _threeBinariesSignalCallbacks.push_back(cb);
}

boost::future<void> TestAbleClient::callWithNothing()
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallWithNothingMethodCalls[correlationId] = boost::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callWithNothing/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callWithNothing") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallWithNothingMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallWithNothingResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callWithNothing");

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallWithNothingMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallWithNothingMethodCalls.end())
    {
        // There are no values in the response.
        promiseItr->second.set_value();
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callWithNothing");
}

boost::future<int> TestAbleClient::callOneInteger(int input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOneIntegerMethodCalls[correlationId] = boost::promise<int>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", input1, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOneInteger/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOneInteger") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneIntegerMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOneIntegerResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOneIntegerMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOneIntegerMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        int output1 = output1Itr->value.GetInt();

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneInteger");
}

boost::future<boost::optional<int>> TestAbleClient::callOptionalInteger(boost::optional<int> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOptionalIntegerMethodCalls[correlationId] = boost::promise<boost::optional<int>>();

    rapidjson::Document doc;
    doc.SetObject();

    if (input1)
        doc.AddMember("input1", *input1, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOptionalInteger/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOptionalInteger") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalIntegerMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOptionalIntegerResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOptionalIntegerMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOptionalIntegerMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // arg is optional, so check if it is set
        boost::optional<int> output1 = boost::none;
        if (output1Itr != doc.MemberEnd())
        {
            boost::optional<int> output1 = output1Itr->value.GetInt();
        }

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalInteger");
}

boost::future<CallThreeIntegersReturnValue> TestAbleClient::callThreeIntegers(int input1, int input2, boost::optional<int> input3)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallThreeIntegersMethodCalls[correlationId] = boost::promise<CallThreeIntegersReturnValue>();

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
    responseTopicStringStream << boost::format("client/%1%/callThreeIntegers/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callThreeIntegers") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeIntegersMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallThreeIntegersResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallThreeIntegersMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallThreeIntegersMethodCalls.end())
    {
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        int output1 = output1Itr->value.GetInt();

        rapidjson::Value::ConstMemberIterator output2Itr = doc.FindMember("output2");

        int output2 = output2Itr->value.GetInt();

        rapidjson::Value::ConstMemberIterator output3Itr = doc.FindMember("output3");

        // arg is optional, so check if it is set
        boost::optional<int> output3 = boost::none;
        if (output3Itr != doc.MemberEnd())
        {
            boost::optional<int> output3 = output3Itr->value.GetInt();
        }

        CallThreeIntegersReturnValue returnValue{ //initializer list

                                                  output1,
                                                  output2,
                                                  output3
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeIntegers");
}

boost::future<std::string> TestAbleClient::callOneString(const std::string& input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOneStringMethodCalls[correlationId] = boost::promise<std::string>();

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
    responseTopicStringStream << boost::format("client/%1%/callOneString/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOneString") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneStringMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOneStringResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOneStringMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOneStringMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        const std::string& output1 = std::string(output1Itr->value.GetString());

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneString");
}

boost::future<std::string> TestAbleClient::callOptionalString(boost::optional<std::string> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOptionalStringMethodCalls[correlationId] = boost::promise<std::string>();

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
    responseTopicStringStream << boost::format("client/%1%/callOptionalString/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOptionalString") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalStringMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOptionalStringResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOptionalStringMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOptionalStringMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // arg is optional, so check if it is set
        boost::optional<std::string> output1 = boost::none;
        if (output1Itr != doc.MemberEnd())
        {
            boost::optional<std::string> output1 = std::string(output1Itr->value.GetString());
        }

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalString");
}

boost::future<CallThreeStringsReturnValue> TestAbleClient::callThreeStrings(const std::string& input1, const std::string& input2, boost::optional<std::string> input3)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallThreeStringsMethodCalls[correlationId] = boost::promise<CallThreeStringsReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1.c_str(), input1.size(), doc.GetAllocator());
        doc.AddMember("input1", tempStringValue, doc.GetAllocator());
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input2.c_str(), input2.size(), doc.GetAllocator());
        doc.AddMember("input2", tempStringValue, doc.GetAllocator());
    }

    if (input3)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input3->c_str(), input3->size(), doc.GetAllocator());
        doc.AddMember("input3", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callThreeStrings/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callThreeStrings") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeStringsMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallThreeStringsResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallThreeStringsMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallThreeStringsMethodCalls.end())
    {
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        const std::string& output1 = std::string(output1Itr->value.GetString());

        rapidjson::Value::ConstMemberIterator output2Itr = doc.FindMember("output2");

        const std::string& output2 = std::string(output2Itr->value.GetString());

        rapidjson::Value::ConstMemberIterator output3Itr = doc.FindMember("output3");

        // arg is optional, so check if it is set
        boost::optional<std::string> output3 = boost::none;
        if (output3Itr != doc.MemberEnd())
        {
            boost::optional<std::string> output3 = std::string(output3Itr->value.GetString());
        }

        CallThreeStringsReturnValue returnValue{ //initializer list

                                                 output1,
                                                 output2,
                                                 output3
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeStrings");
}

boost::future<Numbers> TestAbleClient::callOneEnum(Numbers input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOneEnumMethodCalls[correlationId] = boost::promise<Numbers>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(input1), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOneEnum/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOneEnum") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneEnumMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOneEnumResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOneEnumMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOneEnumMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        Numbers output1 = static_cast<Numbers>(output1Itr->value.GetInt());

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneEnum");
}

boost::future<boost::optional<Numbers>> TestAbleClient::callOptionalEnum(boost::optional<Numbers> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOptionalEnumMethodCalls[correlationId] = boost::promise<boost::optional<Numbers>>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(*input1), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOptionalEnum/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOptionalEnum") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalEnumMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOptionalEnumResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOptionalEnumMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOptionalEnumMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // arg is optional, so check if it is set
        boost::optional<Numbers> output1 = boost::none;
        if (output1Itr != doc.MemberEnd())
        {
            boost::optional<Numbers> output1 = static_cast<boost::optional<Numbers>>(output1Itr->value.GetInt());
        }

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalEnum");
}

boost::future<CallThreeEnumsReturnValue> TestAbleClient::callThreeEnums(Numbers input1, Numbers input2, boost::optional<Numbers> input3)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallThreeEnumsMethodCalls[correlationId] = boost::promise<CallThreeEnumsReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(input1), doc.GetAllocator());

    doc.AddMember("input2", static_cast<int>(input2), doc.GetAllocator());

    doc.AddMember("input3", static_cast<int>(*input3), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callThreeEnums/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callThreeEnums") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeEnumsMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallThreeEnumsResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallThreeEnumsMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallThreeEnumsMethodCalls.end())
    {
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        Numbers output1 = static_cast<Numbers>(output1Itr->value.GetInt());

        rapidjson::Value::ConstMemberIterator output2Itr = doc.FindMember("output2");

        Numbers output2 = static_cast<Numbers>(output2Itr->value.GetInt());

        rapidjson::Value::ConstMemberIterator output3Itr = doc.FindMember("output3");

        // arg is optional, so check if it is set
        boost::optional<Numbers> output3 = boost::none;
        if (output3Itr != doc.MemberEnd())
        {
            boost::optional<Numbers> output3 = static_cast<boost::optional<Numbers>>(output3Itr->value.GetInt());
        }

        CallThreeEnumsReturnValue returnValue{ //initializer list

                                               output1,
                                               output2,
                                               output3
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeEnums");
}

boost::future<AllTypes> TestAbleClient::callOneStruct(AllTypes input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOneStructMethodCalls[correlationId] = boost::promise<AllTypes>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOneStruct/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOneStruct") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneStructMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOneStructResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOneStructMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOneStructMethodCalls.end())
    {
        // Response has multiple values.

        rapidjson::Value::ConstMemberIterator boolItr = doc.FindMember("bool_");

        bool bool_ = boolItr->value.GetBool();

        rapidjson::Value::ConstMemberIterator intItr = doc.FindMember("int_");

        int int_ = intItr->value.GetInt();

        rapidjson::Value::ConstMemberIterator numberItr = doc.FindMember("number");

        double number = numberItr->value.GetDouble();

        rapidjson::Value::ConstMemberIterator strItr = doc.FindMember("str");

        const std::string& str = std::string(strItr->value.GetString());

        rapidjson::Value::ConstMemberIterator enumItr = doc.FindMember("enum_");

        Numbers enum_ = static_cast<Numbers>(enumItr->value.GetInt());

        rapidjson::Value::ConstMemberIterator dateAndTimeItr = doc.FindMember("date_and_time");

        std::chrono::time_point<std::chrono::system_clock> date_and_time;
        if (dateAndTimeItr != doc.MemberEnd() && dateAndTimeItr->value.IsString())
        {
            date_and_time = parseIsoTimestamp(dateAndTimeItr->value.GetString());
        }

        rapidjson::Value::ConstMemberIterator timeDurationItr = doc.FindMember("time_duration");

        // <ArgPrimitive name=bool_ type=bool>

        // <ArgPrimitive name=int_ type=int>

        // <ArgPrimitive name=number type=float>

        // <ArgPrimitive name=str type=str>

        // <ArgEnum name=enum_>

        // <ArgDateTime name=date_and_time>

        // <ArgDuration name=time_duration>

        // <ArgBinary name=data>

        // <ArgPrimitive name=OptionalInteger type=int>

        // <ArgPrimitive name=OptionalString type=str>

        // <ArgEnum name=OptionalEnum>

        // <ArgDateTime name=OptionalDateTime>

        // <ArgDuration name=OptionalDuration>

        // <ArgBinary name=OptionalBinary>

        rapidjson::Value::ConstMemberIterator dataItr = doc.FindMember("data");

        // <ArgPrimitive name=bool_ type=bool>

        // <ArgPrimitive name=int_ type=int>

        // <ArgPrimitive name=number type=float>

        // <ArgPrimitive name=str type=str>

        // <ArgEnum name=enum_>

        // <ArgDateTime name=date_and_time>

        // <ArgDuration name=time_duration>

        // <ArgBinary name=data>

        // <ArgPrimitive name=OptionalInteger type=int>

        // <ArgPrimitive name=OptionalString type=str>

        // <ArgEnum name=OptionalEnum>

        // <ArgDateTime name=OptionalDateTime>

        // <ArgDuration name=OptionalDuration>

        // <ArgBinary name=OptionalBinary>

        rapidjson::Value::ConstMemberIterator optionalIntegerItr = doc.FindMember("OptionalInteger");

        // arg is optional, so check if it is set
        boost::optional<int> OptionalInteger = boost::none;
        if (optionalIntegerItr != doc.MemberEnd())
        {
            boost::optional<int> OptionalInteger = optionalIntegerItr->value.GetInt();
        }

        rapidjson::Value::ConstMemberIterator optionalStringItr = doc.FindMember("OptionalString");

        // arg is optional, so check if it is set
        boost::optional<std::string> OptionalString = boost::none;
        if (optionalStringItr != doc.MemberEnd())
        {
            boost::optional<std::string> OptionalString = std::string(optionalStringItr->value.GetString());
        }

        rapidjson::Value::ConstMemberIterator optionalEnumItr = doc.FindMember("OptionalEnum");

        // arg is optional, so check if it is set
        boost::optional<Numbers> OptionalEnum = boost::none;
        if (optionalEnumItr != doc.MemberEnd())
        {
            boost::optional<Numbers> OptionalEnum = static_cast<boost::optional<Numbers>>(optionalEnumItr->value.GetInt());
        }

        rapidjson::Value::ConstMemberIterator optionalDateTimeItr = doc.FindMember("OptionalDateTime");

        // arg is optional, so check if it is set
        boost::optional<std::chrono::time_point<std::chrono::system_clock>> OptionalDateTime = boost::none;
        if (optionalDateTimeItr != doc.MemberEnd())
        {
            boost::optional<std::chrono::time_point<std::chrono::system_clock>> OptionalDateTime;
            if (optionalDateTimeItr != doc.MemberEnd() && optionalDateTimeItr->value.IsString())
            {
                OptionalDateTime = parseIsoTimestamp(optionalDateTimeItr->value.GetString());
            }
        }

        rapidjson::Value::ConstMemberIterator optionalDurationItr = doc.FindMember("OptionalDuration");

        // arg is optional, so check if it is set
        boost::optional<std::chrono::duration<double>> OptionalDuration = boost::none;
        if (optionalDurationItr != doc.MemberEnd())
        {
            // <ArgPrimitive name=bool_ type=bool>

            // <ArgPrimitive name=int_ type=int>

            // <ArgPrimitive name=number type=float>

            // <ArgPrimitive name=str type=str>

            // <ArgEnum name=enum_>

            // <ArgDateTime name=date_and_time>

            // <ArgDuration name=time_duration>

            // <ArgBinary name=data>

            // <ArgPrimitive name=OptionalInteger type=int>

            // <ArgPrimitive name=OptionalString type=str>

            // <ArgEnum name=OptionalEnum>

            // <ArgDateTime name=OptionalDateTime>

            // <ArgDuration name=OptionalDuration>

            // <ArgBinary name=OptionalBinary>
        }

        rapidjson::Value::ConstMemberIterator optionalBinaryItr = doc.FindMember("OptionalBinary");

        // arg is optional, so check if it is set
        boost::optional<std::vector<uint8_t>> OptionalBinary = boost::none;
        if (optionalBinaryItr != doc.MemberEnd())
        {
            // <ArgPrimitive name=bool_ type=bool>

            // <ArgPrimitive name=int_ type=int>

            // <ArgPrimitive name=number type=float>

            // <ArgPrimitive name=str type=str>

            // <ArgEnum name=enum_>

            // <ArgDateTime name=date_and_time>

            // <ArgDuration name=time_duration>

            // <ArgBinary name=data>

            // <ArgPrimitive name=OptionalInteger type=int>

            // <ArgPrimitive name=OptionalString type=str>

            // <ArgEnum name=OptionalEnum>

            // <ArgDateTime name=OptionalDateTime>

            // <ArgDuration name=OptionalDuration>

            // <ArgBinary name=OptionalBinary>
        }

        AllTypes returnValue{ //initializer list

                              bool_,
                              int_,
                              number,
                              str,
                              enum_,
                              date_and_time,
                              time_duration,
                              data,
                              OptionalInteger,
                              OptionalString,
                              OptionalEnum,
                              OptionalDateTime,
                              OptionalDuration,
                              OptionalBinary
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneStruct");
}

boost::future<AllTypes> TestAbleClient::callOptionalStruct(AllTypes input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOptionalStructMethodCalls[correlationId] = boost::promise<AllTypes>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOptionalStruct/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOptionalStruct") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalStructMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOptionalStructResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOptionalStructMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOptionalStructMethodCalls.end())
    {
        // Response has multiple values.

        rapidjson::Value::ConstMemberIterator boolItr = doc.FindMember("bool_");

        bool bool_ = boolItr->value.GetBool();

        rapidjson::Value::ConstMemberIterator intItr = doc.FindMember("int_");

        int int_ = intItr->value.GetInt();

        rapidjson::Value::ConstMemberIterator numberItr = doc.FindMember("number");

        double number = numberItr->value.GetDouble();

        rapidjson::Value::ConstMemberIterator strItr = doc.FindMember("str");

        const std::string& str = std::string(strItr->value.GetString());

        rapidjson::Value::ConstMemberIterator enumItr = doc.FindMember("enum_");

        Numbers enum_ = static_cast<Numbers>(enumItr->value.GetInt());

        rapidjson::Value::ConstMemberIterator dateAndTimeItr = doc.FindMember("date_and_time");

        std::chrono::time_point<std::chrono::system_clock> date_and_time;
        if (dateAndTimeItr != doc.MemberEnd() && dateAndTimeItr->value.IsString())
        {
            date_and_time = parseIsoTimestamp(dateAndTimeItr->value.GetString());
        }

        rapidjson::Value::ConstMemberIterator timeDurationItr = doc.FindMember("time_duration");

        // <ArgPrimitive name=bool_ type=bool>

        // <ArgPrimitive name=int_ type=int>

        // <ArgPrimitive name=number type=float>

        // <ArgPrimitive name=str type=str>

        // <ArgEnum name=enum_>

        // <ArgDateTime name=date_and_time>

        // <ArgDuration name=time_duration>

        // <ArgBinary name=data>

        // <ArgPrimitive name=OptionalInteger type=int>

        // <ArgPrimitive name=OptionalString type=str>

        // <ArgEnum name=OptionalEnum>

        // <ArgDateTime name=OptionalDateTime>

        // <ArgDuration name=OptionalDuration>

        // <ArgBinary name=OptionalBinary>

        rapidjson::Value::ConstMemberIterator dataItr = doc.FindMember("data");

        // <ArgPrimitive name=bool_ type=bool>

        // <ArgPrimitive name=int_ type=int>

        // <ArgPrimitive name=number type=float>

        // <ArgPrimitive name=str type=str>

        // <ArgEnum name=enum_>

        // <ArgDateTime name=date_and_time>

        // <ArgDuration name=time_duration>

        // <ArgBinary name=data>

        // <ArgPrimitive name=OptionalInteger type=int>

        // <ArgPrimitive name=OptionalString type=str>

        // <ArgEnum name=OptionalEnum>

        // <ArgDateTime name=OptionalDateTime>

        // <ArgDuration name=OptionalDuration>

        // <ArgBinary name=OptionalBinary>

        rapidjson::Value::ConstMemberIterator optionalIntegerItr = doc.FindMember("OptionalInteger");

        // arg is optional, so check if it is set
        boost::optional<int> OptionalInteger = boost::none;
        if (optionalIntegerItr != doc.MemberEnd())
        {
            boost::optional<int> OptionalInteger = optionalIntegerItr->value.GetInt();
        }

        rapidjson::Value::ConstMemberIterator optionalStringItr = doc.FindMember("OptionalString");

        // arg is optional, so check if it is set
        boost::optional<std::string> OptionalString = boost::none;
        if (optionalStringItr != doc.MemberEnd())
        {
            boost::optional<std::string> OptionalString = std::string(optionalStringItr->value.GetString());
        }

        rapidjson::Value::ConstMemberIterator optionalEnumItr = doc.FindMember("OptionalEnum");

        // arg is optional, so check if it is set
        boost::optional<Numbers> OptionalEnum = boost::none;
        if (optionalEnumItr != doc.MemberEnd())
        {
            boost::optional<Numbers> OptionalEnum = static_cast<boost::optional<Numbers>>(optionalEnumItr->value.GetInt());
        }

        rapidjson::Value::ConstMemberIterator optionalDateTimeItr = doc.FindMember("OptionalDateTime");

        // arg is optional, so check if it is set
        boost::optional<std::chrono::time_point<std::chrono::system_clock>> OptionalDateTime = boost::none;
        if (optionalDateTimeItr != doc.MemberEnd())
        {
            boost::optional<std::chrono::time_point<std::chrono::system_clock>> OptionalDateTime;
            if (optionalDateTimeItr != doc.MemberEnd() && optionalDateTimeItr->value.IsString())
            {
                OptionalDateTime = parseIsoTimestamp(optionalDateTimeItr->value.GetString());
            }
        }

        rapidjson::Value::ConstMemberIterator optionalDurationItr = doc.FindMember("OptionalDuration");

        // arg is optional, so check if it is set
        boost::optional<std::chrono::duration<double>> OptionalDuration = boost::none;
        if (optionalDurationItr != doc.MemberEnd())
        {
            // <ArgPrimitive name=bool_ type=bool>

            // <ArgPrimitive name=int_ type=int>

            // <ArgPrimitive name=number type=float>

            // <ArgPrimitive name=str type=str>

            // <ArgEnum name=enum_>

            // <ArgDateTime name=date_and_time>

            // <ArgDuration name=time_duration>

            // <ArgBinary name=data>

            // <ArgPrimitive name=OptionalInteger type=int>

            // <ArgPrimitive name=OptionalString type=str>

            // <ArgEnum name=OptionalEnum>

            // <ArgDateTime name=OptionalDateTime>

            // <ArgDuration name=OptionalDuration>

            // <ArgBinary name=OptionalBinary>
        }

        rapidjson::Value::ConstMemberIterator optionalBinaryItr = doc.FindMember("OptionalBinary");

        // arg is optional, so check if it is set
        boost::optional<std::vector<uint8_t>> OptionalBinary = boost::none;
        if (optionalBinaryItr != doc.MemberEnd())
        {
            // <ArgPrimitive name=bool_ type=bool>

            // <ArgPrimitive name=int_ type=int>

            // <ArgPrimitive name=number type=float>

            // <ArgPrimitive name=str type=str>

            // <ArgEnum name=enum_>

            // <ArgDateTime name=date_and_time>

            // <ArgDuration name=time_duration>

            // <ArgBinary name=data>

            // <ArgPrimitive name=OptionalInteger type=int>

            // <ArgPrimitive name=OptionalString type=str>

            // <ArgEnum name=OptionalEnum>

            // <ArgDateTime name=OptionalDateTime>

            // <ArgDuration name=OptionalDuration>

            // <ArgBinary name=OptionalBinary>
        }

        AllTypes returnValue{ //initializer list

                              bool_,
                              int_,
                              number,
                              str,
                              enum_,
                              date_and_time,
                              time_duration,
                              data,
                              OptionalInteger,
                              OptionalString,
                              OptionalEnum,
                              OptionalDateTime,
                              OptionalDuration,
                              OptionalBinary
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalStruct");
}

boost::future<CallThreeStructsReturnValue> TestAbleClient::callThreeStructs(AllTypes input1, AllTypes input2, AllTypes input3)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallThreeStructsMethodCalls[correlationId] = boost::promise<CallThreeStructsReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callThreeStructs/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callThreeStructs") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeStructsMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallThreeStructsResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallThreeStructsMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallThreeStructsMethodCalls.end())
    {
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // <ArgStruct name=output1>

        // <ArgStruct name=output2>

        // <ArgStruct name=output3>

        rapidjson::Value::ConstMemberIterator output2Itr = doc.FindMember("output2");

        // <ArgStruct name=output1>

        // <ArgStruct name=output2>

        // <ArgStruct name=output3>

        rapidjson::Value::ConstMemberIterator output3Itr = doc.FindMember("output3");

        // arg is optional, so check if it is set
        AllTypes output3 = boost::none;
        if (output3Itr != doc.MemberEnd())
        {
            // <ArgStruct name=output1>

            // <ArgStruct name=output2>

            // <ArgStruct name=output3>
        }

        CallThreeStructsReturnValue returnValue{ //initializer list

                                                 output1,
                                                 output2,
                                                 output3
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeStructs");
}

boost::future<std::chrono::time_point<std::chrono::system_clock>> TestAbleClient::callOneDateTime(std::chrono::time_point<std::chrono::system_clock> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOneDateTimeMethodCalls[correlationId] = boost::promise<std::chrono::time_point<std::chrono::system_clock>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOneDateTime/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOneDateTime") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneDateTimeMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOneDateTimeResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOneDateTimeMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOneDateTimeMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        std::chrono::time_point<std::chrono::system_clock> output1;
        if (output1Itr != doc.MemberEnd() && output1Itr->value.IsString())
        {
            output1 = parseIsoTimestamp(output1Itr->value.GetString());
        }

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneDateTime");
}

boost::future<boost::optional<std::chrono::time_point<std::chrono::system_clock>>> TestAbleClient::callOptionalDateTime(boost::optional<std::chrono::time_point<std::chrono::system_clock>> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOptionalDateTimeMethodCalls[correlationId] = boost::promise<boost::optional<std::chrono::time_point<std::chrono::system_clock>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(*input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOptionalDateTime/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOptionalDateTime") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalDateTimeMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOptionalDateTimeResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOptionalDateTimeMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOptionalDateTimeMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // arg is optional, so check if it is set
        boost::optional<std::chrono::time_point<std::chrono::system_clock>> output1 = boost::none;
        if (output1Itr != doc.MemberEnd())
        {
            boost::optional<std::chrono::time_point<std::chrono::system_clock>> output1;
            if (output1Itr != doc.MemberEnd() && output1Itr->value.IsString())
            {
                output1 = parseIsoTimestamp(output1Itr->value.GetString());
            }
        }

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalDateTime");
}

boost::future<CallThreeDateTimesReturnValue> TestAbleClient::callThreeDateTimes(std::chrono::time_point<std::chrono::system_clock> input1, std::chrono::time_point<std::chrono::system_clock> input2, boost::optional<std::chrono::time_point<std::chrono::system_clock>> input3)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallThreeDateTimesMethodCalls[correlationId] = boost::promise<CallThreeDateTimesReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempInput2StringValue;
        std::string input2IsoString = timePointToIsoString(input2);
        tempInput2StringValue.SetString(input2IsoString.c_str(), input2IsoString.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempInput3StringValue;
        std::string input3IsoString = timePointToIsoString(*input3);
        tempInput3StringValue.SetString(input3IsoString.c_str(), input3IsoString.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callThreeDateTimes/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callThreeDateTimes") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeDateTimesMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallThreeDateTimesResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallThreeDateTimesMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallThreeDateTimesMethodCalls.end())
    {
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        std::chrono::time_point<std::chrono::system_clock> output1;
        if (output1Itr != doc.MemberEnd() && output1Itr->value.IsString())
        {
            output1 = parseIsoTimestamp(output1Itr->value.GetString());
        }

        rapidjson::Value::ConstMemberIterator output2Itr = doc.FindMember("output2");

        std::chrono::time_point<std::chrono::system_clock> output2;
        if (output2Itr != doc.MemberEnd() && output2Itr->value.IsString())
        {
            output2 = parseIsoTimestamp(output2Itr->value.GetString());
        }

        rapidjson::Value::ConstMemberIterator output3Itr = doc.FindMember("output3");

        // arg is optional, so check if it is set
        boost::optional<std::chrono::time_point<std::chrono::system_clock>> output3 = boost::none;
        if (output3Itr != doc.MemberEnd())
        {
            boost::optional<std::chrono::time_point<std::chrono::system_clock>> output3;
            if (output3Itr != doc.MemberEnd() && output3Itr->value.IsString())
            {
                output3 = parseIsoTimestamp(output3Itr->value.GetString());
            }
        }

        CallThreeDateTimesReturnValue returnValue{ //initializer list

                                                   output1,
                                                   output2,
                                                   output3
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeDateTimes");
}

boost::future<std::chrono::duration<double>> TestAbleClient::callOneDuration(std::chrono::duration<double> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOneDurationMethodCalls[correlationId] = boost::promise<std::chrono::duration<double>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOneDuration/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOneDuration") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneDurationMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOneDurationResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOneDurationMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOneDurationMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        std::chrono::duration<double> output1;
        if (output1Itr != doc.MemberEnd() && output1Itr->value.IsString())
        {
            output1 = parseIsoDuration(output1Itr->value.GetString());
        }

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneDuration");
}

boost::future<boost::optional<std::chrono::duration<double>>> TestAbleClient::callOptionalDuration(boost::optional<std::chrono::duration<double>> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOptionalDurationMethodCalls[correlationId] = boost::promise<boost::optional<std::chrono::duration<double>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(*input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOptionalDuration/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOptionalDuration") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalDurationMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOptionalDurationResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOptionalDurationMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOptionalDurationMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // arg is optional, so check if it is set
        boost::optional<std::chrono::duration<double>> output1 = boost::none;
        if (output1Itr != doc.MemberEnd())
        {
            boost::optional<std::chrono::duration<double>> output1;
            if (output1Itr != doc.MemberEnd() && output1Itr->value.IsString())
            {
                output1 = parseIsoDuration(output1Itr->value.GetString());
            }
        }

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalDuration");
}

boost::future<CallThreeDurationsReturnValue> TestAbleClient::callThreeDurations(std::chrono::duration<double> input1, std::chrono::duration<double> input2, boost::optional<std::chrono::duration<double>> input3)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallThreeDurationsMethodCalls[correlationId] = boost::promise<CallThreeDurationsReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempInput2StringValue;
        std::string input2IsoString = durationToIsoString(input2);
        tempInput2StringValue.SetString(input2IsoString.c_str(), input2IsoString.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempInput3StringValue;
        std::string input3IsoString = durationToIsoString(*input3);
        tempInput3StringValue.SetString(input3IsoString.c_str(), input3IsoString.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callThreeDurations/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callThreeDurations") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeDurationsMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallThreeDurationsResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallThreeDurationsMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallThreeDurationsMethodCalls.end())
    {
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // <ArgDuration name=output1>

        // <ArgDuration name=output2>

        // <ArgDuration name=output3>

        rapidjson::Value::ConstMemberIterator output2Itr = doc.FindMember("output2");

        // <ArgDuration name=output1>

        // <ArgDuration name=output2>

        // <ArgDuration name=output3>

        rapidjson::Value::ConstMemberIterator output3Itr = doc.FindMember("output3");

        // arg is optional, so check if it is set
        boost::optional<std::chrono::duration<double>> output3 = boost::none;
        if (output3Itr != doc.MemberEnd())
        {
            // <ArgDuration name=output1>

            // <ArgDuration name=output2>

            // <ArgDuration name=output3>
        }

        CallThreeDurationsReturnValue returnValue{ //initializer list

                                                   output1,
                                                   output2,
                                                   output3
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeDurations");
}

boost::future<std::vector<uint8_t>> TestAbleClient::callOneBinary(std::vector<uint8_t> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOneBinaryMethodCalls[correlationId] = boost::promise<std::vector<uint8_t>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOneBinary/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOneBinary") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOneBinaryMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOneBinaryResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOneBinaryMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOneBinaryMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        TEMPLATE ERROR with unhandled return value type binary

                promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneBinary");
}

boost::future<boost::optional<std::vector<uint8_t>>> TestAbleClient::callOptionalBinary(boost::optional<std::vector<uint8_t>> input1)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallOptionalBinaryMethodCalls[correlationId] = boost::promise<boost::optional<std::vector<uint8_t>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(*input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callOptionalBinary/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callOptionalBinary") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallOptionalBinaryMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallOptionalBinaryResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallOptionalBinaryMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallOptionalBinaryMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // arg is optional, so check if it is set
        boost::optional<std::vector<uint8_t>> output1 = boost::none;
        if (output1Itr != doc.MemberEnd())
        {
            TEMPLATE ERROR with unhandled return value type binary
        }

        promiseItr->second.set_value(output1);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalBinary");
}

boost::future<CallThreeBinariesReturnValue> TestAbleClient::callThreeBinaries(std::vector<uint8_t> input1, std::vector<uint8_t> input2, boost::optional<std::vector<uint8_t>> input3)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingCallThreeBinariesMethodCalls[correlationId] = boost::promise<CallThreeBinariesReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempInput2StringValue;
        std::string input2B64String = base64Encode(input2);
        tempInput2StringValue.SetString(input2B64String.c_str(), input2B64String.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempInput3StringValue;
        std::string input3B64String = base64Encode(*input3);
        tempInput3StringValue.SetString(input3B64String.c_str(), input3B64String.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/callThreeBinaries/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish((boost::format("testAble/%1%/method/callThreeBinaries") % _instanceId).str(), buf.GetString(), 2, false, mqttProps);

    return _pendingCallThreeBinariesMethodCalls[correlationId].get_future();
}

void TestAbleClient::_handleCallThreeBinariesResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
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
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingCallThreeBinariesMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingCallThreeBinariesMethodCalls.end())
    {
        rapidjson::Value::ConstMemberIterator output1Itr = doc.FindMember("output1");

        // <ArgBinary name=output1>

        // <ArgBinary name=output2>

        // <ArgBinary name=output3>

        rapidjson::Value::ConstMemberIterator output2Itr = doc.FindMember("output2");

        // <ArgBinary name=output1>

        // <ArgBinary name=output2>

        // <ArgBinary name=output3>

        rapidjson::Value::ConstMemberIterator output3Itr = doc.FindMember("output3");

        // arg is optional, so check if it is set
        boost::optional<std::vector<uint8_t>> output3 = boost::none;
        if (output3Itr != doc.MemberEnd())
        {
            // <ArgBinary name=output1>

            // <ArgBinary name=output2>

            // <ArgBinary name=output3>
        }

        CallThreeBinariesReturnValue returnValue{ //initializer list

                                                  output1,
                                                  output2,
                                                  output3
        };
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeBinaries");
}

void TestAbleClient::_receiveReadWriteIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_integer payload is not an object");
    }
    ReadWriteIntegerProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteIntegerProperty> TestAbleClient::getReadWriteIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    return _readWriteIntegerProperty;
}

void TestAbleClient::registerReadWriteIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
    _readWriteIntegerPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteIntegerProperty(int value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteInteger/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadOnlyIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_only_integer payload is not an object");
    }
    ReadOnlyIntegerProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadOnlyIntegerProperty> TestAbleClient::getReadOnlyIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    return _readOnlyIntegerProperty;
}

void TestAbleClient::registerReadOnlyIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
    _readOnlyIntegerPropertyCallbacks.push_back(cb);
}

void TestAbleClient::_receiveReadWriteOptionalIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_optional_integer payload is not an object");
    }
    ReadWriteOptionalIntegerProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = itr->value.GetInt();
    }
    else
    {
        tempValue = boost::none;
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteOptionalIntegerProperty> TestAbleClient::getReadWriteOptionalIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    return _readWriteOptionalIntegerProperty;
}

void TestAbleClient::registerReadWriteOptionalIntegerPropertyCallback(const std::function<void(boost::optional<int> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
    _readWriteOptionalIntegerPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteOptionalIntegerProperty(boost::optional<int> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    if (value)
        doc.AddMember("value", *value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteOptionalInteger/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteTwoIntegersPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_two_integers payload is not an object");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            tempValue.second = boost::none;
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

boost::optional<ReadWriteTwoIntegersProperty> TestAbleClient::getReadWriteTwoIntegersProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
    return _readWriteTwoIntegersProperty;
}

void TestAbleClient::registerReadWriteTwoIntegersPropertyCallback(const std::function<void(int first, boost::optional<int> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
    _readWriteTwoIntegersPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteTwoIntegersProperty(int first, boost::optional<int> second) const
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
    return _broker->Publish("testAble/%1%/property/readWriteTwoIntegers/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadOnlyStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_only_string payload is not an object");
    }
    ReadOnlyStringProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
        tempValue = itr->value.GetString();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadOnlyStringProperty> TestAbleClient::getReadOnlyStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    return _readOnlyStringProperty;
}

void TestAbleClient::registerReadOnlyStringPropertyCallback(const std::function<void(const std::string& value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
    _readOnlyStringPropertyCallbacks.push_back(cb);
}

void TestAbleClient::_receiveReadWriteStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_string payload is not an object");
    }
    ReadWriteStringProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
        tempValue = itr->value.GetString();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteStringProperty> TestAbleClient::getReadWriteStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    return _readWriteStringProperty;
}

void TestAbleClient::registerReadWriteStringPropertyCallback(const std::function<void(const std::string& value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
    _readWriteStringPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteStringProperty(const std::string& value) const
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
    return _broker->Publish("testAble/%1%/property/readWriteString/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteOptionalStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_optional_string payload is not an object");
    }
    ReadWriteOptionalStringProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
        tempValue = itr->value.GetString();
    }
    else
    {
        tempValue = boost::none;
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteOptionalStringProperty> TestAbleClient::getReadWriteOptionalStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    return _readWriteOptionalStringProperty;
}

void TestAbleClient::registerReadWriteOptionalStringPropertyCallback(const std::function<void(boost::optional<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
    _readWriteOptionalStringPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteOptionalStringProperty(boost::optional<std::string> value) const
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
    return _broker->Publish("testAble/%1%/property/readWriteOptionalString/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteTwoStringsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_two_strings payload is not an object");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            tempValue.second = boost::none;
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

boost::optional<ReadWriteTwoStringsProperty> TestAbleClient::getReadWriteTwoStringsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
    return _readWriteTwoStringsProperty;
}

void TestAbleClient::registerReadWriteTwoStringsPropertyCallback(const std::function<void(const std::string& first, boost::optional<std::string> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
    _readWriteTwoStringsPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteTwoStringsProperty(const std::string& first, boost::optional<std::string> second) const
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
    return _broker->Publish("testAble/%1%/property/readWriteTwoStrings/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteStructPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_struct payload is not an object");
    }
    ReadWriteStructProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsObject())
    {
        tempValue = AllTypes::FromRapidJsonObject(itr->value);
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteStructProperty> TestAbleClient::getReadWriteStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    return _readWriteStructProperty;
}

void TestAbleClient::registerReadWriteStructPropertyCallback(const std::function<void(AllTypes value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
    _readWriteStructPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteStructProperty(AllTypes value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteStruct/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteOptionalStructPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_optional_struct payload is not an object");
    }
    ReadWriteOptionalStructProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsObject())
    {
        tempValue = AllTypes::FromRapidJsonObject(itr->value);
    }
    else
    {
        tempValue = boost::none;
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteOptionalStructProperty> TestAbleClient::getReadWriteOptionalStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    return _readWriteOptionalStructProperty;
}

void TestAbleClient::registerReadWriteOptionalStructPropertyCallback(const std::function<void(AllTypes value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
    _readWriteOptionalStructPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteOptionalStructProperty(AllTypes value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteOptionalStruct/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteTwoStructsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_two_structs payload is not an object");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            tempValue.second = boost::none;
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

boost::optional<ReadWriteTwoStructsProperty> TestAbleClient::getReadWriteTwoStructsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
    return _readWriteTwoStructsProperty;
}

void TestAbleClient::registerReadWriteTwoStructsPropertyCallback(const std::function<void(AllTypes first, AllTypes second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
    _readWriteTwoStructsPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteTwoStructsProperty(AllTypes first, AllTypes second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteTwoStructs/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadOnlyEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_only_enum payload is not an object");
    }
    ReadOnlyEnumProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = static_cast<Numbers>(itr->value.GetInt());
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadOnlyEnumProperty> TestAbleClient::getReadOnlyEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    return _readOnlyEnumProperty;
}

void TestAbleClient::registerReadOnlyEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
    _readOnlyEnumPropertyCallbacks.push_back(cb);
}

void TestAbleClient::_receiveReadWriteEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_enum payload is not an object");
    }
    ReadWriteEnumProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = static_cast<Numbers>(itr->value.GetInt());
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteEnumProperty> TestAbleClient::getReadWriteEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    return _readWriteEnumProperty;
}

void TestAbleClient::registerReadWriteEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
    _readWriteEnumPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteEnumProperty(Numbers value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteEnum/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteOptionalEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_optional_enum payload is not an object");
    }
    ReadWriteOptionalEnumProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = static_cast<Numbers>(itr->value.GetInt());
    }
    else
    {
        tempValue = boost::none;
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteOptionalEnumProperty> TestAbleClient::getReadWriteOptionalEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    return _readWriteOptionalEnumProperty;
}

void TestAbleClient::registerReadWriteOptionalEnumPropertyCallback(const std::function<void(boost::optional<Numbers> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
    _readWriteOptionalEnumPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteOptionalEnumProperty(boost::optional<Numbers> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(*value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteOptionalEnum/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteTwoEnumsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_two_enums payload is not an object");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            tempValue.second = boost::none;
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

boost::optional<ReadWriteTwoEnumsProperty> TestAbleClient::getReadWriteTwoEnumsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
    return _readWriteTwoEnumsProperty;
}

void TestAbleClient::registerReadWriteTwoEnumsPropertyCallback(const std::function<void(Numbers first, boost::optional<Numbers> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
    _readWriteTwoEnumsPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteTwoEnumsProperty(Numbers first, boost::optional<Numbers> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", static_cast<int>(first), doc.GetAllocator());

    doc.AddMember("second", static_cast<int>(*second), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteTwoEnums/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteDatetimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_datetime payload is not an object");
    }
    ReadWriteDatetimeProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteDatetimeProperty> TestAbleClient::getReadWriteDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    return _readWriteDatetimeProperty;
}

void TestAbleClient::registerReadWriteDatetimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
    _readWriteDatetimePropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteDatetimeProperty(std::chrono::time_point<std::chrono::system_clock> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = timePointToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteDatetime/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteOptionalDatetimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_optional_datetime payload is not an object");
    }
    ReadWriteOptionalDatetimeProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        tempValue = boost::none;
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteOptionalDatetimeProperty> TestAbleClient::getReadWriteOptionalDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    return _readWriteOptionalDatetimeProperty;
}

void TestAbleClient::registerReadWriteOptionalDatetimePropertyCallback(const std::function<void(boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
    _readWriteOptionalDatetimePropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteOptionalDatetimeProperty(boost::optional<std::chrono::time_point<std::chrono::system_clock>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = timePointToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteOptionalDatetime/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteTwoDatetimesPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_two_datetimes payload is not an object");
    }
    ReadWriteTwoDatetimesProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            tempValue.second = boost::none;
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

boost::optional<ReadWriteTwoDatetimesProperty> TestAbleClient::getReadWriteTwoDatetimesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
    return _readWriteTwoDatetimesProperty;
}

void TestAbleClient::registerReadWriteTwoDatetimesPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> first, boost::optional<std::chrono::time_point<std::chrono::system_clock>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
    _readWriteTwoDatetimesPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteTwoDatetimesProperty(std::chrono::time_point<std::chrono::system_clock> first, boost::optional<std::chrono::time_point<std::chrono::system_clock>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = timePointToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = timePointToIsoString(*second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteTwoDatetimes/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteDurationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_duration payload is not an object");
    }
    ReadWriteDurationProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteDurationProperty> TestAbleClient::getReadWriteDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    return _readWriteDurationProperty;
}

void TestAbleClient::registerReadWriteDurationPropertyCallback(const std::function<void(std::chrono::duration<double> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
    _readWriteDurationPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteDurationProperty(std::chrono::duration<double> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = durationToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteDuration/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteOptionalDurationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_optional_duration payload is not an object");
    }
    ReadWriteOptionalDurationProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        tempValue = boost::none;
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteOptionalDurationProperty> TestAbleClient::getReadWriteOptionalDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    return _readWriteOptionalDurationProperty;
}

void TestAbleClient::registerReadWriteOptionalDurationPropertyCallback(const std::function<void(boost::optional<std::chrono::duration<double>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
    _readWriteOptionalDurationPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteOptionalDurationProperty(boost::optional<std::chrono::duration<double>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = durationToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteOptionalDuration/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteTwoDurationsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_two_durations payload is not an object");
    }
    ReadWriteTwoDurationsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            tempValue.second = boost::none;
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

boost::optional<ReadWriteTwoDurationsProperty> TestAbleClient::getReadWriteTwoDurationsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
    return _readWriteTwoDurationsProperty;
}

void TestAbleClient::registerReadWriteTwoDurationsPropertyCallback(const std::function<void(std::chrono::duration<double> first, boost::optional<std::chrono::duration<double>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
    _readWriteTwoDurationsPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteTwoDurationsProperty(std::chrono::duration<double> first, boost::optional<std::chrono::duration<double>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = durationToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = durationToIsoString(*second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteTwoDurations/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteBinaryPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_binary payload is not an object");
    }
    ReadWriteBinaryProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteBinaryProperty> TestAbleClient::getReadWriteBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    return _readWriteBinaryProperty;
}

void TestAbleClient::registerReadWriteBinaryPropertyCallback(const std::function<void(std::vector<uint8_t> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
    _readWriteBinaryPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteBinaryProperty(std::vector<uint8_t> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = base64Encode(value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteBinary/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteOptionalBinaryPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_optional_binary payload is not an object");
    }
    ReadWriteOptionalBinaryProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        tempValue = boost::none;
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

            cb(tempValue);
        }
    }
}

boost::optional<ReadWriteOptionalBinaryProperty> TestAbleClient::getReadWriteOptionalBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    return _readWriteOptionalBinaryProperty;
}

void TestAbleClient::registerReadWriteOptionalBinaryPropertyCallback(const std::function<void(boost::optional<std::vector<uint8_t>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
    _readWriteOptionalBinaryPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteOptionalBinaryProperty(boost::optional<std::vector<uint8_t>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = base64Encode(*value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteOptionalBinary/setValue", buf.GetString(), 1, false, mqttProps);
}

void TestAbleClient::_receiveReadWriteTwoBinariesPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received read_write_two_binaries payload is not an object");
    }
    ReadWriteTwoBinariesProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            tempValue.second = boost::none;
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

boost::optional<ReadWriteTwoBinariesProperty> TestAbleClient::getReadWriteTwoBinariesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
    return _readWriteTwoBinariesProperty;
}

void TestAbleClient::registerReadWriteTwoBinariesPropertyCallback(const std::function<void(std::vector<uint8_t> first, boost::optional<std::vector<uint8_t>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
    _readWriteTwoBinariesPropertyCallbacks.push_back(cb);
}

boost::future<bool> TestAbleClient::updateReadWriteTwoBinariesProperty(std::vector<uint8_t> first, boost::optional<std::vector<uint8_t>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstB64String = base64Encode(first);
        tempFirstStringValue.SetString(firstB64String.c_str(), firstB64String.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondB64String = base64Encode(*second);
        tempSecondStringValue.SetString(secondB64String.c_str(), secondB64String.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("testAble/%1%/property/readWriteTwoBinaries/setValue", buf.GetString(), 1, false, mqttProps);
}
