/*
Discovery service for finding available service instances.
*/

#pragma once

#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <mutex>
#include <stinger/utils/iconnection.hpp>
#include <stinger/utils/mqttproperties.hpp>
#include "structs.hpp"
#include "enums.hpp"

namespace stinger {

namespace gen {
namespace signal_only {

struct InstanceInfo {
public:
    std::optional<std::string> serviceId;
    std::optional<std::string> prefix;

    void UpdateFromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;

    bool isComplete() const;
};

class SignalOnlyDiscovery {
public:
    // Constructor taking a broker connection and service_id
    SignalOnlyDiscovery(std::shared_ptr<stinger::utils::IConnection> broker);

    virtual ~SignalOnlyDiscovery();

    // Set a callback to be invoked when a new service instance is discovered
    void SetDiscoveryCallback(const std::function<void(const InstanceInfo&)>& cb);

    // Get a singleton instance ID. Returns immediately if one is available,
    // otherwise waits until one is discovered.
    std::future<InstanceInfo> GetSingleton();

    // Get all discovered instance IDs
    std::vector<InstanceInfo> GetInstances() const;

private:
    void _onMessage(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps);
    int _discoverySubscriptionId = -1;
    int _allPropertySubscriptionId = -1;
    stinger::utils::CallbackHandleType _brokerMessageCallbackHandle = 0;
    std::shared_ptr<stinger::utils::IConnection> _broker;
    std::map<uint64_t, InstanceInfo> _discoveredInstances; // Keyed by a hash of service_id, and prefix
    std::function<void(const InstanceInfo&)> _discovery_callback;

    mutable std::mutex _mutex;
    std::vector<std::promise<InstanceInfo>> _pending_promises;
};

} // namespace signal_only

} // namespace gen

} // namespace stinger
