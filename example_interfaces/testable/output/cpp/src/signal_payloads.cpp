
#include "signal_payloads.hpp"

// --- (De-)Serialization for empty signal payload ---
EmptyPayload EmptyPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    EmptyPayload emptyPayload;

    return emptyPayload;
};

void EmptyPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for singleInt signal payload ---
SingleIntPayload SingleIntPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleIntPayload singleIntPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            singleIntPayload.value = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return singleIntPayload;
};

void SingleIntPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("value", value, allocator);
}

// --- (De-)Serialization for singleOptionalInt signal payload ---
SingleOptionalIntPayload SingleOptionalIntPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleOptionalIntPayload singleOptionalIntPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            singleOptionalIntPayload.value = itr->value.GetInt();
        }
        else
        {
            singleOptionalIntPayload.value = boost::none;
        }
    }

    return singleOptionalIntPayload;
};

void SingleOptionalIntPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (value)
        parent.AddMember("value", *value, allocator);
}

// --- (De-)Serialization for threeIntegers signal payload ---
ThreeIntegersPayload ThreeIntegersPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ThreeIntegersPayload threeIntegersPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            threeIntegersPayload.first = itr->value.GetInt();
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
            threeIntegersPayload.second = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("third");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            threeIntegersPayload.third = itr->value.GetInt();
        }
        else
        {
            threeIntegersPayload.third = boost::none;
        }
    }

    return threeIntegersPayload;
};

void ThreeIntegersPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("first", first, allocator);

    parent.AddMember("second", second, allocator);

    if (third)
        parent.AddMember("third", *third, allocator);
}

// --- (De-)Serialization for singleString signal payload ---
SingleStringPayload SingleStringPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleStringPayload singleStringPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            singleStringPayload.value = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return singleStringPayload;
};

void SingleStringPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value.c_str(), value.size(), allocator);
        parent.AddMember("value", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for singleOptionalString signal payload ---
SingleOptionalStringPayload SingleOptionalStringPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleOptionalStringPayload singleOptionalStringPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            singleOptionalStringPayload.value = itr->value.GetString();
        }
        else
        {
            singleOptionalStringPayload.value = boost::none;
        }
    }

    return singleOptionalStringPayload;
};

void SingleOptionalStringPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (value)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value->c_str(), value->size(), allocator);
        parent.AddMember("value", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for threeStrings signal payload ---
ThreeStringsPayload ThreeStringsPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ThreeStringsPayload threeStringsPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            threeStringsPayload.first = itr->value.GetString();
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
            threeStringsPayload.second = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("third");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            threeStringsPayload.third = itr->value.GetString();
        }
        else
        {
            threeStringsPayload.third = boost::none;
        }
    }

    return threeStringsPayload;
};

void ThreeStringsPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(first.c_str(), first.size(), allocator);
        parent.AddMember("first", tempStringValue, allocator);
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(second.c_str(), second.size(), allocator);
        parent.AddMember("second", tempStringValue, allocator);
    }

    if (third)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(third->c_str(), third->size(), allocator);
        parent.AddMember("third", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for singleEnum signal payload ---
SingleEnumPayload SingleEnumPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleEnumPayload singleEnumPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            singleEnumPayload.value = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return singleEnumPayload;
};

void SingleEnumPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("value", static_cast<int>(value), allocator);
}

// --- (De-)Serialization for singleOptionalEnum signal payload ---
SingleOptionalEnumPayload SingleOptionalEnumPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleOptionalEnumPayload singleOptionalEnumPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            singleOptionalEnumPayload.value = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            singleOptionalEnumPayload.value = boost::none;
        }
    }

    return singleOptionalEnumPayload;
};

void SingleOptionalEnumPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("value", static_cast<int>(*value), allocator);
}

// --- (De-)Serialization for threeEnums signal payload ---
ThreeEnumsPayload ThreeEnumsPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ThreeEnumsPayload threeEnumsPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            threeEnumsPayload.first = static_cast<Numbers>(itr->value.GetInt());
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
            threeEnumsPayload.second = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("third");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            threeEnumsPayload.third = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            threeEnumsPayload.third = boost::none;
        }
    }

    return threeEnumsPayload;
};

void ThreeEnumsPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("first", static_cast<int>(first), allocator);

    parent.AddMember("second", static_cast<int>(second), allocator);

    parent.AddMember("third", static_cast<int>(*third), allocator);
}

// --- (De-)Serialization for singleStruct signal payload ---
SingleStructPayload SingleStructPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleStructPayload singleStructPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            singleStructPayload.value = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return singleStructPayload;
};

void SingleStructPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for singleOptionalStruct signal payload ---
SingleOptionalStructPayload SingleOptionalStructPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleOptionalStructPayload singleOptionalStructPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            singleOptionalStructPayload.value = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            singleOptionalStructPayload.value = boost::none;
        }
    }

    return singleOptionalStructPayload;
};

void SingleOptionalStructPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for threeStructs signal payload ---
ThreeStructsPayload ThreeStructsPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ThreeStructsPayload threeStructsPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            threeStructsPayload.first = AllTypes::FromRapidJsonObject(itr->value);
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
            threeStructsPayload.second = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("third");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            threeStructsPayload.third = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            threeStructsPayload.third = boost::none;
        }
    }

    return threeStructsPayload;
};

void ThreeStructsPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for singleDateTime signal payload ---
SingleDateTimePayload SingleDateTimePayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleDateTimePayload singleDateTimePayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            singleDateTimePayload.value = parseIsoTimestamp(tempValueIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return singleDateTimePayload;
};

void SingleDateTimePayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = timePointToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

