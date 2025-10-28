/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once

#include <cstdint>
#include <functional>
#include <map>
#include <memory>
#include <exception>
#include <mutex>
#include <chrono>
#include <rapidjson/document.h>
#include <boost/uuid/uuid.hpp>
#include <boost/optional.hpp>
#include "ibrokerconnection.hpp"
#include "enums.hpp"
#include "method_payloads.hpp"
#include "signal_payloads.hpp"

#include "property_structs.hpp"

class TestAbleClient
{
public:
    // This is the name of the API.
    static constexpr const char NAME[] = "Test Able";
    // This is the version of the API contract.
    static constexpr const char INTERFACE_VERSION[] = "0.0.1";

    // Constructor taking a connection object.
    TestAbleClient(std::shared_ptr<IBrokerConnection> broker, const std::string& instanceId);

    virtual ~TestAbleClient();
    // ------------------ SIGNALS --------------------

    // Register a callback for the `empty` signal.
    // The provided method will be called whenever a `empty` is received.
    void registerEmptyCallback(const std::function<void()>& cb);

    // Register a callback for the `singleInt` signal.
    // The provided method will be called whenever a `singleInt` is received.
    void registerSingleIntCallback(const std::function<void(int)>& cb);

    // Register a callback for the `singleOptionalInt` signal.  The argument is optional.
    // The provided method will be called whenever a `singleOptionalInt` is received.
    void registerSingleOptionalIntCallback(const std::function<void(boost::optional<int>)>& cb);

    // Register a callback for the `threeIntegers` signal.
    // The provided method will be called whenever a `threeIntegers` is received.
    void registerThreeIntegersCallback(const std::function<void(int, int, boost::optional<int>)>& cb);

    // Register a callback for the `singleString` signal.
    // The provided method will be called whenever a `singleString` is received.
    void registerSingleStringCallback(const std::function<void(std::string)>& cb);

    // Register a callback for the `singleOptionalString` signal.  The argument is optional.
    // The provided method will be called whenever a `singleOptionalString` is received.
    void registerSingleOptionalStringCallback(const std::function<void(boost::optional<std::string>)>& cb);

    // Register a callback for the `threeStrings` signal.
    // The provided method will be called whenever a `threeStrings` is received.
    void registerThreeStringsCallback(const std::function<void(std::string, std::string, boost::optional<std::string>)>& cb);

    // Register a callback for the `singleEnum` signal.
    // The provided method will be called whenever a `singleEnum` is received.
    void registerSingleEnumCallback(const std::function<void(Numbers)>& cb);

    // Register a callback for the `singleOptionalEnum` signal.  The argument is optional.
    // The provided method will be called whenever a `singleOptionalEnum` is received.
    void registerSingleOptionalEnumCallback(const std::function<void(boost::optional<Numbers>)>& cb);

    // Register a callback for the `threeEnums` signal.
    // The provided method will be called whenever a `threeEnums` is received.
    void registerThreeEnumsCallback(const std::function<void(Numbers, Numbers, boost::optional<Numbers>)>& cb);

    // Register a callback for the `singleStruct` signal.
    // The provided method will be called whenever a `singleStruct` is received.
    void registerSingleStructCallback(const std::function<void(AllTypes)>& cb);

    // Register a callback for the `singleOptionalStruct` signal.  The argument is optional.
    // The provided method will be called whenever a `singleOptionalStruct` is received.
    void registerSingleOptionalStructCallback(const std::function<void(boost::optional<AllTypes>)>& cb);

    // Register a callback for the `threeStructs` signal.
    // The provided method will be called whenever a `threeStructs` is received.
    void registerThreeStructsCallback(const std::function<void(AllTypes, AllTypes, boost::optional<AllTypes>)>& cb);

