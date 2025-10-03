/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/

#pragma once
#include <string>
#include <chrono>
#include "enums.hpp"

struct DoSomethingReturnValue
{
    std::string label;
    int identifier;
    DayOfTheWeek day;
};

struct SetTheTimeReturnValue
{
    std::chrono::time_point<std::chrono::system_clock> timestamp;
    std::string confirmation_message;
};
