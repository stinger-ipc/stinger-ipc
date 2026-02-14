/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Simple interface.

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
namespace simple {

struct Person {
    static Person FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::string name;
    Gender gender;
};

} // namespace simple

} // namespace gen

} // namespace stinger
