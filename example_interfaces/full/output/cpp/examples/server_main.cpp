
#include <iostream>

#include "broker.hpp"
#include "server.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<DefaultConnection>("localhost", 1883);
    ExampleServer server(conn);
    server.emitTodayIsSignal(42, iface_enums.DayOfTheWeek.MONDAY);

    return 0;
}