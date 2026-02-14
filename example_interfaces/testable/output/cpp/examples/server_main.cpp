
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

    auto server = std::make_shared<TestableServer>(conn, "cpp-server-demo:1");

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
    server->updateReadWriteOptionalStringProperty(std::make_optional(std::string("apples")));

    std::cout << "Setting initial value for property 'read_write_two_strings'.\n";
    server->updateReadWriteTwoStringsProperty("apples", std::make_optional(std::string("apples")));

    std::cout << "Setting initial value for property 'read_write_struct'.\n";
    server->updateReadWriteStructProperty(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });

    std::cout << "Setting initial value for property 'read_write_optional_struct'.\n";
    server->updateReadWriteOptionalStructProperty(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });

    std::cout << "Setting initial value for property 'read_write_two_structs'.\n";
    server->updateReadWriteTwoStructsProperty(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } }, AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });

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
    server->updateReadWriteBinaryProperty(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });

    std::cout << "Setting initial value for property 'read_write_optional_binary'.\n";
    server->updateReadWriteOptionalBinaryProperty(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });

    std::cout << "Setting initial value for property 'read_write_two_binaries'.\n";
    server->updateReadWriteTwoBinariesProperty(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });

    std::cout << "Setting initial value for property 'read_write_list_of_strings'.\n";
    server->updateReadWriteListOfStringsProperty(std::vector<std::string>{ "apples", "foo", "foo" });

    std::cout << "Setting initial value for property 'read_write_lists'.\n";
    server->updateReadWriteListsProperty(std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() });

    auto emptyFuture = server->emitEmptySignal();
    auto singleIntFuture = server->emitSingleIntSignal(42);
    auto singleOptionalIntFuture = server->emitSingleOptionalIntSignal(42);
    auto threeIntegersFuture = server->emitThreeIntegersSignal(42, 42, 42);
    auto singleStringFuture = server->emitSingleStringSignal("apples");
    auto singleOptionalStringFuture = server->emitSingleOptionalStringSignal(std::make_optional(std::string("apples")));
    auto threeStringsFuture = server->emitThreeStringsSignal("apples", "apples", std::make_optional(std::string("apples")));
    auto singleEnumFuture = server->emitSingleEnumSignal(Numbers::ONE);
    auto singleOptionalEnumFuture = server->emitSingleOptionalEnumSignal(Numbers::ONE);
    auto threeEnumsFuture = server->emitThreeEnumsSignal(Numbers::ONE, Numbers::ONE, Numbers::ONE);
    auto singleStructFuture = server->emitSingleStructSignal(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });
    auto singleOptionalStructFuture = server->emitSingleOptionalStructSignal(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });
    auto threeStructsFuture = server->emitThreeStructsSignal(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } }, AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } }, AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });
    auto singleDateTimeFuture = server->emitSingleDateTimeSignal(std::chrono::system_clock::now());
    auto singleOptionalDatetimeFuture = server->emitSingleOptionalDatetimeSignal(std::chrono::system_clock::now());
    auto threeDateTimesFuture = server->emitThreeDateTimesSignal(std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now());
    auto singleDurationFuture = server->emitSingleDurationSignal(std::chrono::duration<double>(3536));
    auto singleOptionalDurationFuture = server->emitSingleOptionalDurationSignal(std::chrono::duration<double>(3536));
    auto threeDurationsFuture = server->emitThreeDurationsSignal(std::chrono::duration<double>(3536), std::chrono::duration<double>(3536), std::chrono::duration<double>(3536));
    auto singleBinaryFuture = server->emitSingleBinarySignal(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
    auto singleOptionalBinaryFuture = server->emitSingleOptionalBinarySignal(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
    auto threeBinariesFuture = server->emitThreeBinariesSignal(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
    auto singleArrayOfIntegersFuture = server->emitSingleArrayOfIntegersSignal(std::vector<int>{ 42, 2022, 2022 });
    auto singleOptionalArrayOfStringsFuture = server->emitSingleOptionalArrayOfStringsSignal(std::vector<std::string>{ "apples", "foo", "foo" });
    auto arrayOfEveryTypeFuture = server->emitArrayOfEveryTypeSignal(std::vector<int>{ 42, 2022, 2022 }, std::vector<double>{ 3.14, 1.0, 1.0 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } });
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
    singleArrayOfIntegersFuture.wait();
    singleOptionalArrayOfStringsFuture.wait();
    arrayOfEveryTypeFuture.wait();
    server->registerCallWithNothingHandler([]() -> void
                                           {
                                               std::cout << "Received call for callWithNothing\n";
                                           });

    server->registerCallOneIntegerHandler([](int unused1) -> int
                                          {
                                              std::cout << "Received call for callOneInteger\n";
                                              return 42;
                                          });

    server->registerCallOptionalIntegerHandler([](std::optional<int> unused1) -> std::optional<int>
                                               {
                                                   std::cout << "Received call for callOptionalInteger\n";
                                                   return 42;
                                               });

    server->registerCallThreeIntegersHandler([](int unused1, int unused2, std::optional<int> unused3) -> CallThreeIntegersReturnValues
                                             {
                                                 std::cout << "Received call for callThreeIntegers\n";
                                                 return CallThreeIntegersReturnValues{ 42, 42, 42 };
                                             });

    server->registerCallOneStringHandler([](std::string unused1) -> std::string
                                         {
                                             std::cout << "Received call for callOneString\n";
                                             return "apples";
                                         });

    server->registerCallOptionalStringHandler([](std::optional<std::string> unused1) -> std::optional<std::string>
                                              {
                                                  std::cout << "Received call for callOptionalString\n";
                                                  return std::make_optional(std::string("apples"));
                                              });

    server->registerCallThreeStringsHandler([](std::string unused1, std::optional<std::string> unused2, std::string unused3) -> CallThreeStringsReturnValues
                                            {
                                                std::cout << "Received call for callThreeStrings\n";
                                                return CallThreeStringsReturnValues{ "apples", std::make_optional(std::string("apples")), "apples" };
                                            });

    server->registerCallOneEnumHandler([](Numbers unused1) -> Numbers
                                       {
                                           std::cout << "Received call for callOneEnum\n";
                                           return Numbers::ONE;
                                       });

    server->registerCallOptionalEnumHandler([](std::optional<Numbers> unused1) -> std::optional<Numbers>
                                            {
                                                std::cout << "Received call for callOptionalEnum\n";
                                                return Numbers::ONE;
                                            });

    server->registerCallThreeEnumsHandler([](Numbers unused1, Numbers unused2, std::optional<Numbers> unused3) -> CallThreeEnumsReturnValues
                                          {
                                              std::cout << "Received call for callThreeEnums\n";
                                              return CallThreeEnumsReturnValues{ Numbers::ONE, Numbers::ONE, Numbers::ONE };
                                          });

    server->registerCallOneStructHandler([](AllTypes unused1) -> AllTypes
                                         {
                                             std::cout << "Received call for callOneStruct\n";
                                             return AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } };
                                         });

    server->registerCallOptionalStructHandler([](std::optional<AllTypes> unused1) -> std::optional<AllTypes>
                                              {
                                                  std::cout << "Received call for callOptionalStruct\n";
                                                  return AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } };
                                              });

    server->registerCallThreeStructsHandler([](std::optional<AllTypes> unused1, AllTypes unused2, AllTypes unused3) -> CallThreeStructsReturnValues
                                            {
                                                std::cout << "Received call for callThreeStructs\n";
                                                return CallThreeStructsReturnValues{ AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } }, AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } }, AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } } };
                                            });

    server->registerCallOneDateTimeHandler([](std::chrono::time_point<std::chrono::system_clock> unused1) -> std::chrono::time_point<std::chrono::system_clock>
                                           {
                                               std::cout << "Received call for callOneDateTime\n";
                                               return std::chrono::system_clock::now();
                                           });

    server->registerCallOptionalDateTimeHandler([](std::optional<std::chrono::time_point<std::chrono::system_clock>> unused1) -> std::optional<std::chrono::time_point<std::chrono::system_clock>>
                                                {
                                                    std::cout << "Received call for callOptionalDateTime\n";
                                                    return std::chrono::system_clock::now();
                                                });

    server->registerCallThreeDateTimesHandler([](std::chrono::time_point<std::chrono::system_clock> unused1, std::chrono::time_point<std::chrono::system_clock> unused2, std::optional<std::chrono::time_point<std::chrono::system_clock>> unused3) -> CallThreeDateTimesReturnValues
                                              {
                                                  std::cout << "Received call for callThreeDateTimes\n";
                                                  return CallThreeDateTimesReturnValues{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() };
                                              });

    server->registerCallOneDurationHandler([](std::chrono::duration<double> unused1) -> std::chrono::duration<double>
                                           {
                                               std::cout << "Received call for callOneDuration\n";
                                               return std::chrono::duration<double>(3536);
                                           });

    server->registerCallOptionalDurationHandler([](std::optional<std::chrono::duration<double>> unused1) -> std::optional<std::chrono::duration<double>>
                                                {
                                                    std::cout << "Received call for callOptionalDuration\n";
                                                    return std::chrono::duration<double>(3536);
                                                });

    server->registerCallThreeDurationsHandler([](std::chrono::duration<double> unused1, std::chrono::duration<double> unused2, std::optional<std::chrono::duration<double>> unused3) -> CallThreeDurationsReturnValues
                                              {
                                                  std::cout << "Received call for callThreeDurations\n";
                                                  return CallThreeDurationsReturnValues{ std::chrono::duration<double>(3536), std::chrono::duration<double>(3536), std::chrono::duration<double>(3536) };
                                              });

    server->registerCallOneBinaryHandler([](std::vector<uint8_t> unused1) -> std::vector<uint8_t>
                                         {
                                             std::cout << "Received call for callOneBinary\n";
                                             return std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 };
                                         });

    server->registerCallOptionalBinaryHandler([](std::optional<std::vector<uint8_t>> unused1) -> std::optional<std::vector<uint8_t>>
                                              {
                                                  std::cout << "Received call for callOptionalBinary\n";
                                                  return std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 };
                                              });

    server->registerCallThreeBinariesHandler([](std::vector<uint8_t> unused1, std::vector<uint8_t> unused2, std::optional<std::vector<uint8_t>> unused3) -> CallThreeBinariesReturnValues
                                             {
                                                 std::cout << "Received call for callThreeBinaries\n";
                                                 return CallThreeBinariesReturnValues{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } };
                                             });

    server->registerCallOneListOfIntegersHandler([](std::vector<int> unused1) -> std::vector<int>
                                                 {
                                                     std::cout << "Received call for callOneListOfIntegers\n";
                                                     return std::vector<int>{ 42, 2022, 2022 };
                                                 });

    server->registerCallOptionalListOfFloatsHandler([](std::optional<std::vector<double>> unused1) -> std::optional<std::vector<double>>
                                                    {
                                                        std::cout << "Received call for callOptionalListOfFloats\n";
                                                        return std::vector<double>{ 3.14, 1.0, 1.0 };
                                                    });

    server->registerCallTwoListsHandler([](std::vector<Numbers> unused1, std::optional<std::vector<std::string>> unused2) -> CallTwoListsReturnValues
                                        {
                                            std::cout << "Received call for callTwoLists\n";
                                            return CallTwoListsReturnValues{ std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::string>{ "apples", "foo", "foo" } };
                                        });

    // Start a background thread that emits signals every 60 seconds.
    std::atomic<bool> keepRunning{ true };
    std::thread periodicEmitter([server, &keepRunning]()
                                {
                                    int loopCount = 0;
                                    while (keepRunning) {
                                        loopCount++;
                                        // Call emitTodayIsSignal; do not block forever waiting for publish
                                        try {
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
                                            auto singleOptionalStringFuture = server->emitSingleOptionalStringSignal(std::make_optional(std::string("apples")));
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeStringsFuture = server->emitThreeStringsSignal("apples", "apples", std::make_optional(std::string("apples")));
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleEnumFuture = server->emitSingleEnumSignal(Numbers::ONE);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalEnumFuture = server->emitSingleOptionalEnumSignal(Numbers::ONE);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeEnumsFuture = server->emitThreeEnumsSignal(Numbers::ONE, Numbers::ONE, Numbers::ONE);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleStructFuture = server->emitSingleStructSignal(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalStructFuture = server->emitSingleOptionalStructSignal(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeStructsFuture = server->emitThreeStructsSignal(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } }, AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } }, AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });
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
                                            auto singleBinaryFuture = server->emitSingleBinarySignal(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalBinaryFuture = server->emitSingleOptionalBinarySignal(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto threeBinariesFuture = server->emitThreeBinariesSignal(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleArrayOfIntegersFuture = server->emitSingleArrayOfIntegersSignal(std::vector<int>{ 42, 2022, 2022 });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto singleOptionalArrayOfStringsFuture = server->emitSingleOptionalArrayOfStringsSignal(std::vector<std::string>{ "apples", "foo", "foo" });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto arrayOfEveryTypeFuture = server->emitArrayOfEveryTypeSignal(std::vector<int>{ 42, 2022, 2022 }, std::vector<double>{ 3.14, 1.0, 1.0 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } });
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
                                            singleArrayOfIntegersFuture.wait();
                                            singleOptionalArrayOfStringsFuture.wait();
                                            arrayOfEveryTypeFuture.wait();
                                        } catch (...) { }

                                        std::cout << "Periodic update iteration " << loopCount << " complete. Sleeping for 35 ...\n";

                                        // Sleep in 1-second increments so we can stop quickly
                                        for (int i = 0; i < 35 && keepRunning; ++i) {
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                        }

                                        if (loopCount % 3 == 0) {
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
                                            server->updateReadWriteOptionalStringProperty(std::make_optional(std::string("apples")));

                                            std::cout << "Updating value for property 'read_write_two_strings'.\n";
                                            server->updateReadWriteTwoStringsProperty("apples", std::make_optional(std::string("apples")));

                                            std::cout << "Updating value for property 'read_write_struct'.\n";
                                            server->updateReadWriteStructProperty(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });

                                            std::cout << "Updating value for property 'read_write_optional_struct'.\n";
                                            server->updateReadWriteOptionalStructProperty(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });

                                            std::cout << "Updating value for property 'read_write_two_structs'.\n";
                                            server->updateReadWriteTwoStructsProperty(AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } }, AllTypes{ true, 42, 3.14, "apples", Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, 42, std::make_optional(std::string("apples")), Numbers::ONE, Entry{ 42, "apples" }, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<int>{ 42, 2022, 2022 }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<std::string>{ "apples", "foo", "foo" }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::chrono::duration<double>>{ std::chrono::duration<double>(3536), std::chrono::duration<double>(975), std::chrono::duration<double>(967) }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<std::vector<uint8_t>>{ std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } }, std::vector<Entry>{ Entry{ 42, "apples" }, Entry{ 2022, "foo" }, Entry{ 2022, "foo" } } });

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
                                            server->updateReadWriteBinaryProperty(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });

                                            std::cout << "Updating value for property 'read_write_optional_binary'.\n";
                                            server->updateReadWriteOptionalBinaryProperty(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });

                                            std::cout << "Updating value for property 'read_write_two_binaries'.\n";
                                            server->updateReadWriteTwoBinariesProperty(std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 }, std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });

                                            std::cout << "Updating value for property 'read_write_list_of_strings'.\n";
                                            server->updateReadWriteListOfStringsProperty(std::vector<std::string>{ "apples", "foo", "foo" });

                                            std::cout << "Updating value for property 'read_write_lists'.\n";
                                            server->updateReadWriteListsProperty(std::vector<Numbers>{ Numbers::ONE, Numbers::ONE, Numbers::ONE }, std::vector<std::chrono::time_point<std::chrono::system_clock>>{ std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now() });
                                        }
                                    }
                                });

    std::cout << "Press ENTER to exit\n";
    std::cin.ignore();

    // Signal the emitter thread to stop and join it
    keepRunning = false;
    if (periodicEmitter.joinable()) {
        periodicEmitter.join();
    }

    return 0;
}