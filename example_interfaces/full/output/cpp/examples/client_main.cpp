

#include <iostream>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<LocalConnection>("FullClient-demo");
    FullClient client(conn);
    client.registerTodayIsCallback([](int dayOfMonth, boost::optional<DayOfTheWeek> dayOfWeek)
                                   { std::cout << "dayOfMonth=" << dayOfMonth << " | " << "dayOfWeek=" << "None" << std::endl; });
    client.registerFavoriteNumberPropertyCallback([](int number)
                                                  { std::cout << "Received update for favorite_number property: " << "number=" << number << std::endl; });

    client.registerFavoriteFoodsPropertyCallback([](const std::string& drink, int slices_of_pizza, boost::optional<std::string> breakfast)
                                                 { std::cout << "Received update for favorite_foods property: " << "drink=" << drink << " | " << "slices_of_pizza=" << slices_of_pizza << " | " << "breakfast=" << "None" << std::endl; });

    client.registerLunchMenuPropertyCallback([](Lunch monday, Lunch tuesday)
                                             { std::cout << "Received update for lunch_menu property: " << "monday=" << "[Lunch object]" << " | " << "tuesday=" << "[Lunch object]" << std::endl; });

    client.registerFamilyNamePropertyCallback([](const std::string& family_name)
                                              { std::cout << "Received update for family_name property: " << "family_name=" << family_name << std::endl; });

    std::cout << "Calling addNumbers" << std::endl;
    auto addNumbersResultFuture = client.addNumbers(42, 42, 42);
    auto addNumbersStatus = addNumbersResultFuture.wait_for(boost::chrono::seconds(5));
    if (addNumbersStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for addNumbers response." << std::endl;
    }
    else
    {
        std::cout << "Result: Sum=" << addNumbersResultFuture.get() << std::endl;
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
        std::cout << "Results:" << " label=" << returnValue.label << " identifier=" << returnValue.identifier << " day=" << dayOfTheWeekStrings[static_cast<int>(returnValue.day)] << std::endl;
    }
    std::cout << "Calling echo" << std::endl;
    auto echoResultFuture = client.echo("apples");
    auto echoStatus = echoResultFuture.wait_for(boost::chrono::seconds(5));
    if (echoStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for echo response." << std::endl;
    }
    else
    {
        std::cout << "Result: Message=" << echoResultFuture.get() << std::endl;
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        sleep(10);
    }

    return 0;
}