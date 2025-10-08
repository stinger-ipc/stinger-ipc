
#include <iostream>
#include <syslog.h>
#include <thread>
#include <atomic>

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

    // Start a background thread that emits signals every 60 seconds.
    std::atomic<bool> keepRunning{ true };
    std::thread periodicEmitter([server, &keepRunning]()
                                {
                                    int loopCount = 0;
                                    while (keepRunning)
                                    {
                                        loopCount++;
                                        // Call emitTodayIsSignal; do not block forever waiting for publish
                                        try
                                        {
                                            auto anotherSignalFuture = server->emitAnotherSignalSignal(3.14, true, "apples");
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto barkFuture = server->emitBarkSignal("apples");
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto maybe_numberFuture = server->emitMaybeNumberSignal(42);
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto maybe_nameFuture = server->emitMaybeNameSignal(boost::make_optional(std::string("apples")));
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            auto nowFuture = server->emitNowSignal(std::chrono::system_clock::now());
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            anotherSignalFuture.wait();
                                            barkFuture.wait();
                                            maybe_numberFuture.wait();
                                            maybe_nameFuture.wait();
                                            nowFuture.wait();
                                        }
                                        catch (...)
                                        {
                                        }

                                        // Sleep in 1-second increments so we can stop quickly
                                        for (int i = 0; i < 55 && keepRunning; ++i)
                                        {
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                        }

                                        if (loopCount % 3 == 0)
                                        {
                                        }
                                    }
                                });

    std::cout << "Press ENTER to exit\n";
    std::cin.ignore();

    // Signal the emitter thread to stop and join it
    keepRunning = false;
    if (periodicEmitter.joinable())
    {
        periodicEmitter.join();
    }

    return 0;
}