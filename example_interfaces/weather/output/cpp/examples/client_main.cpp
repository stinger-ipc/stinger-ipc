

#include <iostream>
#include <sstream>
#include <syslog.h>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"
#include "structs.hpp"
#include "discovery.hpp"

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
        auto serviceIdFutStatus = serviceIdFut.wait_for(boost::chrono::seconds(15));
        if (serviceIdFutStatus == boost::future_status::timeout)
        {
            std::cerr << "Failed to discover service instance within timeout." << std::endl;
            return 1;
        }
        serviceId = serviceIdFut.get();
    }

    // Create the client object.
    WeatherClient client(conn, serviceId);

    // Register callbacks for signals.
    client.registerCurrentTimeCallback([](const std::string& current_time)
                                       {
                                           std::cout << "Received CURRENT_TIME signal: " << "current_time=" << current_time << std::endl;
                                       });

    // Register callbacks for property updates.
    client.registerLocationPropertyCallback([](double latitude, double longitude)
                                            {
                                                std::cout << "Received update for location property: " << "latitude=" << latitude /* unhandled arg type*/ << " | " << "longitude=" << longitude /* unhandled arg type*/ << std::endl;
                                            });

    client.registerCurrentTemperaturePropertyCallback([](double temperature_f)
                                                      {
                                                          std::cout << "Received update for current_temperature property: " << "temperature_f=" << temperature_f /* unhandled arg type*/ << std::endl;
                                                      });

    client.registerCurrentConditionPropertyCallback([](WeatherCondition condition, const std::string& description)
                                                    {
                                                        std::cout << "Received update for current_condition property: " << "condition=" << weatherConditionStrings[static_cast<int>(condition)]
                                                                  << " | " << "description=" << description /* unhandled arg type*/ << std::endl;
                                                    });

    client.registerDailyForecastPropertyCallback([](ForecastForDay monday, ForecastForDay tuesday, ForecastForDay wednesday)
                                                 {
                                                     std::cout << "Received update for daily_forecast property: " << "monday=" << "[ForecastForDay object]"
                                                               << " | " << "tuesday=" << "[ForecastForDay object]"
                                                               << " | " << "wednesday=" << "[ForecastForDay object]"
                                                               << std::endl;
                                                 });

    client.registerHourlyForecastPropertyCallback([](ForecastForHour hour_0, ForecastForHour hour_1, ForecastForHour hour_2, ForecastForHour hour_3)
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
    std::cout << "Calling refresh_daily_forecast" << std::endl;
    auto refreshDailyForecastResultFuture = client.refreshDailyForecast();
    auto refreshDailyForecastStatus = refreshDailyForecastResultFuture.wait_for(boost::chrono::seconds(5));
    if (refreshDailyForecastStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for refresh_daily_forecast response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling refresh_hourly_forecast" << std::endl;
    auto refreshHourlyForecastResultFuture = client.refreshHourlyForecast();
    auto refreshHourlyForecastStatus = refreshHourlyForecastResultFuture.wait_for(boost::chrono::seconds(5));
    if (refreshHourlyForecastStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for refresh_hourly_forecast response." << std::endl;
    }
    else
    {
    }
    std::cout << "Calling refresh_current_conditions" << std::endl;
    auto refreshCurrentConditionsResultFuture = client.refreshCurrentConditions();
    auto refreshCurrentConditionsStatus = refreshCurrentConditionsResultFuture.wait_for(boost::chrono::seconds(5));
    if (refreshCurrentConditionsStatus == boost::future_status::timeout)
    {
        std::cout << "TIMEOUT after 5 seconds waiting for refresh_current_conditions response." << std::endl;
    }
    else
    {
    }

    std::cout << "Connected and waiting.  Use Ctrl-C to exit." << std::endl;

    while (true)
    {
        sleep(10);
    }

    return 0;
}