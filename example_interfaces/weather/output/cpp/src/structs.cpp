

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
            throw std::runtime_error("Received payload for the 'temperature' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("starttime");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempStarttimeIsoString = itr->value.GetString();
            forecastForHour.starttime = parseIsoTimestamp(tempStarttimeIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'starttime' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'condition' argument doesn't have required value/type");
        }
    }

    return forecastForHour;
};

void ForecastForHour::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("temperature", temperature, allocator);

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempStarttimeStringValue;
        std::string starttimeIsoString = timePointToIsoString(starttime);
        tempStarttimeStringValue.SetString(starttimeIsoString.c_str(), starttimeIsoString.size(), allocator);
        parent.AddMember("starttime", tempStarttimeStringValue, allocator);
    }

    parent.AddMember("condition", static_cast<int>(condition), allocator);
}

ForecastForDay ForecastForDay::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ForecastForDay forecastForDay;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("high_temperature");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            forecastForDay.highTemperature = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'high_temperature' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("low_temperature");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            forecastForDay.lowTemperature = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'low_temperature' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'condition' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("start_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            forecastForDay.startTime = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'start_time' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("end_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            forecastForDay.endTime = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'end_time' argument doesn't have required value/type");
        }
    }

    return forecastForDay;
};

void ForecastForDay::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("high_temperature", highTemperature, allocator);

    parent.AddMember("low_temperature", lowTemperature, allocator);

    parent.AddMember("condition", static_cast<int>(condition), allocator);

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(startTime.c_str(), startTime.size(), allocator);
        parent.AddMember("start_time", tempStringValue, allocator);
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(endTime.c_str(), endTime.size(), allocator);
        parent.AddMember("end_time", tempStringValue, allocator);
    }
}
