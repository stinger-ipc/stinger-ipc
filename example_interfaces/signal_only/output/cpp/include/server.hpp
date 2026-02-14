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
#include <string>
#include <memory>
#include <exception>
#include <mutex>
#include <chrono>
#include <thread>
#include <atomic>
#include <rapidjson/document.h>

#include <stinger/utils/iconnection.hpp>
#include <stinger/utils/mqttproperties.hpp>
#include "enums.hpp"

namespace stinger {

namespace gen {
namespace signal_only {

class SignalOnlyServer {
public:
    static constexpr const char NAME[] = "SignalOnly";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    SignalOnlyServer(std::shared_ptr<stinger::utils::IConnection> broker, const std::string& instanceId);

    virtual ~SignalOnlyServer();

    std::future<bool> emitAnotherSignalSignal(double, bool, std::string);

    std::future<bool> emitBarkSignal(std::string);

    std::future<bool> emitMaybeNumberSignal(std::optional<int>);

    std::future<bool> emitMaybeNameSignal(std::optional<std::string>);

    std::future<bool> emitNowSignal(std::chrono::time_point<std::chrono::system_clock>);

private:
    std::shared_ptr<stinger::utils::IConnection> _broker;
    std::string _instanceId;

    std::string _prefixTopicParam;

    stinger::utils::CallbackHandleType _brokerMessageCallbackHandle = 0;
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const stinger::utils::MqttProperties& mqttProps
    );

    // ---------------- SERVICE ADVERTISEMENT ------------------

    // Thread for publishing service advertisement messages
    std::thread _advertisementThread;

    // Flag to signal the advertisement thread to stop
    std::atomic<bool> _advertisementThreadRunning;

    // Method that runs in the advertisement thread
    void _advertisementThreadLoop();
};

} // namespace signal_only

} // namespace gen

} // namespace stinger
