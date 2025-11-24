/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the testable interface.

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
#include "utils.hpp"
#include <rapidjson/document.h>

#include "property_structs.hpp"

#include "ibrokerconnection.hpp"
#include "enums.hpp"

#include "method_payloads.hpp"

class TestableServer
{
public:
    static constexpr const char NAME[] = "testable";
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    TestableServer(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId);

    virtual ~TestableServer();

    std::future<bool> emitEmptySignal();

    std::future<bool> emitSingleIntSignal(int);

    std::future<bool> emitSingleOptionalIntSignal(std::optional<int>);

    std::future<bool> emitThreeIntegersSignal(int, int, std::optional<int>);

    std::future<bool> emitSingleStringSignal(std::string);

    std::future<bool> emitSingleOptionalStringSignal(std::optional<std::string>);

    std::future<bool> emitThreeStringsSignal(std::string, std::string, std::optional<std::string>);

    std::future<bool> emitSingleEnumSignal(Numbers);

    std::future<bool> emitSingleOptionalEnumSignal(std::optional<Numbers>);

    std::future<bool> emitThreeEnumsSignal(Numbers, Numbers, std::optional<Numbers>);

    std::future<bool> emitSingleStructSignal(AllTypes);

    std::future<bool> emitSingleOptionalStructSignal(std::optional<AllTypes>);

    std::future<bool> emitThreeStructsSignal(AllTypes, AllTypes, std::optional<AllTypes>);

    std::future<bool> emitSingleDateTimeSignal(std::chrono::time_point<std::chrono::system_clock>);

    std::future<bool> emitSingleOptionalDatetimeSignal(std::optional<std::chrono::time_point<std::chrono::system_clock>>);

    std::future<bool> emitThreeDateTimesSignal(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>);

    std::future<bool> emitSingleDurationSignal(std::chrono::duration<double>);

    std::future<bool> emitSingleOptionalDurationSignal(std::optional<std::chrono::duration<double>>);

    std::future<bool> emitThreeDurationsSignal(std::chrono::duration<double>, std::chrono::duration<double>, std::optional<std::chrono::duration<double>>);

    std::future<bool> emitSingleBinarySignal(std::vector<uint8_t>);

    std::future<bool> emitSingleOptionalBinarySignal(std::optional<std::vector<uint8_t>>);

    std::future<bool> emitThreeBinariesSignal(std::vector<uint8_t>, std::vector<uint8_t>, std::optional<std::vector<uint8_t>>);

    std::future<bool> emitSingleArrayOfIntegersSignal(std::vector<int>);

    std::future<bool> emitSingleOptionalArrayOfStringsSignal(std::optional<std::vector<std::string>>);

    std::future<bool> emitArrayOfEveryTypeSignal(std::vector<int>, std::vector<double>, std::vector<std::string>, std::vector<Numbers>, std::vector<Entry>, std::vector<std::chrono::time_point<std::chrono::system_clock>>, std::vector<std::chrono::duration<double>>, std::vector<std::vector<uint8_t>>);

    void registerCallWithNothingHandler(std::function<void()> func);

    void registerCallOneIntegerHandler(std::function<int(int)> func);

    void registerCallOptionalIntegerHandler(std::function<std::optional<int>(std::optional<int>)> func);

    void registerCallThreeIntegersHandler(std::function<CallThreeIntegersReturnValues(int, int, std::optional<int>)> func);

    void registerCallOneStringHandler(std::function<std::string(std::string)> func);

    void registerCallOptionalStringHandler(std::function<std::optional<std::string>(std::optional<std::string>)> func);

    void registerCallThreeStringsHandler(std::function<CallThreeStringsReturnValues(std::string, std::optional<std::string>, std::string)> func);

    void registerCallOneEnumHandler(std::function<Numbers(Numbers)> func);

    void registerCallOptionalEnumHandler(std::function<std::optional<Numbers>(std::optional<Numbers>)> func);

    void registerCallThreeEnumsHandler(std::function<CallThreeEnumsReturnValues(Numbers, Numbers, std::optional<Numbers>)> func);

    void registerCallOneStructHandler(std::function<AllTypes(AllTypes)> func);

    void registerCallOptionalStructHandler(std::function<std::optional<AllTypes>(std::optional<AllTypes>)> func);

    void registerCallThreeStructsHandler(std::function<CallThreeStructsReturnValues(std::optional<AllTypes>, AllTypes, AllTypes)> func);

