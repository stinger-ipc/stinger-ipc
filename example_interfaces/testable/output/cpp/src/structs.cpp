

#include "structs.hpp"

Entry Entry::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    Entry entry;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("key");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            entry.key = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'key' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("value");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            entry.value = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    return entry;
};

void Entry::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("key", key, allocator);

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value.c_str(), value.size(), allocator);
        parent.AddMember("value", tempStringValue, allocator);
    }
}

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
            throw std::runtime_error("Received payload for the 'the_bool' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'the_int' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'the_number' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'the_str' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'the_enum' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("an_entry_object");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            allTypes.anEntryObject = Entry::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload for the 'an_entry_object' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'date_and_time' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'time_duration' argument doesn't have required value/type");
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
            throw std::runtime_error("Received payload for the 'data' argument doesn't have required value/type");
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
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("optionalEntryObject");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            allTypes.optionalEntryObject = Entry::FromRapidJsonObject(itr->value);
        }
        else
        {
            allTypes.optionalEntryObject = boost::none;
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
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("array_of_integers");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<int> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsInt())
                    {
                        tempArray.push_back(item.GetInt());
                    }
                }
                allTypes.arrayOfIntegers = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'array_of_integers' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("optional_array_of_integers");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<int> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsInt())
                    {
                        tempArray.push_back(item.GetInt());
                    }
                }
                allTypes.optionalArrayOfIntegers = std::move(tempArray);
            }
        }
        else
        {
            allTypes.optionalArrayOfIntegers = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("array_of_strings");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::string> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        tempArray.push_back(item.GetString());
                    }
                }
                allTypes.arrayOfStrings = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'array_of_strings' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("optional_array_of_strings");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::string> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        tempArray.push_back(item.GetString());
                    }
                }
                allTypes.optionalArrayOfStrings = std::move(tempArray);
            }
        }
        else
        {
            allTypes.optionalArrayOfStrings = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("array_of_enums");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<Numbers> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsInt())
                    {
                        tempArray.push_back(static_cast<Numbers>(item.GetInt()));
                    }
                }
                allTypes.arrayOfEnums = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'array_of_enums' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("optional_array_of_enums");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<Numbers> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsInt())
                    {
                        tempArray.push_back(static_cast<Numbers>(item.GetInt()));
                    }
                }
                allTypes.optionalArrayOfEnums = std::move(tempArray);
            }
        }
        else
        {
            allTypes.optionalArrayOfEnums = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("array_of_datetimes");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::chrono::time_point<std::chrono::system_clock>> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        {
                            std::string tempIsoString = item.GetString();
                            tempArray.push_back(parseIsoTimestamp(tempIsoString));
                        }
                    }
                }
                allTypes.arrayOfDatetimes = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'array_of_datetimes' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("optional_array_of_datetimes");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::chrono::time_point<std::chrono::system_clock>> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        {
                            std::string tempIsoString = item.GetString();
                            tempArray.push_back(parseIsoTimestamp(tempIsoString));
                        }
                    }
                }
                allTypes.optionalArrayOfDatetimes = std::move(tempArray);
            }
        }
        else
        {
            allTypes.optionalArrayOfDatetimes = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("array_of_durations");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::chrono::duration<double>> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        {
                            std::string tempIsoString = item.GetString();
                            tempArray.push_back(parseIsoDuration(tempIsoString));
                        }
                    }
                }
                allTypes.arrayOfDurations = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'array_of_durations' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("optional_array_of_durations");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::chrono::duration<double>> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        {
                            std::string tempIsoString = item.GetString();
                            tempArray.push_back(parseIsoDuration(tempIsoString));
                        }
                    }
                }
                allTypes.optionalArrayOfDurations = std::move(tempArray);
            }
        }
        else
        {
            allTypes.optionalArrayOfDurations = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("array_of_binaries");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::vector<uint8_t>> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        {
                            std::string tempB64String = item.GetString();
                            tempArray.push_back(base64Decode(tempB64String));
                        }
                    }
                }
                allTypes.arrayOfBinaries = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'array_of_binaries' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("optional_array_of_binaries");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<std::vector<uint8_t>> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsString())
                    {
                        {
                            std::string tempB64String = item.GetString();
                            tempArray.push_back(base64Decode(tempB64String));
                        }
                    }
                }
                allTypes.optionalArrayOfBinaries = std::move(tempArray);
            }
        }
        else
        {
            allTypes.optionalArrayOfBinaries = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("array_of_entry_objects");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<Entry> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsObject())
                    {
                        tempArray.push_back(Entry::FromRapidJsonObject(item));
                    }
                }
                allTypes.arrayOfEntryObjects = std::move(tempArray);
            }
        }
        else
        {
            throw std::runtime_error("Received payload for the 'array_of_entry_objects' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("optional_array_of_entry_objects");
        if (itr != jsonObj.MemberEnd() && itr->value.IsArray())
        {
            {
                std::vector<Entry> tempArray;
                for (const auto& item: itr->value.GetArray())
                {
                    if (item.IsObject())
                    {
                        tempArray.push_back(Entry::FromRapidJsonObject(item));
                    }
                }
                allTypes.optionalArrayOfEntryObjects = std::move(tempArray);
            }
        }
        else
        {
            allTypes.optionalArrayOfEntryObjects = boost::none;
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

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        anEntryObject.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("an_entry_object", tempStructValue, allocator);
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempDateAndTimeStringValue;
        std::string dateAndTimeIsoString = timePointToIsoString(dateAndTime);
        tempDateAndTimeStringValue.SetString(dateAndTimeIsoString.c_str(), dateAndTimeIsoString.size(), allocator);
        parent.AddMember("date_and_time", tempDateAndTimeStringValue, allocator);
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempTimeDurationStringValue;
        std::string timeDurationIsoString = durationToIsoString(timeDuration);
        tempTimeDurationStringValue.SetString(timeDurationIsoString.c_str(), timeDurationIsoString.size(), allocator);
        parent.AddMember("time_duration", tempTimeDurationStringValue, allocator);
    }

    { // Restrict Scope for binary base64 encoding
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

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (optionalEntryObject)
        {
            tempStructValue.SetObject();
            optionalEntryObject->AddToRapidJsonObject(tempStructValue, allocator);
        }
        else
        {
            tempStructValue.SetNull();
        }
        parent.AddMember("optionalEntryObject", tempStructValue, allocator);
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempOptionalDateTimeStringValue;
        std::string optionalDateTimeIsoString = timePointToIsoString(*optionalDateTime);
        tempOptionalDateTimeStringValue.SetString(optionalDateTimeIsoString.c_str(), optionalDateTimeIsoString.size(), allocator);
        parent.AddMember("OptionalDateTime", tempOptionalDateTimeStringValue, allocator);
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempOptionalDurationStringValue;
        std::string optionalDurationIsoString = durationToIsoString(*optionalDuration);
        tempOptionalDurationStringValue.SetString(optionalDurationIsoString.c_str(), optionalDurationIsoString.size(), allocator);
        parent.AddMember("OptionalDuration", tempOptionalDurationStringValue, allocator);
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempOptionalBinaryStringValue;
        std::string optionalBinaryB64String = base64Encode(*optionalBinary);
        tempOptionalBinaryStringValue.SetString(optionalBinaryB64String.c_str(), optionalBinaryB64String.size(), allocator);
        parent.AddMember("OptionalBinary", tempOptionalBinaryStringValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: arrayOfIntegers)
        {
            tempArrayValue.PushBack(item, allocator);
        }
        parent.AddMember("array_of_integers", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalArrayOfIntegers)
        {
            tempArrayValue.PushBack(item, allocator);
        }
        parent.AddMember("optional_array_of_integers", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: arrayOfStrings)
        {
            rapidjson::Value tempArrayOfStringsStringValue;
            tempArrayOfStringsStringValue.SetString(item.c_str(), item.size(), allocator);
            tempArrayValue.PushBack(tempArrayOfStringsStringValue, allocator);
        }
        parent.AddMember("array_of_strings", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalArrayOfStrings)
        {
            rapidjson::Value tempOptionalArrayOfStringsStringValue;
            tempOptionalArrayOfStringsStringValue.SetString(item.c_str(), item.size(), allocator);
            tempArrayValue.PushBack(tempOptionalArrayOfStringsStringValue, allocator);
        }
        parent.AddMember("optional_array_of_strings", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: arrayOfEnums)
        {
            tempArrayValue.PushBack(static_cast<int>(item), allocator);
        }
        parent.AddMember("array_of_enums", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalArrayOfEnums)
        {
            tempArrayValue.PushBack(static_cast<int>(item), allocator);
        }
        parent.AddMember("optional_array_of_enums", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: arrayOfDatetimes)
        {
            rapidjson::Value tempArrayOfDatetimesStringValue;
            std::string itemIsoString = timePointToIsoString(item);
            tempArrayOfDatetimesStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), allocator);
            tempArrayValue.PushBack(tempArrayOfDatetimesStringValue, allocator);
        }
        parent.AddMember("array_of_datetimes", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalArrayOfDatetimes)
        {
            rapidjson::Value tempOptionalArrayOfDatetimesStringValue;
            std::string itemIsoString = timePointToIsoString(item);
            tempOptionalArrayOfDatetimesStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), allocator);
            tempArrayValue.PushBack(tempOptionalArrayOfDatetimesStringValue, allocator);
        }
        parent.AddMember("optional_array_of_datetimes", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: arrayOfDurations)
        {
            rapidjson::Value tempArrayOfDurationsStringValue;
            std::string itemIsoString = durationToIsoString(item);
            tempArrayOfDurationsStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), allocator);
            tempArrayValue.PushBack(tempArrayOfDurationsStringValue, allocator);
        }
        parent.AddMember("array_of_durations", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalArrayOfDurations)
        {
            rapidjson::Value tempOptionalArrayOfDurationsStringValue;
            std::string itemIsoString = durationToIsoString(item);
            tempOptionalArrayOfDurationsStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), allocator);
            tempArrayValue.PushBack(tempOptionalArrayOfDurationsStringValue, allocator);
        }
        parent.AddMember("optional_array_of_durations", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: arrayOfBinaries)
        {
            rapidjson::Value tempArrayOfBinariesStringValue;
            std::string itemB64String = base64Encode(item);
            tempArrayOfBinariesStringValue.SetString(itemB64String.c_str(), itemB64String.size(), allocator);
            tempArrayValue.PushBack(tempArrayOfBinariesStringValue, allocator);
        }
        parent.AddMember("array_of_binaries", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalArrayOfBinaries)
        {
            rapidjson::Value tempOptionalArrayOfBinariesStringValue;
            std::string itemB64String = base64Encode(item);
            tempOptionalArrayOfBinariesStringValue.SetString(itemB64String.c_str(), itemB64String.size(), allocator);
            tempArrayValue.PushBack(tempOptionalArrayOfBinariesStringValue, allocator);
        }
        parent.AddMember("optional_array_of_binaries", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: arrayOfEntryObjects)
        {
            rapidjson::Value tempArrayOfEntryObjectsObjectValue;
            tempArrayOfEntryObjectsObjectValue.SetObject();
            item.AddToRapidJsonObject(tempArrayOfEntryObjectsObjectValue, allocator);
            tempArrayValue.PushBack(tempArrayOfEntryObjectsObjectValue, allocator);
        }
        parent.AddMember("array_of_entry_objects", tempArrayValue, allocator);
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalArrayOfEntryObjects)
        {
            rapidjson::Value tempOptionalArrayOfEntryObjectsObjectValue;
            tempOptionalArrayOfEntryObjectsObjectValue.SetObject();
            item.AddToRapidJsonObject(tempOptionalArrayOfEntryObjectsObjectValue, allocator);
            tempArrayValue.PushBack(tempOptionalArrayOfEntryObjectsObjectValue, allocator);
        }
        parent.AddMember("optional_array_of_entry_objects", tempArrayValue, allocator);
    }
}
