/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the testable interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once
#include <string>
#include <chrono>
#include <vector>
#include <boost/optional.hpp>
#include "enums.hpp"
#include "structs.hpp"

struct CallWithNothingRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallWithNothingRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct CallWithNothingReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallWithNothingReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
};

struct CallOneIntegerRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneIntegerRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int input1;
};

struct CallOneIntegerReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneIntegerReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int output1;
};

struct CallOptionalIntegerRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalIntegerRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<int> input1;
};

struct CallOptionalIntegerReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalIntegerReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<int> output1;
};

struct CallThreeIntegersRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeIntegersRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int input1;
    int input2;
    boost::optional<int> input3;
};

struct CallThreeIntegersReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeIntegersReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    int output1;
    int output2;
    boost::optional<int> output3;
};

struct CallOneStringRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneStringRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string input1;
};

struct CallOneStringReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneStringReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string output1;
};

struct CallOptionalStringRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalStringRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::string> input1;
};

struct CallOptionalStringReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalStringReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::string> output1;
};

struct CallThreeStringsRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeStringsRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string input1;
    boost::optional<std::string> input2;
    std::string input3;
};

struct CallThreeStringsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeStringsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::string output1;
    boost::optional<std::string> output2;
    std::string output3;
};

struct CallOneEnumRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneEnumRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Numbers input1;
};

struct CallOneEnumReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneEnumReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Numbers output1;
};

struct CallOptionalEnumRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalEnumRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<Numbers> input1;
};

struct CallOptionalEnumReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalEnumReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<Numbers> output1;
};

struct CallThreeEnumsRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeEnumsRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Numbers input1;
    Numbers input2;
    boost::optional<Numbers> input3;
};

struct CallThreeEnumsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeEnumsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    Numbers output1;
    Numbers output2;
    boost::optional<Numbers> output3;
};

struct CallOneStructRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneStructRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    AllTypes input1;
};

struct CallOneStructReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneStructReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    AllTypes output1;
};

struct CallOptionalStructRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalStructRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<AllTypes> input1;
};

struct CallOptionalStructReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalStructReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<AllTypes> output1;
};

struct CallThreeStructsRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeStructsRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<AllTypes> input1;
    AllTypes input2;
    AllTypes input3;
};

struct CallThreeStructsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeStructsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<AllTypes> output1;
    AllTypes output2;
    AllTypes output3;
};

struct CallOneDateTimeRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneDateTimeRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> input1;
};

struct CallOneDateTimeReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneDateTimeReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> output1;
};

struct CallOptionalDateTimeRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalDateTimeRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> input1;
};

struct CallOptionalDateTimeReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalDateTimeReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> output1;
};

struct CallThreeDateTimesRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeDateTimesRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> input1;
    std::chrono::time_point<std::chrono::system_clock> input2;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> input3;
};

struct CallThreeDateTimesReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeDateTimesReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::time_point<std::chrono::system_clock> output1;
    std::chrono::time_point<std::chrono::system_clock> output2;
    boost::optional<std::chrono::time_point<std::chrono::system_clock>> output3;
};

struct CallOneDurationRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneDurationRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> input1;
};

struct CallOneDurationReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneDurationReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> output1;
};

struct CallOptionalDurationRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalDurationRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::chrono::duration<double>> input1;
};

struct CallOptionalDurationReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalDurationReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::chrono::duration<double>> output1;
};

struct CallThreeDurationsRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeDurationsRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> input1;
    std::chrono::duration<double> input2;
    boost::optional<std::chrono::duration<double>> input3;
};

struct CallThreeDurationsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeDurationsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::chrono::duration<double> output1;
    std::chrono::duration<double> output2;
    boost::optional<std::chrono::duration<double>> output3;
};

struct CallOneBinaryRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneBinaryRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<uint8_t> input1;
};

struct CallOneBinaryReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneBinaryReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<uint8_t> output1;
};

struct CallOptionalBinaryRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalBinaryRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::vector<uint8_t>> input1;
};

struct CallOptionalBinaryReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalBinaryReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::vector<uint8_t>> output1;
};

struct CallThreeBinariesRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeBinariesRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<uint8_t> input1;
    std::vector<uint8_t> input2;
    boost::optional<std::vector<uint8_t>> input3;
};

struct CallThreeBinariesReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallThreeBinariesReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<uint8_t> output1;
    std::vector<uint8_t> output2;
    boost::optional<std::vector<uint8_t>> output3;
};

struct CallOneListOfIntegersRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneListOfIntegersRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<int> input1;
};

struct CallOneListOfIntegersReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOneListOfIntegersReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<int> output1;
};

struct CallOptionalListOfFloatsRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalListOfFloatsRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::vector<double>> input1;
};

struct CallOptionalListOfFloatsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallOptionalListOfFloatsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    boost::optional<std::vector<double>> output1;
};

struct CallTwoListsRequestArguments
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallTwoListsRequestArguments FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<Numbers> input1;
    boost::optional<std::vector<std::string>> input2;
};

struct CallTwoListsReturnValues
{
    void AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const;
    static CallTwoListsReturnValues FromRapidJsonObject(const rapidjson::Value& jsonObj);
    // Values...
    std::vector<Numbers> output1;
    boost::optional<std::vector<std::string>> output2;
};