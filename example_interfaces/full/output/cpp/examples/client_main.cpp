
#include <iostream>

#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<LocalConnection>("ExampleClient-demo");
    ExampleClient client(conn);
    client.registerTodayIsCallback([](int dayOfMonth, DayOfTheWeek dayOfWeek) {
        std::cout << "dayOfMonth=" << dayOfMonth << " | " << "dayOfWeek=" << dayOfTheWeekStrings[static_cast<int>(dayOfWeek)] <<  std::endl;
    });
    std::cout << "Calling addNumbers" << std::endl;
    auto addNumbersResultFuture = client.addNumbers(42, 42);
    addNumbersResultFuture.wait();
    std::cout << "Result: sum=" << addNumbersResultFuture.get() << std::endl;
    
    std::cout << "Calling doSomething" << std::endl;
    auto doSomethingResultFuture = client.doSomething("apples");
    doSomethingResultFuture.wait();
    DoSomethingReturnValue returnValue = doSomethingResultFuture.get();
    std::cout << "Results:" << " label=" << returnValue.label  << " identifier=" << returnValue.identifier  << " day=" << dayOfTheWeekStrings[static_cast<int>(returnValue.day)]  << std::endl;
    

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true) {
        sleep(10);
    }

    return 0;
}