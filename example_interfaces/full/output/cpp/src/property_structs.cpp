

#include "property_structs.hpp"
#include <rapidjson/document.h>



FavoriteFoodsProperty FavoriteFoodsProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    FavoriteFoodsProperty favoriteFoods;
    
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("drink");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            
            favoriteFoods.drink = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("slices_of_pizza");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            
            favoriteFoods.slices_of_pizza = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("breakfast");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            
            favoriteFoods.breakfast = itr->value.GetString();

        } else {
            favoriteFoods.breakfast = boost::none;
        }
    }

    return favoriteFoods;
};

rapidjson::Value FavoriteFoodsProperty::ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const
{
    rapidjson::Value obj(rapidjson::kObjectType);
    
    
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(drink.c_str(), drink.size(), allocator);
        obj.AddMember("drink", tempStringValue, allocator);
    }

    
    obj.AddMember("slices_of_pizza", slices_of_pizza, allocator);

    if (breakfast) 
    { 
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(breakfast->c_str(), breakfast->size(), allocator);
        obj.AddMember("breakfast", tempStringValue, allocator);
    }

    return obj;
}

LunchMenuProperty LunchMenuProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    LunchMenuProperty lunchMenu;
    
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("monday");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject()) {
            
            lunchMenu.monday = Lunch::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("tuesday");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject()) {
            
            lunchMenu.tuesday = Lunch::FromRapidJsonObject(itr->value);


        } else {
            throw std::runtime_error("Received payload doesn't have required value/type");
        
        }
    }

    return lunchMenu;
};

rapidjson::Value LunchMenuProperty::ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const
{
    rapidjson::Value obj(rapidjson::kObjectType);
    
    
    
    return obj;
}
