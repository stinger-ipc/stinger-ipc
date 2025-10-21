
#include "signal_payloads.hpp"

// --- (De-)Serialization for todayIs signal payload ---
TodayIsPayload TodayIsPayload::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    TodayIsPayload todayIsPayload;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("dayOfMonth");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            todayIsPayload.dayOfMonth = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'dayOfMonth' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("dayOfWeek");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            todayIsPayload.dayOfWeek = static_cast<DayOfTheWeek>(itr->value.GetInt());
        }
        else
        {
            todayIsPayload.dayOfWeek = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("timestamp");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempTimestampIsoString = itr->value.GetString();
            todayIsPayload.timestamp = parseIsoTimestamp(tempTimestampIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'timestamp' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("process_time");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempProcessTimeIsoString = itr->value.GetString();
            todayIsPayload.processTime = parseIsoDuration(tempProcessTimeIsoString);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'process_time' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("memory_segment");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempMemorySegmentB64String = itr->value.GetString();
            todayIsPayload.memorySegment = base64Decode(tempMemorySegmentB64String);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'memory_segment' argument doesn't have required value/type");
        }
    }

    return todayIsPayload;
};

void TodayIsPayload::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("dayOfMonth", dayOfMonth, allocator);

    parent.AddMember("dayOfWeek", static_cast<int>(*dayOfWeek), allocator);

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempTimestampStringValue;
        std::string timestampIsoString = timePointToIsoString(timestamp);
        tempTimestampStringValue.SetString(timestampIsoString.c_str(), timestampIsoString.size(), allocator);
        parent.AddMember("timestamp", tempTimestampStringValue, allocator);
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempProcessTimeStringValue;
        std::string processTimeIsoString = durationToIsoString(processTime);
        tempProcessTimeStringValue.SetString(processTimeIsoString.c_str(), processTimeIsoString.size(), allocator);
        parent.AddMember("process_time", tempProcessTimeStringValue, allocator);
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempMemorySegmentStringValue;
        std::string memorySegmentB64String = base64Encode(memorySegment);
        tempMemorySegmentStringValue.SetString(memorySegmentB64String.c_str(), memorySegmentB64String.size(), allocator);
        parent.AddMember("memory_segment", tempMemorySegmentStringValue, allocator);
    }
}
