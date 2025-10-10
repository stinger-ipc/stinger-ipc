
#include "method_payloads.hpp"

#include <rapidjson/document.h>
#include "conversions.hpp"

// --- (De-)Serialization for addNumbers method request arguments ---
AddNumbersRequestArguments AddNumbersRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    AddNumbersRequestArguments addNumbersArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            addNumbersArgs.first = itr->value.GetInt();
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
            addNumbersArgs.second = itr->value.GetInt();
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
            addNumbersArgs.third = itr->value.GetInt();
        }
        else
        {
            addNumbersArgs.third = boost::none;
        }
    }

    return addNumbersArgs;
};

void AddNumbersRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("first", first, allocator);

    parent.AddMember("second", second, allocator);

    if (third)
        parent.AddMember("third", *third, allocator);
}

// --- (De-)Serialization for addNumbers method return type ---
AddNumbersReturnValues AddNumbersReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    AddNumbersReturnValues addNumbersRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("sum");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            addNumbersRc.sum = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return addNumbersRc;
};

void AddNumbersReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("sum", sum, allocator);
}

// --- (De-)Serialization for doSomething method request arguments ---
DoSomethingRequestArguments DoSomethingRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    DoSomethingRequestArguments doSomethingArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("aString");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            doSomethingArgs.aString = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return doSomethingArgs;
};

void DoSomethingRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(aString.c_str(), aString.size(), allocator);
        parent.AddMember("aString", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for doSomething method return type ---
DoSomethingReturnValues DoSomethingReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    DoSomethingReturnValues doSomethingRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("label");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            doSomethingRc.label = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("identifier");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            doSomethingRc.identifier = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("day");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            doSomethingRc.day = static_cast<DayOfTheWeek>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return doSomethingRc;
};

void DoSomethingReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(label.c_str(), label.size(), allocator);
        parent.AddMember("label", tempStringValue, allocator);
    }

    parent.AddMember("identifier", identifier, allocator);

    parent.AddMember("day", static_cast<int>(day), allocator);
}

// --- (De-)Serialization for echo method request arguments ---
EchoRequestArguments EchoRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    EchoRequestArguments echoArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("message");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            echoArgs.message = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return echoArgs;
};

void EchoRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(message.c_str(), message.size(), allocator);
        parent.AddMember("message", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for echo method return type ---
EchoReturnValues EchoReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    EchoReturnValues echoRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("message");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            echoRc.message = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return echoRc;
};

void EchoReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(message.c_str(), message.size(), allocator);
        parent.AddMember("message", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for what_time_is_it method request arguments ---
WhatTimeIsItRequestArguments WhatTimeIsItRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    WhatTimeIsItRequestArguments whatTimeIsItArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("the_first_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTheFirstTimeIsoString = itr->value.GetString();
            whatTimeIsItArgs.theFirstTime = parseIsoTimestamp(tempTheFirstTimeIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return whatTimeIsItArgs;
};

void WhatTimeIsItRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempTheFirstTimeStringValue;
        std::string theFirstTimeIsoString = timePointToIsoString(theFirstTime);
        tempTheFirstTimeStringValue.SetString(theFirstTimeIsoString.c_str(), theFirstTimeIsoString.size(), allocator);
        parent.AddMember("the_first_time", tempTheFirstTimeStringValue, allocator);
    }
}

// --- (De-)Serialization for what_time_is_it method return type ---
WhatTimeIsItReturnValues WhatTimeIsItReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    WhatTimeIsItReturnValues whatTimeIsItRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("timestamp");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTimestampIsoString = itr->value.GetString();
            whatTimeIsItRc.timestamp = parseIsoTimestamp(tempTimestampIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return whatTimeIsItRc;
};

void WhatTimeIsItReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), allocator);
        parent.AddMember("timestamp", tempTimestampStringValue, allocator);
    }
}

