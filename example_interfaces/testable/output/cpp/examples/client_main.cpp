

#include <iostream>
#include <sstream>
#include <syslog.h>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"
#include "discovery.hpp"

int main(int argc, char** argv)
{
    // Create a connection to the broker
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "Test Able-client-demo");
    conn->SetLogLevel(LOG_DEBUG);
    conn->SetLogFunction([](int level, const char* msg)
                         {
                             std::cout << "[" << level << "] " << msg << std::endl;
                         });

    // Discover a service ID for a Test Able service.
    std::string serviceId;
    { // restrict scope
        TestAbleDiscovery discovery(conn);
        auto serviceIdFut = discovery.GetSingleton();
        auto serviceIdFutStatus = serviceIdFut.wait_for(boost::chrono::seconds(15));
        if (serviceIdFutStatus == boost::future_status::timeout)
        {
            std::cerr << "Failed to discover service instance within timeout." << std::endl;
            return 1;
        }
        serviceId = serviceIdFut.get();
    }

    // Create the client object.
    TestAbleClient client(conn, serviceId);

    // Register callbacks for signals.
    client.registerEmptyCallback([]()
                                 {
                                     std::cout << "Received EMPTY signal: " << std::endl;
                                 });

    client.registerSingleIntCallback([](int value)
                                     {
                                         std::cout << "Received SINGLE_INT signal: " << "value=" << value << std::endl;
                                     });

    client.registerSingleOptionalIntCallback([](boost::optional<int> value)
                                             {
                                                 std::cout << "Received SINGLE_OPTIONAL_INT signal: " << "value=" << "None" << std::endl;
                                             });

    client.registerThreeIntegersCallback([](int first, int second, boost::optional<int> third)
                                         {
                                             std::cout << "Received THREE_INTEGERS signal: " << "first=" << first << " | " << "second=" << second << " | " << "third=" << "None" << std::endl;
                                         });

    client.registerSingleStringCallback([](const std::string& value)
                                        {
                                            std::cout << "Received SINGLE_STRING signal: " << "value=" << value << std::endl;
                                        });

    client.registerSingleOptionalStringCallback([](boost::optional<std::string> value)
                                                {
                                                    std::cout << "Received SINGLE_OPTIONAL_STRING signal: " << "value=" << "None" << std::endl;
                                                });

    client.registerThreeStringsCallback([](const std::string& first, const std::string& second, boost::optional<std::string> third)
                                        {
                                            std::cout << "Received THREE_STRINGS signal: " << "first=" << first << " | " << "second=" << second << " | " << "third=" << "None" << std::endl;
                                        });

    client.registerSingleEnumCallback([](boost::optional<Numbers> value)
                                      {
                                          std::cout << "Received SINGLE_ENUM signal: " << "value=" << "None" << std::endl;
                                      });

    client.registerSingleOptionalEnumCallback([](boost::optional<Numbers> value)
                                              {
                                                  std::cout << "Received SINGLE_OPTIONAL_ENUM signal: " << "value=" << "None" << std::endl;
                                              });

    client.registerThreeEnumsCallback([](Numbers first, Numbers second, boost::optional<Numbers> third)
                                      {
                                          std::cout << "Received THREE_ENUMS signal: " << "first=" << numbersStrings[static_cast<int>(first)] << " | " << "second=" << numbersStrings[static_cast<int>(second)] << " | " << "third=" << "None" << std::endl;
                                      });

    client.registerSingleStructCallback([](AllTypes value)
                                        {
                                            std::cout << "Received SINGLE_STRUCT signal: " << "value=" << value << std::endl;
                                        });

    client.registerSingleOptionalStructCallback([](AllTypes value)
                                                {
                                                    std::cout << "Received SINGLE_OPTIONAL_STRUCT signal: " << "value=" << "None" << std::endl;
                                                });

    client.registerThreeStructsCallback([](AllTypes first, AllTypes second, AllTypes third)
                                        {
                                            std::cout << "Received THREE_STRUCTS signal: " << "first=" << first << " | " << "second=" << second << " | " << "third=" << "None" << std::endl;
                                        });

    client.registerSingleDateTimeCallback([](std::chrono::time_point<std::chrono::system_clock> value)
                                          {
                                              std::string valueStr = timePointToIsoString(value);

                                              std::cout << "Received SINGLE_DATE_TIME signal: " << "value=" << valueStr << std::endl;
                                          });

    client.registerSingleOptionalDatetimeCallback([](boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)
                                                  {
                                                      if (value)
                                                      {
                                                          std::string valueStr = timePointToIsoString(*value);
                                                      }
                                                      else
                                                      {
                                                          std::string valueStr = "None";
                                                      }

                                                      std::cout << "Received SINGLE_OPTIONAL_DATETIME signal: " << "value=" << "None" << std::endl;
                                                  });

    client.registerThreeDateTimesCallback([](std::chrono::time_point<std::chrono::system_clock> first, std::chrono::time_point<std::chrono::system_clock> second, boost::optional<std::chrono::time_point<std::chrono::system_clock>> third)
                                          {
                                              std::string firstStr = timePointToIsoString(first);

                                              std::string secondStr = timePointToIsoString(second);

                                              if (third)
                                              {
                                                  std::string thirdStr = timePointToIsoString(*third);
                                              }
                                              else
                                              {
                                                  std::string thirdStr = "None";
                                              }

                                              std::cout << "Received THREE_DATE_TIMES signal: " << "first=" << firstStr << " | " << "second=" << secondStr << " | " << "third=" << "None" << std::endl;
                                          });

    client.registerSingleDurationCallback([](std::chrono::duration<double> value)
                                          {
                                              std::string valueStr = durationToIsoString(value);

                                              std::cout << "Received SINGLE_DURATION signal: " << "value=" << valueStr << std::endl;
                                          });

    client.registerSingleOptionalDurationCallback([](boost::optional<std::chrono::duration<double>> value)
                                                  {
                                                      std::string valueStr = durationToIsoString(value);

                                                      std::cout << "Received SINGLE_OPTIONAL_DURATION signal: " << "value=" << "None" << std::endl;
                                                  });

    client.registerThreeDurationsCallback([](std::chrono::duration<double> first, std::chrono::duration<double> second, boost::optional<std::chrono::duration<double>> third)
                                          {
                                              std::string firstStr = durationToIsoString(first);

                                              std::string secondStr = durationToIsoString(second);

                                              std::string thirdStr = durationToIsoString(third);

                                              std::cout << "Received THREE_DURATIONS signal: " << "first=" << firstStr << " | " << "second=" << secondStr << " | " << "third=" << "None" << std::endl;
                                          });

    client.registerSingleBinaryCallback([](std::vector<uint8_t> value)
                                        {
                                            std::string valueStr = "[Binary Data]";

                                            std::cout << "Received SINGLE_BINARY signal: " << "value=" << valueStr << std::endl;
                                        });

    client.registerSingleOptionalBinaryCallback([](boost::optional<std::vector<uint8_t>> value)
                                                {
                                                    std::string valueStr = "[Binary Data]";

                                                    std::cout << "Received SINGLE_OPTIONAL_BINARY signal: " << "value=" << "None" << std::endl;
                                                });

    client.registerThreeBinariesCallback([](std::vector<uint8_t> first, std::vector<uint8_t> second, boost::optional<std::vector<uint8_t>> third)
                                         {
                                             std::string firstStr = "[Binary Data]";

                                             std::string secondStr = "[Binary Data]";

                                             std::string thirdStr = "[Binary Data]";

                                             std::cout << "Received THREE_BINARIES signal: " << "first=" << firstStr << " | " << "second=" << secondStr << " | " << "third=" << "None" << std::endl;
                                         });

    // Register callbacks for property updates.
    client.registerReadWriteIntegerPropertyCallback([](int value)
                                                    {
                                                        std::cout << "Received update for read_write_integer property: " << "value=" << value /* unhandled arg type*/ << std::endl;
                                                    });

    client.registerReadOnlyIntegerPropertyCallback([](int value)
                                                   {
                                                       std::cout << "Received update for read_only_integer property: " << "value=" << value /* unhandled arg type*/ << std::endl;
                                                   });

    client.registerReadWriteOptionalIntegerPropertyCallback([](boost::optional<int> value)
                                                            {
                                                                std::cout << "Received update for read_write_optional_integer property: " << "value=" << "None" << std::endl;
                                                            });

    client.registerReadWriteTwoIntegersPropertyCallback([](int first, boost::optional<int> second)
                                                        {
                                                            std::cout << "Received update for read_write_two_integers property: " << "first=" << first /* unhandled arg type*/ << " | " << "second=" << "None" << std::endl;
                                                        });

    client.registerReadOnlyStringPropertyCallback([](const std::string& value)
                                                  {
                                                      std::cout << "Received update for read_only_string property: " << "value=" << value /* unhandled arg type*/ << std::endl;
                                                  });

    client.registerReadWriteStringPropertyCallback([](const std::string& value)
                                                   {
                                                       std::cout << "Received update for read_write_string property: " << "value=" << value /* unhandled arg type*/ << std::endl;
                                                   });

    client.registerReadWriteOptionalStringPropertyCallback([](boost::optional<std::string> value)
                                                           {
                                                               std::cout << "Received update for read_write_optional_string property: " << "value=" << "None" << std::endl;
                                                           });

    client.registerReadWriteTwoStringsPropertyCallback([](const std::string& first, boost::optional<std::string> second)
                                                       {
                                                           std::cout << "Received update for read_write_two_strings property: " << "first=" << first /* unhandled arg type*/ << " | " << "second=" << "None" << std::endl;
                                                       });

    client.registerReadWriteStructPropertyCallback([](AllTypes value)
                                                   {
                                                       std::cout << "Received update for read_write_struct property: " << "value=" << "[AllTypes object]"
                                                                 << std::endl;
                                                   });

    client.registerReadWriteOptionalStructPropertyCallback([](AllTypes value)
                                                           {
                                                               std::cout << "Received update for read_write_optional_struct property: " << "value=" << "None" << std::endl;
                                                           });

    client.registerReadWriteTwoStructsPropertyCallback([](AllTypes first, AllTypes second)
                                                       {
                                                           std::cout << "Received update for read_write_two_structs property: " << "first=" << "[AllTypes object]"
                                                                     << " | " << "second=" << "None" << std::endl;
                                                       });

    client.registerReadOnlyEnumPropertyCallback([](Numbers value)
                                                {
                                                    std::cout << "Received update for read_only_enum property: " << "value=" << numbersStrings[static_cast<int>(value)]
                                                              << std::endl;
                                                });

    client.registerReadWriteEnumPropertyCallback([](Numbers value)
                                                 {
                                                     std::cout << "Received update for read_write_enum property: " << "value=" << numbersStrings[static_cast<int>(value)]
                                                               << std::endl;
                                                 });

    client.registerReadWriteOptionalEnumPropertyCallback([](boost::optional<Numbers> value)
                                                         {
                                                             std::cout << "Received update for read_write_optional_enum property: " << "value=" << "None" << std::endl;
                                                         });

    client.registerReadWriteTwoEnumsPropertyCallback([](Numbers first, boost::optional<Numbers> second)
                                                     {
                                                         std::cout << "Received update for read_write_two_enums property: " << "first=" << numbersStrings[static_cast<int>(first)]
                                                                   << " | " << "second=" << "None" << std::endl;
                                                     });

    client.registerReadWriteDatetimePropertyCallback([](std::chrono::time_point<std::chrono::system_clock> value)
                                                     {
                                                         std::string valueStr = timePointToIsoString(value);

                                                         std::cout << "Received update for read_write_datetime property: " << "value=" << valueStr
                                                                   << std::endl;
                                                     });

    client.registerReadWriteOptionalDatetimePropertyCallback([](boost::optional<std::chrono::time_point<std::chrono::system_clock>> value)
                                                             {
                                                                 if (value)
                                                                 {
                                                                     std::string valueStr = timePointToIsoString(*value);
                                                                 }
                                                                 else
                                                                 {
                                                                     std::string valueStr = "None";
                                                                 }

                                                                 std::cout << "Received update for read_write_optional_datetime property: " << "value=" << "None" << std::endl;
                                                             });

    client.registerReadWriteTwoDatetimesPropertyCallback([](std::chrono::time_point<std::chrono::system_clock> first, boost::optional<std::chrono::time_point<std::chrono::system_clock>> second)
                                                         {
                                                             std::string firstStr = timePointToIsoString(first);

                                                             if (second)
                                                             {
                                                                 std::string secondStr = timePointToIsoString(*second);
                                                             }
                                                             else
                                                             {
                                                                 std::string secondStr = "None";
                                                             }

                                                             std::cout << "Received update for read_write_two_datetimes property: " << "first=" << firstStr
                                                                       << " | " << "second=" << "None" << std::endl;
                                                         });

    client.registerReadWriteDurationPropertyCallback([](std::chrono::duration<double> value)
                                                     {
                                                         std::string valueStr = durationToIsoString(value);

                                                         std::cout << "Received update for read_write_duration property: " << "value=" << valueStr << std::endl;
                                                     });

    client.registerReadWriteOptionalDurationPropertyCallback([](boost::optional<std::chrono::duration<double>> value)
                                                             {
                                                                 if (value)
                                                                 {
                                                                     std::string valueStr = durationToIsoString(*value);
                                                                 }
                                                                 else
                                                                 {
                                                                     std::string valueStr = "None";
                                                                 }

                                                                 std::cout << "Received update for read_write_optional_duration property: " << "value=" << "None" << std::endl;
                                                             });

    client.registerReadWriteTwoDurationsPropertyCallback([](std::chrono::duration<double> first, boost::optional<std::chrono::duration<double>> second)
                                                         {
                                                             std::string firstStr = durationToIsoString(first);

                                                             if (second)
                                                             {
                                                                 std::string secondStr = durationToIsoString(*second);
                                                             }
                                                             else
                                                             {
                                                                 std::string secondStr = "None";
                                                             }

                                                             std::cout << "Received update for read_write_two_durations property: " << "first=" << firstStr << " | " << "second=" << "None" << std::endl;
                                                         });

    client.registerReadWriteBinaryPropertyCallback([](std::vector<uint8_t> value)
                                                   {
                                                       std::cout << "Received update for read_write_binary property: " << "value=" << value /* unhandled arg type*/ << std::endl;
                                                   });

    client.registerReadWriteOptionalBinaryPropertyCallback([](boost::optional<std::vector<uint8_t>> value)
                                                           {
                                                               std::cout << "Received update for read_write_optional_binary property: " << "value=" << "None" << std::endl;
                                                           });

    client.registerReadWriteTwoBinariesPropertyCallback([](std::vector<uint8_t> first, boost::optional<std::vector<uint8_t>> second)
                                                        {
                                                            std::cout << "Received update for read_write_two_binaries property: " << "first=" << first /* unhandled arg type*/ << " | " << "second=" << "None" << std::endl;
                                                        });

    // Call each method with example values.
    std::cout << "Calling callWithNothing" << std::endl;
    auto callWithNothingResultFuture = client.callWithNothing();
    auto callWithNothingStatus = callWithNothingResultFuture.wait_for(boost::chrono::seconds(5));
    if (callWithNothingStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callWithNothing response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling callOneInteger" << std::endl;
    auto callOneIntegerResultFuture = client.callOneInteger(42);
    auto callOneIntegerStatus = callOneIntegerResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOneIntegerStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOneInteger response." << std::endl;
    }
    else
    {
        std::cout << "Result: Output1=" << callOneIntegerResultFuture.get() << std::endl;
    }
    std::cout << "Calling callOptionalInteger" << std::endl;
    auto callOptionalIntegerResultFuture = client.callOptionalInteger(42);
    auto callOptionalIntegerStatus = callOptionalIntegerResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOptionalIntegerStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOptionalInteger response." << std::endl;
    }
    else
    {
        std::cout << "Result: Output1=" << callOptionalIntegerResultFuture.get() << std::endl;
    }
    std::cout << "Calling callThreeIntegers" << std::endl;
    auto callThreeIntegersResultFuture = client.callThreeIntegers(42, 42, 42);
    auto callThreeIntegersStatus = callThreeIntegersResultFuture.wait_for(boost::chrono::seconds(5));
    if (callThreeIntegersStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callThreeIntegers response." << std::endl;
    }
    else
    {
        CallThreeIntegersReturnValue returnValue = callThreeIntegersResultFuture.get();
        std::cout << "Results:" << " output1=" << returnValue.output1 << " output2=" << returnValue.output2 << " output3=" << returnValue.output3 << std::endl;
    }
    std::cout << "Calling callOneString" << std::endl;
    auto callOneStringResultFuture = client.callOneString("apples");
    auto callOneStringStatus = callOneStringResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOneStringStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOneString response." << std::endl;
    }
    else
    {
        std::cout << "Result: Output1=" << callOneStringResultFuture.get() << std::endl;
    }
    std::cout << "Calling callOptionalString" << std::endl;
    auto callOptionalStringResultFuture = client.callOptionalString(boost::make_optional(std::string("apples")));
    auto callOptionalStringStatus = callOptionalStringResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOptionalStringStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOptionalString response." << std::endl;
    }
    else
    {
        std::cout << "Result: Output1=" << callOptionalStringResultFuture.get() << std::endl;
    }
    std::cout << "Calling callThreeStrings" << std::endl;
    auto callThreeStringsResultFuture = client.callThreeStrings("apples", "apples", boost::make_optional(std::string("apples")));
    auto callThreeStringsStatus = callThreeStringsResultFuture.wait_for(boost::chrono::seconds(5));
    if (callThreeStringsStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callThreeStrings response." << std::endl;
    }
    else
    {
        CallThreeStringsReturnValue returnValue = callThreeStringsResultFuture.get();
        std::cout << "Results:" << " output1=" << returnValue.output1 << " output2=" << returnValue.output2 << " output3=" << returnValue.output3 << std::endl;
    }
    std::cout << "Calling callOneEnum" << std::endl;
    auto callOneEnumResultFuture = client.callOneEnum(Numbers::ONE);
    auto callOneEnumStatus = callOneEnumResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOneEnumStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOneEnum response." << std::endl;
    }
    else
    {
        std::cout << "Result: Output1=" << numbersStrings[callOneEnumResultFuture.get()] << std::endl;
    }
    std::cout << "Calling callOptionalEnum" << std::endl;
    auto callOptionalEnumResultFuture = client.callOptionalEnum(Numbers::ONE);
    auto callOptionalEnumStatus = callOptionalEnumResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOptionalEnumStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOptionalEnum response." << std::endl;
    }
    else
    {
        std::cout << "Result: Output1=" << numbersStrings[callOptionalEnumResultFuture.get()] << std::endl;
    }
    std::cout << "Calling callThreeEnums" << std::endl;
    auto callThreeEnumsResultFuture = client.callThreeEnums(Numbers::ONE, Numbers::ONE, Numbers::ONE);
    auto callThreeEnumsStatus = callThreeEnumsResultFuture.wait_for(boost::chrono::seconds(5));
    if (callThreeEnumsStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callThreeEnums response." << std::endl;
    }
    else
    {
        CallThreeEnumsReturnValue returnValue = callThreeEnumsResultFuture.get();
        std::cout << "Results:" << " output1=" << numbersStrings[static_cast<int>(returnValue.output1)] << " output2=" << numbersStrings[static_cast<int>(returnValue.output2)] << " output3=" << numbersStrings[static_cast<int>(returnValue.output3)] << std::endl;
    }
    std::cout << "Calling callOneStruct" << std::endl;
    auto callOneStructResultFuture = client.callOneStruct({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
    auto callOneStructStatus = callOneStructResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOneStructStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOneStruct response." << std::endl;
    }
    else
    {
        AllTypes returnValue = callOneStructResultFuture.get();
        std::cout << "Results:" << " bool_=" << returnValue.bool_ << " int_=" << returnValue.int_ << " number=" << returnValue.number << " str=" << returnValue.str << " enum_=" << numbersStrings[static_cast<int>(returnValue.enum_)] << " date_and_time=" << timePointToIsoString(returnValue.date_and_time) << " time_duration=" << durationToIsoString(returnValue.time_duration) << " data=" << binaryToString(returnValue.data) << " OptionalInteger=" << returnValue.OptionalInteger << " OptionalString=" << returnValue.OptionalString << " OptionalEnum=" << numbersStrings[static_cast<int>(returnValue.OptionalEnum)] << " OptionalDateTime=" << timePointToIsoString(returnValue.OptionalDateTime) << " OptionalDuration=" << durationToIsoString(returnValue.OptionalDuration) << " OptionalBinary=" << binaryToString(returnValue.OptionalBinary) << std::endl;
    }
    std::cout << "Calling callOptionalStruct" << std::endl;
    auto callOptionalStructResultFuture = client.callOptionalStruct({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
    auto callOptionalStructStatus = callOptionalStructResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOptionalStructStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOptionalStruct response." << std::endl;
    }
    else
    {
        AllTypes returnValue = callOptionalStructResultFuture.get();
        std::cout << "Results:" << " bool_=" << returnValue.bool_ << " int_=" << returnValue.int_ << " number=" << returnValue.number << " str=" << returnValue.str << " enum_=" << numbersStrings[static_cast<int>(returnValue.enum_)] << " date_and_time=" << timePointToIsoString(returnValue.date_and_time) << " time_duration=" << durationToIsoString(returnValue.time_duration) << " data=" << binaryToString(returnValue.data) << " OptionalInteger=" << returnValue.OptionalInteger << " OptionalString=" << returnValue.OptionalString << " OptionalEnum=" << numbersStrings[static_cast<int>(returnValue.OptionalEnum)] << " OptionalDateTime=" << timePointToIsoString(returnValue.OptionalDateTime) << " OptionalDuration=" << durationToIsoString(returnValue.OptionalDuration) << " OptionalBinary=" << binaryToString(returnValue.OptionalBinary) << std::endl;
    }
    std::cout << "Calling callThreeStructs" << std::endl;
    auto callThreeStructsResultFuture = client.callThreeStructs({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
    auto callThreeStructsStatus = callThreeStructsResultFuture.wait_for(boost::chrono::seconds(5));
    if (callThreeStructsStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callThreeStructs response." << std::endl;
    }
    else
    {
        CallThreeStructsReturnValue returnValue = callThreeStructsResultFuture.get();
        std::cout << "Results:" << " output1=" << returnValue.output1 << " output2=" << returnValue.output2 << " output3=" << returnValue.output3 << std::endl;
    }
    std::cout << "Calling callOneDateTime" << std::endl;
    auto callOneDateTimeResultFuture = client.callOneDateTime(std::chrono::system_clock::now());
    auto callOneDateTimeStatus = callOneDateTimeResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOneDateTimeStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOneDateTime response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling callOptionalDateTime" << std::endl;
    auto callOptionalDateTimeResultFuture = client.callOptionalDateTime(std::chrono::system_clock::now());
    auto callOptionalDateTimeStatus = callOptionalDateTimeResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOptionalDateTimeStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOptionalDateTime response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling callThreeDateTimes" << std::endl;
    auto callThreeDateTimesResultFuture = client.callThreeDateTimes(std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now());
    auto callThreeDateTimesStatus = callThreeDateTimesResultFuture.wait_for(boost::chrono::seconds(5));
    if (callThreeDateTimesStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callThreeDateTimes response." << std::endl;
    }
    else
    {
        CallThreeDateTimesReturnValue returnValue = callThreeDateTimesResultFuture.get();
        std::cout << "Results:" << " output1=" << timePointToIsoString(returnValue.output1) << " output2=" << timePointToIsoString(returnValue.output2) << " output3=" << timePointToIsoString(returnValue.output3) << std::endl;
    }
    std::cout << "Calling callOneDuration" << std::endl;
    auto callOneDurationResultFuture = client.callOneDuration(std::chrono::duration<double>(3536));
    auto callOneDurationStatus = callOneDurationResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOneDurationStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOneDuration response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling callOptionalDuration" << std::endl;
    auto callOptionalDurationResultFuture = client.callOptionalDuration(std::chrono::duration<double>(3536));
    auto callOptionalDurationStatus = callOptionalDurationResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOptionalDurationStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOptionalDuration response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling callThreeDurations" << std::endl;
    auto callThreeDurationsResultFuture = client.callThreeDurations(std::chrono::duration<double>(3536), std::chrono::duration<double>(3536), std::chrono::duration<double>(3536));
    auto callThreeDurationsStatus = callThreeDurationsResultFuture.wait_for(boost::chrono::seconds(5));
    if (callThreeDurationsStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callThreeDurations response." << std::endl;
    }
    else
    {
        CallThreeDurationsReturnValue returnValue = callThreeDurationsResultFuture.get();
        std::cout << "Results:" << " output1=" << durationToIsoString(returnValue.output1) << " output2=" << durationToIsoString(returnValue.output2) << " output3=" << durationToIsoString(returnValue.output3) << std::endl;
    }
    std::cout << "Calling callOneBinary" << std::endl;
    auto callOneBinaryResultFuture = client.callOneBinary({ 101, 120, 97, 109, 112, 108, 101 });
    auto callOneBinaryStatus = callOneBinaryResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOneBinaryStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOneBinary response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling callOptionalBinary" << std::endl;
    auto callOptionalBinaryResultFuture = client.callOptionalBinary({ 101, 120, 97, 109, 112, 108, 101 });
    auto callOptionalBinaryStatus = callOptionalBinaryResultFuture.wait_for(boost::chrono::seconds(5));
    if (callOptionalBinaryStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callOptionalBinary response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling callThreeBinaries" << std::endl;
    auto callThreeBinariesResultFuture = client.callThreeBinaries({ 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 });
    auto callThreeBinariesStatus = callThreeBinariesResultFuture.wait_for(boost::chrono::seconds(5));
    if (callThreeBinariesStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for callThreeBinaries response." << std::endl;
    }
    else
    {
        CallThreeBinariesReturnValue returnValue = callThreeBinariesResultFuture.get();
        std::cout << "Results:" << " output1=" << binaryToString(returnValue.output1) << " output2=" << binaryToString(returnValue.output2) << " output3=" << binaryToString(returnValue.output3) << std::endl;
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        sleep(10);
    }

    return 0;
}