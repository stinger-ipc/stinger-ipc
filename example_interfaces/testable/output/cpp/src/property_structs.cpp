

#include "property_structs.hpp"
#include <rapidjson/document.h>

ReadWriteIntegerProperty ReadWriteIntegerProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteIntegerProperty readWriteInteger;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readWriteInteger.value = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readWriteInteger;
};

void ReadWriteIntegerProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("value", value, allocator);
}

ReadOnlyIntegerProperty ReadOnlyIntegerProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadOnlyIntegerProperty readOnlyInteger;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readOnlyInteger.value = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readOnlyInteger;
};

void ReadOnlyIntegerProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("value", value, allocator);
}

ReadWriteOptionalIntegerProperty ReadWriteOptionalIntegerProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteOptionalIntegerProperty readWriteOptionalInteger;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readWriteOptionalInteger.value = itr->value.GetInt();
        }
        else
        {
            readWriteOptionalInteger.value = boost::none;
        }
    }

    return readWriteOptionalInteger;
};

void ReadWriteOptionalIntegerProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (value)
        parent.AddMember("value", *value, allocator);
}

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

ReadOnlyStringProperty ReadOnlyStringProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadOnlyStringProperty readOnlyString;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            readOnlyString.value = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readOnlyString;
};

void ReadOnlyStringProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value.c_str(), value.size(), allocator);
        parent.AddMember("value", tempStringValue, allocator);
    }
}

ReadWriteStringProperty ReadWriteStringProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteStringProperty readWriteString;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            readWriteString.value = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readWriteString;
};

void ReadWriteStringProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value.c_str(), value.size(), allocator);
        parent.AddMember("value", tempStringValue, allocator);
    }
}

ReadWriteOptionalStringProperty ReadWriteOptionalStringProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteOptionalStringProperty readWriteOptionalString;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            readWriteOptionalString.value = itr->value.GetString();
        }
        else
        {
            readWriteOptionalString.value = boost::none;
        }
    }

    return readWriteOptionalString;
};

void ReadWriteOptionalStringProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (value)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value->c_str(), value->size(), allocator);
        parent.AddMember("value", tempStringValue, allocator);
    }
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

ReadWriteStructProperty ReadWriteStructProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteStructProperty readWriteStruct;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            readWriteStruct.value = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readWriteStruct;
};

void ReadWriteStructProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        value.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("value", tempStructValue, allocator);
    }
}

ReadWriteOptionalStructProperty ReadWriteOptionalStructProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteOptionalStructProperty readWriteOptionalStruct;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            readWriteOptionalStruct.value = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            readWriteOptionalStruct.value = boost::none;
        }
    }

    return readWriteOptionalStruct;
};

void ReadWriteOptionalStructProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempStructValue;
        if (value)
        {
            tempStructValue.SetObject();
            value->AddToRapidJsonObject(tempStructValue, allocator);
        }
        else
        {
            tempStructValue.SetNull();
        }
        parent.AddMember("value", tempStructValue, allocator);
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
    { // Restrict Scope
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        first.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("first", tempStructValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempStructValue;
        if (second)
        {
            tempStructValue.SetObject();
            second->AddToRapidJsonObject(tempStructValue, allocator);
        }
        else
        {
            tempStructValue.SetNull();
        }
        parent.AddMember("second", tempStructValue, allocator);
    }
}

ReadOnlyEnumProperty ReadOnlyEnumProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadOnlyEnumProperty readOnlyEnum;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readOnlyEnum.value = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readOnlyEnum;
};

void ReadOnlyEnumProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("value", static_cast<int>(value), allocator);
}

ReadWriteEnumProperty ReadWriteEnumProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteEnumProperty readWriteEnum;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readWriteEnum.value = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readWriteEnum;
};

void ReadWriteEnumProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("value", static_cast<int>(value), allocator);
}

ReadWriteOptionalEnumProperty ReadWriteOptionalEnumProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteOptionalEnumProperty readWriteOptionalEnum;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            readWriteOptionalEnum.value = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            readWriteOptionalEnum.value = boost::none;
        }
    }

    return readWriteOptionalEnum;
};

void ReadWriteOptionalEnumProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("value", static_cast<int>(*value), allocator);
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

ReadWriteDatetimeProperty ReadWriteDatetimeProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteDatetimeProperty readWriteDatetime;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            readWriteDatetime.value = parseIsoTimestamp(tempValueIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readWriteDatetime;
};

void ReadWriteDatetimeProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = timePointToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

ReadWriteOptionalDatetimeProperty ReadWriteOptionalDatetimeProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteOptionalDatetimeProperty readWriteOptionalDatetime;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            readWriteOptionalDatetime.value = parseIsoTimestamp(tempValueIsoString);
        }
        else
        {
            readWriteOptionalDatetime.value = boost::none;
        }
    }

    return readWriteOptionalDatetime;
};

void ReadWriteOptionalDatetimeProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = timePointToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

ReadWriteTwoDatetimesProperty ReadWriteTwoDatetimesProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoDatetimesProperty readWriteTwoDatetimes;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstIsoString = itr->value.GetString();
            readWriteTwoDatetimes.first = parseIsoTimestamp(tempFirstIsoString);
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
            auto tempSecondIsoString = itr->value.GetString();
            readWriteTwoDatetimes.second = parseIsoTimestamp(tempSecondIsoString);
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

ReadWriteDurationProperty ReadWriteDurationProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteDurationProperty readWriteDuration;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            readWriteDuration.value = parseIsoDuration(tempValueIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readWriteDuration;
};

void ReadWriteDurationProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = durationToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

ReadWriteOptionalDurationProperty ReadWriteOptionalDurationProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteOptionalDurationProperty readWriteOptionalDuration;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            readWriteOptionalDuration.value = parseIsoDuration(tempValueIsoString);
        }
        else
        {
            readWriteOptionalDuration.value = boost::none;
        }
    }

    return readWriteOptionalDuration;
};

void ReadWriteOptionalDurationProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = durationToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

ReadWriteTwoDurationsProperty ReadWriteTwoDurationsProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoDurationsProperty readWriteTwoDurations;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstIsoString = itr->value.GetString();
            readWriteTwoDurations.first = parseIsoDuration(tempFirstIsoString);
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
            auto tempSecondIsoString = itr->value.GetString();
            readWriteTwoDurations.second = parseIsoDuration(tempSecondIsoString);
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

ReadWriteBinaryProperty ReadWriteBinaryProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteBinaryProperty readWriteBinary;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueB64String = itr->value.GetString();
            readWriteBinary.value = base64Decode(tempValueB64String);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return readWriteBinary;
};

void ReadWriteBinaryProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = base64Encode(value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

ReadWriteOptionalBinaryProperty ReadWriteOptionalBinaryProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteOptionalBinaryProperty readWriteOptionalBinary;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueB64String = itr->value.GetString();
            readWriteOptionalBinary.value = base64Decode(tempValueB64String);
        }
        else
        {
            readWriteOptionalBinary.value = boost::none;
        }
    }

    return readWriteOptionalBinary;
};

void ReadWriteOptionalBinaryProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = base64Encode(*value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

ReadWriteTwoBinariesProperty ReadWriteTwoBinariesProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ReadWriteTwoBinariesProperty readWriteTwoBinaries;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstB64String = itr->value.GetString();
            readWriteTwoBinaries.first = base64Decode(tempFirstB64String);
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
            auto tempSecondB64String = itr->value.GetString();
            readWriteTwoBinaries.second = base64Decode(tempSecondB64String);
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
