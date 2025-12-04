/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once
#include <string>
#include <chrono>
#include <vector>
#include "utils.hpp"
#include "enums.hpp"
#include "structs.hpp"

struct AddNumbersRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static AddNumbersRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int first;
    int second;
    std::optional<int> third;
};

struct AddNumbersReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static AddNumbersReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int sum;
};

struct DoSomethingRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static DoSomethingRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string taskToDo;
};

struct DoSomethingReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static DoSomethingReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string label;
    int identifier;
};

struct WhatTimeIsItRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static WhatTimeIsItRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct WhatTimeIsItReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static WhatTimeIsItReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> timestamp;
};

struct HoldTemperatureRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static HoldTemperatureRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    double temperatureCelsius;
};

struct HoldTemperatureReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static HoldTemperatureReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    bool success;
};