/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.
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

struct AllTypes
{
    static AllTypes FromRapidJsonObject(const rapidjson::Value& jsonObj);
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    bool theBool;
    int theInt;
    double theNumber;
    std::string theStr;
    Numbers theEnum;
    std::chrono::time_point<std::chrono::system_clock> dateAndTime;
    std::chrono::duration<double> timeDuration;
    std::vector<uint8_t> data;
    boost::optional<int> optionalInteger;
    boost::optional<std::string> optionalString;
    boost::optional<Numbers> optionalEnum;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> optionalDateTime;
    boost::optional<std::chrono::duration<double>> optionalDuration;
    boost::optional<std::vector<uint8_t>> optionalBinary;
};
