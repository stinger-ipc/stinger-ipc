

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

constexpr const char FullServer::NAME[];
constexpr const char FullServer::INTERFACE_VERSION[];

FullServer::FullServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId):
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

    _addNumbersMethodSubscriptionId = _broker->Subscribe((boost::format("full/%1%/method/addNumbers") % _instanceId).str(), 2);
    _doSomethingMethodSubscriptionId = _broker->Subscribe((boost::format("full/%1%/method/doSomething") % _instanceId).str(), 2);
    _echoMethodSubscriptionId = _broker->Subscribe((boost::format("full/%1%/method/echo") % _instanceId).str(), 2);
    _whatTimeIsItMethodSubscriptionId = _broker->Subscribe((boost::format("full/%1%/method/whatTimeIsIt") % _instanceId).str(), 2);
    _setTheTimeMethodSubscriptionId = _broker->Subscribe((boost::format("full/%1%/method/setTheTime") % _instanceId).str(), 2);
    _forwardTimeMethodSubscriptionId = _broker->Subscribe((boost::format("full/%1%/method/forwardTime") % _instanceId).str(), 2);
    _howOffIsTheClockMethodSubscriptionId = _broker->Subscribe((boost::format("full/%1%/method/howOffIsTheClock") % _instanceId).str(), 2);

    _favoriteNumberPropertySubscriptionId = _broker->Subscribe((boost::format("full/%1%/property/favoriteNumber/setValue") % _instanceId).str(), 1);
    _favoriteFoodsPropertySubscriptionId = _broker->Subscribe((boost::format("full/%1%/property/favoriteFoods/setValue") % _instanceId).str(), 1);
    _lunchMenuPropertySubscriptionId = _broker->Subscribe((boost::format("full/%1%/property/lunchMenu/setValue") % _instanceId).str(), 1);
    _familyNamePropertySubscriptionId = _broker->Subscribe((boost::format("full/%1%/property/familyName/setValue") % _instanceId).str(), 1);
    _lastBreakfastTimePropertySubscriptionId = _broker->Subscribe((boost::format("full/%1%/property/lastBreakfastTime/setValue") % _instanceId).str(), 1);
    _breakfastLengthPropertySubscriptionId = _broker->Subscribe((boost::format("full/%1%/property/breakfastLength/setValue") % _instanceId).str(), 1);
    _lastBirthdaysPropertySubscriptionId = _broker->Subscribe((boost::format("full/%1%/property/lastBirthdays/setValue") % _instanceId).str(), 1);

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&FullServer::_advertisementThreadLoop, this);
}

FullServer::~FullServer()
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

    std::string topic = (boost::format("full/%1%/interface") % _instanceId).str();
    _broker->Publish(topic, "", 1, true, MqttProperties());

    _broker->Unsubscribe((boost::format("full/%1%/method/addNumbers") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/method/doSomething") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/method/echo") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/method/whatTimeIsIt") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/method/setTheTime") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/method/forwardTime") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/method/howOffIsTheClock") % _instanceId).str());

    _broker->Unsubscribe((boost::format("full/%1%/property/favoriteNumber/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/property/favoriteFoods/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/property/lunchMenu/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/property/familyName/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/property/lastBreakfastTime/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/property/breakfastLength/setValue") % _instanceId).str());
    _broker->Unsubscribe((boost::format("full/%1%/property/lastBirthdays/setValue") % _instanceId).str());
}

void FullServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    const int noSubId = -1;
    int subscriptionId = mqttProps.subscriptionId.value_or(noSubId);

    if ((subscriptionId == _addNumbersMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/method/addNumbers") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as addNumbers method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_addNumbersHandler)
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

                _callAddNumbersHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _doSomethingMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/method/doSomething") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as doSomething method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_doSomethingHandler)
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

                _callDoSomethingHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _echoMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/method/echo") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as echo method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_echoHandler)
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

                _callEchoHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _whatTimeIsItMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/method/whatTimeIsIt") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as what_time_is_it method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_whatTimeIsItHandler)
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

                _callWhatTimeIsItHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _setTheTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/method/setTheTime") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as set_the_time method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_setTheTimeHandler)
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

                _callSetTheTimeHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _forwardTimeMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/method/forwardTime") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as forward_time method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_forwardTimeHandler)
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

                _callForwardTimeHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if ((subscriptionId == _howOffIsTheClockMethodSubscriptionId) || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/method/howOffIsTheClock") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as how_off_is_the_clock method request.", topic.c_str());
        rapidjson::Document doc;
        try
        {
            if (_howOffIsTheClockHandler)
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

                _callHowOffIsTheClockHandler(topic, doc, mqttProps.correlationId, mqttProps.responseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    if (subscriptionId == _favoriteNumberPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/property/favoriteNumber/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as favorite_number property update.", topic.c_str());
        _receiveFavoriteNumberPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _favoriteFoodsPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/property/favoriteFoods/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as favorite_foods property update.", topic.c_str());
        _receiveFavoriteFoodsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _lunchMenuPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/property/lunchMenu/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as lunch_menu property update.", topic.c_str());
        _receiveLunchMenuPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _familyNamePropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/property/familyName/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as family_name property update.", topic.c_str());
        _receiveFamilyNamePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _lastBreakfastTimePropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/property/lastBreakfastTime/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as last_breakfast_time property update.", topic.c_str());
        _receiveLastBreakfastTimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _breakfastLengthPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/property/breakfastLength/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as breakfast_length property update.", topic.c_str());
        _receiveBreakfastLengthPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _lastBirthdaysPropertySubscriptionId || (subscriptionId == noSubId && _broker->TopicMatchesSubscription(topic, (boost::format("full/%1%/property/lastBirthdays/setValue") % _instanceId).str())))
    {
        _broker->Log(LOG_INFO, "Message to `%s` matched as last_birthdays property update.", topic.c_str());
        _receiveLastBirthdaysPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

boost::future<bool> FullServer::emitTodayIsSignal(int dayOfMonth, boost::optional<DayOfTheWeek> dayOfWeek, std::chrono::time_point<std::chrono::system_clock> timestamp, std::chrono::duration<double> process_time, std::vector<uint8_t> memory_segment)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("dayOfMonth", dayOfMonth, doc.GetAllocator());

    doc.AddMember("dayOfWeek", static_cast<int>(*dayOfWeek), doc.GetAllocator());

    { // Restrict Scope
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), doc.GetAllocator());
        doc.AddMember("timestamp", tempTimestampStringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempProcessTimeStringValue;
        std::string processTimeIsoString = durationToIsoString(process_time);
        tempProcessTimeStringValue.SetString(processTimeIsoString.c_str(), processTimeIsoString.size(), doc.GetAllocator());
        doc.AddMember("process_time", tempProcessTimeStringValue, doc.GetAllocator());
    }

    { // Restrict Scope
        rapidjson::Value tempMemorySegmentStringValue;
        std::string memorySegmentB64String = base64Encode(memory_segment);
        tempMemorySegmentStringValue.SetString(memorySegmentB64String.c_str(), memorySegmentB64String.size(), doc.GetAllocator());
        doc.AddMember("memory_segment", tempMemorySegmentStringValue, doc.GetAllocator());
    }
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish((boost::format("full/%1%/signal/todayIs") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void FullServer::registerAddNumbersHandler(std::function<int(int, int, boost::optional<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle full/+/method/addNumbers method requests.");
    _addNumbersHandler = func;
}

void FullServer::registerDoSomethingHandler(std::function<DoSomethingReturnValue(const std::string&)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle full/+/method/doSomething method requests.");
    _doSomethingHandler = func;
}

void FullServer::registerEchoHandler(std::function<std::string(const std::string&)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle full/+/method/echo method requests.");
    _echoHandler = func;
}

void FullServer::registerWhatTimeIsItHandler(std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::time_point<std::chrono::system_clock>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle full/+/method/whatTimeIsIt method requests.");
    _whatTimeIsItHandler = func;
}

void FullServer::registerSetTheTimeHandler(std::function<SetTheTimeReturnValue(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle full/+/method/setTheTime method requests.");
    _setTheTimeHandler = func;
}

void FullServer::registerForwardTimeHandler(std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::duration<double>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle full/+/method/forwardTime method requests.");
    _forwardTimeHandler = func;
}

void FullServer::registerHowOffIsTheClockHandler(std::function<std::chrono::duration<double>(std::chrono::time_point<std::chrono::system_clock>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle full/+/method/howOffIsTheClock method requests.");
    _howOffIsTheClockHandler = func;
}

void FullServer::_callAddNumbersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to addNumbers");
    if (_addNumbersHandler)
    {
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
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        int ret = _addNumbersHandler(tempFirst, tempSecond, tempThird);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the sum (a/n PRIMITIVE) to the json
            rapidjson::Value returnValueSum;
            returnValueSum.SetInt(ret);
            responseJson.AddMember("sum", returnValueSum, responseJson.GetAllocator());

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

void FullServer::_callDoSomethingHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to doSomething");
    if (_doSomethingHandler)
    {
        std::string tempAString;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("aString");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
                tempAString = itr->value.GetString();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        DoSomethingReturnValue ret = _doSomethingHandler(tempAString);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the label (a/n PRIMITIVE) to the json
            rapidjson::Value returnValueLabel;
            returnValueLabel.SetString(ret.label.c_str(), ret.label.size(), responseJson.GetAllocator());
            responseJson.AddMember("label", returnValueLabel, responseJson.GetAllocator());

            // add the identifier (a/n PRIMITIVE) to the json
            rapidjson::Value returnValueIdentifier;
            returnValueIdentifier.Set(ret.identifier);
            responseJson.AddMember("identifier", returnValueIdentifier, responseJson.GetAllocator());

            // add the day (a/n ENUM) to the json
            rapidjson::Value returnValueDay;
            returnValueDay.SetInt(static_cast<int>(ret.day));
            responseJson.AddMember("day", returnValueDay, responseJson.GetAllocator());

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

void FullServer::_callEchoHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to echo");
    if (_echoHandler)
    {
        std::string tempMessage;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("message");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
                tempMessage = itr->value.GetString();
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::string ret = _echoHandler(tempMessage);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the message (a/n PRIMITIVE) to the json
            rapidjson::Value returnValueMessage;
            returnValueMessage.SetString(ret.c_str(), ret.size(), responseJson.GetAllocator());
            responseJson.AddMember("message", returnValueMessage, responseJson.GetAllocator());

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

void FullServer::_callWhatTimeIsItHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to what_time_is_it");
    if (_whatTimeIsItHandler)
    {
        std::chrono::time_point<std::chrono::system_clock> tempTheFirstTime;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("the_first_time");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::chrono::time_point<std::chrono::system_clock> ret = _whatTimeIsItHandler(tempTheFirstTime);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the timestamp (a/n DATETIME) to the json
            rapidjson::Value returnValueTimestamp;
            responseJson.AddMember("timestamp", returnValueTimestamp, responseJson.GetAllocator());

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

void FullServer::_callSetTheTimeHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to set_the_time");
    if (_setTheTimeHandler)
    {
        std::chrono::time_point<std::chrono::system_clock> tempTheFirstTime;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("the_first_time");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::chrono::time_point<std::chrono::system_clock> tempTheSecondTime;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("the_second_time");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        SetTheTimeReturnValue ret = _setTheTimeHandler(tempTheFirstTime, tempTheSecondTime);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a struct of values that need added to json

            // add the timestamp (a/n DATETIME) to the json
            rapidjson::Value returnValueTimestamp;
            responseJson.AddMember("timestamp", returnValueTimestamp, responseJson.GetAllocator());

            // add the confirmation_message (a/n PRIMITIVE) to the json
            rapidjson::Value returnValueConfirmationMessage;
            returnValueConfirmationMessage.SetString(ret.confirmation_message.c_str(), ret.confirmation_message.size(), responseJson.GetAllocator());
            responseJson.AddMember("confirmation_message", returnValueConfirmationMessage, responseJson.GetAllocator());

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

void FullServer::_callForwardTimeHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to forward_time");
    if (_forwardTimeHandler)
    {
        std::chrono::duration<double> tempAdjustment;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("adjustment");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::chrono::time_point<std::chrono::system_clock> ret = _forwardTimeHandler(tempAdjustment);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the new_time (a/n DATETIME) to the json
            rapidjson::Value returnValueNewTime;
            responseJson.AddMember("new_time", returnValueNewTime, responseJson.GetAllocator());

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

void FullServer::_callHowOffIsTheClockHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to how_off_is_the_clock");
    if (_howOffIsTheClockHandler)
    {
        std::chrono::time_point<std::chrono::system_clock> tempActualTime;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("actual_time");
            if (itr != doc.MemberEnd() && itr->value.IsString())
            {
            }
            else
            {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }

        std::chrono::duration<double> ret = _howOffIsTheClockHandler(tempActualTime);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();

            // Return type is a single value

            // add the difference (a/n DURATION) to the json
            rapidjson::Value returnValueDifference;
            responseJson.AddMember("difference", returnValueDifference, responseJson.GetAllocator());

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

boost::optional<FavoriteNumberProperty> FullServer::getFavoriteNumberProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
    return _favoriteNumberProperty;
}

void FullServer::registerFavoriteNumberPropertyCallback(const std::function<void(int number)>& cb)
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyCallbacksMutex);
    _favoriteNumberPropertyCallbacks.push_back(cb);
}

void FullServer::updateFavoriteNumberProperty(int number)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
        _favoriteNumberProperty = number;
        _lastFavoriteNumberPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteNumberPropertyCallbacksMutex);
        for (const auto& cb: _favoriteNumberPropertyCallbacks)
        {
            cb(number);
        }
    }
    republishFavoriteNumberProperty();
}

void FullServer::republishFavoriteNumberProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
    rapidjson::Document doc;
    if (_favoriteNumberProperty)
    {
        doc.SetObject();

        doc.AddMember("number", *_favoriteNumberProperty, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastFavoriteNumberPropertyVersion;
    _broker->Publish((boost::format("full/%1%/property/favoriteNumber/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void FullServer::_receiveFavoriteNumberPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse favorite_number property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received favorite_number payload is not an object or null");
    }

    // TODO: Check _lastFavoriteNumberPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    int tempNumber;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("number");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempNumber = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
        _favoriteNumberProperty = tempNumber;
        _lastFavoriteNumberPropertyVersion++;
    }
    republishFavoriteNumberProperty();
}

boost::optional<FavoriteFoodsProperty> FullServer::getFavoriteFoodsProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
    return _favoriteFoodsProperty;
}

void FullServer::registerFavoriteFoodsPropertyCallback(const std::function<void(const std::string& drink, int slices_of_pizza, boost::optional<std::string> breakfast)>& cb)
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyCallbacksMutex);
    _favoriteFoodsPropertyCallbacks.push_back(cb);
}

void FullServer::updateFavoriteFoodsProperty(const std::string& drink, int slices_of_pizza, boost::optional<std::string> breakfast)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
        _favoriteFoodsProperty = FavoriteFoodsProperty{ drink, slices_of_pizza, breakfast };
        _lastFavoriteFoodsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyCallbacksMutex);
        for (const auto& cb: _favoriteFoodsPropertyCallbacks)
        {
            cb(drink, slices_of_pizza, breakfast);
        }
    }
    republishFavoriteFoodsProperty();
}

void FullServer::republishFavoriteFoodsProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
    rapidjson::Document doc;
    if (_favoriteFoodsProperty)
    {
        doc.SetObject();

        _favoriteFoodsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastFavoriteFoodsPropertyVersion;
    _broker->Publish((boost::format("full/%1%/property/favoriteFoods/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void FullServer::_receiveFavoriteFoodsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse favorite_foods property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received favorite_foods payload is not an object or null");
    }

    // TODO: Check _lastFavoriteFoodsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 3 values into struct.
    FavoriteFoodsProperty tempValue = FavoriteFoodsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
        _favoriteFoodsProperty = tempValue;
        _lastFavoriteFoodsPropertyVersion++;
    }
    republishFavoriteFoodsProperty();
}

boost::optional<LunchMenuProperty> FullServer::getLunchMenuProperty() const
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
    return _lunchMenuProperty;
}

void FullServer::registerLunchMenuPropertyCallback(const std::function<void(Lunch monday, Lunch tuesday)>& cb)
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyCallbacksMutex);
    _lunchMenuPropertyCallbacks.push_back(cb);
}

void FullServer::updateLunchMenuProperty(Lunch monday, Lunch tuesday)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
        _lunchMenuProperty = LunchMenuProperty{ monday, tuesday };
        _lastLunchMenuPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lunchMenuPropertyCallbacksMutex);
        for (const auto& cb: _lunchMenuPropertyCallbacks)
        {
            cb(monday, tuesday);
        }
    }
    republishLunchMenuProperty();
}

