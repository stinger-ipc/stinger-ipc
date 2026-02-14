

#include <iostream>
#include <sstream>
#include <syslog.h>
#include <chrono>
#include <thread>
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"
#include "discovery.hpp"
#include "enums.hpp"
#include "interface_exceptions.hpp"

int main(int argc, char** argv)
{
    // Create a connection to the broker
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "full-client-demo");
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
        auto serviceIdFutStatus = serviceIdFut.wait_for(std::chrono::seconds(15));
        if (serviceIdFutStatus == std::future_status::timeout) {
            std::cerr << "Failed to discover service instance within timeout." << std::endl;
            return 1;
        }
        serviceId = serviceIdFut.get();
    }

    // Create the client object.
    FullClient client(conn, serviceId);

    // Register callbacks for signals.
    client.registerTodayIsCallback([](int dayOfMonth, DayOfTheWeek dayOfWeek)
                                   {
                                       std::cout << "Received TODAY_IS signal: "
                                                 << "dayOfMonth=" << dayOfMonth << " | " << "dayOfWeek=" << dayOfTheWeekStrings.at(static_cast<int>(dayOfWeek)) << std::endl;
                                   });

    client.registerRandomWordCallback([](std::string word, std::chrono::time_point<std::chrono::system_clock> time)
                                      {
                                          std::string timeStr = stinger::utils::timePointToIsoString(time);

                                          std::cout << "Received RANDOM_WORD signal: "
                                                    << "word=" << word << " | " << "time=" << timeStr << std::endl;
                                      });

    // Register callbacks for property updates.
    client.registerFavoriteNumberPropertyCallback([](int number)
                                                  {
                                                      std::cout << "Received update for favorite_number property: " << "number=" << number /* unhandled arg type*/ << std::endl;
                                                  });

    client.registerFavoriteFoodsPropertyCallback([](std::string drink, int slicesOfPizza, std::optional<std::string> breakfast)
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
                                                         std::string timestampStr = stinger::utils::timePointToIsoString(timestamp);

                                                         std::cout << "Received update for last_breakfast_time property: " << "timestamp=" << timestampStr
                                                                   << std::endl;
                                                     });

    client.registerLastBirthdaysPropertyCallback([](std::chrono::time_point<std::chrono::system_clock> mom, std::chrono::time_point<std::chrono::system_clock> dad, std::optional<std::chrono::time_point<std::chrono::system_clock>> sister, std::optional<int> brothersAge)
                                                 {
                                                     std::string momStr = stinger::utils::timePointToIsoString(mom);

                                                     std::string dadStr = stinger::utils::timePointToIsoString(dad);

                                                     std::string sisterStr = "None";
                                                     if (sister) {
                                                         std::string sisterStr = stinger::utils::timePointToIsoString(*sister);
                                                     }

                                                     std::cout << "Received update for last_birthdays property: " << "mom=" << momStr
                                                               << " | " << "dad=" << dadStr
                                                               << " | " << "sister=" << "None" << " | " << "brothers_age=" << "None" << std::endl;
                                                 });

    // Call each method with example values.

    // ----------------------METHOD ADD_NUMBERS-----------------------------------------
    { // Restrict scope for the `addNumbers` method call.
        std::cout << "CALLING ADD_NUMBERS" << std::endl;
        auto addNumbersResultFuture = client.addNumbers(42, 42, 42);
        auto addNumbersStatus = addNumbersResultFuture.wait_for(std::chrono::seconds(5));
        if (addNumbersStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for ADD_NUMBERS response." << std::endl;
        } else {
            int returnValue;
            bool success = false;
            try {
                returnValue = addNumbersResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "ADD_NUMBERS Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "ADD_NUMBERS Response: "
                          << " sum=" << returnValue << std::endl;
            }
        }
    }

    // ----------------------METHOD DO_SOMETHING-----------------------------------------
    { // Restrict scope for the `doSomething` method call.
        std::cout << "CALLING DO_SOMETHING" << std::endl;
        auto doSomethingResultFuture = client.doSomething("apples");
        auto doSomethingStatus = doSomethingResultFuture.wait_for(std::chrono::seconds(5));
        if (doSomethingStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for DO_SOMETHING response." << std::endl;
        } else {
            DoSomethingReturnValues returnValue;
            bool success = false;
            try {
                returnValue = doSomethingResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "DO_SOMETHING Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "DO_SOMETHING Response: "
                          << " label=" << returnValue.label << " identifier=" << returnValue.identifier << std::endl;
            }
        }
    }

    // ----------------------METHOD WHAT_TIME_IS_IT-----------------------------------------
    { // Restrict scope for the `what_time_is_it` method call.
        std::cout << "CALLING WHAT_TIME_IS_IT" << std::endl;
        auto whatTimeIsItResultFuture = client.whatTimeIsIt();
        auto whatTimeIsItStatus = whatTimeIsItResultFuture.wait_for(std::chrono::seconds(5));
        if (whatTimeIsItStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for WHAT_TIME_IS_IT response." << std::endl;
        } else {
            std::chrono::time_point<std::chrono::system_clock> returnValue;
            bool success = false;
            try {
                returnValue = whatTimeIsItResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "WHAT_TIME_IS_IT Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "WHAT_TIME_IS_IT Response: "
                          << " timestamp=" << stinger::utils::timePointToIsoString(returnValue) << std::endl;
            }
        }
    }

    // ----------------------METHOD HOLD_TEMPERATURE-----------------------------------------
    { // Restrict scope for the `hold_temperature` method call.
        std::cout << "CALLING HOLD_TEMPERATURE" << std::endl;
        auto holdTemperatureResultFuture = client.holdTemperature(3.14);
        auto holdTemperatureStatus = holdTemperatureResultFuture.wait_for(std::chrono::seconds(5));
        if (holdTemperatureStatus == std::future_status::timeout) {
            std::cout << "TIMEOUT after 5 seconds waiting for HOLD_TEMPERATURE response." << std::endl;
        } else {
            bool returnValue;
            bool success = false;
            try {
                returnValue = holdTemperatureResultFuture.get();
                success = true;
            } catch (const StingerMethodException& ex) {
                std::cout << "HOLD_TEMPERATURE Exception: " << ex.what() << std::endl;
            }
            if (success) {
                std::cout << "HOLD_TEMPERATURE Response: "
                          << " success=" << returnValue << std::endl;
            }
        }
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }

    return 0;
}