    // Register a callback for the `singleDateTime` signal.
    // The provided method will be called whenever a `singleDateTime` is received.
    void registerSingleDateTimeCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb);

    // Register a callback for the `singleOptionalDatetime` signal.  The argument is optional.
    // The provided method will be called whenever a `singleOptionalDatetime` is received.
    void registerSingleOptionalDatetimeCallback(const std::function<void(boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb);

    // Register a callback for the `threeDateTimes` signal.
    // The provided method will be called whenever a `threeDateTimes` is received.
    void registerThreeDateTimesCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb);

    // Register a callback for the `singleDuration` signal.
    // The provided method will be called whenever a `singleDuration` is received.
    void registerSingleDurationCallback(const std::function<void(std::chrono::duration<double>)>& cb);

    // Register a callback for the `singleOptionalDuration` signal.  The argument is optional.
    // The provided method will be called whenever a `singleOptionalDuration` is received.
    void registerSingleOptionalDurationCallback(const std::function<void(boost::optional<std::chrono::duration<double>>)>& cb);

    // Register a callback for the `threeDurations` signal.
    // The provided method will be called whenever a `threeDurations` is received.
    void registerThreeDurationsCallback(const std::function<void(std::chrono::duration<double>, std::chrono::duration<double>, boost::optional<std::chrono::duration<double>>)>& cb);

    // Register a callback for the `singleBinary` signal.
    // The provided method will be called whenever a `singleBinary` is received.
    void registerSingleBinaryCallback(const std::function<void(std::vector<uint8_t>)>& cb);

    // Register a callback for the `singleOptionalBinary` signal.  The argument is optional.
    // The provided method will be called whenever a `singleOptionalBinary` is received.
    void registerSingleOptionalBinaryCallback(const std::function<void(boost::optional<std::vector<uint8_t>>)>& cb);

    // Register a callback for the `threeBinaries` signal.
    // The provided method will be called whenever a `threeBinaries` is received.
    void registerThreeBinariesCallback(const std::function<void(std::vector<uint8_t>, std::vector<uint8_t>, boost::optional<std::vector<uint8_t>>)>& cb);

    // Register a callback for the `singleArrayOfIntegers` signal.
    // The provided method will be called whenever a `singleArrayOfIntegers` is received.
    void registerSingleArrayOfIntegersCallback(const std::function<void(std::vector<int>)>& cb);

    // Register a callback for the `singleOptionalArrayOfStrings` signal.  The argument is optional.
    // The provided method will be called whenever a `singleOptionalArrayOfStrings` is received.
    void registerSingleOptionalArrayOfStringsCallback(const std::function<void(boost::optional<std::vector<std::string>>)>& cb);

    // Register a callback for the `arrayOfEveryType` signal.
    // The provided method will be called whenever a `arrayOfEveryType` is received.
    void registerArrayOfEveryTypeCallback(const std::function<void(std::vector<int>, std::vector<double>, std::vector<std::string>, std::vector<Numbers>, std::vector<Entry>, std::vector<std::chrono::time_point<std::chrono::system_clock>>, std::vector<std::chrono::duration<double>>, std::vector<std::vector<uint8_t>>)>& cb);

    // ------------------- METHODS --------------------

    // Calls the `callWithNothing` method.
    // Returns a future.  When that future resolves, it will have the returned value. None
    boost::future<void> callWithNothing();

    // Calls the `callOneInteger` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgPrimitive name=output1 type=int>
    boost::future<int> callOneInteger(int input1);

    // Calls the `callOptionalInteger` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgPrimitive name=output1 type=int>
    boost::future<boost::optional<int>> callOptionalInteger(boost::optional<int> input1);

    // Calls the `callThreeIntegers` method.
    // Returns a future.  When that future resolves, it will have the returned value. [<ArgPrimitive name=output1 type=int>, <ArgPrimitive name=output2 type=int>, <ArgPrimitive name=output3 type=int>]
    boost::future<CallThreeIntegersReturnValues> callThreeIntegers(int input1, int input2, boost::optional<int> input3);

    // Calls the `callOneString` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgPrimitive name=output1 type=str>
    boost::future<std::string> callOneString(std::string input1);

    // Calls the `callOptionalString` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgPrimitive name=output1 type=str>
    boost::future<boost::optional<std::string>> callOptionalString(boost::optional<std::string> input1);

    // Calls the `callThreeStrings` method.
    // Returns a future.  When that future resolves, it will have the returned value. [<ArgPrimitive name=output1 type=str>, <ArgPrimitive name=output2 type=str>, <ArgPrimitive name=output3 type=str>]
    boost::future<CallThreeStringsReturnValues> callThreeStrings(std::string input1, boost::optional<std::string> input2, std::string input3);

    // Calls the `callOneEnum` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgEnum name=output1>
    boost::future<Numbers> callOneEnum(Numbers input1);

    // Calls the `callOptionalEnum` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgEnum name=output1>
    boost::future<boost::optional<Numbers>> callOptionalEnum(boost::optional<Numbers> input1);

    // Calls the `callThreeEnums` method.
    // Returns a future.  When that future resolves, it will have the returned value. [<ArgEnum name=output1>, <ArgEnum name=output2>, <ArgEnum name=output3>]
    boost::future<CallThreeEnumsReturnValues> callThreeEnums(Numbers input1, Numbers input2, boost::optional<Numbers> input3);

    // Calls the `callOneStruct` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgStruct name=output1>
    boost::future<AllTypes> callOneStruct(AllTypes input1);

    // Calls the `callOptionalStruct` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgStruct name=output1>
    boost::future<boost::optional<AllTypes>> callOptionalStruct(boost::optional<AllTypes> input1);

    // Calls the `callThreeStructs` method.
    // Returns a future.  When that future resolves, it will have the returned value. [ArgStruct(name=output1, iface_struct=<InterfaceStruct members=['the_bool', 'the_int', 'the_number', 'the_str', 'the_enum', 'an_entry_object', 'date_and_time', 'time_duration', 'data', 'OptionalInteger', 'OptionalString', 'OptionalEnum', 'optionalEntryObject', 'OptionalDateTime', 'OptionalDuration', 'OptionalBinary', 'array_of_integers', 'optional_array_of_integers', 'array_of_strings', 'optional_array_of_strings', 'array_of_enums', 'optional_array_of_enums', 'array_of_datetimes', 'optional_array_of_datetimes', 'array_of_durations', 'optional_array_of_durations', 'array_of_binaries', 'optional_array_of_binaries', 'array_of_entry_objects', 'optional_array_of_entry_objects']>), ArgStruct(name=output2, iface_struct=<InterfaceStruct members=['the_bool', 'the_int', 'the_number', 'the_str', 'the_enum', 'an_entry_object', 'date_and_time', 'time_duration', 'data', 'OptionalInteger', 'OptionalString', 'OptionalEnum', 'optionalEntryObject', 'OptionalDateTime', 'OptionalDuration', 'OptionalBinary', 'array_of_integers', 'optional_array_of_integers', 'array_of_strings', 'optional_array_of_strings', 'array_of_enums', 'optional_array_of_enums', 'array_of_datetimes', 'optional_array_of_datetimes', 'array_of_durations', 'optional_array_of_durations', 'array_of_binaries', 'optional_array_of_binaries', 'array_of_entry_objects', 'optional_array_of_entry_objects']>), ArgStruct(name=output3, iface_struct=<InterfaceStruct members=['the_bool', 'the_int', 'the_number', 'the_str', 'the_enum', 'an_entry_object', 'date_and_time', 'time_duration', 'data', 'OptionalInteger', 'OptionalString', 'OptionalEnum', 'optionalEntryObject', 'OptionalDateTime', 'OptionalDuration', 'OptionalBinary', 'array_of_integers', 'optional_array_of_integers', 'array_of_strings', 'optional_array_of_strings', 'array_of_enums', 'optional_array_of_enums', 'array_of_datetimes', 'optional_array_of_datetimes', 'array_of_durations', 'optional_array_of_durations', 'array_of_binaries', 'optional_array_of_binaries', 'array_of_entry_objects', 'optional_array_of_entry_objects']>)]
    boost::future<CallThreeStructsReturnValues> callThreeStructs(boost::optional<AllTypes> input1, AllTypes input2, AllTypes input3);

    // Calls the `callOneDateTime` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgDateTime name=output1>
    boost::future<std::chrono::time_point<std::chrono::system_clock>> callOneDateTime(std::chrono::time_point<std::chrono::system_clock> input1);

    // Calls the `callOptionalDateTime` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgDateTime name=output1>
    boost::future<boost::optional<std::chrono::time_point<std::chrono::system_clock>>> callOptionalDateTime(boost::optional<std::chrono::time_point<std::chrono::system_clock>> input1);

    // Calls the `callThreeDateTimes` method.
    // Returns a future.  When that future resolves, it will have the returned value. [ArgDateTime(name=output1), ArgDateTime(name=output2), ArgDateTime(name=output3)]
    boost::future<CallThreeDateTimesReturnValues> callThreeDateTimes(std::chrono::time_point<std::chrono::system_clock> input1, std::chrono::time_point<std::chrono::system_clock> input2, boost::optional<std::chrono::time_point<std::chrono::system_clock>> input3);

    // Calls the `callOneDuration` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgDuration name=output1>
    boost::future<std::chrono::duration<double>> callOneDuration(std::chrono::duration<double> input1);

    // Calls the `callOptionalDuration` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgDuration name=output1>
    boost::future<boost::optional<std::chrono::duration<double>>> callOptionalDuration(boost::optional<std::chrono::duration<double>> input1);

    // Calls the `callThreeDurations` method.
    // Returns a future.  When that future resolves, it will have the returned value. [ArgDuration(name=output1), ArgDuration(name=output2), ArgDuration(name=output3)]
    boost::future<CallThreeDurationsReturnValues> callThreeDurations(std::chrono::duration<double> input1, std::chrono::duration<double> input2, boost::optional<std::chrono::duration<double>> input3);

    // Calls the `callOneBinary` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgBinary name=output1>
    boost::future<std::vector<uint8_t>> callOneBinary(std::vector<uint8_t> input1);

    // Calls the `callOptionalBinary` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgBinary name=output1>
    boost::future<boost::optional<std::vector<uint8_t>>> callOptionalBinary(boost::optional<std::vector<uint8_t>> input1);

    // Calls the `callThreeBinaries` method.
    // Returns a future.  When that future resolves, it will have the returned value. [ArgBinary(name=output1), ArgBinary(name=output2), ArgBinary(name=output3)]
    boost::future<CallThreeBinariesReturnValues> callThreeBinaries(std::vector<uint8_t> input1, std::vector<uint8_t> input2, boost::optional<std::vector<uint8_t>> input3);

    // Calls the `callOneListOfIntegers` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgArray name=output1 element_type=<ArgPrimitive name=name_not_used_in_array_element type=int>>
    boost::future<std::vector<int>> callOneListOfIntegers(std::vector<int> input1);

    // Calls the `callOptionalListOfFloats` method.
    // Returns a future.  When that future resolves, it will have the returned value. <ArgArray name=output1 element_type=<ArgPrimitive name=name_not_used_in_array_element type=float>>
    boost::future<boost::optional<std::vector<double>>> callOptionalListOfFloats(boost::optional<std::vector<double>> input1);

    // Calls the `callTwoLists` method.
    // Returns a future.  When that future resolves, it will have the returned value. [ArgArray(name=output1, element_type=<ArgEnum name=name_not_used_in_array_element>), ArgArray(name=output2, element_type=<ArgPrimitive name=name_not_used_in_array_element type=str>)]
    boost::future<CallTwoListsReturnValues> callTwoLists(std::vector<Numbers> input1, boost::optional<std::vector<std::string>> input2);

    // ---------------- PROPERTIES ------------------

    // ---read_write_integer Property---

    // Gets the latest value of the `read_write_integer` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<int> getReadWriteIntegerProperty() const;

    // Add a callback that will be called whenever the `read_write_integer` property is updated.
    // The provided method will be called whenever a new value for the `read_write_integer` property is received.
    void registerReadWriteIntegerPropertyCallback(const std::function<void(int)>& cb);

    boost::future<bool> updateReadWriteIntegerProperty(int) const;

    // ---read_only_integer Property---

    // Gets the latest value of the `read_only_integer` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<int> getReadOnlyIntegerProperty() const;

    // Add a callback that will be called whenever the `read_only_integer` property is updated.
    // The provided method will be called whenever a new value for the `read_only_integer` property is received.
    void registerReadOnlyIntegerPropertyCallback(const std::function<void(int)>& cb);

    // ---read_write_optional_integer Property---

    // Gets the latest value of the `read_write_optional_integer` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<int> getReadWriteOptionalIntegerProperty() const;

    // Add a callback that will be called whenever the `read_write_optional_integer` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_integer` property is received.
    void registerReadWriteOptionalIntegerPropertyCallback(const std::function<void(boost::optional<int>)>& cb);

    boost::future<bool> updateReadWriteOptionalIntegerProperty(boost::optional<int>) const;

    // ---read_write_two_integers Property---

    // Gets the latest value of the `read_write_two_integers` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<ReadWriteTwoIntegersProperty> getReadWriteTwoIntegersProperty() const;

    // Add a callback that will be called whenever the `read_write_two_integers` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_integers` property is received.
    void registerReadWriteTwoIntegersPropertyCallback(const std::function<void(int, boost::optional<int>)>& cb);

    boost::future<bool> updateReadWriteTwoIntegersProperty(int, boost::optional<int>) const;

    // ---read_only_string Property---

    // Gets the latest value of the `read_only_string` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<const std::string&> getReadOnlyStringProperty() const;

    // Add a callback that will be called whenever the `read_only_string` property is updated.
    // The provided method will be called whenever a new value for the `read_only_string` property is received.
    void registerReadOnlyStringPropertyCallback(const std::function<void(std::string)>& cb);

    // ---read_write_string Property---

    // Gets the latest value of the `read_write_string` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<const std::string&> getReadWriteStringProperty() const;

    // Add a callback that will be called whenever the `read_write_string` property is updated.
    // The provided method will be called whenever a new value for the `read_write_string` property is received.
    void registerReadWriteStringPropertyCallback(const std::function<void(std::string)>& cb);

    boost::future<bool> updateReadWriteStringProperty(std::string) const;

    // ---read_write_optional_string Property---

    // Gets the latest value of the `read_write_optional_string` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<std::string> getReadWriteOptionalStringProperty() const;

    // Add a callback that will be called whenever the `read_write_optional_string` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_string` property is received.
    void registerReadWriteOptionalStringPropertyCallback(const std::function<void(boost::optional<std::string>)>& cb);

    boost::future<bool> updateReadWriteOptionalStringProperty(boost::optional<std::string>) const;

    // ---read_write_two_strings Property---

    // Gets the latest value of the `read_write_two_strings` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<ReadWriteTwoStringsProperty> getReadWriteTwoStringsProperty() const;

    // Add a callback that will be called whenever the `read_write_two_strings` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_strings` property is received.
    void registerReadWriteTwoStringsPropertyCallback(const std::function<void(std::string, boost::optional<std::string>)>& cb);

    boost::future<bool> updateReadWriteTwoStringsProperty(std::string, boost::optional<std::string>) const;

    // ---read_write_struct Property---

    // Gets the latest value of the `read_write_struct` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<AllTypes> getReadWriteStructProperty() const;

    // Add a callback that will be called whenever the `read_write_struct` property is updated.
    // The provided method will be called whenever a new value for the `read_write_struct` property is received.
    void registerReadWriteStructPropertyCallback(const std::function<void(AllTypes)>& cb);

    boost::future<bool> updateReadWriteStructProperty(AllTypes) const;

    // ---read_write_optional_struct Property---

    // Gets the latest value of the `read_write_optional_struct` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<AllTypes> getReadWriteOptionalStructProperty() const;

    // Add a callback that will be called whenever the `read_write_optional_struct` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_struct` property is received.
    void registerReadWriteOptionalStructPropertyCallback(const std::function<void(boost::optional<AllTypes>)>& cb);

    boost::future<bool> updateReadWriteOptionalStructProperty(boost::optional<AllTypes>) const;

    // ---read_write_two_structs Property---

    // Gets the latest value of the `read_write_two_structs` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<ReadWriteTwoStructsProperty> getReadWriteTwoStructsProperty() const;

    // Add a callback that will be called whenever the `read_write_two_structs` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_structs` property is received.
    void registerReadWriteTwoStructsPropertyCallback(const std::function<void(AllTypes, boost::optional<AllTypes>)>& cb);

    boost::future<bool> updateReadWriteTwoStructsProperty(AllTypes, boost::optional<AllTypes>) const;

    // ---read_only_enum Property---

    // Gets the latest value of the `read_only_enum` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<Numbers> getReadOnlyEnumProperty() const;

    // Add a callback that will be called whenever the `read_only_enum` property is updated.
    // The provided method will be called whenever a new value for the `read_only_enum` property is received.
    void registerReadOnlyEnumPropertyCallback(const std::function<void(Numbers)>& cb);

    // ---read_write_enum Property---

    // Gets the latest value of the `read_write_enum` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<Numbers> getReadWriteEnumProperty() const;

    // Add a callback that will be called whenever the `read_write_enum` property is updated.
    // The provided method will be called whenever a new value for the `read_write_enum` property is received.
    void registerReadWriteEnumPropertyCallback(const std::function<void(Numbers)>& cb);

    boost::future<bool> updateReadWriteEnumProperty(Numbers) const;

    // ---read_write_optional_enum Property---

    // Gets the latest value of the `read_write_optional_enum` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<Numbers> getReadWriteOptionalEnumProperty() const;

    // Add a callback that will be called whenever the `read_write_optional_enum` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_enum` property is received.
    void registerReadWriteOptionalEnumPropertyCallback(const std::function<void(boost::optional<Numbers>)>& cb);

    boost::future<bool> updateReadWriteOptionalEnumProperty(boost::optional<Numbers>) const;

    // ---read_write_two_enums Property---

    // Gets the latest value of the `read_write_two_enums` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<ReadWriteTwoEnumsProperty> getReadWriteTwoEnumsProperty() const;

    // Add a callback that will be called whenever the `read_write_two_enums` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_enums` property is received.
    void registerReadWriteTwoEnumsPropertyCallback(const std::function<void(Numbers, boost::optional<Numbers>)>& cb);

    boost::future<bool> updateReadWriteTwoEnumsProperty(Numbers, boost::optional<Numbers>) const;

    // ---read_write_datetime Property---

    // Gets the latest value of the `read_write_datetime` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<std::chrono::time_point<std::chrono::system_clock>> getReadWriteDatetimeProperty() const;

    // Add a callback that will be called whenever the `read_write_datetime` property is updated.
    // The provided method will be called whenever a new value for the `read_write_datetime` property is received.
    void registerReadWriteDatetimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb);

    boost::future<bool> updateReadWriteDatetimeProperty(std::chrono::time_point<std::chrono::system_clock>) const;

    // ---read_write_optional_datetime Property---

    // Gets the latest value of the `read_write_optional_datetime` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<std::chrono::time_point<std::chrono::system_clock>> getReadWriteOptionalDatetimeProperty() const;

    // Add a callback that will be called whenever the `read_write_optional_datetime` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_datetime` property is received.
    void registerReadWriteOptionalDatetimePropertyCallback(const std::function<void(boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb);

    boost::future<bool> updateReadWriteOptionalDatetimeProperty(boost::optional<std::chrono::time_point<std::chrono::system_clock>>) const;

    // ---read_write_two_datetimes Property---

    // Gets the latest value of the `read_write_two_datetimes` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<ReadWriteTwoDatetimesProperty> getReadWriteTwoDatetimesProperty() const;

    // Add a callback that will be called whenever the `read_write_two_datetimes` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_datetimes` property is received.
    void registerReadWriteTwoDatetimesPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb);

    boost::future<bool> updateReadWriteTwoDatetimesProperty(std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>) const;

    // ---read_write_duration Property---

    // Gets the latest value of the `read_write_duration` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<std::chrono::duration<double>> getReadWriteDurationProperty() const;

    // Add a callback that will be called whenever the `read_write_duration` property is updated.
    // The provided method will be called whenever a new value for the `read_write_duration` property is received.
    void registerReadWriteDurationPropertyCallback(const std::function<void(std::chrono::duration<double>)>& cb);

    boost::future<bool> updateReadWriteDurationProperty(std::chrono::duration<double>) const;

    // ---read_write_optional_duration Property---

    // Gets the latest value of the `read_write_optional_duration` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<std::chrono::duration<double>> getReadWriteOptionalDurationProperty() const;

    // Add a callback that will be called whenever the `read_write_optional_duration` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_duration` property is received.
    void registerReadWriteOptionalDurationPropertyCallback(const std::function<void(boost::optional<std::chrono::duration<double>>)>& cb);

    boost::future<bool> updateReadWriteOptionalDurationProperty(boost::optional<std::chrono::duration<double>>) const;

    // ---read_write_two_durations Property---

    // Gets the latest value of the `read_write_two_durations` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<ReadWriteTwoDurationsProperty> getReadWriteTwoDurationsProperty() const;

    // Add a callback that will be called whenever the `read_write_two_durations` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_durations` property is received.
    void registerReadWriteTwoDurationsPropertyCallback(const std::function<void(std::chrono::duration<double>, boost::optional<std::chrono::duration<double>>)>& cb);

    boost::future<bool> updateReadWriteTwoDurationsProperty(std::chrono::duration<double>, boost::optional<std::chrono::duration<double>>) const;

    // ---read_write_binary Property---

    // Gets the latest value of the `read_write_binary` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<std::vector<uint8_t>> getReadWriteBinaryProperty() const;

    // Add a callback that will be called whenever the `read_write_binary` property is updated.
    // The provided method will be called whenever a new value for the `read_write_binary` property is received.
    void registerReadWriteBinaryPropertyCallback(const std::function<void(std::vector<uint8_t>)>& cb);

    boost::future<bool> updateReadWriteBinaryProperty(std::vector<uint8_t>) const;

    // ---read_write_optional_binary Property---

    // Gets the latest value of the `read_write_optional_binary` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<std::vector<uint8_t>> getReadWriteOptionalBinaryProperty() const;

    // Add a callback that will be called whenever the `read_write_optional_binary` property is updated.
    // The provided method will be called whenever a new value for the `read_write_optional_binary` property is received.
    void registerReadWriteOptionalBinaryPropertyCallback(const std::function<void(boost::optional<std::vector<uint8_t>>)>& cb);

    boost::future<bool> updateReadWriteOptionalBinaryProperty(boost::optional<std::vector<uint8_t>>) const;

    // ---read_write_two_binaries Property---

    // Gets the latest value of the `read_write_two_binaries` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<ReadWriteTwoBinariesProperty> getReadWriteTwoBinariesProperty() const;

    // Add a callback that will be called whenever the `read_write_two_binaries` property is updated.
    // The provided method will be called whenever a new value for the `read_write_two_binaries` property is received.
    void registerReadWriteTwoBinariesPropertyCallback(const std::function<void(std::vector<uint8_t>, boost::optional<std::vector<uint8_t>>)>& cb);

    boost::future<bool> updateReadWriteTwoBinariesProperty(std::vector<uint8_t>, boost::optional<std::vector<uint8_t>>) const;

    // ---read_write_list_of_strings Property---

    // Gets the latest value of the `read_write_list_of_strings` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<std::vector<std::string>> getReadWriteListOfStringsProperty() const;

    // Add a callback that will be called whenever the `read_write_list_of_strings` property is updated.
    // The provided method will be called whenever a new value for the `read_write_list_of_strings` property is received.
    void registerReadWriteListOfStringsPropertyCallback(const std::function<void(std::vector<std::string>)>& cb);

    boost::future<bool> updateReadWriteListOfStringsProperty(std::vector<std::string>) const;

    // ---read_write_lists Property---

    // Gets the latest value of the `read_write_lists` property, if one has been received.
    // If no value has been received yet, an empty optional is returned.

    boost::optional<ReadWriteListsProperty> getReadWriteListsProperty() const;

    // Add a callback that will be called whenever the `read_write_lists` property is updated.
    // The provided method will be called whenever a new value for the `read_write_lists` property is received.
    void registerReadWriteListsPropertyCallback(const std::function<void(std::vector<Numbers>, boost::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>>)>& cb);

    boost::future<bool> updateReadWriteListsProperty(std::vector<Numbers>, boost::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>>) const;

