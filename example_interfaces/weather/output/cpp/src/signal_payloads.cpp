
#include "signal_payloads.hpp"

// --- (De-)Serialization for current_time signal payload ---
CurrentTimePayload CurrentTimePayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CurrentTimePayload currentTimePayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("current_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            currentTimePayload.currentTime = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return currentTimePayload;
};

void CurrentTimePayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(currentTime.c_str(), currentTime.size(), allocator);
        parent.AddMember("current_time", tempStringValue, allocator);
    }
}
