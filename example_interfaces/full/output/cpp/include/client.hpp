/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once

#include <cstdint>
#include <functional>
#include <map>
#include <memory>
#include <exception>
#include <mutex>
#include <chrono>
#include <rapidjson/document.h>
#include <stinger/utils/mqttproperties.hpp>
#include <stinger/utils/iconnection.hpp>
#include <stinger/error/return_codes.hpp>
#include "enums.hpp"
#include "method_payloads.hpp"
#include "signal_payloads.hpp"
#include "discovery.hpp"

#include "property_structs.hpp"

namespace stinger {

namespace gen {
namespace full {

class FullClient {
public:
    // This is the name of the API.
    static constexpr const char NAME[] = "Full";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.0.2";

    // Constructor taking a connection object.
    FullClient(std::shared_ptr<stinger::utils::IConnection> broker, const InstanceInfo& instanceInfo);

    virtual ~FullClient();
    // ------------------ SIGNALS --------------------

    // Register a callback for the `todayIs` signal.
    // The provided method will be called whenever a `todayIs` is received.
    void registerTodayIsCallback(const std::function<void(int, DayOfTheWeek)>& cb);

    // Register a callback for the `randomWord` signal.
    // The provided method will be called whenever a `randomWord` is received.
    void registerRandomWordCallback(const std::function<void(std::string, std::chrono::time_point<std::chrono::system_clock>)>& cb);

    // ------------------- METHODS --------------------

    // Calls the `addNumbers` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgPrimitive name=sum type=int>
    std::future<int> addNumbers(int first, int second, std::optional<int> third);

    // Calls the `doSomething` method.
    // Returns a future.  When that future resolves, it will have the returned value. [<ArgPrimitive name=label type=str>, <ArgPrimitive name=identifier type=int>]
    std::future<DoSomethingReturnValues> doSomething(std::string task_to_do);

    // Calls the `what_time_is_it` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgDateTime name=timestamp>
    std::future<std::chrono::time_point<std::chrono::system_clock>> whatTimeIsIt();

    // Calls the `hold_temperature` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgPrimitive name=success type=bool>
    std::future<bool> holdTemperature(double temperature_celsius);

    // ---------------- PROPERTIES ------------------

    // ---favorite_number Property---

    // Gets the latest value of the `favorite_number` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<int> getFavoriteNumberProperty();

    // Add a callback that will be called whenever the `favorite_number` property is updated.
    // The provided method will be called whenever a new value for the `favorite_number` property is received.
    void registerFavoriteNumberPropertyCallback(const std::function<void(int)>& cb);

    std::future<bool> updateFavoriteNumberProperty(int) const;

    // ---favorite_foods Property---

    // Gets the latest value of the `favorite_foods` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<FavoriteFoodsProperty> getFavoriteFoodsProperty();

    // Add a callback that will be called whenever the `favorite_foods` property is updated.
    // The provided method will be called whenever a new value for the `favorite_foods` property is received.
    void registerFavoriteFoodsPropertyCallback(const std::function<void(std::string, int, std::optional<std::string>)>& cb);

    std::future<bool> updateFavoriteFoodsProperty(std::string, int, std::optional<std::string>) const;

    // ---lunch_menu Property---

    // Gets the latest value of the `lunch_menu` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<LunchMenuProperty> getLunchMenuProperty();

    // Add a callback that will be called whenever the `lunch_menu` property is updated.
    // The provided method will be called whenever a new value for the `lunch_menu` property is received.
    void registerLunchMenuPropertyCallback(const std::function<void(Lunch, Lunch)>& cb);

    // ---family_name Property---

    // Gets the latest value of the `family_name` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::string> getFamilyNameProperty();

    // Add a callback that will be called whenever the `family_name` property is updated.
    // The provided method will be called whenever a new value for the `family_name` property is received.
    void registerFamilyNamePropertyCallback(const std::function<void(std::string)>& cb);

    std::future<bool> updateFamilyNameProperty(std::string) const;

    // ---last_breakfast_time Property---

    // Gets the latest value of the `last_breakfast_time` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::chrono::time_point<std::chrono::system_clock>> getLastBreakfastTimeProperty();

