/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.

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
#include <boost/uuid/uuid.hpp>
#include <boost/optional.hpp>
#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "method_payloads.hpp"
#include "signal_payloads.hpp"

class SignalOnlyClient
{
public:
    // This is the name of the API.
    static constexpr const char NAME[] = "SignalOnly";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    // Constructor taking a connection object.
    SignalOnlyClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId);

    virtual ~SignalOnlyClient();
    // ------------------ SIGNALS --------------------

    // Register a callback for the `anotherSignal` signal.
    // The provided method will be called whenever a `anotherSignal` is received.
    void registerAnotherSignalCallback(const std::function<void(double, bool, std::string)>& cb);

    // Register a callback for the `bark` signal.
    // The provided method will be called whenever a `bark` is received.
    void registerBarkCallback(const std::function<void(std::string)>& cb);

    // Register a callback for the `maybe_number` signal.  The argument is optional.
    // The provided method will be called whenever a `maybe_number` is received.
    void registerMaybeNumberCallback(const std::function<void(boost::optional<int>)>& cb);

    // Register a callback for the `maybe_name` signal.  The argument is optional.
    // The provided method will be called whenever a `maybe_name` is received.
    void registerMaybeNameCallback(const std::function<void(boost::optional<std::string>)>& cb);

    // Register a callback for the `now` signal.
    // The provided method will be called whenever a `now` is received.
    void registerNowCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb);

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

    // List of callbacks to be called whenever the `anotherSignal` signal is received.
    std::vector<std::function<void(double, bool, std::string)>> _anotherSignalSignalCallbacks;
    std::mutex _anotherSignalSignalCallbacksMutex;

    // MQTT Subscription ID for `anotherSignal` signal receptions.
    int _anotherSignalSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `bark` signal is received.
    std::vector<std::function<void(std::string)>> _barkSignalCallbacks;
    std::mutex _barkSignalCallbacksMutex;

    // MQTT Subscription ID for `bark` signal receptions.
    int _barkSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `maybe_number` signal is received.
    std::vector<std::function<void(boost::optional<int>)>> _maybeNumberSignalCallbacks;
    std::mutex _maybeNumberSignalCallbacksMutex;

    // MQTT Subscription ID for `maybe_number` signal receptions.
    int _maybeNumberSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `maybe_name` signal is received.
    std::vector<std::function<void(boost::optional<std::string>)>> _maybeNameSignalCallbacks;
    std::mutex _maybeNameSignalCallbacksMutex;

    // MQTT Subscription ID for `maybe_name` signal receptions.
    int _maybeNameSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `now` signal is received.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>)>> _nowSignalCallbacks;
    std::mutex _nowSignalCallbacksMutex;

    // MQTT Subscription ID for `now` signal receptions.
    int _nowSignalSubscriptionId = -1;
};