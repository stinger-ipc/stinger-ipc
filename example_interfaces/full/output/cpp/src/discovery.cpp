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
namespace full {

bool InitialPropertyValues::isComplete() const
{
    if (!favoriteNumber.has_value()) {
        return false;
    }
    if (!favoriteFoods.has_value()) {
        return false;
    }
    if (!lunchMenu.has_value()) {
        return false;
    }
    if (!familyName.has_value()) {
        return false;
    }
    if (!lastBreakfastTime.has_value()) {
        return false;
    }
    if (!lastBirthdays.has_value()) {
        return false;
    }
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
    parent.AddMember("interface_name", rapidjson::Value("Full", allocator), allocator);
    parent.AddMember("interface_version", rapidjson::Value("0.0.2", allocator), allocator);
    if (serviceId.has_value()) {
        parent.AddMember("service_id", rapidjson::Value(serviceId.value().c_str(), allocator), allocator);
    }
    if (prefix.has_value()) {
        parent.AddMember("prefix", rapidjson::Value(prefix.value().c_str(), allocator), allocator);
    }
}

FullDiscovery::FullDiscovery(std::shared_ptr<stinger::utils::IConnection> broker):
    _broker(broker)
{
    // Subscribe to the discovery topic
    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = "+";
    topicArgs["interface_name"] = "Full";
    topicArgs["client_id"] = "+";
    topicArgs["prefix"] = "+";

    _discoverySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/interface", topicArgs), 1);
    _allPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/Full/{service_id}/property/+/value", topicArgs), 1);

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

FullDiscovery::~FullDiscovery()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void FullDiscovery::SetDiscoveryCallback(const std::function<void(const InstanceInfo&)>& cb)
{
    std::lock_guard<std::mutex> lock(_mutex);
    _discovery_callback = cb;
}

std::future<std::string> FullDiscovery::GetSingleton()
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

std::vector<InstanceInfo> FullDiscovery::GetInstances() const
{
    std::lock_guard<std::mutex> lock(_mutex);
    std::vector<InstanceInfo> instances;
    for (const auto& [key, info]: _discoveredInstances) {
        instances.push_back(info);
    }
    return instances;
}

void FullDiscovery::_onMessage(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps)
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
    } else if (mqttProps.subscriptionId == _allPropertySubscriptionId) {
        // Parse out identifying information from the topic to find the corresponding InstanceInfo
        std::vector<std::string> hashableIdentifiers;
        std::string propertyName;
        uint32_t propertyVersion = 0;
        if (mqttProps.hasUserProperty("PropertyVersion")) {
            propertyVersion = mqttProps.userProperty("PropertyVersion");
        }
        const uint8_t instance_id_expected_index = 2;
        const uint8_t prefix_expected_index = 0;

        const uint8_t property_name_expected_index = 4;

        // Split topic by '/' into vector of strings
        std::vector<std::string> topicParts;
        std::stringstream ss(topic);
        std::string part;
        uint8_t index = 0;
        while (std::getline(ss, part, '/')) {
            topicParts.push_back(part);
            if ((index == instance_id_expected_index) || (index == prefix_expected_index)) {
                hashableIdentifiers.push_back(part);
            } else if (index == property_name_expected_index) {
                propertyName = part;
            }
            index++;
        }

        uint64_t instanceHash = stinger::utils::hashStrings(hashableIdentifiers);

        auto it = _discoveredInstances.find(instanceHash);
        if (it == _discoveredInstances.end()) {
            InstanceInfo info;
            _discoveredInstances[instanceHash] = info;
            infoPtr = &_discoveredInstances[instanceHash];
        } else {
            infoPtr = &it->second;
        }

        if (infoPtr) {
            if (propertyName == "favorite_number") {
                auto propertyObj = FavoriteNumberProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.favoriteNumber = propertyObj;
                infoPtr->initial_property_values.favoriteNumberVersion = propertyVersion;
            }

            else if (propertyName == "favorite_foods") {
                auto propertyObj = FavoriteFoodsProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.favoriteFoods = propertyObj;
                infoPtr->initial_property_values.favoriteFoodsVersion = propertyVersion;
            }

            else if (propertyName == "lunch_menu") {
                auto propertyObj = LunchMenuProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.lunchMenu = propertyObj;
                infoPtr->initial_property_values.lunchMenuVersion = propertyVersion;
            }

            else if (propertyName == "family_name") {
                auto propertyObj = FamilyNameProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.familyName = propertyObj;
                infoPtr->initial_property_values.familyNameVersion = propertyVersion;
            }

            else if (propertyName == "last_breakfast_time") {
                auto propertyObj = LastBreakfastTimeProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.lastBreakfastTime = propertyObj;
                infoPtr->initial_property_values.lastBreakfastTimeVersion = propertyVersion;
            }

            else if (propertyName == "last_birthdays") {
                auto propertyObj = LastBirthdaysProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.lastBirthdays = propertyObj;
                infoPtr->initial_property_values.lastBirthdaysVersion = propertyVersion;
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

} // namespace full

} // namespace gen

} // namespace stinger
