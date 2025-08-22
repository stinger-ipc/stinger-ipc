
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
