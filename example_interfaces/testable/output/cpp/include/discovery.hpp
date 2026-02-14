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
namespace testable {

struct InitialPropertyValues {
public:
    std::optional<ReadWriteIntegerProperty> readWriteInteger;
    int readWriteIntegerVersion = 0;

    std::optional<ReadOnlyIntegerProperty> readOnlyInteger;
    int readOnlyIntegerVersion = 0;

    std::optional<ReadWriteOptionalIntegerProperty> readWriteOptionalInteger;
    int readWriteOptionalIntegerVersion = 0;

    std::optional<ReadWriteTwoIntegersProperty> readWriteTwoIntegers;
    int readWriteTwoIntegersVersion = 0;

    std::optional<ReadOnlyStringProperty> readOnlyString;
    int readOnlyStringVersion = 0;

    std::optional<ReadWriteStringProperty> readWriteString;
    int readWriteStringVersion = 0;

    std::optional<ReadWriteOptionalStringProperty> readWriteOptionalString;
    int readWriteOptionalStringVersion = 0;

    std::optional<ReadWriteTwoStringsProperty> readWriteTwoStrings;
    int readWriteTwoStringsVersion = 0;

    std::optional<ReadWriteStructProperty> readWriteStruct;
    int readWriteStructVersion = 0;

    std::optional<ReadWriteOptionalStructProperty> readWriteOptionalStruct;
    int readWriteOptionalStructVersion = 0;

    std::optional<ReadWriteTwoStructsProperty> readWriteTwoStructs;
    int readWriteTwoStructsVersion = 0;

    std::optional<ReadOnlyEnumProperty> readOnlyEnum;
    int readOnlyEnumVersion = 0;

    std::optional<ReadWriteEnumProperty> readWriteEnum;
    int readWriteEnumVersion = 0;

    std::optional<ReadWriteOptionalEnumProperty> readWriteOptionalEnum;
    int readWriteOptionalEnumVersion = 0;

    std::optional<ReadWriteTwoEnumsProperty> readWriteTwoEnums;
    int readWriteTwoEnumsVersion = 0;

    std::optional<ReadWriteDatetimeProperty> readWriteDatetime;
    int readWriteDatetimeVersion = 0;

    std::optional<ReadWriteOptionalDatetimeProperty> readWriteOptionalDatetime;
    int readWriteOptionalDatetimeVersion = 0;

    std::optional<ReadWriteTwoDatetimesProperty> readWriteTwoDatetimes;
    int readWriteTwoDatetimesVersion = 0;

    std::optional<ReadWriteDurationProperty> readWriteDuration;
    int readWriteDurationVersion = 0;

    std::optional<ReadWriteOptionalDurationProperty> readWriteOptionalDuration;
    int readWriteOptionalDurationVersion = 0;

    std::optional<ReadWriteTwoDurationsProperty> readWriteTwoDurations;
    int readWriteTwoDurationsVersion = 0;

    std::optional<ReadWriteBinaryProperty> readWriteBinary;
    int readWriteBinaryVersion = 0;

    std::optional<ReadWriteOptionalBinaryProperty> readWriteOptionalBinary;
    int readWriteOptionalBinaryVersion = 0;

    std::optional<ReadWriteTwoBinariesProperty> readWriteTwoBinaries;
    int readWriteTwoBinariesVersion = 0;

    std::optional<ReadWriteListOfStringsProperty> readWriteListOfStrings;
    int readWriteListOfStringsVersion = 0;

    std::optional<ReadWriteListsProperty> readWriteLists;
    int readWriteListsVersion = 0;

    bool isComplete() const;
};

struct InstanceInfo {
public:
    std::optional<std::string> serviceId;
    std::optional<std::string> prefix;
    InitialPropertyValues initial_property_values; // Not included in (de-)serialization.

    void UpdateFromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;

    bool isComplete() const;
};

class TestableDiscovery {
public:
    // Constructor taking a broker connection and service_id
    TestableDiscovery(std::shared_ptr<stinger::utils::IConnection> broker);

    virtual ~TestableDiscovery();

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

} // namespace testable

} // namespace gen

} // namespace stinger
