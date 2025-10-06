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
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::string drink;
    int slices_of_pizza;
    boost::optional<std::string> breakfast;
};

struct LunchMenuProperty
{
    static LunchMenuProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    Lunch monday;
    Lunch tuesday; ///< Tuesday's lunch menu.
};

/**
 * The `family_name` property contains a single field:
 *   std::string family_name;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * This is to test a property with a single string value.
 */
typedef std::string FamilyNameProperty;

/**
 * The `last_breakfast_time` property contains a single field:
 *   std::chrono::time_point<std::chrono::system_clock> timestamp;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * This is to test a property with a single datetime value.
 */
typedef std::chrono::time_point<std::chrono::system_clock> LastBreakfastTimeProperty;

/**
 * The `breakfast_length` property contains a single field:
 *    length;
 *
 * Because there is only one field, no outer-structure is needed. 
 *
 * This is to test a property with a single duration value.
 */
typedef BreakfastLengthProperty;

/**
 * This is to test a property with multiple datetime values.
 */
struct LastBirthdaysProperty
{
    static LastBirthdaysProperty FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    std::chrono::time_point<std::chrono::system_clock> mom;
    std::chrono::time_point<std::chrono::system_clock> dad;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> sister;
    boost::optional<int> brothers_age;
};
