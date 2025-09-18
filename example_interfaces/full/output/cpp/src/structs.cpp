
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("order_number");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            lunch.order_number = itr->value.GetInt();
        }
        else
        {
            lunch.order_number = boost::none;
        }
    }

    return lunch;
};
