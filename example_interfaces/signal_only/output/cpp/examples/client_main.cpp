

#include <iostream>
#include <sstream>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<DefaultConnection>("localhost", 1883, "SignalOnlyClient-demo");
    SignalOnlyClient client(conn);
    client.registerAnotherSignalCallback([](double one, bool two, const std::string& three)
                                         { std::cout << "one=" << one << " | " << "two=" << two << " | " << "three=" << three << std::endl; });
    client.registerBarkCallback([](const std::string& word)
                                { std::cout << "word=" << word << std::endl; });
    client.registerMaybeNumberCallback([](boost::optional<int> number)
                                       { std::cout << "number=" << "None" << std::endl; });
    client.registerMaybeNameCallback([](boost::optional<std::string> name)
                                     { std::cout << "name=" << "None" << std::endl; });
    client.registerNowCallback([](std::chrono::time_point<std::chrono::system_clock> timestamp)
                               {
        
        std::string timestampStr = timePointToIsoString(timestamp);
        
        std::cout << "timestamp=" <<timestampStr <<  std::endl; });

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        sleep(10);
    }

    return 0;
}