    void registerCallOneDateTimeHandler(std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::time_point<std::chrono::system_clock>)> func);

    void registerCallOptionalDateTimeHandler(std::function<std::optional<std::chrono::time_point<std::chrono::system_clock>>(std::optional<std::chrono::time_point<std::chrono::system_clock>>)> func);

    void registerCallThreeDateTimesHandler(std::function<CallThreeDateTimesReturnValues(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>)> func);

    void registerCallOneDurationHandler(std::function<std::chrono::duration<double>(std::chrono::duration<double>)> func);

    void registerCallOptionalDurationHandler(std::function<std::optional<std::chrono::duration<double>>(std::optional<std::chrono::duration<double>>)> func);

    void registerCallThreeDurationsHandler(std::function<CallThreeDurationsReturnValues(std::chrono::duration<double>, std::chrono::duration<double>, std::optional<std::chrono::duration<double>>)> func);

    void registerCallOneBinaryHandler(std::function<std::vector<uint8_t>(std::vector<uint8_t>)> func);

    void registerCallOptionalBinaryHandler(std::function<std::optional<std::vector<uint8_t>>(std::optional<std::vector<uint8_t>>)> func);

    void registerCallThreeBinariesHandler(std::function<CallThreeBinariesReturnValues(std::vector<uint8_t>, std::vector<uint8_t>, std::optional<std::vector<uint8_t>>)> func);

    void registerCallOneListOfIntegersHandler(std::function<std::vector<int>(std::vector<int>)> func);

    void registerCallOptionalListOfFloatsHandler(std::function<std::optional<std::vector<double>>(std::optional<std::vector<double>>)> func);

    void registerCallTwoListsHandler(std::function<CallTwoListsReturnValues(std::vector<Numbers>, std::optional<std::vector<std::string>>)> func);

    // ---read_write_integer Property---

    // Gets the latest value of the `read_write_integer` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<int> getReadWriteIntegerProperty();

    // Add a callback that will be called whenever the `read_write_integer` property is updated.
    // The provided method will be called whenever a new value for the `read_write_integer` property is received.
    void registerReadWriteIntegerPropertyCallback(const std::function<void(int)>& cb);

    void updateReadWriteIntegerProperty(int);

    void republishReadWriteIntegerProperty() const;

    // ---read_only_integer Property---

    // Gets the latest value of the `read_only_integer` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<int> getReadOnlyIntegerProperty();

    // Add a callback that will be called whenever the `read_only_integer` property is updated.
    // The provided method will be called whenever a new value for the `read_only_integer` property is received.
    void registerReadOnlyIntegerPropertyCallback(const std::function<void(int)>& cb);

    void updateReadOnlyIntegerProperty(int);

    void republishReadOnlyIntegerProperty() const;

    // ---read_write_optional_integer Property---

    // Gets the latest value of the `read_write_optional_integer` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<int> getReadWriteOptionalIntegerProperty();

    // Add a callback that will be called whenever the `read_write_optional_integer` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_integer` property is received.
    void registerReadWriteOptionalIntegerPropertyCallback(const std::function<void(std::optional<int>)>& cb);

    void updateReadWriteOptionalIntegerProperty(std::optional<int>);

    void republishReadWriteOptionalIntegerProperty() const;

    // ---read_write_two_integers Property---

    // Gets the latest value of the `read_write_two_integers` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<ReadWriteTwoIntegersProperty> getReadWriteTwoIntegersProperty();

    // Add a callback that will be called whenever the `read_write_two_integers` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_integers` property is received.
    void registerReadWriteTwoIntegersPropertyCallback(const std::function<void(int, std::optional<int>)>& cb);

    void updateReadWriteTwoIntegersProperty(int, std::optional<int>);

    void republishReadWriteTwoIntegersProperty() const;

    // ---read_only_string Property---

    // Gets the latest value of the `read_only_string` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::string> getReadOnlyStringProperty();

    // Add a callback that will be called whenever the `read_only_string` property is updated.
    // The provided method will be called whenever a new value for the `read_only_string` property is received.
    void registerReadOnlyStringPropertyCallback(const std::function<void(std::string)>& cb);

    void updateReadOnlyStringProperty(std::string);

    void republishReadOnlyStringProperty() const;

    // ---read_write_string Property---

    // Gets the latest value of the `read_write_string` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::string> getReadWriteStringProperty();

    // Add a callback that will be called whenever the `read_write_string` property is updated.
    // The provided method will be called whenever a new value for the `read_write_string` property is received.
    void registerReadWriteStringPropertyCallback(const std::function<void(std::string)>& cb);

    void updateReadWriteStringProperty(std::string);

    void republishReadWriteStringProperty() const;

    // ---read_write_optional_string Property---

    // Gets the latest value of the `read_write_optional_string` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::string> getReadWriteOptionalStringProperty();

    // Add a callback that will be called whenever the `read_write_optional_string` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_string` property is received.
    void registerReadWriteOptionalStringPropertyCallback(const std::function<void(std::optional<std::string>)>& cb);

    void updateReadWriteOptionalStringProperty(std::optional<std::string>);

    void republishReadWriteOptionalStringProperty() const;

    // ---read_write_two_strings Property---

    // Gets the latest value of the `read_write_two_strings` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<ReadWriteTwoStringsProperty> getReadWriteTwoStringsProperty();

    // Add a callback that will be called whenever the `read_write_two_strings` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_strings` property is received.
    void registerReadWriteTwoStringsPropertyCallback(const std::function<void(std::string, std::optional<std::string>)>& cb);

    void updateReadWriteTwoStringsProperty(std::string, std::optional<std::string>);

    void republishReadWriteTwoStringsProperty() const;

    // ---read_write_struct Property---

    // Gets the latest value of the `read_write_struct` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<AllTypes> getReadWriteStructProperty();

    // Add a callback that will be called whenever the `read_write_struct` property is updated.
    // The provided method will be called whenever a new value for the `read_write_struct` property is received.
    void registerReadWriteStructPropertyCallback(const std::function<void(AllTypes)>& cb);

    void updateReadWriteStructProperty(AllTypes);

    void republishReadWriteStructProperty() const;

    // ---read_write_optional_struct Property---

    // Gets the latest value of the `read_write_optional_struct` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<AllTypes> getReadWriteOptionalStructProperty();

    // Add a callback that will be called whenever the `read_write_optional_struct` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_struct` property is received.
    void registerReadWriteOptionalStructPropertyCallback(const std::function<void(std::optional<AllTypes>)>& cb);

    void updateReadWriteOptionalStructProperty(std::optional<AllTypes>);

    void republishReadWriteOptionalStructProperty() const;

    // ---read_write_two_structs Property---

    // Gets the latest value of the `read_write_two_structs` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<ReadWriteTwoStructsProperty> getReadWriteTwoStructsProperty();

    // Add a callback that will be called whenever the `read_write_two_structs` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_structs` property is received.
    void registerReadWriteTwoStructsPropertyCallback(const std::function<void(AllTypes, std::optional<AllTypes>)>& cb);

    void updateReadWriteTwoStructsProperty(AllTypes, std::optional<AllTypes>);

    void republishReadWriteTwoStructsProperty() const;

    // ---read_only_enum Property---

    // Gets the latest value of the `read_only_enum` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<Numbers> getReadOnlyEnumProperty();

    // Add a callback that will be called whenever the `read_only_enum` property is updated.
    // The provided method will be called whenever a new value for the `read_only_enum` property is received.
    void registerReadOnlyEnumPropertyCallback(const std::function<void(Numbers)>& cb);

    void updateReadOnlyEnumProperty(Numbers);

    void republishReadOnlyEnumProperty() const;

    // ---read_write_enum Property---

    // Gets the latest value of the `read_write_enum` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<Numbers> getReadWriteEnumProperty();

    // Add a callback that will be called whenever the `read_write_enum` property is updated.
    // The provided method will be called whenever a new value for the `read_write_enum` property is received.
    void registerReadWriteEnumPropertyCallback(const std::function<void(Numbers)>& cb);

    void updateReadWriteEnumProperty(Numbers);

    void republishReadWriteEnumProperty() const;

    // ---read_write_optional_enum Property---

    // Gets the latest value of the `read_write_optional_enum` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<Numbers> getReadWriteOptionalEnumProperty();

    // Add a callback that will be called whenever the `read_write_optional_enum` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_enum` property is received.
    void registerReadWriteOptionalEnumPropertyCallback(const std::function<void(std::optional<Numbers>)>& cb);

    void updateReadWriteOptionalEnumProperty(std::optional<Numbers>);

    void republishReadWriteOptionalEnumProperty() const;

    // ---read_write_two_enums Property---

    // Gets the latest value of the `read_write_two_enums` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<ReadWriteTwoEnumsProperty> getReadWriteTwoEnumsProperty();

    // Add a callback that will be called whenever the `read_write_two_enums` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_enums` property is received.
    void registerReadWriteTwoEnumsPropertyCallback(const std::function<void(Numbers, std::optional<Numbers>)>& cb);

    void updateReadWriteTwoEnumsProperty(Numbers, std::optional<Numbers>);

    void republishReadWriteTwoEnumsProperty() const;

    // ---read_write_datetime Property---

    // Gets the latest value of the `read_write_datetime` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::chrono::time_point<std::chrono::system_clock>> getReadWriteDatetimeProperty();

    // Add a callback that will be called whenever the `read_write_datetime` property is updated.
    // The provided method will be called whenever a new value for the `read_write_datetime` property is received.
    void registerReadWriteDatetimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb);

    void updateReadWriteDatetimeProperty(std::chrono::time_point<std::chrono::system_clock>);

    void republishReadWriteDatetimeProperty() const;

    // ---read_write_optional_datetime Property---

    // Gets the latest value of the `read_write_optional_datetime` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::chrono::time_point<std::chrono::system_clock>> getReadWriteOptionalDatetimeProperty();

    // Add a callback that will be called whenever the `read_write_optional_datetime` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_datetime` property is received.
    void registerReadWriteOptionalDatetimePropertyCallback(const std::function<void(std::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb);

    void updateReadWriteOptionalDatetimeProperty(std::optional<std::chrono::time_point<std::chrono::system_clock>>);

    void republishReadWriteOptionalDatetimeProperty() const;

    // ---read_write_two_datetimes Property---

    // Gets the latest value of the `read_write_two_datetimes` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<ReadWriteTwoDatetimesProperty> getReadWriteTwoDatetimesProperty();

    // Add a callback that will be called whenever the `read_write_two_datetimes` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_datetimes` property is received.
    void registerReadWriteTwoDatetimesPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb);

    void updateReadWriteTwoDatetimesProperty(std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>);

    void republishReadWriteTwoDatetimesProperty() const;

    // ---read_write_duration Property---

    // Gets the latest value of the `read_write_duration` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::chrono::duration<double>> getReadWriteDurationProperty();

    // Add a callback that will be called whenever the `read_write_duration` property is updated.
    // The provided method will be called whenever a new value for the `read_write_duration` property is received.
    void registerReadWriteDurationPropertyCallback(const std::function<void(std::chrono::duration<double>)>& cb);

    void updateReadWriteDurationProperty(std::chrono::duration<double>);

    void republishReadWriteDurationProperty() const;

    // ---read_write_optional_duration Property---

    // Gets the latest value of the `read_write_optional_duration` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::chrono::duration<double>> getReadWriteOptionalDurationProperty();

    // Add a callback that will be called whenever the `read_write_optional_duration` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_duration` property is received.
    void registerReadWriteOptionalDurationPropertyCallback(const std::function<void(std::optional<std::chrono::duration<double>>)>& cb);

    void updateReadWriteOptionalDurationProperty(std::optional<std::chrono::duration<double>>);

    void republishReadWriteOptionalDurationProperty() const;

    // ---read_write_two_durations Property---

    // Gets the latest value of the `read_write_two_durations` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<ReadWriteTwoDurationsProperty> getReadWriteTwoDurationsProperty();

    // Add a callback that will be called whenever the `read_write_two_durations` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_durations` property is received.
    void registerReadWriteTwoDurationsPropertyCallback(const std::function<void(std::chrono::duration<double>, std::optional<std::chrono::duration<double>>)>& cb);

    void updateReadWriteTwoDurationsProperty(std::chrono::duration<double>, std::optional<std::chrono::duration<double>>);

    void republishReadWriteTwoDurationsProperty() const;

    // ---read_write_binary Property---

    // Gets the latest value of the `read_write_binary` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::vector<uint8_t>> getReadWriteBinaryProperty();

    // Add a callback that will be called whenever the `read_write_binary` property is updated.
    // The provided method will be called whenever a new value for the `read_write_binary` property is received.
    void registerReadWriteBinaryPropertyCallback(const std::function<void(std::vector<uint8_t>)>& cb);

    void updateReadWriteBinaryProperty(std::vector<uint8_t>);

    void republishReadWriteBinaryProperty() const;

    // ---read_write_optional_binary Property---

    // Gets the latest value of the `read_write_optional_binary` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::vector<uint8_t>> getReadWriteOptionalBinaryProperty();

    // Add a callback that will be called whenever the `read_write_optional_binary` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_binary` property is received.
    void registerReadWriteOptionalBinaryPropertyCallback(const std::function<void(std::optional<std::vector<uint8_t>>)>& cb);

    void updateReadWriteOptionalBinaryProperty(std::optional<std::vector<uint8_t>>);

    void republishReadWriteOptionalBinaryProperty() const;

    // ---read_write_two_binaries Property---

    // Gets the latest value of the `read_write_two_binaries` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<ReadWriteTwoBinariesProperty> getReadWriteTwoBinariesProperty();

    // Add a callback that will be called whenever the `read_write_two_binaries` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_binaries` property is received.
    void registerReadWriteTwoBinariesPropertyCallback(const std::function<void(std::vector<uint8_t>, std::optional<std::vector<uint8_t>>)>& cb);

    void updateReadWriteTwoBinariesProperty(std::vector<uint8_t>, std::optional<std::vector<uint8_t>>);

    void republishReadWriteTwoBinariesProperty() const;

    // ---read_write_list_of_strings Property---

    // Gets the latest value of the `read_write_list_of_strings` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<std::vector<std::string>> getReadWriteListOfStringsProperty();

    // Add a callback that will be called whenever the `read_write_list_of_strings` property is updated.
    // The provided method will be called whenever a new value for the `read_write_list_of_strings` property is received.
    void registerReadWriteListOfStringsPropertyCallback(const std::function<void(std::vector<std::string>)>& cb);

    void updateReadWriteListOfStringsProperty(std::vector<std::string>);

    void republishReadWriteListOfStringsProperty() const;

    // ---read_write_lists Property---

    // Gets the latest value of the `read_write_lists` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    std::optional<ReadWriteListsProperty> getReadWriteListsProperty();

    // Add a callback that will be called whenever the `read_write_lists` property is updated.
    // The provided method will be called whenever a new value for the `read_write_lists` property is received.
    void registerReadWriteListsPropertyCallback(const std::function<void(std::vector<Numbers>, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>>)>& cb);

    void updateReadWriteListsProperty(std::vector<Numbers>, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>>);

    void republishReadWriteListsProperty() const;

