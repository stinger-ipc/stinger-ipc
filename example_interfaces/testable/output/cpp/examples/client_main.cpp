

#include <iostream>
#include <sstream>
#include <syslog.h>
#include <chrono>
#include <thread>
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"
#include "discovery.hpp"
#include "enums.hpp"
#include "interface_exceptions.hpp"

int main(int argc, char** argv)
{
    // Create a connection to the broker
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "testable-client-demo");
    conn->SetLogLevel(LOG_DEBUG);
    conn->SetLogFunction([](int level, const char* msg)
                         {
                             std::cout << "[" << level << "] " << msg << std::endl;
                         });

    // Discover a service ID for a testable service.
    std::string serviceId;
    { // restrict scope
        TestableDiscovery discovery(conn);
        auto serviceIdFut = discovery.GetSingleton();
        auto serviceIdFutStatus = serviceIdFut.wait_for(std::chrono::seconds(15));
        if (serviceIdFutStatus == std::future_status::timeout) {
            std::cerr << "Failed to discover service instance within timeout." << std::endl;
            return 1;
        }
        serviceId = serviceIdFut.get();
    }

    // Create the client object.
    TestableClient client(conn, serviceId);

    // Register callbacks for signals.
    client.registerEmptyCallback([]()
                                 {
                                     std::cout << "Received EMPTY signal: "
                                               << std::endl;
                                 });

    client.registerSingleIntCallback([](int value)
                                     {
                                         std::cout << "Received SINGLE_INT signal: "
                                                   << "value=" << value << std::endl;
                                     });

    client.registerSingleOptionalIntCallback([](std::optional<int> value)
                                             {
                                                 std::cout << "Received SINGLE_OPTIONAL_INT signal: "
                                                           << "value=" << *value << std::endl;
                                             });

    client.registerThreeIntegersCallback([](int first, int second, std::optional<int> third)
                                         {
                                             std::cout << "Received THREE_INTEGERS signal: "
                                                       << "first=" << first << " | " << "second=" << second << " | " << "third=" << *third << std::endl;
                                         });

    client.registerSingleStringCallback([](std::string value)
                                        {
                                            std::cout << "Received SINGLE_STRING signal: "
                                                      << "value=" << value << std::endl;
                                        });

    client.registerSingleOptionalStringCallback([](std::optional<std::string> value)
                                                {
                                                    std::cout << "Received SINGLE_OPTIONAL_STRING signal: "
                                                              << "value=" << *value << std::endl;
                                                });

    client.registerThreeStringsCallback([](std::string first, std::string second, std::optional<std::string> third)
                                        {
                                            std::cout << "Received THREE_STRINGS signal: "
                                                      << "first=" << first << " | " << "second=" << second << " | " << "third=" << *third << std::endl;
                                        });

    client.registerSingleEnumCallback([](Numbers value)
                                      {
                                          std::cout << "Received SINGLE_ENUM signal: "
                                                    << "value=" << numbersStrings.at(static_cast<int>(value)) << std::endl;
                                      });

    client.registerSingleOptionalEnumCallback([](std::optional<Numbers> value)
                                              {
                                                  std::cout << "Received SINGLE_OPTIONAL_ENUM signal: "
                                                            << "value=" << numbersStrings.at(static_cast<int>(*value)) << std::endl;
                                              });

    client.registerThreeEnumsCallback([](Numbers first, Numbers second, std::optional<Numbers> third)
                                      {
                                          std::cout << "Received THREE_ENUMS signal: "
                                                    << "first=" << numbersStrings.at(static_cast<int>(first)) << " | " << "second=" << numbersStrings.at(static_cast<int>(second)) << " | " << "third=" << numbersStrings.at(static_cast<int>(*third)) << std::endl;
                                      });

    client.registerSingleStructCallback([](AllTypes value)
                                        {
                                            std::cout << "Received SINGLE_STRUCT signal: "
                                                      << "value=" << "[AllTypes object]"
                                                      << std::endl;
                                        });

    client.registerSingleOptionalStructCallback([](std::optional<AllTypes> value)
                                                {
                                                    std::cout << "Received SINGLE_OPTIONAL_STRUCT signal: "
                                                              << "value=" << "[AllTypes object]"
                                                              << std::endl;
                                                });

    client.registerThreeStructsCallback([](AllTypes first, AllTypes second, std::optional<AllTypes> third)
                                        {
                                            std::cout << "Received THREE_STRUCTS signal: "
                                                      << "first=" << "[AllTypes object]"
                                                      << " | " << "second=" << "[AllTypes object]"
                                                      << " | " << "third=" << "[AllTypes object]"
                                                      << std::endl;
                                        });

    client.registerSingleDateTimeCallback([](std::chrono::time_point<std::chrono::system_clock> value)
                                          {
                                              std::string valueStr = stinger::utils::timePointToIsoString(value);

                                              std::cout << "Received SINGLE_DATE_TIME signal: "
                                                        << "value=" << valueStr << std::endl;
                                          });

    client.registerSingleOptionalDatetimeCallback([](std::optional<std::chrono::time_point<std::chrono::system_clock>> value)
                                                  {
                                                      std::string valueStr = "None";
                                                      if (value) {
                                                          std::string valueStr = stinger::utils::timePointToIsoString(*value);
                                                      }

                                                      std::cout << "Received SINGLE_OPTIONAL_DATETIME signal: "
                                                                << "value=" << valueStr << std::endl;
                                                  });

    client.registerThreeDateTimesCallback([](std::chrono::time_point<std::chrono::system_clock> first, std::chrono::time_point<std::chrono::system_clock> second, std::optional<std::chrono::time_point<std::chrono::system_clock>> third)
                                          {
                                              std::string firstStr = stinger::utils::timePointToIsoString(first);

                                              std::string secondStr = stinger::utils::timePointToIsoString(second);

                                              std::string thirdStr = "None";
                                              if (third) {
                                                  std::string thirdStr = stinger::utils::timePointToIsoString(*third);
                                              }

                                              std::cout << "Received THREE_DATE_TIMES signal: "
                                                        << "first=" << firstStr << " | " << "second=" << secondStr << " | " << "third=" << thirdStr << std::endl;
                                          });

    client.registerSingleDurationCallback([](std::chrono::duration<double> value)
                                          {
                                              std::string valueStr = stinger::utils::durationToIsoString(value);

                                              std::cout << "Received SINGLE_DURATION signal: "
                                                        << "value=" << valueStr << std::endl;
                                          });

    client.registerSingleOptionalDurationCallback([](std::optional<std::chrono::duration<double>> value)
                                                  {
                                                      std::string valueStr = "None";
                                                      if (value) {
                                                          std::string valueStr = stinger::utils::durationToIsoString(*value);
                                                      }

                                                      std::cout << "Received SINGLE_OPTIONAL_DURATION signal: "
                                                                << "value=" << valueStr << std::endl;
                                                  });

    client.registerThreeDurationsCallback([](std::chrono::duration<double> first, std::chrono::duration<double> second, std::optional<std::chrono::duration<double>> third)
                                          {
                                              std::string firstStr = stinger::utils::durationToIsoString(first);
                                              std::string secondStr = stinger::utils::durationToIsoString(second);

                                              std::string thirdStr = "None";
                                              if (third) {
                                                  std::string thirdStr = stinger::utils::durationToIsoString(*third);
                                              }

                                              std::cout << "Received THREE_DURATIONS signal: "
                                                        << "first=" << firstStr << " | " << "second=" << secondStr << " | " << "third=" << thirdStr << std::endl;
                                          });

    client.registerSingleBinaryCallback([](std::vector<uint8_t> value)
                                        {
                                            std::string valueStr = "[Binary Data]";

                                            std::cout << "Received SINGLE_BINARY signal: "
                                                      << "value=" << valueStr << std::endl;
                                        });

    client.registerSingleOptionalBinaryCallback([](std::optional<std::vector<uint8_t>> value)
                                                {
                                                    std::string valueStr = "[Binary Data]";

                                                    std::cout << "Received SINGLE_OPTIONAL_BINARY signal: "
                                                              << "value=" << valueStr << std::endl;
                                                });

    client.registerThreeBinariesCallback([](std::vector<uint8_t> first, std::vector<uint8_t> second, std::optional<std::vector<uint8_t>> third)
                                         {
                                             std::string firstStr = "[Binary Data]";

                                             std::string secondStr = "[Binary Data]";

                                             std::string thirdStr = "[Binary Data]";

                                             std::cout << "Received THREE_BINARIES signal: "
                                                       << "first=" << firstStr << " | " << "second=" << secondStr << " | " << "third=" << thirdStr << std::endl;
                                         });

    client.registerSingleArrayOfIntegersCallback([](std::vector<int> values)
                                                 {
                                                     std::cout << "Received SINGLE_ARRAY_OF_INTEGERS signal: "
                                                               << "values=" << "[Array of " << values.size() << " PRIMITIVE values]" << std::endl;
                                                 });

    client.registerSingleOptionalArrayOfStringsCallback([](std::optional<std::vector<std::string>> values)
                                                        {
                                                            std::cout << "Received SINGLE_OPTIONAL_ARRAY_OF_STRINGS signal: "
                                                                      << "values=" << "[Array of " << values->size() << " PRIMITIVE values]" << std::endl;
                                                        });

    client.registerArrayOfEveryTypeCallback([](std::vector<int> firstOfIntegers, std::vector<double> secondOfFloats, std::vector<std::string> thirdOfStrings, std::vector<Numbers> fourthOfEnums, std::vector<Entry> fifthOfStructs, std::vector<std::chrono::time_point<std::chrono::system_clock>> sixthOfDatetimes, std::vector<std::chrono::duration<double>> seventhOfDurations, std::vector<std::vector<uint8_t>> eighthOfBinaries)
                                            {
                                                std::cout << "Received ARRAY_OF_EVERY_TYPE signal: "
                                                          << "first_of_integers=" << "[Array of " << firstOfIntegers.size() << " PRIMITIVE values]" << " | " << "second_of_floats=" << "[Array of " << secondOfFloats.size() << " PRIMITIVE values]" << " | " << "third_of_strings=" << "[Array of " << thirdOfStrings.size() << " PRIMITIVE values]" << " | " << "fourth_of_enums=" << "[Array of " << fourthOfEnums.size() << " ENUM values]" << " | " << "fifth_of_structs=" << "[Array of " << fifthOfStructs.size() << " STRUCT values]" << " | " << "sixth_of_datetimes=" << "[Array of " << sixthOfDatetimes.size() << " DATETIME values]" << " | " << "seventh_of_durations=" << "[Array of " << seventhOfDurations.size() << " DURATION values]" << " | " << "eighth_of_binaries=" << "[Array of " << eighthOfBinaries.size() << " BINARY values]" << std::endl;
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

    client.registerReadWriteOptionalIntegerPropertyCallback([](std::optional<int> value)
                                                            {
                                                                std::cout << "Received update for read_write_optional_integer property: " << "value=" << "None" << std::endl;
                                                            });

    client.registerReadWriteTwoIntegersPropertyCallback([](int first, std::optional<int> second)
                                                        {
                                                            std::cout << "Received update for read_write_two_integers property: " << "first=" << first /* unhandled arg type*/ << " | " << "second=" << "None" << std::endl;
                                                        });

    client.registerReadOnlyStringPropertyCallback([](std::string value)
                                                  {
                                                      std::cout << "Received update for read_only_string property: " << "value=" << value /* unhandled arg type*/ << std::endl;
                                                  });

    client.registerReadWriteStringPropertyCallback([](std::string value)
                                                   {
                                                       std::cout << "Received update for read_write_string property: " << "value=" << value /* unhandled arg type*/ << std::endl;
                                                   });

    client.registerReadWriteOptionalStringPropertyCallback([](std::optional<std::string> value)
                                                           {
                                                               std::cout << "Received update for read_write_optional_string property: " << "value=" << "None" << std::endl;
                                                           });

    client.registerReadWriteTwoStringsPropertyCallback([](std::string first, std::optional<std::string> second)
                                                       {
                                                           std::cout << "Received update for read_write_two_strings property: " << "first=" << first /* unhandled arg type*/ << " | " << "second=" << "None" << std::endl;
                                                       });

    client.registerReadWriteStructPropertyCallback([](AllTypes value)
                                                   {
                                                       std::cout << "Received update for read_write_struct property: " << "value=" << "[AllTypes object]"
                                                                 << std::endl;
                                                   });

    client.registerReadWriteOptionalStructPropertyCallback([](std::optional<AllTypes> value)
                                                           {
                                                               std::cout << "Received update for read_write_optional_struct property: " << "value=" << "None" << std::endl;
                                                           });

    client.registerReadWriteTwoStructsPropertyCallback([](AllTypes first, std::optional<AllTypes> second)
                                                       {
                                                           std::cout << "Received update for read_write_two_structs property: " << "first=" << "[AllTypes object]"
                                                                     << " | " << "second=" << "None" << std::endl;
                                                       });

    client.registerReadOnlyEnumPropertyCallback([](Numbers value)
                                                {
                                                    std::cout << "Received update for read_only_enum property: " << "value=" << numbersStrings.at(static_cast<int>(value))
                                                              << std::endl;
                                                });

    client.registerReadWriteEnumPropertyCallback([](Numbers value)
                                                 {
                                                     std::cout << "Received update for read_write_enum property: " << "value=" << numbersStrings.at(static_cast<int>(value))
                                                               << std::endl;
                                                 });

    client.registerReadWriteOptionalEnumPropertyCallback([](std::optional<Numbers> value)
                                                         {
                                                             std::cout << "Received update for read_write_optional_enum property: " << "value=" << "None" << std::endl;
                                                         });

    client.registerReadWriteTwoEnumsPropertyCallback([](Numbers first, std::optional<Numbers> second)
                                                     {
                                                         std::cout << "Received update for read_write_two_enums property: " << "first=" << numbersStrings.at(static_cast<int>(first))
                                                                   << " | " << "second=" << "None" << std::endl;
                                                     });

    client.registerReadWriteDatetimePropertyCallback([](std::chrono::time_point<std::chrono::system_clock> value)
                                                     {
                                                         std::string valueStr = stinger::utils::timePointToIsoString(value);

                                                         std::cout << "Received update for read_write_datetime property: " << "value=" << valueStr
                                                                   << std::endl;
                                                     });

    client.registerReadWriteOptionalDatetimePropertyCallback([](std::optional<std::chrono::time_point<std::chrono::system_clock>> value)
                                                             {
                                                                 std::string valueStr = "None";
                                                                 if (value) {
                                                                     std::string valueStr = stinger::utils::timePointToIsoString(*value);
                                                                 }

                                                                 std::cout << "Received update for read_write_optional_datetime property: " << "value=" << "None" << std::endl;
                                                             });

    client.registerReadWriteTwoDatetimesPropertyCallback([](std::chrono::time_point<std::chrono::system_clock> first, std::optional<std::chrono::time_point<std::chrono::system_clock>> second)
                                                         {
                                                             std::string firstStr = stinger::utils::timePointToIsoString(first);

                                                             std::string secondStr = "None";
                                                             if (second) {
                                                                 std::string secondStr = stinger::utils::timePointToIsoString(*second);
                                                             }

                                                             std::cout << "Received update for read_write_two_datetimes property: " << "first=" << firstStr
                                                                       << " | " << "second=" << "None" << std::endl;
                                                         });

    client.registerReadWriteDurationPropertyCallback([](std::chrono::duration<double> value)
                                                     {
                                                         std::string valueStr = stinger::utils::durationToIsoString(value);

                                                         std::cout << "Received update for read_write_duration property: " << "value=" << valueStr
                                                                   << std::endl;
                                                     });

    client.registerReadWriteOptionalDurationPropertyCallback([](std::optional<std::chrono::duration<double>> value)
                                                             {
                                                                 std::string valueStr = "None";
                                                                 if (value) {
                                                                     std::string valueStr = stinger::utils::durationToIsoString(*value);
                                                                 }

                                                                 std::cout << "Received update for read_write_optional_duration property: " << "value=" << "None" << std::endl;
                                                             });

    client.registerReadWriteTwoDurationsPropertyCallback([](std::chrono::duration<double> first, std::optional<std::chrono::duration<double>> second)
                                                         {
                                                             std::string firstStr = stinger::utils::durationToIsoString(first);

                                                             std::string secondStr = "None";
                                                             if (second) {
                                                                 std::string secondStr = stinger::utils::durationToIsoString(*second);
                                                             }

                                                             std::cout << "Received update for read_write_two_durations property: " << "first=" << firstStr
                                                                       << " | " << "second=" << "None" << std::endl;
                                                         });

    client.registerReadWriteBinaryPropertyCallback([](std::vector<uint8_t> value)
                                                   {
                                                       std::cout << "Received update for read_write_binary property: " << "value=" << "[BINARY DATA]"
                                                                 << std::endl;
                                                   });

    client.registerReadWriteOptionalBinaryPropertyCallback([](std::optional<std::vector<uint8_t>> value)
                                                           {
                                                               std::cout << "Received update for read_write_optional_binary property: " << "value=" << "None" << std::endl;
                                                           });

    client.registerReadWriteTwoBinariesPropertyCallback([](std::vector<uint8_t> first, std::optional<std::vector<uint8_t>> second)
                                                        {
                                                            std::cout << "Received update for read_write_two_binaries property: " << "first=" << "[BINARY DATA]"
                                                                      << " | " << "second=" << "None" << std::endl;
                                                        });

    client.registerReadWriteListOfStringsPropertyCallback([](std::vector<std::string> value)
                                                          {
                                                              std::cout << "Received update for read_write_list_of_strings property: " << "value=" << "[Array of " << value.size() << "PRIMITIVE values]" << std::endl;
                                                          });

    client.registerReadWriteListsPropertyCallback([](std::vector<Numbers> theList, std::optional<std::vector<std::chrono::time_point<std::chrono::system_clock>>> optionalList)
                                                  {
                                                      std::cout << "Received update for read_write_lists property: " << "the_list=" << "[Array of " << theList.size() << "ENUM values]" << " | " << "optionalList=" << "None" << std::endl;
                                                  });

    // Call each method with example values.

    // ----------------------METHOD CALL_WITH_NOTHING-----------------------------------------
    { // Restrict scope for the `callWithNothing` method call.
        std::cout << "CALLING CALL_WITH_NOTHING" << std::endl;
        auto callWithNothingResultFuture = client.callWithNothing();
        auto callWithNothingStatus = callWithNothingResultFuture.wait_for(std::chrono::seconds(5));
        if (callWithNothingStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_WITH_NOTHING response." << std::endl;
        } else {
            std::cout << "CALL_WITH_NOTHING Completed.  It has not return values." << std::endl;
        }
    }

    // ----------------------METHOD CALL_ONE_INTEGER-----------------------------------------
    { // Restrict scope for the `callOneInteger` method call.
        std::cout << "CALLING CALL_ONE_INTEGER" << std::endl;
        auto callOneIntegerResultFuture = client.callOneInteger(42);
        auto callOneIntegerStatus = callOneIntegerResultFuture.wait_for(std::chrono::seconds(5));
        if (callOneIntegerStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_ONE_INTEGER response." << std::endl;
        } else {
            int returnValue;
            bool success = false;
            try {
                returnValue = callOneIntegerResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_ONE_INTEGER Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_ONE_INTEGER Response: "
                          << " output1=" << returnValue << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_OPTIONAL_INTEGER-----------------------------------------
    { // Restrict scope for the `callOptionalInteger` method call.
        std::cout << "CALLING CALL_OPTIONAL_INTEGER" << std::endl;
        auto callOptionalIntegerResultFuture = client.callOptionalInteger(42);
        auto callOptionalIntegerStatus = callOptionalIntegerResultFuture.wait_for(std::chrono::seconds(5));
        if (callOptionalIntegerStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_OPTIONAL_INTEGER response." << std::endl;
        } else {
            std::optional<int> returnValue;
            bool success = false;
            try {
                returnValue = callOptionalIntegerResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_OPTIONAL_INTEGER Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_OPTIONAL_INTEGER Response: "
                          << " output1=";
                if (returnValue) {
                    std::cout << *returnValue;
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_THREE_INTEGERS-----------------------------------------
    { // Restrict scope for the `callThreeIntegers` method call.
        std::cout << "CALLING CALL_THREE_INTEGERS" << std::endl;
        auto callThreeIntegersResultFuture = client.callThreeIntegers(42, 42, 42);
        auto callThreeIntegersStatus = callThreeIntegersResultFuture.wait_for(std::chrono::seconds(5));
        if (callThreeIntegersStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_THREE_INTEGERS response." << std::endl;
        } else {
            CallThreeIntegersReturnValues returnValue;
            bool success = false;
            try {
                returnValue = callThreeIntegersResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_THREE_INTEGERS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_THREE_INTEGERS Response: "
                          << " output1=" << returnValue.output1 << " output2=" << returnValue.output2 << " output3=";
                if (returnValue.output3) {
                    std::cout << *returnValue.output3;
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_ONE_STRING-----------------------------------------
    { // Restrict scope for the `callOneString` method call.
        std::cout << "CALLING CALL_ONE_STRING" << std::endl;
        auto callOneStringResultFuture = client.callOneString("apples");
        auto callOneStringStatus = callOneStringResultFuture.wait_for(std::chrono::seconds(5));
        if (callOneStringStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_ONE_STRING response." << std::endl;
        } else {
            std::string returnValue;
            bool success = false;
            try {
                returnValue = callOneStringResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_ONE_STRING Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_ONE_STRING Response: "
                          << " output1=" << returnValue << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_OPTIONAL_STRING-----------------------------------------
    { // Restrict scope for the `callOptionalString` method call.
        std::cout << "CALLING CALL_OPTIONAL_STRING" << std::endl;
        auto callOptionalStringResultFuture = client.callOptionalString(std::make_optional(std::string("apples")));
        auto callOptionalStringStatus = callOptionalStringResultFuture.wait_for(std::chrono::seconds(5));
        if (callOptionalStringStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_OPTIONAL_STRING response." << std::endl;
        } else {
            std::optional<std::string> returnValue;
            bool success = false;
            try {
                returnValue = callOptionalStringResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_OPTIONAL_STRING Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_OPTIONAL_STRING Response: "
                          << " output1=";
                if (returnValue) {
                    std::cout << *returnValue;
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_THREE_STRINGS-----------------------------------------
    { // Restrict scope for the `callThreeStrings` method call.
        std::cout << "CALLING CALL_THREE_STRINGS" << std::endl;
        auto callThreeStringsResultFuture = client.callThreeStrings("apples", std::make_optional(std::string("apples")), "apples");
        auto callThreeStringsStatus = callThreeStringsResultFuture.wait_for(std::chrono::seconds(5));
        if (callThreeStringsStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_THREE_STRINGS response." << std::endl;
        } else {
            CallThreeStringsReturnValues returnValue;
            bool success = false;
            try {
                returnValue = callThreeStringsResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_THREE_STRINGS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_THREE_STRINGS Response: "
                          << " output1=" << returnValue.output1 << " output2=";
                if (returnValue.output2) {
                    std::cout << *returnValue.output2;
                } else {
                    std::cout << "None";
                }
                std::cout
                        << " output3=" << returnValue.output3 << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_ONE_ENUM-----------------------------------------
    { // Restrict scope for the `callOneEnum` method call.
        std::cout << "CALLING CALL_ONE_ENUM" << std::endl;
        auto callOneEnumResultFuture = client.callOneEnum(Numbers::ONE);
        auto callOneEnumStatus = callOneEnumResultFuture.wait_for(std::chrono::seconds(5));
        if (callOneEnumStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_ONE_ENUM response." << std::endl;
        } else {
            Numbers returnValue;
            bool success = false;
            try {
                returnValue = callOneEnumResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_ONE_ENUM Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_ONE_ENUM Response: "
                          << " output1=" << numbersStrings.at(static_cast<int>(returnValue)) << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_OPTIONAL_ENUM-----------------------------------------
    { // Restrict scope for the `callOptionalEnum` method call.
        std::cout << "CALLING CALL_OPTIONAL_ENUM" << std::endl;
        auto callOptionalEnumResultFuture = client.callOptionalEnum(Numbers::ONE);
        auto callOptionalEnumStatus = callOptionalEnumResultFuture.wait_for(std::chrono::seconds(5));
        if (callOptionalEnumStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_OPTIONAL_ENUM response." << std::endl;
        } else {
            std::optional<Numbers> returnValue;
            bool success = false;
            try {
                returnValue = callOptionalEnumResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_OPTIONAL_ENUM Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_OPTIONAL_ENUM Response: "
                          << " output1=";
                if (returnValue) {
                    std::cout << numbersStrings.at(static_cast<int>(*returnValue));
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_THREE_ENUMS-----------------------------------------
    { // Restrict scope for the `callThreeEnums` method call.
        std::cout << "CALLING CALL_THREE_ENUMS" << std::endl;
        auto callThreeEnumsResultFuture = client.callThreeEnums(Numbers::ONE, Numbers::ONE, Numbers::ONE);
        auto callThreeEnumsStatus = callThreeEnumsResultFuture.wait_for(std::chrono::seconds(5));
        if (callThreeEnumsStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_THREE_ENUMS response." << std::endl;
        } else {
            CallThreeEnumsReturnValues returnValue;
            bool success = false;
            try {
                returnValue = callThreeEnumsResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_THREE_ENUMS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_THREE_ENUMS Response: "
                          << " output1=" << numbersStrings.at(static_cast<int>(returnValue.output1)) << " output2=" << numbersStrings.at(static_cast<int>(returnValue.output2)) << " output3=";
                if (returnValue.output3) {
                    std::cout << numbersStrings.at(static_cast<int>(*returnValue.output3));
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_ONE_STRUCT-----------------------------------------
    { // Restrict scope for the `callOneStruct` method call.
        std::cout << "CALLING CALL_ONE_STRUCT" << std::endl;
        AllTypes input1Arg = AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } };
        auto callOneStructResultFuture = client.callOneStruct(input1Arg);
        auto callOneStructStatus = callOneStructResultFuture.wait_for(std::chrono::seconds(5));
        if (callOneStructStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_ONE_STRUCT response." << std::endl;
        } else {
            AllTypes returnValue;
            bool success = false;
            try {
                returnValue = callOneStructResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_ONE_STRUCT Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_ONE_STRUCT Response: "
                          << " output1=" << "[AllTypes object]" << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_OPTIONAL_STRUCT-----------------------------------------
    { // Restrict scope for the `callOptionalStruct` method call.
        std::cout << "CALLING CALL_OPTIONAL_STRUCT" << std::endl;
        AllTypes input1Arg = AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } };
        auto callOptionalStructResultFuture = client.callOptionalStruct(input1Arg);
        auto callOptionalStructStatus = callOptionalStructResultFuture.wait_for(std::chrono::seconds(5));
        if (callOptionalStructStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_OPTIONAL_STRUCT response." << std::endl;
        } else {
            std::optional<AllTypes> returnValue;
            bool success = false;
            try {
                returnValue = callOptionalStructResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_OPTIONAL_STRUCT Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_OPTIONAL_STRUCT Response: "
                          << " output1=";
                if (returnValue) {
                    std::cout << "[AllTypes object]";
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_THREE_STRUCTS-----------------------------------------
    { // Restrict scope for the `callThreeStructs` method call.
        std::cout << "CALLING CALL_THREE_STRUCTS" << std::endl;
        AllTypes input1Arg = AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } };

        AllTypes input2Arg = AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } };

        AllTypes input3Arg = AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } };
        auto callThreeStructsResultFuture = client.callThreeStructs(input1Arg, input2Arg, input3Arg);
        auto callThreeStructsStatus = callThreeStructsResultFuture.wait_for(std::chrono::seconds(5));
        if (callThreeStructsStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_THREE_STRUCTS response." << std::endl;
        } else {
            CallThreeStructsReturnValues returnValue;
            bool success = false;
            try {
                returnValue = callThreeStructsResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_THREE_STRUCTS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_THREE_STRUCTS Response: "
                          << " output1=";
                if (returnValue.output1) {
                    std::cout << "[AllTypes object]";
                } else {
                    std::cout << "None";
                }
                std::cout
                        << " output2=" << "[AllTypes object]" << " output3=" << "[AllTypes object]" << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_ONE_DATE_TIME-----------------------------------------
    { // Restrict scope for the `callOneDateTime` method call.
        std::cout << "CALLING CALL_ONE_DATE_TIME" << std::endl;
        auto callOneDateTimeResultFuture = client.callOneDateTime(std::chrono::system_clock::now());
        auto callOneDateTimeStatus = callOneDateTimeResultFuture.wait_for(std::chrono::seconds(5));
        if (callOneDateTimeStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_ONE_DATE_TIME response." << std::endl;
        } else {
            std::chrono::time_point<std::chrono::system_clock> returnValue;
            bool success = false;
            try {
                returnValue = callOneDateTimeResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_ONE_DATE_TIME Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_ONE_DATE_TIME Response: "
                          << " output1=" << stinger::utils::timePointToIsoString(returnValue) << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_OPTIONAL_DATE_TIME-----------------------------------------
    { // Restrict scope for the `callOptionalDateTime` method call.
        std::cout << "CALLING CALL_OPTIONAL_DATE_TIME" << std::endl;
        auto callOptionalDateTimeResultFuture = client.callOptionalDateTime(std::chrono::system_clock::now());
        auto callOptionalDateTimeStatus = callOptionalDateTimeResultFuture.wait_for(std::chrono::seconds(5));
        if (callOptionalDateTimeStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_OPTIONAL_DATE_TIME response." << std::endl;
        } else {
            std::optional<std::chrono::time_point<std::chrono::system_clock>> returnValue;
            bool success = false;
            try {
                returnValue = callOptionalDateTimeResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_OPTIONAL_DATE_TIME Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_OPTIONAL_DATE_TIME Response: "
                          << " output1=";
                if (returnValue) {
                    std::cout << stinger::utils::timePointToIsoString(*returnValue);
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_THREE_DATE_TIMES-----------------------------------------
    { // Restrict scope for the `callThreeDateTimes` method call.
        std::cout << "CALLING CALL_THREE_DATE_TIMES" << std::endl;
        auto callThreeDateTimesResultFuture = client.callThreeDateTimes(std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now());
        auto callThreeDateTimesStatus = callThreeDateTimesResultFuture.wait_for(std::chrono::seconds(5));
        if (callThreeDateTimesStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_THREE_DATE_TIMES response." << std::endl;
        } else {
            CallThreeDateTimesReturnValues returnValue;
            bool success = false;
            try {
                returnValue = callThreeDateTimesResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_THREE_DATE_TIMES Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_THREE_DATE_TIMES Response: "
                          << " output1=" << stinger::utils::timePointToIsoString(returnValue.output1) << " output2=" << stinger::utils::timePointToIsoString(returnValue.output2) << " output3=";
                if (returnValue.output3) {
                    std::cout << stinger::utils::timePointToIsoString(*returnValue.output3);
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_ONE_DURATION-----------------------------------------
    { // Restrict scope for the `callOneDuration` method call.
        std::cout << "CALLING CALL_ONE_DURATION" << std::endl;
        auto callOneDurationResultFuture = client.callOneDuration(std::chrono::duration<double>(3536));
        auto callOneDurationStatus = callOneDurationResultFuture.wait_for(std::chrono::seconds(5));
        if (callOneDurationStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_ONE_DURATION response." << std::endl;
        } else {
            std::chrono::duration<double> returnValue;
            bool success = false;
            try {
                returnValue = callOneDurationResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_ONE_DURATION Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_ONE_DURATION Response: "
                          << " output1=" << stinger::utils::durationToIsoString(returnValue) << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_OPTIONAL_DURATION-----------------------------------------
    { // Restrict scope for the `callOptionalDuration` method call.
        std::cout << "CALLING CALL_OPTIONAL_DURATION" << std::endl;
        auto callOptionalDurationResultFuture = client.callOptionalDuration(std::chrono::duration<double>(3536));
        auto callOptionalDurationStatus = callOptionalDurationResultFuture.wait_for(std::chrono::seconds(5));
        if (callOptionalDurationStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_OPTIONAL_DURATION response." << std::endl;
        } else {
            std::optional<std::chrono::duration<double>> returnValue;
            bool success = false;
            try {
                returnValue = callOptionalDurationResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_OPTIONAL_DURATION Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_OPTIONAL_DURATION Response: "
                          << " output1=";
                if (returnValue) {
                    std::cout << stinger::utils::durationToIsoString(*returnValue);
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_THREE_DURATIONS-----------------------------------------
    { // Restrict scope for the `callThreeDurations` method call.
        std::cout << "CALLING CALL_THREE_DURATIONS" << std::endl;
        auto callThreeDurationsResultFuture = client.callThreeDurations(std::chrono::duration<double>(3536), std::chrono::duration<double>(3536), std::chrono::duration<double>(3536));
        auto callThreeDurationsStatus = callThreeDurationsResultFuture.wait_for(std::chrono::seconds(5));
        if (callThreeDurationsStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_THREE_DURATIONS response." << std::endl;
        } else {
            CallThreeDurationsReturnValues returnValue;
            bool success = false;
            try {
                returnValue = callThreeDurationsResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_THREE_DURATIONS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_THREE_DURATIONS Response: "
                          << " output1=" << stinger::utils::durationToIsoString(returnValue.output1) << " output2=" << stinger::utils::durationToIsoString(returnValue.output2) << " output3=";
                if (returnValue.output3) {
                    std::cout << stinger::utils::durationToIsoString(*returnValue.output3);
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_ONE_BINARY-----------------------------------------
    { // Restrict scope for the `callOneBinary` method call.
        std::cout << "CALLING CALL_ONE_BINARY" << std::endl;
        auto callOneBinaryResultFuture = client.callOneBinary(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
        auto callOneBinaryStatus = callOneBinaryResultFuture.wait_for(std::chrono::seconds(5));
        if (callOneBinaryStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_ONE_BINARY response." << std::endl;
        } else {
            std::vector<uint8_t> returnValue;
            bool success = false;
            try {
                returnValue = callOneBinaryResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_ONE_BINARY Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_ONE_BINARY Response: "
                          << " output1=" << "[BINARY DATA]"
                          << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_OPTIONAL_BINARY-----------------------------------------
    { // Restrict scope for the `callOptionalBinary` method call.
        std::cout << "CALLING CALL_OPTIONAL_BINARY" << std::endl;
        auto callOptionalBinaryResultFuture = client.callOptionalBinary(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
        auto callOptionalBinaryStatus = callOptionalBinaryResultFuture.wait_for(std::chrono::seconds(5));
        if (callOptionalBinaryStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_OPTIONAL_BINARY response." << std::endl;
        } else {
            std::optional<std::vector<uint8_t>> returnValue;
            bool success = false;
            try {
                returnValue = callOptionalBinaryResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_OPTIONAL_BINARY Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_OPTIONAL_BINARY Response: "
                          << " output1=";
                if (returnValue) {
                    std::cout << "[BINARY DATA]";
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_THREE_BINARIES-----------------------------------------
    { // Restrict scope for the `callThreeBinaries` method call.
        std::cout << "CALLING CALL_THREE_BINARIES" << std::endl;
        auto callThreeBinariesResultFuture = client.callThreeBinaries(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
        auto callThreeBinariesStatus = callThreeBinariesResultFuture.wait_for(std::chrono::seconds(5));
        if (callThreeBinariesStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_THREE_BINARIES response." << std::endl;
        } else {
            CallThreeBinariesReturnValues returnValue;
            bool success = false;
            try {
                returnValue = callThreeBinariesResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_THREE_BINARIES Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_THREE_BINARIES Response: "
                          << " output1=" << "[BINARY DATA]"
                          << " output2=" << "[BINARY DATA]"
                          << " output3=";
                if (returnValue.output3) {
                    std::cout << "[BINARY DATA]";
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_ONE_LIST_OF_INTEGERS-----------------------------------------
    { // Restrict scope for the `callOneListOfIntegers` method call.
        std::cout << "CALLING CALL_ONE_LIST_OF_INTEGERS" << std::endl;
        auto callOneListOfIntegersResultFuture = client.callOneListOfIntegers(std::vector<int>{ 42, 2022, 2022 });
        auto callOneListOfIntegersStatus = callOneListOfIntegersResultFuture.wait_for(std::chrono::seconds(5));
        if (callOneListOfIntegersStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_ONE_LIST_OF_INTEGERS response." << std::endl;
        } else {
            std::vector<int> returnValue;
            bool success = false;
            try {
                returnValue = callOneListOfIntegersResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_ONE_LIST_OF_INTEGERS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_ONE_LIST_OF_INTEGERS Response: "
                          << " output1=" << "[Array of " << returnValue.size() << "PRIMITIVE values]" << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_OPTIONAL_LIST_OF_FLOATS-----------------------------------------
    { // Restrict scope for the `callOptionalListOfFloats` method call.
        std::cout << "CALLING CALL_OPTIONAL_LIST_OF_FLOATS" << std::endl;
        auto callOptionalListOfFloatsResultFuture = client.callOptionalListOfFloats(std::vector<double>{ 3.14, 1.0, 1.0 });
        auto callOptionalListOfFloatsStatus = callOptionalListOfFloatsResultFuture.wait_for(std::chrono::seconds(5));
        if (callOptionalListOfFloatsStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_OPTIONAL_LIST_OF_FLOATS response." << std::endl;
        } else {
            std::optional<std::vector<double>> returnValue;
            bool success = false;
            try {
                returnValue = callOptionalListOfFloatsResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_OPTIONAL_LIST_OF_FLOATS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_OPTIONAL_LIST_OF_FLOATS Response: "
                          << " output1=";
                if (returnValue) {
                    std::cout << (returnValue ? "[Array of PRIMITIVE values]" : "None");
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    // ----------------------METHOD CALL_TWO_LISTS-----------------------------------------
    { // Restrict scope for the `callTwoLists` method call.
        std::cout << "CALLING CALL_TWO_LISTS" << std::endl;
        auto callTwoListsResultFuture = client.callTwoLists(std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::string>{ "apples", "foo", "foo" });
        auto callTwoListsStatus = callTwoListsResultFuture.wait_for(std::chrono::seconds(5));
        if (callTwoListsStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for CALL_TWO_LISTS response." << std::endl;
        } else {
            CallTwoListsReturnValues returnValue;
            bool success = false;
            try {
                returnValue = callTwoListsResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "CALL_TWO_LISTS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "CALL_TWO_LISTS Response: "
                          << " output1=" << "[Array of " << returnValue.output1.size() << "ENUM values]" << " output2=";
                if (returnValue.output2) {
                    std::cout << (returnValue.output2 ? "[Array of PRIMITIVE values]" : "None");
                } else {
                    std::cout << "None";
                }
                std::cout
                        << std::endl;
            }
        }
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }

    return 0;
}