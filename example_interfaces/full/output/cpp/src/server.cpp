

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

    _favoriteNumberPropertySubscriptionId = _broker->Subscribe("full/property/favoriteNumber/setValue", 1);

    _favoriteFoodsPropertySubscriptionId = _broker->Subscribe("full/property/favoriteFoods/setValue", 1);

    _lunchMenuPropertySubscriptionId = _broker->Subscribe("full/property/lunchMenu/setValue", 1);
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

boost::optional<struct FavoriteFoodsProperty> FullServer::getFavoriteFoodsProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
    return _favoriteFoodsProperty;
}

void FullServer::registerFavoriteFoodsPropertyCallback(const std::function<void(const std::string& drink, int slices_of_pizza, boost::optional<std::string> breakfast)>& cb)
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyCallbacksMutex);
    _favoriteFoodsPropertyCallbacks.push_back(cb);
}

boost::optional<struct LunchMenuProperty> FullServer::getLunchMenuProperty() const
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
    return _lunchMenuProperty;
}

void FullServer::registerLunchMenuPropertyCallback(const std::function<void(Lunch monday, Lunch tuesday)>& cb)
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyCallbacksMutex);
    _lunchMenuPropertyCallbacks.push_back(cb);
}