void FullServer::republishLunchMenuProperty() const
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
    rapidjson::Document doc;
    if (_lunchMenuProperty)
    {
        doc.SetObject();

        _lunchMenuProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastLunchMenuPropertyVersion;
    _broker->Publish((boost::format("full/%1%/property/lunchMenu/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void FullServer::_receiveLunchMenuPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse lunch_menu property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received lunch_menu payload is not an object or null");
    }

    // TODO: Check _lastLunchMenuPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    LunchMenuProperty tempValue = LunchMenuProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
        _lunchMenuProperty = tempValue;
        _lastLunchMenuPropertyVersion++;
    }
    republishLunchMenuProperty();
}

boost::optional<FamilyNameProperty> FullServer::getFamilyNameProperty() const
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
    return _familyNameProperty;
}

void FullServer::registerFamilyNamePropertyCallback(const std::function<void(const std::string& family_name)>& cb)
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyCallbacksMutex);
    _familyNamePropertyCallbacks.push_back(cb);
}

void FullServer::updateFamilyNameProperty(const std::string& family_name)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
        _familyNameProperty = family_name;
        _lastFamilyNamePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_familyNamePropertyCallbacksMutex);
        for (const auto& cb: _familyNamePropertyCallbacks)
        {
            cb(family_name);
        }
    }
    republishFamilyNameProperty();
}

