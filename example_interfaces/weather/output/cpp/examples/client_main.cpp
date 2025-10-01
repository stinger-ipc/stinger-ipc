

#include <iostream>
#include <boost/chrono/chrono.hpp>
#include "broker.hpp"
#include "client.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<MqttBrokerConnection>();
    WeatherClient client(conn);
    client.registerCurrentTimeCallback([](const std::string& current_time)
                                       { std::cout << "current_time=" << current_time << std::endl; });
    client.registerLocationPropertyCallback([](double latitude, double longitude)
                                            { std::cout << "Received update for location property: " << "latitude=" << latitude << " | " << "longitude=" << longitude << std::endl; });

    client.registerCurrentTemperaturePropertyCallback([](double temperature_f)
                                                      { std::cout << "Received update for current_temperature property: " << "temperature_f=" << temperature_f << std::endl; });

    client.registerCurrentConditionPropertyCallback([](WeatherCondition condition, const std::string& description)
                                                    { std::cout << "Received update for current_condition property: " << "condition=" << weatherConditionStrings[static_cast<int>(condition)]
                                                                << " | " << "description=" << description << std::endl; });

    client.registerDailyForecastPropertyCallback([](ForecastForDay monday, ForecastForDay tuesday, ForecastForDay wednesday)
                                                 { std::cout << "Received update for daily_forecast property: " << "monday=" << "[ForecastForDay object]" << " | " << "tuesday=" << "[ForecastForDay object]" << " | " << "wednesday=" << "[ForecastForDay object]" << std::endl; });

    client.registerHourlyForecastPropertyCallback([](ForecastForHour hour_0, ForecastForHour hour_1, ForecastForHour hour_2, ForecastForHour hour_3)
                                                  { std::cout << "Received update for hourly_forecast property: " << "hour_0=" << "[ForecastForHour object]" << " | " << "hour_1=" << "[ForecastForHour object]" << " | " << "hour_2=" << "[ForecastForHour object]" << " | " << "hour_3=" << "[ForecastForHour object]" << std::endl; });

    client.registerCurrentConditionRefreshIntervalPropertyCallback([](int seconds)
                                                                   { std::cout << "Received update for current_condition_refresh_interval property: " << "seconds=" << seconds << std::endl; });

    client.registerHourlyForecastRefreshIntervalPropertyCallback([](int seconds)
                                                                 { std::cout << "Received update for hourly_forecast_refresh_interval property: " << "seconds=" << seconds << std::endl; });

    client.registerDailyForecastRefreshIntervalPropertyCallback([](int seconds)
                                                                { std::cout << "Received update for daily_forecast_refresh_interval property: " << "seconds=" << seconds << std::endl; });

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