
#include <vector>
#include <iostream>
#include <syslog.h>

#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>
#include "structs.hpp"
#include "server.hpp"
#include "method_payloads.hpp"
#include "enums.hpp"
#include <stinger/utils/iconnection.hpp>
#include <stinger/utils/format.hpp>
#include <stinger/error/return_codes.hpp>

namespace stinger {

namespace gen {
namespace testable {

constexpr const char TestableServer::NAME[];
constexpr const char TestableServer::INTERFACE_VERSION[];

TestableServer::TestableServer(std::shared_ptr<stinger::utils::IConnection> broker, const std::string& instanceId, const std::string& prefix):
    _broker(broker), _instanceId(instanceId), _advertisementThreadRunning(false), _prefixTopicParam(prefix)

{
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const stinger::mqtt::Message& msg
                                                               )
                                                               {
                                                                   _receiveMessage(msg);
                                                               });

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["prefix"] = _prefixTopicParam;

    _callWithNothingMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callWithNothing/request", topicArgs), 2);
    _callOneIntegerMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneInteger/request", topicArgs), 2);
    _callOptionalIntegerMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalInteger/request", topicArgs), 2);
    _callThreeIntegersMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeIntegers/request", topicArgs), 2);
    _callOneStringMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneString/request", topicArgs), 2);
    _callOptionalStringMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalString/request", topicArgs), 2);
    _callThreeStringsMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeStrings/request", topicArgs), 2);
    _callOneEnumMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneEnum/request", topicArgs), 2);
    _callOptionalEnumMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalEnum/request", topicArgs), 2);
    _callThreeEnumsMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeEnums/request", topicArgs), 2);
    _callOneStructMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneStruct/request", topicArgs), 2);
    _callOptionalStructMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalStruct/request", topicArgs), 2);
    _callThreeStructsMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeStructs/request", topicArgs), 2);
    _callOneDateTimeMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneDateTime/request", topicArgs), 2);
    _callOptionalDateTimeMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalDateTime/request", topicArgs), 2);
    _callThreeDateTimesMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeDateTimes/request", topicArgs), 2);
    _callOneDurationMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneDuration/request", topicArgs), 2);
    _callOptionalDurationMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalDuration/request", topicArgs), 2);
    _callThreeDurationsMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeDurations/request", topicArgs), 2);
    _callOneBinaryMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneBinary/request", topicArgs), 2);
    _callOptionalBinaryMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalBinary/request", topicArgs), 2);
    _callThreeBinariesMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeBinaries/request", topicArgs), 2);
    _callOneListOfIntegersMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneListOfIntegers/request", topicArgs), 2);
    _callOptionalListOfFloatsMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalListOfFloats/request", topicArgs), 2);
    _callTwoListsMethodSubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callTwoLists/request", topicArgs), 2);

    _readWriteIntegerPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_integer/update", topicArgs), 1);
    _readOnlyIntegerPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_integer/update", topicArgs), 1);
    _readWriteOptionalIntegerPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_integer/update", topicArgs), 1);
    _readWriteTwoIntegersPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_integers/update", topicArgs), 1);
    _readOnlyStringPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_string/update", topicArgs), 1);
    _readWriteStringPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_string/update", topicArgs), 1);
    _readWriteOptionalStringPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_string/update", topicArgs), 1);
    _readWriteTwoStringsPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_strings/update", topicArgs), 1);
    _readWriteStructPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_struct/update", topicArgs), 1);
    _readWriteOptionalStructPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_struct/update", topicArgs), 1);
    _readWriteTwoStructsPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_structs/update", topicArgs), 1);
    _readOnlyEnumPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_enum/update", topicArgs), 1);
    _readWriteEnumPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_enum/update", topicArgs), 1);
    _readWriteOptionalEnumPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_enum/update", topicArgs), 1);
    _readWriteTwoEnumsPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_enums/update", topicArgs), 1);
    _readWriteDatetimePropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_datetime/update", topicArgs), 1);
    _readWriteOptionalDatetimePropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_datetime/update", topicArgs), 1);
    _readWriteTwoDatetimesPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_datetimes/update", topicArgs), 1);
    _readWriteDurationPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_duration/update", topicArgs), 1);
    _readWriteOptionalDurationPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_duration/update", topicArgs), 1);
    _readWriteTwoDurationsPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_durations/update", topicArgs), 1);
    _readWriteBinaryPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_binary/update", topicArgs), 1);
    _readWriteOptionalBinaryPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_binary/update", topicArgs), 1);
    _readWriteTwoBinariesPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_binaries/update", topicArgs), 1);
    _readWriteListOfStringsPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_list_of_strings/update", topicArgs), 1);
    _readWriteListsPropertySubscriptionId = _broker->Subscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_lists/update", topicArgs), 1);

    // Start the service advertisement thread
    _advertisementThreadRunning = true;
    _advertisementThread = std::thread(&TestableServer::_advertisementThreadLoop, this);
}

TestableServer::~TestableServer()
{
    // Unregister the message callback from the broker.
    if (_broker && _brokerMessageCallbackHandle != 0) {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }

    // Stop the advertisement thread
    _advertisementThreadRunning = false;
    if (_advertisementThread.joinable()) {
        _advertisementThread.join();
    }

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["prefix"] = _prefixTopicParam;

    std::string topic = stinger::utils::format("{prefix}/testable/{service_id}/interface", topicArgs);
    auto msg = stinger::mqtt::Message::ServiceOffline(topic);
    _broker->Publish(msg);

    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callWithNothing/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneInteger/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalInteger/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeIntegers/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneString/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalString/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeStrings/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneEnum/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalEnum/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeEnums/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneStruct/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalStruct/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeStructs/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneDateTime/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalDateTime/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeDateTimes/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneDuration/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalDuration/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeDurations/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneBinary/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalBinary/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callThreeBinaries/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOneListOfIntegers/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callOptionalListOfFloats/request", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/method/callTwoLists/request", topicArgs));

    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_integer/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_integer/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_integer/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_integers/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_string/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_string/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_string/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_strings/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_struct/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_struct/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_structs/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_enum/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_enum/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_enum/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_enums/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_datetime/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_datetime/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_datetimes/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_duration/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_duration/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_durations/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_binary/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_binary/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_binaries/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_list_of_strings/update", topicArgs));
    _broker->Unsubscribe(stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_lists/update", topicArgs));
}

