
#include "return_types.hpp"

#include "property_structs.hpp"
#include <rapidjson/document.h>

CallThreeIntegersReturnValues CallThreeIntegersReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeIntegersReturnValues callThreeIntegersRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeIntegersRc.output1 = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeIntegersRc.output2 = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeIntegersRc.output3 = itr->value.GetInt();
        }
        else
        {
            callThreeIntegersRc.output3 = boost::none;
        }
    }

    return callThreeIntegersRc;
};

void CallThreeIntegersReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("output1", output1, allocator);

    parent.AddMember("output2", output2, allocator);

    if (output3)
        parent.AddMember("output3", *output3, allocator);
}

CallThreeStringsReturnValues CallThreeStringsReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeStringsReturnValues callThreeStringsRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callThreeStringsRc.output1 = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callThreeStringsRc.output2 = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callThreeStringsRc.output3 = itr->value.GetString();
        }
        else
        {
            callThreeStringsRc.output3 = boost::none;
        }
    }

    return callThreeStringsRc;
};

void CallThreeStringsReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(output1.c_str(), output1.size(), allocator);
        parent.AddMember("output1", tempStringValue, allocator);
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(output2.c_str(), output2.size(), allocator);
        parent.AddMember("output2", tempStringValue, allocator);
    }

    if (output3)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(output3->c_str(), output3->size(), allocator);
        parent.AddMember("output3", tempStringValue, allocator);
    }
}

CallThreeEnumsReturnValues CallThreeEnumsReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeEnumsReturnValues callThreeEnumsRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeEnumsRc.output1 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeEnumsRc.output2 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeEnumsRc.output3 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            callThreeEnumsRc.output3 = boost::none;
        }
    }

    return callThreeEnumsRc;
};

void CallThreeEnumsReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("output1", static_cast<int>(output1), allocator);

    parent.AddMember("output2", static_cast<int>(output2), allocator);

    parent.AddMember("output3", static_cast<int>(*output3), allocator);
}

CallThreeStructsReturnValues CallThreeStructsReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeStructsReturnValues callThreeStructsRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callThreeStructsRc.output1 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callThreeStructsRc.output2 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callThreeStructsRc.output3 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            callThreeStructsRc.output3 = boost::none;
        }
    }

    return callThreeStructsRc;
};

void CallThreeStructsReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

CallThreeDateTimesReturnValues CallThreeDateTimesReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeDateTimesReturnValues callThreeDateTimesRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            callThreeDateTimesRc.output3 = boost::none;
        }
    }

    return callThreeDateTimesRc;
};

void CallThreeDateTimesReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1IsoString = timePointToIsoString(output1);
        tempOutput1StringValue.SetString(output1IsoString.c_str(), output1IsoString.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempOutput2StringValue;
        std::string output2IsoString = timePointToIsoString(output2);
        tempOutput2StringValue.SetString(output2IsoString.c_str(), output2IsoString.size(), allocator);
        parent.AddMember("output2", tempOutput2StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempOutput3StringValue;
        std::string output3IsoString = timePointToIsoString(*output3);
        tempOutput3StringValue.SetString(output3IsoString.c_str(), output3IsoString.size(), allocator);
        parent.AddMember("output3", tempOutput3StringValue, allocator);
    }
}

CallThreeDurationsReturnValues CallThreeDurationsReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeDurationsReturnValues callThreeDurationsRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            callThreeDurationsRc.output3 = boost::none;
        }
    }

    return callThreeDurationsRc;
};

void CallThreeDurationsReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1IsoString = durationToIsoString(output1);
        tempOutput1StringValue.SetString(output1IsoString.c_str(), output1IsoString.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempOutput2StringValue;
        std::string output2IsoString = durationToIsoString(output2);
        tempOutput2StringValue.SetString(output2IsoString.c_str(), output2IsoString.size(), allocator);
        parent.AddMember("output2", tempOutput2StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempOutput3StringValue;
        std::string output3IsoString = durationToIsoString(*output3);
        tempOutput3StringValue.SetString(output3IsoString.c_str(), output3IsoString.size(), allocator);
        parent.AddMember("output3", tempOutput3StringValue, allocator);
    }
}

CallThreeBinariesReturnValues CallThreeBinariesReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeBinariesReturnValues callThreeBinariesRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
        }
        else
        {
            callThreeBinariesRc.output3 = boost::none;
        }
    }

    return callThreeBinariesRc;
};

void CallThreeBinariesReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1B64String = base64Encode(output1);
        tempOutput1StringValue.SetString(output1B64String.c_str(), output1B64String.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempOutput2StringValue;
        std::string output2B64String = base64Encode(output2);
        tempOutput2StringValue.SetString(output2B64String.c_str(), output2B64String.size(), allocator);
        parent.AddMember("output2", tempOutput2StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempOutput3StringValue;
        std::string output3B64String = base64Encode(*output3);
        tempOutput3StringValue.SetString(output3B64String.c_str(), output3B64String.size(), allocator);
        parent.AddMember("output3", tempOutput3StringValue, allocator);
    }
}
