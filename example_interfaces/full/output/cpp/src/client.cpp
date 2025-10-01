

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

constexpr const char FullClient::NAME[];
constexpr const char FullClient::INTERFACE_VERSION[];

FullClient::FullClient(std::shared_ptr<IBrokerConnection> broker)
    : _broker(broker)
{
    _broker->AddMessageCallback([this](
                                        const std::string& topic,
                                        const std::string& payload,
                                        const MqttProperties& mqttProps
                                )
                                { _receiveMessage(topic, payload, mqttProps); });
    _todayIsSignalSubscriptionId = _broker->Subscribe("full/{}/signal/todayIs", 2);
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/full/{}/method/addNumbers/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/full/{}/method/doSomething/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/full/{}/method/echo/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/full/{}/method/whatTimeIsIt/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/full/{}/method/setTheTime/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    _favoriteNumberPropertySubscriptionId = _broker->Subscribe("full/{}/property/favoriteNumber/value", 1);
    _favoriteFoodsPropertySubscriptionId = _broker->Subscribe("full/{}/property/favoriteFoods/value", 1);
    _lunchMenuPropertySubscriptionId = _broker->Subscribe("full/{}/property/lunchMenu/value", 1);
    _familyNamePropertySubscriptionId = _broker->Subscribe("full/{}/property/familyName/value", 1);
    _lastBreakfastTimePropertySubscriptionId = _broker->Subscribe("full/{}/property/lastBreakfastTime/value", 1);
    _lastBirthdaysPropertySubscriptionId = _broker->Subscribe("full/{}/property/lastBirthdays/value", 1);
}

