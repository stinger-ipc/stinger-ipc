
#include "structs.hpp"

ForecastForHour ForecastForHour::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ForecastForHour forecastForHour;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("temperature");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            forecastForHour.temperature = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("starttime");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            forecastForHour.starttime = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("condition");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            forecastForHour.condition = static_cast<WeatherCondition>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return forecastForHour;
};

ForecastForDay ForecastForDay::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ForecastForDay forecastForDay;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("high_temperature");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            forecastForDay.high_temperature = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("low_temperature");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            forecastForDay.low_temperature = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("condition");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            forecastForDay.condition = static_cast<WeatherCondition>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("start_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            forecastForDay.start_time = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("end_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            forecastForDay.end_time = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return forecastForDay;
};
