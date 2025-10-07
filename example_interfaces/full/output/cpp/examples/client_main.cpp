

#include <iostream>
#include <sstream>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "Full-client-demo");
    FullClient client(conn);
    client.registerTodayIsCallback([](int dayOfMonth, boost::optional<DayOfTheWeek> dayOfWeek, std::chrono::time_point<std::chrono::system_clock> timestamp, std::chrono::duration<double> process_time, std::vector<uint8_t> memory_segment)
                                   {
        
        std::string timestampStr = timePointToIsoString(timestamp);
        
        
        std::string processTimeStr = "[Duration Data]";
        
        std::string memorySegmentStr = "[Binary Data]";
        std::cout << "dayOfMonth=" <<dayOfMonth << " | " << "dayOfWeek=" << "None" << " | " << "timestamp=" <<timestampStr << " | " << "process_time=" <<processTimeStr << " | " << "memory_segment=" <<memorySegmentStr <<  std::endl; });
    client.registerFavoriteNumberPropertyCallback([](int number)
                                                  { std::cout << "Received update for favorite_number property: " << "number=" << number /* unhandled arg type*/ << std::endl; });

    client.registerFavoriteFoodsPropertyCallback([](const std::string& drink, int slices_of_pizza, boost::optional<std::string> breakfast)
                                                 { std::cout << "Received update for favorite_foods property: " << "drink=" << drink /* unhandled arg type*/ << " | " << "slices_of_pizza=" << slices_of_pizza /* unhandled arg type*/ << " | " << "breakfast=" << "None" << std::endl; });

    client.registerLunchMenuPropertyCallback([](Lunch monday, Lunch tuesday)
                                             { std::cout << "Received update for lunch_menu property: " << "monday=" << "[Lunch object]"
                                                         << " | " << "tuesday=" << "[Lunch object]"
                                                         << std::endl; });

    client.registerFamilyNamePropertyCallback([](const std::string& family_name)
                                              { std::cout << "Received update for family_name property: " << "family_name=" << family_name /* unhandled arg type*/ << std::endl; });

    client.registerLastBreakfastTimePropertyCallback([](std::chrono::time_point<std::chrono::system_clock> timestamp)
                                                     {
         
        std::string timestampStr = timePointToIsoString(timestamp);
         
        std::cout << "Received update for last_breakfast_time property: " << "timestamp=" << 
                                timestampStr
                             <<std::endl; });

    client.registerBreakfastLengthPropertyCallback([](std::chrono::duration<double> length)
                                                   {
        
        std::string lengthStr = durationToIsoString(length);
        
        std::cout << "Received update for breakfast_length property: " << "length=" << 
                                lengthStr <<std::endl; });

    client.registerLastBirthdaysPropertyCallback([](std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, boost::optional<std::chrono::time_point<std::chrono::system_clock>> sister, boost::optional<int> brothers_age)
                                                 {
         
        std::string momStr = timePointToIsoString(mom);
         
        
         
        std::string dadStr = timePointToIsoString(dad);
         
        
        
        if (sister) {
            std::string sisterStr = timePointToIsoString(*sister);
        } else {
            std::string sisterStr = "None";
        }
         
        std::cout << "Received update for last_birthdays property: " << "mom=" << 
                                momStr
                             << " | " << "dad=" << 
                                dadStr
                             << " | " << "sister=" <<  "None" << " | " << "brothers_age=" <<  "None" <<std::endl; });

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
    std::cout << "Calling what_time_is_it" << std::endl;
    auto whatTimeIsItResultFuture = client.whatTimeIsIt(std::chrono::system_clock::now());
    auto whatTimeIsItStatus = whatTimeIsItResultFuture.wait_for(boost::chrono::seconds(5));
    if (whatTimeIsItStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for what_time_is_it response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling set_the_time" << std::endl;
    auto setTheTimeResultFuture = client.setTheTime(std::chrono::system_clock::now(), std::chrono::system_clock::now());
    auto setTheTimeStatus = setTheTimeResultFuture.wait_for(boost::chrono::seconds(5));
    if (setTheTimeStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for set_the_time response." << std::endl;
    }
    else
    {
        SetTheTimeReturnValue returnValue = setTheTimeResultFuture.get();
        std::cout << "Results:" << " timestamp=" << timePointToIsoString(returnValue.timestamp) << " confirmation_message=" << returnValue.confirmation_message << std::endl;
    }
    std::cout << "Calling forward_time" << std::endl;
    auto forwardTimeResultFuture = client.forwardTime(std::chrono::duration<double>(3536));
    auto forwardTimeStatus = forwardTimeResultFuture.wait_for(boost::chrono::seconds(5));
    if (forwardTimeStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for forward_time response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling how_off_is_the_clock" << std::endl;
    auto howOffIsTheClockResultFuture = client.howOffIsTheClock(std::chrono::system_clock::now());
    auto howOffIsTheClockStatus = howOffIsTheClockResultFuture.wait_for(boost::chrono::seconds(5));
    if (howOffIsTheClockStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for how_off_is_the_clock response." << std::endl;
    }
    else
    {
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        sleep(10);
    }

    return 0;
}