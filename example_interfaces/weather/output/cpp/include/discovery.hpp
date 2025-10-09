/*
Discovery service for finding available service instances.
*/

#pragma once

#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <mutex>
#include "ibrokerconnection.hpp"

class WeatherDiscovery
{
public:
    // Constructor taking a broker connection and service_id
    WeatherDiscovery(std::shared_ptr<IBrokerConnection> broker);

    virtual ~WeatherDiscovery();

    // Set a callback to be invoked when a new service instance is discovered
    void SetDiscoveryCallback(const std::function<void(const std::string&)>& cb);

    // Get a singleton instance ID. Returns immediately if one is available,
    // otherwise waits until one is discovered.
    boost::future<std::string> GetSingleton();

    // Get all discovered instance IDs
    std::vector<std::string> GetInstanceIds() const;

private:
    void _onMessage(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    CallbackHandleType _brokerMessageCallbackHandle = 0;
    std::shared_ptr<IBrokerConnection> _broker;
    std::vector<std::string> _instance_ids;
    std::function<void(const std::string&)> _discovery_callback;

    mutable std::mutex _mutex;
    std::vector<boost::promise<std::string>> _pending_promises;
};