    // Add a callback that will be called whenever the `last_breakfast_time` property is updated.
    // The provided method will be called whenever a new value for the `last_breakfast_time` property is received.
    void registerLastBreakfastTimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb);

    std::future<bool> updateLastBreakfastTimeProperty(std::chrono::time_point<std::chrono::system_clock>) const;

    // ---last_birthdays Property---

    // Gets the latest value of the `last_birthdays` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<LastBirthdaysProperty> getLastBirthdaysProperty();

    // Add a callback that will be called whenever the `last_birthdays` property is updated.
    // The provided method will be called whenever a new value for the `last_birthdays` property is received.
    void registerLastBirthdaysPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>, std::optional<int>)>& cb);

    std::future<bool> updateLastBirthdaysProperty(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>, std::optional<int>) const;

private:
    // Pointer to the broker connection.
    std::shared_ptr<stinger::utils::IConnection> _broker;

    // Service Instance ID that this client is connected to.
    std::string _instanceId;
    InstanceInfo _instanceInfo;

    stinger::utils::CallbackHandleType _brokerMessageCallbackHandle = 0;

    // Internal method for receiving messages from the broker.
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const stinger::utils::MqttProperties& mqttProps
    );

    // ------------------ SIGNALS --------------------

    // List of callbacks to be called whenever the `todayIs` signal is received.
    std::vector<std::function<void(int, DayOfTheWeek)>> _todayIsSignalCallbacks;
    std::mutex _todayIsSignalCallbacksMutex;

    // MQTT Subscription ID for `todayIs` signal receptions.
    int _todayIsSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `randomWord` signal is received.
    std::vector<std::function<void(std::string, std::chrono::time_point<std::chrono::system_clock>)>> _randomWordSignalCallbacks;
    std::mutex _randomWordSignalCallbacksMutex;

    // MQTT Subscription ID for `randomWord` signal receptions.
    int _randomWordSignalSubscriptionId = -1;

    // ------------------- METHODS --------------------
    // Holds promises for pending `addNumbers` method calls.
    std::map<std::vector<std::byte>, std::promise<int>> _pendingAddNumbersMethodCalls;
    int _addNumbersMethodSubscriptionId = -1;
    // This is called internally to process responses to `addNumbers` method calls.
    void _handleAddNumbersResponse(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps);

    // Holds promises for pending `doSomething` method calls.
    std::map<std::vector<std::byte>, std::promise<DoSomethingReturnValues>> _pendingDoSomethingMethodCalls;
    int _doSomethingMethodSubscriptionId = -1;
    // This is called internally to process responses to `doSomething` method calls.
    void _handleDoSomethingResponse(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps);

    // Holds promises for pending `what_time_is_it` method calls.
    std::map<std::vector<std::byte>, std::promise<std::chrono::time_point<std::chrono::system_clock>>> _pendingWhatTimeIsItMethodCalls;
    int _whatTimeIsItMethodSubscriptionId = -1;
    // This is called internally to process responses to `what_time_is_it` method calls.
    void _handleWhatTimeIsItResponse(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps);

    // Holds promises for pending `hold_temperature` method calls.
    std::map<std::vector<std::byte>, std::promise<bool>> _pendingHoldTemperatureMethodCalls;
    int _holdTemperatureMethodSubscriptionId = -1;
    // This is called internally to process responses to `hold_temperature` method calls.
    void _handleHoldTemperatureResponse(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps);

    // ---------------- PROPERTIES ------------------

    // ---favorite_number Property---

    // Last received value for the `favorite_number` property.
    std::optional<FavoriteNumberProperty> _favoriteNumberProperty;

    // This is the property version of the last received `favorite_number` property update.
    int _lastFavoriteNumberPropertyVersion = -1;

    // Mutex for protecting access to the `favorite_number` property and its version.
    mutable std::mutex _favoriteNumberPropertyMutex;

    // MQTT Subscription ID for `favorite_number` property updates.
    int _favoriteNumberPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `favorite_number` property.
    void _receiveFavoriteNumberPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `favorite_number` property.
    std::vector<std::function<void(int)>> _favoriteNumberPropertyCallbacks;
    std::mutex _favoriteNumberPropertyCallbacksMutex;

    // ---favorite_foods Property---

    // Last received values for the `favorite_foods` property.
    std::optional<FavoriteFoodsProperty> _favoriteFoodsProperty;

    // This is the property version of the last received `favorite_foods` property update.
    int _lastFavoriteFoodsPropertyVersion = -1;

    // Mutex for protecting access to the `favorite_foods` property and its version.
    mutable std::mutex _favoriteFoodsPropertyMutex;

    // MQTT Subscription ID for `favorite_foods` property updates.
    int _favoriteFoodsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `favorite_foods` property.
    void _receiveFavoriteFoodsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `favorite_foods` property.
    std::vector<std::function<void(std::string, int, std::optional<std::string>)>> _favoriteFoodsPropertyCallbacks;
    std::mutex _favoriteFoodsPropertyCallbacksMutex;

    // ---lunch_menu Property---

    // Last received values for the `lunch_menu` property.
    std::optional<LunchMenuProperty> _lunchMenuProperty;

    // This is the property version of the last received `lunch_menu` property update.
    int _lastLunchMenuPropertyVersion = -1;

    // Mutex for protecting access to the `lunch_menu` property and its version.
    mutable std::mutex _lunchMenuPropertyMutex;

    // MQTT Subscription ID for `lunch_menu` property updates.
    int _lunchMenuPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `lunch_menu` property.
    void _receiveLunchMenuPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `lunch_menu` property.
    std::vector<std::function<void(Lunch, Lunch)>> _lunchMenuPropertyCallbacks;
    std::mutex _lunchMenuPropertyCallbacksMutex;

    // ---family_name Property---

    // Last received value for the `family_name` property.
    std::optional<FamilyNameProperty> _familyNameProperty;

    // This is the property version of the last received `family_name` property update.
    int _lastFamilyNamePropertyVersion = -1;

    // Mutex for protecting access to the `family_name` property and its version.
    mutable std::mutex _familyNamePropertyMutex;

    // MQTT Subscription ID for `family_name` property updates.
    int _familyNamePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `family_name` property.
    void _receiveFamilyNamePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `family_name` property.
    std::vector<std::function<void(std::string)>> _familyNamePropertyCallbacks;
    std::mutex _familyNamePropertyCallbacksMutex;

    // ---last_breakfast_time Property---

    // Last received value for the `last_breakfast_time` property.
    std::optional<LastBreakfastTimeProperty> _lastBreakfastTimeProperty;

    // This is the property version of the last received `last_breakfast_time` property update.
    int _lastLastBreakfastTimePropertyVersion = -1;

    // Mutex for protecting access to the `last_breakfast_time` property and its version.
    mutable std::mutex _lastBreakfastTimePropertyMutex;

    // MQTT Subscription ID for `last_breakfast_time` property updates.
    int _lastBreakfastTimePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `last_breakfast_time` property.
    void _receiveLastBreakfastTimePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `last_breakfast_time` property.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>)>> _lastBreakfastTimePropertyCallbacks;
    std::mutex _lastBreakfastTimePropertyCallbacksMutex;

    // ---last_birthdays Property---

    // Last received values for the `last_birthdays` property.
    std::optional<LastBirthdaysProperty> _lastBirthdaysProperty;

    // This is the property version of the last received `last_birthdays` property update.
    int _lastLastBirthdaysPropertyVersion = -1;

    // Mutex for protecting access to the `last_birthdays` property and its version.
    mutable std::mutex _lastBirthdaysPropertyMutex;

    // MQTT Subscription ID for `last_birthdays` property updates.
    int _lastBirthdaysPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `last_birthdays` property.
    void _receiveLastBirthdaysPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `last_birthdays` property.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>, std::optional<int>)>> _lastBirthdaysPropertyCallbacks;
    std::mutex _lastBirthdaysPropertyCallbacksMutex;
};

} // namespace full

} // namespace gen

} // namespace stinger
