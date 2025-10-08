
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

    auto server = std::make_shared<FullServer>(conn, "cpp-server-demo:1");
    auto todayIsFuture = server->emitTodayIsSignal(42, DayOfTheWeek::SATURDAY, std::chrono::system_clock::now(), std::chrono::duration<double>(3536), { 101, 120, 97, 109, 112, 108, 101 });
    todayIsFuture.wait();
    server->registerAddNumbersHandler([](int unused1, int unused2, boost::optional<int> unused3) -> int
                                      {
                                          std::cout << "Received call for addNumbers\n";
                                          return 42;
                                      });

    server->registerDoSomethingHandler([](const std::string& unused1) -> DoSomethingReturnValue
                                       {
                                           std::cout << "Received call for doSomething\n";
                                           return DoSomethingReturnValue{ "apples", 42, DayOfTheWeek::SATURDAY };
                                       });

    server->registerEchoHandler([](const std::string& unused1) -> std::string
                                {
                                    std::cout << "Received call for echo\n";
                                    return "apples";
                                });

    server->registerWhatTimeIsItHandler([](std::chrono::time_point<std::chrono::system_clock> unused1) -> std::chrono::time_point<std::chrono::system_clock>
                                        {
                                            std::cout << "Received call for what_time_is_it\n";
                                            return std::chrono::system_clock::now();
                                        });

    server->registerSetTheTimeHandler([](std::chrono::time_point<std::chrono::system_clock> unused1, std::chrono::time_point<std::chrono::system_clock> unused2) -> SetTheTimeReturnValue
                                      {
                                          std::cout << "Received call for set_the_time\n";
                                          return SetTheTimeReturnValue{ std::chrono::system_clock::now(), "apples" };
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

    std::cout << "Press ANY KEY to exit\n";
    std::cin.ignore();
    return 0;
}