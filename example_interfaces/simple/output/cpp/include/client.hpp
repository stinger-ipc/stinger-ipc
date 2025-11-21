/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Simple interface.

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
#include "utils.hpp"
#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "method_payloads.hpp"
#include "signal_payloads.hpp"

#include "property_structs.hpp"

class SimpleClient
{
public:
    // This is the name of the API.
    static constexpr const char NAME[] = "Simple";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    // Constructor taking a connection object.
    SimpleClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId);

    virtual ~SimpleClient();
    // ------------------ SIGNALS --------------------

    // Register a callback for the `person_entered` signal.
    // The provided method will be called whenever a `person_entered` is received.
    void registerPersonEnteredCallback(const std::function<void(Person)>& cb);

    // ------------------- METHODS --------------------

    // Calls the `trade_numbers` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgPrimitive name=my_number type=int>
    std::future<int> tradeNumbers(int your_number);

    // ---------------- PROPERTIES ------------------

    // ---school Property---

    // Gets the latest value of the `school` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::string&> getSchoolProperty();

    // Add a callback that will be called whenever the `school` property is updated.
    // The provided method will be called whenever a new value for the `school` property is received.
    void registerSchoolPropertyCallback(const std::function<void(std::string)>& cb);

    std::future<bool> updateSchoolProperty(std::string) const;

private:
    // Pointer to the broker connection.
    std::shared_ptr<IBrokerConnection> _broker;

    // Service Instance ID that this client is connected to.
    std::string _instanceId;

    CallbackHandleType _brokerMessageCallbackHandle = 0;

    // Internal method for receiving messages from the broker.
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const MqttProperties& mqttProps
    );

    // ------------------ SIGNALS --------------------

    // List of callbacks to be called whenever the `person_entered` signal is received.
    std::vector<std::function<void(Person)>> _personEnteredSignalCallbacks;
    std::mutex _personEnteredSignalCallbacksMutex;

    // MQTT Subscription ID for `person_entered` signal receptions.
    int _personEnteredSignalSubscriptionId = -1;

    // ------------------- METHODS --------------------
    // Holds promises for pending `trade_numbers` method calls.
    std::map<std::string, std::promise<int>> _pendingTradeNumbersMethodCalls;
    int _tradeNumbersMethodSubscriptionId = -1;
    // This is called internally to process responses to `trade_numbers` method calls.
    void _handleTradeNumbersResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // ---------------- PROPERTIES ------------------

    // ---school Property---

    // Last received value for the `school` property.
    std::optional<SchoolProperty> _schoolProperty;

    // This is the property version of the last received `school` property update.
    int _lastSchoolPropertyVersion = -1;

    // Mutex for protecting access to the `school` property and its version.
    mutable std::mutex _schoolPropertyMutex;

    // MQTT Subscription ID for `school` property updates.
    int _schoolPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `school` property.
    void _receiveSchoolPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `school` property.
    std::vector<std::function<void(std::string)>> _schoolPropertyCallbacks;
    std::mutex _schoolPropertyCallbacksMutex;
};