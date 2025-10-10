/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.
*/

#pragma once
#include <string>
#include <rapidjson/document.h>
#include "enums.hpp"
#include "structs.hpp"

/**
 * The `read_write_integer` property contains a single field:
 *   int value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write integer property.
 */
typedef int ReadWriteIntegerProperty;

/**
 * The `read_only_integer` property contains a single field:
 *   int value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-only integer property.
 */
typedef int ReadOnlyIntegerProperty;

/**
 * The `read_write_optional_integer` property contains a single field:
 *   boost::optional<int> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write optional integer property.
 */
typedef boost::optional<int> ReadWriteOptionalIntegerProperty;

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
 * The `read_only_string` property contains a single field:
 *   std::string value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-only string property.
 */
typedef std::string ReadOnlyStringProperty;

/**
 * The `read_write_string` property contains a single field:
 *   std::string value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write string property.
 */
typedef std::string ReadWriteStringProperty;

/**
 * The `read_write_optional_string` property contains a single field:
 *   boost::optional<std::string> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write optional string property.
 */
typedef boost::optional<std::string> ReadWriteOptionalStringProperty;

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
 * The `read_write_struct` property contains a single field:
 *   AllTypes value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write struct property.
 */
typedef AllTypes ReadWriteStructProperty;

/**
 * The `read_write_optional_struct` property contains a single field:
 *   AllTypes value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write optional struct property.
 */
typedef boost::optional<AllTypes> ReadWriteOptionalStructProperty;

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
 * The `read_only_enum` property contains a single field:
 *   Numbers value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-only enum property.
 */
typedef Numbers ReadOnlyEnumProperty;

/**
 * The `read_write_enum` property contains a single field:
 *   Numbers value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write enum property.
 */
typedef Numbers ReadWriteEnumProperty;

/**
 * The `read_write_optional_enum` property contains a single field:
 *   boost::optional<Numbers> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write optional enum property.
 */
typedef boost::optional<Numbers> ReadWriteOptionalEnumProperty;

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
 * The `read_write_datetime` property contains a single field:
 *   std::chrono::time_point<std::chrono::system_clock> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write datetime property.
 */
typedef std::chrono::time_point<std::chrono::system_clock> ReadWriteDatetimeProperty;

/**
 * The `read_write_optional_datetime` property contains a single field:
 *   boost::optional<std::chrono::time_point<std::chrono::system_clock>> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write optional datetime property.
 */
typedef boost::optional<std::chrono::time_point<std::chrono::system_clock>> ReadWriteOptionalDatetimeProperty;

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
 * The `read_write_duration` property contains a single field:
 *   std::chrono::duration<double> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write duration property.
 */
typedef std::chrono::duration<double> ReadWriteDurationProperty;

/**
 * The `read_write_optional_duration` property contains a single field:
 *   boost::optional<std::chrono::duration<double>> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write optional duration property.
 */
typedef boost::optional<std::chrono::duration<double>> ReadWriteOptionalDurationProperty;

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
 * The `read_write_binary` property contains a single field:
 *   std::vector<uint8_t> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write binary property.
 */
typedef std::vector<uint8_t> ReadWriteBinaryProperty;

/**
 * The `read_write_optional_binary` property contains a single field:
 *   boost::optional<std::vector<uint8_t>> value;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * A read-write optional binary property.
 */
typedef boost::optional<std::vector<uint8_t>> ReadWriteOptionalBinaryProperty;

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
