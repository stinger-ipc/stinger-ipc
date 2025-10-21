
#include "signal_payloads.hpp"

// --- (De-)Serialization for anotherSignal signal payload ---
AnotherSignalPayload AnotherSignalPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    AnotherSignalPayload anotherSignalPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("one");
        if (itr != jsonObj.MemberEnd() && itr->value.IsDouble())
        {
            anotherSignalPayload.one = itr->value.GetDouble();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'one' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("two");
        if (itr != jsonObj.MemberEnd() && itr->value.IsBool())
        {
            anotherSignalPayload.two = itr->value.GetBool();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'two' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("three");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            anotherSignalPayload.three = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'three' argument doesn't have required value/type");
        }
    }

    return anotherSignalPayload;
};

void AnotherSignalPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("one", one, allocator);

    parent.AddMember("two", two, allocator);

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(three.c_str(), three.size(), allocator);
        parent.AddMember("three", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for bark signal payload ---
BarkPayload BarkPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    BarkPayload barkPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("word");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            barkPayload.word = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'word' argument doesn't have required value/type");
        }
    }

    return barkPayload;
};

void BarkPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(word.c_str(), word.size(), allocator);
        parent.AddMember("word", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for maybe_number signal payload ---
MaybeNumberPayload MaybeNumberPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    MaybeNumberPayload maybeNumberPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("number");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            maybeNumberPayload.number = itr->value.GetInt();
        }
        else
        {
            maybeNumberPayload.number = boost::none;
        }
    }

    return maybeNumberPayload;
};

void MaybeNumberPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (number)
        parent.AddMember("number", *number, allocator);
}

// --- (De-)Serialization for maybe_name signal payload ---
MaybeNamePayload MaybeNamePayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    MaybeNamePayload maybeNamePayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("name");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            maybeNamePayload.name = itr->value.GetString();
        }
        else
        {
            maybeNamePayload.name = boost::none;
        }
    }

    return maybeNamePayload;
};

void MaybeNamePayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (name)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(name->c_str(), name->size(), allocator);
        parent.AddMember("name", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for now signal payload ---
NowPayload NowPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    NowPayload nowPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("timestamp");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTimestampIsoString = itr->value.GetString();
            nowPayload.timestamp = parseIsoTimestamp(tempTimestampIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'timestamp' argument doesn't have required value/type");
        }
    }

    return nowPayload;
};

void NowPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), allocator);
        parent.AddMember("timestamp", tempTimestampStringValue, allocator);
    }
}
