

#include "property_structs.hpp"
#include <rapidjson/document.h>

ReadWriteTwoIntegersProperty ReadWriteTwoIntegersProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoIntegersProperty readWriteTwoIntegers;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readWriteTwoIntegers.first = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("second");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readWriteTwoIntegers.second = itr->value.GetInt();
        }
        else
        {
            readWriteTwoIntegers.second = boost::none;
        }
    }

    return readWriteTwoIntegers;
};

void ReadWriteTwoIntegersProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("first", first, allocator);

    if (second)
        parent.AddMember("second", *second, allocator);
}

ReadWriteTwoStringsProperty ReadWriteTwoStringsProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoStringsProperty readWriteTwoStrings;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            readWriteTwoStrings.first = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("second");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            readWriteTwoStrings.second = itr->value.GetString();
        }
        else
        {
            readWriteTwoStrings.second = boost::none;
        }
    }

    return readWriteTwoStrings;
};

void ReadWriteTwoStringsProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(first.c_str(), first.size(), allocator);
        parent.AddMember("first", tempStringValue, allocator);
    }

    if (second)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(second->c_str(), second->size(), allocator);
        parent.AddMember("second", tempStringValue, allocator);
    }
}

ReadWriteTwoStructsProperty ReadWriteTwoStructsProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoStructsProperty readWriteTwoStructs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            readWriteTwoStructs.first = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("second");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            readWriteTwoStructs.second = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            readWriteTwoStructs.second = boost::none;
        }
    }

    return readWriteTwoStructs;
};

void ReadWriteTwoStructsProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

ReadWriteTwoEnumsProperty ReadWriteTwoEnumsProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoEnumsProperty readWriteTwoEnums;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readWriteTwoEnums.first = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("second");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readWriteTwoEnums.second = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            readWriteTwoEnums.second = boost::none;
        }
    }

    return readWriteTwoEnums;
};

void ReadWriteTwoEnumsProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("first", static_cast<int>(first), allocator);

    parent.AddMember("second", static_cast<int>(*second), allocator);
}

ReadWriteTwoDatetimesProperty ReadWriteTwoDatetimesProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoDatetimesProperty readWriteTwoDatetimes;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("second");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            readWriteTwoDatetimes.second = boost::none;
        }
    }

    return readWriteTwoDatetimes;
};

void ReadWriteTwoDatetimesProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = timePointToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), allocator);
        parent.AddMember("first", tempFirstStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = timePointToIsoString(*second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), allocator);
        parent.AddMember("second", tempSecondStringValue, allocator);
    }
}

ReadWriteTwoDurationsProperty ReadWriteTwoDurationsProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoDurationsProperty readWriteTwoDurations;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("second");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            readWriteTwoDurations.second = boost::none;
        }
    }

    return readWriteTwoDurations;
};

void ReadWriteTwoDurationsProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = durationToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), allocator);
        parent.AddMember("first", tempFirstStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = durationToIsoString(*second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), allocator);
        parent.AddMember("second", tempSecondStringValue, allocator);
    }
}

ReadWriteTwoBinariesProperty ReadWriteTwoBinariesProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoBinariesProperty readWriteTwoBinaries;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("second");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            readWriteTwoBinaries.second = boost::none;
        }
    }

    return readWriteTwoBinaries;
};

void ReadWriteTwoBinariesProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstB64String = base64Encode(first);
        tempFirstStringValue.SetString(firstB64String.c_str(), firstB64String.size(), allocator);
        parent.AddMember("first", tempFirstStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondB64String = base64Encode(*second);
        tempSecondStringValue.SetString(secondB64String.c_str(), secondB64String.size(), allocator);
        parent.AddMember("second", tempSecondStringValue, allocator);
    }
}
