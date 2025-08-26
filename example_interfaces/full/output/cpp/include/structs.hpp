/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/

#pragma once
#include <string>
#include <boost/optional.hpp>
#include "enums.hpp"


struct Lunch {
    bool drink;
    std::string sandwich;
    double crackers;
    DayOfTheWeek day;
    boost::optional<int> order_number;
};
