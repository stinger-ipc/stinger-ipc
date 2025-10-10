/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.
*/

#pragma once
#include <string>
#include <chrono>
#include <vector>
#include <boost/optional.hpp>
#include "enums.hpp"
#include "structs.hpp"

struct CallThreeIntegersReturnValue
{
    int output1;
    int output2;
    boost::optional<int> output3;
};

struct CallThreeStringsReturnValue
{
    std::string output1;
    std::string output2;
    boost::optional<std::string> output3;
};

struct CallThreeEnumsReturnValue
{
    Numbers output1;
    Numbers output2;
    boost::optional<Numbers> output3;
};

struct CallOneStructReturnValue
{
    bool bool_;
    int int_;
    double number;
    std::string str;
    Numbers enum_;
    std::chrono::time_point<std::chrono::system_clock> date_and_time;
    std::chrono::duration<double> time_duration;
    std::vector<uint8_t> data;
    boost::optional<int> OptionalInteger;
    boost::optional<std::string> OptionalString;
    boost::optional<Numbers> OptionalEnum;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> OptionalDateTime;
    boost::optional<std::chrono::duration<double>> OptionalDuration;
    boost::optional<std::vector<uint8_t>> OptionalBinary;
};

struct CallOptionalStructReturnValue
{
    bool bool_;
    int int_;
    double number;
    std::string str;
    Numbers enum_;
    std::chrono::time_point<std::chrono::system_clock> date_and_time;
    std::chrono::duration<double> time_duration;
    std::vector<uint8_t> data;
    boost::optional<int> OptionalInteger;
    boost::optional<std::string> OptionalString;
    boost::optional<Numbers> OptionalEnum;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> OptionalDateTime;
    boost::optional<std::chrono::duration<double>> OptionalDuration;
    boost::optional<std::vector<uint8_t>> OptionalBinary;
};

struct CallThreeStructsReturnValue
{
    AllTypes output1;
    AllTypes output2;
    boost::optional<AllTypes> output3;
};

struct CallThreeDateTimesReturnValue
{
    std::chrono::time_point<std::chrono::system_clock> output1;
    std::chrono::time_point<std::chrono::system_clock> output2;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> output3;
};

struct CallThreeDurationsReturnValue
{
    std::chrono::duration<double> output1;
    std::chrono::duration<double> output2;
    boost::optional<std::chrono::duration<double>> output3;
};

struct CallThreeBinariesReturnValue
{
    std::vector<uint8_t> output1;
    std::vector<uint8_t> output2;
    boost::optional<std::vector<uint8_t>> output3;
};

struct CallWithNothingReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallWithNothingReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct CallOneIntegerReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneIntegerReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int output1;
};

struct CallOptionalIntegerReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalIntegerReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<int> output1;
};

struct CallThreeIntegersReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeIntegersReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int output1;
    int output2;
    boost::optional<int> output3;
};

struct CallOneStringReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneStringReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string output1;
};

struct CallOptionalStringReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalStringReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::string> output1;
};

struct CallThreeStringsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeStringsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string output1;
    std::string output2;
    boost::optional<std::string> output3;
};

struct CallOneEnumReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneEnumReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Numbers output1;
};

struct CallOptionalEnumReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalEnumReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<Numbers> output1;
};

struct CallThreeEnumsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeEnumsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Numbers output1;
    Numbers output2;
    boost::optional<Numbers> output3;
};

struct CallOneStructReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneStructReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    AllTypes output1;
};

struct CallOptionalStructReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalStructReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<AllTypes> output1;
};

struct CallThreeStructsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeStructsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    AllTypes output1;
    AllTypes output2;
    boost::optional<AllTypes> output3;
};

struct CallOneDateTimeReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneDateTimeReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> output1;
};

struct CallOptionalDateTimeReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalDateTimeReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> output1;
};

struct CallThreeDateTimesReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeDateTimesReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> output1;
    std::chrono::time_point<std::chrono::system_clock> output2;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> output3;
};

struct CallOneDurationReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneDurationReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> output1;
};

struct CallOptionalDurationReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalDurationReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::chrono::duration<double>> output1;
};

struct CallThreeDurationsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeDurationsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> output1;
    std::chrono::duration<double> output2;
    boost::optional<std::chrono::duration<double>> output3;
};

struct CallOneBinaryReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneBinaryReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<uint8_t> output1;
};

struct CallOptionalBinaryReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalBinaryReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::vector<uint8_t>> output1;
};

struct CallThreeBinariesReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeBinariesReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<uint8_t> output1;
    std::vector<uint8_t> output2;
    boost::optional<std::vector<uint8_t>> output3;
};