void FullClient::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _todayIsSignalSubscriptionId)) || _broker->TopicMatchesSubscription(topic, "full/{}/signal/todayIs"))
    {
        //Log("Handling todayIs signal");
        rapidjson::Document doc;
        try
        {
            if (_todayIsSignalCallbacks.size() > 0)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse todayIs signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject())
                {
                    throw std::runtime_error("Received payload is not an object");
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
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }

                boost::optional<DayOfTheWeek> tempDayOfWeek;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dayOfWeek");
                    if (itr != doc.MemberEnd() && itr->value.IsInt())
                    {
                        tempDayOfWeek = static_cast<DayOfTheWeek>(itr->value.GetInt());
                    }
                    else
                    {
                        tempDayOfWeek = boost::none;
                    }
                }

                std::lock_guard<std::mutex> lock(_todayIsSignalCallbacksMutex);
                for (const auto& cb: _todayIsSignalCallbacks)
                {
                    cb(tempDayOfMonth, tempDayOfWeek);
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
    if (_broker->TopicMatchesSubscription(topic, "client/+/full/{}/method/addNumbers/response") && mqttProps.correlationId)
    {
        std::cout << "Matched topic for addNumbers response" << std::endl;
        _handleAddNumbersResponse(topic, payload, *mqttProps.correlationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/full/{}/method/doSomething/response") && mqttProps.correlationId)
    {
        std::cout << "Matched topic for doSomething response" << std::endl;
        _handleDoSomethingResponse(topic, payload, *mqttProps.correlationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/full/{}/method/echo/response") && mqttProps.correlationId)
    {
        std::cout << "Matched topic for echo response" << std::endl;
        _handleEchoResponse(topic, payload, *mqttProps.correlationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/full/{}/method/whatTimeIsIt/response") && mqttProps.correlationId)
    {
        std::cout << "Matched topic for what_time_is_it response" << std::endl;
        _handleWhatTimeIsItResponse(topic, payload, *mqttProps.correlationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/full/{}/method/setTheTime/response") && mqttProps.correlationId)
    {
        std::cout << "Matched topic for set_the_time response" << std::endl;
        _handleSetTheTimeResponse(topic, payload, *mqttProps.correlationId);
    }
    if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _favoriteNumberPropertySubscriptionId)) || topic == "full/{}/property/favoriteNumber/value")
    {
        _receiveFavoriteNumberPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _favoriteFoodsPropertySubscriptionId)) || topic == "full/{}/property/favoriteFoods/value")
    {
        _receiveFavoriteFoodsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _lunchMenuPropertySubscriptionId)) || topic == "full/{}/property/lunchMenu/value")
    {
        _receiveLunchMenuPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _familyNamePropertySubscriptionId)) || topic == "full/{}/property/familyName/value")
    {
        _receiveFamilyNamePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _lastBreakfastTimePropertySubscriptionId)) || topic == "full/{}/property/lastBreakfastTime/value")
    {
        _receiveLastBreakfastTimePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
    else if ((mqttProps.subscriptionId && (*mqttProps.subscriptionId == _lastBirthdaysPropertySubscriptionId)) || topic == "full/{}/property/lastBirthdays/value")
    {
        _receiveLastBirthdaysPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

void FullClient::registerTodayIsCallback(const std::function<void(int, boost::optional<DayOfTheWeek>)>& cb)
{
    std::lock_guard<std::mutex> lock(_todayIsSignalCallbacksMutex);
    _todayIsSignalCallbacks.push_back(cb);
}

boost::future<int> FullClient::addNumbers(int first, int second, boost::optional<int> third)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingAddNumbersMethodCalls[correlationId] = boost::promise<int>();

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
    responseTopicStringStream << boost::format("client/%1%/full/{}/method/addNumbers/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish("full/{}/method/addNumbers", buf.GetString(), 2, false, mqttProps);

    return _pendingAddNumbersMethodCalls[correlationId].get_future();
}

void FullClient::_handleAddNumbersResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse addNumbers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingAddNumbersMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingAddNumbersMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator sumItr = doc.FindMember("sum");
        int sum = sumItr->value.GetInt();

        promiseItr->second.set_value(sum);
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

boost::future<DoSomethingReturnValue> FullClient::doSomething(const std::string& aString)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingDoSomethingMethodCalls[correlationId] = boost::promise<DoSomethingReturnValue>();

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
    responseTopicStringStream << boost::format("client/%1%/full/{}/method/doSomething/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish("full/{}/method/doSomething", buf.GetString(), 2, false, mqttProps);

    return _pendingDoSomethingMethodCalls[correlationId].get_future();
}

void FullClient::_handleDoSomethingResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse doSomething signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingDoSomethingMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingDoSomethingMethodCalls.end())
    {
        // Response has multiple values.

        rapidjson::Value::ConstMemberIterator labelItr = doc.FindMember("label");
        const std::string& label = labelItr->value.GetString();

        rapidjson::Value::ConstMemberIterator identifierItr = doc.FindMember("identifier");
        int identifier = identifierItr->value.GetInt();

        rapidjson::Value::ConstMemberIterator dayItr = doc.FindMember("day");
        DayOfTheWeek day = static_cast<DayOfTheWeek>(dayItr->value.GetInt());

        DoSomethingReturnValue returnValue{ //initializer list

                                            label,
                                            identifier,
                                            day
        };
        promiseItr->second.set_value(returnValue);
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

boost::future<std::string> FullClient::echo(const std::string& message)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingEchoMethodCalls[correlationId] = boost::promise<std::string>();

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
    responseTopicStringStream << boost::format("client/%1%/full/{}/method/echo/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish("full/{}/method/echo", buf.GetString(), 2, false, mqttProps);

    return _pendingEchoMethodCalls[correlationId].get_future();
}

void FullClient::_handleEchoResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse echo signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingEchoMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingEchoMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator messageItr = doc.FindMember("message");
        const std::string& message = messageItr->value.GetString();

        promiseItr->second.set_value(message);
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

boost::future<std::chrono::time_point<std::chrono::system_clock>> FullClient::whatTimeIsIt(std::chrono::time_point<std::chrono::system_clock> the_first_time)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingWhatTimeIsItMethodCalls[correlationId] = boost::promise<std::chrono::time_point<std::chrono::system_clock>>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/full/{}/method/whatTimeIsIt/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish("full/{}/method/whatTimeIsIt", buf.GetString(), 2, false, mqttProps);

    return _pendingWhatTimeIsItMethodCalls[correlationId].get_future();
}

void FullClient::_handleWhatTimeIsItResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse what_time_is_it signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingWhatTimeIsItMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingWhatTimeIsItMethodCalls.end())
    {
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator timestampItr = doc.FindMember("timestamp");

        std::chrono::time_point<std::chrono::system_clock> timestamp;
        if (timestampItr != doc.MemberEnd() && timestampItr->value.IsString())
        {
            timestamp = parseIsoTimestamp(timestampItr->value.GetString());
        }

        promiseItr->second.set_value(timestamp);
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

boost::future<SetTheTimeReturnValue> FullClient::setTheTime(std::chrono::time_point<std::chrono::system_clock> the_first_time, std::chrono::time_point<std::chrono::system_clock> the_second_time)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingSetTheTimeMethodCalls[correlationId] = boost::promise<SetTheTimeReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/full/{}/method/setTheTime/response") % _broker->GetClientId();
    MqttProperties mqttProps;
    mqttProps.correlationId = correlationIdStr;
    mqttProps.responseTopic = responseTopicStringStream.str();
    mqttProps.returnCode = MethodReturnCode::SUCCESS;
    _broker->Publish("full/{}/method/setTheTime", buf.GetString(), 2, false, mqttProps);

    return _pendingSetTheTimeMethodCalls[correlationId].get_future();
}

