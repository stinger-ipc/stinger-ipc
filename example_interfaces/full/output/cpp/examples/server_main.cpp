
#include <iostream>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<LocalConnection>("Full");
    FullServer server(conn);
    auto todayIsFuture = server.emitTodayIsSignal(42, DayOfTheWeek::MONDAY);
    auto barkFuture = server.emitBarkSignal("apples");
    todayIsFuture.wait();
    barkFuture.wait();
    server.registerAddNumbersHandler([](int unused1, int unused2, boost::optional<int> unused3) -> int
                                     {
        std::cout << "Received call for addNumbers\n";
        return 42; });

    server.registerDoSomethingHandler([](const std::string& unused1) -> DoSomethingReturnValue
                                      {
        std::cout << "Received call for doSomething\n";
        return DoSomethingReturnValue{ "apples", 42, DayOfTheWeek::MONDAY }; });

    server.registerEchoHandler([](const std::string& unused1) -> std::string
                               {
        std::cout << "Received call for echo\n";
        return "apples"; });

    std::cout << "Press Enter to exit\n";
    std::cin.ignore();
    return 0;
}