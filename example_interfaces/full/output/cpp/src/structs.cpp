

#include "structs.hpp"

Lunch Lunch::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    Lunch lunch;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("drink");
        if (itr != jsonObj.MemberEnd() && itr->value.IsBool())
        {
            lunch.drink = itr->value.GetBool();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'drink' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("sandwich");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            lunch.sandwich = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'sandwich' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("crackers");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            lunch.crackers = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'crackers' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("day");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            lunch.day = static_cast<DayOfTheWeek>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload for the 'day' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("order_number");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            lunch.orderNumber = itr->value.GetInt();
        }
        else
        {
            lunch.orderNumber = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("time_of_lunch");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTimeOfLunchIsoString = itr->value.GetString();
            lunch.timeOfLunch = parseIsoTimestamp(tempTimeOfLunchIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'time_of_lunch' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("duration_of_lunch");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempDurationOfLunchIsoString = itr->value.GetString();
            lunch.durationOfLunch = parseIsoDuration(tempDurationOfLunchIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'duration_of_lunch' argument doesn't have required value/type");
        }
    }

    return lunch;
};

void Lunch::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("drink", drink, allocator);

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(sandwich.c_str(), sandwich.size(), allocator);
        parent.AddMember("sandwich", tempStringValue, allocator);
    }

    parent.AddMember("crackers", crackers, allocator);

    parent.AddMember("day", static_cast<int>(day), allocator);

    if (orderNumber)
        parent.AddMember("order_number", *orderNumber, allocator);

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTimeOfLunchStringValue;
        std::string timeOfLunchIsoString = timePointToIsoString(timeOfLunch);
        tempTimeOfLunchStringValue.SetString(timeOfLunchIsoString.c_str(), timeOfLunchIsoString.size(), allocator);
        parent.AddMember("time_of_lunch", tempTimeOfLunchStringValue, allocator);
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempDurationOfLunchStringValue;
        std::string durationOfLunchIsoString = durationToIsoString(durationOfLunch);
        tempDurationOfLunchStringValue.SetString(durationOfLunchIsoString.c_str(), durationOfLunchIsoString.size(), allocator);
        parent.AddMember("duration_of_lunch", tempDurationOfLunchStringValue, allocator);
    }
}
