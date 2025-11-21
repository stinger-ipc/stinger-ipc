

#include <iostream>
#include <sstream>
#include <syslog.h>
#include <chrono>
#include <thread>
#include "utils.hpp"
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"
#include "discovery.hpp"
#include "interface_exceptions.hpp"

int main(int argc, char** argv)
{
    // Create a connection to the broker
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "simple-client-demo");
    conn->SetLogLevel(LOG_DEBUG);
    conn->SetLogFunction([](int level, const char* msg)
                         {
                             std::cout << "[" << level << "] " << msg << std::endl;
                         });

    // Discover a service ID for a Simple service.
    std::string serviceId;
    { // restrict scope
        SimpleDiscovery discovery(conn);
        auto serviceIdFut = discovery.GetSingleton();
        auto serviceIdFutStatus = serviceIdFut.wait_for(std::chrono::seconds(15));
        if (serviceIdFutStatus == std::future_status::timeout)
        {
            std::cerr << "Failed to discover service instance within timeout." << std::endl;
            return 1;
        }
        serviceId = serviceIdFut.get();
    }

    // Create the client object.
    SimpleClient client(conn, serviceId);

    // Register callbacks for signals.
    client.registerPersonEnteredCallback([](Person person)
                                         {
                                             std::cout << "Received PERSON_ENTERED signal: "
                                                       << "person=" << "[Person object]"
                                                       << std::endl;
                                         });

    // Register callbacks for property updates.
    client.registerSchoolPropertyCallback([](std::string name)
                                          {
                                              std::cout << "Received update for school property: " << "name=" << name /* unhandled arg type*/ << std::endl;
                                          });

    // Call each method with example values.

    // ----------------------METHOD TRADE_NUMBERS-----------------------------------------
    { // Restrict scope for the `trade_numbers` method call.
        std::cout << "CALLING TRADE_NUMBERS" << std::endl;
        auto tradeNumbersResultFuture = client.tradeNumbers(42);
        auto tradeNumbersStatus = tradeNumbersResultFuture.wait_for(std::chrono::seconds(5));
        if (tradeNumbersStatus == std::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for TRADE_NUMBERS response." << std::endl;
        }
        else
        {
            int returnValue;
            bool success = false;
            try
            {
                returnValue = tradeNumbersResultFuture.get();
                success = true;
            }
            catch (const StingerMethodException& ex)
            {
                std::cout << "TRADE_NUMBERS Exception: " << ex.what() << std::endl;
            }
            if (success)
            {
                std::cout << "TRADE_NUMBERS Response: "
                          << " my_number=" << returnValue << std::endl;
            }
        }
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }

    return 0;
}