private:
    // Pointer to the broker connection.
    std::shared_ptr<IBrokerConnection> _broker;

    // Service Instance ID that this client is connected to.
    std::string _instanceId;

    CallbackHandleType _brokerMessageCallbackHandle = 0;

    // Internal method for receiving messages from the broker.
    void _receiveMessage(
            const std::string& topic,
            const std::string& payload,
            const MqttProperties& mqttProps
    );

    // ------------------ SIGNALS --------------------

    // List of callbacks to be called whenever the `empty` signal is received.
    std::vector<std::function<void()>> _emptySignalCallbacks;
    std::mutex _emptySignalCallbacksMutex;

    // MQTT Subscription ID for `empty` signal receptions.
    int _emptySignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleInt` signal is received.
    std::vector<std::function<void(int)>> _singleIntSignalCallbacks;
    std::mutex _singleIntSignalCallbacksMutex;

    // MQTT Subscription ID for `singleInt` signal receptions.
    int _singleIntSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleOptionalInt` signal is received.
    std::vector<std::function<void(boost::optional<int>)>> _singleOptionalIntSignalCallbacks;
    std::mutex _singleOptionalIntSignalCallbacksMutex;

    // MQTT Subscription ID for `singleOptionalInt` signal receptions.
    int _singleOptionalIntSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `threeIntegers` signal is received.
    std::vector<std::function<void(int, int, boost::optional<int>)>> _threeIntegersSignalCallbacks;
    std::mutex _threeIntegersSignalCallbacksMutex;

    // MQTT Subscription ID for `threeIntegers` signal receptions.
    int _threeIntegersSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleString` signal is received.
    std::vector<std::function<void(std::string)>> _singleStringSignalCallbacks;
    std::mutex _singleStringSignalCallbacksMutex;

    // MQTT Subscription ID for `singleString` signal receptions.
    int _singleStringSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleOptionalString` signal is received.
    std::vector<std::function<void(boost::optional<std::string>)>> _singleOptionalStringSignalCallbacks;
    std::mutex _singleOptionalStringSignalCallbacksMutex;

    // MQTT Subscription ID for `singleOptionalString` signal receptions.
    int _singleOptionalStringSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `threeStrings` signal is received.
    std::vector<std::function<void(std::string, std::string, boost::optional<std::string>)>> _threeStringsSignalCallbacks;
    std::mutex _threeStringsSignalCallbacksMutex;

    // MQTT Subscription ID for `threeStrings` signal receptions.
    int _threeStringsSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleEnum` signal is received.
    std::vector<std::function<void(Numbers)>> _singleEnumSignalCallbacks;
    std::mutex _singleEnumSignalCallbacksMutex;

    // MQTT Subscription ID for `singleEnum` signal receptions.
    int _singleEnumSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleOptionalEnum` signal is received.
    std::vector<std::function<void(boost::optional<Numbers>)>> _singleOptionalEnumSignalCallbacks;
    std::mutex _singleOptionalEnumSignalCallbacksMutex;

    // MQTT Subscription ID for `singleOptionalEnum` signal receptions.
    int _singleOptionalEnumSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `threeEnums` signal is received.
    std::vector<std::function<void(Numbers, Numbers, boost::optional<Numbers>)>> _threeEnumsSignalCallbacks;
    std::mutex _threeEnumsSignalCallbacksMutex;

    // MQTT Subscription ID for `threeEnums` signal receptions.
    int _threeEnumsSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleStruct` signal is received.
    std::vector<std::function<void(AllTypes)>> _singleStructSignalCallbacks;
    std::mutex _singleStructSignalCallbacksMutex;

    // MQTT Subscription ID for `singleStruct` signal receptions.
    int _singleStructSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleOptionalStruct` signal is received.
    std::vector<std::function<void(boost::optional<AllTypes>)>> _singleOptionalStructSignalCallbacks;
    std::mutex _singleOptionalStructSignalCallbacksMutex;

    // MQTT Subscription ID for `singleOptionalStruct` signal receptions.
    int _singleOptionalStructSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `threeStructs` signal is received.
    std::vector<std::function<void(AllTypes, AllTypes, boost::optional<AllTypes>)>> _threeStructsSignalCallbacks;
    std::mutex _threeStructsSignalCallbacksMutex;

    // MQTT Subscription ID for `threeStructs` signal receptions.
    int _threeStructsSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleDateTime` signal is received.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>)>> _singleDateTimeSignalCallbacks;
    std::mutex _singleDateTimeSignalCallbacksMutex;

    // MQTT Subscription ID for `singleDateTime` signal receptions.
    int _singleDateTimeSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleOptionalDatetime` signal is received.
    std::vector<std::function<void(boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>> _singleOptionalDatetimeSignalCallbacks;
    std::mutex _singleOptionalDatetimeSignalCallbacksMutex;

    // MQTT Subscription ID for `singleOptionalDatetime` signal receptions.
    int _singleOptionalDatetimeSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `threeDateTimes` signal is received.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>> _threeDateTimesSignalCallbacks;
    std::mutex _threeDateTimesSignalCallbacksMutex;

    // MQTT Subscription ID for `threeDateTimes` signal receptions.
    int _threeDateTimesSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleDuration` signal is received.
    std::vector<std::function<void(std::chrono::duration<double>)>> _singleDurationSignalCallbacks;
    std::mutex _singleDurationSignalCallbacksMutex;

    // MQTT Subscription ID for `singleDuration` signal receptions.
    int _singleDurationSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleOptionalDuration` signal is received.
    std::vector<std::function<void(boost::optional<std::chrono::duration<double>>)>> _singleOptionalDurationSignalCallbacks;
    std::mutex _singleOptionalDurationSignalCallbacksMutex;

    // MQTT Subscription ID for `singleOptionalDuration` signal receptions.
    int _singleOptionalDurationSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `threeDurations` signal is received.
    std::vector<std::function<void(std::chrono::duration<double>, std::chrono::duration<double>, boost::optional<std::chrono::duration<double>>)>> _threeDurationsSignalCallbacks;
    std::mutex _threeDurationsSignalCallbacksMutex;

    // MQTT Subscription ID for `threeDurations` signal receptions.
    int _threeDurationsSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleBinary` signal is received.
    std::vector<std::function<void(std::vector<uint8_t>)>> _singleBinarySignalCallbacks;
    std::mutex _singleBinarySignalCallbacksMutex;

    // MQTT Subscription ID for `singleBinary` signal receptions.
    int _singleBinarySignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleOptionalBinary` signal is received.
    std::vector<std::function<void(boost::optional<std::vector<uint8_t>>)>> _singleOptionalBinarySignalCallbacks;
    std::mutex _singleOptionalBinarySignalCallbacksMutex;

    // MQTT Subscription ID for `singleOptionalBinary` signal receptions.
    int _singleOptionalBinarySignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `threeBinaries` signal is received.
    std::vector<std::function<void(std::vector<uint8_t>, std::vector<uint8_t>, boost::optional<std::vector<uint8_t>>)>> _threeBinariesSignalCallbacks;
    std::mutex _threeBinariesSignalCallbacksMutex;

    // MQTT Subscription ID for `threeBinaries` signal receptions.
    int _threeBinariesSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleArrayOfIntegers` signal is received.
    std::vector<std::function<void(std::vector<int>)>> _singleArrayOfIntegersSignalCallbacks;
    std::mutex _singleArrayOfIntegersSignalCallbacksMutex;

    // MQTT Subscription ID for `singleArrayOfIntegers` signal receptions.
    int _singleArrayOfIntegersSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `singleOptionalArrayOfStrings` signal is received.
    std::vector<std::function<void(boost::optional<std::vector<std::string>>)>> _singleOptionalArrayOfStringsSignalCallbacks;
    std::mutex _singleOptionalArrayOfStringsSignalCallbacksMutex;

    // MQTT Subscription ID for `singleOptionalArrayOfStrings` signal receptions.
    int _singleOptionalArrayOfStringsSignalSubscriptionId = -1;

    // List of callbacks to be called whenever the `arrayOfEveryType` signal is received.
    std::vector<std::function<void(std::vector<int>, std::vector<double>, std::vector<std::string>, std::vector<Numbers>, std::vector<Entry>, std::vector<std::chrono::time_point<std::chrono::system_clock>>, std::vector<std::chrono::duration<double>>, std::vector<std::vector<uint8_t>>)>> _arrayOfEveryTypeSignalCallbacks;
    std::mutex _arrayOfEveryTypeSignalCallbacksMutex;

    // MQTT Subscription ID for `arrayOfEveryType` signal receptions.
    int _arrayOfEveryTypeSignalSubscriptionId = -1;

    // ------------------- METHODS --------------------
    // Holds promises for pending `callWithNothing` method calls.
    std::map<boost::uuids::uuid, boost::promise<void>> _pendingCallWithNothingMethodCalls;
    int _callWithNothingMethodSubscriptionId = -1;
    // This is called internally to process responses to `callWithNothing` method calls.
    void _handleCallWithNothingResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOneInteger` method calls.
    std::map<boost::uuids::uuid, boost::promise<int>> _pendingCallOneIntegerMethodCalls;
    int _callOneIntegerMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOneInteger` method calls.
    void _handleCallOneIntegerResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOptionalInteger` method calls.
    std::map<boost::uuids::uuid, boost::promise<boost::optional<int>>> _pendingCallOptionalIntegerMethodCalls;
    int _callOptionalIntegerMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOptionalInteger` method calls.
    void _handleCallOptionalIntegerResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callThreeIntegers` method calls.
    std::map<boost::uuids::uuid, boost::promise<CallThreeIntegersReturnValues>> _pendingCallThreeIntegersMethodCalls;
    int _callThreeIntegersMethodSubscriptionId = -1;
    // This is called internally to process responses to `callThreeIntegers` method calls.
    void _handleCallThreeIntegersResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOneString` method calls.
    std::map<boost::uuids::uuid, boost::promise<std::string>> _pendingCallOneStringMethodCalls;
    int _callOneStringMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOneString` method calls.
    void _handleCallOneStringResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOptionalString` method calls.
    std::map<boost::uuids::uuid, boost::promise<boost::optional<std::string>>> _pendingCallOptionalStringMethodCalls;
    int _callOptionalStringMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOptionalString` method calls.
    void _handleCallOptionalStringResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callThreeStrings` method calls.
    std::map<boost::uuids::uuid, boost::promise<CallThreeStringsReturnValues>> _pendingCallThreeStringsMethodCalls;
    int _callThreeStringsMethodSubscriptionId = -1;
    // This is called internally to process responses to `callThreeStrings` method calls.
    void _handleCallThreeStringsResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOneEnum` method calls.
    std::map<boost::uuids::uuid, boost::promise<Numbers>> _pendingCallOneEnumMethodCalls;
    int _callOneEnumMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOneEnum` method calls.
    void _handleCallOneEnumResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOptionalEnum` method calls.
    std::map<boost::uuids::uuid, boost::promise<boost::optional<Numbers>>> _pendingCallOptionalEnumMethodCalls;
    int _callOptionalEnumMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOptionalEnum` method calls.
    void _handleCallOptionalEnumResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callThreeEnums` method calls.
    std::map<boost::uuids::uuid, boost::promise<CallThreeEnumsReturnValues>> _pendingCallThreeEnumsMethodCalls;
    int _callThreeEnumsMethodSubscriptionId = -1;
    // This is called internally to process responses to `callThreeEnums` method calls.
    void _handleCallThreeEnumsResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOneStruct` method calls.
    std::map<boost::uuids::uuid, boost::promise<AllTypes>> _pendingCallOneStructMethodCalls;
    int _callOneStructMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOneStruct` method calls.
    void _handleCallOneStructResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOptionalStruct` method calls.
    std::map<boost::uuids::uuid, boost::promise<boost::optional<AllTypes>>> _pendingCallOptionalStructMethodCalls;
    int _callOptionalStructMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOptionalStruct` method calls.
    void _handleCallOptionalStructResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callThreeStructs` method calls.
    std::map<boost::uuids::uuid, boost::promise<CallThreeStructsReturnValues>> _pendingCallThreeStructsMethodCalls;
    int _callThreeStructsMethodSubscriptionId = -1;
    // This is called internally to process responses to `callThreeStructs` method calls.
    void _handleCallThreeStructsResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOneDateTime` method calls.
    std::map<boost::uuids::uuid, boost::promise<std::chrono::time_point<std::chrono::system_clock>>> _pendingCallOneDateTimeMethodCalls;
    int _callOneDateTimeMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOneDateTime` method calls.
    void _handleCallOneDateTimeResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOptionalDateTime` method calls.
    std::map<boost::uuids::uuid, boost::promise<boost::optional<std::chrono::time_point<std::chrono::system_clock>>>> _pendingCallOptionalDateTimeMethodCalls;
    int _callOptionalDateTimeMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOptionalDateTime` method calls.
    void _handleCallOptionalDateTimeResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callThreeDateTimes` method calls.
    std::map<boost::uuids::uuid, boost::promise<CallThreeDateTimesReturnValues>> _pendingCallThreeDateTimesMethodCalls;
    int _callThreeDateTimesMethodSubscriptionId = -1;
    // This is called internally to process responses to `callThreeDateTimes` method calls.
    void _handleCallThreeDateTimesResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOneDuration` method calls.
    std::map<boost::uuids::uuid, boost::promise<std::chrono::duration<double>>> _pendingCallOneDurationMethodCalls;
    int _callOneDurationMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOneDuration` method calls.
    void _handleCallOneDurationResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOptionalDuration` method calls.
    std::map<boost::uuids::uuid, boost::promise<boost::optional<std::chrono::duration<double>>>> _pendingCallOptionalDurationMethodCalls;
    int _callOptionalDurationMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOptionalDuration` method calls.
    void _handleCallOptionalDurationResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callThreeDurations` method calls.
    std::map<boost::uuids::uuid, boost::promise<CallThreeDurationsReturnValues>> _pendingCallThreeDurationsMethodCalls;
    int _callThreeDurationsMethodSubscriptionId = -1;
    // This is called internally to process responses to `callThreeDurations` method calls.
    void _handleCallThreeDurationsResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOneBinary` method calls.
    std::map<boost::uuids::uuid, boost::promise<std::vector<uint8_t>>> _pendingCallOneBinaryMethodCalls;
    int _callOneBinaryMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOneBinary` method calls.
    void _handleCallOneBinaryResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOptionalBinary` method calls.
    std::map<boost::uuids::uuid, boost::promise<boost::optional<std::vector<uint8_t>>>> _pendingCallOptionalBinaryMethodCalls;
    int _callOptionalBinaryMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOptionalBinary` method calls.
    void _handleCallOptionalBinaryResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callThreeBinaries` method calls.
    std::map<boost::uuids::uuid, boost::promise<CallThreeBinariesReturnValues>> _pendingCallThreeBinariesMethodCalls;
    int _callThreeBinariesMethodSubscriptionId = -1;
    // This is called internally to process responses to `callThreeBinaries` method calls.
    void _handleCallThreeBinariesResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOneListOfIntegers` method calls.
    std::map<boost::uuids::uuid, boost::promise<std::vector<int>>> _pendingCallOneListOfIntegersMethodCalls;
    int _callOneListOfIntegersMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOneListOfIntegers` method calls.
    void _handleCallOneListOfIntegersResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callOptionalListOfFloats` method calls.
    std::map<boost::uuids::uuid, boost::promise<boost::optional<std::vector<double>>>> _pendingCallOptionalListOfFloatsMethodCalls;
    int _callOptionalListOfFloatsMethodSubscriptionId = -1;
    // This is called internally to process responses to `callOptionalListOfFloats` method calls.
    void _handleCallOptionalListOfFloatsResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // Holds promises for pending `callTwoLists` method calls.
    std::map<boost::uuids::uuid, boost::promise<CallTwoListsReturnValues>> _pendingCallTwoListsMethodCalls;
    int _callTwoListsMethodSubscriptionId = -1;
    // This is called internally to process responses to `callTwoLists` method calls.
    void _handleCallTwoListsResponse(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps);

    // ---------------- PROPERTIES ------------------

    // ---read_write_integer Property---

    // Last received value for the `read_write_integer` property.
    boost::optional<ReadWriteIntegerProperty> _readWriteIntegerProperty;

    // This is the property version of the last received `read_write_integer` property update.
    int _lastReadWriteIntegerPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_integer` property and its version.
    mutable std::mutex _readWriteIntegerPropertyMutex;

    // MQTT Subscription ID for `read_write_integer` property updates.
    int _readWriteIntegerPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_integer` property.
    void _receiveReadWriteIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_integer` property.
    std::vector<std::function<void(int)>> _readWriteIntegerPropertyCallbacks;
    std::mutex _readWriteIntegerPropertyCallbacksMutex;

    // ---read_only_integer Property---

    // Last received value for the `read_only_integer` property.
    boost::optional<ReadOnlyIntegerProperty> _readOnlyIntegerProperty;

    // This is the property version of the last received `read_only_integer` property update.
    int _lastReadOnlyIntegerPropertyVersion = -1;

    // Mutex for protecting access to the `read_only_integer` property and its version.
    mutable std::mutex _readOnlyIntegerPropertyMutex;

    // MQTT Subscription ID for `read_only_integer` property updates.
    int _readOnlyIntegerPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_only_integer` property.
    void _receiveReadOnlyIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_only_integer` property.
    std::vector<std::function<void(int)>> _readOnlyIntegerPropertyCallbacks;
    std::mutex _readOnlyIntegerPropertyCallbacksMutex;

    // ---read_write_optional_integer Property---

    // Last received value for the `read_write_optional_integer` property.
    boost::optional<ReadWriteOptionalIntegerProperty> _readWriteOptionalIntegerProperty;

    // This is the property version of the last received `read_write_optional_integer` property update.
    int _lastReadWriteOptionalIntegerPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_integer` property and its version.
    mutable std::mutex _readWriteOptionalIntegerPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_integer` property updates.
    int _readWriteOptionalIntegerPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_integer` property.
    void _receiveReadWriteOptionalIntegerPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_integer` property.
    std::vector<std::function<void(boost::optional<int>)>> _readWriteOptionalIntegerPropertyCallbacks;
    std::mutex _readWriteOptionalIntegerPropertyCallbacksMutex;

    // ---read_write_two_integers Property---

    // Last received values for the `read_write_two_integers` property.
    boost::optional<ReadWriteTwoIntegersProperty> _readWriteTwoIntegersProperty;

    // This is the property version of the last received `read_write_two_integers` property update.
    int _lastReadWriteTwoIntegersPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_integers` property and its version.
    mutable std::mutex _readWriteTwoIntegersPropertyMutex;

    // MQTT Subscription ID for `read_write_two_integers` property updates.
    int _readWriteTwoIntegersPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_integers` property.
    void _receiveReadWriteTwoIntegersPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_integers` property.
    std::vector<std::function<void(int, boost::optional<int>)>> _readWriteTwoIntegersPropertyCallbacks;
    std::mutex _readWriteTwoIntegersPropertyCallbacksMutex;

    // ---read_only_string Property---

    // Last received value for the `read_only_string` property.
    boost::optional<ReadOnlyStringProperty> _readOnlyStringProperty;

    // This is the property version of the last received `read_only_string` property update.
    int _lastReadOnlyStringPropertyVersion = -1;

    // Mutex for protecting access to the `read_only_string` property and its version.
    mutable std::mutex _readOnlyStringPropertyMutex;

    // MQTT Subscription ID for `read_only_string` property updates.
    int _readOnlyStringPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_only_string` property.
    void _receiveReadOnlyStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_only_string` property.
    std::vector<std::function<void(std::string)>> _readOnlyStringPropertyCallbacks;
    std::mutex _readOnlyStringPropertyCallbacksMutex;

    // ---read_write_string Property---

    // Last received value for the `read_write_string` property.
    boost::optional<ReadWriteStringProperty> _readWriteStringProperty;

    // This is the property version of the last received `read_write_string` property update.
    int _lastReadWriteStringPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_string` property and its version.
    mutable std::mutex _readWriteStringPropertyMutex;

    // MQTT Subscription ID for `read_write_string` property updates.
    int _readWriteStringPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_string` property.
    void _receiveReadWriteStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_string` property.
    std::vector<std::function<void(std::string)>> _readWriteStringPropertyCallbacks;
    std::mutex _readWriteStringPropertyCallbacksMutex;

    // ---read_write_optional_string Property---

    // Last received value for the `read_write_optional_string` property.
    boost::optional<ReadWriteOptionalStringProperty> _readWriteOptionalStringProperty;

    // This is the property version of the last received `read_write_optional_string` property update.
    int _lastReadWriteOptionalStringPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_string` property and its version.
    mutable std::mutex _readWriteOptionalStringPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_string` property updates.
    int _readWriteOptionalStringPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_string` property.
    void _receiveReadWriteOptionalStringPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_string` property.
    std::vector<std::function<void(boost::optional<std::string>)>> _readWriteOptionalStringPropertyCallbacks;
    std::mutex _readWriteOptionalStringPropertyCallbacksMutex;

    // ---read_write_two_strings Property---

    // Last received values for the `read_write_two_strings` property.
    boost::optional<ReadWriteTwoStringsProperty> _readWriteTwoStringsProperty;

    // This is the property version of the last received `read_write_two_strings` property update.
    int _lastReadWriteTwoStringsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_strings` property and its version.
    mutable std::mutex _readWriteTwoStringsPropertyMutex;

    // MQTT Subscription ID for `read_write_two_strings` property updates.
    int _readWriteTwoStringsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_strings` property.
    void _receiveReadWriteTwoStringsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_strings` property.
    std::vector<std::function<void(std::string, boost::optional<std::string>)>> _readWriteTwoStringsPropertyCallbacks;
    std::mutex _readWriteTwoStringsPropertyCallbacksMutex;

    // ---read_write_struct Property---

    // Last received value for the `read_write_struct` property.
    boost::optional<ReadWriteStructProperty> _readWriteStructProperty;

    // This is the property version of the last received `read_write_struct` property update.
    int _lastReadWriteStructPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_struct` property and its version.
    mutable std::mutex _readWriteStructPropertyMutex;

    // MQTT Subscription ID for `read_write_struct` property updates.
    int _readWriteStructPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_struct` property.
    void _receiveReadWriteStructPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_struct` property.
    std::vector<std::function<void(AllTypes)>> _readWriteStructPropertyCallbacks;
    std::mutex _readWriteStructPropertyCallbacksMutex;

    // ---read_write_optional_struct Property---

    // Last received value for the `read_write_optional_struct` property.
    boost::optional<ReadWriteOptionalStructProperty> _readWriteOptionalStructProperty;

    // This is the property version of the last received `read_write_optional_struct` property update.
    int _lastReadWriteOptionalStructPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_struct` property and its version.
    mutable std::mutex _readWriteOptionalStructPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_struct` property updates.
    int _readWriteOptionalStructPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_struct` property.
    void _receiveReadWriteOptionalStructPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_struct` property.
    std::vector<std::function<void(boost::optional<AllTypes>)>> _readWriteOptionalStructPropertyCallbacks;
    std::mutex _readWriteOptionalStructPropertyCallbacksMutex;

    // ---read_write_two_structs Property---

    // Last received values for the `read_write_two_structs` property.
    boost::optional<ReadWriteTwoStructsProperty> _readWriteTwoStructsProperty;

    // This is the property version of the last received `read_write_two_structs` property update.
    int _lastReadWriteTwoStructsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_structs` property and its version.
    mutable std::mutex _readWriteTwoStructsPropertyMutex;

    // MQTT Subscription ID for `read_write_two_structs` property updates.
    int _readWriteTwoStructsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_structs` property.
    void _receiveReadWriteTwoStructsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_structs` property.
    std::vector<std::function<void(AllTypes, boost::optional<AllTypes>)>> _readWriteTwoStructsPropertyCallbacks;
    std::mutex _readWriteTwoStructsPropertyCallbacksMutex;

    // ---read_only_enum Property---

    // Last received value for the `read_only_enum` property.
    boost::optional<ReadOnlyEnumProperty> _readOnlyEnumProperty;

    // This is the property version of the last received `read_only_enum` property update.
    int _lastReadOnlyEnumPropertyVersion = -1;

    // Mutex for protecting access to the `read_only_enum` property and its version.
    mutable std::mutex _readOnlyEnumPropertyMutex;

    // MQTT Subscription ID for `read_only_enum` property updates.
    int _readOnlyEnumPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_only_enum` property.
    void _receiveReadOnlyEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_only_enum` property.
    std::vector<std::function<void(Numbers)>> _readOnlyEnumPropertyCallbacks;
    std::mutex _readOnlyEnumPropertyCallbacksMutex;

    // ---read_write_enum Property---

    // Last received value for the `read_write_enum` property.
    boost::optional<ReadWriteEnumProperty> _readWriteEnumProperty;

    // This is the property version of the last received `read_write_enum` property update.
    int _lastReadWriteEnumPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_enum` property and its version.
    mutable std::mutex _readWriteEnumPropertyMutex;

    // MQTT Subscription ID for `read_write_enum` property updates.
    int _readWriteEnumPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_enum` property.
    void _receiveReadWriteEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_enum` property.
    std::vector<std::function<void(Numbers)>> _readWriteEnumPropertyCallbacks;
    std::mutex _readWriteEnumPropertyCallbacksMutex;

    // ---read_write_optional_enum Property---

    // Last received value for the `read_write_optional_enum` property.
    boost::optional<ReadWriteOptionalEnumProperty> _readWriteOptionalEnumProperty;

    // This is the property version of the last received `read_write_optional_enum` property update.
    int _lastReadWriteOptionalEnumPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_enum` property and its version.
    mutable std::mutex _readWriteOptionalEnumPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_enum` property updates.
    int _readWriteOptionalEnumPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_enum` property.
    void _receiveReadWriteOptionalEnumPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_enum` property.
    std::vector<std::function<void(boost::optional<Numbers>)>> _readWriteOptionalEnumPropertyCallbacks;
    std::mutex _readWriteOptionalEnumPropertyCallbacksMutex;

    // ---read_write_two_enums Property---

    // Last received values for the `read_write_two_enums` property.
    boost::optional<ReadWriteTwoEnumsProperty> _readWriteTwoEnumsProperty;

    // This is the property version of the last received `read_write_two_enums` property update.
    int _lastReadWriteTwoEnumsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_enums` property and its version.
    mutable std::mutex _readWriteTwoEnumsPropertyMutex;

    // MQTT Subscription ID for `read_write_two_enums` property updates.
    int _readWriteTwoEnumsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_enums` property.
    void _receiveReadWriteTwoEnumsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_enums` property.
    std::vector<std::function<void(Numbers, boost::optional<Numbers>)>> _readWriteTwoEnumsPropertyCallbacks;
    std::mutex _readWriteTwoEnumsPropertyCallbacksMutex;

    // ---read_write_datetime Property---

    // Last received value for the `read_write_datetime` property.
    boost::optional<ReadWriteDatetimeProperty> _readWriteDatetimeProperty;

    // This is the property version of the last received `read_write_datetime` property update.
    int _lastReadWriteDatetimePropertyVersion = -1;

    // Mutex for protecting access to the `read_write_datetime` property and its version.
    mutable std::mutex _readWriteDatetimePropertyMutex;

    // MQTT Subscription ID for `read_write_datetime` property updates.
    int _readWriteDatetimePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_datetime` property.
    void _receiveReadWriteDatetimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_datetime` property.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>)>> _readWriteDatetimePropertyCallbacks;
    std::mutex _readWriteDatetimePropertyCallbacksMutex;

    // ---read_write_optional_datetime Property---

    // Last received value for the `read_write_optional_datetime` property.
    boost::optional<ReadWriteOptionalDatetimeProperty> _readWriteOptionalDatetimeProperty;

    // This is the property version of the last received `read_write_optional_datetime` property update.
    int _lastReadWriteOptionalDatetimePropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_datetime` property and its version.
    mutable std::mutex _readWriteOptionalDatetimePropertyMutex;

    // MQTT Subscription ID for `read_write_optional_datetime` property updates.
    int _readWriteOptionalDatetimePropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_datetime` property.
    void _receiveReadWriteOptionalDatetimePropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_datetime` property.
    std::vector<std::function<void(boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>> _readWriteOptionalDatetimePropertyCallbacks;
    std::mutex _readWriteOptionalDatetimePropertyCallbacksMutex;

    // ---read_write_two_datetimes Property---

    // Last received values for the `read_write_two_datetimes` property.
    boost::optional<ReadWriteTwoDatetimesProperty> _readWriteTwoDatetimesProperty;

    // This is the property version of the last received `read_write_two_datetimes` property update.
    int _lastReadWriteTwoDatetimesPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_datetimes` property and its version.
    mutable std::mutex _readWriteTwoDatetimesPropertyMutex;

    // MQTT Subscription ID for `read_write_two_datetimes` property updates.
    int _readWriteTwoDatetimesPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_datetimes` property.
    void _receiveReadWriteTwoDatetimesPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_datetimes` property.
    std::vector<std::function<void(std::chrono::time_point<std::chrono::system_clock>, boost::optional<std::chrono::time_point<std::chrono::system_clock>>)>> _readWriteTwoDatetimesPropertyCallbacks;
    std::mutex _readWriteTwoDatetimesPropertyCallbacksMutex;

    // ---read_write_duration Property---

    // Last received value for the `read_write_duration` property.
    boost::optional<ReadWriteDurationProperty> _readWriteDurationProperty;

    // This is the property version of the last received `read_write_duration` property update.
    int _lastReadWriteDurationPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_duration` property and its version.
    mutable std::mutex _readWriteDurationPropertyMutex;

    // MQTT Subscription ID for `read_write_duration` property updates.
    int _readWriteDurationPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_duration` property.
    void _receiveReadWriteDurationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_duration` property.
    std::vector<std::function<void(std::chrono::duration<double>)>> _readWriteDurationPropertyCallbacks;
    std::mutex _readWriteDurationPropertyCallbacksMutex;

    // ---read_write_optional_duration Property---

    // Last received value for the `read_write_optional_duration` property.
    boost::optional<ReadWriteOptionalDurationProperty> _readWriteOptionalDurationProperty;

    // This is the property version of the last received `read_write_optional_duration` property update.
    int _lastReadWriteOptionalDurationPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_duration` property and its version.
    mutable std::mutex _readWriteOptionalDurationPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_duration` property updates.
    int _readWriteOptionalDurationPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_duration` property.
    void _receiveReadWriteOptionalDurationPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_duration` property.
    std::vector<std::function<void(boost::optional<std::chrono::duration<double>>)>> _readWriteOptionalDurationPropertyCallbacks;
    std::mutex _readWriteOptionalDurationPropertyCallbacksMutex;

    // ---read_write_two_durations Property---

    // Last received values for the `read_write_two_durations` property.
    boost::optional<ReadWriteTwoDurationsProperty> _readWriteTwoDurationsProperty;

    // This is the property version of the last received `read_write_two_durations` property update.
    int _lastReadWriteTwoDurationsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_durations` property and its version.
    mutable std::mutex _readWriteTwoDurationsPropertyMutex;

    // MQTT Subscription ID for `read_write_two_durations` property updates.
    int _readWriteTwoDurationsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_durations` property.
    void _receiveReadWriteTwoDurationsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_durations` property.
    std::vector<std::function<void(std::chrono::duration<double>, boost::optional<std::chrono::duration<double>>)>> _readWriteTwoDurationsPropertyCallbacks;
    std::mutex _readWriteTwoDurationsPropertyCallbacksMutex;

    // ---read_write_binary Property---

    // Last received value for the `read_write_binary` property.
    boost::optional<ReadWriteBinaryProperty> _readWriteBinaryProperty;

    // This is the property version of the last received `read_write_binary` property update.
    int _lastReadWriteBinaryPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_binary` property and its version.
    mutable std::mutex _readWriteBinaryPropertyMutex;

    // MQTT Subscription ID for `read_write_binary` property updates.
    int _readWriteBinaryPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_binary` property.
    void _receiveReadWriteBinaryPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_binary` property.
    std::vector<std::function<void(std::vector<uint8_t>)>> _readWriteBinaryPropertyCallbacks;
    std::mutex _readWriteBinaryPropertyCallbacksMutex;

    // ---read_write_optional_binary Property---

    // Last received value for the `read_write_optional_binary` property.
    boost::optional<ReadWriteOptionalBinaryProperty> _readWriteOptionalBinaryProperty;

    // This is the property version of the last received `read_write_optional_binary` property update.
    int _lastReadWriteOptionalBinaryPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_optional_binary` property and its version.
    mutable std::mutex _readWriteOptionalBinaryPropertyMutex;

    // MQTT Subscription ID for `read_write_optional_binary` property updates.
    int _readWriteOptionalBinaryPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_optional_binary` property.
    void _receiveReadWriteOptionalBinaryPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_optional_binary` property.
    std::vector<std::function<void(boost::optional<std::vector<uint8_t>>)>> _readWriteOptionalBinaryPropertyCallbacks;
    std::mutex _readWriteOptionalBinaryPropertyCallbacksMutex;

    // ---read_write_two_binaries Property---

    // Last received values for the `read_write_two_binaries` property.
    boost::optional<ReadWriteTwoBinariesProperty> _readWriteTwoBinariesProperty;

    // This is the property version of the last received `read_write_two_binaries` property update.
    int _lastReadWriteTwoBinariesPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_two_binaries` property and its version.
    mutable std::mutex _readWriteTwoBinariesPropertyMutex;

    // MQTT Subscription ID for `read_write_two_binaries` property updates.
    int _readWriteTwoBinariesPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_two_binaries` property.
    void _receiveReadWriteTwoBinariesPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_two_binaries` property.
    std::vector<std::function<void(std::vector<uint8_t>, boost::optional<std::vector<uint8_t>>)>> _readWriteTwoBinariesPropertyCallbacks;
    std::mutex _readWriteTwoBinariesPropertyCallbacksMutex;

    // ---read_write_list_of_strings Property---

    // Last received value for the `read_write_list_of_strings` property.
    boost::optional<ReadWriteListOfStringsProperty> _readWriteListOfStringsProperty;

    // This is the property version of the last received `read_write_list_of_strings` property update.
    int _lastReadWriteListOfStringsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_list_of_strings` property and its version.
    mutable std::mutex _readWriteListOfStringsPropertyMutex;

    // MQTT Subscription ID for `read_write_list_of_strings` property updates.
    int _readWriteListOfStringsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_list_of_strings` property.
    void _receiveReadWriteListOfStringsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_list_of_strings` property.
    std::vector<std::function<void(std::vector<std::string>)>> _readWriteListOfStringsPropertyCallbacks;
    std::mutex _readWriteListOfStringsPropertyCallbacksMutex;

    // ---read_write_lists Property---

    // Last received values for the `read_write_lists` property.
    boost::optional<ReadWriteListsProperty> _readWriteListsProperty;

    // This is the property version of the last received `read_write_lists` property update.
    int _lastReadWriteListsPropertyVersion = -1;

    // Mutex for protecting access to the `read_write_lists` property and its version.
    mutable std::mutex _readWriteListsPropertyMutex;

    // MQTT Subscription ID for `read_write_lists` property updates.
    int _readWriteListsPropertySubscriptionId;

    // Method for parsing a JSON payload that updates the `read_write_lists` property.
    void _receiveReadWriteListsPropertyUpdate(const std::string& topic, const std::string& payload, boost::optional<int> optPropertyVersion);

    // Callbacks registered for changes to the `read_write_lists` property.
    std::vector<std::function<void(std::vector<Numbers>, boost::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>>)>> _readWriteListsPropertyCallbacks;
    std::mutex _readWriteListsPropertyCallbacksMutex;
};