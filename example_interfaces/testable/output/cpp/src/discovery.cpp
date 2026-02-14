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
namespace testable {

bool InitialPropertyValues::isComplete() const
{
    if (!readWriteInteger.has_value()) {
        return false;
    }
    if (!readOnlyInteger.has_value()) {
        return false;
    }
    if (!readWriteOptionalInteger.has_value()) {
        return false;
    }
    if (!readWriteTwoIntegers.has_value()) {
        return false;
    }
    if (!readOnlyString.has_value()) {
        return false;
    }
    if (!readWriteString.has_value()) {
        return false;
    }
    if (!readWriteOptionalString.has_value()) {
        return false;
    }
    if (!readWriteTwoStrings.has_value()) {
        return false;
    }
    if (!readWriteStruct.has_value()) {
        return false;
    }
    if (!readWriteOptionalStruct.has_value()) {
        return false;
    }
    if (!readWriteTwoStructs.has_value()) {
        return false;
    }
    if (!readOnlyEnum.has_value()) {
        return false;
    }
    if (!readWriteEnum.has_value()) {
        return false;
    }
    if (!readWriteOptionalEnum.has_value()) {
        return false;
    }
    if (!readWriteTwoEnums.has_value()) {
        return false;
    }
    if (!readWriteDatetime.has_value()) {
        return false;
    }
    if (!readWriteOptionalDatetime.has_value()) {
        return false;
    }
    if (!readWriteTwoDatetimes.has_value()) {
        return false;
    }
    if (!readWriteDuration.has_value()) {
        return false;
    }
    if (!readWriteOptionalDuration.has_value()) {
        return false;
    }
    if (!readWriteTwoDurations.has_value()) {
        return false;
    }
    if (!readWriteBinary.has_value()) {
        return false;
    }
    if (!readWriteOptionalBinary.has_value()) {
        return false;
    }
    if (!readWriteTwoBinaries.has_value()) {
        return false;
    }
    if (!readWriteListOfStrings.has_value()) {
        return false;
    }
    if (!readWriteLists.has_value()) {
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
    parent.AddMember("interface_name", rapidjson::Value("testable", allocator), allocator);
    parent.AddMember("interface_version", rapidjson::Value("0.0.1", allocator), allocator);
    if (serviceId.has_value()) {
        parent.AddMember("service_id", rapidjson::Value(serviceId.value().c_str(), allocator), allocator);
    }
    if (prefix.has_value()) {
        parent.AddMember("prefix", rapidjson::Value(prefix.value().c_str(), allocator), allocator);
    }
}

TestableDiscovery::TestableDiscovery(std::shared_ptr<stinger::utils::IConnection> broker):
    _broker(broker)
{
    // Subscribe to the discovery topic
    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = "+";
    topicArgs["interface_name"] = "testable";
    topicArgs["client_id"] = "+";
    topicArgs["prefix"] = "+";

    _discoverySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/interface", topicArgs), 1);
    _allPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/+/value", topicArgs), 1);

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

TestableDiscovery::~TestableDiscovery()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void TestableDiscovery::SetDiscoveryCallback(const std::function<void(const InstanceInfo&)>& cb)
{
    std::lock_guard<std::mutex> lock(_mutex);
    _discovery_callback = cb;
}

std::future<std::string> TestableDiscovery::GetSingleton()
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

std::vector<InstanceInfo> TestableDiscovery::GetInstances() const
{
    std::lock_guard<std::mutex> lock(_mutex);
    std::vector<InstanceInfo> instances;
    for (const auto& [key, info]: _discoveredInstances) {
        instances.push_back(info);
    }
    return instances;
}

void TestableDiscovery::_onMessage(const std::string& topic, const std::string& payload, const stinger::utils::MqttProperties& mqttProps)
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
            if (propertyName == "read_write_integer") {
                auto propertyObj = ReadWriteIntegerProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteInteger = propertyObj;
                infoPtr->initial_property_values.readWriteIntegerVersion = propertyVersion;
            }

            else if (propertyName == "read_only_integer") {
                auto propertyObj = ReadOnlyIntegerProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readOnlyInteger = propertyObj;
                infoPtr->initial_property_values.readOnlyIntegerVersion = propertyVersion;
            }

            else if (propertyName == "read_write_optional_integer") {
                auto propertyObj = ReadWriteOptionalIntegerProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteOptionalInteger = propertyObj;
                infoPtr->initial_property_values.readWriteOptionalIntegerVersion = propertyVersion;
            }

            else if (propertyName == "read_write_two_integers") {
                auto propertyObj = ReadWriteTwoIntegersProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteTwoIntegers = propertyObj;
                infoPtr->initial_property_values.readWriteTwoIntegersVersion = propertyVersion;
            }

            else if (propertyName == "read_only_string") {
                auto propertyObj = ReadOnlyStringProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readOnlyString = propertyObj;
                infoPtr->initial_property_values.readOnlyStringVersion = propertyVersion;
            }

            else if (propertyName == "read_write_string") {
                auto propertyObj = ReadWriteStringProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteString = propertyObj;
                infoPtr->initial_property_values.readWriteStringVersion = propertyVersion;
            }

            else if (propertyName == "read_write_optional_string") {
                auto propertyObj = ReadWriteOptionalStringProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteOptionalString = propertyObj;
                infoPtr->initial_property_values.readWriteOptionalStringVersion = propertyVersion;
            }

            else if (propertyName == "read_write_two_strings") {
                auto propertyObj = ReadWriteTwoStringsProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteTwoStrings = propertyObj;
                infoPtr->initial_property_values.readWriteTwoStringsVersion = propertyVersion;
            }

            else if (propertyName == "read_write_struct") {
                auto propertyObj = ReadWriteStructProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteStruct = propertyObj;
                infoPtr->initial_property_values.readWriteStructVersion = propertyVersion;
            }

            else if (propertyName == "read_write_optional_struct") {
                auto propertyObj = ReadWriteOptionalStructProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteOptionalStruct = propertyObj;
                infoPtr->initial_property_values.readWriteOptionalStructVersion = propertyVersion;
            }

            else if (propertyName == "read_write_two_structs") {
                auto propertyObj = ReadWriteTwoStructsProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteTwoStructs = propertyObj;
                infoPtr->initial_property_values.readWriteTwoStructsVersion = propertyVersion;
            }

            else if (propertyName == "read_only_enum") {
                auto propertyObj = ReadOnlyEnumProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readOnlyEnum = propertyObj;
                infoPtr->initial_property_values.readOnlyEnumVersion = propertyVersion;
            }

            else if (propertyName == "read_write_enum") {
                auto propertyObj = ReadWriteEnumProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteEnum = propertyObj;
                infoPtr->initial_property_values.readWriteEnumVersion = propertyVersion;
            }

            else if (propertyName == "read_write_optional_enum") {
                auto propertyObj = ReadWriteOptionalEnumProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteOptionalEnum = propertyObj;
                infoPtr->initial_property_values.readWriteOptionalEnumVersion = propertyVersion;
            }

            else if (propertyName == "read_write_two_enums") {
                auto propertyObj = ReadWriteTwoEnumsProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteTwoEnums = propertyObj;
                infoPtr->initial_property_values.readWriteTwoEnumsVersion = propertyVersion;
            }

            else if (propertyName == "read_write_datetime") {
                auto propertyObj = ReadWriteDatetimeProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteDatetime = propertyObj;
                infoPtr->initial_property_values.readWriteDatetimeVersion = propertyVersion;
            }

            else if (propertyName == "read_write_optional_datetime") {
                auto propertyObj = ReadWriteOptionalDatetimeProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteOptionalDatetime = propertyObj;
                infoPtr->initial_property_values.readWriteOptionalDatetimeVersion = propertyVersion;
            }

            else if (propertyName == "read_write_two_datetimes") {
                auto propertyObj = ReadWriteTwoDatetimesProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteTwoDatetimes = propertyObj;
                infoPtr->initial_property_values.readWriteTwoDatetimesVersion = propertyVersion;
            }

            else if (propertyName == "read_write_duration") {
                auto propertyObj = ReadWriteDurationProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteDuration = propertyObj;
                infoPtr->initial_property_values.readWriteDurationVersion = propertyVersion;
            }

            else if (propertyName == "read_write_optional_duration") {
                auto propertyObj = ReadWriteOptionalDurationProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteOptionalDuration = propertyObj;
                infoPtr->initial_property_values.readWriteOptionalDurationVersion = propertyVersion;
            }

            else if (propertyName == "read_write_two_durations") {
                auto propertyObj = ReadWriteTwoDurationsProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteTwoDurations = propertyObj;
                infoPtr->initial_property_values.readWriteTwoDurationsVersion = propertyVersion;
            }

            else if (propertyName == "read_write_binary") {
                auto propertyObj = ReadWriteBinaryProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteBinary = propertyObj;
                infoPtr->initial_property_values.readWriteBinaryVersion = propertyVersion;
            }

            else if (propertyName == "read_write_optional_binary") {
                auto propertyObj = ReadWriteOptionalBinaryProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteOptionalBinary = propertyObj;
                infoPtr->initial_property_values.readWriteOptionalBinaryVersion = propertyVersion;
            }

            else if (propertyName == "read_write_two_binaries") {
                auto propertyObj = ReadWriteTwoBinariesProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteTwoBinaries = propertyObj;
                infoPtr->initial_property_values.readWriteTwoBinariesVersion = propertyVersion;
            }

            else if (propertyName == "read_write_list_of_strings") {
                auto propertyObj = ReadWriteListOfStringsProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteListOfStrings = propertyObj;
                infoPtr->initial_property_values.readWriteListOfStringsVersion = propertyVersion;
            }

            else if (propertyName == "read_write_lists") {
                auto propertyObj = ReadWriteListsProperty::FromRapidJsonObject(document);
                infoPtr->initial_property_values.readWriteLists = propertyObj;
                infoPtr->initial_property_values.readWriteListsVersion = propertyVersion;
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

} // namespace testable

} // namespace gen

} // namespace stinger
