

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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return location;
};

rapidjson::Value LocationProperty::ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const
{
    rapidjson::Value obj(rapidjson::kObjectType);

    obj.AddMember("latitude", latitude, allocator);

    obj.AddMember("longitude", longitude, allocator);

    return obj;
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return currentCondition;
};

rapidjson::Value CurrentConditionProperty::ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const
{
    rapidjson::Value obj(rapidjson::kObjectType);

    obj.AddMember("condition", static_cast<int>(condition), allocator);

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(description.c_str(), description.size(), allocator);
        obj.AddMember("description", tempStringValue, allocator);
    }

    return obj;
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return dailyForecast;
};

rapidjson::Value DailyForecastProperty::ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const
{
    rapidjson::Value obj(rapidjson::kObjectType);

    return obj;
}

HourlyForecastProperty HourlyForecastProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    HourlyForecastProperty hourlyForecast;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("hour_0");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            hourlyForecast.hour_0 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("hour_1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            hourlyForecast.hour_1 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("hour_2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            hourlyForecast.hour_2 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("hour_3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            hourlyForecast.hour_3 = ForecastForHour::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return hourlyForecast;
};

rapidjson::Value HourlyForecastProperty::ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const
{
    rapidjson::Value obj(rapidjson::kObjectType);

    return obj;
}
