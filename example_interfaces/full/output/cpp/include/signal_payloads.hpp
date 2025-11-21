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

struct TodayIsPayload
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static TodayIsPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int dayOfMonth;
    std::optional<DayOfTheWeek> dayOfWeek;
    std::chrono::time_point<std::chrono::system_clock> timestamp;
    std::chrono::duration<double> processTime;
    std::vector<uint8_t> memorySegment;
};
