

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
#include "enums.hpp"
#include "ibrokerconnection.hpp"

constexpr const char TestAbleServer::NAME[];
constexpr const char TestAbleServer::INTERFACE_VERSION[];

TestAbleServer::TestAbleServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId):
    _broker(broker), _instanceId(instanceId), _advertisementThreadRunning(false)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _receiveMessage(topic, payload, mqttProps);
                                                               });

    _callWithNothingMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callWithNothing") % _instanceId).str(), 2);
    _callOneIntegerMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOneInteger") % _instanceId).str(), 2);
    _callOptionalIntegerMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOptionalInteger") % _instanceId).str(), 2);
    _callThreeIntegersMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callThreeIntegers") % _instanceId).str(), 2);
    _callOneStringMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOneString") % _instanceId).str(), 2);
    _callOptionalStringMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOptionalString") % _instanceId).str(), 2);
    _callThreeStringsMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callThreeStrings") % _instanceId).str(), 2);
    _callOneEnumMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOneEnum") % _instanceId).str(), 2);
    _callOptionalEnumMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOptionalEnum") % _instanceId).str(), 2);
    _callThreeEnumsMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callThreeEnums") % _instanceId).str(), 2);
    _callOneStructMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOneStruct") % _instanceId).str(), 2);
    _callOptionalStructMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOptionalStruct") % _instanceId).str(), 2);
    _callThreeStructsMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callThreeStructs") % _instanceId).str(), 2);
    _callOneDateTimeMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOneDateTime") % _instanceId).str(), 2);
    _callOptionalDateTimeMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOptionalDateTime") % _instanceId).str(), 2);
    _callThreeDateTimesMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callThreeDateTimes") % _instanceId).str(), 2);
    _callOneDurationMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOneDuration") % _instanceId).str(), 2);
    _callOptionalDurationMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOptionalDuration") % _instanceId).str(), 2);
    _callThreeDurationsMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callThreeDurations") % _instanceId).str(), 2);
    _callOneBinaryMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOneBinary") % _instanceId).str(), 2);
    _callOptionalBinaryMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callOptionalBinary") % _instanceId).str(), 2);
    _callThreeBinariesMethodSubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/method/callThreeBinaries") % _instanceId).str(), 2);

    _readWriteIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteInteger/setValue") % _instanceId).str(), 1);
    _readOnlyIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readOnlyInteger/setValue") % _instanceId).str(), 1);
    _readWriteOptionalIntegerPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalInteger/setValue") % _instanceId).str(), 1);
    _readWriteTwoIntegersPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoIntegers/setValue") % _instanceId).str(), 1);
    _readOnlyStringPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readOnlyString/setValue") % _instanceId).str(), 1);
    _readWriteStringPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteString/setValue") % _instanceId).str(), 1);
    _readWriteOptionalStringPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalString/setValue") % _instanceId).str(), 1);
    _readWriteTwoStringsPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoStrings/setValue") % _instanceId).str(), 1);
    _readWriteStructPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteStruct/setValue") % _instanceId).str(), 1);
    _readWriteOptionalStructPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalStruct/setValue") % _instanceId).str(), 1);
    _readWriteTwoStructsPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoStructs/setValue") % _instanceId).str(), 1);
    _readOnlyEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readOnlyEnum/setValue") % _instanceId).str(), 1);
    _readWriteEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteEnum/setValue") % _instanceId).str(), 1);
    _readWriteOptionalEnumPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalEnum/setValue") % _instanceId).str(), 1);
    _readWriteTwoEnumsPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoEnums/setValue") % _instanceId).str(), 1);
    _readWriteDatetimePropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteDatetime/setValue") % _instanceId).str(), 1);
    _readWriteOptionalDatetimePropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalDatetime/setValue") % _instanceId).str(), 1);
    _readWriteTwoDatetimesPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoDatetimes/setValue") % _instanceId).str(), 1);
    _readWriteDurationPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteDuration/setValue") % _instanceId).str(), 1);
    _readWriteOptionalDurationPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalDuration/setValue") % _instanceId).str(), 1);
    _readWriteTwoDurationsPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoDurations/setValue") % _instanceId).str(), 1);
    _readWriteBinaryPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteBinary/setValue") % _instanceId).str(), 1);
    _readWriteOptionalBinaryPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteOptionalBinary/setValue") % _instanceId).str(), 1);
    _readWriteTwoBinariesPropertySubscriptionId = _broker->Subscribe((boost::format("testAble/%1%/property/readWriteTwoBinaries/setValue") % _instanceId).str(), 1);

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&TestAbleServer::_advertisementThreadLoop, this);
}

TestAbleServer::~TestAbleServer()
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

    std::string topic = (boost::format("testAble/%1%/interface") % _instanceId).str();
    _broker->Publish(topic, "", 1, true, MqttProperties());

    _broker->Unsubscribe((boost::format("testAble/%1%/method/callWithNothing") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOneInteger") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOptionalInteger") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callThreeIntegers") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOneString") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOptionalString") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callThreeStrings") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOneEnum") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOptionalEnum") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callThreeEnums") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOneStruct") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOptionalStruct") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callThreeStructs") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOneDateTime") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOptionalDateTime") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callThreeDateTimes") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOneDuration") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOptionalDuration") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callThreeDurations") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOneBinary") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callOptionalBinary") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/method/callThreeBinaries") % _instanceId).str());

    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteInteger/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readOnlyInteger/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteOptionalInteger/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteTwoIntegers/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readOnlyString/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteString/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteOptionalString/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteTwoStrings/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteStruct/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteOptionalStruct/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteTwoStructs/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readOnlyEnum/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteEnum/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteOptionalEnum/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteTwoEnums/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteDatetime/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteOptionalDatetime/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteTwoDatetimes/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteDuration/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteOptionalDuration/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteTwoDurations/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteBinary/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteOptionalBinary/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("testAble/%1%/property/readWriteTwoBinaries/setValue") % _instanceId).str());
}

void TestAbleServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);

    if ((subscriptionId == _callWithNothingMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callWithNothing") % _instanceId).str())))
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

    else if ((subscriptionId == _callOneIntegerMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOneInteger") % _instanceId).str())))
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

    else if ((subscriptionId == _callOptionalIntegerMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOptionalInteger") % _instanceId).str())))
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

    else if ((subscriptionId == _callThreeIntegersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callThreeIntegers") % _instanceId).str())))
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

    else if ((subscriptionId == _callOneStringMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOneString") % _instanceId).str())))
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

    else if ((subscriptionId == _callOptionalStringMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOptionalString") % _instanceId).str())))
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

    else if ((subscriptionId == _callThreeStringsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callThreeStrings") % _instanceId).str())))
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

    else if ((subscriptionId == _callOneEnumMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOneEnum") % _instanceId).str())))
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

    else if ((subscriptionId == _callOptionalEnumMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOptionalEnum") % _instanceId).str())))
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

    else if ((subscriptionId == _callThreeEnumsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callThreeEnums") % _instanceId).str())))
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

    else if ((subscriptionId == _callOneStructMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOneStruct") % _instanceId).str())))
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

    else if ((subscriptionId == _callOptionalStructMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOptionalStruct") % _instanceId).str())))
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

    else if ((subscriptionId == _callThreeStructsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callThreeStructs") % _instanceId).str())))
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

    else if ((subscriptionId == _callOneDateTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOneDateTime") % _instanceId).str())))
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

    else if ((subscriptionId == _callOptionalDateTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOptionalDateTime") % _instanceId).str())))
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

    else if ((subscriptionId == _callThreeDateTimesMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callThreeDateTimes") % _instanceId).str())))
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

    else if ((subscriptionId == _callOneDurationMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOneDuration") % _instanceId).str())))
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

    else if ((subscriptionId == _callOptionalDurationMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOptionalDuration") % _instanceId).str())))
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

    else if ((subscriptionId == _callThreeDurationsMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callThreeDurations") % _instanceId).str())))
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

    else if ((subscriptionId == _callOneBinaryMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOneBinary") % _instanceId).str())))
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

    else if ((subscriptionId == _callOptionalBinaryMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callOptionalBinary") % _instanceId).str())))
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

    else if ((subscriptionId == _callThreeBinariesMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/method/callThreeBinaries") % _instanceId).str())))
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

    if (subscriptionId == _readWriteIntegerPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteInteger/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_integer property update.", topic.c_str());
        _receiveReadWriteIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readOnlyIntegerPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readOnlyInteger/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_integer property update.", topic.c_str());
        _receiveReadOnlyIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalIntegerPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteOptionalInteger/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_integer property update.", topic.c_str());
        _receiveReadWriteOptionalIntegerPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoIntegersPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteTwoIntegers/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_integers property update.", topic.c_str());
        _receiveReadWriteTwoIntegersPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readOnlyStringPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readOnlyString/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_string property update.", topic.c_str());
        _receiveReadOnlyStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteStringPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteString/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_string property update.", topic.c_str());
        _receiveReadWriteStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalStringPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteOptionalString/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_string property update.", topic.c_str());
        _receiveReadWriteOptionalStringPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoStringsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteTwoStrings/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_strings property update.", topic.c_str());
        _receiveReadWriteTwoStringsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteStructPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteStruct/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_struct property update.", topic.c_str());
        _receiveReadWriteStructPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalStructPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteOptionalStruct/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_struct property update.", topic.c_str());
        _receiveReadWriteOptionalStructPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoStructsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteTwoStructs/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_structs property update.", topic.c_str());
        _receiveReadWriteTwoStructsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readOnlyEnumPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readOnlyEnum/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_enum property update.", topic.c_str());
        _receiveReadOnlyEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteEnumPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteEnum/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_enum property update.", topic.c_str());
        _receiveReadWriteEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalEnumPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteOptionalEnum/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_enum property update.", topic.c_str());
        _receiveReadWriteOptionalEnumPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoEnumsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteTwoEnums/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_enums property update.", topic.c_str());
        _receiveReadWriteTwoEnumsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteDatetimePropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteDatetime/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_datetime property update.", topic.c_str());
        _receiveReadWriteDatetimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalDatetimePropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteOptionalDatetime/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_datetime property update.", topic.c_str());
        _receiveReadWriteOptionalDatetimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoDatetimesPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteTwoDatetimes/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_datetimes property update.", topic.c_str());
        _receiveReadWriteTwoDatetimesPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteDurationPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteDuration/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_duration property update.", topic.c_str());
        _receiveReadWriteDurationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalDurationPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteOptionalDuration/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_duration property update.", topic.c_str());
        _receiveReadWriteOptionalDurationPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoDurationsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteTwoDurations/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_durations property update.", topic.c_str());
        _receiveReadWriteTwoDurationsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteBinaryPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteBinary/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_binary property update.", topic.c_str());
        _receiveReadWriteBinaryPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteOptionalBinaryPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteOptionalBinary/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_binary property update.", topic.c_str());
        _receiveReadWriteOptionalBinaryPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _readWriteTwoBinariesPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("testAble/%1%/property/readWriteTwoBinaries/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_binaries property update.", topic.c_str());
        _receiveReadWriteTwoBinariesPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

boost::future<bool> TestAbleServer::emitEmptySignal()
{
    rapidjson::Document doc;
    doc.SetObject();
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/empty") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleIntSignal(int value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/singleInt") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleOptionalIntSignal(boost::optional<int> value)
{
    rapidjson::Document doc;
    doc.SetObject();
    if (value)
        doc.AddMember("value", *value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/singleOptionalInt") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitThreeIntegersSignal(int first, int second, boost::optional<int> third)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/threeIntegers") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleStringSignal(const std::string& value)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/singleString") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleOptionalStringSignal(boost::optional<std::string> value)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/singleOptionalString") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitThreeStringsSignal(const std::string& first, const std::string& second, boost::optional<std::string> third)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/threeStrings") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleEnumSignal(Numbers value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/singleEnum") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleOptionalEnumSignal(boost::optional<Numbers> value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(*value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/singleOptionalEnum") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitThreeEnumsSignal(Numbers first, Numbers second, boost::optional<Numbers> third)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/threeEnums") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleStructSignal(AllTypes value)
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/singleStruct") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleOptionalStructSignal(AllTypes value)
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/singleOptionalStruct") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitThreeStructsSignal(AllTypes first, AllTypes second, AllTypes third)
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/threeStructs") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleDateTimeSignal(std::chrono::time_point<std::chrono::system_clock> value)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/singleDateTime") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleOptionalDatetimeSignal(boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/singleOptionalDatetime") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitThreeDateTimesSignal(std::chrono::time_point<std::chrono::system_clock> first, std::chrono::time_point<std::chrono::system_clock> second, boost::optional<std::chrono::time_point<std::chrono::system_clock>> third)
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
        std::string secondIsoString = timePointToIsoString(second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempThirdStringValue;
        std::string thirdIsoString = timePointToIsoString(*third);
        tempThirdStringValue.SetString(thirdIsoString.c_str(), thirdIsoString.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/threeDateTimes") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleDurationSignal(std::chrono::duration<double> value)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/singleDuration") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleOptionalDurationSignal(boost::optional<std::chrono::duration<double>> value)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/singleOptionalDuration") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitThreeDurationsSignal(std::chrono::duration<double> first, std::chrono::duration<double> second, boost::optional<std::chrono::duration<double>> third)
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
        std::string secondIsoString = durationToIsoString(second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempThirdStringValue;
        std::string thirdIsoString = durationToIsoString(*third);
        tempThirdStringValue.SetString(thirdIsoString.c_str(), thirdIsoString.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/threeDurations") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleBinarySignal(std::vector<uint8_t> value)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/singleBinary") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitSingleOptionalBinarySignal(boost::optional<std::vector<uint8_t>> value)
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
    return _broker->Publish((boost::format("testAble/%1%/signal/singleOptionalBinary") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> TestAbleServer::emitThreeBinariesSignal(std::vector<uint8_t> first, std::vector<uint8_t> second, boost::optional<std::vector<uint8_t>> third)
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
        std::string secondB64String = base64Encode(second);
        tempSecondStringValue.SetString(secondB64String.c_str(), secondB64String.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempThirdStringValue;
        std::string thirdB64String = base64Encode(*third);
        tempThirdStringValue.SetString(thirdB64String.c_str(), thirdB64String.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("testAble/%1%/signal/threeBinaries") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::registerCallWithNothingHandler(std::function<void()> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callWithNothing method requests.");
    _callWithNothingHandler = func;
}

void TestAbleServer::registerCallOneIntegerHandler(std::function<int(int)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOneInteger method requests.");
    _callOneIntegerHandler = func;
}

void TestAbleServer::registerCallOptionalIntegerHandler(std::function<boost::optional<int>(boost::optional<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOptionalInteger method requests.");
    _callOptionalIntegerHandler = func;
}

void TestAbleServer::registerCallThreeIntegersHandler(std::function<CallThreeIntegersReturnValue(int, int, boost::optional<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callThreeIntegers method requests.");
    _callThreeIntegersHandler = func;
}

void TestAbleServer::registerCallOneStringHandler(std::function<std::string(std::string)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOneString method requests.");
    _callOneStringHandler = func;
}

void TestAbleServer::registerCallOptionalStringHandler(std::function<boost::optional<std::string>(boost::optional<std::string>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOptionalString method requests.");
    _callOptionalStringHandler = func;
}

void TestAbleServer::registerCallThreeStringsHandler(std::function<CallThreeStringsReturnValue(std::string, std::string, boost::optional<std::string>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callThreeStrings method requests.");
    _callThreeStringsHandler = func;
}

void TestAbleServer::registerCallOneEnumHandler(std::function<Numbers(Numbers)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOneEnum method requests.");
    _callOneEnumHandler = func;
}

void TestAbleServer::registerCallOptionalEnumHandler(std::function<boost::optional<Numbers>(boost::optional<Numbers>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOptionalEnum method requests.");
    _callOptionalEnumHandler = func;
}

void TestAbleServer::registerCallThreeEnumsHandler(std::function<CallThreeEnumsReturnValue(Numbers, Numbers, boost::optional<Numbers>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callThreeEnums method requests.");
    _callThreeEnumsHandler = func;
}

void TestAbleServer::registerCallOneStructHandler(std::function<AllTypes(AllTypes)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOneStruct method requests.");
    _callOneStructHandler = func;
}

void TestAbleServer::registerCallOptionalStructHandler(std::function<boost::optional<AllTypes>(boost::optional<AllTypes>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOptionalStruct method requests.");
    _callOptionalStructHandler = func;
}

void TestAbleServer::registerCallThreeStructsHandler(std::function<CallThreeStructsReturnValue(AllTypes, AllTypes, boost::optional<AllTypes>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callThreeStructs method requests.");
    _callThreeStructsHandler = func;
}

void TestAbleServer::registerCallOneDateTimeHandler(std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::time_point<std::chrono::system_clock>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOneDateTime method requests.");
    _callOneDateTimeHandler = func;
}

void TestAbleServer::registerCallOptionalDateTimeHandler(std::function<boost::optional<std::chrono::time_point<std::chrono::system_clock>>(boost::optional<std::chrono::time_point<std::chrono::system_clock>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOptionalDateTime method requests.");
    _callOptionalDateTimeHandler = func;
}

void TestAbleServer::registerCallThreeDateTimesHandler(std::function<CallThreeDateTimesReturnValue(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callThreeDateTimes method requests.");
    _callThreeDateTimesHandler = func;
}

void TestAbleServer::registerCallOneDurationHandler(std::function<std::chrono::duration<double>(std::chrono::duration<double>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOneDuration method requests.");
    _callOneDurationHandler = func;
}

void TestAbleServer::registerCallOptionalDurationHandler(std::function<boost::optional<std::chrono::duration<double>>(boost::optional<std::chrono::duration<double>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOptionalDuration method requests.");
    _callOptionalDurationHandler = func;
}

void TestAbleServer::registerCallThreeDurationsHandler(std::function<CallThreeDurationsReturnValue(std::chrono::duration<double>, std::chrono::duration<double>, boost::optional<std::chrono::duration<double>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callThreeDurations method requests.");
    _callThreeDurationsHandler = func;
}

void TestAbleServer::registerCallOneBinaryHandler(std::function<std::vector<uint8_t>(std::vector<uint8_t>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOneBinary method requests.");
    _callOneBinaryHandler = func;
}

void TestAbleServer::registerCallOptionalBinaryHandler(std::function<boost::optional<std::vector<uint8_t>>(boost::optional<std::vector<uint8_t>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callOptionalBinary method requests.");
    _callOptionalBinaryHandler = func;
}

void TestAbleServer::registerCallThreeBinariesHandler(std::function<CallThreeBinariesReturnValue(std::vector<uint8_t>, std::vector<uint8_t>, boost::optional<std::vector<uint8_t>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle testAble/+/method/callThreeBinaries method requests.");
    _callThreeBinariesHandler = func;
}

void TestAbleServer::_callCallWithNothingHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callWithNothing");
    if (_callWithNothingHandler)
    {
        // No Return Value.
        _callWithNothingHandler();

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOneIntegerHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneInteger");
    if (_callOneIntegerHandler)
    {
        int tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                tempInput1 = itr->value.GetInt();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        int ret = _callOneIntegerHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            returnValueOutput1.SetInt(ret); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOptionalIntegerHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalInteger");
    if (_callOptionalIntegerHandler)
    {
        boost::optional<int> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                tempInput1 = itr->value.GetInt();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        boost::optional<int> ret = _callOptionalIntegerHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            returnValueOutput1.SetInt(*ret); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallThreeIntegersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeIntegers");
    if (_callThreeIntegersHandler)
    {
        int tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                tempInput1 = itr->value.GetInt();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        int tempInput2;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input2");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                tempInput2 = itr->value.GetInt();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        boost::optional<int> tempInput3;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input3");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                tempInput3 = itr->value.GetInt();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value has multiple values.
        CallThreeIntegersReturnValue ret = _callThreeIntegersHandler(tempInput1, tempInput2, tempInput3);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret.output1' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            returnValueOutput1.SetInt(ret.output1); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            // add the 'ret.output2' value to the json as 'output2'.
            rapidjson::Value returnValueOutput2;
            returnValueOutput2.SetInt(ret.output2); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("output2", returnValueOutput2, responseJson.GetAllocator());

            // add the 'ret.output3' value to the json as 'output3'.
            rapidjson::Value returnValueOutput3;
            returnValueOutput3.SetInt(*ret.output3); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("output3", returnValueOutput3, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOneStringHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneString");
    if (_callOneStringHandler)
    {
        std::string tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
                tempInput1 = itr->value.GetString();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        std::string ret = _callOneStringHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            returnValueOutput1.SetString(ret.c_str(), ret.size(), responseJson.GetAllocator());
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOptionalStringHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalString");
    if (_callOptionalStringHandler)
    {
        boost::optional<std::string> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
                tempInput1 = itr->value.GetString();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        boost::optional<std::string> ret = _callOptionalStringHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            returnValueOutput1.SetString(ret->c_str(), ret->size(), responseJson.GetAllocator());
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallThreeStringsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeStrings");
    if (_callThreeStringsHandler)
    {
        std::string tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
                tempInput1 = itr->value.GetString();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::string tempInput2;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input2");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
                tempInput2 = itr->value.GetString();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        boost::optional<std::string> tempInput3;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input3");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
                tempInput3 = itr->value.GetString();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value has multiple values.
        CallThreeStringsReturnValue ret = _callThreeStringsHandler(tempInput1, tempInput2, tempInput3);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret.output1' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            returnValueOutput1.SetString(ret.output1.c_str(), ret.output1.size(), responseJson.GetAllocator());
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            // add the 'ret.output2' value to the json as 'output2'.
            rapidjson::Value returnValueOutput2;
            returnValueOutput2.SetString(ret.output2.c_str(), ret.output2.size(), responseJson.GetAllocator());
            responseJson.AddMember("output2", returnValueOutput2, responseJson.GetAllocator());

            // add the 'ret.output3' value to the json as 'output3'.
            rapidjson::Value returnValueOutput3;
            returnValueOutput3.SetString(ret.output3->c_str(), ret.output3->size(), responseJson.GetAllocator());
            responseJson.AddMember("output3", returnValueOutput3, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOneEnumHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneEnum");
    if (_callOneEnumHandler)
    {
        Numbers tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                // Convert the json integer into the enum type.
                tempInput1 = static_cast<Numbers>(itr->value.GetInt());
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        Numbers ret = _callOneEnumHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;

            returnValueOutput1.SetInt(static_cast<int>(ret));

            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOptionalEnumHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalEnum");
    if (_callOptionalEnumHandler)
    {
        boost::optional<Numbers> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                // Convert the json integer into the enum type.
                tempInput1 = static_cast<Numbers>(itr->value.GetInt());
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        boost::optional<Numbers> ret = _callOptionalEnumHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;

            if (ret)
            {
                returnValueOutput1.SetInt(static_cast<int>(*ret));
            }
            else
            {
                returnValueOutput1.SetNull();
            }

            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallThreeEnumsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeEnums");
    if (_callThreeEnumsHandler)
    {
        Numbers tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                // Convert the json integer into the enum type.
                tempInput1 = static_cast<Numbers>(itr->value.GetInt());
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        Numbers tempInput2;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input2");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                // Convert the json integer into the enum type.
                tempInput2 = static_cast<Numbers>(itr->value.GetInt());
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        boost::optional<Numbers> tempInput3;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input3");
            if (itr != doc.MemberEnd() && itr->value.IsInt())
            {
                // Convert the json integer into the enum type.
                tempInput3 = static_cast<Numbers>(itr->value.GetInt());
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value has multiple values.
        CallThreeEnumsReturnValue ret = _callThreeEnumsHandler(tempInput1, tempInput2, tempInput3);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret.output1' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;

            returnValueOutput1.SetInt(static_cast<int>(ret.output1));

            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            // add the 'ret.output2' value to the json as 'output2'.
            rapidjson::Value returnValueOutput2;

            returnValueOutput2.SetInt(static_cast<int>(ret.output2));

            responseJson.AddMember("output2", returnValueOutput2, responseJson.GetAllocator());

            // add the 'ret.output3' value to the json as 'output3'.
            rapidjson::Value returnValueOutput3;

            if (ret.output3)
            {
                returnValueOutput3.SetInt(static_cast<int>(*ret.output3));
            }
            else
            {
                returnValueOutput3.SetNull();
            }

            responseJson.AddMember("output3", returnValueOutput3, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOneStructHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneStruct");
    if (_callOneStructHandler)
    {
        AllTypes tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsObject())
            {
                // Convert the json object into the struct type.
                if (itr->value.IsObject())
                {
                    tempInput1 = AllTypes::FromRapidJsonObject(itr->value);
                }
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        AllTypes ret = _callOneStructHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret.bool_' value to the json as 'bool_'.
            rapidjson::Value returnValueBool;
            returnValueBool.SetBool(ret.bool_); // Rapid Json type for ArgType.PRIMITIVE is Bool
            responseJson.AddMember("bool_", returnValueBool, responseJson.GetAllocator());

            // add the 'ret.int_' value to the json as 'int_'.
            rapidjson::Value returnValueInt;
            returnValueInt.SetInt(ret.int_); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("int_", returnValueInt, responseJson.GetAllocator());

            // add the 'ret.number' value to the json as 'number'.
            rapidjson::Value returnValueNumber;
            returnValueNumber.SetDouble(ret.number); // Rapid Json type for ArgType.PRIMITIVE is Double
            responseJson.AddMember("number", returnValueNumber, responseJson.GetAllocator());

            // add the 'ret.str' value to the json as 'str'.
            rapidjson::Value returnValueStr;
            returnValueStr.SetString(ret.str.c_str(), ret.str.size(), responseJson.GetAllocator());
            responseJson.AddMember("str", returnValueStr, responseJson.GetAllocator());

            // add the 'ret.enum_' value to the json as 'enum_'.
            rapidjson::Value returnValueEnum;

            returnValueEnum.SetInt(static_cast<int>(ret.enum_));

            responseJson.AddMember("enum_", returnValueEnum, responseJson.GetAllocator());

            // add the 'ret.date_and_time' value to the json as 'date_and_time'.
            rapidjson::Value returnValueDateAndTime;
            responseJson.AddMember("date_and_time", returnValueDateAndTime, responseJson.GetAllocator());

            // add the 'ret.time_duration' value to the json as 'time_duration'.
            rapidjson::Value returnValueTimeDuration;
            responseJson.AddMember("time_duration", returnValueTimeDuration, responseJson.GetAllocator());

            // add the 'ret.data' value to the json as 'data'.
            rapidjson::Value returnValueData;
            responseJson.AddMember("data", returnValueData, responseJson.GetAllocator());

            // add the 'ret.OptionalInteger' value to the json as 'OptionalInteger'.
            rapidjson::Value returnValueOptionalInteger;
            returnValueOptionalInteger.SetInt(*ret.OptionalInteger); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("OptionalInteger", returnValueOptionalInteger, responseJson.GetAllocator());

            // add the 'ret.OptionalString' value to the json as 'OptionalString'.
            rapidjson::Value returnValueOptionalString;
            returnValueOptionalString.SetString(ret.OptionalString->c_str(), ret.OptionalString->size(), responseJson.GetAllocator());
            responseJson.AddMember("OptionalString", returnValueOptionalString, responseJson.GetAllocator());

            // add the 'ret.OptionalEnum' value to the json as 'OptionalEnum'.
            rapidjson::Value returnValueOptionalEnum;

            if (ret.OptionalEnum)
            {
                returnValueOptionalEnum.SetInt(static_cast<int>(*ret.OptionalEnum));
            }
            else
            {
                returnValueOptionalEnum.SetNull();
            }

            responseJson.AddMember("OptionalEnum", returnValueOptionalEnum, responseJson.GetAllocator());

            // add the 'ret.OptionalDateTime' value to the json as 'OptionalDateTime'.
            rapidjson::Value returnValueOptionalDateTime;
            responseJson.AddMember("OptionalDateTime", returnValueOptionalDateTime, responseJson.GetAllocator());

            // add the 'ret.OptionalDuration' value to the json as 'OptionalDuration'.
            rapidjson::Value returnValueOptionalDuration;
            responseJson.AddMember("OptionalDuration", returnValueOptionalDuration, responseJson.GetAllocator());

            // add the 'ret.OptionalBinary' value to the json as 'OptionalBinary'.
            rapidjson::Value returnValueOptionalBinary;
            responseJson.AddMember("OptionalBinary", returnValueOptionalBinary, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOptionalStructHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalStruct");
    if (_callOptionalStructHandler)
    {
        boost::optional<AllTypes> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsObject())
            {
                // Convert the json object into the struct type.
                if (itr->value.IsObject())
                {
                    tempInput1 = AllTypes::FromRapidJsonObject(itr->value);
                }
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        boost::optional<AllTypes> ret = _callOptionalStructHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret->bool_' value to the json as 'bool_'.
            rapidjson::Value returnValueBool;
            returnValueBool.SetBool(ret->bool_); // Rapid Json type for ArgType.PRIMITIVE is Bool
            responseJson.AddMember("bool_", returnValueBool, responseJson.GetAllocator());

            // add the 'ret->int_' value to the json as 'int_'.
            rapidjson::Value returnValueInt;
            returnValueInt.SetInt(ret->int_); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("int_", returnValueInt, responseJson.GetAllocator());

            // add the 'ret->number' value to the json as 'number'.
            rapidjson::Value returnValueNumber;
            returnValueNumber.SetDouble(ret->number); // Rapid Json type for ArgType.PRIMITIVE is Double
            responseJson.AddMember("number", returnValueNumber, responseJson.GetAllocator());

            // add the 'ret->str' value to the json as 'str'.
            rapidjson::Value returnValueStr;
            returnValueStr.SetString(ret->str.c_str(), ret->str.size(), responseJson.GetAllocator());
            responseJson.AddMember("str", returnValueStr, responseJson.GetAllocator());

            // add the 'ret->enum_' value to the json as 'enum_'.
            rapidjson::Value returnValueEnum;

            returnValueEnum.SetInt(static_cast<int>(ret->enum_));

            responseJson.AddMember("enum_", returnValueEnum, responseJson.GetAllocator());

            // add the 'ret->date_and_time' value to the json as 'date_and_time'.
            rapidjson::Value returnValueDateAndTime;
            responseJson.AddMember("date_and_time", returnValueDateAndTime, responseJson.GetAllocator());

            // add the 'ret->time_duration' value to the json as 'time_duration'.
            rapidjson::Value returnValueTimeDuration;
            responseJson.AddMember("time_duration", returnValueTimeDuration, responseJson.GetAllocator());

            // add the 'ret->data' value to the json as 'data'.
            rapidjson::Value returnValueData;
            responseJson.AddMember("data", returnValueData, responseJson.GetAllocator());

            // add the 'ret->OptionalInteger' value to the json as 'OptionalInteger'.
            rapidjson::Value returnValueOptionalInteger;
            returnValueOptionalInteger.SetInt(*ret->OptionalInteger); // Rapid Json type for ArgType.PRIMITIVE is Int
            responseJson.AddMember("OptionalInteger", returnValueOptionalInteger, responseJson.GetAllocator());

            // add the 'ret->OptionalString' value to the json as 'OptionalString'.
            rapidjson::Value returnValueOptionalString;
            returnValueOptionalString.SetString(ret->OptionalString->c_str(), ret->OptionalString->size(), responseJson.GetAllocator());
            responseJson.AddMember("OptionalString", returnValueOptionalString, responseJson.GetAllocator());

            // add the 'ret->OptionalEnum' value to the json as 'OptionalEnum'.
            rapidjson::Value returnValueOptionalEnum;

            if (ret->OptionalEnum)
            {
                returnValueOptionalEnum.SetInt(static_cast<int>(*ret->OptionalEnum));
            }
            else
            {
                returnValueOptionalEnum.SetNull();
            }

            responseJson.AddMember("OptionalEnum", returnValueOptionalEnum, responseJson.GetAllocator());

            // add the 'ret->OptionalDateTime' value to the json as 'OptionalDateTime'.
            rapidjson::Value returnValueOptionalDateTime;
            responseJson.AddMember("OptionalDateTime", returnValueOptionalDateTime, responseJson.GetAllocator());

            // add the 'ret->OptionalDuration' value to the json as 'OptionalDuration'.
            rapidjson::Value returnValueOptionalDuration;
            responseJson.AddMember("OptionalDuration", returnValueOptionalDuration, responseJson.GetAllocator());

            // add the 'ret->OptionalBinary' value to the json as 'OptionalBinary'.
            rapidjson::Value returnValueOptionalBinary;
            responseJson.AddMember("OptionalBinary", returnValueOptionalBinary, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallThreeStructsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeStructs");
    if (_callThreeStructsHandler)
    {
        AllTypes tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsObject())
            {
                // Convert the json object into the struct type.
                if (itr->value.IsObject())
                {
                    tempInput1 = AllTypes::FromRapidJsonObject(itr->value);
                }
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        AllTypes tempInput2;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input2");
            if (itr != doc.MemberEnd() && itr->value.IsObject())
            {
                // Convert the json object into the struct type.
                if (itr->value.IsObject())
                {
                    tempInput2 = AllTypes::FromRapidJsonObject(itr->value);
                }
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        boost::optional<AllTypes> tempInput3;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input3");
            if (itr != doc.MemberEnd() && itr->value.IsObject())
            {
                // Convert the json object into the struct type.
                if (itr->value.IsObject())
                {
                    tempInput3 = AllTypes::FromRapidJsonObject(itr->value);
                }
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value has multiple values.
        CallThreeStructsReturnValue ret = _callThreeStructsHandler(tempInput1, tempInput2, tempInput3);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret.output1' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            // add the 'ret.output2' value to the json as 'output2'.
            rapidjson::Value returnValueOutput2;
            responseJson.AddMember("output2", returnValueOutput2, responseJson.GetAllocator());

            // add the 'ret.output3' value to the json as 'output3'.
            rapidjson::Value returnValueOutput3;
            responseJson.AddMember("output3", returnValueOutput3, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOneDateTimeHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneDateTime");
    if (_callOneDateTimeHandler)
    {
        std::chrono::time_point<std::chrono::system_clock> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        std::chrono::time_point<std::chrono::system_clock> ret = _callOneDateTimeHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOptionalDateTimeHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalDateTime");
    if (_callOptionalDateTimeHandler)
    {
        boost::optional<std::chrono::time_point<std::chrono::system_clock>> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        boost::optional<std::chrono::time_point<std::chrono::system_clock>> ret = _callOptionalDateTimeHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallThreeDateTimesHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeDateTimes");
    if (_callThreeDateTimesHandler)
    {
        std::chrono::time_point<std::chrono::system_clock> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::chrono::time_point<std::chrono::system_clock> tempInput2;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input2");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        boost::optional<std::chrono::time_point<std::chrono::system_clock>> tempInput3;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input3");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value has multiple values.
        CallThreeDateTimesReturnValue ret = _callThreeDateTimesHandler(tempInput1, tempInput2, tempInput3);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret.output1' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            // add the 'ret.output2' value to the json as 'output2'.
            rapidjson::Value returnValueOutput2;
            responseJson.AddMember("output2", returnValueOutput2, responseJson.GetAllocator());

            // add the 'ret.output3' value to the json as 'output3'.
            rapidjson::Value returnValueOutput3;
            responseJson.AddMember("output3", returnValueOutput3, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOneDurationHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneDuration");
    if (_callOneDurationHandler)
    {
        std::chrono::duration<double> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        std::chrono::duration<double> ret = _callOneDurationHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOptionalDurationHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalDuration");
    if (_callOptionalDurationHandler)
    {
        boost::optional<std::chrono::duration<double>> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        boost::optional<std::chrono::duration<double>> ret = _callOptionalDurationHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallThreeDurationsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeDurations");
    if (_callThreeDurationsHandler)
    {
        std::chrono::duration<double> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::chrono::duration<double> tempInput2;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input2");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        boost::optional<std::chrono::duration<double>> tempInput3;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input3");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value has multiple values.
        CallThreeDurationsReturnValue ret = _callThreeDurationsHandler(tempInput1, tempInput2, tempInput3);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret.output1' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            // add the 'ret.output2' value to the json as 'output2'.
            rapidjson::Value returnValueOutput2;
            responseJson.AddMember("output2", returnValueOutput2, responseJson.GetAllocator());

            // add the 'ret.output3' value to the json as 'output3'.
            rapidjson::Value returnValueOutput3;
            responseJson.AddMember("output3", returnValueOutput3, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOneBinaryHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneBinary");
    if (_callOneBinaryHandler)
    {
        std::vector<uint8_t> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        std::vector<uint8_t> ret = _callOneBinaryHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallOptionalBinaryHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalBinary");
    if (_callOptionalBinaryHandler)
    {
        boost::optional<std::vector<uint8_t>> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value is a single value.
        boost::optional<std::vector<uint8_t>> ret = _callOptionalBinaryHandler(tempInput1);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the 'ret' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

void TestAbleServer::_callCallThreeBinariesHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeBinaries");
    if (_callThreeBinariesHandler)
    {
        std::vector<uint8_t> tempInput1;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input1");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::vector<uint8_t> tempInput2;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input2");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        boost::optional<std::vector<uint8_t>> tempInput3;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("input3");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        // Return value has multiple values.
        CallThreeBinariesReturnValue ret = _callThreeBinariesHandler(tempInput1, tempInput2, tempInput3);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the 'ret.output1' value to the json as 'output1'.
            rapidjson::Value returnValueOutput1;
            responseJson.AddMember("output1", returnValueOutput1, responseJson.GetAllocator());

            // add the 'ret.output2' value to the json as 'output2'.
            rapidjson::Value returnValueOutput2;
            responseJson.AddMember("output2", returnValueOutput2, responseJson.GetAllocator());

            // add the 'ret.output3' value to the json as 'output3'.
            rapidjson::Value returnValueOutput3;
            responseJson.AddMember("output3", returnValueOutput3, responseJson.GetAllocator());

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            MqttProperties mqttProps;
            mqttProps.correlationId = optCorrelationId;
            mqttProps.returnCode = MethodReturnCode::SUCCESS;
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, mqttProps);
        }
    }
}

boost::optional<ReadWriteIntegerProperty> TestAbleServer::getReadWriteIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    return _readWriteIntegerProperty;
}

void TestAbleServer::registerReadWriteIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
    _readWriteIntegerPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteIntegerProperty(int value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
        _readWriteIntegerProperty = value;
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

void TestAbleServer::republishReadWriteIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteIntegerProperty)
    {
        doc.SetObject();

        doc.AddMember("value", *_readWriteIntegerProperty, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteInteger/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    int tempValue;
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
        _lastReadWriteIntegerPropertyVersion++;
    }
    republishReadWriteIntegerProperty();
}

boost::optional<ReadOnlyIntegerProperty> TestAbleServer::getReadOnlyIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    return _readOnlyIntegerProperty;
}

void TestAbleServer::registerReadOnlyIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
    _readOnlyIntegerPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadOnlyIntegerProperty(int value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
        _readOnlyIntegerProperty = value;
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

void TestAbleServer::republishReadOnlyIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyIntegerProperty)
    {
        doc.SetObject();

        doc.AddMember("value", *_readOnlyIntegerProperty, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readOnlyInteger/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadOnlyIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    int tempValue;
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
        _lastReadOnlyIntegerPropertyVersion++;
    }
    republishReadOnlyIntegerProperty();
}

boost::optional<int> TestAbleServer::getReadWriteOptionalIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    return _readWriteOptionalIntegerProperty;
}

void TestAbleServer::registerReadWriteOptionalIntegerPropertyCallback(const std::function<void(boost::optional<int> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
    _readWriteOptionalIntegerPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteOptionalIntegerProperty(boost::optional<int> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
        _readWriteOptionalIntegerProperty = value;
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

void TestAbleServer::republishReadWriteOptionalIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalIntegerProperty)
    {
        doc.SetObject();

        doc.AddMember("value", *_readWriteOptionalIntegerProperty, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteOptionalInteger/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteOptionalIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    boost::optional<int> tempValue = boost::none;
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
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
        _readWriteOptionalIntegerProperty = tempValue;
        _lastReadWriteOptionalIntegerPropertyVersion++;
    }
    republishReadWriteOptionalIntegerProperty();
}

boost::optional<ReadWriteTwoIntegersProperty> TestAbleServer::getReadWriteTwoIntegersProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
    return _readWriteTwoIntegersProperty;
}

void TestAbleServer::registerReadWriteTwoIntegersPropertyCallback(const std::function<void(int first, boost::optional<int> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
    _readWriteTwoIntegersPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteTwoIntegersProperty(int first, boost::optional<int> second)
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

void TestAbleServer::republishReadWriteTwoIntegersProperty() const
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteTwoIntegers/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteTwoIntegersPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

boost::optional<ReadOnlyStringProperty> TestAbleServer::getReadOnlyStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    return _readOnlyStringProperty;
}

void TestAbleServer::registerReadOnlyStringPropertyCallback(const std::function<void(const std::string& value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
    _readOnlyStringPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadOnlyStringProperty(const std::string& value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
        _readOnlyStringProperty = value;
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

void TestAbleServer::republishReadOnlyStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyStringProperty)
    {
        doc.SetObject();
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(_readOnlyStringProperty->c_str(), _readOnlyStringProperty->size(), doc.GetAllocator());
        doc.AddMember("value", tempStringValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readOnlyString/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadOnlyStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    std::string tempValue;
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
        _lastReadOnlyStringPropertyVersion++;
    }
    republishReadOnlyStringProperty();
}

boost::optional<ReadWriteStringProperty> TestAbleServer::getReadWriteStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    return _readWriteStringProperty;
}

void TestAbleServer::registerReadWriteStringPropertyCallback(const std::function<void(const std::string& value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
    _readWriteStringPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteStringProperty(const std::string& value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
        _readWriteStringProperty = value;
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

void TestAbleServer::republishReadWriteStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteStringProperty)
    {
        doc.SetObject();
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(_readWriteStringProperty->c_str(), _readWriteStringProperty->size(), doc.GetAllocator());
        doc.AddMember("value", tempStringValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteString/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    std::string tempValue;
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
        _lastReadWriteStringPropertyVersion++;
    }
    republishReadWriteStringProperty();
}

boost::optional<std::string> TestAbleServer::getReadWriteOptionalStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    return _readWriteOptionalStringProperty;
}

void TestAbleServer::registerReadWriteOptionalStringPropertyCallback(const std::function<void(boost::optional<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
    _readWriteOptionalStringPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteOptionalStringProperty(boost::optional<std::string> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
        _readWriteOptionalStringProperty = value;
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

void TestAbleServer::republishReadWriteOptionalStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalStringProperty)
    {
        doc.SetObject();
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(_readWriteOptionalStringProperty->c_str(), _readWriteOptionalStringProperty->size(), doc.GetAllocator());
        doc.AddMember("value", tempStringValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteOptionalString/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteOptionalStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    boost::optional<std::string> tempValue = boost::none;
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
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
        _readWriteOptionalStringProperty = tempValue;
        _lastReadWriteOptionalStringPropertyVersion++;
    }
    republishReadWriteOptionalStringProperty();
}

boost::optional<ReadWriteTwoStringsProperty> TestAbleServer::getReadWriteTwoStringsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
    return _readWriteTwoStringsProperty;
}

void TestAbleServer::registerReadWriteTwoStringsPropertyCallback(const std::function<void(const std::string& first, boost::optional<std::string> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
    _readWriteTwoStringsPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteTwoStringsProperty(const std::string& first, boost::optional<std::string> second)
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

void TestAbleServer::republishReadWriteTwoStringsProperty() const
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteTwoStrings/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteTwoStringsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

boost::optional<ReadWriteStructProperty> TestAbleServer::getReadWriteStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    return _readWriteStructProperty;
}

void TestAbleServer::registerReadWriteStructPropertyCallback(const std::function<void(AllTypes value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
    _readWriteStructPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteStructProperty(AllTypes value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
        _readWriteStructProperty = value;
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

void TestAbleServer::republishReadWriteStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteStructProperty)
    {
        doc.SetObject();
        // structure
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteStruct/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteStructPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    AllTypes tempValue;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsObject())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
        _readWriteStructProperty = tempValue;
        _lastReadWriteStructPropertyVersion++;
    }
    republishReadWriteStructProperty();
}

ReadWriteOptionalStructProperty TestAbleServer::getReadWriteOptionalStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    return _readWriteOptionalStructProperty;
}

void TestAbleServer::registerReadWriteOptionalStructPropertyCallback(const std::function<void(AllTypes value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
    _readWriteOptionalStructPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteOptionalStructProperty(AllTypes value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
        _readWriteOptionalStructProperty = value;
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

void TestAbleServer::republishReadWriteOptionalStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalStructProperty)
    {
        doc.SetObject();
        // structure
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteOptionalStruct/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteOptionalStructPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    boost::optional<AllTypes> tempValue = boost::none;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsObject())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
        _readWriteOptionalStructProperty = tempValue;
        _lastReadWriteOptionalStructPropertyVersion++;
    }
    republishReadWriteOptionalStructProperty();
}

boost::optional<ReadWriteTwoStructsProperty> TestAbleServer::getReadWriteTwoStructsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
    return _readWriteTwoStructsProperty;
}

void TestAbleServer::registerReadWriteTwoStructsPropertyCallback(const std::function<void(AllTypes first, AllTypes second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
    _readWriteTwoStructsPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteTwoStructsProperty(AllTypes first, AllTypes second)
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

void TestAbleServer::republishReadWriteTwoStructsProperty() const
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteTwoStructs/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteTwoStructsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

boost::optional<ReadOnlyEnumProperty> TestAbleServer::getReadOnlyEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    return _readOnlyEnumProperty;
}

void TestAbleServer::registerReadOnlyEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
    _readOnlyEnumPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadOnlyEnumProperty(Numbers value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
        _readOnlyEnumProperty = value;
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

void TestAbleServer::republishReadOnlyEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyEnumProperty)
    {
        doc.SetObject();
        // enumeration
        doc.AddMember("value", static_cast<int>(*_readOnlyEnumProperty), doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readOnlyEnum/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadOnlyEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    Numbers tempValue;
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
        _lastReadOnlyEnumPropertyVersion++;
    }
    republishReadOnlyEnumProperty();
}

boost::optional<ReadWriteEnumProperty> TestAbleServer::getReadWriteEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    return _readWriteEnumProperty;
}

void TestAbleServer::registerReadWriteEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
    _readWriteEnumPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteEnumProperty(Numbers value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
        _readWriteEnumProperty = value;
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

void TestAbleServer::republishReadWriteEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteEnumProperty)
    {
        doc.SetObject();
        // enumeration
        doc.AddMember("value", static_cast<int>(*_readWriteEnumProperty), doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteEnum/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    Numbers tempValue;
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
        _lastReadWriteEnumPropertyVersion++;
    }
    republishReadWriteEnumProperty();
}

boost::optional<Numbers> TestAbleServer::getReadWriteOptionalEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    return _readWriteOptionalEnumProperty;
}

void TestAbleServer::registerReadWriteOptionalEnumPropertyCallback(const std::function<void(boost::optional<Numbers> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
    _readWriteOptionalEnumPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteOptionalEnumProperty(boost::optional<Numbers> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
        _readWriteOptionalEnumProperty = value;
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

void TestAbleServer::republishReadWriteOptionalEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalEnumProperty)
    {
        doc.SetObject();
        // enumeration
        doc.AddMember("value", static_cast<int>(*_readWriteOptionalEnumProperty), doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteOptionalEnum/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteOptionalEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    boost::optional<Numbers> tempValue = boost::none;
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
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
        _readWriteOptionalEnumProperty = tempValue;
        _lastReadWriteOptionalEnumPropertyVersion++;
    }
    republishReadWriteOptionalEnumProperty();
}

boost::optional<ReadWriteTwoEnumsProperty> TestAbleServer::getReadWriteTwoEnumsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
    return _readWriteTwoEnumsProperty;
}

void TestAbleServer::registerReadWriteTwoEnumsPropertyCallback(const std::function<void(Numbers first, boost::optional<Numbers> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
    _readWriteTwoEnumsPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteTwoEnumsProperty(Numbers first, boost::optional<Numbers> second)
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

void TestAbleServer::republishReadWriteTwoEnumsProperty() const
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteTwoEnums/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteTwoEnumsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

boost::optional<ReadWriteDatetimeProperty> TestAbleServer::getReadWriteDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    return _readWriteDatetimeProperty;
}

void TestAbleServer::registerReadWriteDatetimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
    _readWriteDatetimePropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteDatetimeProperty(std::chrono::time_point<std::chrono::system_clock> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
        _readWriteDatetimeProperty = value;
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

void TestAbleServer::republishReadWriteDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    rapidjson::Document doc;
    if (_readWriteDatetimeProperty)
    {
        doc.SetObject();
        // Datetime field
        std::string valueStr = timePointToIsoString(*_readWriteDatetimeProperty);
        rapidjson::Value valueValue(valueStr.c_str(), doc.GetAllocator());
        doc.AddMember("value", valueValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteDatetime/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteDatetimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    std::chrono::time_point<std::chrono::system_clock> tempValue;
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
        _lastReadWriteDatetimePropertyVersion++;
    }
    republishReadWriteDatetimeProperty();
}

boost::optional<std::chrono::time_point<std::chrono::system_clock>> TestAbleServer::getReadWriteOptionalDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    return _readWriteOptionalDatetimeProperty;
}

void TestAbleServer::registerReadWriteOptionalDatetimePropertyCallback(const std::function<void(boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
    _readWriteOptionalDatetimePropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteOptionalDatetimeProperty(boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
        _readWriteOptionalDatetimeProperty = value;
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

void TestAbleServer::republishReadWriteOptionalDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalDatetimeProperty)
    {
        doc.SetObject();
        // Datetime field
        std::string valueStr = timePointToIsoString(*_readWriteOptionalDatetimeProperty);
        rapidjson::Value valueValue(valueStr.c_str(), doc.GetAllocator());
        doc.AddMember("value", valueValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteOptionalDatetime/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteOptionalDatetimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    boost::optional<std::chrono::time_point<std::chrono::system_clock>> tempValue = boost::none;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
        _readWriteOptionalDatetimeProperty = tempValue;
        _lastReadWriteOptionalDatetimePropertyVersion++;
    }
    republishReadWriteOptionalDatetimeProperty();
}

boost::optional<ReadWriteTwoDatetimesProperty> TestAbleServer::getReadWriteTwoDatetimesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
    return _readWriteTwoDatetimesProperty;
}

void TestAbleServer::registerReadWriteTwoDatetimesPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> first, boost::optional<std::chrono::time_point<std::chrono::system_clock>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
    _readWriteTwoDatetimesPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteTwoDatetimesProperty(std::chrono::time_point<std::chrono::system_clock> first, boost::optional<std::chrono::time_point<std::chrono::system_clock>> second)
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

void TestAbleServer::republishReadWriteTwoDatetimesProperty() const
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteTwoDatetimes/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteTwoDatetimesPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

boost::optional<ReadWriteDurationProperty> TestAbleServer::getReadWriteDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    return _readWriteDurationProperty;
}

void TestAbleServer::registerReadWriteDurationPropertyCallback(const std::function<void(std::chrono::duration<double> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
    _readWriteDurationPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteDurationProperty(std::chrono::duration<double> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
        _readWriteDurationProperty = value;
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

void TestAbleServer::republishReadWriteDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteDurationProperty)
    {
        doc.SetObject();
        // duration field
        std::string valueStr = durationToIsoString(*_readWriteDurationProperty);
        rapidjson::Value valueValue(valueStr.c_str(), doc.GetAllocator());
        doc.AddMember("value", valueValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteDuration/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteDurationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    std::chrono::duration<double> tempValue;
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
        _lastReadWriteDurationPropertyVersion++;
    }
    republishReadWriteDurationProperty();
}

boost::optional<std::chrono::duration<double>> TestAbleServer::getReadWriteOptionalDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    return _readWriteOptionalDurationProperty;
}

void TestAbleServer::registerReadWriteOptionalDurationPropertyCallback(const std::function<void(boost::optional<std::chrono::duration<double>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
    _readWriteOptionalDurationPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteOptionalDurationProperty(boost::optional<std::chrono::duration<double>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
        _readWriteOptionalDurationProperty = value;
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

void TestAbleServer::republishReadWriteOptionalDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalDurationProperty)
    {
        doc.SetObject();
        // duration field
        std::string valueStr = durationToIsoString(*_readWriteOptionalDurationProperty);
        rapidjson::Value valueValue(valueStr.c_str(), doc.GetAllocator());
        doc.AddMember("value", valueValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteOptionalDuration/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteOptionalDurationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    boost::optional<std::chrono::duration<double>> tempValue = boost::none;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
        _readWriteOptionalDurationProperty = tempValue;
        _lastReadWriteOptionalDurationPropertyVersion++;
    }
    republishReadWriteOptionalDurationProperty();
}

boost::optional<ReadWriteTwoDurationsProperty> TestAbleServer::getReadWriteTwoDurationsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
    return _readWriteTwoDurationsProperty;
}

void TestAbleServer::registerReadWriteTwoDurationsPropertyCallback(const std::function<void(std::chrono::duration<double> first, boost::optional<std::chrono::duration<double>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
    _readWriteTwoDurationsPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteTwoDurationsProperty(std::chrono::duration<double> first, boost::optional<std::chrono::duration<double>> second)
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

void TestAbleServer::republishReadWriteTwoDurationsProperty() const
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteTwoDurations/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteTwoDurationsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

boost::optional<ReadWriteBinaryProperty> TestAbleServer::getReadWriteBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    return _readWriteBinaryProperty;
}

void TestAbleServer::registerReadWriteBinaryPropertyCallback(const std::function<void(std::vector<uint8_t> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
    _readWriteBinaryPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteBinaryProperty(std::vector<uint8_t> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
        _readWriteBinaryProperty = value;
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

void TestAbleServer::republishReadWriteBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteBinaryProperty)
    {
        doc.SetObject();
        // binary field
        std::string valueStr = base64Encode(*_readWriteBinaryProperty);
        rapidjson::Value valueValue(valueStr.c_str(), doc.GetAllocator());
        doc.AddMember("value", valueValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteBinary/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteBinaryPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    std::vector<uint8_t> tempValue;
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
        _lastReadWriteBinaryPropertyVersion++;
    }
    republishReadWriteBinaryProperty();
}

boost::optional<std::vector<uint8_t>> TestAbleServer::getReadWriteOptionalBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    return _readWriteOptionalBinaryProperty;
}

void TestAbleServer::registerReadWriteOptionalBinaryPropertyCallback(const std::function<void(boost::optional<std::vector<uint8_t>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
    _readWriteOptionalBinaryPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteOptionalBinaryProperty(boost::optional<std::vector<uint8_t>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
        _readWriteOptionalBinaryProperty = value;
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

void TestAbleServer::republishReadWriteOptionalBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalBinaryProperty)
    {
        doc.SetObject();
        // binary field
        std::string valueStr = base64Encode(*_readWriteOptionalBinaryProperty);
        rapidjson::Value valueValue(valueStr.c_str(), doc.GetAllocator());
        doc.AddMember("value", valueValue, doc.GetAllocator());
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteOptionalBinary/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteOptionalBinaryPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

    boost::optional<std::vector<uint8_t>> tempValue = boost::none;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
        _readWriteOptionalBinaryProperty = tempValue;
        _lastReadWriteOptionalBinaryPropertyVersion++;
    }
    republishReadWriteOptionalBinaryProperty();
}

boost::optional<ReadWriteTwoBinariesProperty> TestAbleServer::getReadWriteTwoBinariesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
    return _readWriteTwoBinariesProperty;
}

void TestAbleServer::registerReadWriteTwoBinariesPropertyCallback(const std::function<void(std::vector<uint8_t> first, boost::optional<std::vector<uint8_t>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
    _readWriteTwoBinariesPropertyCallbacks.push_back(cb);
}

void TestAbleServer::updateReadWriteTwoBinariesProperty(std::vector<uint8_t> first, boost::optional<std::vector<uint8_t>> second)
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

void TestAbleServer::republishReadWriteTwoBinariesProperty() const
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
    _broker->Publish((boost::format("testAble/%1%/property/readWriteTwoBinaries/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void TestAbleServer::_receiveReadWriteTwoBinariesPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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

void TestAbleServer::_advertisementThreadLoop()
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

        // Publish to testAble/<instance_id>/interface
        std::string topic = (boost::format("testAble/%1%/interface") % _instanceId).str();
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
