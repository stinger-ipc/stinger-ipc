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
namespace weather {

bool InitialPropertyValues::isComplete() const
{
    if (!location.has_value()) {
        return false;
    }
    if (!currentTemperature.has_value()) {
        return false;
    }
    if (!currentCondition.has_value()) {
        return false;
    }
    if (!dailyForecast.has_value()) {
        return false;
    }
    if (!hourlyForecast.has_value()) {
        return false;
    }
    if (!currentConditionRefreshInterval.has_value()) {
        return false;
    }
    if (!hourlyForecastRefreshInterval.has_value()) {
        return false;
    }
    if (!dailyForecastRefreshInterval.has_value()) {
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
    parent.AddMember("interface_name", rapidjson::Value("weather", allocator), allocator);
    parent.AddMember("interface_version", rapidjson::Value("0.1.2", allocator), allocator);
    if (serviceId.has_value()) {
        parent.AddMember("service_id", rapidjson::Value(serviceId.value().c_str(), allocator), allocator);
    }
    if (prefix.has_value()) {
        parent.AddMember("prefix", rapidjson::Value(prefix.value().c_str(), allocator), allocator);
    }
}

WeatherDiscovery::WeatherDiscovery(std::shared_ptr<stinger::utils::IConnection> broker):
    _broker(broker)
{
    // Subscribe to the discovery topic
    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = "+";
    topicArgs["interface_name"] = "weather";
    topicArgs["client_id"] = "+";
    topicArgs["prefix"] = "+";

    _discoverySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/weather/{service_id}/interface", topicArgs), 1);
    _allPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/weather/{service_id}/property/+/value", topicArgs), 1);

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

WeatherDiscovery::~WeatherDiscovery()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void WeatherDiscovery::SetDiscoveryCallback(const std::function<void(const InstanceInfo&)>& cb)
{
    std::lock_guard<std::mutex> lock(_mutex);
    _discovery_callback = cb;
}

std::future<std::string> WeatherDiscovery::GetSingleton()
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

std::vector<InstanceInfo> WeatherDiscovery::GetInstances() const
{
    std::lock_guard<std::mutex> lock(_mutex);
    std::vector<InstanceInfo> instances;
    for (const auto& [key, info]: _discoveredInstances) {
        instances.push_back(info);
    }
    return instances;
}

void WeatherDiscovery::_onMessage(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps)
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
            if (propertyName == "location") {
                auto propertyObj = LocationProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.location = propertyObj;
                infoPtr->initial_property_values.locationVersion = propertyVersion;
            }

            else if (propertyName == "current_temperature") {
                auto propertyObj = CurrentTemperatureProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.currentTemperature = propertyObj;
                infoPtr->initial_property_values.currentTemperatureVersion = propertyVersion;
            }

            else if (propertyName == "current_condition") {
                auto propertyObj = CurrentConditionProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.currentCondition = propertyObj;
                infoPtr->initial_property_values.currentConditionVersion = propertyVersion;
            }

            else if (propertyName == "daily_forecast") {
                auto propertyObj = DailyForecastProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.dailyForecast = propertyObj;
                infoPtr->initial_property_values.dailyForecastVersion = propertyVersion;
            }

            else if (propertyName == "hourly_forecast") {
                auto propertyObj = HourlyForecastProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.hourlyForecast = propertyObj;
                infoPtr->initial_property_values.hourlyForecastVersion = propertyVersion;
            }

            else if (propertyName == "current_condition_refresh_interval") {
                auto propertyObj = CurrentConditionRefreshIntervalProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.currentConditionRefreshInterval = propertyObj;
                infoPtr->initial_property_values.currentConditionRefreshIntervalVersion = propertyVersion;
            }

            else if (propertyName == "hourly_forecast_refresh_interval") {
                auto propertyObj = HourlyForecastRefreshIntervalProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.hourlyForecastRefreshInterval = propertyObj;
                infoPtr->initial_property_values.hourlyForecastRefreshIntervalVersion = propertyVersion;
            }

            else if (propertyName == "daily_forecast_refresh_interval") {
                auto propertyObj = DailyForecastRefreshIntervalProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.dailyForecastRefreshInterval = propertyObj;
                infoPtr->initial_property_values.dailyForecastRefreshIntervalVersion = propertyVersion;
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

} // namespace weather

} // namespace gen

} // namespace stinger
