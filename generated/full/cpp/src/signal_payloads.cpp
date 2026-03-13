
#include "signal_payloads.hpp"

namespace stinger {

namespace gen {
namespace full {

// --- (De-)Serialization for todayIs signal payload ---
TodayIsPayload TodayIsPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    TodayIsPayload todayIsPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("dayOfMonth");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            todayIsPayload.dayOfMonth = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'dayOfMonth' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("dayOfWeek");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            todayIsPayload.dayOfWeek = static_cast<DayOfTheWeek>(itr->value.GetInt());

        } else {
            throw std::runtime_error("Received payload for the 'dayOfWeek' argument doesn't have required value/type");
        }
    }

    return todayIsPayload;
};

void TodayIsPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("dayOfMonth", dayOfMonth, allocator);

    parent.AddMember("dayOfWeek", static_cast<int>(dayOfWeek), allocator);
}

// --- (De-)Serialization for randomWord signal payload ---
RandomWordPayload RandomWordPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    RandomWordPayload randomWordPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("word");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            randomWordPayload.word = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'word' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            auto tempTimeIsoString = itr->value.GetString();
            randomWordPayload.time = stinger::utils::parseIsoTimestamp(tempTimeIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'time' argument doesn't have required value/type");
        }
    }

    return randomWordPayload;
};

void RandomWordPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(word.c_str(), word.size(), allocator);
        parent.AddMember("word", tempStringValue, allocator);
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTimeStringValue;
        std::string timeIsoString = stinger::utils::timePointToIsoString(time);
        tempTimeStringValue.SetString(timeIsoString.c_str(), timeIsoString.size(), allocator);
        parent.AddMember("time", tempTimeStringValue, allocator);
    }
}

} // namespace full

} // namespace gen

} // namespace stinger
