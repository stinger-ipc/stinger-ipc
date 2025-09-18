/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/

#pragma once
#include <string>
#include <rapidjson/document.h>
#include "enums.hpp"
#include "structs.hpp"

/**
 * The `favorite_number` property contains a single field:
 *   int number;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * My favorite number
 * 
 */
typedef int FavoriteNumberProperty;

struct FavoriteFoodsProperty
{
    static FavoriteFoodsProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    rapidjson::Value ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const;
    std::string drink;
    int slices_of_pizza;
    boost::optional<std::string> breakfast;
};

struct LunchMenuProperty
{
    static LunchMenuProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    rapidjson::Value ToRapidJsonObject(rapidjson::Document::AllocatorType& allocator) const;
    Lunch monday;
    Lunch tuesday;
};
