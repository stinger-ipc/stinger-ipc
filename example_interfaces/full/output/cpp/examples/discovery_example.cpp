#include <iostream>
#include <thread>
#include <chrono>
#include "broker.hpp"
#include "discovery.hpp"

int main(int argc, char** argv)
{
    // Create a broker connection
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "Discovery-example");

    // Create a Discovery instance for service "myapp"
    FullDiscovery discovery(conn);

    // Set up a callback for when new services are discovered
    discovery.SetDiscoveryCallback([](const std::string& instance_id)
                                   {
                                       std::cout << "New service instance discovered: " << instance_id << std::endl;
                                   });

    // Try to get a singleton instance
    std::cout << "Waiting for a service instance..." << std::endl;
    auto future = discovery.GetSingleton();

    // Wait for the future to resolve (with a timeout)
    auto status = future.wait_for(boost::chrono::seconds(10));

    if (status == boost::future_status::ready)
    {
        std::string instance_id = future.get();
        std::cout << "Got singleton instance: " << instance_id << std::endl;

        // Get all discovered instances
        auto all_instances = discovery.GetInstanceIds();
        std::cout << "Total instances discovered: " << all_instances.size() << std::endl;
        for (const auto& id: all_instances)
        {
            std::cout << "  - " << id << std::endl;
        }
    }
    else
    {
        std::cout << "Timeout waiting for service instance" << std::endl;
    }

    // Keep the program running to receive more discoveries
    std::cout << "Continuing to listen for discoveries (press Ctrl+C to exit)..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(30));

    return 0;
}