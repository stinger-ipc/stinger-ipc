/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.

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

struct RefreshDailyForecastRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static RefreshDailyForecastRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct RefreshDailyForecastReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static RefreshDailyForecastReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct RefreshHourlyForecastRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static RefreshHourlyForecastRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct RefreshHourlyForecastReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static RefreshHourlyForecastReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct RefreshCurrentConditionsRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static RefreshCurrentConditionsRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct RefreshCurrentConditionsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static RefreshCurrentConditionsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
};