/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/

#pragma once
#include <string>
#include <boost/optional.hpp>
#include <rapidjson/document.h>
#include "enums.hpp"

struct ForecastForHour
{
    static ForecastForHour FromRapidJsonObject(const rapidjson::Value& jsonObj);
    double temperature;
    std::string starttime;
    WeatherCondition condition;
};

struct ForecastForDay
{
    static ForecastForDay FromRapidJsonObject(const rapidjson::Value& jsonObj);
    double high_temperature;
    double low_temperature;
    WeatherCondition condition;
    std::string start_time;
    std::string end_time;
};
