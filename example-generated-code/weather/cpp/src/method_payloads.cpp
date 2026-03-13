
#include "method_payloads.hpp"

#include <rapidjson/document.h>
#include <stinger/utils/conversions.hpp>

namespace stinger {

namespace gen {
namespace weather {

// --- (De-)Serialization for refresh_daily_forecast method request arguments ---
RefreshDailyForecastRequestArguments RefreshDailyForecastRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    RefreshDailyForecastRequestArguments refreshDailyForecastArgs;

    return refreshDailyForecastArgs;
};

void RefreshDailyForecastRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for refresh_daily_forecast method return type ---
RefreshDailyForecastReturnValues RefreshDailyForecastReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    RefreshDailyForecastReturnValues refreshDailyForecastRc;

    return refreshDailyForecastRc;
};

void RefreshDailyForecastReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for refresh_hourly_forecast method request arguments ---
RefreshHourlyForecastRequestArguments RefreshHourlyForecastRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    RefreshHourlyForecastRequestArguments refreshHourlyForecastArgs;

    return refreshHourlyForecastArgs;
};

void RefreshHourlyForecastRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for refresh_hourly_forecast method return type ---
RefreshHourlyForecastReturnValues RefreshHourlyForecastReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    RefreshHourlyForecastReturnValues refreshHourlyForecastRc;

    return refreshHourlyForecastRc;
};

void RefreshHourlyForecastReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for refresh_current_conditions method request arguments ---
RefreshCurrentConditionsRequestArguments RefreshCurrentConditionsRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    RefreshCurrentConditionsRequestArguments refreshCurrentConditionsArgs;

    return refreshCurrentConditionsArgs;
};

void RefreshCurrentConditionsRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for refresh_current_conditions method return type ---
RefreshCurrentConditionsReturnValues RefreshCurrentConditionsReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    RefreshCurrentConditionsReturnValues refreshCurrentConditionsRc;

    return refreshCurrentConditionsRc;
};

void RefreshCurrentConditionsReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

} // namespace weather

} // namespace gen

} // namespace stinger