void FullServer::republishFamilyNameProperty() const
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
    rapidjson::Document doc;
    if (_familyNameProperty)
    {
        doc.SetObject();
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(_familyNameProperty->c_str(), _familyNameProperty->size(), doc.GetAllocator());
        doc.AddMember("family_name", tempStringValue, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastFamilyNamePropertyVersion;
    _broker->Publish((boost::format("full/%1%/property/familyName/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void FullServer::_receiveFamilyNamePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse family_name property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received family_name payload is not an object or null");
    }

    // TODO: Check _lastFamilyNamePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    std::string tempFamilyName;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("family_name");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
        tempFamilyName = itr->value.GetString();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
        _familyNameProperty = tempFamilyName;
        _lastFamilyNamePropertyVersion++;
    }
    republishFamilyNameProperty();
}

boost::optional<LastBreakfastTimeProperty> FullServer::getLastBreakfastTimeProperty() const
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
    return _lastBreakfastTimeProperty;
}

void FullServer::registerLastBreakfastTimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> timestamp)>& cb)
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyCallbacksMutex);
    _lastBreakfastTimePropertyCallbacks.push_back(cb);
}

void FullServer::updateLastBreakfastTimeProperty(std::chrono::time_point<std::chrono::system_clock> timestamp)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
        _lastBreakfastTimeProperty = timestamp;
        _lastLastBreakfastTimePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyCallbacksMutex);
        for (const auto& cb: _lastBreakfastTimePropertyCallbacks)
        {
            cb(timestamp);
        }
    }
    republishLastBreakfastTimeProperty();
}