void FullClient::_handleSetTheTimeResponse(
        const std::string& topic,
        const std::string& payload,
        const std::string& correlationId
)
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse set_the_time signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject())
    {
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingSetTheTimeMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingSetTheTimeMethodCalls.end())
    {
        // Response has multiple values.

        rapidjson::Value::ConstMemberIterator timestampItr = doc.FindMember("timestamp");

        std::chrono::time_point<std::chrono::system_clock> timestamp;
        if (timestampItr != doc.MemberEnd() && timestampItr->value.IsString())
        {
            timestamp = parseIsoTimestamp(timestampItr->value.GetString());
        }

        rapidjson::Value::ConstMemberIterator confirmationMessageItr = doc.FindMember("confirmation_message");
        const std::string& confirmation_message = confirmationMessageItr->value.GetString();

        SetTheTimeReturnValue returnValue{ //initializer list

                                           timestamp,
                                           confirmation_message
        };
        promiseItr->second.set_value(returnValue);
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

void FullClient::_receiveFavoriteNumberPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received favorite_number payload is not an object");
    }
    FavoriteNumberProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("number");
    if (itr != doc.MemberEnd() && itr->value.IsInt())
    {
        tempValue = itr->value.GetInt();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<FavoriteNumberProperty> FullClient::getFavoriteNumberProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
    return _favoriteNumberProperty;
}

void FullClient::registerFavoriteNumberPropertyCallback(const std::function<void(int number)>& cb)
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyCallbacksMutex);
    _favoriteNumberPropertyCallbacks.push_back(cb);
}

boost::future<bool> FullClient::updateFavoriteNumberProperty(int number) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("number", number, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/{}/property/favoriteNumber/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveFavoriteFoodsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received favorite_foods payload is not an object");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("slices_of_pizza");
        if (itr != doc.MemberEnd() && itr->value.IsInt())
        {
            tempValue.slices_of_pizza = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            tempValue.breakfast = boost::none;
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

            cb(tempValue.drink, tempValue.slices_of_pizza, tempValue.breakfast);
        }
    }
}

boost::optional<FavoriteFoodsProperty> FullClient::getFavoriteFoodsProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
    return _favoriteFoodsProperty;
}

void FullClient::registerFavoriteFoodsPropertyCallback(const std::function<void(const std::string& drink, int slices_of_pizza, boost::optional<std::string> breakfast)>& cb)
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyCallbacksMutex);
    _favoriteFoodsPropertyCallbacks.push_back(cb);
}

