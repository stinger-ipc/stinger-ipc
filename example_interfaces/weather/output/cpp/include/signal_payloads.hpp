/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.

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

struct CurrentTimePayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CurrentTimePayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string currentTime;
};
