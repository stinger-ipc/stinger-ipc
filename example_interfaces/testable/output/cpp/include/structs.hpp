/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once
#include <string>
#include <cstddef>
#include <chrono>
#include <vector>
#include <boost/optional.hpp>
#include <rapidjson/document.h>
#include "enums.hpp"
#include "conversions.hpp"

struct Entry
{
    static Entry FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    int key;
    std::string value;
};

struct AllTypes
{
    static AllTypes FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    bool theBool;
    int theInt;
    double theNumber;
    std::string theStr;
    Numbers theEnum;
    Entry anEntryObject;
    std::chrono::time_point<std::chrono::system_clock> dateAndTime;
    std::chrono::duration<double> timeDuration;
    std::vector<uint8_t> data;
    boost::optional<int> optionalInteger;
    boost::optional<std::string> optionalString;
    boost::optional<Numbers> optionalEnum;
    boost::optional<Entry> optionalEntryObject;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> optionalDateTime;
    boost::optional<std::chrono::duration<double>> optionalDuration;
    boost::optional<std::vector<uint8_t>> optionalBinary;
    std::vector<int> arrayOfIntegers;
    boost::optional<std::vector<int>> optionalArrayOfIntegers;
    std::vector<std::string> arrayOfStrings;
    boost::optional<std::vector<std::string>> optionalArrayOfStrings;
    std::vector<Numbers> arrayOfEnums;
    boost::optional<std::vector<Numbers>> optionalArrayOfEnums;
    std::vector<std::chrono::time_point<std::chrono::system_clock>> arrayOfDatetimes;
    boost::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalArrayOfDatetimes;
    std::vector<std::chrono::duration<double>> arrayOfDurations;
    boost::optional<std::vector<std::chrono::duration<double>>> optionalArrayOfDurations;
    std::vector<std::vector<uint8_t>> arrayOfBinaries;
    boost::optional<std::vector<std::vector<uint8_t>>> optionalArrayOfBinaries;
    std::vector<Entry> arrayOfEntryObjects;
    boost::optional<std::vector<Entry>> optionalArrayOfEntryObjects;
};
