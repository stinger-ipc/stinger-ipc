
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

    auto server = std::make_shared<FullServer>(conn, "cpp-server-demo:1");

    std::cout << "Setting initial value for property 'favorite_number'.\n";
    server->updateFavoriteNumberProperty(42);

    std::cout << "Setting initial value for property 'favorite_foods'.\n";
    server->updateFavoriteFoodsProperty("apples", 42, boost::make_optional(std::string("apples")));

    std::cout << "Setting initial value for property 'lunch_menu'.\n";
    server->updateLunchMenuProperty(Lunch{ true, "apples", 3.14, DayOfTheWeek::SATURDAY, 42, std::chrono::system_clock::now(), std::chrono::duration<double>(3536) }, Lunch{ true, "apples", 3.14, DayOfTheWeek::SATURDAY, 42, std::chrono::system_clock::now(), std::chrono::duration<double>(3536) });

    std::cout << "Setting initial value for property 'family_name'.\n";
    server->updateFamilyNameProperty("apples");

    std::cout << "Setting initial value for property 'last_breakfast_time'.\n";
    server->updateLastBreakfastTimeProperty(std::chrono::system_clock::now());

    std::cout << "Setting initial value for property 'breakfast_length'.\n";
    server->updateBreakfastLengthProperty(std::chrono::duration<double>(3536));

    std::cout << "Setting initial value for property 'last_birthdays'.\n";
    server->updateLastBirthdaysProperty(std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now(), 42);

    auto todayIsFuture = server->emitTodayIsSignal(42, DayOfTheWeek::SATURDAY, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
    todayIsFuture.wait();
    server->registerAddNumbersHandler([](int unused1, int unused2, boost::optional<int> unused3) -> int
                                      {
                                          std::cout << "Received call for addNumbers\n";
                                          return 42;
                                      });

    server->registerDoSomethingHandler([](std::string unused1) -> DoSomethingReturnValues
                                       {
                                           std::cout << "Received call for doSomething\n";
                                           return DoSomethingReturnValues{ "apples", 42, DayOfTheWeek::SATURDAY };
                                       });

    server->registerEchoHandler([](std::string unused1) -> std::string
                                {
                                    std::cout << "Received call for echo\n";
                                    return "apples";
                                });

    server->registerWhatTimeIsItHandler([](std::chrono::time_point<std::chrono::system_clock> unused1) -> std::chrono::time_point<std::chrono::system_clock>
                                        {
                                            std::cout << "Received call for what_time_is_it\n";
                                            return std::chrono::system_clock::now();
                                        });

    server->registerSetTheTimeHandler([](std::chrono::time_point<std::chrono::system_clock> unused1, std::chrono::time_point<std::chrono::system_clock> unused2) -> SetTheTimeReturnValues
                                      {
                                          std::cout << "Received call for set_the_time\n";
                                          return SetTheTimeReturnValues{ std::chrono::system_clock::now(), "apples" };
                                      });

    server->registerForwardTimeHandler([](std::chrono::duration<double> unused1) -> std::chrono::time_point<std::chrono::system_clock>
                                       {
                                           std::cout << "Received call for forward_time\n";
                                           return std::chrono::system_clock::now();
                                       });

    server->registerHowOffIsTheClockHandler([](std::chrono::time_point<std::chrono::system_clock> unused1) -> std::chrono::duration<double>
                                            {
                                                std::cout << "Received call for how_off_is_the_clock\n";
                                                return std::chrono::duration<double>(3536);
                                            });

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
                                            auto todayIsFuture = server->emitTodayIsSignal(42, DayOfTheWeek::SATURDAY, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), std::vector<uint8_t>{ 101, 120, 97, 109, 112, 108, 101 });
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            todayIsFuture.wait();
                                        }
                                        catch (...)
                                        {
                                        }

                                        // Sleep in 1-second increments so we can stop quickly
                                        for (int i = 0; i < 59 && keepRunning; ++i)
                                        {
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                        }

                                        if (loopCount % 3 == 0)
                                        {
                                            std::cout << "Updating value for property 'favorite_number'.\n";
                                            server->updateFavoriteNumberProperty(42);

                                            std::cout << "Updating value for property 'favorite_foods'.\n";
                                            server->updateFavoriteFoodsProperty("apples", 42, boost::make_optional(std::string("apples")));

                                            std::cout << "Updating value for property 'lunch_menu'.\n";
                                            server->updateLunchMenuProperty(Lunch{ true, "apples", 3.14, DayOfTheWeek::SATURDAY, 42, std::chrono::system_clock::now(), std::chrono::duration<double>(3536) }, Lunch{ true, "apples", 3.14, DayOfTheWeek::SATURDAY, 42, std::chrono::system_clock::now(), std::chrono::duration<double>(3536) });

                                            std::cout << "Updating value for property 'family_name'.\n";
                                            server->updateFamilyNameProperty("apples");

                                            std::cout << "Updating value for property 'last_breakfast_time'.\n";
                                            server->updateLastBreakfastTimeProperty(std::chrono::system_clock::now());

                                            std::cout << "Updating value for property 'breakfast_length'.\n";
                                            server->updateBreakfastLengthProperty(std::chrono::duration<double>(3536));

                                            std::cout << "Updating value for property 'last_birthdays'.\n";
                                            server->updateLastBirthdaysProperty(std::chrono::system_clock::now(), std::chrono::system_clock::now(), std::chrono::system_clock::now(), 42);
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