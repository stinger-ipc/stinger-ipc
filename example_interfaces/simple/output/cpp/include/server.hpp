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
#include <string>
#include <memory>
#include <exception>
#include <mutex>
#include <chrono>
#include <thread>
#include <atomic>
#include "utils.hpp"
#include <rapidjson/document.h>

#include "property_structs.hpp"

#include "ibrokerconnection.hpp"
#include "enums.hpp"

#include "method_payloads.hpp"

class SimpleServer
{
public:
    static constexpr const char NAME[] = "Simple";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    SimpleServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId);

    virtual ~SimpleServer();

    std::future<bool> emitPersonEnteredSignal(Person);

    void registerTradeNumbersHandler(std::function<int(int)> func);

    // ---school Property---

    // Gets the latest value of the `school` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::string&> getSchoolProperty();

    // Add a callback that will be called whenever the `school` property is updated.
    // The provided method will be called whenever a new value for the `school` property is received.
    void registerSchoolPropertyCallback(const std::function<void(std::string)>& cb);

    void updateSchoolProperty(std::string);

    void republishSchoolProperty() const;

private:
    std::shared_ptr<IBrokerConnection> _broker;
    std::string _instanceId;
    CallbackHandleType _brokerMessageCallbackHandle = 0;
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const MqttProperties& mqttProps
    );

    void _callTradeNumbersHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<int(int)> _tradeNumbersHandler;
    int _tradeNumbersMethodSubscriptionId;

    // ---------------- PROPERTIES ------------------

    // ---school Property---

    // Current value for the `school` property.
    std::optional<SchoolProperty> _schoolProperty;

    // This is the property version  of `school`.
    int _lastSchoolPropertyVersion = -1;

    // Mutex for protecting access to the `school` property and its version.
    mutable std::mutex _schoolPropertyMutex;

    // MQTT Subscription ID for `school` property update requests.
    int _schoolPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `school` property.
    void _receiveSchoolPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `school` property.
    std::vector<std::function<void(std::string)>> _schoolPropertyCallbacks;
    std::mutex _schoolPropertyCallbacksMutex;

    // ---------------- SERVICE ADVERTISEMENT ------------------

    // Thread for publishing service advertisement messages
    std::thread _advertisementThread;

    // Flag to signal the advertisement thread to stop
    std::atomic<bool> _advertisementThreadRunning;

    // Method that runs in the advertisement thread
    void _advertisementThreadLoop();
};