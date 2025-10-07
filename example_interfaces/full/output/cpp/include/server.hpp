/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/

#pragma once

#include <cstdint>
#include <functional>
#include <map>
#include <string>
#include <memory>
#include <exception>
#include <mutex>
#include <chrono>
#include <boost/optional.hpp>
#include <rapidjson/document.h>

#include "property_structs.hpp"

#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "return_types.hpp"

class FullServer
{
public:
    static constexpr const char NAME[] = "Full";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    FullServer(std::shared_ptr<IBrokerConnection> broker);

    virtual ~FullServer();

    boost::future<bool> emitTodayIsSignal(int, boost::optional<DayOfTheWeek>, std::chrono::time_point<std::chrono::system_clock>, std::chrono::duration<double>, std::vector<uint8_t>);

    void registerAddNumbersHandler(std::function<int(int, int, boost::optional<int>)> func);

    void registerDoSomethingHandler(std::function<DoSomethingReturnValue(const std::string&)> func);

    void registerEchoHandler(std::function<std::string(const std::string&)> func);

    void registerWhatTimeIsItHandler(std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::time_point<std::chrono::system_clock>)> func);

    void registerSetTheTimeHandler(std::function<SetTheTimeReturnValue(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>)> func);

    void registerForwardTimeHandler(std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::duration<double>)> func);

    void registerHowOffIsTheClockHandler(std::function<std::chrono::duration<double>(std::chrono::time_point<std::chrono::system_clock>)> func);

    // ---favorite_number Property---

    // Gets the latest value of the `favorite_number` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<FavoriteNumberProperty> getFavoriteNumberProperty() const;

    // Add a callback that will be called whenever the `favorite_number` property is updated.
    // The provided method will be called whenever a new value for the `favorite_number` property is received.
    void registerFavoriteNumberPropertyCallback(const std::function<void(int)>& cb);

    void updateFavoriteNumberProperty(int);

    void republishFavoriteNumberProperty() const;

    // ---favorite_foods Property---

    // Gets the latest value of the `favorite_foods` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<FavoriteFoodsProperty> getFavoriteFoodsProperty() const;

    // Add a callback that will be called whenever the `favorite_foods` property is updated.
    // The provided method will be called whenever a new value for the `favorite_foods` property is received.
    void registerFavoriteFoodsPropertyCallback(const std::function<void(const std::string&, int, boost::optional<std::string>)>& cb);

    void updateFavoriteFoodsProperty(const std::string&, int, boost::optional<std::string>);

    void republishFavoriteFoodsProperty() const;

    // ---lunch_menu Property---

    // Gets the latest value of the `lunch_menu` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<LunchMenuProperty> getLunchMenuProperty() const;

    // Add a callback that will be called whenever the `lunch_menu` property is updated.
    // The provided method will be called whenever a new value for the `lunch_menu` property is received.
    void registerLunchMenuPropertyCallback(const std::function<void(Lunch, Lunch)>& cb);

    void updateLunchMenuProperty(Lunch, Lunch);

    void republishLunchMenuProperty() const;

    // ---family_name Property---

    // Gets the latest value of the `family_name` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<FamilyNameProperty> getFamilyNameProperty() const;

    // Add a callback that will be called whenever the `family_name` property is updated.
    // The provided method will be called whenever a new value for the `family_name` property is received.
    void registerFamilyNamePropertyCallback(const std::function<void(const std::string&)>& cb);

    void updateFamilyNameProperty(const std::string&);

    void republishFamilyNameProperty() const;

    // ---last_breakfast_time Property---

    // Gets the latest value of the `last_breakfast_time` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<LastBreakfastTimeProperty> getLastBreakfastTimeProperty() const;

    // Add a callback that will be called whenever the `last_breakfast_time` property is updated.
    // The provided method will be called whenever a new value for the `last_breakfast_time` property is received.
    void registerLastBreakfastTimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb);

    void updateLastBreakfastTimeProperty(std::chrono::time_point<std::chrono::system_clock>);

    void republishLastBreakfastTimeProperty() const;

    // ---breakfast_length Property---

    // Gets the latest value of the `breakfast_length` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<BreakfastLengthProperty> getBreakfastLengthProperty() const;

    // Add a callback that will be called whenever the `breakfast_length` property is updated.
    // The provided method will be called whenever a new value for the `breakfast_length` property is received.
    void registerBreakfastLengthPropertyCallback(const std::function<void(std::chrono::duration<double>)>& cb);

    void updateBreakfastLengthProperty(std::chrono::duration<double>);

    void republishBreakfastLengthProperty() const;

    // ---last_birthdays Property---

    // Gets the latest value of the `last_birthdays` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<LastBirthdaysProperty> getLastBirthdaysProperty() const;

    // Add a callback that will be called whenever the `last_birthdays` property is updated.
    // The provided method will be called whenever a new value for the `last_birthdays` property is received.
    void registerLastBirthdaysPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>, boost::optional<int>)>& cb);

    void updateLastBirthdaysProperty(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>, boost::optional<int>);

    void republishLastBirthdaysProperty() const;

