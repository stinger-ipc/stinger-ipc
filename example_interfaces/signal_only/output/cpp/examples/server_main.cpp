
#include <iostream>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<DefaultConnection>("localhost", 1883, "SignalOnly");
    SignalOnlyServer server(conn);
    auto anotherSignalFuture = server.emitAnotherSignalSignal(3.14, true, "apples");
    auto barkFuture = server.emitBarkSignal("apples");
    auto maybe_numberFuture = server.emitMaybeNumberSignal(42);
    auto maybe_nameFuture = server.emitMaybeNameSignal(boost::make_optional(std::string("apples")));
    anotherSignalFuture.wait();
    barkFuture.wait();
    maybe_numberFuture.wait();
    maybe_nameFuture.wait();
    std::cout << "Press Enter to exit\n";
    std::cin.ignore();
    return 0;
}