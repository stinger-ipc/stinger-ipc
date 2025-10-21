

#include <iostream>
#include <sstream>
#include <syslog.h>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"
#include "discovery.hpp"
#include "interface_exceptions.hpp"

int main(int argc, char** argv)
{
    // Create a connection to the broker
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "signal-only-client-demo");
    conn->SetLogLevel(LOG_DEBUG);
    conn->SetLogFunction([](int level, const char* msg)
                         {
                             std::cout << "[" << level << "] " << msg << std::endl;
                         });

    // Discover a service ID for a SignalOnly service.
    std::string serviceId;
    { // restrict scope
        SignalOnlyDiscovery discovery(conn);
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
    SignalOnlyClient client(conn, serviceId);

    // Register callbacks for signals.
    client.registerAnotherSignalCallback([](double one, bool two, std::string three)
                                         {
                                             std::cout << "Received ANOTHER_SIGNAL signal: "
                                                       << "one=" << one << " | " << "two=" << two << " | " << "three=" << three << std::endl;
                                         });

    client.registerBarkCallback([](std::string word)
                                {
                                    std::cout << "Received BARK signal: "
                                              << "word=" << word << std::endl;
                                });

    client.registerMaybeNumberCallback([](boost::optional<int> number)
                                       {
                                           std::cout << "Received MAYBE_NUMBER signal: "
                                                     << "number=" << *number << std::endl;
                                       });

    client.registerMaybeNameCallback([](boost::optional<std::string> name)
                                     {
                                         std::cout << "Received MAYBE_NAME signal: "
                                                   << "name=" << *name << std::endl;
                                     });

    client.registerNowCallback([](std::chrono::time_point<std::chrono::system_clock> timestamp)
                               {
                                   std::string timestampStr = timePointToIsoString(timestamp);

                                   std::cout << "Received NOW signal: "
                                             << "timestamp=" << timestampStr << std::endl;
                               });

    // Register callbacks for property updates.

    // Call each method with example values.

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        sleep(10);
    }

    return 0;
}