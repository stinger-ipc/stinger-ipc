
#include <iostream>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<DefaultConnection>("localhost", 1883);
    ExampleServer server(conn);
    auto todayIsFuture = server.emitTodayIsSignal(42, DayOfTheWeek::MONDAY);
    todayIsFuture.wait();
    return 0;
}