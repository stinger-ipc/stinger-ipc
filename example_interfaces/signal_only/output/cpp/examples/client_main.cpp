
#include <iostream>

#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<DefaultConnection>("localhost", 1883);
    SignalOnlyClient client(conn);
    client.registerAnotherSignalCallback([](double one, bool two, const std::string& three) {
        std::cout << "one=" << one << " | " << "two=" << two << " | " << "three=" << three <<  std::endl;
    });

    std::cout << "Connected and waiting" << std::endl;

    while (true) {
        std::cout << ".";
        sleep(10);
    }

    return 0;
}