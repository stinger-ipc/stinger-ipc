/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once
#include <string>
#include <chrono>
#include <vector>
#include "enums.hpp"
#include "structs.hpp"

namespace stinger {

namespace gen {
namespace simple {

struct PersonEnteredPayload {
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static PersonEnteredPayload FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Person person;
};

} // namespace simple

} // namespace gen

} // namespace stinger
