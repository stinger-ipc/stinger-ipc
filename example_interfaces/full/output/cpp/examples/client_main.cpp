

#include <iostream>
#include <sstream>
#include <syslog.h>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"
#include "discovery.hpp"

int main(int argc, char** argv)
{
    // Create a connection to the broker
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "Full-client-demo");
    conn->SetLogLevel(LOG_DEBUG);
    conn->SetLogFunction([](int level, const char* msg)
                         {
                             std::cout << "[" << level << "] " << msg << std::endl;
                         });

    // Discover a service ID for a Full service.
    std::string serviceId;
    { // restrict scope
        FullDiscovery discovery(conn);
        auto serviceIdFut = discovery.GetSingleton();
        auto serviceIdFutStatus = serviceIdFut.wait_for(boost::chrono::seconds(15));
        if (serviceIdFutStatus == boost::future_status::timeout)
        {
            std::cerr << "Failed to discover service instance within timeout." << std::endl;
            return 1;
        }
        serviceId = serviceIdFut.get();
    }

    // Create the client object.
    FullClient client(conn, serviceId);

    // Register callbacks for signals.
    client.registerTodayIsCallback([](int dayOfMonth, boost::optional<DayOfTheWeek> dayOfWeek, std::chrono::time_point<std::chrono::system_clock> timestamp, std::chrono::duration<double> processTime, std::vector<uint8_t> memorySegment)
                                   {
                                       std::string timestampStr = timePointToIsoString(timestamp);

                                       std::string processTimeStr = durationToIsoString(processTime);
                                       std::string memorySegmentStr = "[Binary Data]";

                                       std::cout << "Received TODAY_IS signal: "
                                                 << "dayOfMonth=" << dayOfMonth << " | " << "dayOfWeek=" << dayOfTheWeekStrings[static_cast<int>(*dayOfWeek)] << " | " << "timestamp=" << timestampStr << " | " << "process_time=" << processTimeStr << " | " << "memory_segment=" << memorySegmentStr << std::endl;
                                   });

    // Register callbacks for property updates.
    client.registerFavoriteNumberPropertyCallback([](int number)
                                                  {
                                                      std::cout << "Received update for favorite_number property: " << "number=" << number /* unhandled arg type*/ << std::endl;
                                                  });

    client.registerFavoriteFoodsPropertyCallback([](std::string drink, int slicesOfPizza, boost::optional<std::string> breakfast)
                                                 {
                                                     std::cout << "Received update for favorite_foods property: " << "drink=" << drink /* unhandled arg type*/ << " | " << "slices_of_pizza=" << slicesOfPizza /* unhandled arg type*/ << " | " << "breakfast=" << "None" << std::endl;
                                                 });

    client.registerLunchMenuPropertyCallback([](Lunch monday, Lunch tuesday)
                                             {
                                                 std::cout << "Received update for lunch_menu property: " << "monday=" << "[Lunch object]"
                                                           << " | " << "tuesday=" << "[Lunch object]"
                                                           << std::endl;
                                             });

    client.registerFamilyNamePropertyCallback([](std::string familyName)
                                              {
                                                  std::cout << "Received update for family_name property: " << "family_name=" << familyName /* unhandled arg type*/ << std::endl;
                                              });

    client.registerLastBreakfastTimePropertyCallback([](std::chrono::time_point<std::chrono::system_clock> timestamp)
                                                     {
                                                         std::string timestampStr = timePointToIsoString(timestamp);

                                                         std::cout << "Received update for last_breakfast_time property: " << "timestamp=" << timestampStr
                                                                   << std::endl;
                                                     });

    client.registerBreakfastLengthPropertyCallback([](std::chrono::duration<double> length)
                                                   {
                                                       std::string lengthStr = durationToIsoString(length);

                                                       std::cout << "Received update for breakfast_length property: " << "length=" << lengthStr
                                                                 << std::endl;
                                                   });

    client.registerLastBirthdaysPropertyCallback([](std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, boost::optional<std::chrono::time_point<std::chrono::system_clock>> sister, boost::optional<int> brothersAge)
                                                 {
                                                     std::string momStr = timePointToIsoString(mom);

                                                     std::string dadStr = timePointToIsoString(dad);

                                                     std::string sisterStr = "None";
                                                     if (sister)
                                                     {
                                                         std::string sisterStr = timePointToIsoString(*sister);
                                                     }

                                                     std::cout << "Received update for last_birthdays property: " << "mom=" << momStr
                                                               << " | " << "dad=" << dadStr
                                                               << " | " << "sister=" << "None" << " | " << "brothers_age=" << "None" << std::endl;
                                                 });

    // Call each method with example values.

    // ----------------------METHOD ADD_NUMBERS-----------------------------------------
    { // Restrict scope
        std::cout << "CALLING ADD_NUMBERS" << std::endl;
        auto addNumbersResultFuture = client.addNumbers(42, 42, 42);
        auto addNumbersStatus = addNumbersResultFuture.wait_for(boost::chrono::seconds(5));
        if (addNumbersStatus == boost::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for ADD_NUMBERS response." << std::endl;
        }
        else
        {
            int returnValue = addNumbersResultFuture.get();
            std::cout << "ADD_NUMBERS Response: "
                      << " sum=" << returnValue << std::endl;
        }
    }

    // ----------------------METHOD DO_SOMETHING-----------------------------------------
    { // Restrict scope
        std::cout << "CALLING DO_SOMETHING" << std::endl;
        auto doSomethingResultFuture = client.doSomething("apples");
        auto doSomethingStatus = doSomethingResultFuture.wait_for(boost::chrono::seconds(5));
        if (doSomethingStatus == boost::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for DO_SOMETHING response." << std::endl;
        }
        else
        {
            DoSomethingReturnValues returnValue = doSomethingResultFuture.get();
            std::cout << "DO_SOMETHING Response: "
                      << " label=" << returnValue.label << " identifier=" << returnValue.identifier << " day=" << dayOfTheWeekStrings[static_cast<int>(returnValue.day)] << std::endl;
        }
    }

    // ----------------------METHOD ECHO-----------------------------------------
    { // Restrict scope
        std::cout << "CALLING ECHO" << std::endl;
        auto echoResultFuture = client.echo("apples");
        auto echoStatus = echoResultFuture.wait_for(boost::chrono::seconds(5));
        if (echoStatus == boost::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for ECHO response." << std::endl;
        }
        else
        {
            std::string returnValue = echoResultFuture.get();
            std::cout << "ECHO Response: "
                      << " message=" << returnValue << std::endl;
        }
    }

    // ----------------------METHOD WHAT_TIME_IS_IT-----------------------------------------
    { // Restrict scope
        std::cout << "CALLING WHAT_TIME_IS_IT" << std::endl;
        auto whatTimeIsItResultFuture = client.whatTimeIsIt(std::chrono::system_clock::now());
        auto whatTimeIsItStatus = whatTimeIsItResultFuture.wait_for(boost::chrono::seconds(5));
        if (whatTimeIsItStatus == boost::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for WHAT_TIME_IS_IT response." << std::endl;
        }
        else
        {
            std::chrono::time_point<std::chrono::system_clock> returnValue = whatTimeIsItResultFuture.get();
            std::cout << "WHAT_TIME_IS_IT Response: "
                      << " timestamp=" << timePointToIsoString(returnValue) << std::endl;
        }
    }

    // ----------------------METHOD SET_THE_TIME-----------------------------------------
    { // Restrict scope
        std::cout << "CALLING SET_THE_TIME" << std::endl;
        auto setTheTimeResultFuture = client.setTheTime(std::chrono::system_clock::now(), std::chrono::system_clock::now());
        auto setTheTimeStatus = setTheTimeResultFuture.wait_for(boost::chrono::seconds(5));
        if (setTheTimeStatus == boost::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for SET_THE_TIME response." << std::endl;
        }
        else
        {
            SetTheTimeReturnValues returnValue = setTheTimeResultFuture.get();
            std::cout << "SET_THE_TIME Response: "
                      << " timestamp=" << timePointToIsoString(returnValue.timestamp) << " confirmation_message=" << returnValue.confirmationMessage << std::endl;
        }
    }

    // ----------------------METHOD FORWARD_TIME-----------------------------------------
    { // Restrict scope
        std::cout << "CALLING FORWARD_TIME" << std::endl;
        auto forwardTimeResultFuture = client.forwardTime(std::chrono::duration<double>(3536));
        auto forwardTimeStatus = forwardTimeResultFuture.wait_for(boost::chrono::seconds(5));
        if (forwardTimeStatus == boost::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for FORWARD_TIME response." << std::endl;
        }
        else
        {
            std::chrono::time_point<std::chrono::system_clock> returnValue = forwardTimeResultFuture.get();
            std::cout << "FORWARD_TIME Response: "
                      << " new_time=" << timePointToIsoString(returnValue) << std::endl;
        }
    }

    // ----------------------METHOD HOW_OFF_IS_THE_CLOCK-----------------------------------------
    { // Restrict scope
        std::cout << "CALLING HOW_OFF_IS_THE_CLOCK" << std::endl;
        auto howOffIsTheClockResultFuture = client.howOffIsTheClock(std::chrono::system_clock::now());
        auto howOffIsTheClockStatus = howOffIsTheClockResultFuture.wait_for(boost::chrono::seconds(5));
        if (howOffIsTheClockStatus == boost::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for HOW_OFF_IS_THE_CLOCK response." << std::endl;
        }
        else
        {
            std::chrono::duration<double> returnValue = howOffIsTheClockResultFuture.get();
            std::cout << "HOW_OFF_IS_THE_CLOCK Response: "
                      << " difference=" << durationToIsoString(returnValue) << std::endl;
        }
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        sleep(10);
    }

    return 0;
}