

#include <vector>
#include <iostream>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>

#include "server.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"

constexpr const char FullServer::NAME[];
constexpr const char FullServer::INTERFACE_VERSION[];

FullServer::FullServer(std::shared_ptr<IBrokerConnection> broker)
    : _broker(broker)
{
    _broker->AddMessageCallback([this](
                                        const std::string& topic,
                                        const std::string& payload,
                                        const MqttProperties& mqttProps
                                )
                                { _receiveMessage(topic, payload, mqttProps); });

    _addNumbersMethodSubscriptionId = _broker->Subscribe("full/method/addNumbers", 2);
    _doSomethingMethodSubscriptionId = _broker->Subscribe("full/method/doSomething", 2);
    _echoMethodSubscriptionId = _broker->Subscribe("full/method/echo", 2);

    _favoriteNumberPropertySubscriptionId = _broker->Subscribe("full/property/favoriteNumber/setValue", 1);
    _favoriteFoodsPropertySubscriptionId = _broker->Subscribe("full/property/favoriteFoods/setValue", 1);
    _lunchMenuPropertySubscriptionId = _broker->Subscribe("full/property/lunchMenu/setValue", 1);
    _familyNamePropertySubscriptionId = _broker->Subscribe("full/property/familyName/setValue", 1);
}

void FullServer::_receiveMessage(
        const std::string& topic,
        const std::string& payload,
        const MqttProperties& mqttProps
)
{
    int subscriptionId = mqttProps.subscriptionId.value_or(-1);

    if ((subscriptionId == _addNumbersMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "full/method/addNumbers"))
    {
        std::cout << "Message matched topic full/method/addNumbers\n";
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

    else if ((subscriptionId == _doSomethingMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "full/method/doSomething"))
    {
        std::cout << "Message matched topic full/method/doSomething\n";
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

    else if ((subscriptionId == _echoMethodSubscriptionId) || _broker->TopicMatchesSubscription(topic, "full/method/echo"))
    {
        std::cout << "Message matched topic full/method/echo\n";
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

    if (subscriptionId == _favoriteNumberPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "full/property/favoriteNumber/setValue"))
    {
        std::cout << "Message matched topic full/property/favoriteNumber/setValue\n";
        _receiveFavoriteNumberPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _favoriteFoodsPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "full/property/favoriteFoods/setValue"))
    {
        std::cout << "Message matched topic full/property/favoriteFoods/setValue\n";
        _receiveFavoriteFoodsPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _lunchMenuPropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "full/property/lunchMenu/setValue"))
    {
        std::cout << "Message matched topic full/property/lunchMenu/setValue\n";
        _receiveLunchMenuPropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }

    else if (subscriptionId == _familyNamePropertySubscriptionId || _broker->TopicMatchesSubscription(topic, "full/property/familyName/setValue"))
    {
        std::cout << "Message matched topic full/property/familyName/setValue\n";
        _receiveFamilyNamePropertyUpdate(topic, payload, mqttProps.propertyVersion);
    }
}

boost::future<bool> FullServer::emitTodayIsSignal(int dayOfMonth, boost::optional<DayOfTheWeek> dayOfWeek)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("dayOfMonth", dayOfMonth, doc.GetAllocator());

    doc.AddMember("dayOfWeek", static_cast<int>(*dayOfWeek), doc.GetAllocator());
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/signal/todayIs", buf.GetString(), 1, false, mqttProps);
}

boost::future<bool> FullServer::emitBarkSignal(const std::string& word)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(word.c_str(), word.size(), doc.GetAllocator());
        doc.AddMember("word", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    MqttProperties mqttProps;
    return _broker->Publish("full/signal/bark", buf.GetString(), 1, false, mqttProps);
}

void FullServer::registerAddNumbersHandler(std::function<int(int, int, boost::optional<int>)> func)
{
    std::cout << "Registered method to handle full/method/addNumbers\n";
    _addNumbersHandler = func;
}

void FullServer::registerDoSomethingHandler(std::function<DoSomethingReturnValue(const std::string&)> func)
{
    std::cout << "Registered method to handle full/method/doSomething\n";
    _doSomethingHandler = func;
}

void FullServer::registerEchoHandler(std::function<std::string(const std::string&)> func)
{
    std::cout << "Registered method to handle full/method/echo\n";
    _echoHandler = func;
}

void FullServer::_callAddNumbersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic
) const
{
    std::cout << "Handling call to addNumbers\n";
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
            mqttProps.resultCode = MethodResultCode::SUCCESS;
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
    std::cout << "Handling call to doSomething\n";
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
            mqttProps.resultCode = MethodResultCode::SUCCESS;
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
    std::cout << "Handling call to echo\n";
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
            mqttProps.resultCode = MethodResultCode::SUCCESS;
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
    _broker->Publish("full/property/favoriteNumber/value", buf.GetString(), 1, false, mqttProps);
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
    _broker->Publish("full/property/favoriteFoods/value", buf.GetString(), 1, false, mqttProps);
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
    _broker->Publish("full/property/lunchMenu/value", buf.GetString(), 1, false, mqttProps);
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
    _broker->Publish("full/property/familyName/value", buf.GetString(), 1, false, mqttProps);
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
