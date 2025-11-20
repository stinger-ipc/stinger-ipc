

#include <vector>
#include <iostream>
#include <syslog.h>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "server.hpp"
#include "method_payloads.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"

constexpr const char TestableServer::NAME[];
constexpr const char TestableServer::INTERFACE_VERSION[];

TestableServer::TestableServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId): _broker(broker), _instanceId(instanceId), _advertisementThreadRunning(false)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _receiveMessage(topic, payload, mqttProps);
                                                               });

    _callWithNothingMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callWithNothing") % _instanceId).str(), 2);
    _callOneIntegerMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOneInteger") % _instanceId).str(), 2);
    _callOptionalIntegerMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOptionalInteger") % _instanceId).str(), 2);
    _callThreeIntegersMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callThreeIntegers") % _instanceId).str(), 2);
    _callOneStringMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOneString") % _instanceId).str(), 2);
    _callOptionalStringMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOptionalString") % _instanceId).str(), 2);
    _callThreeStringsMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callThreeStrings") % _instanceId).str(), 2);
    _callOneEnumMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOneEnum") % _instanceId).str(), 2);
    _callOptionalEnumMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOptionalEnum") % _instanceId).str(), 2);
    _callThreeEnumsMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callThreeEnums") % _instanceId).str(), 2);
    _callOneStructMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOneStruct") % _instanceId).str(), 2);
    _callOptionalStructMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOptionalStruct") % _instanceId).str(), 2);
    _callThreeStructsMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callThreeStructs") % _instanceId).str(), 2);
    _callOneDateTimeMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOneDateTime") % _instanceId).str(), 2);
    _callOptionalDateTimeMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOptionalDateTime") % _instanceId).str(), 2);
    _callThreeDateTimesMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callThreeDateTimes") % _instanceId).str(), 2);
    _callOneDurationMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOneDuration") % _instanceId).str(), 2);
    _callOptionalDurationMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOptionalDuration") % _instanceId).str(), 2);
    _callThreeDurationsMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callThreeDurations") % _instanceId).str(), 2);
    _callOneBinaryMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOneBinary") % _instanceId).str(), 2);
    _callOptionalBinaryMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOptionalBinary") % _instanceId).str(), 2);
    _callThreeBinariesMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callThreeBinaries") % _instanceId).str(), 2);
    _callOneListOfIntegersMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOneListOfIntegers") % _instanceId).str(), 2);
    _callOptionalListOfFloatsMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callOptionalListOfFloats") % _instanceId).str(), 2);
    _callTwoListsMethodSubscriptionId = _broker->Subscribe((boost::format("testable/%1%/method/callTwoLists") % _instanceId).str(), 2);

    _readWriteIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteInteger/setValue") % _instanceId).str(), 1);
    _readOnlyIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readOnlyInteger/setValue") % _instanceId).str(), 1);
    _readWriteOptionalIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteOptionalInteger/setValue") % _instanceId).str(), 1);
    _readWriteTwoIntegersPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteTwoIntegers/setValue") % _instanceId).str(), 1);
    _readOnlyStringPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readOnlyString/setValue") % _instanceId).str(), 1);
    _readWriteStringPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteString/setValue") % _instanceId).str(), 1);
    _readWriteOptionalStringPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteOptionalString/setValue") % _instanceId).str(), 1);
    _readWriteTwoStringsPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteTwoStrings/setValue") % _instanceId).str(), 1);
    _readWriteStructPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteStruct/setValue") % _instanceId).str(), 1);
    _readWriteOptionalStructPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteOptionalStruct/setValue") % _instanceId).str(), 1);
    _readWriteTwoStructsPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteTwoStructs/setValue") % _instanceId).str(), 1);
    _readOnlyEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readOnlyEnum/setValue") % _instanceId).str(), 1);
    _readWriteEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteEnum/setValue") % _instanceId).str(), 1);
    _readWriteOptionalEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteOptionalEnum/setValue") % _instanceId).str(), 1);
    _readWriteTwoEnumsPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteTwoEnums/setValue") % _instanceId).str(), 1);
    _readWriteDatetimePropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteDatetime/setValue") % _instanceId).str(), 1);
    _readWriteOptionalDatetimePropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteOptionalDatetime/setValue") % _instanceId).str(), 1);
    _readWriteTwoDatetimesPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteTwoDatetimes/setValue") % _instanceId).str(), 1);
    _readWriteDurationPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteDuration/setValue") % _instanceId).str(), 1);
    _readWriteOptionalDurationPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteOptionalDuration/setValue") % _instanceId).str(), 1);
    _readWriteTwoDurationsPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteTwoDurations/setValue") % _instanceId).str(), 1);
    _readWriteBinaryPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteBinary/setValue") % _instanceId).str(), 1);
    _readWriteOptionalBinaryPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteOptionalBinary/setValue") % _instanceId).str(), 1);
    _readWriteTwoBinariesPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteTwoBinaries/setValue") % _instanceId).str(), 1);
    _readWriteListOfStringsPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteListOfStrings/setValue") % _instanceId).str(), 1);
    _readWriteListsPropertySubscriptionId = _broker->Subscribe((boost::format("testable/%1%/property/readWriteLists/setValue") % _instanceId).str(), 1);

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&TestableServer::_advertisementThreadLoop, this);
}

TestableServer::~TestableServer()
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

    std::string topic = (boost::format("testable/%1%/interface") % _instanceId).str();
    _broker->Publish(topic, "", 1, true, MqttProperties());

    _broker->Unsubscribe((boost::format("testable/%1%/method/callWithNothing") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOneInteger") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOptionalInteger") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callThreeIntegers") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOneString") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOptionalString") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callThreeStrings") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOneEnum") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOptionalEnum") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callThreeEnums") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOneStruct") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOptionalStruct") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callThreeStructs") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOneDateTime") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOptionalDateTime") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callThreeDateTimes") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOneDuration") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOptionalDuration") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callThreeDurations") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOneBinary") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOptionalBinary") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callThreeBinaries") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOneListOfIntegers") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callOptionalListOfFloats") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/method/callTwoLists") % _instanceId).str());

    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteInteger/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readOnlyInteger/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteOptionalInteger/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteTwoIntegers/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readOnlyString/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteString/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteOptionalString/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteTwoStrings/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteStruct/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteOptionalStruct/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteTwoStructs/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readOnlyEnum/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteEnum/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteOptionalEnum/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteTwoEnums/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteDatetime/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteOptionalDatetime/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteTwoDatetimes/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteDuration/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteOptionalDuration/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteTwoDurations/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteBinary/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteOptionalBinary/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteTwoBinaries/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteListOfStrings/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testable/%1%/property/readWriteLists/setValue") % _instanceId).str());
}

void TestableServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);

    if ((subscriptionId == _callWithNothingMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callWithNothing") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callWithNothing method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callWithNothingHandler)
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

                _callCallWithNothingHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOneIntegerMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOneInteger") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneInteger method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOneIntegerHandler)
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

                _callCallOneIntegerHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOptionalIntegerMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOptionalInteger") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalInteger method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOptionalIntegerHandler)
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

                _callCallOptionalIntegerHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callThreeIntegersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callThreeIntegers") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeIntegers method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callThreeIntegersHandler)
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

                _callCallThreeIntegersHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOneStringMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOneString") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneString method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOneStringHandler)
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

                _callCallOneStringHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOptionalStringMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOptionalString") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalString method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOptionalStringHandler)
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

                _callCallOptionalStringHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callThreeStringsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callThreeStrings") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeStrings method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callThreeStringsHandler)
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

                _callCallThreeStringsHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOneEnumMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOneEnum") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneEnum method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOneEnumHandler)
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

                _callCallOneEnumHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOptionalEnumMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOptionalEnum") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalEnum method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOptionalEnumHandler)
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

                _callCallOptionalEnumHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callThreeEnumsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callThreeEnums") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeEnums method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callThreeEnumsHandler)
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

                _callCallThreeEnumsHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOneStructMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOneStruct") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneStruct method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOneStructHandler)
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

                _callCallOneStructHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOptionalStructMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOptionalStruct") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalStruct method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOptionalStructHandler)
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

                _callCallOptionalStructHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callThreeStructsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callThreeStructs") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeStructs method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callThreeStructsHandler)
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

                _callCallThreeStructsHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOneDateTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOneDateTime") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneDateTime method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOneDateTimeHandler)
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

                _callCallOneDateTimeHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOptionalDateTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOptionalDateTime") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalDateTime method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOptionalDateTimeHandler)
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

                _callCallOptionalDateTimeHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callThreeDateTimesMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callThreeDateTimes") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeDateTimes method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callThreeDateTimesHandler)
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

                _callCallThreeDateTimesHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOneDurationMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOneDuration") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneDuration method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOneDurationHandler)
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

                _callCallOneDurationHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOptionalDurationMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOptionalDuration") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalDuration method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOptionalDurationHandler)
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

                _callCallOptionalDurationHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callThreeDurationsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callThreeDurations") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeDurations method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callThreeDurationsHandler)
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

                _callCallThreeDurationsHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOneBinaryMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOneBinary") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneBinary method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOneBinaryHandler)
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

                _callCallOneBinaryHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOptionalBinaryMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOptionalBinary") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalBinary method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOptionalBinaryHandler)
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

                _callCallOptionalBinaryHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callThreeBinariesMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callThreeBinaries") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeBinaries method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callThreeBinariesHandler)
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

                _callCallThreeBinariesHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOneListOfIntegersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOneListOfIntegers") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneListOfIntegers method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOneListOfIntegersHandler)
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

                _callCallOneListOfIntegersHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callOptionalListOfFloatsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callOptionalListOfFloats") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalListOfFloats method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callOptionalListOfFloatsHandler)
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

                _callCallOptionalListOfFloatsHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _callTwoListsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/method/callTwoLists") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callTwoLists method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_callTwoListsHandler)
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

                _callCallTwoListsHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    if (subscriptionId == _readWriteIntegerPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteInteger/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_integer property update.", topic.c_str());
        _receiveReadWriteIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readOnlyIntegerPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readOnlyInteger/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_integer property update.", topic.c_str());
        _receiveReadOnlyIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalIntegerPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteOptionalInteger/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_integer property update.", topic.c_str());
        _receiveReadWriteOptionalIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoIntegersPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteTwoIntegers/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_integers property update.", topic.c_str());
        _receiveReadWriteTwoIntegersPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readOnlyStringPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readOnlyString/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_string property update.", topic.c_str());
        _receiveReadOnlyStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteStringPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteString/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_string property update.", topic.c_str());
        _receiveReadWriteStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalStringPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteOptionalString/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_string property update.", topic.c_str());
        _receiveReadWriteOptionalStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoStringsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteTwoStrings/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_strings property update.", topic.c_str());
        _receiveReadWriteTwoStringsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteStructPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteStruct/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_struct property update.", topic.c_str());
        _receiveReadWriteStructPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalStructPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteOptionalStruct/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_struct property update.", topic.c_str());
        _receiveReadWriteOptionalStructPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoStructsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteTwoStructs/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_structs property update.", topic.c_str());
        _receiveReadWriteTwoStructsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readOnlyEnumPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readOnlyEnum/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_enum property update.", topic.c_str());
        _receiveReadOnlyEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteEnumPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteEnum/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_enum property update.", topic.c_str());
        _receiveReadWriteEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalEnumPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteOptionalEnum/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_enum property update.", topic.c_str());
        _receiveReadWriteOptionalEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoEnumsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteTwoEnums/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_enums property update.", topic.c_str());
        _receiveReadWriteTwoEnumsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteDatetimePropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteDatetime/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_datetime property update.", topic.c_str());
        _receiveReadWriteDatetimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalDatetimePropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteOptionalDatetime/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_datetime property update.", topic.c_str());
        _receiveReadWriteOptionalDatetimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoDatetimesPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteTwoDatetimes/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_datetimes property update.", topic.c_str());
        _receiveReadWriteTwoDatetimesPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteDurationPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteDuration/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_duration property update.", topic.c_str());
        _receiveReadWriteDurationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalDurationPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteOptionalDuration/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_duration property update.", topic.c_str());
        _receiveReadWriteOptionalDurationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoDurationsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteTwoDurations/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_durations property update.", topic.c_str());
        _receiveReadWriteTwoDurationsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteBinaryPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteBinary/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_binary property update.", topic.c_str());
        _receiveReadWriteBinaryPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalBinaryPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteOptionalBinary/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_binary property update.", topic.c_str());
        _receiveReadWriteOptionalBinaryPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoBinariesPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteTwoBinaries/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_binaries property update.", topic.c_str());
        _receiveReadWriteTwoBinariesPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteListOfStringsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteListOfStrings/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_list_of_strings property update.", topic.c_str());
        _receiveReadWriteListOfStringsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteListsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testable/%1%/property/readWriteLists/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_lists property update.", topic.c_str());
        _receiveReadWriteListsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

boost::future<bool> TestableServer::emitEmptySignal()
{
    rapidjson::Document doc;
    doc.SetObject();
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/empty") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleIntSignal(int value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/singleInt") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleOptionalIntSignal(boost::optional<int> value)
{
    rapidjson::Document doc;
    doc.SetObject();
    if (value)
        doc.AddMember("value", *value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/singleOptionalInt") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitThreeIntegersSignal(int first, int second, boost::optional<int> third)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", first, doc.GetAllocator());

    doc.AddMember("second", second, doc.GetAllocator());

    if (third)
        doc.AddMember("third", *third, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/threeIntegers") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleStringSignal(const std::string& value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleString") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleOptionalStringSignal(boost::optional<std::string> value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleOptionalString") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitThreeStringsSignal(const std::string& first, const std::string& second, boost::optional<std::string> third)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(first.c_str(), first.size(), doc.GetAllocator());
        doc.AddMember("first", tempStringValue, doc.GetAllocator());
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(second.c_str(), second.size(), doc.GetAllocator());
        doc.AddMember("second", tempStringValue, doc.GetAllocator());
    }

    if (third)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(third->c_str(), third->size(), doc.GetAllocator());
        doc.AddMember("third", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/threeStrings") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleEnumSignal(Numbers value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/singleEnum") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleOptionalEnumSignal(boost::optional<Numbers> value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(*value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/singleOptionalEnum") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitThreeEnumsSignal(Numbers first, Numbers second, boost::optional<Numbers> third)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", static_cast<int>(first), doc.GetAllocator());

    doc.AddMember("second", static_cast<int>(second), doc.GetAllocator());

    doc.AddMember("third", static_cast<int>(*third), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/threeEnums") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleStructSignal(AllTypes value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleStruct") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleOptionalStructSignal(boost::optional<AllTypes> value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleOptionalStruct") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitThreeStructsSignal(AllTypes first, AllTypes second, boost::optional<AllTypes> third)
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

        tempStructValue.SetObject();
        second.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("second", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (third)
        {
            tempStructValue.SetObject();
            third->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        }
        else
        {
            tempStructValue.SetNull();
        }
        doc.AddMember("third", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/threeStructs") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleDateTimeSignal(std::chrono::time_point<std::chrono::system_clock> value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleDateTime") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleOptionalDatetimeSignal(boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleOptionalDatetime") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitThreeDateTimesSignal(std::chrono::time_point<std::chrono::system_clock> first, std::chrono::time_point<std::chrono::system_clock> second, boost::optional<std::chrono::time_point<std::chrono::system_clock>> third)
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
        std::string secondIsoString = timePointToIsoString(second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempThirdStringValue;
        std::string thirdIsoString = timePointToIsoString(*third);
        tempThirdStringValue.SetString(thirdIsoString.c_str(), thirdIsoString.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/threeDateTimes") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleDurationSignal(std::chrono::duration<double> value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleDuration") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleOptionalDurationSignal(boost::optional<std::chrono::duration<double>> value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleOptionalDuration") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitThreeDurationsSignal(std::chrono::duration<double> first, std::chrono::duration<double> second, boost::optional<std::chrono::duration<double>> third)
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
        std::string secondIsoString = durationToIsoString(second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempThirdStringValue;
        std::string thirdIsoString = durationToIsoString(*third);
        tempThirdStringValue.SetString(thirdIsoString.c_str(), thirdIsoString.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/threeDurations") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleBinarySignal(std::vector<uint8_t> value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleBinary") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleOptionalBinarySignal(boost::optional<std::vector<uint8_t>> value)
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
    return _broker->Publish((boost::format("testable/%1%/signal/singleOptionalBinary") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitThreeBinariesSignal(std::vector<uint8_t> first, std::vector<uint8_t> second, boost::optional<std::vector<uint8_t>> third)
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
        std::string secondB64String = base64Encode(second);
        tempSecondStringValue.SetString(secondB64String.c_str(), secondB64String.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempThirdStringValue;
        std::string thirdB64String = base64Encode(*third);
        tempThirdStringValue.SetString(thirdB64String.c_str(), thirdB64String.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/threeBinaries") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleArrayOfIntegersSignal(std::vector<int> values)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: values)
        {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("values", tempArrayValue, doc.GetAllocator());
    }
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/singleArrayOfIntegers") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitSingleOptionalArrayOfStringsSignal(boost::optional<std::vector<std::string>> values)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *values)
        {
            rapidjson::Value tempValuesStringValue;
            tempValuesStringValue.SetString(item.c_str(), item.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempValuesStringValue, doc.GetAllocator());
        }
        doc.AddMember("values", tempArrayValue, doc.GetAllocator());
    }
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/singleOptionalArrayOfStrings") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestableServer::emitArrayOfEveryTypeSignal(std::vector<int> firstOfIntegers, std::vector<double> secondOfFloats, std::vector<std::string> thirdOfStrings, std::vector<Numbers> fourthOfEnums, std::vector<Entry> fifthOfStructs, std::vector<std::chrono::time_point<std::chrono::system_clock>> sixthOfDatetimes, std::vector<std::chrono::duration<double>> seventhOfDurations, std::vector<std::vector<uint8_t>> eighthOfBinaries)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: firstOfIntegers)
        {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("first_of_integers", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: secondOfFloats)
        {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("second_of_floats", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: thirdOfStrings)
        {
            rapidjson::Value tempThirdOfStringsStringValue;
            tempThirdOfStringsStringValue.SetString(item.c_str(), item.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempThirdOfStringsStringValue, doc.GetAllocator());
        }
        doc.AddMember("third_of_strings", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: fourthOfEnums)
        {
            tempArrayValue.PushBack(static_cast<int>(item), doc.GetAllocator());
        }
        doc.AddMember("fourth_of_enums", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: fifthOfStructs)
        {
            rapidjson::Value tempFifthOfStructsObjectValue;
            tempFifthOfStructsObjectValue.SetObject();
            item.AddToRapidJsonObject(tempFifthOfStructsObjectValue, doc.GetAllocator());
            tempArrayValue.PushBack(tempFifthOfStructsObjectValue, doc.GetAllocator());
        }
        doc.AddMember("fifth_of_structs", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: sixthOfDatetimes)
        {
            rapidjson::Value tempSixthOfDatetimesStringValue;
            std::string itemIsoString = timePointToIsoString(item);
            tempSixthOfDatetimesStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempSixthOfDatetimesStringValue, doc.GetAllocator());
        }
        doc.AddMember("sixth_of_datetimes", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: seventhOfDurations)
        {
            rapidjson::Value tempSeventhOfDurationsStringValue;
            std::string itemIsoString = durationToIsoString(item);
            tempSeventhOfDurationsStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempSeventhOfDurationsStringValue, doc.GetAllocator());
        }
        doc.AddMember("seventh_of_durations", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: eighthOfBinaries)
        {
            rapidjson::Value tempEighthOfBinariesStringValue;
            std::string itemB64String = base64Encode(item);
            tempEighthOfBinariesStringValue.SetString(itemB64String.c_str(), itemB64String.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempEighthOfBinariesStringValue, doc.GetAllocator());
        }
        doc.AddMember("eighth_of_binaries", tempArrayValue, doc.GetAllocator());
    }
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testable/%1%/signal/arrayOfEveryType") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::registerCallWithNothingHandler(std::function<void()> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callWithNothing method requests.");
    _callWithNothingHandler = func;
}

void TestableServer::registerCallOneIntegerHandler(std::function<int(int)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOneInteger method requests.");
    _callOneIntegerHandler = func;
}

void TestableServer::registerCallOptionalIntegerHandler(std::function<boost::optional<int>(boost::optional<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOptionalInteger method requests.");
    _callOptionalIntegerHandler = func;
}

void TestableServer::registerCallThreeIntegersHandler(std::function<CallThreeIntegersReturnValues(int, int, boost::optional<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callThreeIntegers method requests.");
    _callThreeIntegersHandler = func;
}

void TestableServer::registerCallOneStringHandler(std::function<std::string(std::string)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOneString method requests.");
    _callOneStringHandler = func;
}

void TestableServer::registerCallOptionalStringHandler(std::function<boost::optional<std::string>(boost::optional<std::string>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOptionalString method requests.");
    _callOptionalStringHandler = func;
}

void TestableServer::registerCallThreeStringsHandler(std::function<CallThreeStringsReturnValues(std::string, boost::optional<std::string>, std::string)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callThreeStrings method requests.");
    _callThreeStringsHandler = func;
}

void TestableServer::registerCallOneEnumHandler(std::function<Numbers(Numbers)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOneEnum method requests.");
    _callOneEnumHandler = func;
}

void TestableServer::registerCallOptionalEnumHandler(std::function<boost::optional<Numbers>(boost::optional<Numbers>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOptionalEnum method requests.");
    _callOptionalEnumHandler = func;
}

void TestableServer::registerCallThreeEnumsHandler(std::function<CallThreeEnumsReturnValues(Numbers, Numbers, boost::optional<Numbers>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callThreeEnums method requests.");
    _callThreeEnumsHandler = func;
}

void TestableServer::registerCallOneStructHandler(std::function<AllTypes(AllTypes)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOneStruct method requests.");
    _callOneStructHandler = func;
}

void TestableServer::registerCallOptionalStructHandler(std::function<boost::optional<AllTypes>(boost::optional<AllTypes>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOptionalStruct method requests.");
    _callOptionalStructHandler = func;
}

void TestableServer::registerCallThreeStructsHandler(std::function<CallThreeStructsReturnValues(boost::optional<AllTypes>, AllTypes, AllTypes)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callThreeStructs method requests.");
    _callThreeStructsHandler = func;
}

void TestableServer::registerCallOneDateTimeHandler(std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::time_point<std::chrono::system_clock>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOneDateTime method requests.");
    _callOneDateTimeHandler = func;
}

void TestableServer::registerCallOptionalDateTimeHandler(std::function<boost::optional<std::chrono::time_point<std::chrono::system_clock>>(boost::optional<std::chrono::time_point<std::chrono::system_clock>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOptionalDateTime method requests.");
    _callOptionalDateTimeHandler = func;
}

void TestableServer::registerCallThreeDateTimesHandler(std::function<CallThreeDateTimesReturnValues(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callThreeDateTimes method requests.");
    _callThreeDateTimesHandler = func;
}

void TestableServer::registerCallOneDurationHandler(std::function<std::chrono::duration<double>(std::chrono::duration<double>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOneDuration method requests.");
    _callOneDurationHandler = func;
}

void TestableServer::registerCallOptionalDurationHandler(std::function<boost::optional<std::chrono::duration<double>>(boost::optional<std::chrono::duration<double>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOptionalDuration method requests.");
    _callOptionalDurationHandler = func;
}

void TestableServer::registerCallThreeDurationsHandler(std::function<CallThreeDurationsReturnValues(std::chrono::duration<double>, std::chrono::duration<double>, boost::optional<std::chrono::duration<double>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callThreeDurations method requests.");
    _callThreeDurationsHandler = func;
}

void TestableServer::registerCallOneBinaryHandler(std::function<std::vector<uint8_t>(std::vector<uint8_t>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOneBinary method requests.");
    _callOneBinaryHandler = func;
}

void TestableServer::registerCallOptionalBinaryHandler(std::function<boost::optional<std::vector<uint8_t>>(boost::optional<std::vector<uint8_t>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOptionalBinary method requests.");
    _callOptionalBinaryHandler = func;
}

void TestableServer::registerCallThreeBinariesHandler(std::function<CallThreeBinariesReturnValues(std::vector<uint8_t>, std::vector<uint8_t>, boost::optional<std::vector<uint8_t>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callThreeBinaries method requests.");
    _callThreeBinariesHandler = func;
}

void TestableServer::registerCallOneListOfIntegersHandler(std::function<std::vector<int>(std::vector<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOneListOfIntegers method requests.");
    _callOneListOfIntegersHandler = func;
}

void TestableServer::registerCallOptionalListOfFloatsHandler(std::function<boost::optional<std::vector<double>>(boost::optional<std::vector<double>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callOptionalListOfFloats method requests.");
    _callOptionalListOfFloatsHandler = func;
}

void TestableServer::registerCallTwoListsHandler(std::function<CallTwoListsReturnValues(std::vector<Numbers>, boost::optional<std::vector<std::string>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testable/+/method/callTwoLists method requests.");
    _callTwoListsHandler = func;
}

void TestableServer::_callCallWithNothingHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callWithNothing");
    if (!_callWithNothingHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    // Method doesn't have any return values.
    _callWithNothingHandler();
    auto returnValues = CallWithNothingReturnValues();

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

void TestableServer::_callCallOneIntegerHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneInteger");
    if (!_callOneIntegerHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneIntegerRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneIntegerHandler(requestArgs.input1);
    CallOneIntegerReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallOptionalIntegerHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalInteger");
    if (!_callOptionalIntegerHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalIntegerRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalIntegerHandler(requestArgs.input1);
    CallOptionalIntegerReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallThreeIntegersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeIntegers");
    if (!_callThreeIntegersHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeIntegersRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeIntegersHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

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

void TestableServer::_callCallOneStringHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneString");
    if (!_callOneStringHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneStringRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneStringHandler(requestArgs.input1);
    CallOneStringReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallOptionalStringHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalString");
    if (!_callOptionalStringHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalStringRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalStringHandler(requestArgs.input1);
    CallOptionalStringReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallThreeStringsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeStrings");
    if (!_callThreeStringsHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeStringsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeStringsHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

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

void TestableServer::_callCallOneEnumHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneEnum");
    if (!_callOneEnumHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneEnumRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneEnumHandler(requestArgs.input1);
    CallOneEnumReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallOptionalEnumHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalEnum");
    if (!_callOptionalEnumHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalEnumRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalEnumHandler(requestArgs.input1);
    CallOptionalEnumReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallThreeEnumsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeEnums");
    if (!_callThreeEnumsHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeEnumsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeEnumsHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

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

void TestableServer::_callCallOneStructHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneStruct");
    if (!_callOneStructHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneStructRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneStructHandler(requestArgs.input1);
    CallOneStructReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallOptionalStructHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalStruct");
    if (!_callOptionalStructHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalStructRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalStructHandler(requestArgs.input1);
    CallOptionalStructReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallThreeStructsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeStructs");
    if (!_callThreeStructsHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeStructsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeStructsHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

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

void TestableServer::_callCallOneDateTimeHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneDateTime");
    if (!_callOneDateTimeHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneDateTimeRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneDateTimeHandler(requestArgs.input1);
    CallOneDateTimeReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallOptionalDateTimeHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalDateTime");
    if (!_callOptionalDateTimeHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalDateTimeRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalDateTimeHandler(requestArgs.input1);
    CallOptionalDateTimeReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallThreeDateTimesHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeDateTimes");
    if (!_callThreeDateTimesHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeDateTimesRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeDateTimesHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

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

void TestableServer::_callCallOneDurationHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneDuration");
    if (!_callOneDurationHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneDurationRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneDurationHandler(requestArgs.input1);
    CallOneDurationReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallOptionalDurationHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalDuration");
    if (!_callOptionalDurationHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalDurationRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalDurationHandler(requestArgs.input1);
    CallOptionalDurationReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallThreeDurationsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeDurations");
    if (!_callThreeDurationsHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeDurationsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeDurationsHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

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

void TestableServer::_callCallOneBinaryHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneBinary");
    if (!_callOneBinaryHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneBinaryRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneBinaryHandler(requestArgs.input1);
    CallOneBinaryReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallOptionalBinaryHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalBinary");
    if (!_callOptionalBinaryHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalBinaryRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalBinaryHandler(requestArgs.input1);
    CallOptionalBinaryReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallThreeBinariesHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeBinaries");
    if (!_callThreeBinariesHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeBinariesRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeBinariesHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

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

void TestableServer::_callCallOneListOfIntegersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneListOfIntegers");
    if (!_callOneListOfIntegersHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneListOfIntegersRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneListOfIntegersHandler(requestArgs.input1);
    CallOneListOfIntegersReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallOptionalListOfFloatsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalListOfFloats");
    if (!_callOptionalListOfFloatsHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalListOfFloatsRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalListOfFloatsHandler(requestArgs.input1);
    CallOptionalListOfFloatsReturnValues returnValues = { returnValue };

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

void TestableServer::_callCallTwoListsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callTwoLists");
    if (!_callTwoListsHandler)
    {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallTwoListsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callTwoListsHandler(requestArgs.input1, requestArgs.input2);

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

boost::optional<int> TestableServer::getReadWriteIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    if (_readWriteIntegerProperty)
    {
        return _readWriteIntegerProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
    _readWriteIntegerPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteIntegerProperty(int value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
        _readWriteIntegerProperty = ReadWriteIntegerProperty{ value };
        _lastReadWriteIntegerPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readWriteIntegerPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteIntegerProperty();
}

void TestableServer::republishReadWriteIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteIntegerProperty)
    {
        doc.SetObject();
        _readWriteIntegerProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteIntegerPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteInteger/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_integer payload is not an object or null");
    }

    // TODO: Check _lastReadWriteIntegerPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteIntegerProperty tempValue = ReadWriteIntegerProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
        _readWriteIntegerProperty = tempValue;
        _lastReadWriteIntegerPropertyVersion++;
    }
    republishReadWriteIntegerProperty();
}

boost::optional<int> TestableServer::getReadOnlyIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    if (_readOnlyIntegerProperty)
    {
        return _readOnlyIntegerProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadOnlyIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
    _readOnlyIntegerPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadOnlyIntegerProperty(int value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
        _readOnlyIntegerProperty = ReadOnlyIntegerProperty{ value };
        _lastReadOnlyIntegerPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyIntegerPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadOnlyIntegerProperty();
}

void TestableServer::republishReadOnlyIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyIntegerProperty)
    {
        doc.SetObject();
        _readOnlyIntegerProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadOnlyIntegerPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readOnlyInteger/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadOnlyIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_only_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_only_integer payload is not an object or null");
    }

    // TODO: Check _lastReadOnlyIntegerPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadOnlyIntegerProperty tempValue = ReadOnlyIntegerProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
        _readOnlyIntegerProperty = tempValue;
        _lastReadOnlyIntegerPropertyVersion++;
    }
    republishReadOnlyIntegerProperty();
}

boost::optional<int> TestableServer::getReadWriteOptionalIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    if (_readWriteOptionalIntegerProperty)
    {
        return _readWriteOptionalIntegerProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteOptionalIntegerPropertyCallback(const std::function<void(boost::optional<int> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
    _readWriteOptionalIntegerPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalIntegerProperty(boost::optional<int> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
        _readWriteOptionalIntegerProperty = ReadWriteOptionalIntegerProperty{ value };
        _lastReadWriteOptionalIntegerPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalIntegerPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteOptionalIntegerProperty();
}

void TestableServer::republishReadWriteOptionalIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalIntegerProperty)
    {
        doc.SetObject();
        _readWriteOptionalIntegerProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteOptionalIntegerPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteOptionalInteger/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteOptionalIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_optional_integer payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalIntegerPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalIntegerProperty tempValue = ReadWriteOptionalIntegerProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
        _readWriteOptionalIntegerProperty = tempValue;
        _lastReadWriteOptionalIntegerPropertyVersion++;
    }
    republishReadWriteOptionalIntegerProperty();
}

boost::optional<ReadWriteTwoIntegersProperty> TestableServer::getReadWriteTwoIntegersProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
    if (_readWriteTwoIntegersProperty)
    {
        return *_readWriteTwoIntegersProperty;
    }
    return boost::none;
}

void TestableServer::registerReadWriteTwoIntegersPropertyCallback(const std::function<void(int first, boost::optional<int> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
    _readWriteTwoIntegersPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoIntegersProperty(int first, boost::optional<int> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
        _readWriteTwoIntegersProperty = ReadWriteTwoIntegersProperty{ first, second };
        _lastReadWriteTwoIntegersPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoIntegersPropertyCallbacks)
        {
            cb(first, second);
        }
    }
    republishReadWriteTwoIntegersProperty();
}

void TestableServer::republishReadWriteTwoIntegersProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoIntegersProperty)
    {
        doc.SetObject();
        _readWriteTwoIntegersProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteTwoIntegersPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteTwoIntegers/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteTwoIntegersPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_integers property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_two_integers payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoIntegersPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoIntegersProperty tempValue = ReadWriteTwoIntegersProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
        _readWriteTwoIntegersProperty = tempValue;
        _lastReadWriteTwoIntegersPropertyVersion++;
    }
    republishReadWriteTwoIntegersProperty();
}

boost::optional<const std::string&> TestableServer::getReadOnlyStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    if (_readOnlyStringProperty)
    {
        return _readOnlyStringProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadOnlyStringPropertyCallback(const std::function<void(std::string value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
    _readOnlyStringPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadOnlyStringProperty(std::string value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
        _readOnlyStringProperty = ReadOnlyStringProperty{ value };
        _lastReadOnlyStringPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyStringPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadOnlyStringProperty();
}

void TestableServer::republishReadOnlyStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyStringProperty)
    {
        doc.SetObject();
        _readOnlyStringProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadOnlyStringPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readOnlyString/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadOnlyStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_only_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_only_string payload is not an object or null");
    }

    // TODO: Check _lastReadOnlyStringPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadOnlyStringProperty tempValue = ReadOnlyStringProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
        _readOnlyStringProperty = tempValue;
        _lastReadOnlyStringPropertyVersion++;
    }
    republishReadOnlyStringProperty();
}

boost::optional<const std::string&> TestableServer::getReadWriteStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    if (_readWriteStringProperty)
    {
        return _readWriteStringProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteStringPropertyCallback(const std::function<void(std::string value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
    _readWriteStringPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteStringProperty(std::string value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
        _readWriteStringProperty = ReadWriteStringProperty{ value };
        _lastReadWriteStringPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
        for (const auto& cb: _readWriteStringPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteStringProperty();
}

void TestableServer::republishReadWriteStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteStringProperty)
    {
        doc.SetObject();
        _readWriteStringProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteStringPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteString/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_string payload is not an object or null");
    }

    // TODO: Check _lastReadWriteStringPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteStringProperty tempValue = ReadWriteStringProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
        _readWriteStringProperty = tempValue;
        _lastReadWriteStringPropertyVersion++;
    }
    republishReadWriteStringProperty();
}

boost::optional<std::string> TestableServer::getReadWriteOptionalStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    if (_readWriteOptionalStringProperty)
    {
        return _readWriteOptionalStringProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteOptionalStringPropertyCallback(const std::function<void(boost::optional<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
    _readWriteOptionalStringPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalStringProperty(boost::optional<std::string> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
        _readWriteOptionalStringProperty = ReadWriteOptionalStringProperty{ value };
        _lastReadWriteOptionalStringPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalStringPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteOptionalStringProperty();
}

void TestableServer::republishReadWriteOptionalStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalStringProperty)
    {
        doc.SetObject();
        _readWriteOptionalStringProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteOptionalStringPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteOptionalString/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteOptionalStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_optional_string payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalStringPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalStringProperty tempValue = ReadWriteOptionalStringProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
        _readWriteOptionalStringProperty = tempValue;
        _lastReadWriteOptionalStringPropertyVersion++;
    }
    republishReadWriteOptionalStringProperty();
}

boost::optional<ReadWriteTwoStringsProperty> TestableServer::getReadWriteTwoStringsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
    if (_readWriteTwoStringsProperty)
    {
        return *_readWriteTwoStringsProperty;
    }
    return boost::none;
}

void TestableServer::registerReadWriteTwoStringsPropertyCallback(const std::function<void(std::string first, boost::optional<std::string> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
    _readWriteTwoStringsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoStringsProperty(std::string first, boost::optional<std::string> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
        _readWriteTwoStringsProperty = ReadWriteTwoStringsProperty{ first, second };
        _lastReadWriteTwoStringsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoStringsPropertyCallbacks)
        {
            cb(first, second);
        }
    }
    republishReadWriteTwoStringsProperty();
}

void TestableServer::republishReadWriteTwoStringsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoStringsProperty)
    {
        doc.SetObject();
        _readWriteTwoStringsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteTwoStringsPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteTwoStrings/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteTwoStringsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_strings property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_two_strings payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoStringsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoStringsProperty tempValue = ReadWriteTwoStringsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
        _readWriteTwoStringsProperty = tempValue;
        _lastReadWriteTwoStringsPropertyVersion++;
    }
    republishReadWriteTwoStringsProperty();
}

boost::optional<AllTypes> TestableServer::getReadWriteStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    if (_readWriteStructProperty)
    {
        return _readWriteStructProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteStructPropertyCallback(const std::function<void(AllTypes value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
    _readWriteStructPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteStructProperty(AllTypes value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
        _readWriteStructProperty = ReadWriteStructProperty{ value };
        _lastReadWriteStructPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
        for (const auto& cb: _readWriteStructPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteStructProperty();
}

void TestableServer::republishReadWriteStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteStructProperty)
    {
        doc.SetObject();
        _readWriteStructProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteStructPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteStruct/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteStructPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_struct property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_struct payload is not an object or null");
    }

    // TODO: Check _lastReadWriteStructPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteStructProperty tempValue = ReadWriteStructProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
        _readWriteStructProperty = tempValue;
        _lastReadWriteStructPropertyVersion++;
    }
    republishReadWriteStructProperty();
}

boost::optional<AllTypes> TestableServer::getReadWriteOptionalStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    if (_readWriteOptionalStructProperty)
    {
        return _readWriteOptionalStructProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteOptionalStructPropertyCallback(const std::function<void(boost::optional<AllTypes> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
    _readWriteOptionalStructPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalStructProperty(boost::optional<AllTypes> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
        _readWriteOptionalStructProperty = ReadWriteOptionalStructProperty{ value };
        _lastReadWriteOptionalStructPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalStructPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteOptionalStructProperty();
}

void TestableServer::republishReadWriteOptionalStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalStructProperty)
    {
        doc.SetObject();
        _readWriteOptionalStructProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteOptionalStructPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteOptionalStruct/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteOptionalStructPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_struct property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_optional_struct payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalStructPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalStructProperty tempValue = ReadWriteOptionalStructProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
        _readWriteOptionalStructProperty = tempValue;
        _lastReadWriteOptionalStructPropertyVersion++;
    }
    republishReadWriteOptionalStructProperty();
}

boost::optional<ReadWriteTwoStructsProperty> TestableServer::getReadWriteTwoStructsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
    if (_readWriteTwoStructsProperty)
    {
        return *_readWriteTwoStructsProperty;
    }
    return boost::none;
}

void TestableServer::registerReadWriteTwoStructsPropertyCallback(const std::function<void(AllTypes first, boost::optional<AllTypes> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
    _readWriteTwoStructsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoStructsProperty(AllTypes first, boost::optional<AllTypes> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
        _readWriteTwoStructsProperty = ReadWriteTwoStructsProperty{ first, second };
        _lastReadWriteTwoStructsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoStructsPropertyCallbacks)
        {
            cb(first, second);
        }
    }
    republishReadWriteTwoStructsProperty();
}

void TestableServer::republishReadWriteTwoStructsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoStructsProperty)
    {
        doc.SetObject();
        _readWriteTwoStructsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteTwoStructsPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteTwoStructs/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteTwoStructsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_structs property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_two_structs payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoStructsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoStructsProperty tempValue = ReadWriteTwoStructsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
        _readWriteTwoStructsProperty = tempValue;
        _lastReadWriteTwoStructsPropertyVersion++;
    }
    republishReadWriteTwoStructsProperty();
}

boost::optional<Numbers> TestableServer::getReadOnlyEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    if (_readOnlyEnumProperty)
    {
        return _readOnlyEnumProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadOnlyEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
    _readOnlyEnumPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadOnlyEnumProperty(Numbers value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
        _readOnlyEnumProperty = ReadOnlyEnumProperty{ value };
        _lastReadOnlyEnumPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyEnumPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadOnlyEnumProperty();
}

void TestableServer::republishReadOnlyEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyEnumProperty)
    {
        doc.SetObject();
        _readOnlyEnumProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadOnlyEnumPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readOnlyEnum/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadOnlyEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_only_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_only_enum payload is not an object or null");
    }

    // TODO: Check _lastReadOnlyEnumPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadOnlyEnumProperty tempValue = ReadOnlyEnumProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
        _readOnlyEnumProperty = tempValue;
        _lastReadOnlyEnumPropertyVersion++;
    }
    republishReadOnlyEnumProperty();
}

boost::optional<Numbers> TestableServer::getReadWriteEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    if (_readWriteEnumProperty)
    {
        return _readWriteEnumProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
    _readWriteEnumPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteEnumProperty(Numbers value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
        _readWriteEnumProperty = ReadWriteEnumProperty{ value };
        _lastReadWriteEnumPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
        for (const auto& cb: _readWriteEnumPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteEnumProperty();
}

void TestableServer::republishReadWriteEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteEnumProperty)
    {
        doc.SetObject();
        _readWriteEnumProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteEnumPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteEnum/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_enum payload is not an object or null");
    }

    // TODO: Check _lastReadWriteEnumPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteEnumProperty tempValue = ReadWriteEnumProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
        _readWriteEnumProperty = tempValue;
        _lastReadWriteEnumPropertyVersion++;
    }
    republishReadWriteEnumProperty();
}

boost::optional<Numbers> TestableServer::getReadWriteOptionalEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    if (_readWriteOptionalEnumProperty)
    {
        return _readWriteOptionalEnumProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteOptionalEnumPropertyCallback(const std::function<void(boost::optional<Numbers> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
    _readWriteOptionalEnumPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalEnumProperty(boost::optional<Numbers> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
        _readWriteOptionalEnumProperty = ReadWriteOptionalEnumProperty{ value };
        _lastReadWriteOptionalEnumPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalEnumPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteOptionalEnumProperty();
}

void TestableServer::republishReadWriteOptionalEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalEnumProperty)
    {
        doc.SetObject();
        _readWriteOptionalEnumProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteOptionalEnumPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteOptionalEnum/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteOptionalEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_optional_enum payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalEnumPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalEnumProperty tempValue = ReadWriteOptionalEnumProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
        _readWriteOptionalEnumProperty = tempValue;
        _lastReadWriteOptionalEnumPropertyVersion++;
    }
    republishReadWriteOptionalEnumProperty();
}

boost::optional<ReadWriteTwoEnumsProperty> TestableServer::getReadWriteTwoEnumsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
    if (_readWriteTwoEnumsProperty)
    {
        return *_readWriteTwoEnumsProperty;
    }
    return boost::none;
}

void TestableServer::registerReadWriteTwoEnumsPropertyCallback(const std::function<void(Numbers first, boost::optional<Numbers> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
    _readWriteTwoEnumsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoEnumsProperty(Numbers first, boost::optional<Numbers> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
        _readWriteTwoEnumsProperty = ReadWriteTwoEnumsProperty{ first, second };
        _lastReadWriteTwoEnumsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoEnumsPropertyCallbacks)
        {
            cb(first, second);
        }
    }
    republishReadWriteTwoEnumsProperty();
}

void TestableServer::republishReadWriteTwoEnumsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoEnumsProperty)
    {
        doc.SetObject();
        _readWriteTwoEnumsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteTwoEnumsPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteTwoEnums/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteTwoEnumsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_enums property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_two_enums payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoEnumsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoEnumsProperty tempValue = ReadWriteTwoEnumsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
        _readWriteTwoEnumsProperty = tempValue;
        _lastReadWriteTwoEnumsPropertyVersion++;
    }
    republishReadWriteTwoEnumsProperty();
}

boost::optional<std::chrono::time_point<std::chrono::system_clock>> TestableServer::getReadWriteDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    if (_readWriteDatetimeProperty)
    {
        return _readWriteDatetimeProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteDatetimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
    _readWriteDatetimePropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteDatetimeProperty(std::chrono::time_point<std::chrono::system_clock> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
        _readWriteDatetimeProperty = ReadWriteDatetimeProperty{ value };
        _lastReadWriteDatetimePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
        for (const auto& cb: _readWriteDatetimePropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteDatetimeProperty();
}

void TestableServer::republishReadWriteDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    rapidjson::Document doc;
    if (_readWriteDatetimeProperty)
    {
        doc.SetObject();
        _readWriteDatetimeProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteDatetimePropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteDatetime/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteDatetimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_datetime property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_datetime payload is not an object or null");
    }

    // TODO: Check _lastReadWriteDatetimePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteDatetimeProperty tempValue = ReadWriteDatetimeProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
        _readWriteDatetimeProperty = tempValue;
        _lastReadWriteDatetimePropertyVersion++;
    }
    republishReadWriteDatetimeProperty();
}

boost::optional<std::chrono::time_point<std::chrono::system_clock>> TestableServer::getReadWriteOptionalDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    if (_readWriteOptionalDatetimeProperty)
    {
        return _readWriteOptionalDatetimeProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteOptionalDatetimePropertyCallback(const std::function<void(boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
    _readWriteOptionalDatetimePropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalDatetimeProperty(boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
        _readWriteOptionalDatetimeProperty = ReadWriteOptionalDatetimeProperty{ value };
        _lastReadWriteOptionalDatetimePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalDatetimePropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteOptionalDatetimeProperty();
}

void TestableServer::republishReadWriteOptionalDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalDatetimeProperty)
    {
        doc.SetObject();
        _readWriteOptionalDatetimeProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteOptionalDatetimePropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteOptionalDatetime/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteOptionalDatetimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_datetime property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_optional_datetime payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalDatetimePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalDatetimeProperty tempValue = ReadWriteOptionalDatetimeProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
        _readWriteOptionalDatetimeProperty = tempValue;
        _lastReadWriteOptionalDatetimePropertyVersion++;
    }
    republishReadWriteOptionalDatetimeProperty();
}

boost::optional<ReadWriteTwoDatetimesProperty> TestableServer::getReadWriteTwoDatetimesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
    if (_readWriteTwoDatetimesProperty)
    {
        return *_readWriteTwoDatetimesProperty;
    }
    return boost::none;
}

void TestableServer::registerReadWriteTwoDatetimesPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> first, boost::optional<std::chrono::time_point<std::chrono::system_clock>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
    _readWriteTwoDatetimesPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoDatetimesProperty(std::chrono::time_point<std::chrono::system_clock> first, boost::optional<std::chrono::time_point<std::chrono::system_clock>> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
        _readWriteTwoDatetimesProperty = ReadWriteTwoDatetimesProperty{ first, second };
        _lastReadWriteTwoDatetimesPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoDatetimesPropertyCallbacks)
        {
            cb(first, second);
        }
    }
    republishReadWriteTwoDatetimesProperty();
}

void TestableServer::republishReadWriteTwoDatetimesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoDatetimesProperty)
    {
        doc.SetObject();
        _readWriteTwoDatetimesProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteTwoDatetimesPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteTwoDatetimes/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteTwoDatetimesPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_datetimes property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_two_datetimes payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoDatetimesPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoDatetimesProperty tempValue = ReadWriteTwoDatetimesProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
        _readWriteTwoDatetimesProperty = tempValue;
        _lastReadWriteTwoDatetimesPropertyVersion++;
    }
    republishReadWriteTwoDatetimesProperty();
}

boost::optional<std::chrono::duration<double>> TestableServer::getReadWriteDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    if (_readWriteDurationProperty)
    {
        return _readWriteDurationProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteDurationPropertyCallback(const std::function<void(std::chrono::duration<double> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
    _readWriteDurationPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteDurationProperty(std::chrono::duration<double> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
        _readWriteDurationProperty = ReadWriteDurationProperty{ value };
        _lastReadWriteDurationPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
        for (const auto& cb: _readWriteDurationPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteDurationProperty();
}

void TestableServer::republishReadWriteDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteDurationProperty)
    {
        doc.SetObject();
        _readWriteDurationProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteDurationPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteDuration/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteDurationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_duration property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_duration payload is not an object or null");
    }

    // TODO: Check _lastReadWriteDurationPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteDurationProperty tempValue = ReadWriteDurationProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
        _readWriteDurationProperty = tempValue;
        _lastReadWriteDurationPropertyVersion++;
    }
    republishReadWriteDurationProperty();
}

boost::optional<std::chrono::duration<double>> TestableServer::getReadWriteOptionalDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    if (_readWriteOptionalDurationProperty)
    {
        return _readWriteOptionalDurationProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteOptionalDurationPropertyCallback(const std::function<void(boost::optional<std::chrono::duration<double>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
    _readWriteOptionalDurationPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalDurationProperty(boost::optional<std::chrono::duration<double>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
        _readWriteOptionalDurationProperty = ReadWriteOptionalDurationProperty{ value };
        _lastReadWriteOptionalDurationPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalDurationPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteOptionalDurationProperty();
}

void TestableServer::republishReadWriteOptionalDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalDurationProperty)
    {
        doc.SetObject();
        _readWriteOptionalDurationProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteOptionalDurationPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteOptionalDuration/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteOptionalDurationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_duration property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_optional_duration payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalDurationPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalDurationProperty tempValue = ReadWriteOptionalDurationProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
        _readWriteOptionalDurationProperty = tempValue;
        _lastReadWriteOptionalDurationPropertyVersion++;
    }
    republishReadWriteOptionalDurationProperty();
}

boost::optional<ReadWriteTwoDurationsProperty> TestableServer::getReadWriteTwoDurationsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
    if (_readWriteTwoDurationsProperty)
    {
        return *_readWriteTwoDurationsProperty;
    }
    return boost::none;
}

void TestableServer::registerReadWriteTwoDurationsPropertyCallback(const std::function<void(std::chrono::duration<double> first, boost::optional<std::chrono::duration<double>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
    _readWriteTwoDurationsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoDurationsProperty(std::chrono::duration<double> first, boost::optional<std::chrono::duration<double>> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
        _readWriteTwoDurationsProperty = ReadWriteTwoDurationsProperty{ first, second };
        _lastReadWriteTwoDurationsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoDurationsPropertyCallbacks)
        {
            cb(first, second);
        }
    }
    republishReadWriteTwoDurationsProperty();
}

void TestableServer::republishReadWriteTwoDurationsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoDurationsProperty)
    {
        doc.SetObject();
        _readWriteTwoDurationsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteTwoDurationsPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteTwoDurations/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteTwoDurationsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_durations property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_two_durations payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoDurationsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoDurationsProperty tempValue = ReadWriteTwoDurationsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
        _readWriteTwoDurationsProperty = tempValue;
        _lastReadWriteTwoDurationsPropertyVersion++;
    }
    republishReadWriteTwoDurationsProperty();
}

boost::optional<std::vector<uint8_t>> TestableServer::getReadWriteBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    if (_readWriteBinaryProperty)
    {
        return _readWriteBinaryProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteBinaryPropertyCallback(const std::function<void(std::vector<uint8_t> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
    _readWriteBinaryPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteBinaryProperty(std::vector<uint8_t> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
        _readWriteBinaryProperty = ReadWriteBinaryProperty{ value };
        _lastReadWriteBinaryPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
        for (const auto& cb: _readWriteBinaryPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteBinaryProperty();
}

void TestableServer::republishReadWriteBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteBinaryProperty)
    {
        doc.SetObject();
        _readWriteBinaryProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteBinaryPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteBinary/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteBinaryPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_binary property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_binary payload is not an object or null");
    }

    // TODO: Check _lastReadWriteBinaryPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteBinaryProperty tempValue = ReadWriteBinaryProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
        _readWriteBinaryProperty = tempValue;
        _lastReadWriteBinaryPropertyVersion++;
    }
    republishReadWriteBinaryProperty();
}

boost::optional<std::vector<uint8_t>> TestableServer::getReadWriteOptionalBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    if (_readWriteOptionalBinaryProperty)
    {
        return _readWriteOptionalBinaryProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteOptionalBinaryPropertyCallback(const std::function<void(boost::optional<std::vector<uint8_t>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
    _readWriteOptionalBinaryPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalBinaryProperty(boost::optional<std::vector<uint8_t>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
        _readWriteOptionalBinaryProperty = ReadWriteOptionalBinaryProperty{ value };
        _lastReadWriteOptionalBinaryPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalBinaryPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteOptionalBinaryProperty();
}

void TestableServer::republishReadWriteOptionalBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalBinaryProperty)
    {
        doc.SetObject();
        _readWriteOptionalBinaryProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteOptionalBinaryPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteOptionalBinary/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteOptionalBinaryPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_optional_binary property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_optional_binary payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalBinaryPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalBinaryProperty tempValue = ReadWriteOptionalBinaryProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
        _readWriteOptionalBinaryProperty = tempValue;
        _lastReadWriteOptionalBinaryPropertyVersion++;
    }
    republishReadWriteOptionalBinaryProperty();
}

boost::optional<ReadWriteTwoBinariesProperty> TestableServer::getReadWriteTwoBinariesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
    if (_readWriteTwoBinariesProperty)
    {
        return *_readWriteTwoBinariesProperty;
    }
    return boost::none;
}

void TestableServer::registerReadWriteTwoBinariesPropertyCallback(const std::function<void(std::vector<uint8_t> first, boost::optional<std::vector<uint8_t>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
    _readWriteTwoBinariesPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoBinariesProperty(std::vector<uint8_t> first, boost::optional<std::vector<uint8_t>> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
        _readWriteTwoBinariesProperty = ReadWriteTwoBinariesProperty{ first, second };
        _lastReadWriteTwoBinariesPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoBinariesPropertyCallbacks)
        {
            cb(first, second);
        }
    }
    republishReadWriteTwoBinariesProperty();
}

void TestableServer::republishReadWriteTwoBinariesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoBinariesProperty)
    {
        doc.SetObject();
        _readWriteTwoBinariesProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteTwoBinariesPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteTwoBinaries/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteTwoBinariesPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_two_binaries property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_two_binaries payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoBinariesPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoBinariesProperty tempValue = ReadWriteTwoBinariesProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
        _readWriteTwoBinariesProperty = tempValue;
        _lastReadWriteTwoBinariesPropertyVersion++;
    }
    republishReadWriteTwoBinariesProperty();
}

boost::optional<std::vector<std::string>> TestableServer::getReadWriteListOfStringsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
    if (_readWriteListOfStringsProperty)
    {
        return _readWriteListOfStringsProperty->value;
    }
    return boost::none;
}

void TestableServer::registerReadWriteListOfStringsPropertyCallback(const std::function<void(std::vector<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyCallbacksMutex);
    _readWriteListOfStringsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteListOfStringsProperty(std::vector<std::string> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
        _readWriteListOfStringsProperty = ReadWriteListOfStringsProperty{ value };
        _lastReadWriteListOfStringsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteListOfStringsPropertyCallbacks)
        {
            cb(value);
        }
    }
    republishReadWriteListOfStringsProperty();
}

void TestableServer::republishReadWriteListOfStringsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteListOfStringsProperty)
    {
        doc.SetObject();
        _readWriteListOfStringsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteListOfStringsPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteListOfStrings/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteListOfStringsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_list_of_strings property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_list_of_strings payload is not an object or null");
    }

    // TODO: Check _lastReadWriteListOfStringsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteListOfStringsProperty tempValue = ReadWriteListOfStringsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
        _readWriteListOfStringsProperty = tempValue;
        _lastReadWriteListOfStringsPropertyVersion++;
    }
    republishReadWriteListOfStringsProperty();
}

boost::optional<ReadWriteListsProperty> TestableServer::getReadWriteListsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
    if (_readWriteListsProperty)
    {
        return *_readWriteListsProperty;
    }
    return boost::none;
}

void TestableServer::registerReadWriteListsPropertyCallback(const std::function<void(std::vector<Numbers> theList, boost::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyCallbacksMutex);
    _readWriteListsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteListsProperty(std::vector<Numbers> theList, boost::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
        _readWriteListsProperty = ReadWriteListsProperty{ theList, optionalList };
        _lastReadWriteListsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteListsPropertyCallbacks)
        {
            cb(theList, optionalList);
        }
    }
    republishReadWriteListsProperty();
}

void TestableServer::republishReadWriteListsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteListsProperty)
    {
        doc.SetObject();
        _readWriteListsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastReadWriteListsPropertyVersion;
    _broker->Publish((boost::format("testable/%1%/property/readWriteLists/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestableServer::_receiveReadWriteListsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse read_write_lists property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received read_write_lists payload is not an object or null");
    }

    // TODO: Check _lastReadWriteListsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteListsProperty tempValue = ReadWriteListsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
        _readWriteListsProperty = tempValue;
        _lastReadWriteListsPropertyVersion++;
    }
    republishReadWriteListsProperty();
}

void TestableServer::_advertisementThreadLoop()
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

        doc.AddMember("interface_name", rapidjson::Value("testable", allocator), allocator);
        doc.AddMember("instance", rapidjson::Value(_instanceId.c_str(), allocator), allocator);
        doc.AddMember("title", rapidjson::Value("Interface for testing", allocator), allocator);
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

        // Publish to testable/<instance_id>/interface
        std::string topic = (boost::format("testable/%1%/interface") % _instanceId).str();
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