private:
    std::shared_ptr<IBrokerConnection> _broker;
    std::string _instanceId;
    CallbackHandleType _brokerMessageCallbackHandle = 0;
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const MqttProperties& mqttProps
    );

    void _callCallWithNothingHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<void()> _callWithNothingHandler;
    int _callWithNothingMethodSubscriptionId;

    void _callCallOneIntegerHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<int(int)> _callOneIntegerHandler;
    int _callOneIntegerMethodSubscriptionId;

    void _callCallOptionalIntegerHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::optional<int>(std::optional<int>)> _callOptionalIntegerHandler;
    int _callOptionalIntegerMethodSubscriptionId;

    void _callCallThreeIntegersHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<CallThreeIntegersReturnValues(int, int, std::optional<int>)> _callThreeIntegersHandler;
    int _callThreeIntegersMethodSubscriptionId;

    void _callCallOneStringHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::string(std::string)> _callOneStringHandler;
    int _callOneStringMethodSubscriptionId;

    void _callCallOptionalStringHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::optional<std::string>(std::optional<std::string>)> _callOptionalStringHandler;
    int _callOptionalStringMethodSubscriptionId;

    void _callCallThreeStringsHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<CallThreeStringsReturnValues(std::string, std::optional<std::string>, std::string)> _callThreeStringsHandler;
    int _callThreeStringsMethodSubscriptionId;

    void _callCallOneEnumHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<Numbers(Numbers)> _callOneEnumHandler;
    int _callOneEnumMethodSubscriptionId;

    void _callCallOptionalEnumHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::optional<Numbers>(std::optional<Numbers>)> _callOptionalEnumHandler;
    int _callOptionalEnumMethodSubscriptionId;

    void _callCallThreeEnumsHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<CallThreeEnumsReturnValues(Numbers, Numbers, std::optional<Numbers>)> _callThreeEnumsHandler;
    int _callThreeEnumsMethodSubscriptionId;

    void _callCallOneStructHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<AllTypes(AllTypes)> _callOneStructHandler;
    int _callOneStructMethodSubscriptionId;

    void _callCallOptionalStructHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::optional<AllTypes>(std::optional<AllTypes>)> _callOptionalStructHandler;
    int _callOptionalStructMethodSubscriptionId;

    void _callCallThreeStructsHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<CallThreeStructsReturnValues(std::optional<AllTypes>, AllTypes, AllTypes)> _callThreeStructsHandler;
    int _callThreeStructsMethodSubscriptionId;

    void _callCallOneDateTimeHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::time_point<std::chrono::system_clock>)> _callOneDateTimeHandler;
    int _callOneDateTimeMethodSubscriptionId;

    void _callCallOptionalDateTimeHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::optional<std::chrono::time_point<std::chrono::system_clock>>(std::optional<std::chrono::time_point<std::chrono::system_clock>>)> _callOptionalDateTimeHandler;
    int _callOptionalDateTimeMethodSubscriptionId;

    void _callCallThreeDateTimesHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<CallThreeDateTimesReturnValues(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>)> _callThreeDateTimesHandler;
    int _callThreeDateTimesMethodSubscriptionId;

    void _callCallOneDurationHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::chrono::duration<double>(std::chrono::duration<double>)> _callOneDurationHandler;
    int _callOneDurationMethodSubscriptionId;

    void _callCallOptionalDurationHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::optional<std::chrono::duration<double>>(std::optional<std::chrono::duration<double>>)> _callOptionalDurationHandler;
    int _callOptionalDurationMethodSubscriptionId;

    void _callCallThreeDurationsHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<CallThreeDurationsReturnValues(std::chrono::duration<double>, std::chrono::duration<double>, std::optional<std::chrono::duration<double>>)> _callThreeDurationsHandler;
    int _callThreeDurationsMethodSubscriptionId;

    void _callCallOneBinaryHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::vector<uint8_t>(std::vector<uint8_t>)> _callOneBinaryHandler;
    int _callOneBinaryMethodSubscriptionId;

    void _callCallOptionalBinaryHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::optional<std::vector<uint8_t>>(std::optional<std::vector<uint8_t>>)> _callOptionalBinaryHandler;
    int _callOptionalBinaryMethodSubscriptionId;

    void _callCallThreeBinariesHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<CallThreeBinariesReturnValues(std::vector<uint8_t>, std::vector<uint8_t>, std::optional<std::vector<uint8_t>>)> _callThreeBinariesHandler;
    int _callThreeBinariesMethodSubscriptionId;

    void _callCallOneListOfIntegersHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::vector<int>(std::vector<int>)> _callOneListOfIntegersHandler;
    int _callOneListOfIntegersMethodSubscriptionId;

    void _callCallOptionalListOfFloatsHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<std::optional<std::vector<double>>(std::optional<std::vector<double>>)> _callOptionalListOfFloatsHandler;
    int _callOptionalListOfFloatsMethodSubscriptionId;

    void _callCallTwoListsHandler(const std::string& topic, const rapidjson::Document& doc, std::optional<std::string> clientId, std::optional<std::string> correlationId) const;
    std::function<CallTwoListsReturnValues(std::vector<Numbers>, std::optional<std::vector<std::string>>)> _callTwoListsHandler;
    int _callTwoListsMethodSubscriptionId;

    // ---------------- PROPERTIES ------------------

    // ---read_write_integer Property---

    // Current value for the `read_write_integer` property.
    std::optional<ReadWriteIntegerProperty> _readWriteIntegerProperty;

    // This is the property version  of `read_write_integer`.
    int _lastReadWriteIntegerPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_integer` property and its version.
    mutable std::mutex _readWriteIntegerPropertyMutex;

    // MQTT Subscription ID for `read_write_integer` property update requests.
    int _readWriteIntegerPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_integer` property.
    void _receiveReadWriteIntegerPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_integer` property.
    std::vector<std::function<void(int)>> _readWriteIntegerPropertyCallbacks;
    std::mutex _readWriteIntegerPropertyCallbacksMutex;

    // ---read_only_integer Property---

    // Current value for the `read_only_integer` property.
    std::optional<ReadOnlyIntegerProperty> _readOnlyIntegerProperty;

    // This is the property version  of `read_only_integer`.
    int _lastReadOnlyIntegerPropertyVersion = -1;

    // Mutex for protecting access to the `read_only_integer` property and its version.
    mutable std::mutex _readOnlyIntegerPropertyMutex;

    // MQTT Subscription ID for `read_only_integer` property update requests.
    int _readOnlyIntegerPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_only_integer` property.
    void _receiveReadOnlyIntegerPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_only_integer` property.
    std::vector<std::function<void(int)>> _readOnlyIntegerPropertyCallbacks;
    std::mutex _readOnlyIntegerPropertyCallbacksMutex;

    // ---read_write_optional_integer Property---

    // Current value for the `read_write_optional_integer` property.
    std::optional<ReadWriteOptionalIntegerProperty> _readWriteOptionalIntegerProperty;

    // This is the property version  of `read_write_optional_integer`.
    int _lastReadWriteOptionalIntegerPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_integer` property and its version.
    mutable std::mutex _readWriteOptionalIntegerPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_integer` property update requests.
    int _readWriteOptionalIntegerPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_integer` property.
    void _receiveReadWriteOptionalIntegerPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_integer` property.
    std::vector<std::function<void(std::optional<int>)>> _readWriteOptionalIntegerPropertyCallbacks;
    std::mutex _readWriteOptionalIntegerPropertyCallbacksMutex;

    // ---read_write_two_integers Property---

    // Current values for the `read_write_two_integers` property.
    std::optional<ReadWriteTwoIntegersProperty> _readWriteTwoIntegersProperty;

    // This is the property version  of `read_write_two_integers`.
    int _lastReadWriteTwoIntegersPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_integers` property and its version.
    mutable std::mutex _readWriteTwoIntegersPropertyMutex;

    // MQTT Subscription ID for `read_write_two_integers` property update requests.
    int _readWriteTwoIntegersPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_integers` property.
    void _receiveReadWriteTwoIntegersPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_integers` property.
    std::vector<std::function<void(int, std::optional<int>)>> _readWriteTwoIntegersPropertyCallbacks;
    std::mutex _readWriteTwoIntegersPropertyCallbacksMutex;

    // ---read_only_string Property---

    // Current value for the `read_only_string` property.
    std::optional<ReadOnlyStringProperty> _readOnlyStringProperty;

    // This is the property version  of `read_only_string`.
    int _lastReadOnlyStringPropertyVersion = -1;

    // Mutex for protecting access to the `read_only_string` property and its version.
    mutable std::mutex _readOnlyStringPropertyMutex;

    // MQTT Subscription ID for `read_only_string` property update requests.
    int _readOnlyStringPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_only_string` property.
    void _receiveReadOnlyStringPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_only_string` property.
    std::vector<std::function<void(std::string)>> _readOnlyStringPropertyCallbacks;
    std::mutex _readOnlyStringPropertyCallbacksMutex;

    // ---read_write_string Property---

    // Current value for the `read_write_string` property.
    std::optional<ReadWriteStringProperty> _readWriteStringProperty;

    // This is the property version  of `read_write_string`.
    int _lastReadWriteStringPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_string` property and its version.
    mutable std::mutex _readWriteStringPropertyMutex;

    // MQTT Subscription ID for `read_write_string` property update requests.
    int _readWriteStringPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_string` property.
    void _receiveReadWriteStringPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_string` property.
    std::vector<std::function<void(std::string)>> _readWriteStringPropertyCallbacks;
    std::mutex _readWriteStringPropertyCallbacksMutex;

    // ---read_write_optional_string Property---

    // Current value for the `read_write_optional_string` property.
    std::optional<ReadWriteOptionalStringProperty> _readWriteOptionalStringProperty;

    // This is the property version  of `read_write_optional_string`.
    int _lastReadWriteOptionalStringPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_string` property and its version.
    mutable std::mutex _readWriteOptionalStringPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_string` property update requests.
    int _readWriteOptionalStringPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_string` property.
    void _receiveReadWriteOptionalStringPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_string` property.
    std::vector<std::function<void(std::optional<std::string>)>> _readWriteOptionalStringPropertyCallbacks;
    std::mutex _readWriteOptionalStringPropertyCallbacksMutex;

    // ---read_write_two_strings Property---

    // Current values for the `read_write_two_strings` property.
    std::optional<ReadWriteTwoStringsProperty> _readWriteTwoStringsProperty;

    // This is the property version  of `read_write_two_strings`.
    int _lastReadWriteTwoStringsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_strings` property and its version.
    mutable std::mutex _readWriteTwoStringsPropertyMutex;

    // MQTT Subscription ID for `read_write_two_strings` property update requests.
    int _readWriteTwoStringsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_strings` property.
    void _receiveReadWriteTwoStringsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_strings` property.
    std::vector<std::function<void(std::string, std::optional<std::string>)>> _readWriteTwoStringsPropertyCallbacks;
    std::mutex _readWriteTwoStringsPropertyCallbacksMutex;

    // ---read_write_struct Property---

    // Current value for the `read_write_struct` property.
    std::optional<ReadWriteStructProperty> _readWriteStructProperty;

    // This is the property version  of `read_write_struct`.
    int _lastReadWriteStructPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_struct` property and its version.
    mutable std::mutex _readWriteStructPropertyMutex;

    // MQTT Subscription ID for `read_write_struct` property update requests.
    int _readWriteStructPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_struct` property.
    void _receiveReadWriteStructPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_struct` property.
    std::vector<std::function<void(AllTypes)>> _readWriteStructPropertyCallbacks;
    std::mutex _readWriteStructPropertyCallbacksMutex;

    // ---read_write_optional_struct Property---

    // Current value for the `read_write_optional_struct` property.
    std::optional<ReadWriteOptionalStructProperty> _readWriteOptionalStructProperty;

    // This is the property version  of `read_write_optional_struct`.
    int _lastReadWriteOptionalStructPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_struct` property and its version.
    mutable std::mutex _readWriteOptionalStructPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_struct` property update requests.
    int _readWriteOptionalStructPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_struct` property.
    void _receiveReadWriteOptionalStructPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_struct` property.
    std::vector<std::function<void(std::optional<AllTypes>)>> _readWriteOptionalStructPropertyCallbacks;
    std::mutex _readWriteOptionalStructPropertyCallbacksMutex;

    // ---read_write_two_structs Property---

    // Current values for the `read_write_two_structs` property.
    std::optional<ReadWriteTwoStructsProperty> _readWriteTwoStructsProperty;

    // This is the property version  of `read_write_two_structs`.
    int _lastReadWriteTwoStructsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_structs` property and its version.
    mutable std::mutex _readWriteTwoStructsPropertyMutex;

    // MQTT Subscription ID for `read_write_two_structs` property update requests.
    int _readWriteTwoStructsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_structs` property.
    void _receiveReadWriteTwoStructsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_structs` property.
    std::vector<std::function<void(AllTypes, std::optional<AllTypes>)>> _readWriteTwoStructsPropertyCallbacks;
    std::mutex _readWriteTwoStructsPropertyCallbacksMutex;

    // ---read_only_enum Property---

    // Current value for the `read_only_enum` property.
    std::optional<ReadOnlyEnumProperty> _readOnlyEnumProperty;

    // This is the property version  of `read_only_enum`.
    int _lastReadOnlyEnumPropertyVersion = -1;

    // Mutex for protecting access to the `read_only_enum` property and its version.
    mutable std::mutex _readOnlyEnumPropertyMutex;

    // MQTT Subscription ID for `read_only_enum` property update requests.
    int _readOnlyEnumPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_only_enum` property.
    void _receiveReadOnlyEnumPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_only_enum` property.
    std::vector<std::function<void(Numbers)>> _readOnlyEnumPropertyCallbacks;
    std::mutex _readOnlyEnumPropertyCallbacksMutex;

    // ---read_write_enum Property---

    // Current value for the `read_write_enum` property.
    std::optional<ReadWriteEnumProperty> _readWriteEnumProperty;

    // This is the property version  of `read_write_enum`.
    int _lastReadWriteEnumPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_enum` property and its version.
    mutable std::mutex _readWriteEnumPropertyMutex;

    // MQTT Subscription ID for `read_write_enum` property update requests.
    int _readWriteEnumPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_enum` property.
    void _receiveReadWriteEnumPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_enum` property.
    std::vector<std::function<void(Numbers)>> _readWriteEnumPropertyCallbacks;
    std::mutex _readWriteEnumPropertyCallbacksMutex;

    // ---read_write_optional_enum Property---

    // Current value for the `read_write_optional_enum` property.
    std::optional<ReadWriteOptionalEnumProperty> _readWriteOptionalEnumProperty;

    // This is the property version  of `read_write_optional_enum`.
    int _lastReadWriteOptionalEnumPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_enum` property and its version.
    mutable std::mutex _readWriteOptionalEnumPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_enum` property update requests.
    int _readWriteOptionalEnumPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_enum` property.
    void _receiveReadWriteOptionalEnumPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_enum` property.
    std::vector<std::function<void(std::optional<Numbers>)>> _readWriteOptionalEnumPropertyCallbacks;
    std::mutex _readWriteOptionalEnumPropertyCallbacksMutex;

    // ---read_write_two_enums Property---

    // Current values for the `read_write_two_enums` property.
    std::optional<ReadWriteTwoEnumsProperty> _readWriteTwoEnumsProperty;

    // This is the property version  of `read_write_two_enums`.
    int _lastReadWriteTwoEnumsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_enums` property and its version.
    mutable std::mutex _readWriteTwoEnumsPropertyMutex;

    // MQTT Subscription ID for `read_write_two_enums` property update requests.
    int _readWriteTwoEnumsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_enums` property.
    void _receiveReadWriteTwoEnumsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_enums` property.
    std::vector<std::function<void(Numbers, std::optional<Numbers>)>> _readWriteTwoEnumsPropertyCallbacks;
    std::mutex _readWriteTwoEnumsPropertyCallbacksMutex;

    // ---read_write_datetime Property---

    // Current value for the `read_write_datetime` property.
    std::optional<ReadWriteDatetimeProperty> _readWriteDatetimeProperty;

    // This is the property version  of `read_write_datetime`.
    int _lastReadWriteDatetimePropertyVersion = -1;

    // Mutex for protecting access to the `read_write_datetime` property and its version.
    mutable std::mutex _readWriteDatetimePropertyMutex;

    // MQTT Subscription ID for `read_write_datetime` property update requests.
    int _readWriteDatetimePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_datetime` property.
    void _receiveReadWriteDatetimePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_datetime` property.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>)>> _readWriteDatetimePropertyCallbacks;
    std::mutex _readWriteDatetimePropertyCallbacksMutex;

    // ---read_write_optional_datetime Property---

    // Current value for the `read_write_optional_datetime` property.
    std::optional<ReadWriteOptionalDatetimeProperty> _readWriteOptionalDatetimeProperty;

    // This is the property version  of `read_write_optional_datetime`.
    int _lastReadWriteOptionalDatetimePropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_datetime` property and its version.
    mutable std::mutex _readWriteOptionalDatetimePropertyMutex;

    // MQTT Subscription ID for `read_write_optional_datetime` property update requests.
    int _readWriteOptionalDatetimePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_datetime` property.
    void _receiveReadWriteOptionalDatetimePropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_datetime` property.
    std::vector<std::function<void(std::optional<std::chrono::time_point<std::chrono::system_clock>>)>> _readWriteOptionalDatetimePropertyCallbacks;
    std::mutex _readWriteOptionalDatetimePropertyCallbacksMutex;

    // ---read_write_two_datetimes Property---

    // Current values for the `read_write_two_datetimes` property.
    std::optional<ReadWriteTwoDatetimesProperty> _readWriteTwoDatetimesProperty;

    // This is the property version  of `read_write_two_datetimes`.
    int _lastReadWriteTwoDatetimesPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_datetimes` property and its version.
    mutable std::mutex _readWriteTwoDatetimesPropertyMutex;

    // MQTT Subscription ID for `read_write_two_datetimes` property update requests.
    int _readWriteTwoDatetimesPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_datetimes` property.
    void _receiveReadWriteTwoDatetimesPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_datetimes` property.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>)>> _readWriteTwoDatetimesPropertyCallbacks;
    std::mutex _readWriteTwoDatetimesPropertyCallbacksMutex;

    // ---read_write_duration Property---

    // Current value for the `read_write_duration` property.
    std::optional<ReadWriteDurationProperty> _readWriteDurationProperty;

    // This is the property version  of `read_write_duration`.
    int _lastReadWriteDurationPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_duration` property and its version.
    mutable std::mutex _readWriteDurationPropertyMutex;

    // MQTT Subscription ID for `read_write_duration` property update requests.
    int _readWriteDurationPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_duration` property.
    void _receiveReadWriteDurationPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_duration` property.
    std::vector<std::function<void(std::chrono::duration<double>)>> _readWriteDurationPropertyCallbacks;
    std::mutex _readWriteDurationPropertyCallbacksMutex;

    // ---read_write_optional_duration Property---

    // Current value for the `read_write_optional_duration` property.
    std::optional<ReadWriteOptionalDurationProperty> _readWriteOptionalDurationProperty;

    // This is the property version  of `read_write_optional_duration`.
    int _lastReadWriteOptionalDurationPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_duration` property and its version.
    mutable std::mutex _readWriteOptionalDurationPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_duration` property update requests.
    int _readWriteOptionalDurationPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_duration` property.
    void _receiveReadWriteOptionalDurationPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_duration` property.
    std::vector<std::function<void(std::optional<std::chrono::duration<double>>)>> _readWriteOptionalDurationPropertyCallbacks;
    std::mutex _readWriteOptionalDurationPropertyCallbacksMutex;

    // ---read_write_two_durations Property---

    // Current values for the `read_write_two_durations` property.
    std::optional<ReadWriteTwoDurationsProperty> _readWriteTwoDurationsProperty;

    // This is the property version  of `read_write_two_durations`.
    int _lastReadWriteTwoDurationsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_durations` property and its version.
    mutable std::mutex _readWriteTwoDurationsPropertyMutex;

    // MQTT Subscription ID for `read_write_two_durations` property update requests.
    int _readWriteTwoDurationsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_durations` property.
    void _receiveReadWriteTwoDurationsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_durations` property.
    std::vector<std::function<void(std::chrono::duration<double>, std::optional<std::chrono::duration<double>>)>> _readWriteTwoDurationsPropertyCallbacks;
    std::mutex _readWriteTwoDurationsPropertyCallbacksMutex;

    // ---read_write_binary Property---

    // Current value for the `read_write_binary` property.
    std::optional<ReadWriteBinaryProperty> _readWriteBinaryProperty;

    // This is the property version  of `read_write_binary`.
    int _lastReadWriteBinaryPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_binary` property and its version.
    mutable std::mutex _readWriteBinaryPropertyMutex;

    // MQTT Subscription ID for `read_write_binary` property update requests.
    int _readWriteBinaryPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_binary` property.
    void _receiveReadWriteBinaryPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_binary` property.
    std::vector<std::function<void(std::vector<uint8_t>)>> _readWriteBinaryPropertyCallbacks;
    std::mutex _readWriteBinaryPropertyCallbacksMutex;

    // ---read_write_optional_binary Property---

    // Current value for the `read_write_optional_binary` property.
    std::optional<ReadWriteOptionalBinaryProperty> _readWriteOptionalBinaryProperty;

    // This is the property version  of `read_write_optional_binary`.
    int _lastReadWriteOptionalBinaryPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_binary` property and its version.
    mutable std::mutex _readWriteOptionalBinaryPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_binary` property update requests.
    int _readWriteOptionalBinaryPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_binary` property.
    void _receiveReadWriteOptionalBinaryPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_binary` property.
    std::vector<std::function<void(std::optional<std::vector<uint8_t>>)>> _readWriteOptionalBinaryPropertyCallbacks;
    std::mutex _readWriteOptionalBinaryPropertyCallbacksMutex;

    // ---read_write_two_binaries Property---

    // Current values for the `read_write_two_binaries` property.
    std::optional<ReadWriteTwoBinariesProperty> _readWriteTwoBinariesProperty;

    // This is the property version  of `read_write_two_binaries`.
    int _lastReadWriteTwoBinariesPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_binaries` property and its version.
    mutable std::mutex _readWriteTwoBinariesPropertyMutex;

    // MQTT Subscription ID for `read_write_two_binaries` property update requests.
    int _readWriteTwoBinariesPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_binaries` property.
    void _receiveReadWriteTwoBinariesPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_binaries` property.
    std::vector<std::function<void(std::vector<uint8_t>, std::optional<std::vector<uint8_t>>)>> _readWriteTwoBinariesPropertyCallbacks;
    std::mutex _readWriteTwoBinariesPropertyCallbacksMutex;

    // ---read_write_list_of_strings Property---

    // Current value for the `read_write_list_of_strings` property.
    std::optional<ReadWriteListOfStringsProperty> _readWriteListOfStringsProperty;

    // This is the property version  of `read_write_list_of_strings`.
    int _lastReadWriteListOfStringsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_list_of_strings` property and its version.
    mutable std::mutex _readWriteListOfStringsPropertyMutex;

    // MQTT Subscription ID for `read_write_list_of_strings` property update requests.
    int _readWriteListOfStringsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_list_of_strings` property.
    void _receiveReadWriteListOfStringsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_list_of_strings` property.
    std::vector<std::function<void(std::vector<std::string>)>> _readWriteListOfStringsPropertyCallbacks;
    std::mutex _readWriteListOfStringsPropertyCallbacksMutex;

    // ---read_write_lists Property---

    // Current values for the `read_write_lists` property.
    std::optional<ReadWriteListsProperty> _readWriteListsProperty;

    // This is the property version  of `read_write_lists`.
    int _lastReadWriteListsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_lists` property and its version.
    mutable std::mutex _readWriteListsPropertyMutex;

    // MQTT Subscription ID for `read_write_lists` property update requests.
    int _readWriteListsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_lists` property.
    void _receiveReadWriteListsPropertyUpdate(const std::string& topic, const std::string& payload, std::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_lists` property.
    std::vector<std::function<void(std::vector<Numbers>, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>>)>> _readWriteListsPropertyCallbacks;
    std::mutex _readWriteListsPropertyCallbacksMutex;

    // ---------------- SERVICE ADVERTISEMENT ------------------

    // Thread for publishing service advertisement messages
    std::thread _advertisementThread;

    // Flag to signal the advertisement thread to stop
    std::atomic<bool> _advertisementThreadRunning;

    // Method that runs in the advertisement thread
    void _advertisementThreadLoop();
};