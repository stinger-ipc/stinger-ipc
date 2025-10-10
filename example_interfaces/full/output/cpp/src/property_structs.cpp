

#include "property_structs.hpp"
#include <rapidjson/document.h>

FavoriteNumberProperty FavoriteNumberProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    FavoriteNumberProperty favoriteNumber;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("number");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            favoriteNumber.number = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return favoriteNumber;
};

void FavoriteNumberProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("number", number, allocator);
}

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
            favoriteFoods.slicesOfPizza = itr->value.GetInt();
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

    parent.AddMember("slices_of_pizza", slicesOfPizza, allocator);

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

FamilyNameProperty FamilyNameProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    FamilyNameProperty familyName;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("family_name");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            familyName.familyName = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return familyName;
};

void FamilyNameProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(familyName.c_str(), familyName.size(), allocator);
        parent.AddMember("family_name", tempStringValue, allocator);
    }
}

LastBreakfastTimeProperty LastBreakfastTimeProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    LastBreakfastTimeProperty lastBreakfastTime;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("timestamp");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTimestampIsoString = itr->value.GetString();
            lastBreakfastTime.timestamp = parseIsoTimestamp(tempTimestampIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return lastBreakfastTime;
};

void LastBreakfastTimeProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), allocator);
        parent.AddMember("timestamp", tempTimestampStringValue, allocator);
    }
}

BreakfastLengthProperty BreakfastLengthProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    BreakfastLengthProperty breakfastLength;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("length");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempLengthIsoString = itr->value.GetString();
            breakfastLength.length = parseIsoDuration(tempLengthIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return breakfastLength;
};

void BreakfastLengthProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempLengthStringValue;
        std::string lengthIsoString = durationToIsoString(length);
        tempLengthStringValue.SetString(lengthIsoString.c_str(), lengthIsoString.size(), allocator);
        parent.AddMember("length", tempLengthStringValue, allocator);
    }
}

LastBirthdaysProperty LastBirthdaysProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    LastBirthdaysProperty lastBirthdays;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("mom");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempMomIsoString = itr->value.GetString();
            lastBirthdays.mom = parseIsoTimestamp(tempMomIsoString);
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
            auto tempDadIsoString = itr->value.GetString();
            lastBirthdays.dad = parseIsoTimestamp(tempDadIsoString);
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
            auto tempSisterIsoString = itr->value.GetString();
            lastBirthdays.sister = parseIsoTimestamp(tempSisterIsoString);
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
            lastBirthdays.brothersAge = itr->value.GetInt();
        }
        else
        {
            lastBirthdays.brothersAge = boost::none;
        }
    }

    return lastBirthdays;
};

void LastBirthdaysProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempMomStringValue;
        std::string momIsoString = timePointToIsoString(mom);
        tempMomStringValue.SetString(momIsoString.c_str(), momIsoString.size(), allocator);
        parent.AddMember("mom", tempMomStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempDadStringValue;
        std::string dadIsoString = timePointToIsoString(dad);
        tempDadStringValue.SetString(dadIsoString.c_str(), dadIsoString.size(), allocator);
        parent.AddMember("dad", tempDadStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempSisterStringValue;
        std::string sisterIsoString = timePointToIsoString(*sister);
        tempSisterStringValue.SetString(sisterIsoString.c_str(), sisterIsoString.size(), allocator);
        parent.AddMember("sister", tempSisterStringValue, allocator);
    }

    if (brothersAge)
        parent.AddMember("brothers_age", *brothersAge, allocator);
}
