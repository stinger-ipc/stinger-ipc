#include "discovery.hpp"
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
#include <stinger/util/format.hpp>
#include <stinger/util/hash.hpp
#include <iostream>
#include <algorithm>
#include <sstream>

namespace stinger {

namespace gen {
namespace signal_only {

bool InitialPropertyValues::isComplete() const
{
    return true;
}

void InstanceInfo::UpdateFromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    if (jsonObj.HasMember("service_id") && jsonObj["service_id"].IsString()) {
        serviceId = jsonObj["service_id"].GetString();
    }
    if (jsonObj.HasMember("prefix") && jsonObj["prefix"].IsString()) {
        prefix = jsonObj["prefix"].GetString();
    }
};

void InstanceInfo::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("interface_name", rapidjson::Value("SignalOnly", allocator), allocator);
    parent.AddMember("interface_version", rapidjson::Value("0.0.1", allocator), allocator);
    if (serviceId.has_value()) {
        parent.AddMember("service_id", rapidjson::Value(serviceId.value().c_str(), allocator), allocator);
    }
    if (prefix.has_value()) {
        parent.AddMember("prefix", rapidjson::Value(prefix.value().c_str(), allocator), allocator);
    }
}

SignalOnlyDiscovery::SignalOnlyDiscovery(std::shared_ptr<stinger::utils::IConnection> broker):
    _broker(broker)
{
    // Subscribe to the discovery topic
    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = "+";
    topicArgs["interface_name"] = "SignalOnly";
    topicArgs["client_id"] = "+";
    topicArgs["prefix"] = "+";

    _discoverySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/SignalOnly/{service_id}/interface", topicArgs), 1);
    _allPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/SignalOnly/{service_id}/property/+/value", topicArgs), 1);

    // Register message callback
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const stinger::utils::MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _onMessage(topic, payload, mqttProps);
                                                               });
}

SignalOnlyDiscovery::~SignalOnlyDiscovery()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void SignalOnlyDiscovery::SetDiscoveryCallback(const std::function<void(const InstanceInfo&)>& cb)
{
    std::lock_guard<std::mutex> lock(_mutex);
    _discovery_callback = cb;
}

std::future<std::string> SignalOnlyDiscovery::GetSingleton()
{
    std::lock_guard<std::mutex> lock(_mutex);

    // If we already have at least one instance, return it immediately
    if (!_instance_ids.empty()) {
        std::promise<std::string> promise;
        promise.set_value(_instance_ids[0]);
        return promise.get_future();
    }

    // Otherwise, create a promise that will be fulfilled when an instance is discovered
    _pending_promises.emplace_back();
    return _pending_promises.back().get_future();
}

std::vector<InstanceInfo> SignalOnlyDiscovery::GetInstances() const
{
    std::lock_guard<std::mutex> lock(_mutex);
    std::vector<InstanceInfo> instances;
    for (const auto& [key, info]: _discoveredInstances) {
        instances.push_back(info);
    }
    return instances;
}

void SignalOnlyDiscovery::_onMessage(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps)
{
    // Check content type
    if (!mqttProps.contentType.has_value() || mqttProps.contentType.value() != "application/json") {
        std::cerr << "Invalid content type in Discovery message. Expected 'application/json'" << std::endl;
        return;
    }

    // Parse the JSON payload
    rapidjson::Document document;
    document.Parse(payload.c_str());

    if (document.HasParseError()) {
        std::cerr << "JSON parse error in Discovery: "
                  << rapidjson::GetParseError_En(document.GetParseError())
                  << " at offset " << document.GetErrorOffset() << std::endl;
        return;
    }

    InstanceInfo* infoPtr = nullptr;

    if (mqttProps.subscriptionId == _discoverySubscriptionId) {
        std::vector<std::string> hashableIdentifiers;
        const uint8_t instance_id_expected_index = 2;
        const uint8_t prefix_expected_index = 0;

        // Split topic by '/' into vector of strings
        std::vector<std::string> topicParts;
        std::stringstream ss(topic);
        std::string part;
        uint8_t index = 0;
        while (std::getline(ss, part, '/')) {
            topicParts.push_back(part);
            if ((index == instance_id_expected_index) || (index == prefix_expected_index)) {
                hashableIdentifiers.push_back(part);
            }
            index++;
        }

        uint64_t instanceHash = stinger::utils::hashStrings(hashableIdentifiers);

        if (_discoveredInstances.find(instanceHash) == _discoveredInstances.end()) {
            // Create a new InstanceInfo
            InstanceInfo info;
            info.UpdateFromRapidJsonObject(document);
            _discoveredInstances[instanceHash] = info;
            infoPtr = &_discoveredInstances[instanceHash];
        } else {
            // Update existing InstanceInfo with any new information from the payload
            _discoveredInstances[instanceHash].UpdateFromRapidJsonObject(document);
            infoPtr = &_discoveredInstances[instanceHash];
        }
    }

    if (infoPtr && infoPtr->isComplete()) {
        std::lock_guard<std::mutex> lock(_mutex);

        // Fulfill any pending promises
        for (auto& promise: _pending_promises) {
            promise.set_value(*infoPtr);
        }
        _pending_promises.clear();

        // Call the discovery callback if set
        if (_discovery_callback) {
            _discovery_callback(instance_id);
        }
    }
}

} // namespace signal_only

} // namespace gen

} // namespace stinger
