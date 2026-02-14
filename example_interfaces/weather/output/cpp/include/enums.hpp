/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once

#include <map>
#include <string>

namespace stinger {

namespace gen {
namespace weather {

/** 
 * @enum WeatherCondition
 * @brief This enum contains the possible weather conditions that can be reported.

 */
enum class WeatherCondition {
    RAINY = 1,
    SUNNY = 2,
    PARTLY_CLOUDY = 3,
    MOSTLY_CLOUDY = 4,
    OVERCAST = 5,
    WINDY = 6,
    SNOWY = 7
};
static const std::map<int, std::string> weatherConditionStrings = {
    { 1, "rainy" },

    { 2, "sunny" },

    { 3, "partly_cloudy" },

    { 4, "mostly_cloudy" },

    { 5, "overcast" },

    { 6, "windy" },

    { 7, "snowy" }
};

} // namespace weather

} // namespace gen

} // namespace stinger
