/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/


#pragma once

#include <cstdint>
#include <functional>
#include <map>
#include <memory>
#include <exception>
#include <mutex>
#include <rapidjson/document.h>
#include <boost/uuid/uuid.hpp>
#include <boost/optional.hpp>
#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "return_types.hpp"



#include "property_structs.hpp"

class FullClient {

public:
    // This is the name of the API.
    static constexpr const char NAME[] = "Full";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    // Constructor taking a connection object.
    FullClient(std::shared_ptr<IBrokerConnection> broker);

    virtual ~FullClient() = default;
    // ------------------ SIGNALS --------------------
    
    // Register a callback for the `todayIs` signal.
    // The provided method will be called whenever a `todayIs` is received.
    void registerTodayIsCallback(const std::function<void(int, boost::optional<DayOfTheWeek>)>& cb);
    
    
    // ------------------- METHODS --------------------
    
    // Calls the `addNumbers` method.
    // Returns a future.  When that future resolves, it will have the returned value.
    boost::future<int> addNumbers(int first, int second, boost::optional<int> third);
    
    // Calls the `doSomething` method.
    // Returns a future.  When that future resolves, it will have the returned value.
    boost::future<DoSomethingReturnValue> doSomething(const std::string& aString);
    
    
    // ---------------- PROPERTIES ------------------
    
    // ---favorite_number Property---

    // Gets the latest value of the `favorite_number` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<FavoriteNumberProperty> getFavoriteNumberProperty() const;

    // Add a callback that will be called whenever the `favorite_number` property is updated.
    // The provided method will be called whenever a new value for the `favorite_number` property is received.
    void registerFavoriteNumberPropertyCallback(const std::function<void(const FavoriteNumberProperty&)>& cb);
    
    // ---favorite_foods Property---

    // Gets the latest value of the `favorite_foods` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<struct FavoriteFoodsProperty> getFavoriteFoodsProperty() const;

    // Add a callback that will be called whenever the `favorite_foods` property is updated.
    // The provided method will be called whenever a new value for the `favorite_foods` property is received.
    void registerFavoriteFoodsPropertyCallback(const std::function<void(const struct FavoriteFoodsProperty&)>& cb);
    
    // ---lunch_menu Property---

    // Gets the latest value of the `lunch_menu` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.
    boost::optional<struct LunchMenuProperty> getLunchMenuProperty() const;

    // Add a callback that will be called whenever the `lunch_menu` property is updated.
    // The provided method will be called whenever a new value for the `lunch_menu` property is received.
    void registerLunchMenuPropertyCallback(const std::function<void(const struct LunchMenuProperty&)>& cb);
    
    
private:

    std::shared_ptr<IBrokerConnection> _broker;
    void _receiveMessage(
            const std::string& topic, 
            const std::string& payload, 
            const boost::optional<std::string> optCorrelationId, 
            const boost::optional<MethodResultCode> optResultCode, 
            const boost::optional<int> optSubscriptionId,
            const boost::optional<int> optPropertyVersion);
    // ------------------ SIGNALS --------------------

    
    // List of callbacks to be called whenever the `todayIs` signal is received.
    std::vector<std::function<void(int, boost::optional<DayOfTheWeek>)>> _todayIsSignalCallbacks;
    std::mutex _todayIsSignalCallbacksMutex;

    // MQTT Subscription ID for `todayIs` signal receptions.
    int _todayIsSignalSubscriptionId;
    
    
    // ------------------- METHODS --------------------
    // Holds promises for pending `` method calls.
    std::map<boost::uuids::uuid, boost::promise<int>> _pendingAddNumbersMethodCalls;

    void _handleAddNumbersResponse(const std::string& topic, const std::string& payload, const std::string& optCorrelationId);
    // Holds promises for pending `` method calls.
    std::map<boost::uuids::uuid, boost::promise<DoSomethingReturnValue>> _pendingDoSomethingMethodCalls;

    void _handleDoSomethingResponse(const std::string& topic, const std::string& payload, const std::string& optCorrelationId);
    
    // ---------------- PROPERTIES ------------------
    

    // ---favorite_number Property---

    // Last received value for the `favorite_number` property.
    boost::optional<FavoriteNumberProperty> _favoriteNumberProperty;
    int _lastFavoriteNumberPropertyVersion = -1;
    std::mutex _favoriteNumberPropertyMutex;
   
    // MQTT Subscription ID for `favorite_number` property updates.
    int _favoriteNumberPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `favorite_number` property.
    void _receiveFavoriteNumberPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `favorite_number` property.
    std::vector<std::function<void(const FavoriteNumberProperty&)>> _favoriteNumberPropertyCallbacks;
    std::mutex _favoriteNumberPropertyCallbacksMutex;
    

    // ---favorite_foods Property---

    // Last received values for the `favorite_foods` property.
    boost::optional<struct FavoriteFoodsProperty> _favoriteFoodsProperty;
    int _lastFavoriteFoodsPropertyVersion = -1;
    std::mutex _favoriteFoodsPropertyMutex;
   
    // MQTT Subscription ID for `favorite_foods` property updates.
    int _favoriteFoodsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `favorite_foods` property.
    void _receiveFavoriteFoodsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `favorite_foods` property.
    std::vector<std::function<void(const struct FavoriteFoodsProperty&)>> _favoriteFoodsPropertyCallbacks;
    std::mutex _favoriteFoodsPropertyCallbacksMutex;
    

    // ---lunch_menu Property---

    // Last received values for the `lunch_menu` property.
    boost::optional<struct LunchMenuProperty> _lunchMenuProperty;
    int _lastLunchMenuPropertyVersion = -1;
    std::mutex _lunchMenuPropertyMutex;
   
    // MQTT Subscription ID for `lunch_menu` property updates.
    int _lunchMenuPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `lunch_menu` property.
    void _receiveLunchMenuPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `lunch_menu` property.
    std::vector<std::function<void(const struct LunchMenuProperty&)>> _lunchMenuPropertyCallbacks;
    std::mutex _lunchMenuPropertyCallbacksMutex;
    
    
};