/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/
use futures::executor::block_on;
use mqttier::MqttierClient;
use tokio::time::{Duration, sleep};
use weather_server::WeatherServer;

#[allow(unused_imports)]
use weather_types::payloads::{MethodResultCode, *};

fn refresh_daily_forecast_handler() -> Result<(), MethodResultCode> {
    println!("Handling refresh_daily_forecast");
    Ok(())
}

fn refresh_hourly_forecast_handler() -> Result<(), MethodResultCode> {
    println!("Handling refresh_hourly_forecast");
    Ok(())
}

fn refresh_current_conditions_handler() -> Result<(), MethodResultCode> {
    println!("Handling refresh_current_conditions");
    Ok(())
}

#[tokio::main]
async fn main() {
    env_logger::Builder::from_default_env()
        .target(env_logger::Target::Stdout)
        .init();

    block_on(async {
        let mut connection = MqttierClient::new("localhost", 1883, None).unwrap();
        let mut server = WeatherServer::new(&mut connection).await;

        println!("Setting initial value for property 'location'");
        let new_value = LocationProperty {
            latitude: 3.14,
            longitude: 3.14,
        };
        server.set_location(new_value).await;

        println!("Setting initial value for property 'current_temperature'");
        server.set_current_temperature(3.14).await;

        println!("Setting initial value for property 'current_condition'");
        let new_value = CurrentConditionProperty {
            condition: WeatherCondition::Sunny,
            description: "apples".to_string(),
        };
        server.set_current_condition(new_value).await;

        println!("Setting initial value for property 'daily_forecast'");
        let new_value = DailyForecastProperty {
            monday: ForecastForDay {
                high_temperature: 3.14,
                low_temperature: 3.14,
                condition: WeatherCondition::Sunny,
                start_time: "apples".to_string(),
                end_time: "apples".to_string(),
            },
            tuesday: ForecastForDay {
                high_temperature: 3.14,
                low_temperature: 3.14,
                condition: WeatherCondition::Sunny,
                start_time: "apples".to_string(),
                end_time: "apples".to_string(),
            },
            wednesday: ForecastForDay {
                high_temperature: 3.14,
                low_temperature: 3.14,
                condition: WeatherCondition::Sunny,
                start_time: "apples".to_string(),
                end_time: "apples".to_string(),
            },
        };
        server.set_daily_forecast(new_value).await;

        println!("Setting initial value for property 'hourly_forecast'");
        let new_value = HourlyForecastProperty {
            hour_0: ForecastForHour {
                temperature: 3.14,
                starttime: "apples".to_string(),
                condition: WeatherCondition::Sunny,
            },
            hour_1: ForecastForHour {
                temperature: 3.14,
                starttime: "apples".to_string(),
                condition: WeatherCondition::Sunny,
            },
            hour_2: ForecastForHour {
                temperature: 3.14,
                starttime: "apples".to_string(),
                condition: WeatherCondition::Sunny,
            },
            hour_3: ForecastForHour {
                temperature: 3.14,
                starttime: "apples".to_string(),
                condition: WeatherCondition::Sunny,
            },
        };
        server.set_hourly_forecast(new_value).await;

        println!("Setting initial value for property 'current_condition_refresh_interval'");
        server.set_current_condition_refresh_interval(42).await;

        println!("Setting initial value for property 'hourly_forecast_refresh_interval'");
        server.set_hourly_forecast_refresh_interval(42).await;

        println!("Setting initial value for property 'daily_forecast_refresh_interval'");
        server.set_daily_forecast_refresh_interval(42).await;

        server.set_method_handler_for_refresh_daily_forecast(refresh_daily_forecast_handler);

        server.set_method_handler_for_refresh_hourly_forecast(refresh_hourly_forecast_handler);

        server
            .set_method_handler_for_refresh_current_conditions(refresh_current_conditions_handler);

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'current_time'");
        server.emit_current_time("apples".to_string()).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'location'");
        let new_value = LocationProperty {
            latitude: 1.0,
            longitude: 1.0,
        };
        server.set_location(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'current_temperature'");
        server.set_current_temperature(1.0).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'current_condition'");
        let new_value = CurrentConditionProperty {
            condition: WeatherCondition::Sunny,
            description: "Joe".to_string(),
        };
        server.set_current_condition(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'daily_forecast'");
        let new_value = DailyForecastProperty {
            monday: ForecastForDay {
                high_temperature: 1.0,
                low_temperature: 1.0,
                condition: WeatherCondition::Sunny,
                start_time: "Joe".to_string(),
                end_time: "Joe".to_string(),
            },
            tuesday: ForecastForDay {
                high_temperature: 1.0,
                low_temperature: 1.0,
                condition: WeatherCondition::Sunny,
                start_time: "Joe".to_string(),
                end_time: "Joe".to_string(),
            },
            wednesday: ForecastForDay {
                high_temperature: 1.0,
                low_temperature: 1.0,
                condition: WeatherCondition::Sunny,
                start_time: "Joe".to_string(),
                end_time: "Joe".to_string(),
            },
        };
        server.set_daily_forecast(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'hourly_forecast'");
        let new_value = HourlyForecastProperty {
            hour_0: ForecastForHour {
                temperature: 1.0,
                starttime: "Joe".to_string(),
                condition: WeatherCondition::Sunny,
            },
            hour_1: ForecastForHour {
                temperature: 1.0,
                starttime: "Joe".to_string(),
                condition: WeatherCondition::Sunny,
            },
            hour_2: ForecastForHour {
                temperature: 1.0,
                starttime: "Joe".to_string(),
                condition: WeatherCondition::Sunny,
            },
            hour_3: ForecastForHour {
                temperature: 1.0,
                starttime: "Joe".to_string(),
                condition: WeatherCondition::Sunny,
            },
        };
        server.set_hourly_forecast(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'current_condition_refresh_interval'");
        server.set_current_condition_refresh_interval(2022).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'hourly_forecast_refresh_interval'");
        server.set_hourly_forecast_refresh_interval(2022).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'daily_forecast_refresh_interval'");
        server.set_daily_forecast_refresh_interval(2022).await;
        let _server_loop_task = server.receive_loop().await;
    });
    // Ctrl-C to stop
}
