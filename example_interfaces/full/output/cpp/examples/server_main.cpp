
#include <iostream>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<LocalConnection>();
    ExampleServer server(conn);
    auto todayIsFuture = server.emitTodayIsSignal(42, DayOfTheWeek::MONDAY);
    todayIsFuture.wait();
    server.registerAddNumbersHandler([](int unused1, int unused2) -> int
    {
        std::cout << "Received call for addNumbers\n";
        return 42;
    });
    
    std::cout << "Press Enter to exit\n"; 
    std::cin.ignore();
    return 0;
}