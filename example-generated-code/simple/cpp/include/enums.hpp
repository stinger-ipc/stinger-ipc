/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once

#include <map>
#include <string>

namespace stinger {

namespace gen {
namespace simple {

/** 
 * @enum Gender
 */
enum class Gender {
    MALE = 1,
    FEMALE = 2,
    OTHER = 3
};
static const std::map<int, std::string> genderStrings = {
    { 1, "male" },

    { 2, "female" },

    { 3, "other" }
};

} // namespace simple

} // namespace gen

} // namespace stinger
