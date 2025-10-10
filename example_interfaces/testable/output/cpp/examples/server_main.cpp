
#include <iostream>
#include <syslog.h>
#include <thread>
#include <atomic>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "cpp-server-demo");
    conn->SetLogLevel(LOG_DEBUG);
    conn->SetLogFunction([](int level, const char* msg)
                         {
                             std::cout << "[" << level << "] " << msg << std::endl;
                         });

    auto server = std::make_shared<TestAbleServer>(conn, "cpp-server-demo:1");

    std::cout << "Setting initial value for property 'read_write_integer'.\n";
    server->updateReadWriteIntegerProperty(42);

    std::cout << "Setting initial value for property 'read_only_integer'.\n";
    server->updateReadOnlyIntegerProperty(42);

    std::cout << "Setting initial value for property 'read_write_optional_integer'.\n";
    server->updateReadWriteOptionalIntegerProperty(42);

    std::cout << "Setting initial value for property 'read_write_two_integers'.\n";
    server->updateReadWriteTwoIntegersProperty(42, 42);

    std::cout << "Setting initial value for property 'read_only_string'.\n";
    server->updateReadOnlyStringProperty("apples");

    std::cout << "Setting initial value for property 'read_write_string'.\n";
    server->updateReadWriteStringProperty("apples");

    std::cout << "Setting initial value for property 'read_write_optional_string'.\n";
    server->updateReadWriteOptionalStringProperty(boost::make_optional(std::string("apples")));

    std::cout << "Setting initial value for property 'read_write_two_strings'.\n";
    server->updateReadWriteTwoStringsProperty("apples", boost::make_optional(std::string("apples")));

    std::cout << "Setting initial value for property 'read_write_struct'.\n";
    server->updateReadWriteStructProperty({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });

    std::cout << "Setting initial value for property 'read_write_optional_struct'.\n";
    server->updateReadWriteOptionalStructProperty({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });

    std::cout << "Setting initial value for property 'read_write_two_structs'.\n";
    server->updateReadWriteTwoStructsProperty({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });

    std::cout << "Setting initial value for property 'read_only_enum'.\n";
    server->updateReadOnlyEnumProperty(Numbers::ONE);

    std::cout << "Setting initial value for property 'read_write_enum'.\n";
    server->updateReadWriteEnumProperty(Numbers::ONE);

    std::cout << "Setting initial value for property 'read_write_optional_enum'.\n";
    server->updateReadWriteOptionalEnumProperty(Numbers::ONE);

    std::cout << "Setting initial value for property 'read_write_two_enums'.\n";
    server->updateReadWriteTwoEnumsProperty(Numbers::ONE, Numbers::ONE);

    std::cout << "Setting initial value for property 'read_write_datetime'.\n";
    server->updateReadWriteDatetimeProperty(std::chrono::system_clock::now());

    std::cout << "Setting initial value for property 'read_write_optional_datetime'.\n";
    server->updateReadWriteOptionalDatetimeProperty(std::chrono::system_clock::now());

    std::cout << "Setting initial value for property 'read_write_two_datetimes'.\n";
    server->updateReadWriteTwoDatetimesProperty(std::chrono::system_clock::now(), std::chrono::system_clock::now());

    std::cout << "Setting initial value for property 'read_write_duration'.\n";
    server->updateReadWriteDurationProperty(std::chrono::duration<double>(3536));

    std::cout << "Setting initial value for property 'read_write_optional_duration'.\n";
    server->updateReadWriteOptionalDurationProperty(std::chrono::duration<double>(3536));

    std::cout << "Setting initial value for property 'read_write_two_durations'.\n";
    server->updateReadWriteTwoDurationsProperty(std::chrono::duration<double>(3536), std::chrono::duration<double>(3536));

    std::cout << "Setting initial value for property 'read_write_binary'.\n";
    server->updateReadWriteBinaryProperty({ 101, 120, 97, 109, 112, 108, 101 });

    std::cout << "Setting initial value for property 'read_write_optional_binary'.\n";
    server->updateReadWriteOptionalBinaryProperty({ 101, 120, 97, 109, 112, 108, 101 });

    std::cout << "Setting initial value for property 'read_write_two_binaries'.\n";
    server->updateReadWriteTwoBinariesProperty({ 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 });

    auto emptyFuture = server->emitEmptySignal();
    auto singleIntFuture = server->emitSingleIntSignal(42);
    auto singleOptionalIntFuture = server->emitSingleOptionalIntSignal(42);
    auto threeIntegersFuture = server->emitThreeIntegersSignal(42, 42, 42);
    auto singleStringFuture = server->emitSingleStringSignal("apples");
    auto singleOptionalStringFuture = server->emitSingleOptionalStringSignal(boost::make_optional(std::string("apples")));
    auto threeStringsFuture = server->emitThreeStringsSignal("apples", "apples", boost::make_optional(std::string("apples")));
    auto singleEnumFuture = server->emitSingleEnumSignal(Numbers::ONE);
    auto singleOptionalEnumFuture = server->emitSingleOptionalEnumSignal(Numbers::ONE);
    auto threeEnumsFuture = server->emitThreeEnumsSignal(Numbers::ONE, Numbers::ONE, Numbers::ONE);
    auto singleStructFuture = server->emitSingleStructSignal({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
    auto singleOptionalStructFuture = server->emitSingleOptionalStructSignal({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
    auto threeStructsFuture = server->emitThreeStructsSignal({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
    auto singleDateTimeFuture = server->emitSingleDateTimeSignal(std::chrono::system_clock::now());
    auto singleOptionalDatetimeFuture = server->emitSingleOptionalDatetimeSignal(std::chrono::system_clock::now());
    auto threeDateTimesFuture = server->emitThreeDateTimesSignal(std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now());
    auto singleDurationFuture = server->emitSingleDurationSignal(std::chrono::duration<double>(3536));
    auto singleOptionalDurationFuture = server->emitSingleOptionalDurationSignal(std::chrono::duration<double>(3536));
    auto threeDurationsFuture = server->emitThreeDurationsSignal(std::chrono::duration<double>(3536), std::chrono::duration<double>(3536), std::chrono::duration<double>(3536));
    auto singleBinaryFuture = server->emitSingleBinarySignal({ 101, 120, 97, 109, 112, 108, 101 });
    auto singleOptionalBinaryFuture = server->emitSingleOptionalBinarySignal({ 101, 120, 97, 109, 112, 108, 101 });
    auto threeBinariesFuture = server->emitThreeBinariesSignal({ 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 });
    emptyFuture.wait();
    singleIntFuture.wait();
    singleOptionalIntFuture.wait();
    threeIntegersFuture.wait();
    singleStringFuture.wait();
    singleOptionalStringFuture.wait();
    threeStringsFuture.wait();
    singleEnumFuture.wait();
    singleOptionalEnumFuture.wait();
    threeEnumsFuture.wait();
    singleStructFuture.wait();
    singleOptionalStructFuture.wait();
    threeStructsFuture.wait();
    singleDateTimeFuture.wait();
    singleOptionalDatetimeFuture.wait();
    threeDateTimesFuture.wait();
    singleDurationFuture.wait();
    singleOptionalDurationFuture.wait();
    threeDurationsFuture.wait();
    singleBinaryFuture.wait();
    singleOptionalBinaryFuture.wait();
    threeBinariesFuture.wait();
    server->registerCallWithNothingHandler([]() -> void
                                           {
                                               std::cout << "Received call for callWithNothing\n";
                                           });

    server->registerCallOneIntegerHandler([](int unused1) -> int
                                          {
                                              std::cout << "Received call for callOneInteger\n";
                                              return 42;
                                          });

    server->registerCallOptionalIntegerHandler([](boost::optional<int> unused1) -> boost::optional<int>
                                               {
                                                   std::cout << "Received call for callOptionalInteger\n";
                                                   return 42;
                                               });

    server->registerCallThreeIntegersHandler([](int unused1, int unused2, boost::optional<int> unused3) -> CallThreeIntegersReturnValue
                                             {
                                                 std::cout << "Received call for callThreeIntegers\n";
                                                 return CallThreeIntegersReturnValue{ 42, 42, 42 };
                                             });

    server->registerCallOneStringHandler([](const std::string& unused1) -> std::string
                                         {
                                             std::cout << "Received call for callOneString\n";
                                             return "apples";
                                         });

    server->registerCallOptionalStringHandler([](boost::optional<std::string> unused1) -> boost::optional<std::string>
                                              {
                                                  std::cout << "Received call for callOptionalString\n";
                                                  return boost::make_optional(std::string("apples"));
                                              });

    server->registerCallThreeStringsHandler([](const std::string& unused1, const std::string& unused2, boost::optional<std::string> unused3) -> CallThreeStringsReturnValue
                                            {
                                                std::cout << "Received call for callThreeStrings\n";
                                                return CallThreeStringsReturnValue{ "apples", "apples", boost::make_optional(std::string("apples")) };
                                            });

    server->registerCallOneEnumHandler([](Numbers unused1) -> Numbers
                                       {
                                           std::cout << "Received call for callOneEnum\n";
                                           return Numbers::ONE;
                                       });

    server->registerCallOptionalEnumHandler([](boost::optional<Numbers> unused1) -> boost::optional<Numbers>
                                            {
                                                std::cout << "Received call for callOptionalEnum\n";
                                                return Numbers::ONE;
                                            });

    server->registerCallThreeEnumsHandler([](Numbers unused1, Numbers unused2, boost::optional<Numbers> unused3) -> CallThreeEnumsReturnValue
                                          {
                                              std::cout << "Received call for callThreeEnums\n";
                                              return CallThreeEnumsReturnValue{ Numbers::ONE, Numbers::ONE, Numbers::ONE };
                                          });

    server->registerCallOneStructHandler([](AllTypes unused1) -> AllTypes
                                         {
                                             std::cout << "Received call for callOneStruct\n";
                                             return CallOneStructReturnValue{ { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } } };
                                         });

    server->registerCallOptionalStructHandler([](AllTypes unused1) -> boost::optional<AllTypes>
                                              {
                                                  std::cout << "Received call for callOptionalStruct\n";
                                                  return CallOptionalStructReturnValue{ { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } } };
                                              });

    server->registerCallThreeStructsHandler([](AllTypes unused1, AllTypes unused2, AllTypes unused3) -> CallThreeStructsReturnValue
                                            {
                                                std::cout << "Received call for callThreeStructs\n";
                                                return CallThreeStructsReturnValue{ { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } } };
                                            });

    server->registerCallOneDateTimeHandler([](std::chrono::time_point<std::chrono::system_clock> unused1) -> std::chrono::time_point<std::chrono::system_clock>
                                           {
                                               std::cout << "Received call for callOneDateTime\n";
                                               return std::chrono::system_clock::now();
                                           });

    server->registerCallOptionalDateTimeHandler([](boost::optional<std::chrono::time_point<std::chrono::system_clock>> unused1) -> boost::optional<std::chrono::time_point<std::chrono::system_clock>>
                                                {
                                                    std::cout << "Received call for callOptionalDateTime\n";
                                                    return std::chrono::system_clock::now();
                                                });

    server->registerCallThreeDateTimesHandler([](std::chrono::time_point<std::chrono::system_clock> unused1, std::chrono::time_point<std::chrono::system_clock> unused2, boost::optional<std::chrono::time_point<std::chrono::system_clock>> unused3) -> CallThreeDateTimesReturnValue
                                              {
                                                  std::cout << "Received call for callThreeDateTimes\n";
                                                  return CallThreeDateTimesReturnValue{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() };
                                              });

    server->registerCallOneDurationHandler([](std::chrono::duration<double> unused1) -> std::chrono::duration<double>
                                           {
                                               std::cout << "Received call for callOneDuration\n";
                                               return std::chrono::duration<double>(3536);
                                           });

    server->registerCallOptionalDurationHandler([](boost::optional<std::chrono::duration<double>> unused1) -> boost::optional<std::chrono::duration<double>>
                                                {
                                                    std::cout << "Received call for callOptionalDuration\n";
                                                    return std::chrono::duration<double>(3536);
                                                });

    server->registerCallThreeDurationsHandler([](std::chrono::duration<double> unused1, std::chrono::duration<double> unused2, boost::optional<std::chrono::duration<double>> unused3) -> CallThreeDurationsReturnValue
                                              {
                                                  std::cout << "Received call for callThreeDurations\n";
                                                  return CallThreeDurationsReturnValue{ std::chrono::duration<double>(3536), std::chrono::duration<double>(3536), std::chrono::duration<double>(3536) };
                                              });

    server->registerCallOneBinaryHandler([](std::vector<uint8_t> unused1) -> std::vector<uint8_t>
                                         {
                                             std::cout << "Received call for callOneBinary\n";
                                             return { 101, 120, 97, 109, 112, 108, 101 };
                                         });

    server->registerCallOptionalBinaryHandler([](boost::optional<std::vector<uint8_t>> unused1) -> boost::optional<std::vector<uint8_t>>
                                              {
                                                  std::cout << "Received call for callOptionalBinary\n";
                                                  return { 101, 120, 97, 109, 112, 108, 101 };
                                              });

    server->registerCallThreeBinariesHandler([](std::vector<uint8_t> unused1, std::vector<uint8_t> unused2, boost::optional<std::vector<uint8_t>> unused3) -> CallThreeBinariesReturnValue
                                             {
                                                 std::cout << "Received call for callThreeBinaries\n";
                                                 return CallThreeBinariesReturnValue{ { 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 } };
                                             });

    // Start a background thread that emits signals every 60 seconds.
    std::atomic<bool> keepRunning{ true };
    std::thread periodicEmitter([server, &keepRunning]()
                                {
                                    int loopCount = 0;
                                    while (keepRunning)
                                    {
                                        loopCount++;
                                        // Call emitTodayIsSignal; do not block forever waiting for publish
                                        try
                                        {
                                            auto emptyFuture = server->emitEmptySignal();
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleIntFuture = server->emitSingleIntSignal(42);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalIntFuture = server->emitSingleOptionalIntSignal(42);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeIntegersFuture = server->emitThreeIntegersSignal(42, 42, 42);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleStringFuture = server->emitSingleStringSignal("apples");
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalStringFuture = server->emitSingleOptionalStringSignal(boost::make_optional(std::string("apples")));
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeStringsFuture = server->emitThreeStringsSignal("apples", "apples", boost::make_optional(std::string("apples")));
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleEnumFuture = server->emitSingleEnumSignal(Numbers::ONE);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalEnumFuture = server->emitSingleOptionalEnumSignal(Numbers::ONE);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeEnumsFuture = server->emitThreeEnumsSignal(Numbers::ONE, Numbers::ONE, Numbers::ONE);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleStructFuture = server->emitSingleStructSignal({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalStructFuture = server->emitSingleOptionalStructSignal({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeStructsFuture = server->emitThreeStructsSignal({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleDateTimeFuture = server->emitSingleDateTimeSignal(std::chrono::system_clock::now());
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalDatetimeFuture = server->emitSingleOptionalDatetimeSignal(std::chrono::system_clock::now());
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeDateTimesFuture = server->emitThreeDateTimesSignal(std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now());
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleDurationFuture = server->emitSingleDurationSignal(std::chrono::duration<double>(3536));
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalDurationFuture = server->emitSingleOptionalDurationSignal(std::chrono::duration<double>(3536));
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeDurationsFuture = server->emitThreeDurationsSignal(std::chrono::duration<double>(3536), std::chrono::duration<double>(3536), std::chrono::duration<double>(3536));
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleBinaryFuture = server->emitSingleBinarySignal({ 101, 120, 97, 109, 112, 108, 101 });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalBinaryFuture = server->emitSingleOptionalBinarySignal({ 101, 120, 97, 109, 112, 108, 101 });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeBinariesFuture = server->emitThreeBinariesSignal({ 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            emptyFuture.wait();
                                            singleIntFuture.wait();
                                            singleOptionalIntFuture.wait();
                                            threeIntegersFuture.wait();
                                            singleStringFuture.wait();
                                            singleOptionalStringFuture.wait();
                                            threeStringsFuture.wait();
                                            singleEnumFuture.wait();
                                            singleOptionalEnumFuture.wait();
                                            threeEnumsFuture.wait();
                                            singleStructFuture.wait();
                                            singleOptionalStructFuture.wait();
                                            threeStructsFuture.wait();
                                            singleDateTimeFuture.wait();
                                            singleOptionalDatetimeFuture.wait();
                                            threeDateTimesFuture.wait();
                                            singleDurationFuture.wait();
                                            singleOptionalDurationFuture.wait();
                                            threeDurationsFuture.wait();
                                            singleBinaryFuture.wait();
                                            singleOptionalBinaryFuture.wait();
                                            threeBinariesFuture.wait();
                                        }
                                        catch (...)
                                        {
                                        }

                                        // Sleep in 1-second increments so we can stop quickly
                                        for (int i = 0; i < 38 && keepRunning; ++i)
                                        {
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                        }

                                        if (loopCount % 3 == 0)
                                        {
                                            std::cout << "Updating value for property 'read_write_integer'.\n";
                                            server->updateReadWriteIntegerProperty(42);

                                            std::cout << "Updating value for property 'read_only_integer'.\n";
                                            server->updateReadOnlyIntegerProperty(42);

                                            std::cout << "Updating value for property 'read_write_optional_integer'.\n";
                                            server->updateReadWriteOptionalIntegerProperty(42);

                                            std::cout << "Updating value for property 'read_write_two_integers'.\n";
                                            server->updateReadWriteTwoIntegersProperty(42, 42);

                                            std::cout << "Updating value for property 'read_only_string'.\n";
                                            server->updateReadOnlyStringProperty("apples");

                                            std::cout << "Updating value for property 'read_write_string'.\n";
                                            server->updateReadWriteStringProperty("apples");

                                            std::cout << "Updating value for property 'read_write_optional_string'.\n";
                                            server->updateReadWriteOptionalStringProperty(boost::make_optional(std::string("apples")));

                                            std::cout << "Updating value for property 'read_write_two_strings'.\n";
                                            server->updateReadWriteTwoStringsProperty("apples", boost::make_optional(std::string("apples")));

                                            std::cout << "Updating value for property 'read_write_struct'.\n";
                                            server->updateReadWriteStructProperty({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });

                                            std::cout << "Updating value for property 'read_write_optional_struct'.\n";
                                            server->updateReadWriteOptionalStructProperty({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });

                                            std::cout << "Updating value for property 'read_write_two_structs'.\n";
                                            server->updateReadWriteTwoStructsProperty({ true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } }, { true, 42, 3.14, "apples", Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 }, 42, boost::make_optional(std::string("apples")), Numbers::ONE, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 } });

                                            std::cout << "Updating value for property 'read_only_enum'.\n";
                                            server->updateReadOnlyEnumProperty(Numbers::ONE);

                                            std::cout << "Updating value for property 'read_write_enum'.\n";
                                            server->updateReadWriteEnumProperty(Numbers::ONE);

                                            std::cout << "Updating value for property 'read_write_optional_enum'.\n";
                                            server->updateReadWriteOptionalEnumProperty(Numbers::ONE);

                                            std::cout << "Updating value for property 'read_write_two_enums'.\n";
                                            server->updateReadWriteTwoEnumsProperty(Numbers::ONE, Numbers::ONE);

                                            std::cout << "Updating value for property 'read_write_datetime'.\n";
                                            server->updateReadWriteDatetimeProperty(std::chrono::system_clock::now());

                                            std::cout << "Updating value for property 'read_write_optional_datetime'.\n";
                                            server->updateReadWriteOptionalDatetimeProperty(std::chrono::system_clock::now());

                                            std::cout << "Updating value for property 'read_write_two_datetimes'.\n";
                                            server->updateReadWriteTwoDatetimesProperty(std::chrono::system_clock::now(), std::chrono::system_clock::now());

                                            std::cout << "Updating value for property 'read_write_duration'.\n";
                                            server->updateReadWriteDurationProperty(std::chrono::duration<double>(3536));

                                            std::cout << "Updating value for property 'read_write_optional_duration'.\n";
                                            server->updateReadWriteOptionalDurationProperty(std::chrono::duration<double>(3536));

                                            std::cout << "Updating value for property 'read_write_two_durations'.\n";
                                            server->updateReadWriteTwoDurationsProperty(std::chrono::duration<double>(3536), std::chrono::duration<double>(3536));

                                            std::cout << "Updating value for property 'read_write_binary'.\n";
                                            server->updateReadWriteBinaryProperty({ 101, 120, 97, 109, 112, 108, 101 });

                                            std::cout << "Updating value for property 'read_write_optional_binary'.\n";
                                            server->updateReadWriteOptionalBinaryProperty({ 101, 120, 97, 109, 112, 108, 101 });

                                            std::cout << "Updating value for property 'read_write_two_binaries'.\n";
                                            server->updateReadWriteTwoBinariesProperty({ 101, 120, 97, 109, 112, 108, 101 }, { 101, 120, 97, 109, 112, 108, 101 });
                                        }
                                    }
                                });

    std::cout << "Press ENTER to exit\n";
    std::cin.ignore();

    // Signal the emitter thread to stop and join it
    keepRunning = false;
    if (periodicEmitter.joinable())
    {
        periodicEmitter.join();
    }

    return 0;
}