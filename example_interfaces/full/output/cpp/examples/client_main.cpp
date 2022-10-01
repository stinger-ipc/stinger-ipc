
#include <iostream>

#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<LocalConnection>("ExampleServer");
    ExampleClient client(conn);
    client.registerTodayIsCallback([](int dayOfMonth, DayOfTheWeek dayOfWeek) {
        std::cout << "dayOfMonth=" << dayOfMonth << " | " << "dayOfWeek=" << static_cast<int>(dayOfWeek) <<  std::endl;
    });

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true) {
        sleep(10);
    }

    return 0;
}