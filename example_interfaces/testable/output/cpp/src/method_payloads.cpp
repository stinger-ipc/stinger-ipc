
#include "method_payloads.hpp"

#include <rapidjson/document.h>
#include "conversions.hpp"

// --- (De-)Serialization for callWithNothing method request arguments ---
CallWithNothingRequestArguments CallWithNothingRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallWithNothingRequestArguments callWithNothingArgs;

    return callWithNothingArgs;
};

void CallWithNothingRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for callWithNothing method return type ---
CallWithNothingReturnValues CallWithNothingReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallWithNothingReturnValues callWithNothingRc;

    return callWithNothingRc;
};

void CallWithNothingReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
}

// --- (De-)Serialization for callOneInteger method request arguments ---
CallOneIntegerRequestArguments CallOneIntegerRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneIntegerRequestArguments callOneIntegerArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callOneIntegerArgs.input1 = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneIntegerArgs;
};

void CallOneIntegerRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("input1", input1, allocator);
}

// --- (De-)Serialization for callOneInteger method return type ---
CallOneIntegerReturnValues CallOneIntegerReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneIntegerReturnValues callOneIntegerRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callOneIntegerRc.output1 = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneIntegerRc;
};

void CallOneIntegerReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("output1", output1, allocator);
}

// --- (De-)Serialization for callOptionalInteger method request arguments ---
CallOptionalIntegerRequestArguments CallOptionalIntegerRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalIntegerRequestArguments callOptionalIntegerArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callOptionalIntegerArgs.input1 = itr->value.GetInt();
        }
        else
        {
            callOptionalIntegerArgs.input1 = boost::none;
        }
    }

    return callOptionalIntegerArgs;
};

void CallOptionalIntegerRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (input1)
        parent.AddMember("input1", *input1, allocator);
}

// --- (De-)Serialization for callOptionalInteger method return type ---
CallOptionalIntegerReturnValues CallOptionalIntegerReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalIntegerReturnValues callOptionalIntegerRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callOptionalIntegerRc.output1 = itr->value.GetInt();
        }
        else
        {
            callOptionalIntegerRc.output1 = boost::none;
        }
    }

    return callOptionalIntegerRc;
};

void CallOptionalIntegerReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (output1)
        parent.AddMember("output1", *output1, allocator);
}

// --- (De-)Serialization for callThreeIntegers method request arguments ---
CallThreeIntegersRequestArguments CallThreeIntegersRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeIntegersRequestArguments callThreeIntegersArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeIntegersArgs.input1 = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeIntegersArgs.input2 = itr->value.GetInt();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeIntegersArgs.input3 = itr->value.GetInt();
        }
        else
        {
            callThreeIntegersArgs.input3 = boost::none;
        }
    }

    return callThreeIntegersArgs;
};

void CallThreeIntegersRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("input1", input1, allocator);

    parent.AddMember("input2", input2, allocator);

    if (input3)
        parent.AddMember("input3", *input3, allocator);
}

// --- (De-)Serialization for callThreeIntegers method return type ---
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

// --- (De-)Serialization for callOneString method request arguments ---
CallOneStringRequestArguments CallOneStringRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneStringRequestArguments callOneStringArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callOneStringArgs.input1 = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneStringArgs;
};

void CallOneStringRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1.c_str(), input1.size(), allocator);
        parent.AddMember("input1", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for callOneString method return type ---
CallOneStringReturnValues CallOneStringReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneStringReturnValues callOneStringRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callOneStringRc.output1 = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneStringRc;
};

void CallOneStringReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(output1.c_str(), output1.size(), allocator);
        parent.AddMember("output1", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalString method request arguments ---
CallOptionalStringRequestArguments CallOptionalStringRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalStringRequestArguments callOptionalStringArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callOptionalStringArgs.input1 = itr->value.GetString();
        }
        else
        {
            callOptionalStringArgs.input1 = boost::none;
        }
    }

    return callOptionalStringArgs;
};

void CallOptionalStringRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (input1)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1->c_str(), input1->size(), allocator);
        parent.AddMember("input1", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalString method return type ---
CallOptionalStringReturnValues CallOptionalStringReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalStringReturnValues callOptionalStringRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callOptionalStringRc.output1 = itr->value.GetString();
        }
        else
        {
            callOptionalStringRc.output1 = boost::none;
        }
    }

    return callOptionalStringRc;
};

void CallOptionalStringReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    if (output1)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(output1->c_str(), output1->size(), allocator);
        parent.AddMember("output1", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for callThreeStrings method request arguments ---
CallThreeStringsRequestArguments CallThreeStringsRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeStringsRequestArguments callThreeStringsArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callThreeStringsArgs.input1 = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callThreeStringsArgs.input2 = itr->value.GetString();
        }
        else
        {
            callThreeStringsArgs.input2 = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            callThreeStringsArgs.input3 = itr->value.GetString();
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callThreeStringsArgs;
};

void CallThreeStringsRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1.c_str(), input1.size(), allocator);
        parent.AddMember("input1", tempStringValue, allocator);
    }

    if (input2)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input2->c_str(), input2->size(), allocator);
        parent.AddMember("input2", tempStringValue, allocator);
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input3.c_str(), input3.size(), allocator);
        parent.AddMember("input3", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for callThreeStrings method return type ---
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
            callThreeStringsRc.output2 = boost::none;
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
            throw std::runtime_error("Received payload doesn't have required value/type");
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

    if (output2)
    {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(output2->c_str(), output2->size(), allocator);
        parent.AddMember("output2", tempStringValue, allocator);
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(output3.c_str(), output3.size(), allocator);
        parent.AddMember("output3", tempStringValue, allocator);
    }
}

// --- (De-)Serialization for callOneEnum method request arguments ---
CallOneEnumRequestArguments CallOneEnumRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneEnumRequestArguments callOneEnumArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callOneEnumArgs.input1 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneEnumArgs;
};

void CallOneEnumRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("input1", static_cast<int>(input1), allocator);
}

// --- (De-)Serialization for callOneEnum method return type ---
CallOneEnumReturnValues CallOneEnumReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneEnumReturnValues callOneEnumRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callOneEnumRc.output1 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneEnumRc;
};

void CallOneEnumReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("output1", static_cast<int>(output1), allocator);
}

// --- (De-)Serialization for callOptionalEnum method request arguments ---
CallOptionalEnumRequestArguments CallOptionalEnumRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalEnumRequestArguments callOptionalEnumArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callOptionalEnumArgs.input1 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            callOptionalEnumArgs.input1 = boost::none;
        }
    }

    return callOptionalEnumArgs;
};

void CallOptionalEnumRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("input1", static_cast<int>(*input1), allocator);
}

// --- (De-)Serialization for callOptionalEnum method return type ---
CallOptionalEnumReturnValues CallOptionalEnumReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalEnumReturnValues callOptionalEnumRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callOptionalEnumRc.output1 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            callOptionalEnumRc.output1 = boost::none;
        }
    }

    return callOptionalEnumRc;
};

void CallOptionalEnumReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("output1", static_cast<int>(*output1), allocator);
}

// --- (De-)Serialization for callThreeEnums method request arguments ---
CallThreeEnumsRequestArguments CallThreeEnumsRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeEnumsRequestArguments callThreeEnumsArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeEnumsArgs.input1 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeEnumsArgs.input2 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt())
        {
            callThreeEnumsArgs.input3 = static_cast<Numbers>(itr->value.GetInt());
        }
        else
        {
            callThreeEnumsArgs.input3 = boost::none;
        }
    }

    return callThreeEnumsArgs;
};

void CallThreeEnumsRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    parent.AddMember("input1", static_cast<int>(input1), allocator);

    parent.AddMember("input2", static_cast<int>(input2), allocator);

    parent.AddMember("input3", static_cast<int>(*input3), allocator);
}

// --- (De-)Serialization for callThreeEnums method return type ---
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

// --- (De-)Serialization for callOneStruct method request arguments ---
CallOneStructRequestArguments CallOneStructRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneStructRequestArguments callOneStructArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callOneStructArgs.input1 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneStructArgs;
};

void CallOneStructRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input1.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("input1", tempStructValue, allocator);
    }
}

// --- (De-)Serialization for callOneStruct method return type ---
CallOneStructReturnValues CallOneStructReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneStructReturnValues callOneStructRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callOneStructRc.output1 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneStructRc;
};

void CallOneStructReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        output1.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("output1", tempStructValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalStruct method request arguments ---
CallOptionalStructRequestArguments CallOptionalStructRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalStructRequestArguments callOptionalStructArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callOptionalStructArgs.input1 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            callOptionalStructArgs.input1 = boost::none;
        }
    }

    return callOptionalStructArgs;
};

void CallOptionalStructRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempStructValue;
        if (input1)
        {
            tempStructValue.SetObject();
            input1->AddToRapidJsonObject(tempStructValue, allocator);
        }
        else
        {
            tempStructValue.SetNull();
        }
        parent.AddMember("input1", tempStructValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalStruct method return type ---
CallOptionalStructReturnValues CallOptionalStructReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalStructReturnValues callOptionalStructRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callOptionalStructRc.output1 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            callOptionalStructRc.output1 = boost::none;
        }
    }

    return callOptionalStructRc;
};

void CallOptionalStructReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempStructValue;
        if (output1)
        {
            tempStructValue.SetObject();
            output1->AddToRapidJsonObject(tempStructValue, allocator);
        }
        else
        {
            tempStructValue.SetNull();
        }
        parent.AddMember("output1", tempStructValue, allocator);
    }
}

// --- (De-)Serialization for callThreeStructs method request arguments ---
CallThreeStructsRequestArguments CallThreeStructsRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeStructsRequestArguments callThreeStructsArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callThreeStructsArgs.input1 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            callThreeStructsArgs.input1 = boost::none;
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callThreeStructsArgs.input2 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsObject())
        {
            callThreeStructsArgs.input3 = AllTypes::FromRapidJsonObject(itr->value);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callThreeStructsArgs;
};

void CallThreeStructsRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempStructValue;
        if (input1)
        {
            tempStructValue.SetObject();
            input1->AddToRapidJsonObject(tempStructValue, allocator);
        }
        else
        {
            tempStructValue.SetNull();
        }
        parent.AddMember("input1", tempStructValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input2.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("input2", tempStructValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input3.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("input3", tempStructValue, allocator);
    }
}

// --- (De-)Serialization for callThreeStructs method return type ---
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
            callThreeStructsRc.output1 = boost::none;
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
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callThreeStructsRc;
};

void CallThreeStructsReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempStructValue;
        if (output1)
        {
            tempStructValue.SetObject();
            output1->AddToRapidJsonObject(tempStructValue, allocator);
        }
        else
        {
            tempStructValue.SetNull();
        }
        parent.AddMember("output1", tempStructValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        output2.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("output2", tempStructValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        output3.AddToRapidJsonObject(tempStructValue, allocator);

        parent.AddMember("output3", tempStructValue, allocator);
    }
}

// --- (De-)Serialization for callOneDateTime method request arguments ---
CallOneDateTimeRequestArguments CallOneDateTimeRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneDateTimeRequestArguments callOneDateTimeArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1IsoString = itr->value.GetString();
            callOneDateTimeArgs.input1 = parseIsoTimestamp(tempInput1IsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneDateTimeArgs;
};

void CallOneDateTimeRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOneDateTime method return type ---
CallOneDateTimeReturnValues CallOneDateTimeReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneDateTimeReturnValues callOneDateTimeRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1IsoString = itr->value.GetString();
            callOneDateTimeRc.output1 = parseIsoTimestamp(tempOutput1IsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneDateTimeRc;
};

void CallOneDateTimeReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1IsoString = timePointToIsoString(output1);
        tempOutput1StringValue.SetString(output1IsoString.c_str(), output1IsoString.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalDateTime method request arguments ---
CallOptionalDateTimeRequestArguments CallOptionalDateTimeRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalDateTimeRequestArguments callOptionalDateTimeArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1IsoString = itr->value.GetString();
            callOptionalDateTimeArgs.input1 = parseIsoTimestamp(tempInput1IsoString);
        }
        else
        {
            callOptionalDateTimeArgs.input1 = boost::none;
        }
    }

    return callOptionalDateTimeArgs;
};

void CallOptionalDateTimeRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(*input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalDateTime method return type ---
CallOptionalDateTimeReturnValues CallOptionalDateTimeReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalDateTimeReturnValues callOptionalDateTimeRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1IsoString = itr->value.GetString();
            callOptionalDateTimeRc.output1 = parseIsoTimestamp(tempOutput1IsoString);
        }
        else
        {
            callOptionalDateTimeRc.output1 = boost::none;
        }
    }

    return callOptionalDateTimeRc;
};

void CallOptionalDateTimeReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1IsoString = timePointToIsoString(*output1);
        tempOutput1StringValue.SetString(output1IsoString.c_str(), output1IsoString.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callThreeDateTimes method request arguments ---
CallThreeDateTimesRequestArguments CallThreeDateTimesRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeDateTimesRequestArguments callThreeDateTimesArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1IsoString = itr->value.GetString();
            callThreeDateTimesArgs.input1 = parseIsoTimestamp(tempInput1IsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput2IsoString = itr->value.GetString();
            callThreeDateTimesArgs.input2 = parseIsoTimestamp(tempInput2IsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput3IsoString = itr->value.GetString();
            callThreeDateTimesArgs.input3 = parseIsoTimestamp(tempInput3IsoString);
        }
        else
        {
            callThreeDateTimesArgs.input3 = boost::none;
        }
    }

    return callThreeDateTimesArgs;
};

void CallThreeDateTimesRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = timePointToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempInput2StringValue;
        std::string input2IsoString = timePointToIsoString(input2);
        tempInput2StringValue.SetString(input2IsoString.c_str(), input2IsoString.size(), allocator);
        parent.AddMember("input2", tempInput2StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempInput3StringValue;
        std::string input3IsoString = timePointToIsoString(*input3);
        tempInput3StringValue.SetString(input3IsoString.c_str(), input3IsoString.size(), allocator);
        parent.AddMember("input3", tempInput3StringValue, allocator);
    }
}

// --- (De-)Serialization for callThreeDateTimes method return type ---
CallThreeDateTimesReturnValues CallThreeDateTimesReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeDateTimesReturnValues callThreeDateTimesRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1IsoString = itr->value.GetString();
            callThreeDateTimesRc.output1 = parseIsoTimestamp(tempOutput1IsoString);
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
            auto tempOutput2IsoString = itr->value.GetString();
            callThreeDateTimesRc.output2 = parseIsoTimestamp(tempOutput2IsoString);
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
            auto tempOutput3IsoString = itr->value.GetString();
            callThreeDateTimesRc.output3 = parseIsoTimestamp(tempOutput3IsoString);
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

// --- (De-)Serialization for callOneDuration method request arguments ---
CallOneDurationRequestArguments CallOneDurationRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneDurationRequestArguments callOneDurationArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1IsoString = itr->value.GetString();
            callOneDurationArgs.input1 = parseIsoDuration(tempInput1IsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneDurationArgs;
};

void CallOneDurationRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOneDuration method return type ---
CallOneDurationReturnValues CallOneDurationReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneDurationReturnValues callOneDurationRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1IsoString = itr->value.GetString();
            callOneDurationRc.output1 = parseIsoDuration(tempOutput1IsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneDurationRc;
};

void CallOneDurationReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1IsoString = durationToIsoString(output1);
        tempOutput1StringValue.SetString(output1IsoString.c_str(), output1IsoString.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalDuration method request arguments ---
CallOptionalDurationRequestArguments CallOptionalDurationRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalDurationRequestArguments callOptionalDurationArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1IsoString = itr->value.GetString();
            callOptionalDurationArgs.input1 = parseIsoDuration(tempInput1IsoString);
        }
        else
        {
            callOptionalDurationArgs.input1 = boost::none;
        }
    }

    return callOptionalDurationArgs;
};

void CallOptionalDurationRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(*input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalDuration method return type ---
CallOptionalDurationReturnValues CallOptionalDurationReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalDurationReturnValues callOptionalDurationRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1IsoString = itr->value.GetString();
            callOptionalDurationRc.output1 = parseIsoDuration(tempOutput1IsoString);
        }
        else
        {
            callOptionalDurationRc.output1 = boost::none;
        }
    }

    return callOptionalDurationRc;
};

void CallOptionalDurationReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1IsoString = durationToIsoString(*output1);
        tempOutput1StringValue.SetString(output1IsoString.c_str(), output1IsoString.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callThreeDurations method request arguments ---
CallThreeDurationsRequestArguments CallThreeDurationsRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeDurationsRequestArguments callThreeDurationsArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1IsoString = itr->value.GetString();
            callThreeDurationsArgs.input1 = parseIsoDuration(tempInput1IsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput2IsoString = itr->value.GetString();
            callThreeDurationsArgs.input2 = parseIsoDuration(tempInput2IsoString);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput3IsoString = itr->value.GetString();
            callThreeDurationsArgs.input3 = parseIsoDuration(tempInput3IsoString);
        }
        else
        {
            callThreeDurationsArgs.input3 = boost::none;
        }
    }

    return callThreeDurationsArgs;
};

void CallThreeDurationsRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = durationToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempInput2StringValue;
        std::string input2IsoString = durationToIsoString(input2);
        tempInput2StringValue.SetString(input2IsoString.c_str(), input2IsoString.size(), allocator);
        parent.AddMember("input2", tempInput2StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempInput3StringValue;
        std::string input3IsoString = durationToIsoString(*input3);
        tempInput3StringValue.SetString(input3IsoString.c_str(), input3IsoString.size(), allocator);
        parent.AddMember("input3", tempInput3StringValue, allocator);
    }
}