void FullServer::republishLastBreakfastTimeProperty() const
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
    rapidjson::Document doc;
    if (_lastBreakfastTimeProperty)
    {
        doc.SetObject();
        // Datetime field
        std::string timestampStr = timePointToIsoString(*_lastBreakfastTimeProperty);
        rapidjson::Value timestampValue(timestampStr.c_str(), doc.GetAllocator());
        doc.AddMember("timestamp", timestampValue, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastLastBreakfastTimePropertyVersion;
    _broker->Publish((boost::format("full/%1%/property/lastBreakfastTime/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void FullServer::_receiveLastBreakfastTimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse last_breakfast_time property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received last_breakfast_time payload is not an object or null");
    }

    // TODO: Check _lastLastBreakfastTimePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    std::chrono::time_point<std::chrono::system_clock> tempTimestamp;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("timestamp");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
        _lastBreakfastTimeProperty = tempTimestamp;
        _lastLastBreakfastTimePropertyVersion++;
    }
    republishLastBreakfastTimeProperty();
}

boost::optional<BreakfastLengthProperty> FullServer::getBreakfastLengthProperty() const
{
    std::lock_guard<std::mutex> lock(_breakfastLengthPropertyMutex);
    return _breakfastLengthProperty;
}

void FullServer::registerBreakfastLengthPropertyCallback(const std::function<void(std::chrono::duration<double> length)>& cb)
{
    std::lock_guard<std::mutex> lock(_breakfastLengthPropertyCallbacksMutex);
    _breakfastLengthPropertyCallbacks.push_back(cb);
}

void FullServer::updateBreakfastLengthProperty(std::chrono::duration<double> length)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_breakfastLengthPropertyMutex);
        _breakfastLengthProperty = length;
        _lastBreakfastLengthPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_breakfastLengthPropertyCallbacksMutex);
        for (const auto& cb: _breakfastLengthPropertyCallbacks)
        {
            cb(length);
        }
    }
    republishBreakfastLengthProperty();
}

