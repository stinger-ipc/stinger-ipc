

#include "property_structs.hpp"
#include <rapidjson/document.h>

LocationProperty LocationProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    LocationProperty location;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("latitude");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            location.latitude = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'latitude' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("longitude");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            location.longitude = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'longitude' argument doesn't have required value/type");
        }
    }

    return location;
};

void LocationProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("latitude", latitude, allocator);

    parent.AddMember("longitude", longitude, allocator);
}

CurrentTemperatureProperty CurrentTemperatureProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CurrentTemperatureProperty currentTemperature;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("temperature_f");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            currentTemperature.temperatureF = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'temperature_f' argument doesn't have required value/type");
        }
    }

    return currentTemperature;
};

void CurrentTemperatureProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("temperature_f", temperatureF, allocator);
}

CurrentConditionProperty CurrentConditionProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CurrentConditionProperty currentCondition;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("condition");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            currentCondition.condition = static_cast<WeatherCondition>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload for the 'condition' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("description");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            currentCondition.description = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'description' argument doesn't have required value/type");
        }
    }

    return currentCondition;
};

void CurrentConditionProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("condition", static_cast<int>(condition), allocator);

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(description.c_str(), description.size(), allocator);
        parent.AddMember("description", tempStringValue, allocator);
    }
}

DailyForecastProperty DailyForecastProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    DailyForecastProperty dailyForecast;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("monday");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            dailyForecast.monday = ForecastForDay::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'monday' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("tuesday");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            dailyForecast.tuesday = ForecastForDay::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'tuesday' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("wednesday");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            dailyForecast.wednesday = ForecastForDay::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'wednesday' argument doesn't have required value/type");
        }
    }

    return dailyForecast;
};

void DailyForecastProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        monday.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("monday", tempStructValue, allocator);
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        tuesday.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("tuesday", tempStructValue, allocator);
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        wednesday.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("wednesday", tempStructValue, allocator);
    }
}

HourlyForecastProperty HourlyForecastProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    HourlyForecastProperty hourlyForecast;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("hour_0");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            hourlyForecast.hour0 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'hour_0' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("hour_1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            hourlyForecast.hour1 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'hour_1' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("hour_2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            hourlyForecast.hour2 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'hour_2' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("hour_3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            hourlyForecast.hour3 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'hour_3' argument doesn't have required value/type");
        }
    }

    return hourlyForecast;
};

void HourlyForecastProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        hour0.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("hour_0", tempStructValue, allocator);
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        hour1.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("hour_1", tempStructValue, allocator);
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        hour2.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("hour_2", tempStructValue, allocator);
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        hour3.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("hour_3", tempStructValue, allocator);
    }
}

CurrentConditionRefreshIntervalProperty CurrentConditionRefreshIntervalProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CurrentConditionRefreshIntervalProperty currentConditionRefreshInterval;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("seconds");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            currentConditionRefreshInterval.seconds = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'seconds' argument doesn't have required value/type");
        }
    }

    return currentConditionRefreshInterval;
};

void CurrentConditionRefreshIntervalProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("seconds", seconds, allocator);
}

HourlyForecastRefreshIntervalProperty HourlyForecastRefreshIntervalProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    HourlyForecastRefreshIntervalProperty hourlyForecastRefreshInterval;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("seconds");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            hourlyForecastRefreshInterval.seconds = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'seconds' argument doesn't have required value/type");
        }
    }

    return hourlyForecastRefreshInterval;
};

void HourlyForecastRefreshIntervalProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("seconds", seconds, allocator);
}

DailyForecastRefreshIntervalProperty DailyForecastRefreshIntervalProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    DailyForecastRefreshIntervalProperty dailyForecastRefreshInterval;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("seconds");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            dailyForecastRefreshInterval.seconds = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'seconds' argument doesn't have required value/type");
        }
    }

    return dailyForecastRefreshInterval;
};

void DailyForecastRefreshIntervalProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("seconds", seconds, allocator);
}
