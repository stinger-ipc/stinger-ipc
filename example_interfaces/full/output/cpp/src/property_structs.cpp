

#include "property_structs.hpp"
#include <rapidjson/document.h>

FavoriteFoodsProperty FavoriteFoodsProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    FavoriteFoodsProperty favoriteFoods;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("drink");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            favoriteFoods.drink = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("slices_of_pizza");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            favoriteFoods.slices_of_pizza = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("breakfast");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            favoriteFoods.breakfast = itr->value.GetString();
        }
        else
        {
            favoriteFoods.breakfast = boost::none;
        }
    }

    return favoriteFoods;
};

void FavoriteFoodsProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(drink.c_str(), drink.size(), allocator);
        parent.AddMember("drink", tempStringValue, allocator);
    }

    parent.AddMember("slices_of_pizza", slices_of_pizza, allocator);

    if (breakfast)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(breakfast->c_str(), breakfast->size(), allocator);
        parent.AddMember("breakfast", tempStringValue, allocator);
    }
}

LunchMenuProperty LunchMenuProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    LunchMenuProperty lunchMenu;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("monday");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            lunchMenu.monday = Lunch::FromRapidJsonObject(itr->value);
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
            lunchMenu.tuesday = Lunch::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return lunchMenu;
};

void LunchMenuProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

LastBirthdaysProperty LastBirthdaysProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    LastBirthdaysProperty lastBirthdays;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("mom");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("dad");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("sister");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            lastBirthdays.sister = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("brothers_age");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            lastBirthdays.brothers_age = itr->value.GetInt();
        }
        else
        {
            lastBirthdays.brothers_age = boost::none;
        }
    }

    return lastBirthdays;
};

void LastBirthdaysProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (brothers_age)
        parent.AddMember("brothers_age", *brothers_age, allocator);
}
