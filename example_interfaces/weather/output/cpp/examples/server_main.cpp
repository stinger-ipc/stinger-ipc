
#include <iostream>

#include "broker.hpp"
#include "server.hpp"
#include "enums.hpp"

int main(int argc, char** argv)
{
    auto conn = std::make_shared<MqttBrokerConnection>();
    WeatherServer server(conn);
    auto current_timeFuture = server.emitCurrentTimeSignal("apples");
    current_timeFuture.wait();
    server.registerRefreshDailyForecastHandler([]() -> void
                                               { std::cout << "Received call for refresh_daily_forecast\n"; });

    server.registerRefreshHourlyForecastHandler([]() -> void
                                                { std::cout << "Received call for refresh_hourly_forecast\n"; });

    server.registerRefreshCurrentConditionsHandler([]() -> void
                                                   { std::cout << "Received call for refresh_current_conditions\n"; });

    std::cout << "Press Enter to exit\n";
    std::cin.ignore();
    return 0;
}