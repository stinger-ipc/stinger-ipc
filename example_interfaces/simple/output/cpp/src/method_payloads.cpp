
#include "method_payloads.hpp"

#include <rapidjson/document.h>
#include "conversions.hpp"

// --- (De-)Serialization for trade_numbers method request arguments ---
TradeNumbersRequestArguments TradeNumbersRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    TradeNumbersRequestArguments tradeNumbersArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("your_number");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            tradeNumbersArgs.yourNumber = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'your_number' argument doesn't have required value/type");
        }
    }

    return tradeNumbersArgs;
};

void TradeNumbersRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("your_number", yourNumber, allocator);
}

// --- (De-)Serialization for trade_numbers method return type ---
TradeNumbersReturnValues TradeNumbersReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    TradeNumbersReturnValues tradeNumbersRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("my_number");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            tradeNumbersRc.myNumber = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload for the 'my_number' argument doesn't have required value/type");
        }
    }

    return tradeNumbersRc;
};

void TradeNumbersReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("my_number", myNumber, allocator);
}
