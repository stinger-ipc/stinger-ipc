
#include <iostream>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<DefaultConnection>("localhost", 1883);
    SignalOnlyServer server(conn);
    server.emitAnotherSignalSignal(3.14, True, "apples");

    return 0;
}