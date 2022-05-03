
#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv) {

    
    auto conn = DefaultConnection('localhost', 1883);
    auto client = ExampleClient(conn);
    client.registerTodayIsCallback([](int dayOfMonth, DayOfTheWeek dayOfWeek) {
        std::cout << "dayOfMonth=" << dayOfMonth << " | " << "dayOfWeek=" << dayOfWeek <<  std::endl;
    });

    pause();

    return 0;
}