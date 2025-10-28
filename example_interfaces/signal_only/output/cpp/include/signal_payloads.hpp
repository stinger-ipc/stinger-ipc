/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once
#include <string>
#include <chrono>
#include <vector>
#include <boost/optional.hpp>
#include "enums.hpp"
#include "structs.hpp"

struct AnotherSignalPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static AnotherSignalPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    double one;
    bool two;
    std::string three;
};

struct BarkPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static BarkPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string word;
};

struct MaybeNumberPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static MaybeNumberPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<int> number;
};

struct MaybeNamePayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static MaybeNamePayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::string> name;
};

struct NowPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static NowPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> timestamp;
};
