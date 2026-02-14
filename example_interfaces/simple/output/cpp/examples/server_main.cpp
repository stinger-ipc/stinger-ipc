
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

    auto server = std::make_shared<SimpleServer>(conn, "cpp-server-demo:1");

    std::cout << "Setting initial value for property 'school'.\n";
    server->updateSchoolProperty("apples");

    auto person_enteredFuture = server->emitPersonEnteredSignal(Person{ "apples", Gender::MALE });
    person_enteredFuture.wait();
    server->registerTradeNumbersHandler([](int unused1) -> int
                                        {
                                            std::cout << "Received call for trade_numbers\n";
                                            return 42;
                                        });

    // Start a background thread that emits signals every 60 seconds.
    std::atomic<bool> keepRunning{ true };
    std::thread periodicEmitter([server, &keepRunning]()
                                {
                                    int loopCount = 0;
                                    while (keepRunning) {
                                        loopCount++;
                                        // Call emitTodayIsSignal; do not block forever waiting for publish
                                        try {
                                            auto person_enteredFuture = server->emitPersonEnteredSignal(Person{ "apples", Gender::MALE });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            person_enteredFuture.wait();
                                        } catch (...) { }

                                        std::cout << "Periodic update iteration " << loopCount << " complete. Sleeping for 59 ...\n";

                                        // Sleep in 1-second increments so we can stop quickly
                                        for (int i = 0; i < 59 && keepRunning; ++i) {
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                        }

                                        if (loopCount % 3 == 0) {
                                            std::cout << "Updating value for property 'school'.\n";
                                            server->updateSchoolProperty("apples");
                                        }
                                    }
                                });

    std::cout << "Press ENTER to exit\n";
    std::cin.ignore();

    // Signal the emitter thread to stop and join it
    keepRunning = false;
    if (periodicEmitter.joinable()) {
        periodicEmitter.join();
    }

    return 0;
}