// --- (De-)Serialization for singleOptionalDatetime signal payload ---
SingleOptionalDatetimePayload SingleOptionalDatetimePayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleOptionalDatetimePayload singleOptionalDatetimePayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            singleOptionalDatetimePayload.value = parseIsoTimestamp(tempValueIsoString);
        }
        else
        {
            singleOptionalDatetimePayload.value = boost::none;
        }
    }

    return singleOptionalDatetimePayload;
};

void SingleOptionalDatetimePayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = timePointToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

// --- (De-)Serialization for threeDateTimes signal payload ---
ThreeDateTimesPayload ThreeDateTimesPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ThreeDateTimesPayload threeDateTimesPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstIsoString = itr->value.GetString();
            threeDateTimesPayload.first = parseIsoTimestamp(tempFirstIsoString);
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
            threeDateTimesPayload.second = parseIsoTimestamp(tempSecondIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("third");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempThirdIsoString = itr->value.GetString();
            threeDateTimesPayload.third = parseIsoTimestamp(tempThirdIsoString);
        }
        else
        {
            threeDateTimesPayload.third = boost::none;
        }
    }

    return threeDateTimesPayload;
};

void ThreeDateTimesPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = timePointToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), allocator);
        parent.AddMember("first", tempFirstStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = timePointToIsoString(second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), allocator);
        parent.AddMember("second", tempSecondStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempThirdStringValue;
        std::string thirdIsoString = timePointToIsoString(*third);
        tempThirdStringValue.SetString(thirdIsoString.c_str(), thirdIsoString.size(), allocator);
        parent.AddMember("third", tempThirdStringValue, allocator);
    }
}

// --- (De-)Serialization for singleDuration signal payload ---
SingleDurationPayload SingleDurationPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleDurationPayload singleDurationPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            singleDurationPayload.value = parseIsoDuration(tempValueIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return singleDurationPayload;
};

void SingleDurationPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = durationToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

// --- (De-)Serialization for singleOptionalDuration signal payload ---
SingleOptionalDurationPayload SingleOptionalDurationPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleOptionalDurationPayload singleOptionalDurationPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueIsoString = itr->value.GetString();
            singleOptionalDurationPayload.value = parseIsoDuration(tempValueIsoString);
        }
        else
        {
            singleOptionalDurationPayload.value = boost::none;
        }
    }

    return singleOptionalDurationPayload;
};

void SingleOptionalDurationPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = durationToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

// --- (De-)Serialization for threeDurations signal payload ---
ThreeDurationsPayload ThreeDurationsPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ThreeDurationsPayload threeDurationsPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstIsoString = itr->value.GetString();
            threeDurationsPayload.first = parseIsoDuration(tempFirstIsoString);
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
            threeDurationsPayload.second = parseIsoDuration(tempSecondIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("third");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempThirdIsoString = itr->value.GetString();
            threeDurationsPayload.third = parseIsoDuration(tempThirdIsoString);
        }
        else
        {
            threeDurationsPayload.third = boost::none;
        }
    }

    return threeDurationsPayload;
};

void ThreeDurationsPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = durationToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), allocator);
        parent.AddMember("first", tempFirstStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = durationToIsoString(second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), allocator);
        parent.AddMember("second", tempSecondStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempThirdStringValue;
        std::string thirdIsoString = durationToIsoString(*third);
        tempThirdStringValue.SetString(thirdIsoString.c_str(), thirdIsoString.size(), allocator);
        parent.AddMember("third", tempThirdStringValue, allocator);
    }
}

// --- (De-)Serialization for singleBinary signal payload ---
SingleBinaryPayload SingleBinaryPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleBinaryPayload singleBinaryPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueB64String = itr->value.GetString();
            singleBinaryPayload.value = base64Decode(tempValueB64String);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return singleBinaryPayload;
};

void SingleBinaryPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = base64Encode(value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

// --- (De-)Serialization for singleOptionalBinary signal payload ---
SingleOptionalBinaryPayload SingleOptionalBinaryPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SingleOptionalBinaryPayload singleOptionalBinaryPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempValueB64String = itr->value.GetString();
            singleOptionalBinaryPayload.value = base64Decode(tempValueB64String);
        }
        else
        {
            singleOptionalBinaryPayload.value = boost::none;
        }
    }

    return singleOptionalBinaryPayload;
};

void SingleOptionalBinaryPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = base64Encode(*value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), allocator);
        parent.AddMember("value", tempValueStringValue, allocator);
    }
}

// --- (De-)Serialization for threeBinaries signal payload ---
ThreeBinariesPayload ThreeBinariesPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ThreeBinariesPayload threeBinariesPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempFirstB64String = itr->value.GetString();
            threeBinariesPayload.first = base64Decode(tempFirstB64String);
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
            threeBinariesPayload.second = base64Decode(tempSecondB64String);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("third");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempThirdB64String = itr->value.GetString();
            threeBinariesPayload.third = base64Decode(tempThirdB64String);
        }
        else
        {
            threeBinariesPayload.third = boost::none;
        }
    }

    return threeBinariesPayload;
};

void ThreeBinariesPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempFirstStringValue;
        std::string firstB64String = base64Encode(first);
        tempFirstStringValue.SetString(firstB64String.c_str(), firstB64String.size(), allocator);
        parent.AddMember("first", tempFirstStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempSecondStringValue;
        std::string secondB64String = base64Encode(second);
        tempSecondStringValue.SetString(secondB64String.c_str(), secondB64String.size(), allocator);
        parent.AddMember("second", tempSecondStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempThirdStringValue;
        std::string thirdB64String = base64Encode(*third);
        tempThirdStringValue.SetString(thirdB64String.c_str(), thirdB64String.size(), allocator);
        parent.AddMember("third", tempThirdStringValue, allocator);
    }
}
