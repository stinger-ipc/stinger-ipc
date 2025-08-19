
#include <iostream>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<LocalConnection>("ExampleClient-demo");
    ExampleClient client(conn);
    client.registerTodayIsCallback([](int dayOfMonth, boost::optional<DayOfTheWeek> dayOfWeek) {
        std::cout << "dayOfMonth=" <<dayOfMonth << " | " << "dayOfWeek=" << "None" <<  std::endl;
    });
    std::cout << "Calling addNumbers" << std::endl;
    auto addNumbersResultFuture = client.addNumbers(42, 42, 42);
    auto addNumbersStatus = addNumbersResultFuture.wait_for(boost::chrono::seconds(5));
    if (addNumbersStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for addNumbers response." << std::endl;
    }
    else
    {
        std::cout << "Result: sum=" << addNumbersResultFuture.get() << std::endl;
        
    }
    std::cout << "Calling doSomething" << std::endl;
    auto doSomethingResultFuture = client.doSomething("apples");
    auto doSomethingStatus = doSomethingResultFuture.wait_for(boost::chrono::seconds(5));
    if (doSomethingStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for doSomething response." << std::endl;
    }
    else
    {
        DoSomethingReturnValue returnValue = doSomethingResultFuture.get();
        std::cout << "Results:" << " label=" << returnValue.label  << " identifier=" << returnValue.identifier  << " day=" << dayOfTheWeekStrings[static_cast<int>(returnValue.day)]  << std::endl;
        
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true) {
        sleep(10);
    }

    return 0;
}