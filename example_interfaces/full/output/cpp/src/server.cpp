
#include <vector>
#include <iostream>
#include <syslog.h>

#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "server.hpp"
#include "method_payloads.hpp"
#include "enums.hpp"
#include <stinger/utils/iconnection.hpp>
#include <stinger/utils/format.hpp>
#include <stinger/error/return_codes.hpp>

namespace stinger {

namespace gen {
namespace full {

constexpr const char FullServer::NAME[];
constexpr const char FullServer::INTERFACE_VERSION[];

FullServer::FullServer(std::shared_ptr<stinger::utils::IConnection> broker, const std::string& instanceId, const std::string& prefix):
    _broker(broker), _instanceId(instanceId), _advertisementThreadRunning(false), _prefixTopicParam(prefix)

{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const stinger::mqtt::Message& msg
                                                               )
                                                               {
                                                                   _receiveMessage(msg);
                                                               });

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["prefix"] = _prefixTopicParam;

    _addNumbersMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/method/addNumbers/request", topicArgs), 2);
    _doSomethingMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/method/doSomething/request", topicArgs), 2);
    _whatTimeIsItMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/method/what_time_is_it/request", topicArgs), 2);
    _holdTemperatureMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/method/hold_temperature/request", topicArgs), 2);

    _favoriteNumberPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/favorite_number/update", topicArgs), 1);
    _favoriteFoodsPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/favorite_foods/update", topicArgs), 1);
    _lunchMenuPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/lunch_menu/update", topicArgs), 1);
    _familyNamePropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/family_name/update", topicArgs), 1);
    _lastBreakfastTimePropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/last_breakfast_time/update", topicArgs), 1);
    _lastBirthdaysPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/last_birthdays/update", topicArgs), 1);

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&FullServer::_advertisementThreadLoop, this);
}

FullServer::~FullServer()
{
    // Unregister the message callback from the broker.
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }

    // Stop the advertisement thread
    _advertisementThreadRunning = false;
    if (_advertisementThread.joinable()) {
        _advertisementThread.join();
    }

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["prefix"] = _prefixTopicParam;

    std::string topic = stinger::utils::format("{prefix}/Full/{service_id}/interface", topicArgs);
    auto msg = stinger::mqtt::Message::ServiceOffline(topic);
    _broker->Publish(msg);

    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/method/addNumbers/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/method/doSomething/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/method/what_time_is_it/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/method/hold_temperature/request", topicArgs));

    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/favorite_number/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/favorite_foods/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/lunch_menu/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/family_name/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/last_breakfast_time/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/last_birthdays/update", topicArgs));
}