void TestableServer::_receiveMessage(const stinger::mqtt::Message& msg)
{
    const int noSubId = -1;
    int subscriptionId = msg.properties.subscriptionId.value_or(noSubId);

    if (subscriptionId == _callWithNothingMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callWithNothing method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callWithNothingHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallWithNothingHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOneIntegerMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneInteger method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOneIntegerHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOneIntegerHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOptionalIntegerMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalInteger method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOptionalIntegerHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOptionalIntegerHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callThreeIntegersMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeIntegers method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callThreeIntegersHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallThreeIntegersHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOneStringMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneString method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOneStringHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOneStringHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOptionalStringMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalString method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOptionalStringHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOptionalStringHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callThreeStringsMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeStrings method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callThreeStringsHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallThreeStringsHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOneEnumMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneEnum method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOneEnumHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOneEnumHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOptionalEnumMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalEnum method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOptionalEnumHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOptionalEnumHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callThreeEnumsMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeEnums method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callThreeEnumsHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallThreeEnumsHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOneStructMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneStruct method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOneStructHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOneStructHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOptionalStructMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalStruct method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOptionalStructHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOptionalStructHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callThreeStructsMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeStructs method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callThreeStructsHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallThreeStructsHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOneDateTimeMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneDateTime method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOneDateTimeHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOneDateTimeHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOptionalDateTimeMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalDateTime method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOptionalDateTimeHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOptionalDateTimeHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callThreeDateTimesMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeDateTimes method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callThreeDateTimesHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallThreeDateTimesHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOneDurationMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneDuration method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOneDurationHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOneDurationHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOptionalDurationMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalDuration method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOptionalDurationHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOptionalDurationHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callThreeDurationsMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeDurations method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callThreeDurationsHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallThreeDurationsHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOneBinaryMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneBinary method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOneBinaryHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOneBinaryHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOptionalBinaryMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalBinary method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOptionalBinaryHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOptionalBinaryHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callThreeBinariesMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callThreeBinaries method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callThreeBinariesHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallThreeBinariesHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOneListOfIntegersMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOneListOfIntegers method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOneListOfIntegersHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOneListOfIntegersHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callOptionalListOfFloatsMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callOptionalListOfFloats method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callOptionalListOfFloatsHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallOptionalListOfFloatsHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    else if (subscriptionId == _callTwoListsMethodSubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as callTwoLists method request.", msg.topic.c_str());
        rapidjson::Document doc;
        try {
            if (_callTwoListsHandler) {
                rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
                if (!ok) {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callCallTwoListsHandler(msg.topic, doc, msg.properties.correlationData, msg.properties.responseTopic);
            }
        } catch (const std::exception&) {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely.
            // TODO: Log this failure
        }
    }

    if (subscriptionId == _readWriteIntegerPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_integer property update.", msg.topic.c_str());
        _receiveReadWriteIntegerPropertyUpdate(msg);
    }

    else if (subscriptionId == _readOnlyIntegerPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_integer property update.", msg.topic.c_str());
        _receiveReadOnlyIntegerPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteOptionalIntegerPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_integer property update.", msg.topic.c_str());
        _receiveReadWriteOptionalIntegerPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteTwoIntegersPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_integers property update.", msg.topic.c_str());
        _receiveReadWriteTwoIntegersPropertyUpdate(msg);
    }

    else if (subscriptionId == _readOnlyStringPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_string property update.", msg.topic.c_str());
        _receiveReadOnlyStringPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteStringPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_string property update.", msg.topic.c_str());
        _receiveReadWriteStringPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteOptionalStringPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_string property update.", msg.topic.c_str());
        _receiveReadWriteOptionalStringPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteTwoStringsPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_strings property update.", msg.topic.c_str());
        _receiveReadWriteTwoStringsPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteStructPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_struct property update.", msg.topic.c_str());
        _receiveReadWriteStructPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteOptionalStructPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_struct property update.", msg.topic.c_str());
        _receiveReadWriteOptionalStructPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteTwoStructsPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_structs property update.", msg.topic.c_str());
        _receiveReadWriteTwoStructsPropertyUpdate(msg);
    }

    else if (subscriptionId == _readOnlyEnumPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_only_enum property update.", msg.topic.c_str());
        _receiveReadOnlyEnumPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteEnumPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_enum property update.", msg.topic.c_str());
        _receiveReadWriteEnumPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteOptionalEnumPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_enum property update.", msg.topic.c_str());
        _receiveReadWriteOptionalEnumPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteTwoEnumsPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_enums property update.", msg.topic.c_str());
        _receiveReadWriteTwoEnumsPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteDatetimePropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_datetime property update.", msg.topic.c_str());
        _receiveReadWriteDatetimePropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteOptionalDatetimePropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_datetime property update.", msg.topic.c_str());
        _receiveReadWriteOptionalDatetimePropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteTwoDatetimesPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_datetimes property update.", msg.topic.c_str());
        _receiveReadWriteTwoDatetimesPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteDurationPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_duration property update.", msg.topic.c_str());
        _receiveReadWriteDurationPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteOptionalDurationPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_duration property update.", msg.topic.c_str());
        _receiveReadWriteOptionalDurationPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteTwoDurationsPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_durations property update.", msg.topic.c_str());
        _receiveReadWriteTwoDurationsPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteBinaryPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_binary property update.", msg.topic.c_str());
        _receiveReadWriteBinaryPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteOptionalBinaryPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_optional_binary property update.", msg.topic.c_str());
        _receiveReadWriteOptionalBinaryPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteTwoBinariesPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_two_binaries property update.", msg.topic.c_str());
        _receiveReadWriteTwoBinariesPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteListOfStringsPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_list_of_strings property update.", msg.topic.c_str());
        _receiveReadWriteListOfStringsPropertyUpdate(msg);
    }

    else if (subscriptionId == _readWriteListsPropertySubscriptionId) {
        _broker->Log(LOG_INFO, "Message to `%s` matched as read_write_lists property update.", msg.topic.c_str());
        _receiveReadWriteListsPropertyUpdate(msg);
    }
}

std::future<bool> TestableServer::emitEmptySignal()
{
    rapidjson::Document doc;
    doc.SetObject();
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "empty";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/empty", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleIntSignal(int value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleInt";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleInt", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleOptionalIntSignal(std::optional<int> value)
{
    rapidjson::Document doc;
    doc.SetObject();
    if (value)
        doc.AddMember("value", *value, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleOptionalInt";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalInt", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitThreeIntegersSignal(int first, int second, std::optional<int> third)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", first, doc.GetAllocator());

    doc.AddMember("second", second, doc.GetAllocator());

    if (third)
        doc.AddMember("third", *third, doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "threeIntegers";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeIntegers", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleStringSignal(std::string value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleString";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleString", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleOptionalStringSignal(std::optional<std::string> value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleOptionalString";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalString", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitThreeStringsSignal(std::string first, std::string second, std::optional<std::string> third)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(first.c_str(), first.size(), doc.GetAllocator());
        doc.AddMember("first", tempStringValue, doc.GetAllocator());
    }

    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(second.c_str(), second.size(), doc.GetAllocator());
        doc.AddMember("second", tempStringValue, doc.GetAllocator());
    }

    if (third) {
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(third->c_str(), third->size(), doc.GetAllocator());
        doc.AddMember("third", tempStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "threeStrings";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeStrings", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleEnumSignal(Numbers value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleEnum";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleEnum", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleOptionalEnumSignal(std::optional<Numbers> value)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("value", static_cast<int>(*value), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleOptionalEnum";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalEnum", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitThreeEnumsSignal(Numbers first, Numbers second, std::optional<Numbers> third)
{
    rapidjson::Document doc;
    doc.SetObject();

    doc.AddMember("first", static_cast<int>(first), doc.GetAllocator());

    doc.AddMember("second", static_cast<int>(second), doc.GetAllocator());

    doc.AddMember("third", static_cast<int>(*third), doc.GetAllocator());

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "threeEnums";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeEnums", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleStructSignal(AllTypes value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleStruct";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleStruct", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleOptionalStructSignal(std::optional<AllTypes> value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleOptionalStruct";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalStruct", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitThreeStructsSignal(AllTypes first, AllTypes second, std::optional<AllTypes> third)
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

        tempStructValue.SetObject();
        second.AddToRapidJsonObject(tempStructValue, doc.GetAllocator());

        doc.AddMember("second", tempStructValue, doc.GetAllocator());
    }

    { // Restrict Scope for struct serialization
        rapidjson::Value tempStructValue;
        if (third) {
            tempStructValue.SetObject();
            third->AddToRapidJsonObject(tempStructValue, doc.GetAllocator());
        } else {
            tempStructValue.SetNull();
        }
        doc.AddMember("third", tempStructValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "threeStructs";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeStructs", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleDateTimeSignal(std::chrono::time_point<std::chrono::system_clock> value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleDateTime";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleDateTime", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleOptionalDatetimeSignal(std::optional<std::chrono::time_point<std::chrono::system_clock>> value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleOptionalDatetime";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalDatetime", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitThreeDateTimesSignal(std::chrono::time_point<std::chrono::system_clock> first, std::chrono::time_point<std::chrono::system_clock> second, std::optional<std::chrono::time_point<std::chrono::system_clock>> third)
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
        std::string secondIsoString = stinger::utils::timePointToIsoString(second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for datetime ISO string conversion
        rapidjson::Value tempThirdStringValue;
        std::string thirdIsoString = stinger::utils::timePointToIsoString(*third);
        tempThirdStringValue.SetString(thirdIsoString.c_str(), thirdIsoString.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "threeDateTimes";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeDateTimes", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleDurationSignal(std::chrono::duration<double> value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleDuration";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleDuration", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleOptionalDurationSignal(std::optional<std::chrono::duration<double>> value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleOptionalDuration";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalDuration", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitThreeDurationsSignal(std::chrono::duration<double> first, std::chrono::duration<double> second, std::optional<std::chrono::duration<double>> third)
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
        std::string secondIsoString = stinger::utils::durationToIsoString(second);
        tempSecondStringValue.SetString(secondIsoString.c_str(), secondIsoString.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for duration ISO string conversion
        rapidjson::Value tempThirdStringValue;
        std::string thirdIsoString = stinger::utils::durationToIsoString(*third);
        tempThirdStringValue.SetString(thirdIsoString.c_str(), thirdIsoString.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "threeDurations";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeDurations", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleBinarySignal(std::vector<uint8_t> value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleBinary";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleBinary", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleOptionalBinarySignal(std::optional<std::vector<uint8_t>> value)
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

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleOptionalBinary";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalBinary", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitThreeBinariesSignal(std::vector<uint8_t> first, std::vector<uint8_t> second, std::optional<std::vector<uint8_t>> third)
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
        std::string secondB64String = stinger::utils::base64Encode(second);
        tempSecondStringValue.SetString(secondB64String.c_str(), secondB64String.size(), doc.GetAllocator());
        doc.AddMember("second", tempSecondStringValue, doc.GetAllocator());
    }

    { // Restrict Scope for binary base64 encoding
        rapidjson::Value tempThirdStringValue;
        std::string thirdB64String = stinger::utils::base64Encode(*third);
        tempThirdStringValue.SetString(thirdB64String.c_str(), thirdB64String.size(), doc.GetAllocator());
        doc.AddMember("third", tempThirdStringValue, doc.GetAllocator());
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "threeBinaries";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/threeBinaries", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleArrayOfIntegersSignal(std::vector<int> values)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: values) {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("values", tempArrayValue, doc.GetAllocator());
    }
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleArrayOfIntegers";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleArrayOfIntegers", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitSingleOptionalArrayOfStringsSignal(std::optional<std::vector<std::string>> values)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: *values) {
            rapidjson::Value tempValuesStringValue;
            tempValuesStringValue.SetString(item.c_str(), item.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempValuesStringValue, doc.GetAllocator());
        }
        doc.AddMember("values", tempArrayValue, doc.GetAllocator());
    }
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "singleOptionalArrayOfStrings";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/singleOptionalArrayOfStrings", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

std::future<bool> TestableServer::emitArrayOfEveryTypeSignal(std::vector<int> firstOfIntegers, std::vector<double> secondOfFloats, std::vector<std::string> thirdOfStrings, std::vector<Numbers> fourthOfEnums, std::vector<Entry> fifthOfStructs, std::vector<std::chrono::time_point<std::chrono::system_clock>> sixthOfDatetimes, std::vector<std::chrono::duration<double>> seventhOfDurations, std::vector<std::vector<uint8_t>> eighthOfBinaries)
{
    rapidjson::Document doc;
    doc.SetObject();

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: firstOfIntegers) {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("first_of_integers", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: secondOfFloats) {
            tempArrayValue.PushBack(item, doc.GetAllocator());
        }
        doc.AddMember("second_of_floats", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: thirdOfStrings) {
            rapidjson::Value tempThirdOfStringsStringValue;
            tempThirdOfStringsStringValue.SetString(item.c_str(), item.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempThirdOfStringsStringValue, doc.GetAllocator());
        }
        doc.AddMember("third_of_strings", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: fourthOfEnums) {
            tempArrayValue.PushBack(static_cast<int>(item), doc.GetAllocator());
        }
        doc.AddMember("fourth_of_enums", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: fifthOfStructs) {
            rapidjson::Value tempFifthOfStructsObjectValue;
            tempFifthOfStructsObjectValue.SetObject();
            item.AddToRapidJsonObject(tempFifthOfStructsObjectValue, doc.GetAllocator());
            tempArrayValue.PushBack(tempFifthOfStructsObjectValue, doc.GetAllocator());
        }
        doc.AddMember("fifth_of_structs", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: sixthOfDatetimes) {
            rapidjson::Value tempSixthOfDatetimesStringValue;
            std::string itemIsoString = stinger::utils::timePointToIsoString(item);
            tempSixthOfDatetimesStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempSixthOfDatetimesStringValue, doc.GetAllocator());
        }
        doc.AddMember("sixth_of_datetimes", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: seventhOfDurations) {
            rapidjson::Value tempSeventhOfDurationsStringValue;
            std::string itemIsoString = stinger::utils::durationToIsoString(item);
            tempSeventhOfDurationsStringValue.SetString(itemIsoString.c_str(), itemIsoString.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempSeventhOfDurationsStringValue, doc.GetAllocator());
        }
        doc.AddMember("seventh_of_durations", tempArrayValue, doc.GetAllocator());
    }

    { // Restrict Scope for array serialization
        rapidjson::Value tempArrayValue;
        tempArrayValue.SetArray();
        for (const auto& item: eighthOfBinaries) {
            rapidjson::Value tempEighthOfBinariesStringValue;
            std::string itemB64String = stinger::utils::base64Encode(item);
            tempEighthOfBinariesStringValue.SetString(itemB64String.c_str(), itemB64String.size(), doc.GetAllocator());
            tempArrayValue.PushBack(tempEighthOfBinariesStringValue, doc.GetAllocator());
        }
        doc.AddMember("eighth_of_binaries", tempArrayValue, doc.GetAllocator());
    }
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["signal_name"] = "arrayOfEveryType";
    topicArgs["prefix"] = _prefixTopicParam;
    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/signal/arrayOfEveryType", topicArgs);
    auto msg = stinger::mqtt::Message::Signal(topic, buf.GetString());
    return _broker->Publish(msg);
}

void TestableServer::registerCallWithNothingHandler(std::function<void()> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callWithNothingHandler = func;
}

void TestableServer::registerCallOneIntegerHandler(std::function<int(int)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOneIntegerHandler = func;
}

void TestableServer::registerCallOptionalIntegerHandler(std::function<std::optional<int>(std::optional<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOptionalIntegerHandler = func;
}

void TestableServer::registerCallThreeIntegersHandler(std::function<CallThreeIntegersReturnValues(int, int, std::optional<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callThreeIntegersHandler = func;
}

void TestableServer::registerCallOneStringHandler(std::function<std::string(std::string)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOneStringHandler = func;
}

void TestableServer::registerCallOptionalStringHandler(std::function<std::optional<std::string>(std::optional<std::string>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOptionalStringHandler = func;
}

void TestableServer::registerCallThreeStringsHandler(std::function<CallThreeStringsReturnValues(std::string, std::optional<std::string>, std::string)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callThreeStringsHandler = func;
}

void TestableServer::registerCallOneEnumHandler(std::function<Numbers(Numbers)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOneEnumHandler = func;
}

void TestableServer::registerCallOptionalEnumHandler(std::function<std::optional<Numbers>(std::optional<Numbers>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOptionalEnumHandler = func;
}

void TestableServer::registerCallThreeEnumsHandler(std::function<CallThreeEnumsReturnValues(Numbers, Numbers, std::optional<Numbers>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callThreeEnumsHandler = func;
}

void TestableServer::registerCallOneStructHandler(std::function<AllTypes(AllTypes)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOneStructHandler = func;
}

void TestableServer::registerCallOptionalStructHandler(std::function<std::optional<AllTypes>(std::optional<AllTypes>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOptionalStructHandler = func;
}

void TestableServer::registerCallThreeStructsHandler(std::function<CallThreeStructsReturnValues(std::optional<AllTypes>, AllTypes, AllTypes)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callThreeStructsHandler = func;
}

void TestableServer::registerCallOneDateTimeHandler(std::function<std::chrono::time_point<std::chrono::system_clock>(std::chrono::time_point<std::chrono::system_clock>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOneDateTimeHandler = func;
}

void TestableServer::registerCallOptionalDateTimeHandler(std::function<std::optional<std::chrono::time_point<std::chrono::system_clock>>(std::optional<std::chrono::time_point<std::chrono::system_clock>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOptionalDateTimeHandler = func;
}

void TestableServer::registerCallThreeDateTimesHandler(std::function<CallThreeDateTimesReturnValues(std::chrono::time_point<std::chrono::system_clock>, std::chrono::time_point<std::chrono::system_clock>, std::optional<std::chrono::time_point<std::chrono::system_clock>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callThreeDateTimesHandler = func;
}

void TestableServer::registerCallOneDurationHandler(std::function<std::chrono::duration<double>(std::chrono::duration<double>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOneDurationHandler = func;
}

void TestableServer::registerCallOptionalDurationHandler(std::function<std::optional<std::chrono::duration<double>>(std::optional<std::chrono::duration<double>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOptionalDurationHandler = func;
}

void TestableServer::registerCallThreeDurationsHandler(std::function<CallThreeDurationsReturnValues(std::chrono::duration<double>, std::chrono::duration<double>, std::optional<std::chrono::duration<double>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callThreeDurationsHandler = func;
}

void TestableServer::registerCallOneBinaryHandler(std::function<std::vector<uint8_t>(std::vector<uint8_t>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOneBinaryHandler = func;
}

void TestableServer::registerCallOptionalBinaryHandler(std::function<std::optional<std::vector<uint8_t>>(std::optional<std::vector<uint8_t>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOptionalBinaryHandler = func;
}

void TestableServer::registerCallThreeBinariesHandler(std::function<CallThreeBinariesReturnValues(std::vector<uint8_t>, std::vector<uint8_t>, std::optional<std::vector<uint8_t>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callThreeBinariesHandler = func;
}

void TestableServer::registerCallOneListOfIntegersHandler(std::function<std::vector<int>(std::vector<int>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOneListOfIntegersHandler = func;
}

void TestableServer::registerCallOptionalListOfFloatsHandler(std::function<std::optional<std::vector<double>>(std::optional<std::vector<double>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callOptionalListOfFloatsHandler = func;
}

void TestableServer::registerCallTwoListsHandler(std::function<CallTwoListsReturnValues(std::vector<Numbers>, std::optional<std::vector<std::string>>)> func)
{
    _broker->Log(LOG_DEBUG, "Application registered a function to handle  method requests.");
    _callTwoListsHandler = func;
}

void TestableServer::_callCallWithNothingHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callWithNothing");
    if (!_callWithNothingHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    // Method doesn't have any return values.
    _callWithNothingHandler();
    auto returnValues = CallWithNothingReturnValues();

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOneIntegerHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneInteger");
    if (!_callOneIntegerHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneIntegerRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneIntegerHandler(requestArgs.input1);
    CallOneIntegerReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOptionalIntegerHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalInteger");
    if (!_callOptionalIntegerHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalIntegerRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalIntegerHandler(requestArgs.input1);
    CallOptionalIntegerReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallThreeIntegersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeIntegers");
    if (!_callThreeIntegersHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeIntegersRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeIntegersHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOneStringHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneString");
    if (!_callOneStringHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneStringRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneStringHandler(requestArgs.input1);
    CallOneStringReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOptionalStringHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalString");
    if (!_callOptionalStringHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalStringRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalStringHandler(requestArgs.input1);
    CallOptionalStringReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallThreeStringsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeStrings");
    if (!_callThreeStringsHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeStringsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeStringsHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOneEnumHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneEnum");
    if (!_callOneEnumHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneEnumRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneEnumHandler(requestArgs.input1);
    CallOneEnumReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOptionalEnumHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalEnum");
    if (!_callOptionalEnumHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalEnumRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalEnumHandler(requestArgs.input1);
    CallOptionalEnumReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallThreeEnumsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeEnums");
    if (!_callThreeEnumsHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeEnumsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeEnumsHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOneStructHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneStruct");
    if (!_callOneStructHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneStructRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneStructHandler(requestArgs.input1);
    CallOneStructReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOptionalStructHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalStruct");
    if (!_callOptionalStructHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalStructRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalStructHandler(requestArgs.input1);
    CallOptionalStructReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallThreeStructsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeStructs");
    if (!_callThreeStructsHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeStructsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeStructsHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOneDateTimeHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneDateTime");
    if (!_callOneDateTimeHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneDateTimeRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneDateTimeHandler(requestArgs.input1);
    CallOneDateTimeReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOptionalDateTimeHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalDateTime");
    if (!_callOptionalDateTimeHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalDateTimeRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalDateTimeHandler(requestArgs.input1);
    CallOptionalDateTimeReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallThreeDateTimesHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeDateTimes");
    if (!_callThreeDateTimesHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeDateTimesRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeDateTimesHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOneDurationHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneDuration");
    if (!_callOneDurationHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneDurationRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneDurationHandler(requestArgs.input1);
    CallOneDurationReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOptionalDurationHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalDuration");
    if (!_callOptionalDurationHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalDurationRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalDurationHandler(requestArgs.input1);
    CallOptionalDurationReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallThreeDurationsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeDurations");
    if (!_callThreeDurationsHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeDurationsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeDurationsHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOneBinaryHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneBinary");
    if (!_callOneBinaryHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneBinaryRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneBinaryHandler(requestArgs.input1);
    CallOneBinaryReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOptionalBinaryHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalBinary");
    if (!_callOptionalBinaryHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalBinaryRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalBinaryHandler(requestArgs.input1);
    CallOptionalBinaryReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallThreeBinariesHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callThreeBinaries");
    if (!_callThreeBinariesHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallThreeBinariesRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callThreeBinariesHandler(requestArgs.input1, requestArgs.input2, requestArgs.input3);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOneListOfIntegersHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOneListOfIntegers");
    if (!_callOneListOfIntegersHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOneListOfIntegersRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOneListOfIntegersHandler(requestArgs.input1);
    CallOneListOfIntegersReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallOptionalListOfFloatsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callOptionalListOfFloats");
    if (!_callOptionalListOfFloatsHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallOptionalListOfFloatsRequestArguments::FromRapidJsonObject(doc);

    // Method has a single return value.
    auto returnValue = _callOptionalListOfFloatsHandler(requestArgs.input1);
    CallOptionalListOfFloatsReturnValues returnValues = { returnValue };

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

void TestableServer::_callCallTwoListsHandler(
        const std::string& topic,
        const rapidjson::Document& doc,
        const std::optional<std::vector<std::byte>>& optCorrelationData,
        const std::optional<std::string>& optResponseTopic
) const
{
    _broker->Log(LOG_INFO, "Handling call to callTwoLists");
    if (!_callTwoListsHandler) {
        // TODO: publish an error response because we don't have a method handler.
        return;
    }

    auto requestArgs = CallTwoListsRequestArguments::FromRapidJsonObject(doc);

    // Method has multiple return values.
    auto returnValues = _callTwoListsHandler(requestArgs.input1, requestArgs.input2);

    if (optResponseTopic) {
        rapidjson::Document responseJson;
        responseJson.SetObject();

        returnValues.AddToRapidJsonObject(responseJson, responseJson.GetAllocator());

        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        responseJson.Accept(writer);

        auto msg = stinger::mqtt::Message::MethodResponse(*optResponseTopic, buf.GetString(), optCorrelationData, stinger::error::MethodReturnCode::SUCCESS);
        _broker->Publish(msg);
    }
}

std::optional<int> TestableServer::getReadWriteIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    if (_readWriteIntegerProperty) {
        return _readWriteIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
    _readWriteIntegerPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteIntegerProperty(int value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
        _readWriteIntegerProperty = ReadWriteIntegerProperty{ value };
        _lastReadWriteIntegerPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readWriteIntegerPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteIntegerProperty();
}

void TestableServer::republishReadWriteIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteIntegerProperty) {
        doc.SetObject();
        _readWriteIntegerProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_integer";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_integer/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteIntegerPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteIntegerPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_integer payload is not an object or null");
    }

    // TODO: Check _lastReadWriteIntegerPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteIntegerProperty tempValue = ReadWriteIntegerProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteIntegerPropertyMutex);
        _readWriteIntegerProperty = tempValue;
        _lastReadWriteIntegerPropertyVersion++;
    }
    republishReadWriteIntegerProperty();
}

std::optional<int> TestableServer::getReadOnlyIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    if (_readOnlyIntegerProperty) {
        return _readOnlyIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadOnlyIntegerPropertyCallback(const std::function<void(int value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
    _readOnlyIntegerPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadOnlyIntegerProperty(int value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
        _readOnlyIntegerProperty = ReadOnlyIntegerProperty{ value };
        _lastReadOnlyIntegerPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyIntegerPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadOnlyIntegerProperty();
}

void TestableServer::republishReadOnlyIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyIntegerProperty) {
        doc.SetObject();
        _readOnlyIntegerProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_only_integer";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_integer/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadOnlyIntegerPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadOnlyIntegerPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_only_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_only_integer payload is not an object or null");
    }

    // TODO: Check _lastReadOnlyIntegerPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadOnlyIntegerProperty tempValue = ReadOnlyIntegerProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyIntegerPropertyMutex);
        _readOnlyIntegerProperty = tempValue;
        _lastReadOnlyIntegerPropertyVersion++;
    }
    republishReadOnlyIntegerProperty();
}

std::optional<int> TestableServer::getReadWriteOptionalIntegerProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    if (_readWriteOptionalIntegerProperty) {
        return _readWriteOptionalIntegerProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteOptionalIntegerPropertyCallback(const std::function<void(std::optional<int> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
    _readWriteOptionalIntegerPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalIntegerProperty(std::optional<int> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
        _readWriteOptionalIntegerProperty = ReadWriteOptionalIntegerProperty{ value };
        _lastReadWriteOptionalIntegerPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalIntegerPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteOptionalIntegerProperty();
}

void TestableServer::republishReadWriteOptionalIntegerProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalIntegerProperty) {
        doc.SetObject();
        _readWriteOptionalIntegerProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_optional_integer";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_integer/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteOptionalIntegerPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteOptionalIntegerPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_integer property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_optional_integer payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalIntegerPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalIntegerProperty tempValue = ReadWriteOptionalIntegerProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalIntegerPropertyMutex);
        _readWriteOptionalIntegerProperty = tempValue;
        _lastReadWriteOptionalIntegerPropertyVersion++;
    }
    republishReadWriteOptionalIntegerProperty();
}

std::optional<ReadWriteTwoIntegersProperty> TestableServer::getReadWriteTwoIntegersProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
    if (_readWriteTwoIntegersProperty) {
        return *_readWriteTwoIntegersProperty;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteTwoIntegersPropertyCallback(const std::function<void(int first, std::optional<int> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
    _readWriteTwoIntegersPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoIntegersProperty(int first, std::optional<int> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
        _readWriteTwoIntegersProperty = ReadWriteTwoIntegersProperty{ first, second };
        _lastReadWriteTwoIntegersPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoIntegersPropertyCallbacks) {
            cb(first, second);
        }
    }
    republishReadWriteTwoIntegersProperty();
}

void TestableServer::republishReadWriteTwoIntegersProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoIntegersProperty) {
        doc.SetObject();
        _readWriteTwoIntegersProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_two_integers";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_integers/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteTwoIntegersPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteTwoIntegersPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_integers property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_two_integers payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoIntegersPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoIntegersProperty tempValue = ReadWriteTwoIntegersProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoIntegersPropertyMutex);
        _readWriteTwoIntegersProperty = tempValue;
        _lastReadWriteTwoIntegersPropertyVersion++;
    }
    republishReadWriteTwoIntegersProperty();
}

std::optional<std::string> TestableServer::getReadOnlyStringProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    if (_readOnlyStringProperty) {
        return _readOnlyStringProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadOnlyStringPropertyCallback(const std::function<void(std::string value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
    _readOnlyStringPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadOnlyStringProperty(std::string value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
        _readOnlyStringProperty = ReadOnlyStringProperty{ value };
        _lastReadOnlyStringPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyStringPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadOnlyStringProperty();
}

void TestableServer::republishReadOnlyStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyStringProperty) {
        doc.SetObject();
        _readOnlyStringProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_only_string";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_string/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadOnlyStringPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadOnlyStringPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_only_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_only_string payload is not an object or null");
    }

    // TODO: Check _lastReadOnlyStringPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadOnlyStringProperty tempValue = ReadOnlyStringProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyStringPropertyMutex);
        _readOnlyStringProperty = tempValue;
        _lastReadOnlyStringPropertyVersion++;
    }
    republishReadOnlyStringProperty();
}

std::optional<std::string> TestableServer::getReadWriteStringProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    if (_readWriteStringProperty) {
        return _readWriteStringProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteStringPropertyCallback(const std::function<void(std::string value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
    _readWriteStringPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteStringProperty(std::string value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
        _readWriteStringProperty = ReadWriteStringProperty{ value };
        _lastReadWriteStringPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyCallbacksMutex);
        for (const auto& cb: _readWriteStringPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteStringProperty();
}

void TestableServer::republishReadWriteStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteStringProperty) {
        doc.SetObject();
        _readWriteStringProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_string";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_string/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteStringPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteStringPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_string payload is not an object or null");
    }

    // TODO: Check _lastReadWriteStringPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteStringProperty tempValue = ReadWriteStringProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStringPropertyMutex);
        _readWriteStringProperty = tempValue;
        _lastReadWriteStringPropertyVersion++;
    }
    republishReadWriteStringProperty();
}

std::optional<std::string> TestableServer::getReadWriteOptionalStringProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    if (_readWriteOptionalStringProperty) {
        return _readWriteOptionalStringProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteOptionalStringPropertyCallback(const std::function<void(std::optional<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
    _readWriteOptionalStringPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalStringProperty(std::optional<std::string> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
        _readWriteOptionalStringProperty = ReadWriteOptionalStringProperty{ value };
        _lastReadWriteOptionalStringPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalStringPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteOptionalStringProperty();
}

void TestableServer::republishReadWriteOptionalStringProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalStringProperty) {
        doc.SetObject();
        _readWriteOptionalStringProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_optional_string";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_string/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteOptionalStringPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteOptionalStringPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_string property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_optional_string payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalStringPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalStringProperty tempValue = ReadWriteOptionalStringProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStringPropertyMutex);
        _readWriteOptionalStringProperty = tempValue;
        _lastReadWriteOptionalStringPropertyVersion++;
    }
    republishReadWriteOptionalStringProperty();
}

std::optional<ReadWriteTwoStringsProperty> TestableServer::getReadWriteTwoStringsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
    if (_readWriteTwoStringsProperty) {
        return *_readWriteTwoStringsProperty;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteTwoStringsPropertyCallback(const std::function<void(std::string first, std::optional<std::string> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
    _readWriteTwoStringsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoStringsProperty(std::string first, std::optional<std::string> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
        _readWriteTwoStringsProperty = ReadWriteTwoStringsProperty{ first, second };
        _lastReadWriteTwoStringsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoStringsPropertyCallbacks) {
            cb(first, second);
        }
    }
    republishReadWriteTwoStringsProperty();
}

void TestableServer::republishReadWriteTwoStringsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoStringsProperty) {
        doc.SetObject();
        _readWriteTwoStringsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_two_strings";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_strings/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteTwoStringsPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteTwoStringsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_strings property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_two_strings payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoStringsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoStringsProperty tempValue = ReadWriteTwoStringsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStringsPropertyMutex);
        _readWriteTwoStringsProperty = tempValue;
        _lastReadWriteTwoStringsPropertyVersion++;
    }
    republishReadWriteTwoStringsProperty();
}

std::optional<AllTypes> TestableServer::getReadWriteStructProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    if (_readWriteStructProperty) {
        return _readWriteStructProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteStructPropertyCallback(const std::function<void(AllTypes value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
    _readWriteStructPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteStructProperty(AllTypes value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
        _readWriteStructProperty = ReadWriteStructProperty{ value };
        _lastReadWriteStructPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyCallbacksMutex);
        for (const auto& cb: _readWriteStructPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteStructProperty();
}

void TestableServer::republishReadWriteStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteStructProperty) {
        doc.SetObject();
        _readWriteStructProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_struct";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_struct/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteStructPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteStructPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_struct property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_struct payload is not an object or null");
    }

    // TODO: Check _lastReadWriteStructPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteStructProperty tempValue = ReadWriteStructProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteStructPropertyMutex);
        _readWriteStructProperty = tempValue;
        _lastReadWriteStructPropertyVersion++;
    }
    republishReadWriteStructProperty();
}

std::optional<AllTypes> TestableServer::getReadWriteOptionalStructProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    if (_readWriteOptionalStructProperty) {
        return _readWriteOptionalStructProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteOptionalStructPropertyCallback(const std::function<void(std::optional<AllTypes> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
    _readWriteOptionalStructPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalStructProperty(std::optional<AllTypes> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
        _readWriteOptionalStructProperty = ReadWriteOptionalStructProperty{ value };
        _lastReadWriteOptionalStructPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalStructPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteOptionalStructProperty();
}

void TestableServer::republishReadWriteOptionalStructProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalStructProperty) {
        doc.SetObject();
        _readWriteOptionalStructProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_optional_struct";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_struct/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteOptionalStructPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteOptionalStructPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_struct property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_optional_struct payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalStructPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalStructProperty tempValue = ReadWriteOptionalStructProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalStructPropertyMutex);
        _readWriteOptionalStructProperty = tempValue;
        _lastReadWriteOptionalStructPropertyVersion++;
    }
    republishReadWriteOptionalStructProperty();
}

std::optional<ReadWriteTwoStructsProperty> TestableServer::getReadWriteTwoStructsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
    if (_readWriteTwoStructsProperty) {
        return *_readWriteTwoStructsProperty;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteTwoStructsPropertyCallback(const std::function<void(AllTypes first, std::optional<AllTypes> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
    _readWriteTwoStructsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoStructsProperty(AllTypes first, std::optional<AllTypes> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
        _readWriteTwoStructsProperty = ReadWriteTwoStructsProperty{ first, second };
        _lastReadWriteTwoStructsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoStructsPropertyCallbacks) {
            cb(first, second);
        }
    }
    republishReadWriteTwoStructsProperty();
}

void TestableServer::republishReadWriteTwoStructsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoStructsProperty) {
        doc.SetObject();
        _readWriteTwoStructsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_two_structs";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_structs/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteTwoStructsPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteTwoStructsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_structs property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_two_structs payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoStructsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoStructsProperty tempValue = ReadWriteTwoStructsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoStructsPropertyMutex);
        _readWriteTwoStructsProperty = tempValue;
        _lastReadWriteTwoStructsPropertyVersion++;
    }
    republishReadWriteTwoStructsProperty();
}

std::optional<Numbers> TestableServer::getReadOnlyEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    if (_readOnlyEnumProperty) {
        return _readOnlyEnumProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadOnlyEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
    _readOnlyEnumPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadOnlyEnumProperty(Numbers value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
        _readOnlyEnumProperty = ReadOnlyEnumProperty{ value };
        _lastReadOnlyEnumPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyCallbacksMutex);
        for (const auto& cb: _readOnlyEnumPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadOnlyEnumProperty();
}

void TestableServer::republishReadOnlyEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readOnlyEnumProperty) {
        doc.SetObject();
        _readOnlyEnumProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_only_enum";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_only_enum/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadOnlyEnumPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadOnlyEnumPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_only_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_only_enum payload is not an object or null");
    }

    // TODO: Check _lastReadOnlyEnumPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadOnlyEnumProperty tempValue = ReadOnlyEnumProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readOnlyEnumPropertyMutex);
        _readOnlyEnumProperty = tempValue;
        _lastReadOnlyEnumPropertyVersion++;
    }
    republishReadOnlyEnumProperty();
}

std::optional<Numbers> TestableServer::getReadWriteEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    if (_readWriteEnumProperty) {
        return _readWriteEnumProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteEnumPropertyCallback(const std::function<void(Numbers value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
    _readWriteEnumPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteEnumProperty(Numbers value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
        _readWriteEnumProperty = ReadWriteEnumProperty{ value };
        _lastReadWriteEnumPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyCallbacksMutex);
        for (const auto& cb: _readWriteEnumPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteEnumProperty();
}

void TestableServer::republishReadWriteEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteEnumProperty) {
        doc.SetObject();
        _readWriteEnumProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_enum";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_enum/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteEnumPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteEnumPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_enum payload is not an object or null");
    }

    // TODO: Check _lastReadWriteEnumPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteEnumProperty tempValue = ReadWriteEnumProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteEnumPropertyMutex);
        _readWriteEnumProperty = tempValue;
        _lastReadWriteEnumPropertyVersion++;
    }
    republishReadWriteEnumProperty();
}

std::optional<Numbers> TestableServer::getReadWriteOptionalEnumProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    if (_readWriteOptionalEnumProperty) {
        return _readWriteOptionalEnumProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteOptionalEnumPropertyCallback(const std::function<void(std::optional<Numbers> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
    _readWriteOptionalEnumPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalEnumProperty(std::optional<Numbers> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
        _readWriteOptionalEnumProperty = ReadWriteOptionalEnumProperty{ value };
        _lastReadWriteOptionalEnumPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalEnumPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteOptionalEnumProperty();
}

void TestableServer::republishReadWriteOptionalEnumProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalEnumProperty) {
        doc.SetObject();
        _readWriteOptionalEnumProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_optional_enum";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_enum/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteOptionalEnumPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteOptionalEnumPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_enum property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_optional_enum payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalEnumPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalEnumProperty tempValue = ReadWriteOptionalEnumProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalEnumPropertyMutex);
        _readWriteOptionalEnumProperty = tempValue;
        _lastReadWriteOptionalEnumPropertyVersion++;
    }
    republishReadWriteOptionalEnumProperty();
}

std::optional<ReadWriteTwoEnumsProperty> TestableServer::getReadWriteTwoEnumsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
    if (_readWriteTwoEnumsProperty) {
        return *_readWriteTwoEnumsProperty;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteTwoEnumsPropertyCallback(const std::function<void(Numbers first, std::optional<Numbers> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
    _readWriteTwoEnumsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoEnumsProperty(Numbers first, std::optional<Numbers> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
        _readWriteTwoEnumsProperty = ReadWriteTwoEnumsProperty{ first, second };
        _lastReadWriteTwoEnumsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoEnumsPropertyCallbacks) {
            cb(first, second);
        }
    }
    republishReadWriteTwoEnumsProperty();
}

void TestableServer::republishReadWriteTwoEnumsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoEnumsProperty) {
        doc.SetObject();
        _readWriteTwoEnumsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_two_enums";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_enums/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteTwoEnumsPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteTwoEnumsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_enums property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_two_enums payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoEnumsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoEnumsProperty tempValue = ReadWriteTwoEnumsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoEnumsPropertyMutex);
        _readWriteTwoEnumsProperty = tempValue;
        _lastReadWriteTwoEnumsPropertyVersion++;
    }
    republishReadWriteTwoEnumsProperty();
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> TestableServer::getReadWriteDatetimeProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    if (_readWriteDatetimeProperty) {
        return _readWriteDatetimeProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteDatetimePropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
    _readWriteDatetimePropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteDatetimeProperty(std::chrono::time_point<std::chrono::system_clock> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
        _readWriteDatetimeProperty = ReadWriteDatetimeProperty{ value };
        _lastReadWriteDatetimePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyCallbacksMutex);
        for (const auto& cb: _readWriteDatetimePropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteDatetimeProperty();
}

void TestableServer::republishReadWriteDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
    rapidjson::Document doc;
    if (_readWriteDatetimeProperty) {
        doc.SetObject();
        _readWriteDatetimeProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_datetime";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_datetime/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteDatetimePropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteDatetimePropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_datetime property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_datetime payload is not an object or null");
    }

    // TODO: Check _lastReadWriteDatetimePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteDatetimeProperty tempValue = ReadWriteDatetimeProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDatetimePropertyMutex);
        _readWriteDatetimeProperty = tempValue;
        _lastReadWriteDatetimePropertyVersion++;
    }
    republishReadWriteDatetimeProperty();
}

std::optional<std::chrono::time_point<std::chrono::system_clock>> TestableServer::getReadWriteOptionalDatetimeProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    if (_readWriteOptionalDatetimeProperty) {
        return _readWriteOptionalDatetimeProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteOptionalDatetimePropertyCallback(const std::function<void(std::optional<std::chrono::time_point<std::chrono::system_clock>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
    _readWriteOptionalDatetimePropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalDatetimeProperty(std::optional<std::chrono::time_point<std::chrono::system_clock>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
        _readWriteOptionalDatetimeProperty = ReadWriteOptionalDatetimeProperty{ value };
        _lastReadWriteOptionalDatetimePropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalDatetimePropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteOptionalDatetimeProperty();
}

void TestableServer::republishReadWriteOptionalDatetimeProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalDatetimeProperty) {
        doc.SetObject();
        _readWriteOptionalDatetimeProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_optional_datetime";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_datetime/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteOptionalDatetimePropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteOptionalDatetimePropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_datetime property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_optional_datetime payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalDatetimePropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalDatetimeProperty tempValue = ReadWriteOptionalDatetimeProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDatetimePropertyMutex);
        _readWriteOptionalDatetimeProperty = tempValue;
        _lastReadWriteOptionalDatetimePropertyVersion++;
    }
    republishReadWriteOptionalDatetimeProperty();
}

std::optional<ReadWriteTwoDatetimesProperty> TestableServer::getReadWriteTwoDatetimesProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
    if (_readWriteTwoDatetimesProperty) {
        return *_readWriteTwoDatetimesProperty;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteTwoDatetimesPropertyCallback(const std::function<void(std::chrono::time_point<std::chrono::system_clock> first, std::optional<std::chrono::time_point<std::chrono::system_clock>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
    _readWriteTwoDatetimesPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoDatetimesProperty(std::chrono::time_point<std::chrono::system_clock> first, std::optional<std::chrono::time_point<std::chrono::system_clock>> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
        _readWriteTwoDatetimesProperty = ReadWriteTwoDatetimesProperty{ first, second };
        _lastReadWriteTwoDatetimesPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoDatetimesPropertyCallbacks) {
            cb(first, second);
        }
    }
    republishReadWriteTwoDatetimesProperty();
}

void TestableServer::republishReadWriteTwoDatetimesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoDatetimesProperty) {
        doc.SetObject();
        _readWriteTwoDatetimesProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_two_datetimes";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_datetimes/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteTwoDatetimesPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteTwoDatetimesPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_datetimes property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_two_datetimes payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoDatetimesPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoDatetimesProperty tempValue = ReadWriteTwoDatetimesProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDatetimesPropertyMutex);
        _readWriteTwoDatetimesProperty = tempValue;
        _lastReadWriteTwoDatetimesPropertyVersion++;
    }
    republishReadWriteTwoDatetimesProperty();
}

std::optional<std::chrono::duration<double>> TestableServer::getReadWriteDurationProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    if (_readWriteDurationProperty) {
        return _readWriteDurationProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteDurationPropertyCallback(const std::function<void(std::chrono::duration<double> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
    _readWriteDurationPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteDurationProperty(std::chrono::duration<double> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
        _readWriteDurationProperty = ReadWriteDurationProperty{ value };
        _lastReadWriteDurationPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyCallbacksMutex);
        for (const auto& cb: _readWriteDurationPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteDurationProperty();
}

void TestableServer::republishReadWriteDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteDurationProperty) {
        doc.SetObject();
        _readWriteDurationProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_duration";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_duration/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteDurationPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteDurationPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_duration property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_duration payload is not an object or null");
    }

    // TODO: Check _lastReadWriteDurationPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteDurationProperty tempValue = ReadWriteDurationProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteDurationPropertyMutex);
        _readWriteDurationProperty = tempValue;
        _lastReadWriteDurationPropertyVersion++;
    }
    republishReadWriteDurationProperty();
}

std::optional<std::chrono::duration<double>> TestableServer::getReadWriteOptionalDurationProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    if (_readWriteOptionalDurationProperty) {
        return _readWriteOptionalDurationProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteOptionalDurationPropertyCallback(const std::function<void(std::optional<std::chrono::duration<double>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
    _readWriteOptionalDurationPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalDurationProperty(std::optional<std::chrono::duration<double>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
        _readWriteOptionalDurationProperty = ReadWriteOptionalDurationProperty{ value };
        _lastReadWriteOptionalDurationPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalDurationPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteOptionalDurationProperty();
}

void TestableServer::republishReadWriteOptionalDurationProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalDurationProperty) {
        doc.SetObject();
        _readWriteOptionalDurationProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_optional_duration";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_duration/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteOptionalDurationPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteOptionalDurationPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_duration property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_optional_duration payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalDurationPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalDurationProperty tempValue = ReadWriteOptionalDurationProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalDurationPropertyMutex);
        _readWriteOptionalDurationProperty = tempValue;
        _lastReadWriteOptionalDurationPropertyVersion++;
    }
    republishReadWriteOptionalDurationProperty();
}

std::optional<ReadWriteTwoDurationsProperty> TestableServer::getReadWriteTwoDurationsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
    if (_readWriteTwoDurationsProperty) {
        return *_readWriteTwoDurationsProperty;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteTwoDurationsPropertyCallback(const std::function<void(std::chrono::duration<double> first, std::optional<std::chrono::duration<double>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
    _readWriteTwoDurationsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoDurationsProperty(std::chrono::duration<double> first, std::optional<std::chrono::duration<double>> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
        _readWriteTwoDurationsProperty = ReadWriteTwoDurationsProperty{ first, second };
        _lastReadWriteTwoDurationsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoDurationsPropertyCallbacks) {
            cb(first, second);
        }
    }
    republishReadWriteTwoDurationsProperty();
}

void TestableServer::republishReadWriteTwoDurationsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoDurationsProperty) {
        doc.SetObject();
        _readWriteTwoDurationsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_two_durations";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_durations/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteTwoDurationsPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteTwoDurationsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_durations property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_two_durations payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoDurationsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoDurationsProperty tempValue = ReadWriteTwoDurationsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoDurationsPropertyMutex);
        _readWriteTwoDurationsProperty = tempValue;
        _lastReadWriteTwoDurationsPropertyVersion++;
    }
    republishReadWriteTwoDurationsProperty();
}

std::optional<std::vector<uint8_t>> TestableServer::getReadWriteBinaryProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    if (_readWriteBinaryProperty) {
        return _readWriteBinaryProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteBinaryPropertyCallback(const std::function<void(std::vector<uint8_t> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
    _readWriteBinaryPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteBinaryProperty(std::vector<uint8_t> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
        _readWriteBinaryProperty = ReadWriteBinaryProperty{ value };
        _lastReadWriteBinaryPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyCallbacksMutex);
        for (const auto& cb: _readWriteBinaryPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteBinaryProperty();
}

void TestableServer::republishReadWriteBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteBinaryProperty) {
        doc.SetObject();
        _readWriteBinaryProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_binary";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_binary/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteBinaryPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteBinaryPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_binary property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_binary payload is not an object or null");
    }

    // TODO: Check _lastReadWriteBinaryPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteBinaryProperty tempValue = ReadWriteBinaryProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteBinaryPropertyMutex);
        _readWriteBinaryProperty = tempValue;
        _lastReadWriteBinaryPropertyVersion++;
    }
    republishReadWriteBinaryProperty();
}

std::optional<std::vector<uint8_t>> TestableServer::getReadWriteOptionalBinaryProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    if (_readWriteOptionalBinaryProperty) {
        return _readWriteOptionalBinaryProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteOptionalBinaryPropertyCallback(const std::function<void(std::optional<std::vector<uint8_t>> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
    _readWriteOptionalBinaryPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteOptionalBinaryProperty(std::optional<std::vector<uint8_t>> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
        _readWriteOptionalBinaryProperty = ReadWriteOptionalBinaryProperty{ value };
        _lastReadWriteOptionalBinaryPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyCallbacksMutex);
        for (const auto& cb: _readWriteOptionalBinaryPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteOptionalBinaryProperty();
}

void TestableServer::republishReadWriteOptionalBinaryProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteOptionalBinaryProperty) {
        doc.SetObject();
        _readWriteOptionalBinaryProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_optional_binary";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_optional_binary/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteOptionalBinaryPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteOptionalBinaryPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_optional_binary property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_optional_binary payload is not an object or null");
    }

    // TODO: Check _lastReadWriteOptionalBinaryPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteOptionalBinaryProperty tempValue = ReadWriteOptionalBinaryProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteOptionalBinaryPropertyMutex);
        _readWriteOptionalBinaryProperty = tempValue;
        _lastReadWriteOptionalBinaryPropertyVersion++;
    }
    republishReadWriteOptionalBinaryProperty();
}

std::optional<ReadWriteTwoBinariesProperty> TestableServer::getReadWriteTwoBinariesProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
    if (_readWriteTwoBinariesProperty) {
        return *_readWriteTwoBinariesProperty;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteTwoBinariesPropertyCallback(const std::function<void(std::vector<uint8_t> first, std::optional<std::vector<uint8_t>> second)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
    _readWriteTwoBinariesPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteTwoBinariesProperty(std::vector<uint8_t> first, std::optional<std::vector<uint8_t>> second)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
        _readWriteTwoBinariesProperty = ReadWriteTwoBinariesProperty{ first, second };
        _lastReadWriteTwoBinariesPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyCallbacksMutex);
        for (const auto& cb: _readWriteTwoBinariesPropertyCallbacks) {
            cb(first, second);
        }
    }
    republishReadWriteTwoBinariesProperty();
}

void TestableServer::republishReadWriteTwoBinariesProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteTwoBinariesProperty) {
        doc.SetObject();
        _readWriteTwoBinariesProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_two_binaries";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_two_binaries/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteTwoBinariesPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteTwoBinariesPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_two_binaries property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_two_binaries payload is not an object or null");
    }

    // TODO: Check _lastReadWriteTwoBinariesPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteTwoBinariesProperty tempValue = ReadWriteTwoBinariesProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteTwoBinariesPropertyMutex);
        _readWriteTwoBinariesProperty = tempValue;
        _lastReadWriteTwoBinariesPropertyVersion++;
    }
    republishReadWriteTwoBinariesProperty();
}

std::optional<std::vector<std::string>> TestableServer::getReadWriteListOfStringsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
    if (_readWriteListOfStringsProperty) {
        return _readWriteListOfStringsProperty->value;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteListOfStringsPropertyCallback(const std::function<void(std::vector<std::string> value)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyCallbacksMutex);
    _readWriteListOfStringsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteListOfStringsProperty(std::vector<std::string> value)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
        _readWriteListOfStringsProperty = ReadWriteListOfStringsProperty{ value };
        _lastReadWriteListOfStringsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteListOfStringsPropertyCallbacks) {
            cb(value);
        }
    }
    republishReadWriteListOfStringsProperty();
}

void TestableServer::republishReadWriteListOfStringsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteListOfStringsProperty) {
        doc.SetObject();
        _readWriteListOfStringsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_list_of_strings";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_list_of_strings/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteListOfStringsPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteListOfStringsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_list_of_strings property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_list_of_strings payload is not an object or null");
    }

    // TODO: Check _lastReadWriteListOfStringsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 1 values into struct.
    ReadWriteListOfStringsProperty tempValue = ReadWriteListOfStringsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListOfStringsPropertyMutex);
        _readWriteListOfStringsProperty = tempValue;
        _lastReadWriteListOfStringsPropertyVersion++;
    }
    republishReadWriteListOfStringsProperty();
}

std::optional<ReadWriteListsProperty> TestableServer::getReadWriteListsProperty()
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
    if (_readWriteListsProperty) {
        return *_readWriteListsProperty;
    }
    return std::nullopt;
}

void TestableServer::registerReadWriteListsPropertyCallback(const std::function<void(std::vector<Numbers> theList, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList)>& cb)
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyCallbacksMutex);
    _readWriteListsPropertyCallbacks.push_back(cb);
}

void TestableServer::updateReadWriteListsProperty(std::vector<Numbers> theList, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList)
{
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
        _readWriteListsProperty = ReadWriteListsProperty{ theList, optionalList };
        _lastReadWriteListsPropertyVersion++;
    }
    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyCallbacksMutex);
        for (const auto& cb: _readWriteListsPropertyCallbacks) {
            cb(theList, optionalList);
        }
    }
    republishReadWriteListsProperty();
}

void TestableServer::republishReadWriteListsProperty() const
{
    std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
    rapidjson::Document doc;
    if (_readWriteListsProperty) {
        doc.SetObject();
        _readWriteListsProperty->AddToRapidJsonObject(doc, doc.GetAllocator());
    } else {
        doc.SetNull();
    }

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);

    std::map<std::string, std::string> topicArgs;
    topicArgs["service_id"] = _instanceId;
    topicArgs["interface_name"] = NAME;
    topicArgs["client_id"] = _broker->GetClientId();
    topicArgs["property_name"] = "read_write_lists";
    topicArgs["prefix"] = _prefixTopicParam;

    auto topic = stinger::utils::format("{prefix}/testable/{service_id}/property/read_write_lists/value", topicArgs);
    auto msg = stinger::mqtt::Message::PropertyValue(topic, buf.GetString(), _lastReadWriteListsPropertyVersion);
    _broker->Publish(msg);
}

void TestableServer::_receiveReadWriteListsPropertyUpdate(const stinger::mqtt::Message& msg)
{
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(msg.payload.c_str());
    if (!ok) {
        //Log("Could not JSON parse read_write_lists property update payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject() && !doc.IsNull()) {
        throw std::runtime_error("Received read_write_lists payload is not an object or null");
    }

    // TODO: Check _lastReadWriteListsPropertyVersion against optPropertyVersion and
    // reject the update if it's older than what we have.

    // Deserialize 2 values into struct.
    ReadWriteListsProperty tempValue = ReadWriteListsProperty::FromRapidJsonObject(doc);

    { // Scope lock
        std::lock_guard<std::mutex> lock(_readWriteListsPropertyMutex);
        _readWriteListsProperty = tempValue;
        _lastReadWriteListsPropertyVersion++;
    }
    republishReadWriteListsProperty();
}

void TestableServer::_advertisementThreadLoop()
{
    while (_advertisementThreadRunning) {
        // Get current timestamp
        auto now = std::chrono::system_clock::now();
        std::string timestamp = stinger::utils::timePointToIsoString(now);

        // Build JSON message
        rapidjson::Document doc;
        doc.SetObject();
        rapidjson::Document::AllocatorType& allocator = doc.GetAllocator();

        doc.AddMember("interface_name", rapidjson::Value("testable", allocator), allocator);
        doc.AddMember("instance", rapidjson::Value(_instanceId.c_str(), allocator), allocator);
        doc.AddMember("title", rapidjson::Value("Interface for testing", allocator), allocator);
        doc.AddMember("version", rapidjson::Value("0.0.1", allocator), allocator);
        doc.AddMember("connection_topic", rapidjson::Value(_broker->GetOnlineTopic().c_str(), allocator), allocator);
        doc.AddMember("timestamp", rapidjson::Value(timestamp.c_str(), allocator), allocator);

        doc.AddMember("prefix", rapidjson::Value(_prefixTopicParam.c_str(), allocator), allocator);

        // Convert to JSON string
        rapidjson::StringBuffer buf;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
        doc.Accept(writer);

        std::map<std::string, std::string> topicArgs;
        topicArgs["service_id"] = _instanceId;
        topicArgs["interface_name"] = NAME;
        topicArgs["client_id"] = _broker->GetClientId();
        topicArgs["prefix"] = _prefixTopicParam;

        // Publish to "{prefix}/testable/{service_id}/interface"
        std::string topic = stinger::utils::format("{prefix}/testable/{service_id}/interface", topicArgs);
        auto msg = stinger::mqtt::Message::ServiceOnline(topic, buf.GetString(), 120);
        _broker->Publish(msg);

        _broker->Log(LOG_INFO, "Published service advertisement to %s", topic.c_str());

        // Wait for 120 seconds or until thread should stop
        // Use smaller sleep intervals to allow quick shutdown
        for (int i = 0; i < 120 && _advertisementThreadRunning; ++i) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
}

} // namespace testable

} // namespace gen

} // namespace stinger