void FullServer::republishBreakfastLengthProperty() const
{
    std::lock_guard<std::mutex> lock(_breakfastLengthPropertyMutex);
    rapidjson::Document doc;
    if (_breakfastLengthProperty)
    {
        doc.SetObject();
        // duration field
        std::string lengthStr = durationToIsoString(*_breakfastLengthProperty);
        rapidjson::Value lengthValue(lengthStr.c_str(), doc.GetAllocator());
        doc.AddMember("length", lengthValue, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastBreakfastLengthPropertyVersion;
    _broker->Publish((boost::format("full/%1%/property/breakfastLength/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void FullServer::_receiveBreakfastLengthPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse breakfast_length property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received breakfast_length payload is not an object or null");
    }

    // TODO: Check _lastBreakfastLengthPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    std::chrono::duration<double> tempLength;
    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("length");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_breakfastLengthPropertyMutex);
        _breakfastLengthProperty = tempLength;
        _lastBreakfastLengthPropertyVersion++;
    }
    republishBreakfastLengthProperty();
}

boost::optional<LastBirthdaysProperty> FullServer::getLastBirthdaysProperty() const
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
    return _lastBirthdaysProperty;
}

void FullServer::registerLastBirthdaysPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, boost::optional<std::chrono::time_point<std::chrono::system_clock>> sister, boost::optional<int> brothers_age)>& cb)
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyCallbacksMutex);
    _lastBirthdaysPropertyCallbacks.push_back(cb);
}

void FullServer::updateLastBirthdaysProperty(std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, boost::optional<std::chrono::time_point<std::chrono::system_clock>> sister, boost::optional<int> brothers_age)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
        _lastBirthdaysProperty = LastBirthdaysProperty{ mom, dad, sister, brothers_age };
        _lastLastBirthdaysPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyCallbacksMutex);
        for (const auto& cb: _lastBirthdaysPropertyCallbacks)
        {
            cb(mom, dad, sister, brothers_age);
        }
    }
    republishLastBirthdaysProperty();
}

void FullServer::republishLastBirthdaysProperty() const
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
    rapidjson::Document doc;
    if (_lastBirthdaysProperty)
    {
        doc.SetObject();

        _lastBirthdaysProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    }
    else
    {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    mqttProps.propertyVersion = _lastLastBirthdaysPropertyVersion;
    _broker->Publish((boost::format("full/%1%/property/lastBirthdays/value") % _instanceId).str(), buf.GetString(), 1, false, mqttProps);
}

void FullServer::_receiveLastBirthdaysPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse last_birthdays property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull())
    {
        throw std::runtime_error("Received last_birthdays payload is not an object or null");
    }

    // TODO: Check _lastLastBirthdaysPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 4 values into struct.
    LastBirthdaysProperty tempValue = LastBirthdaysProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
        _lastBirthdaysProperty = tempValue;
        _lastLastBirthdaysPropertyVersion++;
    }
    republishLastBirthdaysProperty();
}

void FullServer::_advertisementThreadLoop()
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
        doc.AddMember("title", rapidjson::Value("Fully Featured Example Interface", allocator), allocator);
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

        // Publish to full/<instance_id>/interface
        std::string topic = (boost::format("full/%1%/interface") % _instanceId).str();
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