void FullServer::_receiveMessage(const stinger::mqtt::Message& msg)
{
    const int noSubId = -1;
    int subscriptionId = msg.properties.subscriptionId.value_or(noSubId);

    if (subscriptionId == _addNumbersMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as addNumbers method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_addNumbersHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callAddNumbersHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _doSomethingMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as doSomething method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_doSomethingHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callDoSomethingHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _whatTimeIsItMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as what_time_is_it method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_whatTimeIsItHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callWhatTimeIsItHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _holdTemperatureMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as hold_temperature method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_holdTemperatureHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callHoldTemperatureHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    if (subscriptionId == _favoriteNumberPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as favorite_number property update.", msg.topic.c_str());
        _receiveFavoriteNumberPropertyUpdate(msg);
    }

    else if (subscriptionId == _favoriteFoodsPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as favorite_foods property update.", msg.topic.c_str());
        _receiveFavoriteFoodsPropertyUpdate(msg);
    }

    else if (subscriptionId == _lunchMenuPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as lunch_menu property update.", msg.topic.c_str());
        _receiveLunchMenuPropertyUpdate(msg);
    }

    else if (subscriptionId == _familyNamePropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as family_name property update.", msg.topic.c_str());
        _receiveFamilyNamePropertyUpdate(msg);
    }

    else if (subscriptionId == _lastBreakfastTimePropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as last_breakfast_time property update.", msg.topic.c_str());
        _receiveLastBreakfastTimePropertyUpdate(msg);
    }

    else if (subscriptionId == _lastBirthdaysPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as last_birthdays property update.", msg.topic.c_str());
        _receiveLastBirthdaysPropertyUpdate(msg);
    }
}

std::future<bool> FullServer::emitTodayIsSignal(int dayOfMonth, DayOfTheWeek dayOfWeek)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("dayOfMonth", dayOfMonth, doc.GetAllocator());

    doc.AddMember("dayOfWeek", static_cast<int>(dayOfWeek), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "todayIs";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/Full/{service_id}/signal/todayIs", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> FullServer::emitRandomWordSignal(std::string word, std::chrono::time_point<std::chrono::system_clock> time)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(word.c_str(), word.size(), doc.GetAllocator());
        doc.AddMember("word", tempStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTimeStringValue;
        std::string timeIsoString = stinger::utils::timePointToIsoString(time);
        tempTimeStringValue.SetString(timeIsoString.c_str(), timeIsoString.size(), doc.GetAllocator());
        doc.AddMember("time", tempTimeStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "randomWord";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/Full/{service_id}/signal/randomWord", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

void FullServer::registerAddNumbersHandler(std::function<int(int, int, std::optional<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _addNumbersHandler = func;
}

void FullServer::registerDoSomethingHandler(std::function<DoSomethingReturnValues(std::string)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _doSomethingHandler = func;
}

void FullServer::registerWhatTimeIsItHandler(std::function<std::chrono::time_point<std::chrono::system_clock>()> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _whatTimeIsItHandler = func;
}

void FullServer::registerHoldTemperatureHandler(std::function<bool(double)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _holdTemperatureHandler = func;
}

void FullServer::_callAddNumbersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to addNumbers");
    if (!_addNumbersHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = AddNumbersRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _addNumbersHandler(requestArgs.first, requestArgs.second, requestArgs.third);
    AddNumbersReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void FullServer::_callDoSomethingHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to doSomething");
    if (!_doSomethingHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = DoSomethingRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _doSomethingHandler(requestArgs.taskToDo);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void FullServer::_callWhatTimeIsItHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to what_time_is_it");
    if (!_whatTimeIsItHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    // Method has a single return value.
    auto returnValue = _whatTimeIsItHandler();
    WhatTimeIsItReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void FullServer::_callHoldTemperatureHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to hold_temperature");
    if (!_holdTemperatureHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = HoldTemperatureRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _holdTemperatureHandler(requestArgs.temperatureCelsius);
    HoldTemperatureReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

std::optional<int> FullServer::getFavoriteNumberProperty()
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
    if (_favoriteNumberProperty) {
        return _favoriteNumberProperty->number;
    }
    return std::nullopt;
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
        _favoriteNumberProperty = FavoriteNumberProperty{ number };
        _lastFavoriteNumberPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteNumberPropertyCallbacksMutex);
        for (const auto& cb: _favoriteNumberPropertyCallbacks) {
            cb(number);
        }
    }
    republishFavoriteNumberProperty();
}

void FullServer::republishFavoriteNumberProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
    rapidjson::Document doc;
    if (_favoriteNumberProperty) {
        doc.SetObject();
        _favoriteNumberProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "favorite_number";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/Full/{service_id}/property/favorite_number/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastFavoriteNumberPropertyVersion);
    _broker->Publish(msg);
}

void FullServer::_receiveFavoriteNumberPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse favorite_number property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received favorite_number payload is not an object or null");
    }

    // TODO: Check _lastFavoriteNumberPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    FavoriteNumberProperty tempValue = FavoriteNumberProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteNumberPropertyMutex);
        _favoriteNumberProperty = tempValue;
        _lastFavoriteNumberPropertyVersion++;
    }
    republishFavoriteNumberProperty();
}

std::optional<FavoriteFoodsProperty> FullServer::getFavoriteFoodsProperty()
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
    if (_favoriteFoodsProperty) {
        return *_favoriteFoodsProperty;
    }
    return std::nullopt;
}

void FullServer::registerFavoriteFoodsPropertyCallback(const std::function<void(std::string drink, int slicesOfPizza, std::optional<std::string> breakfast)>& cb)
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyCallbacksMutex);
    _favoriteFoodsPropertyCallbacks.push_back(cb);
}

