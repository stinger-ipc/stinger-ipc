/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/


#pragma once
#include <string>
#include "enums.hpp"
#include "structs.hpp"


struct LocationProperty {
    double latitude;
    
    double longitude;
    
};

struct CurrentTemperatureProperty {
    double temperature_f;
    
};

struct CurrentConditionProperty {
    WeatherCondition condition;
    
    std::string description;
    
};

struct DailyForecastProperty {
    ForecastForDay monday;
    ForecastForDay tuesday;
    ForecastForDay wednesday;
};

struct HourlyForecastProperty {
    ForecastForHour hour_0;
    ForecastForHour hour_1;
    ForecastForHour hour_2;
    ForecastForHour hour_3;
};

struct CurrentConditionRefreshIntervalProperty {
    int seconds;
    
};

struct HourlyForecastRefreshIntervalProperty {
    int seconds;
    
};

struct DailyForecastRefreshIntervalProperty {
    int seconds;
    
};
