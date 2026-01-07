/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once

#include <map>
#include <string>

/** 
 * @enum DayOfTheWeek
 * @brief The days of the week.
 */
enum class DayOfTheWeek
{
    SUNDAY = 1, // First day of the week.
    MONDAY = 2,
    TUESDAY = 3,
    WEDNESDAY = 4,
    THURSDAY = 5,
    FRIDAY = 6,
    SATURDAY = 7
};
static const std::map<int, std::string> dayOfTheWeekStrings = {
    { 1, "Sunday" },

    { 2, "Monday" },

    { 3, "Tuesday" },

    { 4, "Wednesday" },

    { 5, "Thursday" },

    { 6, "Friday" },

    { 7, "Saturday" }
};

/** 
 * @enum MultiplesOfTen
 * @brief Enumeration of multiples of ten.
 */
enum class MultiplesOfTen
{
    TEN = 10, // First multiple of ten.
    TWENTY = 20, // Second multiple of ten.
    THIRTY = 30,
    FORTY = 40,
    FIFTY = 50
};
static const std::map<int, std::string> multiplesOfTenStrings = {
    { 10, "Ten" },

    { 20, "Twenty" },

    { 30, "Thirty" },

    { 40, "Forty" },

    { 50, "Fifty" }
};
