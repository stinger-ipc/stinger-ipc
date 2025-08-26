
#include <iostream>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv) {

    
    auto conn = std::make_shared<DefaultConnection>("localhost", 1883, "WeatherClient-demo");
    WeatherClient client(conn);
    client.registerCurrentTimeCallback([](const std::string& current_time) {
        std::cout << "current_time=" <<current_time <<  std::endl;
    });
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

    while (true) {
        sleep(10);
    }

    return 0;
}