
#include <iostream>
#include <syslog.h>
#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "cpp-server-demo");
    conn->SetLogLevel(LOG_DEBUG);
    conn->SetLogFunction([](int level, const char* msg)
                         {
                             std::cout << "[" << level << "] " << msg << std::endl;
                         });

    auto server = std::make_shared<SignalOnlyServer>(conn, "cpp-server-demo:1");
    auto anotherSignalFuture = server->emitAnotherSignalSignal(3.14, true, "apples");
    auto barkFuture = server->emitBarkSignal("apples");
    auto maybe_numberFuture = server->emitMaybeNumberSignal(42);
    auto maybe_nameFuture = server->emitMaybeNameSignal(boost::make_optional(std::string("apples")));
    auto nowFuture = server->emitNowSignal(std::chrono::system_clock::now());
    anotherSignalFuture.wait();
    barkFuture.wait();
    maybe_numberFuture.wait();
    maybe_nameFuture.wait();
    nowFuture.wait();
    std::cout << "Press ANY KEY to exit\n";
    std::cin.ignore();
    return 0;
}