#include <iostream>
#include <thread>
#include <chrono>
#include "discovery.hpp"
#include <stinger/mqtt/brokerconnection.hpp>

using namespace stinger::gen::simple;

int main(int argc, char** argv)
{
    // Create a broker connection
    auto conn = std::make_shared<stinger::mqtt::BrokerConnection>("localhost", 1883, "Discovery-example");

    // Create a Discovery instance for service "myapp"
    SimpleDiscovery discovery(conn);

    // Set up a callback for when new services are discovered
    discovery.SetDiscoveryCallback([](const InstanceInfo& info)
                                   {
                                       std::cout << "New service instance discovered: " << info.serviceId.value_or("error") << std::endl;
                                   });

    // Try to get a singleton instance
    std::cout << "Waiting for a service instance..." << std::endl;
    auto future = discovery.GetSingleton();

    // Wait for the future to resolve (with a timeout)
    auto status = future.wait_for(std::chrono::seconds(10));

    if (status == std::future_status::ready) {
        InstanceInfo info = future.get();
        std::cout << "Got singleton instance: " << info.serviceId.value_or("error") << std::endl;

        // Get all discovered instances
        auto allInstances = discovery.GetInstances();
        std::cout << "Total instances discovered: " << allInstances.size() << std::endl;
        for (const auto& info: allInstances) {
            std::cout << "  - " << info.serviceId.value_or("error") << std::endl;
        }
    } else {
        std::cout << "Timeout waiting for service instance" << std::endl;
    }

    // Keep the program running to receive more discoveries
    std::cout << "Continuing to listen for discoveries (press Ctrl+C to exit)..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(30));

    return 0;
}