// --- (De-)Serialization for set_the_time method request arguments ---
SetTheTimeRequestArguments SetTheTimeRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SetTheTimeRequestArguments setTheTimeArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("the_first_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTheFirstTimeIsoString = itr->value.GetString();
            setTheTimeArgs.theFirstTime = parseIsoTimestamp(tempTheFirstTimeIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("the_second_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTheSecondTimeIsoString = itr->value.GetString();
            setTheTimeArgs.theSecondTime = parseIsoTimestamp(tempTheSecondTimeIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return setTheTimeArgs;
};

void SetTheTimeRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempTheFirstTimeStringValue;
        std::string theFirstTimeIsoString = timePointToIsoString(theFirstTime);
        tempTheFirstTimeStringValue.SetString(theFirstTimeIsoString.c_str(), theFirstTimeIsoString.size(), allocator);
        parent.AddMember("the_first_time", tempTheFirstTimeStringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempTheSecondTimeStringValue;
        std::string theSecondTimeIsoString = timePointToIsoString(theSecondTime);
        tempTheSecondTimeStringValue.SetString(theSecondTimeIsoString.c_str(), theSecondTimeIsoString.size(), allocator);
        parent.AddMember("the_second_time", tempTheSecondTimeStringValue, allocator);
    }
}

// --- (De-)Serialization for set_the_time method return type ---
SetTheTimeReturnValues SetTheTimeReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SetTheTimeReturnValues setTheTimeRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("timestamp");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTimestampIsoString = itr->value.GetString();
            setTheTimeRc.timestamp = parseIsoTimestamp(tempTimestampIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("confirmation_message");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            setTheTimeRc.confirmationMessage = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return setTheTimeRc;
};

void SetTheTimeReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), allocator);
        parent.AddMember("timestamp", tempTimestampStringValue, allocator);
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(confirmationMessage.c_str(), confirmationMessage.size(), allocator);
        parent.AddMember("confirmation_message", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for forward_time method request arguments ---
ForwardTimeRequestArguments ForwardTimeRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ForwardTimeRequestArguments forwardTimeArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("adjustment");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempAdjustmentIsoString = itr->value.GetString();
            forwardTimeArgs.adjustment = parseIsoDuration(tempAdjustmentIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return forwardTimeArgs;
};

void ForwardTimeRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempAdjustmentStringValue;
        std::string adjustmentIsoString = durationToIsoString(adjustment);
        tempAdjustmentStringValue.SetString(adjustmentIsoString.c_str(), adjustmentIsoString.size(), allocator);
        parent.AddMember("adjustment", tempAdjustmentStringValue, allocator);
    }
}

// --- (De-)Serialization for forward_time method return type ---
ForwardTimeReturnValues ForwardTimeReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    ForwardTimeReturnValues forwardTimeRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("new_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempNewTimeIsoString = itr->value.GetString();
            forwardTimeRc.newTime = parseIsoTimestamp(tempNewTimeIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return forwardTimeRc;
};

void ForwardTimeReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempNewTimeStringValue;
        std::string newTimeIsoString = timePointToIsoString(newTime);
        tempNewTimeStringValue.SetString(newTimeIsoString.c_str(), newTimeIsoString.size(), allocator);
        parent.AddMember("new_time", tempNewTimeStringValue, allocator);
    }
}

// --- (De-)Serialization for how_off_is_the_clock method request arguments ---
HowOffIsTheClockRequestArguments HowOffIsTheClockRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    HowOffIsTheClockRequestArguments howOffIsTheClockArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("actual_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempActualTimeIsoString = itr->value.GetString();
            howOffIsTheClockArgs.actualTime = parseIsoTimestamp(tempActualTimeIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return howOffIsTheClockArgs;
};

void HowOffIsTheClockRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempActualTimeStringValue;
        std::string actualTimeIsoString = timePointToIsoString(actualTime);
        tempActualTimeStringValue.SetString(actualTimeIsoString.c_str(), actualTimeIsoString.size(), allocator);
        parent.AddMember("actual_time", tempActualTimeStringValue, allocator);
    }
}

// --- (De-)Serialization for how_off_is_the_clock method return type ---
HowOffIsTheClockReturnValues HowOffIsTheClockReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    HowOffIsTheClockReturnValues howOffIsTheClockRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("difference");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempDifferenceIsoString = itr->value.GetString();
            howOffIsTheClockRc.difference = parseIsoDuration(tempDifferenceIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return howOffIsTheClockRc;
};

void HowOffIsTheClockReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempDifferenceStringValue;
        std::string differenceIsoString = durationToIsoString(difference);
        tempDifferenceStringValue.SetString(differenceIsoString.c_str(), differenceIsoString.size(), allocator);
        parent.AddMember("difference", tempDifferenceStringValue, allocator);
    }
}
