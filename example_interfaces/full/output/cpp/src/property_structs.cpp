

#include "property_structs.hpp"
#include <rapidjson/document.h>

namespace stinger {

namespace gen {
namespace full {

FavoriteNumberProperty FavoriteNumberProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    FavoriteNumberProperty favoriteNumber;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("number");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            favoriteNumber.number = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'number' argument doesn't have required value/type");
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
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            favoriteFoods.drink = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'drink' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("slices_of_pizza");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            favoriteFoods.slicesOfPizza = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'slices_of_pizza' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("breakfast");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            favoriteFoods.breakfast = itr->value.GetString();

        } else {
            favoriteFoods.breakfast = std::nullopt;
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

    if (breakfast) {
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
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject()) {
            lunchMenu.monday = Lunch::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'monday' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("tuesday");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject()) {
            lunchMenu.tuesday = Lunch::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'tuesday' argument doesn't have required value/type");
        }
    }

    return lunchMenu;
};

void LunchMenuProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
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
}

FamilyNameProperty FamilyNameProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    FamilyNameProperty familyName;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("family_name");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            familyName.familyName = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'family_name' argument doesn't have required value/type");
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
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            auto tempTimestampIsoString = itr->value.GetString();
            lastBreakfastTime.timestamp = stinger::utils::parseIsoTimestamp(tempTimestampIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'timestamp' argument doesn't have required value/type");
        }
    }

    return lastBreakfastTime;
};

void LastBreakfastTimeProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = stinger::utils::timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), allocator);
        parent.AddMember("timestamp", tempTimestampStringValue, allocator);
    }
}

LastBirthdaysProperty LastBirthdaysProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    LastBirthdaysProperty lastBirthdays;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("mom");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            auto tempMomIsoString = itr->value.GetString();
            lastBirthdays.mom = stinger::utils::parseIsoTimestamp(tempMomIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'mom' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("dad");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            auto tempDadIsoString = itr->value.GetString();
            lastBirthdays.dad = stinger::utils::parseIsoTimestamp(tempDadIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'dad' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("sister");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            auto tempSisterIsoString = itr->value.GetString();
            lastBirthdays.sister = stinger::utils::parseIsoTimestamp(tempSisterIsoString);

        } else {
            lastBirthdays.sister = std::nullopt;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("brothers_age");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            lastBirthdays.brothersAge = itr->value.GetInt();

        } else {
            lastBirthdays.brothersAge = std::nullopt;
        }
    }

    return lastBirthdays;
};

void LastBirthdaysProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempMomStringValue;
        std::string momIsoString = stinger::utils::timePointToIsoString(mom);
        tempMomStringValue.SetString(momIsoString.c_str(), momIsoString.size(), allocator);
        parent.AddMember("mom", tempMomStringValue, allocator);
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempDadStringValue;
        std::string dadIsoString = stinger::utils::timePointToIsoString(dad);
        tempDadStringValue.SetString(dadIsoString.c_str(), dadIsoString.size(), allocator);
        parent.AddMember("dad", tempDadStringValue, allocator);
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempSisterStringValue;
        std::string sisterIsoString = stinger::utils::timePointToIsoString(*sister);
        tempSisterStringValue.SetString(sisterIsoString.c_str(), sisterIsoString.size(), allocator);
        parent.AddMember("sister", tempSisterStringValue, allocator);
    }

    if (brothersAge)
        parent.AddMember("brothers_age", *brothersAge, allocator);
}

} // namespace full

} // namespace gen

} // namespace stinger
