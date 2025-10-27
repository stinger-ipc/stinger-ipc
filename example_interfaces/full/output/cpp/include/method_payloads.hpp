/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions.
You may use, modify, and distribute it under any license of your choosing.
*/

#pragma once
#include <string>
#include <chrono>
#include <vector>
#include <boost/optional.hpp>
#include "enums.hpp"
#include "structs.hpp"

struct AddNumbersRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static AddNumbersRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int first;
    int second;
    boost::optional<int> third;
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
    std::string aString;
};

struct DoSomethingReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static DoSomethingReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string label;
    int identifier;
    DayOfTheWeek day;
};

struct EchoRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static EchoRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string message;
};

struct EchoReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static EchoReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string message;
};

struct WhatTimeIsItRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static WhatTimeIsItRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> theFirstTime;
};

struct WhatTimeIsItReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static WhatTimeIsItReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> timestamp;
};

struct SetTheTimeRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SetTheTimeRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> theFirstTime;
    std::chrono::time_point<std::chrono::system_clock> theSecondTime;
};

struct SetTheTimeReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static SetTheTimeReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> timestamp;
    std::string confirmationMessage;
};

struct ForwardTimeRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ForwardTimeRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> adjustment;
};

struct ForwardTimeReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static ForwardTimeReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> newTime;
};

struct HowOffIsTheClockRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static HowOffIsTheClockRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> actualTime;
};

struct HowOffIsTheClockReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static HowOffIsTheClockReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> difference;
};