boost::future<bool> FullClient::updateFavoriteFoodsProperty(const std::string& drink, int slices_of_pizza, boost::optional<std::string> breakfast) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(drink.c_str(), drink.size(), doc.GetAllocator());
        doc.AddMember("drink", tempStringValue, doc.GetAllocator());
    }

    doc.AddMember("slices_of_pizza", slices_of_pizza, doc.GetAllocator());

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
    return _broker->Publish("full/{}/property/favoriteFoods/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLunchMenuPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received lunch_menu payload is not an object");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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

boost::optional<LunchMenuProperty> FullClient::getLunchMenuProperty() const
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
    return _lunchMenuProperty;
}

void FullClient::registerLunchMenuPropertyCallback(const std::function<void(Lunch monday, Lunch tuesday)>& cb)
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyCallbacksMutex);
    _lunchMenuPropertyCallbacks.push_back(cb);
}

boost::future<bool> FullClient::updateLunchMenuProperty(Lunch monday, Lunch tuesday) const
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/{}/property/lunchMenu/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveFamilyNamePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received family_name payload is not an object");
    }
    FamilyNameProperty tempValue;

    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("family_name");
    if (itr != doc.MemberEnd() && itr->value.IsString())
    {
        tempValue = itr->value.GetString();
    }
    else
    {
        throw std::runtime_error("Received payload doesn't have required value/type");
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

            cb(tempValue);
        }
    }
}

boost::optional<FamilyNameProperty> FullClient::getFamilyNameProperty() const
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
    return _familyNameProperty;
}

void FullClient::registerFamilyNamePropertyCallback(const std::function<void(const std::string& family_name)>& cb)
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyCallbacksMutex);
    _familyNamePropertyCallbacks.push_back(cb);
}

boost::future<bool> FullClient::updateFamilyNameProperty(const std::string& family_name) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(family_name.c_str(), family_name.size(), doc.GetAllocator());
        doc.AddMember("family_name", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/{}/property/familyName/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLastBreakfastTimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received last_breakfast_time payload is not an object");
    }
    LastBreakfastTimeProperty tempValue;

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
        _lastBreakfastTimeProperty = tempValue;
        _lastLastBreakfastTimePropertyVersion = optPropertyVersion ? *optPropertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyCallbacksMutex);
        for (const auto& cb: _lastBreakfastTimePropertyCallbacks)
        {
            // Don't need a mutex since we're using tempValue.

            cb(tempValue);
        }
    }
}

boost::optional<LastBreakfastTimeProperty> FullClient::getLastBreakfastTimeProperty() const
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
    return _lastBreakfastTimeProperty;
}

void FullClient::registerLastBreakfastTimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> timestamp)>& cb)
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyCallbacksMutex);
    _lastBreakfastTimePropertyCallbacks.push_back(cb);
}

boost::future<bool> FullClient::updateLastBreakfastTimeProperty(std::chrono::time_point<std::chrono::system_clock> timestamp) const
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/{}/property/lastBreakfastTime/setValue", buf.GetString(), 1, false, mqttProps);
}

void FullClient::_receiveLastBirthdaysPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion)
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
        throw std::runtime_error("Received last_birthdays payload is not an object");
    }
    LastBirthdaysProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("mom");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dad");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("sister");
        if (itr != doc.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            tempValue.sister = boost::none;
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

            cb(tempValue.mom, tempValue.dad, tempValue.sister);
        }
    }
}

boost::optional<LastBirthdaysProperty> FullClient::getLastBirthdaysProperty() const
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
    return _lastBirthdaysProperty;
}

void FullClient::registerLastBirthdaysPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, boost::optional<std::chrono::time_point<std::chrono::system_clock>> sister)>& cb)
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyCallbacksMutex);
    _lastBirthdaysPropertyCallbacks.push_back(cb);
}

boost::future<bool> FullClient::updateLastBirthdaysProperty(std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, boost::optional<std::chrono::time_point<std::chrono::system_clock>> sister) const
{
    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/{}/property/lastBirthdays/setValue", buf.GetString(), 1, false, mqttProps);
}
