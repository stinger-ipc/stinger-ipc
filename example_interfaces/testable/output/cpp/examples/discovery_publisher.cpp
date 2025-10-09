#include <iostream>
#include <thread>
#include <chrono>
#include <sstream>
#include "broker.hpp"

int main(int argc, char** argv)
{
    if (argc < 2)
    {
        std::cout << "Usage: " << argv[0] << " <instance_id>" << std::endl;
        return 1;
    }

    std::string instance_id = argv[1];

    // Create a broker connection
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "Discovery-publisher");

    // Wait a moment for connection to establish
    std::this_thread::sleep_for(std::chrono::seconds(2));

    // Publish a discovery message
    std::stringstream json;
    json << "{\"instance\":\"" << instance_id << "\"}";

    std::cout << "Publishing discovery message for instance: " << instance_id << std::endl;
    std::cout << "Topic: myservice/myapp/interface" << std::endl;
    std::cout << "Payload: " << json.str() << std::endl;

    MqttProperties props;
    conn->Publish("myservice/myapp/interface", json.str(), 0, false, props);

    // Wait a moment for the message to be sent
    std::this_thread::sleep_for(std::chrono::seconds(2));

    std::cout << "Discovery message published!" << std::endl;

    return 0;
}