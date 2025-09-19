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

    virtual ~FullServer() = default;

    boost::future<bool> emitTodayIsSignal(int, boost::optional<DayOfTheWeek>);

    void registerAddNumbersHandler(std::function<int(int, int, boost::optional<int>)> func);

    void registerDoSomethingHandler(std::function<DoSomethingReturnValue(const std::string&)> func);

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

private:
    std::shared_ptr<IBrokerConnection> _broker;
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
};