
#include <iostream>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "Full-server-demo");
    FullServer server(conn);
    auto todayIsFuture = server.emitTodayIsSignal(42, DayOfTheWeek::SATURDAY, std::chrono::system_clock::now(), None, { 101, 120, 97, 109, 112, 108, 101 });
    todayIsFuture.wait();
    server.registerAddNumbersHandler([](int unused1, int unused2, boost::optional<int> unused3) -> int
                                     {
        std::cout << "Received call for addNumbers\n";
        return 42; });

    server.registerDoSomethingHandler([](const std::string& unused1) -> DoSomethingReturnValue
                                      {
        std::cout << "Received call for doSomething\n";
        return DoSomethingReturnValue{ "apples", 42, DayOfTheWeek::SATURDAY }; });

    server.registerEchoHandler([](const std::string& unused1) -> std::string
                               {
        std::cout << "Received call for echo\n";
        return "apples"; });

    server.registerWhatTimeIsItHandler([](std::chrono::time_point<std::chrono::system_clock> unused1) -> std::chrono::time_point<std::chrono::system_clock>
                                       {
        std::cout << "Received call for what_time_is_it\n";
        return std::chrono::system_clock::now(); });

    server.registerSetTheTimeHandler([](std::chrono::time_point<std::chrono::system_clock> unused1, std::chrono::time_point<std::chrono::system_clock> unused2) -> SetTheTimeReturnValue
                                     {
        std::cout << "Received call for set_the_time\n";
        return SetTheTimeReturnValue{ std::chrono::system_clock::now(), "apples" }; });

    server.registerForwardTimeHandler([](std::chrono::milliseconds unused1) -> std::chrono::time_point<std::chrono::system_clock>
                                      {
        std::cout << "Received call for forward_time\n";
        return std::chrono::system_clock::now(); });

    server.registerHowOffIsTheClockHandler([](std::chrono::time_point<std::chrono::system_clock> unused1) -> std::chrono::milliseconds
                                           {
        std::cout << "Received call for how_off_is_the_clock\n";
        return None; });

    std::cout << "Press Enter to exit\n";
    std::cin.ignore();
    return 0;
}