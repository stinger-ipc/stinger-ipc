

#include "structs.hpp"

AllTypes AllTypes::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    AllTypes allTypes;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("the_bool");
        if (itr != jsonObj.MemberEnd() && itr->value.IsBool())
        {
            allTypes.theBool = itr->value.GetBool();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("the_int");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            allTypes.theInt = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("the_number");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            allTypes.theNumber = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("the_str");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            allTypes.theStr = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("the_enum");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            allTypes.theEnum = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("date_and_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempDateAndTimeIsoString = itr->value.GetString();
            allTypes.dateAndTime = parseIsoTimestamp(tempDateAndTimeIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("time_duration");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTimeDurationIsoString = itr->value.GetString();
            allTypes.timeDuration = parseIsoDuration(tempTimeDurationIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("data");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempDataB64String = itr->value.GetString();
            allTypes.data = base64Decode(tempDataB64String);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("OptionalInteger");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            allTypes.optionalInteger = itr->value.GetInt();
        }
        else
        {
            allTypes.optionalInteger = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("OptionalString");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            allTypes.optionalString = itr->value.GetString();
        }
        else
        {
            allTypes.optionalString = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("OptionalEnum");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            allTypes.optionalEnum = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            allTypes.optionalEnum = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("OptionalDateTime");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOptionalDateTimeIsoString = itr->value.GetString();
            allTypes.optionalDateTime = parseIsoTimestamp(tempOptionalDateTimeIsoString);
        }
        else
        {
            allTypes.optionalDateTime = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("OptionalDuration");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOptionalDurationIsoString = itr->value.GetString();
            allTypes.optionalDuration = parseIsoDuration(tempOptionalDurationIsoString);
        }
        else
        {
            allTypes.optionalDuration = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("OptionalBinary");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOptionalBinaryB64String = itr->value.GetString();
            allTypes.optionalBinary = base64Decode(tempOptionalBinaryB64String);
        }
        else
        {
            allTypes.optionalBinary = boost::none;
        }
    }

    return allTypes;
};

void AllTypes::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("the_bool", theBool, allocator);

    parent.AddMember("the_int", theInt, allocator);

    parent.AddMember("the_number", theNumber, allocator);

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(theStr.c_str(), theStr.size(), allocator);
        parent.AddMember("the_str", tempStringValue, allocator);
    }

    parent.AddMember("the_enum", static_cast<int>(theEnum), allocator);

    { // Restrict Scope
        rapidjson::Value tempDateAndTimeStringValue;
        std::string dateAndTimeIsoString = timePointToIsoString(dateAndTime);
        tempDateAndTimeStringValue.SetString(dateAndTimeIsoString.c_str(), dateAndTimeIsoString.size(), allocator);
        parent.AddMember("date_and_time", tempDateAndTimeStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempTimeDurationStringValue;
        std::string timeDurationIsoString = durationToIsoString(timeDuration);
        tempTimeDurationStringValue.SetString(timeDurationIsoString.c_str(), timeDurationIsoString.size(), allocator);
        parent.AddMember("time_duration", tempTimeDurationStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempDataStringValue;
        std::string dataB64String = base64Encode(data);
        tempDataStringValue.SetString(dataB64String.c_str(), dataB64String.size(), allocator);
        parent.AddMember("data", tempDataStringValue, allocator);
    }
    if (optionalInteger)
        parent.AddMember("OptionalInteger", *optionalInteger, allocator);

    if (optionalString)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(optionalString->c_str(), optionalString->size(), allocator);
        parent.AddMember("OptionalString", tempStringValue, allocator);
    }

    parent.AddMember("OptionalEnum", static_cast<int>(*optionalEnum), allocator);

    { // Restrict Scope
        rapidjson::Value tempOptionalDateTimeStringValue;
        std::string optionalDateTimeIsoString = timePointToIsoString(*optionalDateTime);
        tempOptionalDateTimeStringValue.SetString(optionalDateTimeIsoString.c_str(), optionalDateTimeIsoString.size(), allocator);
        parent.AddMember("OptionalDateTime", tempOptionalDateTimeStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempOptionalDurationStringValue;
        std::string optionalDurationIsoString = durationToIsoString(*optionalDuration);
        tempOptionalDurationStringValue.SetString(optionalDurationIsoString.c_str(), optionalDurationIsoString.size(), allocator);
        parent.AddMember("OptionalDuration", tempOptionalDurationStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempOptionalBinaryStringValue;
        std::string optionalBinaryB64String = base64Encode(*optionalBinary);
        tempOptionalBinaryStringValue.SetString(optionalBinaryB64String.c_str(), optionalBinaryB64String.size(), allocator);
        parent.AddMember("OptionalBinary", tempOptionalBinaryStringValue, allocator);
    }
}
