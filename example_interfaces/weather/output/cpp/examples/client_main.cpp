

#include <iostream>
#include <sstream>
#include <syslog.h>
#include <chrono>
#include <thread>
#include "utils.hpp"
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"
#include "discovery.hpp"
#include "enums.hpp"
#include "interface_exceptions.hpp"

int main(int argc, char** argv)
{
    // Create a connection to the broker
    auto conn = std::make_shared<MqttBrokerConnection>("localhost", 1883, "weather-client-demo");
    conn->SetLogLevel(LOG_DEBUG);
    conn->SetLogFunction([](int level, const char* msg)
                         {
                             std::cout << "[" << level << "] " << msg << std::endl;
                         });

    // Discover a service ID for a weather service.
    std::string serviceId;
    { // restrict scope
        WeatherDiscovery discovery(conn);
        auto serviceIdFut = discovery.GetSingleton();
        auto serviceIdFutStatus = serviceIdFut.wait_for(std::chrono::seconds(15));
        if (serviceIdFutStatus == std::future_status::timeout)
        {
            std::cerr << "Failed to discover service instance within timeout." << std::endl;
            return 1;
        }
        serviceId = serviceIdFut.get();
    }

    // Create the client object.
    WeatherClient client(conn, serviceId);

    // Register callbacks for signals.
    client.registerCurrentTimeCallback([](std::string currentTime)
                                       {
                                           std::cout << "Received CURRENT_TIME signal: "
                                                     << "current_time=" << currentTime << std::endl;
                                       });

    // Register callbacks for property updates.
    client.registerLocationPropertyCallback([](double latitude, double longitude)
                                            {
                                                std::cout << "Received update for location property: " << "latitude=" << latitude /* unhandled arg type*/ << " | " << "longitude=" << longitude /* unhandled arg type*/ << std::endl;
                                            });

    client.registerCurrentTemperaturePropertyCallback([](double temperatureF)
                                                      {
                                                          std::cout << "Received update for current_temperature property: " << "temperature_f=" << temperatureF /* unhandled arg type*/ << std::endl;
                                                      });

    client.registerCurrentConditionPropertyCallback([](WeatherCondition condition, std::string description)
                                                    {
                                                        std::cout << "Received update for current_condition property: " << "condition=" << weatherConditionStrings.at(static_cast<int>(condition))
                                                                  << " | " << "description=" << description /* unhandled arg type*/ << std::endl;
                                                    });

    client.registerDailyForecastPropertyCallback([](ForecastForDay monday, ForecastForDay tuesday, ForecastForDay wednesday)
                                                 {
                                                     std::cout << "Received update for daily_forecast property: " << "monday=" << "[ForecastForDay object]"
                                                               << " | " << "tuesday=" << "[ForecastForDay object]"
                                                               << " | " << "wednesday=" << "[ForecastForDay object]"
                                                               << std::endl;
                                                 });

    client.registerHourlyForecastPropertyCallback([](ForecastForHour hour0, ForecastForHour hour1, ForecastForHour hour2, ForecastForHour hour3)
                                                  {
                                                      std::cout << "Received update for hourly_forecast property: " << "hour_0=" << "[ForecastForHour object]"
                                                                << " | " << "hour_1=" << "[ForecastForHour object]"
                                                                << " | " << "hour_2=" << "[ForecastForHour object]"
                                                                << " | " << "hour_3=" << "[ForecastForHour object]"
                                                                << std::endl;
                                                  });

    client.registerCurrentConditionRefreshIntervalPropertyCallback([](int seconds)
                                                                   {
                                                                       std::cout << "Received update for current_condition_refresh_interval property: " << "seconds=" << seconds /* unhandled arg type*/ << std::endl;
                                                                   });

    client.registerHourlyForecastRefreshIntervalPropertyCallback([](int seconds)
                                                                 {
                                                                     std::cout << "Received update for hourly_forecast_refresh_interval property: " << "seconds=" << seconds /* unhandled arg type*/ << std::endl;
                                                                 });

    client.registerDailyForecastRefreshIntervalPropertyCallback([](int seconds)
                                                                {
                                                                    std::cout << "Received update for daily_forecast_refresh_interval property: " << "seconds=" << seconds /* unhandled arg type*/ << std::endl;
                                                                });

    // Call each method with example values.

    // ----------------------METHOD REFRESH_DAILY_FORECAST-----------------------------------------
    { // Restrict scope for the `refresh_daily_forecast` method call.
        std::cout << "CALLING REFRESH_DAILY_FORECAST" << std::endl;
        auto refreshDailyForecastResultFuture = client.refreshDailyForecast();
        auto refreshDailyForecastStatus = refreshDailyForecastResultFuture.wait_for(std::chrono::seconds(5));
        if (refreshDailyForecastStatus == std::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for REFRESH_DAILY_FORECAST response." << std::endl;
        }
        else
        {
            std::cout << "REFRESH_DAILY_FORECAST Completed.  It has not return values." << std::endl;
        }
    }

    // ----------------------METHOD REFRESH_HOURLY_FORECAST-----------------------------------------
    { // Restrict scope for the `refresh_hourly_forecast` method call.
        std::cout << "CALLING REFRESH_HOURLY_FORECAST" << std::endl;
        auto refreshHourlyForecastResultFuture = client.refreshHourlyForecast();
        auto refreshHourlyForecastStatus = refreshHourlyForecastResultFuture.wait_for(std::chrono::seconds(5));
        if (refreshHourlyForecastStatus == std::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for REFRESH_HOURLY_FORECAST response." << std::endl;
        }
        else
        {
            std::cout << "REFRESH_HOURLY_FORECAST Completed.  It has not return values." << std::endl;
        }
    }

    // ----------------------METHOD REFRESH_CURRENT_CONDITIONS-----------------------------------------
    { // Restrict scope for the `refresh_current_conditions` method call.
        std::cout << "CALLING REFRESH_CURRENT_CONDITIONS" << std::endl;
        auto refreshCurrentConditionsResultFuture = client.refreshCurrentConditions();
        auto refreshCurrentConditionsStatus = refreshCurrentConditionsResultFuture.wait_for(std::chrono::seconds(5));
        if (refreshCurrentConditionsStatus == std::future_status::timeout)
        {
            std::cout << "TIMEOUT after 5 seconds waiting for REFRESH_CURRENT_CONDITIONS response." << std::endl;
        }
        else
        {
            std::cout << "REFRESH_CURRENT_CONDITIONS Completed.  It has not return values." << std::endl;
        }
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }

    return 0;
}