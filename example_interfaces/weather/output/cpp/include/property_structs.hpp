/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/


#pragma once
#include <string>
#include <rapidjson/document.h>
#include "enums.hpp"
#include "structs.hpp"

/**
 * Weather will be retrieved for the provided location.
 * 
 */
struct LocationProperty {
    static LocationProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    rapidjson::Value ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const;
    double latitude;
    double longitude;
};



/**
 * The `current_temperature` property contains a single field:
 *   double temperature_f;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * This is the current (estimated) temperature in degrees fahrenheit.  This values
 * is regularly updated.  The value is extrapolated from the hourly forecast, but
 * adjusted based on the latest conditions at the nearest weather station.
 * 
 */
typedef double CurrentTemperatureProperty;

/**
 * This is the current weather outside.  This comes from the hourly forecast and is
 * updated about once per hour.
 * 
 */
struct CurrentConditionProperty {
    static CurrentConditionProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    rapidjson::Value ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const;
    WeatherCondition condition;
    std::string description;
};

/**
 * This contains the weather forecast for each day of the next few days.  It is updated
 * a couple of times a day.  The current day may not have the high or low temperature
 * provided.  This is an example which shows only a few days.  The actual implementation
 * will have a value for each day of the week.
 * 
 */
struct DailyForecastProperty {
    static DailyForecastProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    rapidjson::Value ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const;
    ForecastForDay monday;  ///< This is the forecast for Monday.
    ForecastForDay tuesday;
    ForecastForDay wednesday;
};

/**
 * This contains the weather forecast for each hour of the next 24 hours.  The data source
 * us updated a couple of times per day, but this API property is updated every hour on the
 * hour.
 * 
 */
struct HourlyForecastProperty {
    static HourlyForecastProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    rapidjson::Value ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const;
    ForecastForHour hour_0;  ///< This is the forecast for the current hour.
    ForecastForHour hour_1;  ///< This is the forecast for the next hour.
    ForecastForHour hour_2;
    ForecastForHour hour_3;
};



/**
 * The `current_condition_refresh_interval` property contains a single field:
 *   int seconds;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * This is the maximum interval, in seconds, that the latest weather conditions at the nearest weather
 * station are retrieved.
 * 
 */
typedef int CurrentConditionRefreshIntervalProperty;



/**
 * The `hourly_forecast_refresh_interval` property contains a single field:
 *   int seconds;  ///< Interval duration in seconds.
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * This is the maximum interval, in seconds, that the hourly forecast data is retrieved.
 * 
 */
typedef int HourlyForecastRefreshIntervalProperty;



/**
 * The `daily_forecast_refresh_interval` property contains a single field:
 *   int seconds;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * This is the maximum interval, in seconds, that the daily forecast data is retrieved.
 * 
 */
typedef int DailyForecastRefreshIntervalProperty;

