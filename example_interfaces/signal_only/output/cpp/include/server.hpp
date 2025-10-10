/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
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
#include <boost/optional.hpp>
#include <rapidjson/document.h>

#include "ibrokerconnection.hpp"
#include "enums.hpp"

class SignalOnlyServer
{
public:
    static constexpr const char NAME[] = "SignalOnly";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    SignalOnlyServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId);

    virtual ~SignalOnlyServer();

    boost::future<bool> emitAnotherSignalSignal(double, bool, const std::string&);

    boost::future<bool> emitBarkSignal(const std::string&);

    boost::future<bool> emitMaybeNumberSignal(boost::optional<int>);

    boost::future<bool> emitMaybeNameSignal(boost::optional<std::string>);

    boost::future<bool> emitNowSignal(std::chrono::time_point<std::chrono::system_clock>);

private:
    std::shared_ptr<IBrokerConnection> _broker;
    std::string _instanceId;
    CallbackHandleType _brokerMessageCallbackHandle = 0;
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const MqttProperties& mqttProps
    );

    // ---------------- SERVICE ADVERTISEMENT ------------------

    // Thread for publishing service advertisement messages
    std::thread _advertisementThread;

    // Flag to signal the advertisement thread to stop
    std::atomic<bool> _advertisementThreadRunning;

    // Method that runs in the advertisement thread
    void _advertisementThreadLoop();
};