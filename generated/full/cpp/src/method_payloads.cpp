
#include "method_payloads.hpp"

#include <rapidjson/document.h>
#include <stinger/utils/conversions.hpp>

namespace stinger {

namespace gen {
namespace full {

// --- (De-)Serialization for addNumbers method request arguments ---
AddNumbersRequestArguments AddNumbersRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    AddNumbersRequestArguments addNumbersArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("first");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            addNumbersArgs.first = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("second");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            addNumbersArgs.second = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'second' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("third");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            addNumbersArgs.third = itr->value.GetInt();

        } else {
            addNumbersArgs.third = std::nullopt;
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
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            addNumbersRc.sum = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'sum' argument doesn't have required value/type");
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
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("task_to_do");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            doSomethingArgs.taskToDo = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'task_to_do' argument doesn't have required value/type");
        }
    }

    return doSomethingArgs;
};

void DoSomethingRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(taskToDo.c_str(), taskToDo.size(), allocator);
        parent.AddMember("task_to_do", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for doSomething method return type ---
DoSomethingReturnValues DoSomethingReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    DoSomethingReturnValues doSomethingRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("label");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            doSomethingRc.label = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'label' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("identifier");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            doSomethingRc.identifier = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'identifier' argument doesn't have required value/type");
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
}

// --- (De-)Serialization for what_time_is_it method request arguments ---
WhatTimeIsItRequestArguments WhatTimeIsItRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    WhatTimeIsItRequestArguments whatTimeIsItArgs;

    return whatTimeIsItArgs;
};

void WhatTimeIsItRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for what_time_is_it method return type ---
WhatTimeIsItReturnValues WhatTimeIsItReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    WhatTimeIsItReturnValues whatTimeIsItRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("timestamp");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            auto tempTimestampIsoString = itr->value.GetString();
            whatTimeIsItRc.timestamp = stinger::utils::parseIsoTimestamp(tempTimestampIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'timestamp' argument doesn't have required value/type");
        }
    }

    return whatTimeIsItRc;
};

void WhatTimeIsItReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = stinger::utils::timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), allocator);
        parent.AddMember("timestamp", tempTimestampStringValue, allocator);
    }
}

// --- (De-)Serialization for hold_temperature method request arguments ---
HoldTemperatureRequestArguments HoldTemperatureRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    HoldTemperatureRequestArguments holdTemperatureArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("temperature_celsius");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble()) {
            holdTemperatureArgs.temperatureCelsius = itr->value.GetDouble();

        } else {
            throw std::runtime_error("Received payload for the 'temperature_celsius' argument doesn't have required value/type");
        }
    }

    return holdTemperatureArgs;
};

void HoldTemperatureRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("temperature_celsius", temperatureCelsius, allocator);
}

// --- (De-)Serialization for hold_temperature method return type ---
HoldTemperatureReturnValues HoldTemperatureReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    HoldTemperatureReturnValues holdTemperatureRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("success");
        if (itr != jsonObj.MemberEnd() && itr->value.IsBool()) {
            holdTemperatureRc.success = itr->value.GetBool();

        } else {
            throw std::runtime_error("Received payload for the 'success' argument doesn't have required value/type");
        }
    }

    return holdTemperatureRc;
};

void HoldTemperatureReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("success", success, allocator);
}

} // namespace full

} // namespace gen

} // namespace stinger
