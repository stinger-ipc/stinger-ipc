

#include <vector>
#include <iostream>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <syslog.h>
#include <sstream>
#include <stinger/utils/iconnection.hpp>
#include <stinger/utils/uuid.hpp>
#include <stinger/utils/format.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "client.hpp"
#include "enums.hpp"
#include "discovery.hpp"

namespace stinger {

namespace gen {
namespace testable {

constexpr const char TestableClient::NAME[];
constexpr const char TestableClient::INTERFACE_VERSION[];

TestableClient::TestableClient(std::shared_ptr<stinger::utils::IConnection> broker, const InstanceInfo& instanceInfo):
    _broker(broker), _instanceId(instanceInfo.serviceId.value_or("error_service_id_not_found")), _instanceInfo(instanceInfo)
{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](const stinger::mqtt::Message& msg)
                                                               {
                                                                   _receiveMessage(msg);
                                                               });

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto emptyTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/empty", topicParams);
    _emptySignalSubscriptionId = _broker->Subscribe(emptyTopic, 2);
    auto singleIntTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleInt", topicParams);
    _singleIntSignalSubscriptionId = _broker->Subscribe(singleIntTopic, 2);
    auto singleOptionalIntTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalInt", topicParams);
    _singleOptionalIntSignalSubscriptionId = _broker->Subscribe(singleOptionalIntTopic, 2);
    auto threeIntegersTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeIntegers", topicParams);
    _threeIntegersSignalSubscriptionId = _broker->Subscribe(threeIntegersTopic, 2);
    auto singleStringTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleString", topicParams);
    _singleStringSignalSubscriptionId = _broker->Subscribe(singleStringTopic, 2);
    auto singleOptionalStringTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalString", topicParams);
    _singleOptionalStringSignalSubscriptionId = _broker->Subscribe(singleOptionalStringTopic, 2);
    auto threeStringsTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeStrings", topicParams);
    _threeStringsSignalSubscriptionId = _broker->Subscribe(threeStringsTopic, 2);
    auto singleEnumTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleEnum", topicParams);
    _singleEnumSignalSubscriptionId = _broker->Subscribe(singleEnumTopic, 2);
    auto singleOptionalEnumTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalEnum", topicParams);
    _singleOptionalEnumSignalSubscriptionId = _broker->Subscribe(singleOptionalEnumTopic, 2);
    auto threeEnumsTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeEnums", topicParams);
    _threeEnumsSignalSubscriptionId = _broker->Subscribe(threeEnumsTopic, 2);
    auto singleStructTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleStruct", topicParams);
    _singleStructSignalSubscriptionId = _broker->Subscribe(singleStructTopic, 2);
    auto singleOptionalStructTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalStruct", topicParams);
    _singleOptionalStructSignalSubscriptionId = _broker->Subscribe(singleOptionalStructTopic, 2);
    auto threeStructsTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeStructs", topicParams);
    _threeStructsSignalSubscriptionId = _broker->Subscribe(threeStructsTopic, 2);
    auto singleDateTimeTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleDateTime", topicParams);
    _singleDateTimeSignalSubscriptionId = _broker->Subscribe(singleDateTimeTopic, 2);
    auto singleOptionalDatetimeTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalDatetime", topicParams);
    _singleOptionalDatetimeSignalSubscriptionId = _broker->Subscribe(singleOptionalDatetimeTopic, 2);
    auto threeDateTimesTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeDateTimes", topicParams);
    _threeDateTimesSignalSubscriptionId = _broker->Subscribe(threeDateTimesTopic, 2);
    auto singleDurationTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleDuration", topicParams);
    _singleDurationSignalSubscriptionId = _broker->Subscribe(singleDurationTopic, 2);
    auto singleOptionalDurationTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalDuration", topicParams);
    _singleOptionalDurationSignalSubscriptionId = _broker->Subscribe(singleOptionalDurationTopic, 2);
    auto threeDurationsTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeDurations", topicParams);
    _threeDurationsSignalSubscriptionId = _broker->Subscribe(threeDurationsTopic, 2);
    auto singleBinaryTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleBinary", topicParams);
    _singleBinarySignalSubscriptionId = _broker->Subscribe(singleBinaryTopic, 2);
    auto singleOptionalBinaryTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalBinary", topicParams);
    _singleOptionalBinarySignalSubscriptionId = _broker->Subscribe(singleOptionalBinaryTopic, 2);
    auto threeBinariesTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeBinaries", topicParams);
    _threeBinariesSignalSubscriptionId = _broker->Subscribe(threeBinariesTopic, 2);
    auto singleArrayOfIntegersTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleArrayOfIntegers", topicParams);
    _singleArrayOfIntegersSignalSubscriptionId = _broker->Subscribe(singleArrayOfIntegersTopic, 2);
    auto singleOptionalArrayOfStringsTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalArrayOfStrings", topicParams);
    _singleOptionalArrayOfStringsSignalSubscriptionId = _broker->Subscribe(singleOptionalArrayOfStringsTopic, 2);
    auto arrayOfEveryTypeTopic = stinger::utils::format("{prefix}/testable/{service_id}/signal/arrayOfEveryType", topicParams);
    _arrayOfEveryTypeSignalSubscriptionId = _broker->Subscribe(arrayOfEveryTypeTopic, 2);
    { // Restrict scope
        auto callWithNothingRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callWithNothing/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callWithNothingRequestTopic, topicParams);
        _callWithNothingMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOneIntegerRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneInteger/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOneIntegerRequestTopic, topicParams);
        _callOneIntegerMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOptionalIntegerRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalInteger/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOptionalIntegerRequestTopic, topicParams);
        _callOptionalIntegerMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callThreeIntegersRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeIntegers/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callThreeIntegersRequestTopic, topicParams);
        _callThreeIntegersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOneStringRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneString/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOneStringRequestTopic, topicParams);
        _callOneStringMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOptionalStringRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalString/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOptionalStringRequestTopic, topicParams);
        _callOptionalStringMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callThreeStringsRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeStrings/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callThreeStringsRequestTopic, topicParams);
        _callThreeStringsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOneEnumRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneEnum/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOneEnumRequestTopic, topicParams);
        _callOneEnumMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOptionalEnumRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalEnum/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOptionalEnumRequestTopic, topicParams);
        _callOptionalEnumMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callThreeEnumsRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeEnums/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callThreeEnumsRequestTopic, topicParams);
        _callThreeEnumsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOneStructRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneStruct/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOneStructRequestTopic, topicParams);
        _callOneStructMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOptionalStructRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalStruct/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOptionalStructRequestTopic, topicParams);
        _callOptionalStructMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callThreeStructsRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeStructs/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callThreeStructsRequestTopic, topicParams);
        _callThreeStructsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOneDateTimeRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneDateTime/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOneDateTimeRequestTopic, topicParams);
        _callOneDateTimeMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOptionalDateTimeRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalDateTime/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOptionalDateTimeRequestTopic, topicParams);
        _callOptionalDateTimeMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callThreeDateTimesRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeDateTimes/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callThreeDateTimesRequestTopic, topicParams);
        _callThreeDateTimesMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOneDurationRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneDuration/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOneDurationRequestTopic, topicParams);
        _callOneDurationMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOptionalDurationRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalDuration/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOptionalDurationRequestTopic, topicParams);
        _callOptionalDurationMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callThreeDurationsRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeDurations/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callThreeDurationsRequestTopic, topicParams);
        _callThreeDurationsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOneBinaryRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneBinary/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOneBinaryRequestTopic, topicParams);
        _callOneBinaryMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOptionalBinaryRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalBinary/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOptionalBinaryRequestTopic, topicParams);
        _callOptionalBinaryMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callThreeBinariesRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeBinaries/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callThreeBinariesRequestTopic, topicParams);
        _callThreeBinariesMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOneListOfIntegersRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneListOfIntegers/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOneListOfIntegersRequestTopic, topicParams);
        _callOneListOfIntegersMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callOptionalListOfFloatsRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalListOfFloats/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callOptionalListOfFloatsRequestTopic, topicParams);
        _callOptionalListOfFloatsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        auto callTwoListsRequestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callTwoLists/request", topicParams);
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << stinger::utils::format(callTwoListsRequestTopic, topicParams);
        _callTwoListsMethodSubscriptionId = _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    auto readWriteIntegerValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_integer/value", topicParams);
    _readWriteIntegerPropertySubscriptionId = _broker->Subscribe(readWriteIntegerValueTopic, 1);
    auto readOnlyIntegerValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_integer/value", topicParams);
    _readOnlyIntegerPropertySubscriptionId = _broker->Subscribe(readOnlyIntegerValueTopic, 1);
    auto readWriteOptionalIntegerValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_integer/value", topicParams);
    _readWriteOptionalIntegerPropertySubscriptionId = _broker->Subscribe(readWriteOptionalIntegerValueTopic, 1);
    auto readWriteTwoIntegersValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_integers/value", topicParams);
    _readWriteTwoIntegersPropertySubscriptionId = _broker->Subscribe(readWriteTwoIntegersValueTopic, 1);
    auto readOnlyStringValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_string/value", topicParams);
    _readOnlyStringPropertySubscriptionId = _broker->Subscribe(readOnlyStringValueTopic, 1);
    auto readWriteStringValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_string/value", topicParams);
    _readWriteStringPropertySubscriptionId = _broker->Subscribe(readWriteStringValueTopic, 1);
    auto readWriteOptionalStringValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_string/value", topicParams);
    _readWriteOptionalStringPropertySubscriptionId = _broker->Subscribe(readWriteOptionalStringValueTopic, 1);
    auto readWriteTwoStringsValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_strings/value", topicParams);
    _readWriteTwoStringsPropertySubscriptionId = _broker->Subscribe(readWriteTwoStringsValueTopic, 1);
    auto readWriteStructValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_struct/value", topicParams);
    _readWriteStructPropertySubscriptionId = _broker->Subscribe(readWriteStructValueTopic, 1);
    auto readWriteOptionalStructValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_struct/value", topicParams);
    _readWriteOptionalStructPropertySubscriptionId = _broker->Subscribe(readWriteOptionalStructValueTopic, 1);
    auto readWriteTwoStructsValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_structs/value", topicParams);
    _readWriteTwoStructsPropertySubscriptionId = _broker->Subscribe(readWriteTwoStructsValueTopic, 1);
    auto readOnlyEnumValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_enum/value", topicParams);
    _readOnlyEnumPropertySubscriptionId = _broker->Subscribe(readOnlyEnumValueTopic, 1);
    auto readWriteEnumValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_enum/value", topicParams);
    _readWriteEnumPropertySubscriptionId = _broker->Subscribe(readWriteEnumValueTopic, 1);
    auto readWriteOptionalEnumValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_enum/value", topicParams);
    _readWriteOptionalEnumPropertySubscriptionId = _broker->Subscribe(readWriteOptionalEnumValueTopic, 1);
    auto readWriteTwoEnumsValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_enums/value", topicParams);
    _readWriteTwoEnumsPropertySubscriptionId = _broker->Subscribe(readWriteTwoEnumsValueTopic, 1);
    auto readWriteDatetimeValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_datetime/value", topicParams);
    _readWriteDatetimePropertySubscriptionId = _broker->Subscribe(readWriteDatetimeValueTopic, 1);
    auto readWriteOptionalDatetimeValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_datetime/value", topicParams);
    _readWriteOptionalDatetimePropertySubscriptionId = _broker->Subscribe(readWriteOptionalDatetimeValueTopic, 1);
    auto readWriteTwoDatetimesValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_datetimes/value", topicParams);
    _readWriteTwoDatetimesPropertySubscriptionId = _broker->Subscribe(readWriteTwoDatetimesValueTopic, 1);
    auto readWriteDurationValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_duration/value", topicParams);
    _readWriteDurationPropertySubscriptionId = _broker->Subscribe(readWriteDurationValueTopic, 1);
    auto readWriteOptionalDurationValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_duration/value", topicParams);
    _readWriteOptionalDurationPropertySubscriptionId = _broker->Subscribe(readWriteOptionalDurationValueTopic, 1);
    auto readWriteTwoDurationsValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_durations/value", topicParams);
    _readWriteTwoDurationsPropertySubscriptionId = _broker->Subscribe(readWriteTwoDurationsValueTopic, 1);
    auto readWriteBinaryValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_binary/value", topicParams);
    _readWriteBinaryPropertySubscriptionId = _broker->Subscribe(readWriteBinaryValueTopic, 1);
    auto readWriteOptionalBinaryValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_binary/value", topicParams);
    _readWriteOptionalBinaryPropertySubscriptionId = _broker->Subscribe(readWriteOptionalBinaryValueTopic, 1);
    auto readWriteTwoBinariesValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_binaries/value", topicParams);
    _readWriteTwoBinariesPropertySubscriptionId = _broker->Subscribe(readWriteTwoBinariesValueTopic, 1);
    auto readWriteListOfStringsValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_list_of_strings/value", topicParams);
    _readWriteListOfStringsPropertySubscriptionId = _broker->Subscribe(readWriteListOfStringsValueTopic, 1);
    auto readWriteListsValueTopic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_lists/value", topicParams);
    _readWriteListsPropertySubscriptionId = _broker->Subscribe(readWriteListsValueTopic, 1);

    auto anyPropertyUpdateResponseTopic = stinger::utils::format("client/{client_id}/testable/property/+/update/response", topicParams);
    _anyPropertyUpdateResponseSubscriptionId = _broker->Subscribe(anyPropertyUpdateResponseTopic, 1);
}

