/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once
#include <string>
#include <cstddef>
#include <chrono>
#include <vector>
#include <rapidjson/document.h>
#include "enums.hpp"
#include <stinger/utils/conversions.hpp>

namespace stinger {

namespace gen {
namespace full {

struct Lunch {
    static Lunch FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    bool drink;
    std::string sandwich;
    double crackers;
    DayOfTheWeek day;
    std::optional<int> orderNumber;
    std::chrono::time_point<std::chrono::system_clock> timeOfLunch;
    std::chrono::duration<double> durationOfLunch;
};

} // namespace full

} // namespace gen

} // namespace stinger