private:
    std::shared_ptr<IBrokerConnection> _broker;
    CallbackHandleType _brokerMessageCallbackHandle = 0;
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const MqttProperties& mqttProps
    );

    void _callAddNumbersHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<int(int, int, boost::optional<int>)> _addNumbersHandler;
    int _addNumbersMethodSubscriptionId;

    void _callDoSomethingHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<DoSomethingReturnValue(const std::string&)> _doSomethingHandler;
    int _doSomethingMethodSubscriptionId;

    void _callEchoHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<std::string(const std::string&)> _echoHandler;
    int _echoMethodSubscriptionId;

    void _callWhatTimeIsItHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::time_point<std::chrono::system_clock>)> _whatTimeIsItHandler;
    int _whatTimeIsItMethodSubscriptionId;

    void _callSetTheTimeHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<SetTheTimeReturnValue(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>)> _setTheTimeHandler;
    int _setTheTimeMethodSubscriptionId;

    void _callForwardTimeHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::duration<double>)> _forwardTimeHandler;
    int _forwardTimeMethodSubscriptionId;

    void _callHowOffIsTheClockHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const;
    std::function<std::chrono::duration<double>(std::chrono::time_point<std::chrono::system_clock>)> _howOffIsTheClockHandler;
    int _howOffIsTheClockMethodSubscriptionId;

    // ---------------- PROPERTIES ------------------

    // ---favorite_number Property---

    // Current value for the `favorite_number` property.
    boost::optional<FavoriteNumberProperty> _favoriteNumberProperty;

    // This is the property version  of `favorite_number`.
    int _lastFavoriteNumberPropertyVersion = -1;

    // Mutex for protecting access to the `favorite_number` property and its version.
    mutable std::mutex _favoriteNumberPropertyMutex;

    // MQTT Subscription ID for `favorite_number` property update requests.
    int _favoriteNumberPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `favorite_number` property.
    void _receiveFavoriteNumberPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `favorite_number` property.
    std::vector<std::function<void(int)>> _favoriteNumberPropertyCallbacks;
    std::mutex _favoriteNumberPropertyCallbacksMutex;

    // ---favorite_foods Property---

    // Current values for the `favorite_foods` property.
    boost::optional<FavoriteFoodsProperty> _favoriteFoodsProperty;

    // This is the property version  of `favorite_foods`.
    int _lastFavoriteFoodsPropertyVersion = -1;

    // Mutex for protecting access to the `favorite_foods` property and its version.
    mutable std::mutex _favoriteFoodsPropertyMutex;

    // MQTT Subscription ID for `favorite_foods` property update requests.
    int _favoriteFoodsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `favorite_foods` property.
    void _receiveFavoriteFoodsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `favorite_foods` property.
    std::vector<std::function<void(const std::string&, int, boost::optional<std::string>)>> _favoriteFoodsPropertyCallbacks;
    std::mutex _favoriteFoodsPropertyCallbacksMutex;

    // ---lunch_menu Property---

    // Current values for the `lunch_menu` property.
    boost::optional<LunchMenuProperty> _lunchMenuProperty;

    // This is the property version  of `lunch_menu`.
    int _lastLunchMenuPropertyVersion = -1;

    // Mutex for protecting access to the `lunch_menu` property and its version.
    mutable std::mutex _lunchMenuPropertyMutex;

    // MQTT Subscription ID for `lunch_menu` property update requests.
    int _lunchMenuPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `lunch_menu` property.
    void _receiveLunchMenuPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `lunch_menu` property.
    std::vector<std::function<void(Lunch, Lunch)>> _lunchMenuPropertyCallbacks;
    std::mutex _lunchMenuPropertyCallbacksMutex;

    // ---family_name Property---

    // Current value for the `family_name` property.
    boost::optional<FamilyNameProperty> _familyNameProperty;

    // This is the property version  of `family_name`.
    int _lastFamilyNamePropertyVersion = -1;

    // Mutex for protecting access to the `family_name` property and its version.
    mutable std::mutex _familyNamePropertyMutex;

    // MQTT Subscription ID for `family_name` property update requests.
    int _familyNamePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `family_name` property.
    void _receiveFamilyNamePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `family_name` property.
    std::vector<std::function<void(const std::string&)>> _familyNamePropertyCallbacks;
    std::mutex _familyNamePropertyCallbacksMutex;

    // ---last_breakfast_time Property---

    // Current value for the `last_breakfast_time` property.
    boost::optional<LastBreakfastTimeProperty> _lastBreakfastTimeProperty;

    // This is the property version  of `last_breakfast_time`.
    int _lastLastBreakfastTimePropertyVersion = -1;

    // Mutex for protecting access to the `last_breakfast_time` property and its version.
    mutable std::mutex _lastBreakfastTimePropertyMutex;

    // MQTT Subscription ID for `last_breakfast_time` property update requests.
    int _lastBreakfastTimePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `last_breakfast_time` property.
    void _receiveLastBreakfastTimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `last_breakfast_time` property.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>)>> _lastBreakfastTimePropertyCallbacks;
    std::mutex _lastBreakfastTimePropertyCallbacksMutex;

    // ---breakfast_length Property---

    // Current value for the `breakfast_length` property.
    boost::optional<BreakfastLengthProperty> _breakfastLengthProperty;

    // This is the property version  of `breakfast_length`.
    int _lastBreakfastLengthPropertyVersion = -1;

    // Mutex for protecting access to the `breakfast_length` property and its version.
    mutable std::mutex _breakfastLengthPropertyMutex;

    // MQTT Subscription ID for `breakfast_length` property update requests.
    int _breakfastLengthPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `breakfast_length` property.
    void _receiveBreakfastLengthPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `breakfast_length` property.
    std::vector<std::function<void(std::chrono::duration<double>)>> _breakfastLengthPropertyCallbacks;
    std::mutex _breakfastLengthPropertyCallbacksMutex;

    // ---last_birthdays Property---

    // Current values for the `last_birthdays` property.
    boost::optional<LastBirthdaysProperty> _lastBirthdaysProperty;

    // This is the property version  of `last_birthdays`.
    int _lastLastBirthdaysPropertyVersion = -1;

    // Mutex for protecting access to the `last_birthdays` property and its version.
    mutable std::mutex _lastBirthdaysPropertyMutex;

    // MQTT Subscription ID for `last_birthdays` property update requests.
    int _lastBirthdaysPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `last_birthdays` property.
    void _receiveLastBirthdaysPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `last_birthdays` property.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>, boost::optional<int>)>> _lastBirthdaysPropertyCallbacks;
    std::mutex _lastBirthdaysPropertyCallbacksMutex;
};