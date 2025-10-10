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

struct EmptyPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static EmptyPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct SingleIntPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleIntPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int value;
};

struct SingleOptionalIntPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleOptionalIntPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<int> value;
};

struct ThreeIntegersPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ThreeIntegersPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int first;
    int second;
    boost::optional<int> third;
};

struct SingleStringPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleStringPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string value;
};

struct SingleOptionalStringPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleOptionalStringPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::string> value;
};

struct ThreeStringsPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ThreeStringsPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string first;
    std::string second;
    boost::optional<std::string> third;
};

struct SingleEnumPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleEnumPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Numbers value;
};

struct SingleOptionalEnumPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleOptionalEnumPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<Numbers> value;
};

struct ThreeEnumsPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ThreeEnumsPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Numbers first;
    Numbers second;
    boost::optional<Numbers> third;
};

struct SingleStructPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleStructPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    AllTypes value;
};

struct SingleOptionalStructPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleOptionalStructPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<AllTypes> value;
};

struct ThreeStructsPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ThreeStructsPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    AllTypes first;
    AllTypes second;
    boost::optional<AllTypes> third;
};

struct SingleDateTimePayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleDateTimePayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> value;
};

struct SingleOptionalDatetimePayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleOptionalDatetimePayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> value;
};

struct ThreeDateTimesPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ThreeDateTimesPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> first;
    std::chrono::time_point<std::chrono::system_clock> second;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> third;
};

struct SingleDurationPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleDurationPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> value;
};

struct SingleOptionalDurationPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleOptionalDurationPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::chrono::duration<double>> value;
};

struct ThreeDurationsPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ThreeDurationsPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> first;
    std::chrono::duration<double> second;
    boost::optional<std::chrono::duration<double>> third;
};

struct SingleBinaryPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleBinaryPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<uint8_t> value;
};

struct SingleOptionalBinaryPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SingleOptionalBinaryPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::vector<uint8_t>> value;
};

struct ThreeBinariesPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ThreeBinariesPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<uint8_t> first;
    std::vector<uint8_t> second;
    boost::optional<std::vector<uint8_t>> third;
};
