
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

    auto server = std::make_shared<WeatherServer>(conn, "cpp-server-demo:1");

    std::cout << "Setting initial value for property 'location'.\n";
    server->updateLocationProperty(3.14, 3.14);

    std::cout << "Setting initial value for property 'current_temperature'.\n";
    server->updateCurrentTemperatureProperty(3.14);

    std::cout << "Setting initial value for property 'current_condition'.\n";
    server->updateCurrentConditionProperty(WeatherCondition::SNOWY, "apples");

    std::cout << "Setting initial value for property 'daily_forecast'.\n";
    server->updateDailyForecastProperty(ForecastForDay{ 3.14, 3.14, WeatherCondition::SNOWY, "apples", "apples" }, ForecastForDay{ 3.14, 3.14, WeatherCondition::SNOWY, "apples", "apples" }, ForecastForDay{ 3.14, 3.14, WeatherCondition::SNOWY, "apples", "apples" });

    std::cout << "Setting initial value for property 'hourly_forecast'.\n";
    server->updateHourlyForecastProperty(ForecastForHour{ 3.14, std::chrono::system_clock::now(), WeatherCondition::SNOWY }, ForecastForHour{ 3.14, std::chrono::system_clock::now(), WeatherCondition::SNOWY }, ForecastForHour{ 3.14, std::chrono::system_clock::now(), WeatherCondition::SNOWY }, ForecastForHour{ 3.14, std::chrono::system_clock::now(), WeatherCondition::SNOWY });

    std::cout << "Setting initial value for property 'current_condition_refresh_interval'.\n";
    server->updateCurrentConditionRefreshIntervalProperty(42);

    std::cout << "Setting initial value for property 'hourly_forecast_refresh_interval'.\n";
    server->updateHourlyForecastRefreshIntervalProperty(42);

    std::cout << "Setting initial value for property 'daily_forecast_refresh_interval'.\n";
    server->updateDailyForecastRefreshIntervalProperty(42);

    auto current_timeFuture = server->emitCurrentTimeSignal("apples");
    current_timeFuture.wait();
    server->registerRefreshDailyForecastHandler([]() -> void
                                                {
                                                    std::cout << "Received call for refresh_daily_forecast\n";
                                                });

    server->registerRefreshHourlyForecastHandler([]() -> void
                                                 {
                                                     std::cout << "Received call for refresh_hourly_forecast\n";
                                                 });

    server->registerRefreshCurrentConditionsHandler([]() -> void
                                                    {
                                                        std::cout << "Received call for refresh_current_conditions\n";
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
                                            auto current_timeFuture = server->emitCurrentTimeSignal("apples");
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                            current_timeFuture.wait();
                                        }
                                        catch (...)
                                        {
                                        }

                                        std::cout << "Periodic update iteration " << loopCount << " complete. Sleeping for 59 ...\n";

                                        // Sleep in 1-second increments so we can stop quickly
                                        for (int i = 0; i < 59 && keepRunning; ++i)
                                        {
                                            std::this_thread::sleep_for(std::chrono::seconds(1));
                                        }

                                        if (loopCount % 3 == 0)
                                        {
                                            std::cout << "Updating value for property 'location'.\n";
                                            server->updateLocationProperty(3.14, 3.14);

                                            std::cout << "Updating value for property 'current_temperature'.\n";
                                            server->updateCurrentTemperatureProperty(3.14);

                                            std::cout << "Updating value for property 'current_condition'.\n";
                                            server->updateCurrentConditionProperty(WeatherCondition::SNOWY, "apples");

                                            std::cout << "Updating value for property 'daily_forecast'.\n";
                                            server->updateDailyForecastProperty(ForecastForDay{ 3.14, 3.14, WeatherCondition::SNOWY, "apples", "apples" }, ForecastForDay{ 3.14, 3.14, WeatherCondition::SNOWY, "apples", "apples" }, ForecastForDay{ 3.14, 3.14, WeatherCondition::SNOWY, "apples", "apples" });

                                            std::cout << "Updating value for property 'hourly_forecast'.\n";
                                            server->updateHourlyForecastProperty(ForecastForHour{ 3.14, std::chrono::system_clock::now(), WeatherCondition::SNOWY }, ForecastForHour{ 3.14, std::chrono::system_clock::now(), WeatherCondition::SNOWY }, ForecastForHour{ 3.14, std::chrono::system_clock::now(), WeatherCondition::SNOWY }, ForecastForHour{ 3.14, std::chrono::system_clock::now(), WeatherCondition::SNOWY });

                                            std::cout << "Updating value for property 'current_condition_refresh_interval'.\n";
                                            server->updateCurrentConditionRefreshIntervalProperty(42);

                                            std::cout << "Updating value for property 'hourly_forecast_refresh_interval'.\n";
                                            server->updateHourlyForecastRefreshIntervalProperty(42);

                                            std::cout << "Updating value for property 'daily_forecast_refresh_interval'.\n";
                                            server->updateDailyForecastRefreshIntervalProperty(42);
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