// --- (De-)Serialization for callThreeDurations method return type ---
CallThreeDurationsReturnValues CallThreeDurationsReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeDurationsReturnValues callThreeDurationsRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1IsoString = itr->value.GetString();
            callThreeDurationsRc.output1 = parseIsoDuration(tempOutput1IsoString);
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
            auto tempOutput2IsoString = itr->value.GetString();
            callThreeDurationsRc.output2 = parseIsoDuration(tempOutput2IsoString);
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
            auto tempOutput3IsoString = itr->value.GetString();
            callThreeDurationsRc.output3 = parseIsoDuration(tempOutput3IsoString);
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

// --- (De-)Serialization for callOneBinary method request arguments ---
CallOneBinaryRequestArguments CallOneBinaryRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneBinaryRequestArguments callOneBinaryArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1B64String = itr->value.GetString();
            callOneBinaryArgs.input1 = base64Decode(tempInput1B64String);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneBinaryArgs;
};

void CallOneBinaryRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOneBinary method return type ---
CallOneBinaryReturnValues CallOneBinaryReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOneBinaryReturnValues callOneBinaryRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1B64String = itr->value.GetString();
            callOneBinaryRc.output1 = base64Decode(tempOutput1B64String);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }

    return callOneBinaryRc;
};

void CallOneBinaryReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1B64String = base64Encode(output1);
        tempOutput1StringValue.SetString(output1B64String.c_str(), output1B64String.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalBinary method request arguments ---
CallOptionalBinaryRequestArguments CallOptionalBinaryRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalBinaryRequestArguments callOptionalBinaryArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1B64String = itr->value.GetString();
            callOptionalBinaryArgs.input1 = base64Decode(tempInput1B64String);
        }
        else
        {
            callOptionalBinaryArgs.input1 = boost::none;
        }
    }

    return callOptionalBinaryArgs;
};

void CallOptionalBinaryRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(*input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callOptionalBinary method return type ---
CallOptionalBinaryReturnValues CallOptionalBinaryReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallOptionalBinaryReturnValues callOptionalBinaryRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1B64String = itr->value.GetString();
            callOptionalBinaryRc.output1 = base64Decode(tempOutput1B64String);
        }
        else
        {
            callOptionalBinaryRc.output1 = boost::none;
        }
    }

    return callOptionalBinaryRc;
};

void CallOptionalBinaryReturnValues::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempOutput1StringValue;
        std::string output1B64String = base64Encode(*output1);
        tempOutput1StringValue.SetString(output1B64String.c_str(), output1B64String.size(), allocator);
        parent.AddMember("output1", tempOutput1StringValue, allocator);
    }
}

// --- (De-)Serialization for callThreeBinaries method request arguments ---
CallThreeBinariesRequestArguments CallThreeBinariesRequestArguments::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeBinariesRequestArguments callThreeBinariesArgs;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput1B64String = itr->value.GetString();
            callThreeBinariesArgs.input1 = base64Decode(tempInput1B64String);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input2");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput2B64String = itr->value.GetString();
            callThreeBinariesArgs.input2 = base64Decode(tempInput2B64String);
        }
        else
        {
            throw std::runtime_error("Received payload doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("input3");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempInput3B64String = itr->value.GetString();
            callThreeBinariesArgs.input3 = base64Decode(tempInput3B64String);
        }
        else
        {
            callThreeBinariesArgs.input3 = boost::none;
        }
    }

    return callThreeBinariesArgs;
};

void CallThreeBinariesRequestArguments::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // Restrict Scope
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = base64Encode(input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), allocator);
        parent.AddMember("input1", tempInput1StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempInput2StringValue;
        std::string input2B64String = base64Encode(input2);
        tempInput2StringValue.SetString(input2B64String.c_str(), input2B64String.size(), allocator);
        parent.AddMember("input2", tempInput2StringValue, allocator);
    }

    { // Restrict Scope
        rapidjson::Value tempInput3StringValue;
        std::string input3B64String = base64Encode(*input3);
        tempInput3StringValue.SetString(input3B64String.c_str(), input3B64String.size(), allocator);
        parent.AddMember("input3", tempInput3StringValue, allocator);
    }
}

// --- (De-)Serialization for callThreeBinaries method return type ---
CallThreeBinariesReturnValues CallThreeBinariesReturnValues::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    CallThreeBinariesReturnValues callThreeBinariesRc;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("output1");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString())
        {
            auto tempOutput1B64String = itr->value.GetString();
            callThreeBinariesRc.output1 = base64Decode(tempOutput1B64String);
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
            auto tempOutput2B64String = itr->value.GetString();
            callThreeBinariesRc.output2 = base64Decode(tempOutput2B64String);
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
            auto tempOutput3B64String = itr->value.GetString();
            callThreeBinariesRc.output3 = base64Decode(tempOutput3B64String);
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
