
#include <iostream>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<DefaultConnection>("localhost", 1883, "SignalOnlyServe-demo");
    SignalOnlyServer server(conn);
    auto anotherSignalFuture = server.emitAnotherSignalSignal(3.14, true, "apples");
    anotherSignalFuture.wait();
    std::cout << "Press Enter to exit\n"; 
    std::cin.ignore();
    return 0;
}