void FullServer::updateFavoriteFoodsProperty(std::string drink, int slicesOfPizza, std::optional<std::string> breakfast)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
        _favoriteFoodsProperty = FavoriteFoodsProperty{ drink, slicesOfPizza, breakfast };
        _lastFavoriteFoodsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyCallbacksMutex);
        for (const auto& cb: _favoriteFoodsPropertyCallbacks) {
            cb(drink, slicesOfPizza, breakfast);
        }
    }
    republishFavoriteFoodsProperty();
}

void FullServer::republishFavoriteFoodsProperty() const
{
    std::lock_guard<std::mutex> lock(_favoriteFoodsPropertyMutex);
    rapidjson::Document doc;
    if (_favoriteFoodsProperty) {
        doc.SetObject();
        _favoriteFoodsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "favorite_foods";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/Full/{service_id}/property/favorite_foods/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastFavoriteFoodsPropertyVersion);
    _broker->Publish(msg);
}

void FullServer::_receiveFavoriteFoodsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse favorite_foods property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
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

std::optional<LunchMenuProperty> FullServer::getLunchMenuProperty()
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
    if (_lunchMenuProperty) {
        return *_lunchMenuProperty;
    }
    return std::nullopt;
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
        for (const auto& cb: _lunchMenuPropertyCallbacks) {
            cb(monday, tuesday);
        }
    }
    republishLunchMenuProperty();
}

void FullServer::republishLunchMenuProperty() const
{
    std::lock_guard<std::mutex> lock(_lunchMenuPropertyMutex);
    rapidjson::Document doc;
    if (_lunchMenuProperty) {
        doc.SetObject();
        _lunchMenuProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "lunch_menu";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/Full/{service_id}/property/lunch_menu/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastLunchMenuPropertyVersion);
    _broker->Publish(msg);
}

void FullServer::_receiveLunchMenuPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse lunch_menu property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
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

std::optional<std::string> FullServer::getFamilyNameProperty()
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
    if (_familyNameProperty) {
        return _familyNameProperty->familyName;
    }
    return std::nullopt;
}

void FullServer::registerFamilyNamePropertyCallback(const std::function<void(std::string familyName)>& cb)
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyCallbacksMutex);
    _familyNamePropertyCallbacks.push_back(cb);
}

void FullServer::updateFamilyNameProperty(std::string familyName)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
        _familyNameProperty = FamilyNameProperty{ familyName };
        _lastFamilyNamePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_familyNamePropertyCallbacksMutex);
        for (const auto& cb: _familyNamePropertyCallbacks) {
            cb(familyName);
        }
    }
    republishFamilyNameProperty();
}

void FullServer::republishFamilyNameProperty() const
{
    std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
    rapidjson::Document doc;
    if (_familyNameProperty) {
        doc.SetObject();
        _familyNameProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "family_name";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/Full/{service_id}/property/family_name/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastFamilyNamePropertyVersion);
    _broker->Publish(msg);
}

void FullServer::_receiveFamilyNamePropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse family_name property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received family_name payload is not an object or null");
    }

    // TODO: Check _lastFamilyNamePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    FamilyNameProperty tempValue = FamilyNameProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_familyNamePropertyMutex);
        _familyNameProperty = tempValue;
        _lastFamilyNamePropertyVersion++;
    }
    republishFamilyNameProperty();
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> FullServer::getLastBreakfastTimeProperty()
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
    if (_lastBreakfastTimeProperty) {
        return _lastBreakfastTimeProperty->timestamp;
    }
    return std::nullopt;
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
        _lastBreakfastTimeProperty = LastBreakfastTimeProperty{ timestamp };
        _lastLastBreakfastTimePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyCallbacksMutex);
        for (const auto& cb: _lastBreakfastTimePropertyCallbacks) {
            cb(timestamp);
        }
    }
    republishLastBreakfastTimeProperty();
}

void FullServer::republishLastBreakfastTimeProperty() const
{
    std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
    rapidjson::Document doc;
    if (_lastBreakfastTimeProperty) {
        doc.SetObject();
        _lastBreakfastTimeProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "last_breakfast_time";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/Full/{service_id}/property/last_breakfast_time/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastLastBreakfastTimePropertyVersion);
    _broker->Publish(msg);
}

void FullServer::_receiveLastBreakfastTimePropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse last_breakfast_time property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received last_breakfast_time payload is not an object or null");
    }

    // TODO: Check _lastLastBreakfastTimePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    LastBreakfastTimeProperty tempValue = LastBreakfastTimeProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBreakfastTimePropertyMutex);
        _lastBreakfastTimeProperty = tempValue;
        _lastLastBreakfastTimePropertyVersion++;
    }
    republishLastBreakfastTimeProperty();
}

std::optional<LastBirthdaysProperty> FullServer::getLastBirthdaysProperty()
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
    if (_lastBirthdaysProperty) {
        return *_lastBirthdaysProperty;
    }
    return std::nullopt;
}

void FullServer::registerLastBirthdaysPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, std::optional<std::chrono::time_point<std::chrono::system_clock>> sister, std::optional<int> brothersAge)>& cb)
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyCallbacksMutex);
    _lastBirthdaysPropertyCallbacks.push_back(cb);
}

void FullServer::updateLastBirthdaysProperty(std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, std::optional<std::chrono::time_point<std::chrono::system_clock>> sister, std::optional<int> brothersAge)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
        _lastBirthdaysProperty = LastBirthdaysProperty{ mom, dad, sister, brothersAge };
        _lastLastBirthdaysPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyCallbacksMutex);
        for (const auto& cb: _lastBirthdaysPropertyCallbacks) {
            cb(mom, dad, sister, brothersAge);
        }
    }
    republishLastBirthdaysProperty();
}

void FullServer::republishLastBirthdaysProperty() const
{
    std::lock_guard<std::mutex> lock(_lastBirthdaysPropertyMutex);
    rapidjson::Document doc;
    if (_lastBirthdaysProperty) {
        doc.SetObject();
        _lastBirthdaysProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "last_birthdays";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/Full/{service_id}/property/last_birthdays/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastLastBirthdaysPropertyVersion);
    _broker->Publish(msg);
}

void FullServer::_receiveLastBirthdaysPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse last_birthdays property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
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
    while (_advertisementThreadRunning) {
        // Get current timestamp
        auto now = std::chrono::system_clock::now();
        std::string timestamp = stinger::utils::timePointToIsoString(now);

        // Build JSON message
        rapidjson::Document doc;
        doc.SetObject();
        rapidjson::Document::AllocatorType& allocator = doc.GetAllocator();

        doc.AddMember("interface_name", rapidjson::Value("Full", allocator), allocator);
        doc.AddMember("instance", rapidjson::Value(_instanceId.c_str(), allocator), allocator);
        doc.AddMember("title", rapidjson::Value("Example Interface", allocator), allocator);
        doc.AddMember("version", rapidjson::Value("0.0.2", allocator), allocator);
        doc.AddMember("connection_topic", rapidjson::Value(_broker->GetOnlineTopic().c_str(), allocator), allocator);
        doc.AddMember("timestamp", rapidjson::Value(timestamp.c_str(), allocator), allocator);

        doc.AddMember("prefix", rapidjson::Value(_prefixTopicParam.c_str(), allocator), allocator);

        // Convert to JSON string
        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        doc.Accept(writer);

        std::map<std::string, std::string> topicArgs;
        topicArgs["service_id"] = _instanceId;
        topicArgs["interface_name"] = NAME;
        topicArgs["client_id"] = _broker->GetClientId();
        topicArgs["prefix"] = _prefixTopicParam;

        // Publish to "{prefix}/Full/{service_id}/interface"
        std::string topic = stinger::utils::format("{prefix}/Full/{service_id}/interface", topicArgs);
        auto msg = stinger::mqtt::Message::ServiceOnline(topic, buf.GetString(), 120);
        _broker->Publish(msg);

        _broker->Log(LOG_INFO, "Published service advertisement to %s", topic.c_str());

        // Wait for 120 seconds or until thread should stop
        // Use smaller sleep intervals to allow quick shutdown
        for (int i = 0; i < 120 && _advertisementThreadRunning; ++i) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
}

} // namespace full

} // namespace gen

} // namespace stinger