TestableClient::~TestableClient()
{
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void TestableClient::_receiveMessage(const stinger::mqtt::Message& msg)
{
    const int noSubId = -1;
    int subscriptionId = msg.properties.subscriptionId.value_or(noSubId);
    _broker->Log(LOG_DEBUG, "Received message on topic %s with subscription id=%d", msg.topic.c_str(), subscriptionId);
    if (subscriptionId == _emptySignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling empty signal");
        rapidjson::Document doc;
        try {
            if (_emptySignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse empty signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::lock_guard<std::mutex> lock(_emptySignalCallbacksMutex);
                for (const auto& cb: _emptySignalCallbacks) {
                    cb();
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleIntSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleInt signal");
        rapidjson::Document doc;
        try {
            if (_singleIntSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleInt signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                int tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempValue = itr->value.GetInt();

                    } else {
                        throw std::runtime_error("Received payload for 'singleInt' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleIntSignalCallbacksMutex);
                for (const auto& cb: _singleIntSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleOptionalIntSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleOptionalInt signal");
        rapidjson::Document doc;
        try {
            if (_singleOptionalIntSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalInt signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<int> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempValue = itr->value.GetInt();

                    } else {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalIntSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalIntSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _threeIntegersSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling threeIntegers signal");
        rapidjson::Document doc;
        try {
            if (_threeIntegersSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeIntegers signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                int tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempFirst = itr->value.GetInt();

                    } else {
                        throw std::runtime_error("Received payload for 'threeIntegers' doesn't have required value/type");
                    }
                }

                int tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempSecond = itr->value.GetInt();

                    } else {
                        throw std::runtime_error("Received payload for 'threeIntegers' doesn't have required value/type");
                    }
                }

                std::optional<int> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempThird = itr->value.GetInt();

                    } else {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeIntegersSignalCallbacksMutex);
                for (const auto& cb: _threeIntegersSignalCallbacks) {
                    cb(tempFirst, tempSecond, tempThird);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleStringSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleString signal");
        rapidjson::Document doc;
        try {
            if (_singleStringSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleString signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::string tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempValue = itr->value.GetString();

                    } else {
                        throw std::runtime_error("Received payload for 'singleString' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleStringSignalCallbacksMutex);
                for (const auto& cb: _singleStringSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleOptionalStringSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleOptionalString signal");
        rapidjson::Document doc;
        try {
            if (_singleOptionalStringSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalString signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::string> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempValue = itr->value.GetString();

                    } else {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalStringSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalStringSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _threeStringsSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling threeStrings signal");
        rapidjson::Document doc;
        try {
            if (_threeStringsSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeStrings signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::string tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempFirst = itr->value.GetString();

                    } else {
                        throw std::runtime_error("Received payload for 'threeStrings' doesn't have required value/type");
                    }
                }

                std::string tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempSecond = itr->value.GetString();

                    } else {
                        throw std::runtime_error("Received payload for 'threeStrings' doesn't have required value/type");
                    }
                }

                std::optional<std::string> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempThird = itr->value.GetString();

                    } else {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeStringsSignalCallbacksMutex);
                for (const auto& cb: _threeStringsSignalCallbacks) {
                    cb(tempFirst, tempSecond, tempThird);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleEnumSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleEnum signal");
        rapidjson::Document doc;
        try {
            if (_singleEnumSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleEnum signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                Numbers tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempValue = static_cast<Numbers>(itr->value.GetInt());

                    } else {
                        throw std::runtime_error("Received payload for 'singleEnum' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleEnumSignalCallbacksMutex);
                for (const auto& cb: _singleEnumSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleOptionalEnumSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleOptionalEnum signal");
        rapidjson::Document doc;
        try {
            if (_singleOptionalEnumSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalEnum signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<Numbers> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempValue = static_cast<Numbers>(itr->value.GetInt());

                    } else {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalEnumSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalEnumSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _threeEnumsSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling threeEnums signal");
        rapidjson::Document doc;
        try {
            if (_threeEnumsSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeEnums signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                Numbers tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempFirst = static_cast<Numbers>(itr->value.GetInt());

                    } else {
                        throw std::runtime_error("Received payload for 'threeEnums' doesn't have required value/type");
                    }
                }

                Numbers tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempSecond = static_cast<Numbers>(itr->value.GetInt());

                    } else {
                        throw std::runtime_error("Received payload for 'threeEnums' doesn't have required value/type");
                    }
                }

                std::optional<Numbers> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        tempThird = static_cast<Numbers>(itr->value.GetInt());

                    } else {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeEnumsSignalCallbacksMutex);
                for (const auto& cb: _threeEnumsSignalCallbacks) {
                    cb(tempFirst, tempSecond, tempThird);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleStructSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleStruct signal");
        rapidjson::Document doc;
        try {
            if (_singleStructSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleStruct signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                AllTypes tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsObject()) {
                    } else {
                        throw std::runtime_error("Received payload for 'singleStruct' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleStructSignalCallbacksMutex);
                for (const auto& cb: _singleStructSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleOptionalStructSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleOptionalStruct signal");
        rapidjson::Document doc;
        try {
            if (_singleOptionalStructSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalStruct signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<AllTypes> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsObject()) {
                    } else {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalStructSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalStructSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _threeStructsSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling threeStructs signal");
        rapidjson::Document doc;
        try {
            if (_threeStructsSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeStructs signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                AllTypes tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsObject()) {
                    } else {
                        throw std::runtime_error("Received payload for 'threeStructs' doesn't have required value/type");
                    }
                }

                AllTypes tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsObject()) {
                    } else {
                        throw std::runtime_error("Received payload for 'threeStructs' doesn't have required value/type");
                    }
                }

                std::optional<AllTypes> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsObject()) {
                    } else {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeStructsSignalCallbacksMutex);
                for (const auto& cb: _threeStructsSignalCallbacks) {
                    cb(tempFirst, tempSecond, tempThird);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleDateTimeSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleDateTime signal");
        rapidjson::Document doc;
        try {
            if (_singleDateTimeSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleDateTime signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::time_point<std::chrono::system_clock> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail()) {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempValue = std::chrono::system_clock::from_time_t(std::mktime(&tm));

                    } else {
                        throw std::runtime_error("Received payload for 'singleDateTime' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleDateTimeSignalCallbacksMutex);
                for (const auto& cb: _singleDateTimeSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleOptionalDatetimeSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleOptionalDatetime signal");
        rapidjson::Document doc;
        try {
            if (_singleOptionalDatetimeSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalDatetime signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::chrono::time_point<std::chrono::system_clock>> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail()) {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempValue = std::chrono::system_clock::from_time_t(std::mktime(&tm));

                    } else {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalDatetimeSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalDatetimeSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _threeDateTimesSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling threeDateTimes signal");
        rapidjson::Document doc;
        try {
            if (_threeDateTimesSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeDateTimes signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::time_point<std::chrono::system_clock> tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail()) {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempFirst = std::chrono::system_clock::from_time_t(std::mktime(&tm));

                    } else {
                        throw std::runtime_error("Received payload for 'threeDateTimes' doesn't have required value/type");
                    }
                }

                std::chrono::time_point<std::chrono::system_clock> tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail()) {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempSecond = std::chrono::system_clock::from_time_t(std::mktime(&tm));

                    } else {
                        throw std::runtime_error("Received payload for 'threeDateTimes' doesn't have required value/type");
                    }
                }

                std::optional<std::chrono::time_point<std::chrono::system_clock>> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        std::istringstream ss(itr->value.GetString());
                        std::tm tm = {};
                        ss >> std::get_time(&tm, "%Y-%m-%dT%H:%M:%S");
                        if (ss.fail()) {
                            throw std::runtime_error("Failed to parse datetime string");
                        }
                        tempThird = std::chrono::system_clock::from_time_t(std::mktime(&tm));

                    } else {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeDateTimesSignalCallbacksMutex);
                for (const auto& cb: _threeDateTimesSignalCallbacks) {
                    cb(tempFirst, tempSecond, tempThird);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleDurationSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleDuration signal");
        rapidjson::Document doc;
        try {
            if (_singleDurationSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleDuration signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::duration<double> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempValue = stinger::utils::parseIsoDuration(itr->value.GetString());

                    } else {
                        throw std::runtime_error("Received payload for 'singleDuration' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleDurationSignalCallbacksMutex);
                for (const auto& cb: _singleDurationSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleOptionalDurationSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleOptionalDuration signal");
        rapidjson::Document doc;
        try {
            if (_singleOptionalDurationSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalDuration signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::chrono::duration<double>> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempValue = stinger::utils::parseIsoDuration(itr->value.GetString());

                    } else {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalDurationSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalDurationSignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _threeDurationsSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling threeDurations signal");
        rapidjson::Document doc;
        try {
            if (_threeDurationsSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeDurations signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::chrono::duration<double> tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempFirst = stinger::utils::parseIsoDuration(itr->value.GetString());

                    } else {
                        throw std::runtime_error("Received payload for 'threeDurations' doesn't have required value/type");
                    }
                }

                std::chrono::duration<double> tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempSecond = stinger::utils::parseIsoDuration(itr->value.GetString());

                    } else {
                        throw std::runtime_error("Received payload for 'threeDurations' doesn't have required value/type");
                    }
                }

                std::optional<std::chrono::duration<double>> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempThird = stinger::utils::parseIsoDuration(itr->value.GetString());

                    } else {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeDurationsSignalCallbacksMutex);
                for (const auto& cb: _threeDurationsSignalCallbacks) {
                    cb(tempFirst, tempSecond, tempThird);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleBinarySignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleBinary signal");
        rapidjson::Document doc;
        try {
            if (_singleBinarySignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleBinary signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::vector<uint8_t> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempValue = stinger::utils::base64Decode(itr->value.GetString());

                    } else {
                        throw std::runtime_error("Received payload for 'singleBinary' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleBinarySignalCallbacksMutex);
                for (const auto& cb: _singleBinarySignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleOptionalBinarySignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleOptionalBinary signal");
        rapidjson::Document doc;
        try {
            if (_singleOptionalBinarySignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalBinary signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::vector<uint8_t>> tempValue;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempValue = stinger::utils::base64Decode(itr->value.GetString());

                    } else {
                        tempValue = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalBinarySignalCallbacksMutex);
                for (const auto& cb: _singleOptionalBinarySignalCallbacks) {
                    cb(tempValue);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _threeBinariesSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling threeBinaries signal");
        rapidjson::Document doc;
        try {
            if (_threeBinariesSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse threeBinaries signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::vector<uint8_t> tempFirst;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempFirst = stinger::utils::base64Decode(itr->value.GetString());

                    } else {
                        throw std::runtime_error("Received payload for 'threeBinaries' doesn't have required value/type");
                    }
                }

                std::vector<uint8_t> tempSecond;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempSecond = stinger::utils::base64Decode(itr->value.GetString());

                    } else {
                        throw std::runtime_error("Received payload for 'threeBinaries' doesn't have required value/type");
                    }
                }

                std::optional<std::vector<uint8_t>> tempThird;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        tempThird = stinger::utils::base64Decode(itr->value.GetString());

                    } else {
                        tempThird = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_threeBinariesSignalCallbacksMutex);
                for (const auto& cb: _threeBinariesSignalCallbacks) {
                    cb(tempFirst, tempSecond, tempThird);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleArrayOfIntegersSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleArrayOfIntegers signal");
        rapidjson::Document doc;
        try {
            if (_singleArrayOfIntegersSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleArrayOfIntegers signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::vector<int> tempValues;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("values");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'singleArrayOfIntegers' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_singleArrayOfIntegersSignalCallbacksMutex);
                for (const auto& cb: _singleArrayOfIntegersSignalCallbacks) {
                    cb(tempValues);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _singleOptionalArrayOfStringsSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling singleOptionalArrayOfStrings signal");
        rapidjson::Document doc;
        try {
            if (_singleOptionalArrayOfStringsSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse singleOptionalArrayOfStrings signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::optional<std::vector<std::string>> tempValues;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("values");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        tempValues = std::nullopt;
                    }
                }

                std::lock_guard<std::mutex> lock(_singleOptionalArrayOfStringsSignalCallbacksMutex);
                for (const auto& cb: _singleOptionalArrayOfStringsSignalCallbacks) {
                    cb(tempValues);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _arrayOfEveryTypeSignalSubscriptionId) {
        _broker->Log(LOG_INFO, "Handling arrayOfEveryType signal");
        rapidjson::Document doc;
        try {
            if (_arrayOfEveryTypeSignalCallbacks.size() > 0) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    _broker->Log(LOG_WARNING, "Could not JSON parse arrayOfEveryType signal payload.");
                    return;
                }

                if (!doc.IsObject()) {
                    _broker->Log(LOG_WARNING, "Received payload is not an object");
                    return;
                }

                std::vector<int> tempFirstOfIntegers;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first_of_integers");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<double> tempSecondOfFloats;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second_of_floats");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<std::string> tempThirdOfStrings;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third_of_strings");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<Numbers> tempFourthOfEnums;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("fourth_of_enums");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<Entry> tempFifthOfStructs;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("fifth_of_structs");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<std::chrono::time_point<std::chrono::system_clock>> tempSixthOfDatetimes;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("sixth_of_datetimes");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<std::chrono::duration<double>> tempSeventhOfDurations;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("seventh_of_durations");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::vector<std::vector<uint8_t>> tempEighthOfBinaries;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("eighth_of_binaries");
                    if (itr != doc.MemberEnd() && itr->value.IsArray()) {
                    } else {
                        throw std::runtime_error("Received payload for 'arrayOfEveryType' doesn't have required value/type");
                    }
                }

                std::lock_guard<std::mutex> lock(_arrayOfEveryTypeSignalCallbacksMutex);
                for (const auto& cb: _arrayOfEveryTypeSignalCallbacks) {
                    cb(tempFirstOfIntegers, tempSecondOfFloats, tempThirdOfStrings, tempFourthOfEnums, tempFifthOfStructs, tempSixthOfDatetimes, tempSeventhOfDurations, tempEighthOfBinaries);
                }
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }
    if (subscriptionId == _callWithNothingMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callWithNothing response");
        _handleCallWithNothingResponse(msg);
    } else if (subscriptionId == _callOneIntegerMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneInteger response");
        _handleCallOneIntegerResponse(msg);
    } else if (subscriptionId == _callOptionalIntegerMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalInteger response");
        _handleCallOptionalIntegerResponse(msg);
    } else if (subscriptionId == _callThreeIntegersMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeIntegers response");
        _handleCallThreeIntegersResponse(msg);
    } else if (subscriptionId == _callOneStringMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneString response");
        _handleCallOneStringResponse(msg);
    } else if (subscriptionId == _callOptionalStringMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalString response");
        _handleCallOptionalStringResponse(msg);
    } else if (subscriptionId == _callThreeStringsMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeStrings response");
        _handleCallThreeStringsResponse(msg);
    } else if (subscriptionId == _callOneEnumMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneEnum response");
        _handleCallOneEnumResponse(msg);
    } else if (subscriptionId == _callOptionalEnumMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalEnum response");
        _handleCallOptionalEnumResponse(msg);
    } else if (subscriptionId == _callThreeEnumsMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeEnums response");
        _handleCallThreeEnumsResponse(msg);
    } else if (subscriptionId == _callOneStructMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneStruct response");
        _handleCallOneStructResponse(msg);
    } else if (subscriptionId == _callOptionalStructMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalStruct response");
        _handleCallOptionalStructResponse(msg);
    } else if (subscriptionId == _callThreeStructsMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeStructs response");
        _handleCallThreeStructsResponse(msg);
    } else if (subscriptionId == _callOneDateTimeMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneDateTime response");
        _handleCallOneDateTimeResponse(msg);
    } else if (subscriptionId == _callOptionalDateTimeMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalDateTime response");
        _handleCallOptionalDateTimeResponse(msg);
    } else if (subscriptionId == _callThreeDateTimesMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeDateTimes response");
        _handleCallThreeDateTimesResponse(msg);
    } else if (subscriptionId == _callOneDurationMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneDuration response");
        _handleCallOneDurationResponse(msg);
    } else if (subscriptionId == _callOptionalDurationMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalDuration response");
        _handleCallOptionalDurationResponse(msg);
    } else if (subscriptionId == _callThreeDurationsMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeDurations response");
        _handleCallThreeDurationsResponse(msg);
    } else if (subscriptionId == _callOneBinaryMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneBinary response");
        _handleCallOneBinaryResponse(msg);
    } else if (subscriptionId == _callOptionalBinaryMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalBinary response");
        _handleCallOptionalBinaryResponse(msg);
    } else if (subscriptionId == _callThreeBinariesMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callThreeBinaries response");
        _handleCallThreeBinariesResponse(msg);
    } else if (subscriptionId == _callOneListOfIntegersMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOneListOfIntegers response");
        _handleCallOneListOfIntegersResponse(msg);
    } else if (subscriptionId == _callOptionalListOfFloatsMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callOptionalListOfFloats response");
        _handleCallOptionalListOfFloatsResponse(msg);
    } else if (subscriptionId == _callTwoListsMethodSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for callTwoLists response");
        _handleCallTwoListsResponse(msg);
    }
    if (subscriptionId == _readWriteIntegerPropertySubscriptionId) {
        _receiveReadWriteIntegerPropertyUpdate(msg);
    } else if (subscriptionId == _readOnlyIntegerPropertySubscriptionId) {
        _receiveReadOnlyIntegerPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteOptionalIntegerPropertySubscriptionId) {
        _receiveReadWriteOptionalIntegerPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteTwoIntegersPropertySubscriptionId) {
        _receiveReadWriteTwoIntegersPropertyUpdate(msg);
    } else if (subscriptionId == _readOnlyStringPropertySubscriptionId) {
        _receiveReadOnlyStringPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteStringPropertySubscriptionId) {
        _receiveReadWriteStringPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteOptionalStringPropertySubscriptionId) {
        _receiveReadWriteOptionalStringPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteTwoStringsPropertySubscriptionId) {
        _receiveReadWriteTwoStringsPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteStructPropertySubscriptionId) {
        _receiveReadWriteStructPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteOptionalStructPropertySubscriptionId) {
        _receiveReadWriteOptionalStructPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteTwoStructsPropertySubscriptionId) {
        _receiveReadWriteTwoStructsPropertyUpdate(msg);
    } else if (subscriptionId == _readOnlyEnumPropertySubscriptionId) {
        _receiveReadOnlyEnumPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteEnumPropertySubscriptionId) {
        _receiveReadWriteEnumPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteOptionalEnumPropertySubscriptionId) {
        _receiveReadWriteOptionalEnumPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteTwoEnumsPropertySubscriptionId) {
        _receiveReadWriteTwoEnumsPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteDatetimePropertySubscriptionId) {
        _receiveReadWriteDatetimePropertyUpdate(msg);
    } else if (subscriptionId == _readWriteOptionalDatetimePropertySubscriptionId) {
        _receiveReadWriteOptionalDatetimePropertyUpdate(msg);
    } else if (subscriptionId == _readWriteTwoDatetimesPropertySubscriptionId) {
        _receiveReadWriteTwoDatetimesPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteDurationPropertySubscriptionId) {
        _receiveReadWriteDurationPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteOptionalDurationPropertySubscriptionId) {
        _receiveReadWriteOptionalDurationPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteTwoDurationsPropertySubscriptionId) {
        _receiveReadWriteTwoDurationsPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteBinaryPropertySubscriptionId) {
        _receiveReadWriteBinaryPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteOptionalBinaryPropertySubscriptionId) {
        _receiveReadWriteOptionalBinaryPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteTwoBinariesPropertySubscriptionId) {
        _receiveReadWriteTwoBinariesPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteListOfStringsPropertySubscriptionId) {
        _receiveReadWriteListOfStringsPropertyUpdate(msg);
    } else if (subscriptionId == _readWriteListsPropertySubscriptionId) {
        _receiveReadWriteListsPropertyUpdate(msg);
    } else if (subscriptionId == _anyPropertyUpdateResponseSubscriptionId) {
        _broker->Log(LOG_DEBUG, "Matched topic for any property update response");
    }
}

void TestableClient::registerEmptyCallback(const std::function<void()>& cb)
{
    std::lock_guard<std::mutex> lock(_emptySignalCallbacksMutex);
    _emptySignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleIntCallback(const std::function<void(int)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleIntSignalCallbacksMutex);
    _singleIntSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalIntCallback(const std::function<void(std::optional<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalIntSignalCallbacksMutex);
    _singleOptionalIntSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeIntegersCallback(const std::function<void(int, int, std::optional<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeIntegersSignalCallbacksMutex);
    _threeIntegersSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleStringCallback(const std::function<void(std::string)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleStringSignalCallbacksMutex);
    _singleStringSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalStringCallback(const std::function<void(std::optional<std::string>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalStringSignalCallbacksMutex);
    _singleOptionalStringSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeStringsCallback(const std::function<void(std::string, std::string, std::optional<std::string>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeStringsSignalCallbacksMutex);
    _threeStringsSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleEnumCallback(const std::function<void(Numbers)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleEnumSignalCallbacksMutex);
    _singleEnumSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalEnumCallback(const std::function<void(std::optional<Numbers>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalEnumSignalCallbacksMutex);
    _singleOptionalEnumSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeEnumsCallback(const std::function<void(Numbers, Numbers, std::optional<Numbers>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeEnumsSignalCallbacksMutex);
    _threeEnumsSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleStructCallback(const std::function<void(AllTypes)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleStructSignalCallbacksMutex);
    _singleStructSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalStructCallback(const std::function<void(std::optional<AllTypes>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalStructSignalCallbacksMutex);
    _singleOptionalStructSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeStructsCallback(const std::function<void(AllTypes, AllTypes, std::optional<AllTypes>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeStructsSignalCallbacksMutex);
    _threeStructsSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleDateTimeCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleDateTimeSignalCallbacksMutex);
    _singleDateTimeSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalDatetimeCallback(const std::function<void(std::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalDatetimeSignalCallbacksMutex);
    _singleOptionalDatetimeSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeDateTimesCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeDateTimesSignalCallbacksMutex);
    _threeDateTimesSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleDurationCallback(const std::function<void(std::chrono::duration<double>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleDurationSignalCallbacksMutex);
    _singleDurationSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalDurationCallback(const std::function<void(std::optional<std::chrono::duration<double>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalDurationSignalCallbacksMutex);
    _singleOptionalDurationSignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeDurationsCallback(const std::function<void(std::chrono::duration<double>, std::chrono::duration<double>, std::optional<std::chrono::duration<double>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeDurationsSignalCallbacksMutex);
    _threeDurationsSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleBinaryCallback(const std::function<void(std::vector<uint8_t>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleBinarySignalCallbacksMutex);
    _singleBinarySignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalBinaryCallback(const std::function<void(std::optional<std::vector<uint8_t>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalBinarySignalCallbacksMutex);
    _singleOptionalBinarySignalCallbacks.push_back(cb);
}

void TestableClient::registerThreeBinariesCallback(const std::function<void(std::vector<uint8_t>, std::vector<uint8_t>, std::optional<std::vector<uint8_t>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_threeBinariesSignalCallbacksMutex);
    _threeBinariesSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleArrayOfIntegersCallback(const std::function<void(std::vector<int>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleArrayOfIntegersSignalCallbacksMutex);
    _singleArrayOfIntegersSignalCallbacks.push_back(cb);
}

void TestableClient::registerSingleOptionalArrayOfStringsCallback(const std::function<void(std::optional<std::vector<std::string>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_singleOptionalArrayOfStringsSignalCallbacksMutex);
    _singleOptionalArrayOfStringsSignalCallbacks.push_back(cb);
}

void TestableClient::registerArrayOfEveryTypeCallback(const std::function<void(std::vector<int>, std::vector<double>, std::vector<std::string>, std::vector<Numbers>, std::vector<Entry>, std::vector<std::chrono::time_point<std::chrono::system_clock>>, std::vector<std::chrono::duration<double>>, std::vector<std::vector<uint8_t>>)>& cb)
{
    std::lock_guard<std::mutex> lock(_arrayOfEveryTypeSignalCallbacksMutex);
    _arrayOfEveryTypeSignalCallbacks.push_back(cb);
}

std::future<void> TestableClient::callWithNothing()
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallWithNothingMethodCalls[correlationData] = std::promise<void>();

    rapidjson::Document doc;
    doc.SetObject();

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callWithNothing/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callWithNothing/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallWithNothingMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallWithNothingResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callWithNothing");

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallWithNothingMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallWithNothingMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method doesn't have any return values.
        promiseItr->second.set_value();
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callWithNothing");
}

std::future<int> TestableClient::callOneInteger(int input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOneIntegerMethodCalls[correlationData] = std::promise<int>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", input1, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOneInteger/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneInteger/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOneIntegerMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOneIntegerResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneInteger");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOneInteger signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOneInteger' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOneIntegerMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOneIntegerMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneIntegerReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneInteger");
}

std::future<std::optional<int>> TestableClient::callOptionalInteger(std::optional<int> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOptionalIntegerMethodCalls[correlationData] = std::promise<std::optional<int>>();

    rapidjson::Document doc;
    doc.SetObject();

    if (input1)
        doc.AddMember("input1", *input1, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOptionalInteger/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalInteger/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOptionalIntegerMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOptionalIntegerResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalInteger");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOptionalInteger signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOptionalInteger' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOptionalIntegerMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOptionalIntegerMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalIntegerReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalInteger");
}

std::future<CallThreeIntegersReturnValues> TestableClient::callThreeIntegers(int input1, int input2, std::optional<int> input3)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallThreeIntegersMethodCalls[correlationData] = std::promise<CallThreeIntegersReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", input1, doc.GetAllocator());

    doc.AddMember("input2", input2, doc.GetAllocator());

    if (input3)
        doc.AddMember("input3", *input3, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callThreeIntegers/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeIntegers/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallThreeIntegersMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallThreeIntegersResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeIntegers");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callThreeIntegers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callThreeIntegers' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallThreeIntegersMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallThreeIntegersMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeIntegersReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeIntegers");
}

std::future<std::string> TestableClient::callOneString(std::string input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOneStringMethodCalls[correlationData] = std::promise<std::string>();

    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1.c_str(), input1.size(), doc.GetAllocator());
        doc.AddMember("input1", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOneString/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneString/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOneStringMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOneStringResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneString");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOneString signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOneString' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOneStringMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOneStringMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneStringReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneString");
}

std::future<std::optional<std::string>> TestableClient::callOptionalString(std::optional<std::string> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOptionalStringMethodCalls[correlationData] = std::promise<std::optional<std::string>>();

    rapidjson::Document doc;
    doc.SetObject();

    if (input1) {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1->c_str(), input1->size(), doc.GetAllocator());
        doc.AddMember("input1", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOptionalString/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalString/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOptionalStringMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOptionalStringResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalString");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOptionalString signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOptionalString' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOptionalStringMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOptionalStringMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalStringReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalString");
}

std::future<CallThreeStringsReturnValues> TestableClient::callThreeStrings(std::string input1, std::optional<std::string> input2, std::string input3)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallThreeStringsMethodCalls[correlationData] = std::promise<CallThreeStringsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input1.c_str(), input1.size(), doc.GetAllocator());
        doc.AddMember("input1", tempStringValue, doc.GetAllocator());
    }

    if (input2) {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input2->c_str(), input2->size(), doc.GetAllocator());
        doc.AddMember("input2", tempStringValue, doc.GetAllocator());
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(input3.c_str(), input3.size(), doc.GetAllocator());
        doc.AddMember("input3", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callThreeStrings/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeStrings/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallThreeStringsMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallThreeStringsResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeStrings");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callThreeStrings signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callThreeStrings' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallThreeStringsMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallThreeStringsMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeStringsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeStrings");
}

std::future<Numbers> TestableClient::callOneEnum(Numbers input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOneEnumMethodCalls[correlationData] = std::promise<Numbers>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(input1), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOneEnum/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneEnum/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOneEnumMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOneEnumResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneEnum");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOneEnum signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOneEnum' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOneEnumMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOneEnumMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneEnumReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneEnum");
}

std::future<std::optional<Numbers>> TestableClient::callOptionalEnum(std::optional<Numbers> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOptionalEnumMethodCalls[correlationData] = std::promise<std::optional<Numbers>>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(*input1), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOptionalEnum/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalEnum/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOptionalEnumMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOptionalEnumResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalEnum");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOptionalEnum signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOptionalEnum' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOptionalEnumMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOptionalEnumMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalEnumReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalEnum");
}

std::future<CallThreeEnumsReturnValues> TestableClient::callThreeEnums(Numbers input1, Numbers input2, std::optional<Numbers> input3)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallThreeEnumsMethodCalls[correlationData] = std::promise<CallThreeEnumsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("input1", static_cast<int>(input1), doc.GetAllocator());

    doc.AddMember("input2", static_cast<int>(input2), doc.GetAllocator());

    doc.AddMember("input3", static_cast<int>(*input3), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callThreeEnums/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeEnums/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallThreeEnumsMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallThreeEnumsResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeEnums");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callThreeEnums signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callThreeEnums' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallThreeEnumsMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallThreeEnumsMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeEnumsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeEnums");
}

std::future<AllTypes> TestableClient::callOneStruct(AllTypes input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOneStructMethodCalls[correlationData] = std::promise<AllTypes>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input1.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("input1", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOneStruct/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneStruct/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOneStructMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOneStructResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneStruct");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOneStruct signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOneStruct' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOneStructMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOneStructMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneStructReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneStruct");
}

std::future<std::optional<AllTypes>> TestableClient::callOptionalStruct(std::optional<AllTypes> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOptionalStructMethodCalls[correlationData] = std::promise<std::optional<AllTypes>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (input1) {
            tempStructValue.SetObject();
            input1->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        } else {
            tempStructValue.SetNull();
        }
        doc.AddMember("input1", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOptionalStruct/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalStruct/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOptionalStructMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOptionalStructResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalStruct");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOptionalStruct signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOptionalStruct' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOptionalStructMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOptionalStructMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalStructReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalStruct");
}

std::future<CallThreeStructsReturnValues> TestableClient::callThreeStructs(std::optional<AllTypes> input1, AllTypes input2, AllTypes input3)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallThreeStructsMethodCalls[correlationData] = std::promise<CallThreeStructsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (input1) {
            tempStructValue.SetObject();
            input1->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        } else {
            tempStructValue.SetNull();
        }
        doc.AddMember("input1", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input2.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("input2", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        input3.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("input3", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callThreeStructs/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeStructs/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallThreeStructsMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallThreeStructsResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeStructs");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callThreeStructs signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callThreeStructs' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallThreeStructsMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallThreeStructsMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeStructsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeStructs");
}

std::future<std::chrono::time_point<std::chrono::system_clock>> TestableClient::callOneDateTime(std::chrono::time_point<std::chrono::system_clock> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOneDateTimeMethodCalls[correlationData] = std::promise<std::chrono::time_point<std::chrono::system_clock>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = stinger::utils::timePointToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOneDateTime/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneDateTime/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOneDateTimeMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOneDateTimeResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneDateTime");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOneDateTime signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOneDateTime' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOneDateTimeMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOneDateTimeMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneDateTimeReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneDateTime");
}

std::future<std::optional<std::chrono::time_point<std::chrono::system_clock>>> TestableClient::callOptionalDateTime(std::optional<std::chrono::time_point<std::chrono::system_clock>> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOptionalDateTimeMethodCalls[correlationData] = std::promise<std::optional<std::chrono::time_point<std::chrono::system_clock>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = stinger::utils::timePointToIsoString(*input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOptionalDateTime/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalDateTime/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOptionalDateTimeMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOptionalDateTimeResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalDateTime");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOptionalDateTime signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOptionalDateTime' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOptionalDateTimeMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOptionalDateTimeMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalDateTimeReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalDateTime");
}

std::future<CallThreeDateTimesReturnValues> TestableClient::callThreeDateTimes(std::chrono::time_point<std::chrono::system_clock> input1, std::chrono::time_point<std::chrono::system_clock> input2, std::optional<std::chrono::time_point<std::chrono::system_clock>> input3)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallThreeDateTimesMethodCalls[correlationData] = std::promise<CallThreeDateTimesReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = stinger::utils::timePointToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput2StringValue;
        std::string input2IsoString = stinger::utils::timePointToIsoString(input2);
        tempInput2StringValue.SetString(input2IsoString.c_str(), input2IsoString.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempInput3StringValue;
        std::string input3IsoString = stinger::utils::timePointToIsoString(*input3);
        tempInput3StringValue.SetString(input3IsoString.c_str(), input3IsoString.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callThreeDateTimes/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeDateTimes/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallThreeDateTimesMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallThreeDateTimesResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeDateTimes");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callThreeDateTimes signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callThreeDateTimes' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallThreeDateTimesMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallThreeDateTimesMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeDateTimesReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeDateTimes");
}

std::future<std::chrono::duration<double>> TestableClient::callOneDuration(std::chrono::duration<double> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOneDurationMethodCalls[correlationData] = std::promise<std::chrono::duration<double>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = stinger::utils::durationToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOneDuration/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneDuration/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOneDurationMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOneDurationResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneDuration");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOneDuration signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOneDuration' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOneDurationMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOneDurationMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneDurationReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneDuration");
}

std::future<std::optional<std::chrono::duration<double>>> TestableClient::callOptionalDuration(std::optional<std::chrono::duration<double>> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOptionalDurationMethodCalls[correlationData] = std::promise<std::optional<std::chrono::duration<double>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = stinger::utils::durationToIsoString(*input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOptionalDuration/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalDuration/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOptionalDurationMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOptionalDurationResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalDuration");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOptionalDuration signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOptionalDuration' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOptionalDurationMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOptionalDurationMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalDurationReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalDuration");
}

std::future<CallThreeDurationsReturnValues> TestableClient::callThreeDurations(std::chrono::duration<double> input1, std::chrono::duration<double> input2, std::optional<std::chrono::duration<double>> input3)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallThreeDurationsMethodCalls[correlationData] = std::promise<CallThreeDurationsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput1StringValue;
        std::string input1IsoString = stinger::utils::durationToIsoString(input1);
        tempInput1StringValue.SetString(input1IsoString.c_str(), input1IsoString.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput2StringValue;
        std::string input2IsoString = stinger::utils::durationToIsoString(input2);
        tempInput2StringValue.SetString(input2IsoString.c_str(), input2IsoString.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempInput3StringValue;
        std::string input3IsoString = stinger::utils::durationToIsoString(*input3);
        tempInput3StringValue.SetString(input3IsoString.c_str(), input3IsoString.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callThreeDurations/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeDurations/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallThreeDurationsMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallThreeDurationsResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeDurations");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callThreeDurations signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callThreeDurations' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallThreeDurationsMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallThreeDurationsMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeDurationsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeDurations");
}

std::future<std::vector<uint8_t>> TestableClient::callOneBinary(std::vector<uint8_t> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOneBinaryMethodCalls[correlationData] = std::promise<std::vector<uint8_t>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = stinger::utils::base64Encode(input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOneBinary/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneBinary/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOneBinaryMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOneBinaryResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneBinary");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOneBinary signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOneBinary' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOneBinaryMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOneBinaryMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneBinaryReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneBinary");
}

std::future<std::optional<std::vector<uint8_t>>> TestableClient::callOptionalBinary(std::optional<std::vector<uint8_t>> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOptionalBinaryMethodCalls[correlationData] = std::promise<std::optional<std::vector<uint8_t>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = stinger::utils::base64Encode(*input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOptionalBinary/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalBinary/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOptionalBinaryMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOptionalBinaryResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalBinary");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOptionalBinary signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOptionalBinary' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOptionalBinaryMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOptionalBinaryMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalBinaryReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalBinary");
}

std::future<CallThreeBinariesReturnValues> TestableClient::callThreeBinaries(std::vector<uint8_t> input1, std::vector<uint8_t> input2, std::optional<std::vector<uint8_t>> input3)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallThreeBinariesMethodCalls[correlationData] = std::promise<CallThreeBinariesReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput1StringValue;
        std::string input1B64String = stinger::utils::base64Encode(input1);
        tempInput1StringValue.SetString(input1B64String.c_str(), input1B64String.size(), doc.GetAllocator());
        doc.AddMember("input1", tempInput1StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput2StringValue;
        std::string input2B64String = stinger::utils::base64Encode(input2);
        tempInput2StringValue.SetString(input2B64String.c_str(), input2B64String.size(), doc.GetAllocator());
        doc.AddMember("input2", tempInput2StringValue, doc.GetAllocator());
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempInput3StringValue;
        std::string input3B64String = stinger::utils::base64Encode(*input3);
        tempInput3StringValue.SetString(input3B64String.c_str(), input3B64String.size(), doc.GetAllocator());
        doc.AddMember("input3", tempInput3StringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callThreeBinaries/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeBinaries/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallThreeBinariesMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallThreeBinariesResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callThreeBinaries");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callThreeBinaries signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callThreeBinaries' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallThreeBinariesMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallThreeBinariesMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallThreeBinariesReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callThreeBinaries");
}

std::future<std::vector<int>> TestableClient::callOneListOfIntegers(std::vector<int> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOneListOfIntegersMethodCalls[correlationData] = std::promise<std::vector<int>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: input1) {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("input1", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOneListOfIntegers/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOneListOfIntegers/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOneListOfIntegersMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOneListOfIntegersResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOneListOfIntegers");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOneListOfIntegers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOneListOfIntegers' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOneListOfIntegersMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOneListOfIntegersMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOneListOfIntegersReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOneListOfIntegers");
}

std::future<std::optional<std::vector<double>>> TestableClient::callOptionalListOfFloats(std::optional<std::vector<double>> input1)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallOptionalListOfFloatsMethodCalls[correlationData] = std::promise<std::optional<std::vector<double>>>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *input1) {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("input1", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callOptionalListOfFloats/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalListOfFloats/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallOptionalListOfFloatsMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallOptionalListOfFloatsResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callOptionalListOfFloats");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callOptionalListOfFloats signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callOptionalListOfFloats' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallOptionalListOfFloatsMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallOptionalListOfFloatsMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has a single return value.
        auto returnValue = CallOptionalListOfFloatsReturnValues::FromRapidJsonObject(doc).output1;
        promiseItr->second.set_value(returnValue);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callOptionalListOfFloats");
}

std::future<CallTwoListsReturnValues> TestableClient::callTwoLists(std::vector<Numbers> input1, std::optional<std::vector<std::string>> input2)
{
    std::vector<std::byte> correlationData = stinger::utils::generate_uuid_bytes();
    _pendingCallTwoListsMethodCalls[correlationData] = std::promise<CallTwoListsReturnValues>();

    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: input1) {
            tempArrayValue.PushBack(static_cast<int>(item), doc.GetAllocator());
        }
        doc.AddMember("input1", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *input2) {
            rapidjson::Value tempInput2StringValue;
            tempInput2StringValue.SetString(item.c_str(), item.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempInput2StringValue, doc.GetAllocator());
        }
        doc.AddMember("input2", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    auto responseTopic = stinger::utils::format("client/{client_id}/testable/method/callTwoLists/response", topicParams);
    auto requestTopic = stinger::utils::format("{prefix}/testable/{service_id}/method/callTwoLists/request", topicParams);
    auto msg = stinger::mqtt::Message::MethodRequest(requestTopic, buf.GetString(), correlationData, responseTopic);

    _broker->Publish(msg);

    return _pendingCallTwoListsMethodCalls[correlationData].get_future();
}

void TestableClient::_handleCallTwoListsResponse(
        const stinger::mqtt::Message& msg
)
{
    _broker->Log(LOG_DEBUG, "In response handler for callTwoLists");

    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse callTwoLists signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }
    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload for 'callTwoLists' response is not an object");
    }

    auto correlationData = msg.properties.correlationData.value_or({});
    auto promiseItr = _pendingCallTwoListsMethodCalls.find(correlationData);
    if (promiseItr != _pendingCallTwoListsMethodCalls.end()) {
        if (msg.properties.returnCode && (static_cast<stinger::error::MethodReturnCode>(*(msg.properties.returnCode)) != stinger::error::MethodReturnCode::SUCCESS)) {
            // The method call failed, so set an exception on the promise.
            promiseItr->second.set_exception(createStingerException(static_cast<stinger::error::MethodReturnCode>(msg.properties.returnCode.value_or(static_cast<int>(stinger::error::MethodReturnCode::UNKNOWN_ERROR))), msg.properties.debugInfo.value_or("Exception returned via MQTT")));
            return;
        }

        // Found the promise for this correlation ID.

        // Method has multiple return values.
        auto returnValues = CallTwoListsReturnValues::FromRapidJsonObject(doc);
        promiseItr->second.set_value(returnValues);
    }

    _broker->Log(LOG_DEBUG, "End of response handler for callTwoLists");
}

void TestableClient::_receiveReadWriteIntegerPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_integer' property update payload is not an object");
    }
    ReadWriteIntegerProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.value = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
        _readWriteIntegerProperty = tempValue;
        _lastReadWriteIntegerPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readWriteIntegerPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<int> TestableClient::getReadWriteIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    if (_readWriteIntegerProperty) {
        return _readWriteIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
    _readWriteIntegerPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteIntegerProperty(int value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_integer/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_integer/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteIntegerPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadOnlyIntegerPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_only_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_only_integer' property update payload is not an object");
    }
    ReadOnlyIntegerProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.value = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
        _readOnlyIntegerProperty = tempValue;
        _lastReadOnlyIntegerPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyIntegerPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<int> TestableClient::getReadOnlyIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    if (_readOnlyIntegerProperty) {
        return _readOnlyIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadOnlyIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
    _readOnlyIntegerPropertyCallbacks.push_back(cb);
}

void TestableClient::_receiveReadWriteOptionalIntegerPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_optional_integer' property update payload is not an object");
    }
    ReadWriteOptionalIntegerProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.value = itr->value.GetInt();

        } else {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
        _readWriteOptionalIntegerProperty = tempValue;
        _lastReadWriteOptionalIntegerPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalIntegerPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<int> TestableClient::getReadWriteOptionalIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    if (_readWriteOptionalIntegerProperty) {
        return _readWriteOptionalIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalIntegerPropertyCallback(const std::function<void(std::optional<int> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
    _readWriteOptionalIntegerPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalIntegerProperty(std::optional<int> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    if (value)
        doc.AddMember("value", *value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_integer/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_optional_integer/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteOptionalIntegerPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteTwoIntegersPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_integers property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_two_integers' property update payload is not an object");
    }
    ReadWriteTwoIntegersProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.first = itr->value.GetInt();

        } else {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.second = itr->value.GetInt();

        } else {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
        _readWriteTwoIntegersProperty = tempValue;
        _lastReadWriteTwoIntegersPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoIntegersPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoIntegersProperty> TestableClient::getReadWriteTwoIntegersProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
    if (_readWriteTwoIntegersProperty) {
        return *_readWriteTwoIntegersProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoIntegersPropertyCallback(const std::function<void(int first, std::optional<int> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
    _readWriteTwoIntegersPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoIntegersProperty(int first, std::optional<int> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", first, doc.GetAllocator());

    if (second)
        doc.AddMember("second", *second, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_integers/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_two_integers/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteTwoIntegersPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadOnlyStringPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_only_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_only_string' property update payload is not an object");
    }
    ReadOnlyStringProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.value = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
        _readOnlyStringProperty = tempValue;
        _lastReadOnlyStringPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyStringPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::string> TestableClient::getReadOnlyStringProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    if (_readOnlyStringProperty) {
        return _readOnlyStringProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadOnlyStringPropertyCallback(const std::function<void(std::string value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
    _readOnlyStringPropertyCallbacks.push_back(cb);
}

void TestableClient::_receiveReadWriteStringPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_string' property update payload is not an object");
    }
    ReadWriteStringProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.value = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
        _readWriteStringProperty = tempValue;
        _lastReadWriteStringPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
        for (const auto& cb: _readWriteStringPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::string> TestableClient::getReadWriteStringProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    if (_readWriteStringProperty) {
        return _readWriteStringProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteStringPropertyCallback(const std::function<void(std::string value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
    _readWriteStringPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteStringProperty(std::string value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value.c_str(), value.size(), doc.GetAllocator());
        doc.AddMember("value", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_string/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_string/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteStringPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteOptionalStringPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_optional_string' property update payload is not an object");
    }
    ReadWriteOptionalStringProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.value = itr->value.GetString();

        } else {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
        _readWriteOptionalStringProperty = tempValue;
        _lastReadWriteOptionalStringPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalStringPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::string> TestableClient::getReadWriteOptionalStringProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    if (_readWriteOptionalStringProperty) {
        return _readWriteOptionalStringProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalStringPropertyCallback(const std::function<void(std::optional<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
    _readWriteOptionalStringPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalStringProperty(std::optional<std::string> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    if (value) {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(value->c_str(), value->size(), doc.GetAllocator());
        doc.AddMember("value", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_string/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_optional_string/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteOptionalStringPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteTwoStringsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_strings property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_two_strings' property update payload is not an object");
    }
    ReadWriteTwoStringsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.first = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            tempValue.second = itr->value.GetString();

        } else {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
        _readWriteTwoStringsProperty = tempValue;
        _lastReadWriteTwoStringsPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoStringsPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoStringsProperty> TestableClient::getReadWriteTwoStringsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
    if (_readWriteTwoStringsProperty) {
        return *_readWriteTwoStringsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoStringsPropertyCallback(const std::function<void(std::string first, std::optional<std::string> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
    _readWriteTwoStringsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoStringsProperty(std::string first, std::optional<std::string> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(first.c_str(), first.size(), doc.GetAllocator());
        doc.AddMember("first", tempStringValue, doc.GetAllocator());
    }

    if (second) {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(second->c_str(), second->size(), doc.GetAllocator());
        doc.AddMember("second", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_strings/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_two_strings/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteTwoStringsPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteStructPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_struct property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_struct' property update payload is not an object");
    }
    ReadWriteStructProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.value = AllTypes::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
        _readWriteStructProperty = tempValue;
        _lastReadWriteStructPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
        for (const auto& cb: _readWriteStructPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<AllTypes> TestableClient::getReadWriteStructProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    if (_readWriteStructProperty) {
        return _readWriteStructProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteStructPropertyCallback(const std::function<void(AllTypes value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
    _readWriteStructPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteStructProperty(AllTypes value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        value.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("value", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_struct/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_struct/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteStructPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteOptionalStructPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_struct property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_optional_struct' property update payload is not an object");
    }
    ReadWriteOptionalStructProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.value = AllTypes::FromRapidJsonObject(itr->value);

        } else {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
        _readWriteOptionalStructProperty = tempValue;
        _lastReadWriteOptionalStructPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalStructPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<AllTypes> TestableClient::getReadWriteOptionalStructProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    if (_readWriteOptionalStructProperty) {
        return _readWriteOptionalStructProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalStructPropertyCallback(const std::function<void(std::optional<AllTypes> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
    _readWriteOptionalStructPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalStructProperty(std::optional<AllTypes> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (value) {
            tempStructValue.SetObject();
            value->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        } else {
            tempStructValue.SetNull();
        }
        doc.AddMember("value", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_struct/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_optional_struct/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteOptionalStructPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteTwoStructsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_structs property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_two_structs' property update payload is not an object");
    }
    ReadWriteTwoStructsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.first = AllTypes::FromRapidJsonObject(itr->value);

        } else {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsObject()) {
            tempValue.second = AllTypes::FromRapidJsonObject(itr->value);

        } else {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
        _readWriteTwoStructsProperty = tempValue;
        _lastReadWriteTwoStructsPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoStructsPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoStructsProperty> TestableClient::getReadWriteTwoStructsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
    if (_readWriteTwoStructsProperty) {
        return *_readWriteTwoStructsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoStructsPropertyCallback(const std::function<void(AllTypes first, std::optional<AllTypes> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
    _readWriteTwoStructsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoStructsProperty(AllTypes first, std::optional<AllTypes> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;

        tempStructValue.SetObject();
        first.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("first", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (second) {
            tempStructValue.SetObject();
            second->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        } else {
            tempStructValue.SetNull();
        }
        doc.AddMember("second", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_structs/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_two_structs/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteTwoStructsPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadOnlyEnumPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_only_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_only_enum' property update payload is not an object");
    }
    ReadOnlyEnumProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.value = static_cast<Numbers>(itr->value.GetInt());

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
        _readOnlyEnumProperty = tempValue;
        _lastReadOnlyEnumPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyEnumPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<Numbers> TestableClient::getReadOnlyEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    if (_readOnlyEnumProperty) {
        return _readOnlyEnumProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadOnlyEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
    _readOnlyEnumPropertyCallbacks.push_back(cb);
}

void TestableClient::_receiveReadWriteEnumPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_enum' property update payload is not an object");
    }
    ReadWriteEnumProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.value = static_cast<Numbers>(itr->value.GetInt());

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
        _readWriteEnumProperty = tempValue;
        _lastReadWriteEnumPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
        for (const auto& cb: _readWriteEnumPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<Numbers> TestableClient::getReadWriteEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    if (_readWriteEnumProperty) {
        return _readWriteEnumProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
    _readWriteEnumPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteEnumProperty(Numbers value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_enum/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_enum/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteEnumPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteOptionalEnumPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_optional_enum' property update payload is not an object");
    }
    ReadWriteOptionalEnumProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.value = static_cast<Numbers>(itr->value.GetInt());

        } else {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
        _readWriteOptionalEnumProperty = tempValue;
        _lastReadWriteOptionalEnumPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalEnumPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<Numbers> TestableClient::getReadWriteOptionalEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    if (_readWriteOptionalEnumProperty) {
        return _readWriteOptionalEnumProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalEnumPropertyCallback(const std::function<void(std::optional<Numbers> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
    _readWriteOptionalEnumPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalEnumProperty(std::optional<Numbers> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(*value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_enum/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_optional_enum/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteOptionalEnumPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteTwoEnumsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_enums property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_two_enums' property update payload is not an object");
    }
    ReadWriteTwoEnumsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.first = static_cast<Numbers>(itr->value.GetInt());

        } else {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsInt()) {
            tempValue.second = static_cast<Numbers>(itr->value.GetInt());

        } else {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
        _readWriteTwoEnumsProperty = tempValue;
        _lastReadWriteTwoEnumsPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoEnumsPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoEnumsProperty> TestableClient::getReadWriteTwoEnumsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
    if (_readWriteTwoEnumsProperty) {
        return *_readWriteTwoEnumsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoEnumsPropertyCallback(const std::function<void(Numbers first, std::optional<Numbers> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
    _readWriteTwoEnumsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoEnumsProperty(Numbers first, std::optional<Numbers> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", static_cast<int>(first), doc.GetAllocator());

    doc.AddMember("second", static_cast<int>(*second), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_enums/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_two_enums/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteTwoEnumsPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteDatetimePropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_datetime property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_datetime' property update payload is not an object");
    }
    ReadWriteDatetimeProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempValueIsoString = itr->value.GetString();
            tempValue.value = stinger::utils::parseIsoTimestamp(tempValueIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
        _readWriteDatetimeProperty = tempValue;
        _lastReadWriteDatetimePropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
        for (const auto& cb: _readWriteDatetimePropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> TestableClient::getReadWriteDatetimeProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    if (_readWriteDatetimeProperty) {
        return _readWriteDatetimeProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteDatetimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
    _readWriteDatetimePropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteDatetimeProperty(std::chrono::time_point<std::chrono::system_clock> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = stinger::utils::timePointToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_datetime/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_datetime/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteDatetimePropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteOptionalDatetimePropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_datetime property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_optional_datetime' property update payload is not an object");
    }
    ReadWriteOptionalDatetimeProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempValueIsoString = itr->value.GetString();
            tempValue.value = stinger::utils::parseIsoTimestamp(tempValueIsoString);

        } else {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
        _readWriteOptionalDatetimeProperty = tempValue;
        _lastReadWriteOptionalDatetimePropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalDatetimePropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> TestableClient::getReadWriteOptionalDatetimeProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    if (_readWriteOptionalDatetimeProperty) {
        return _readWriteOptionalDatetimeProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalDatetimePropertyCallback(const std::function<void(std::optional<std::chrono::time_point<std::chrono::system_clock>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
    _readWriteOptionalDatetimePropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalDatetimeProperty(std::optional<std::chrono::time_point<std::chrono::system_clock>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = stinger::utils::timePointToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_datetime/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_optional_datetime/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteOptionalDatetimePropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteTwoDatetimesPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_datetimes property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_two_datetimes' property update payload is not an object");
    }
    ReadWriteTwoDatetimesProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempFirstIsoString = itr->value.GetString();
            tempValue.first = stinger::utils::parseIsoTimestamp(tempFirstIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempSecondIsoString = itr->value.GetString();
            tempValue.second = stinger::utils::parseIsoTimestamp(tempSecondIsoString);

        } else {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
        _readWriteTwoDatetimesProperty = tempValue;
        _lastReadWriteTwoDatetimesPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoDatetimesPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoDatetimesProperty> TestableClient::getReadWriteTwoDatetimesProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
    if (_readWriteTwoDatetimesProperty) {
        return *_readWriteTwoDatetimesProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoDatetimesPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> first, std::optional<std::chrono::time_point<std::chrono::system_clock>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
    _readWriteTwoDatetimesPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoDatetimesProperty(std::chrono::time_point<std::chrono::system_clock> first, std::optional<std::chrono::time_point<std::chrono::system_clock>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = stinger::utils::timePointToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = stinger::utils::timePointToIsoString(*second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_datetimes/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_two_datetimes/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteTwoDatetimesPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteDurationPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_duration property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_duration' property update payload is not an object");
    }
    ReadWriteDurationProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempValueIsoString = itr->value.GetString();
            tempValue.value = stinger::utils::parseIsoDuration(tempValueIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
        _readWriteDurationProperty = tempValue;
        _lastReadWriteDurationPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
        for (const auto& cb: _readWriteDurationPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::chrono::duration<double>> TestableClient::getReadWriteDurationProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    if (_readWriteDurationProperty) {
        return _readWriteDurationProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteDurationPropertyCallback(const std::function<void(std::chrono::duration<double> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
    _readWriteDurationPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteDurationProperty(std::chrono::duration<double> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = stinger::utils::durationToIsoString(value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_duration/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_duration/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteDurationPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteOptionalDurationPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_duration property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_optional_duration' property update payload is not an object");
    }
    ReadWriteOptionalDurationProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempValueIsoString = itr->value.GetString();
            tempValue.value = stinger::utils::parseIsoDuration(tempValueIsoString);

        } else {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
        _readWriteOptionalDurationProperty = tempValue;
        _lastReadWriteOptionalDurationPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalDurationPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::chrono::duration<double>> TestableClient::getReadWriteOptionalDurationProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    if (_readWriteOptionalDurationProperty) {
        return _readWriteOptionalDurationProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalDurationPropertyCallback(const std::function<void(std::optional<std::chrono::duration<double>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
    _readWriteOptionalDurationPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalDurationProperty(std::optional<std::chrono::duration<double>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempValueStringValue;
        std::string valueIsoString = stinger::utils::durationToIsoString(*value);
        tempValueStringValue.SetString(valueIsoString.c_str(), valueIsoString.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_duration/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_optional_duration/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteOptionalDurationPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteTwoDurationsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_durations property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_two_durations' property update payload is not an object");
    }
    ReadWriteTwoDurationsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempFirstIsoString = itr->value.GetString();
            tempValue.first = stinger::utils::parseIsoDuration(tempFirstIsoString);

        } else {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempSecondIsoString = itr->value.GetString();
            tempValue.second = stinger::utils::parseIsoDuration(tempSecondIsoString);

        } else {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
        _readWriteTwoDurationsProperty = tempValue;
        _lastReadWriteTwoDurationsPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoDurationsPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoDurationsProperty> TestableClient::getReadWriteTwoDurationsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
    if (_readWriteTwoDurationsProperty) {
        return *_readWriteTwoDurationsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoDurationsPropertyCallback(const std::function<void(std::chrono::duration<double> first, std::optional<std::chrono::duration<double>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
    _readWriteTwoDurationsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoDurationsProperty(std::chrono::duration<double> first, std::optional<std::chrono::duration<double>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempFirstStringValue;
        std::string firstIsoString = stinger::utils::durationToIsoString(first);
        tempFirstStringValue.SetString(firstIsoString.c_str(), firstIsoString.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempSecondStringValue;
        std::string secondIsoString = stinger::utils::durationToIsoString(*second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_durations/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_two_durations/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteTwoDurationsPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteBinaryPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_binary property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_binary' property update payload is not an object");
    }
    ReadWriteBinaryProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempValueB64String = itr->value.GetString();
            tempValue.value = stinger::utils::base64Decode(tempValueB64String);

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
        _readWriteBinaryProperty = tempValue;
        _lastReadWriteBinaryPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
        for (const auto& cb: _readWriteBinaryPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::vector<uint8_t>> TestableClient::getReadWriteBinaryProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    if (_readWriteBinaryProperty) {
        return _readWriteBinaryProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteBinaryPropertyCallback(const std::function<void(std::vector<uint8_t> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
    _readWriteBinaryPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteBinaryProperty(std::vector<uint8_t> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = stinger::utils::base64Encode(value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_binary/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_binary/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteBinaryPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteOptionalBinaryPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_binary property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_optional_binary' property update payload is not an object");
    }
    ReadWriteOptionalBinaryProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempValueB64String = itr->value.GetString();
            tempValue.value = stinger::utils::base64Decode(tempValueB64String);

        } else {
            tempValue.value = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
        _readWriteOptionalBinaryProperty = tempValue;
        _lastReadWriteOptionalBinaryPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalBinaryPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::vector<uint8_t>> TestableClient::getReadWriteOptionalBinaryProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    if (_readWriteOptionalBinaryProperty) {
        return _readWriteOptionalBinaryProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteOptionalBinaryPropertyCallback(const std::function<void(std::optional<std::vector<uint8_t>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
    _readWriteOptionalBinaryPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteOptionalBinaryProperty(std::optional<std::vector<uint8_t>> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempValueStringValue;
        std::string valueB64String = stinger::utils::base64Encode(*value);
        tempValueStringValue.SetString(valueB64String.c_str(), valueB64String.size(), doc.GetAllocator());
        doc.AddMember("value", tempValueStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_binary/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_optional_binary/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteOptionalBinaryPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteTwoBinariesPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_binaries property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_two_binaries' property update payload is not an object");
    }
    ReadWriteTwoBinariesProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempFirstB64String = itr->value.GetString();
            tempValue.first = stinger::utils::base64Decode(tempFirstB64String);

        } else {
            throw std::runtime_error("Received payload for the 'first' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
        if (itr != doc.MemberEnd() && itr->value.IsString()) {
            auto tempSecondB64String = itr->value.GetString();
            tempValue.second = stinger::utils::base64Decode(tempSecondB64String);

        } else {
            tempValue.second = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
        _readWriteTwoBinariesProperty = tempValue;
        _lastReadWriteTwoBinariesPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoBinariesPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.first, tempValue.second);
        }
    }
}

std::optional<ReadWriteTwoBinariesProperty> TestableClient::getReadWriteTwoBinariesProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
    if (_readWriteTwoBinariesProperty) {
        return *_readWriteTwoBinariesProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteTwoBinariesPropertyCallback(const std::function<void(std::vector<uint8_t> first, std::optional<std::vector<uint8_t>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
    _readWriteTwoBinariesPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteTwoBinariesProperty(std::vector<uint8_t> first, std::optional<std::vector<uint8_t>> second) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempFirstStringValue;
        std::string firstB64String = stinger::utils::base64Encode(first);
        tempFirstStringValue.SetString(firstB64String.c_str(), firstB64String.size(), doc.GetAllocator());
        doc.AddMember("first", tempFirstStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempSecondStringValue;
        std::string secondB64String = stinger::utils::base64Encode(*second);
        tempSecondStringValue.SetString(secondB64String.c_str(), secondB64String.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_binaries/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_two_binaries/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteTwoBinariesPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteListOfStringsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_list_of_strings property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_list_of_strings' property update payload is not an object");
    }
    ReadWriteListOfStringsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("value");
        if (itr != doc.MemberEnd() && itr->value.IsArray()) {
            {
                std::vector<std::string> tempArray;
                for (const auto& item: itr->value.GetArray()) {
                    if (item.IsString()) {
                        tempArray.push_back(item.GetString());
                    }
                }
                tempValue.value = std::move(tempArray);
            }

        } else {
            throw std::runtime_error("Received payload for the 'value' argument doesn't have required value/type");
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
        _readWriteListOfStringsProperty = tempValue;
        _lastReadWriteListOfStringsPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteListOfStringsPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.value);
        }
    }
}

std::optional<std::vector<std::string>> TestableClient::getReadWriteListOfStringsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
    if (_readWriteListOfStringsProperty) {
        return _readWriteListOfStringsProperty->value;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteListOfStringsPropertyCallback(const std::function<void(std::vector<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyCallbacksMutex);
    _readWriteListOfStringsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteListOfStringsProperty(std::vector<std::string> value) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: value) {
            rapidjson::Value tempValueStringValue;
            tempValueStringValue.SetString(item.c_str(), item.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempValueStringValue, doc.GetAllocator());
        }
        doc.AddMember("value", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_list_of_strings/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_list_of_strings/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteListOfStringsPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

void TestableClient::_receiveReadWriteListsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_lists property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received 'read_write_lists' property update payload is not an object");
    }
    ReadWriteListsProperty tempValue;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("the_list");
        if (itr != doc.MemberEnd() && itr->value.IsArray()) {
            {
                std::vector<Numbers> tempArray;
                for (const auto& item: itr->value.GetArray()) {
                    if (item.IsInt()) {
                        tempArray.push_back(static_cast<Numbers>(item.GetInt()));
                    }
                }
                tempValue.theList = std::move(tempArray);
            }

        } else {
            throw std::runtime_error("Received payload for the 'the_list' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = doc.FindMember("optionalList");
        if (itr != doc.MemberEnd() && itr->value.IsArray()) {
            {
                std::vector<std::chrono::time_point<std::chrono::system_clock>> tempArray;
                for (const auto& item: itr->value.GetArray()) {
                    if (item.IsString()) {
                        {
                            std::string tempIsoString = item.GetString();
                            tempArray.push_back(stinger::utils::parseIsoTimestamp(tempIsoString));
                        }
                    }
                }
                tempValue.optionalList = std::move(tempArray);
            }

        } else {
            tempValue.optionalList = std::nullopt;
        }
    }

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
        _readWriteListsProperty = tempValue;
        _lastReadWriteListsPropertyVersion = msg.properties.propertyVersion ? *msg.properties.propertyVersion : -1;
    }
    // Notify all registered callbacks.
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteListsPropertyCallbacks) {
            // Don't need a mutex since we're using tempValue.
            cb(tempValue.theList, tempValue.optionalList);
        }
    }
}

std::optional<ReadWriteListsProperty> TestableClient::getReadWriteListsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
    if (_readWriteListsProperty) {
        return *_readWriteListsProperty;
    }
    return std::nullopt;
}

void TestableClient::registerReadWriteListsPropertyCallback(const std::function<void(std::vector<Numbers> theList, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyCallbacksMutex);
    _readWriteListsPropertyCallbacks.push_back(cb);
}

std::future<bool> TestableClient::updateReadWriteListsProperty(std::vector<Numbers> theList, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList) const
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: theList) {
            tempArrayValue.PushBack(static_cast<int>(item), doc.GetAllocator());
        }
        doc.AddMember("the_list", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *optionalList) {
            rapidjson::Value tempOptionalListStringValue;
            std::string itemIsoString = stinger::utils::timePointToIsoString(item);
            tempOptionalListStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempOptionalListStringValue, doc.GetAllocator());
        }
        doc.AddMember("optionalList", tempArrayValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicParams;
    topicParams["client_id"] = _broker->GetClientId();
    topicParams["service_id"] = _instanceInfo.serviceId.value_or("error_service_id_not_found");
    topicParams["interface_name"] = NAME;
    topicParams["prefix"] = _instanceInfo.prefix.value_or("error_prefix_not_found");

    std::string update_topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_lists/update", topicParams);
    std::string response_topic = stinger::utils::format("client/{client_id}/testable/property/read_write_lists/update/response", topicParams);
    auto correlationData = stinger::utils::generate_uuid_bytes();
    auto msg = stinger::mqtt::Message::PropertyUpdateRequest(update_topic, buf.GetString(), _lastReadWriteListsPropertyVersion, correlationData, response_topic);
    return _broker->Publish(msg);
}

} // namespace testable

} // namespace gen

} // namespace stinger
