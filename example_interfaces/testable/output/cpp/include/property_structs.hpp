/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.

LICENSE: This generated code is not subject to any license restrictions.
You may use, modify, and distribute it under any license of your choosing.
*/

#pragma once
#include <string>
#include <rapidjson/document.h>
#include "enums.hpp"
#include "structs.hpp"

/**
 * A read-write integer property.
 */
struct ReadWriteIntegerProperty
{
    static ReadWriteIntegerProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    int value;
};

/**
 * A read-only integer property.
 */
struct ReadOnlyIntegerProperty
{
    static ReadOnlyIntegerProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    int value;
};

/**
 * A read-write optional integer property.
 */
struct ReadWriteOptionalIntegerProperty
{
    static ReadWriteOptionalIntegerProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    boost::optional<int> value;
};

/**
 * A read-write property with two integer values. The second is optional.
 */
struct ReadWriteTwoIntegersProperty
{
    static ReadWriteTwoIntegersProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    int first; ///< An integer value.
    boost::optional<int> second;
};

/**
 * A read-only string property.
 */
struct ReadOnlyStringProperty
{
    static ReadOnlyStringProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::string value;
};

/**
 * A read-write string property.
 */
struct ReadWriteStringProperty
{
    static ReadWriteStringProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::string value;
};

/**
 * A read-write optional string property.
 */
struct ReadWriteOptionalStringProperty
{
    static ReadWriteOptionalStringProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    boost::optional<std::string> value;
};

/**
 * A read-write property with two string values. The second is optional.
 */
struct ReadWriteTwoStringsProperty
{
    static ReadWriteTwoStringsProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::string first; ///< A string value.
    boost::optional<std::string> second;
};

/**
 * A read-write struct property.
 */
struct ReadWriteStructProperty
{
    static ReadWriteStructProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    AllTypes value;
};

/**
 * A read-write optional struct property.
 */
struct ReadWriteOptionalStructProperty
{
    static ReadWriteOptionalStructProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    boost::optional<AllTypes> value;
};

/**
 * A read-write property with two struct values. The second is optional.
 */
struct ReadWriteTwoStructsProperty
{
    static ReadWriteTwoStructsProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    AllTypes first; ///< A struct value.
    boost::optional<AllTypes> second;
};

/**
 * A read-only enum property.
 */
struct ReadOnlyEnumProperty
{
    static ReadOnlyEnumProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    Numbers value;
};

/**
 * A read-write enum property.
 */
struct ReadWriteEnumProperty
{
    static ReadWriteEnumProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    Numbers value;
};

/**
 * A read-write optional enum property.
 */
struct ReadWriteOptionalEnumProperty
{
    static ReadWriteOptionalEnumProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    boost::optional<Numbers> value;
};

/**
 * A read-write property with two enum values. The second is optional.
 */
struct ReadWriteTwoEnumsProperty
{
    static ReadWriteTwoEnumsProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    Numbers first; ///< An enum value.
    boost::optional<Numbers> second;
};

/**
 * A read-write datetime property.
 */
struct ReadWriteDatetimeProperty
{
    static ReadWriteDatetimeProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::chrono::time_point<std::chrono::system_clock> value;
};

/**
 * A read-write optional datetime property.
 */
struct ReadWriteOptionalDatetimeProperty
{
    static ReadWriteOptionalDatetimeProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> value;
};

/**
 * A read-write property with two datetime values. The second is optional.
 */
struct ReadWriteTwoDatetimesProperty
{
    static ReadWriteTwoDatetimesProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::chrono::time_point<std::chrono::system_clock> first; ///< A date and time value.
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> second;
};

/**
 * A read-write duration property.
 */
struct ReadWriteDurationProperty
{
    static ReadWriteDurationProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::chrono::duration<double> value;
};

/**
 * A read-write optional duration property.
 */
struct ReadWriteOptionalDurationProperty
{
    static ReadWriteOptionalDurationProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    boost::optional<std::chrono::duration<double>> value;
};

/**
 * A read-write property with two duration values. The second is optional.
 */
struct ReadWriteTwoDurationsProperty
{
    static ReadWriteTwoDurationsProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::chrono::duration<double> first; ///< A duration of time.
    boost::optional<std::chrono::duration<double>> second;
};

/**
 * A read-write binary property.
 */
struct ReadWriteBinaryProperty
{
    static ReadWriteBinaryProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::vector<uint8_t> value;
};

/**
 * A read-write optional binary property.
 */
struct ReadWriteOptionalBinaryProperty
{
    static ReadWriteOptionalBinaryProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    boost::optional<std::vector<uint8_t>> value;
};

/**
 * A read-write property with two binary values.  The second is optional.
 */
struct ReadWriteTwoBinariesProperty
{
    static ReadWriteTwoBinariesProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::vector<uint8_t> first; ///< A binary blob of data.
    boost::optional<std::vector<uint8_t>> second;
};

/**
 * A read-write property that is a list of strings.
 */
struct ReadWriteListOfStringsProperty
{
    static ReadWriteListOfStringsProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::vector<std::string> value;
};

/**
 * A read-write property containing two lists.  The second list is optional.
 */
struct ReadWriteListsProperty
{
    static ReadWriteListsProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::vector<Numbers> theList;
    boost::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList;
};
