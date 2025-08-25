/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/
use futures::{executor::block_on};
use weather_server::WeatherServer;
use connection::Connection;
use tokio::time::{sleep, Duration};
use tokio::join;
use connection::payloads::{MethodResultCode, *};


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
    block_on(async {
        
        let mut connection = Connection::new_default_connection().await.unwrap();
        let mut server = WeatherServer::new(&mut connection).await;

        let loop_task = tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = connection.start_loop().await;
        });
        
        println!("Setting initial value for property 'location'");
        let new_value = connection::payloads::LocationProperty {
                latitude: 3.14,
                longitude: 3.14,
        };
        server.set_location(new_value).await;
        
        
        println!("Setting initial value for property 'current_temperature'");
        server.set_current_temperature(3.14).await;
        
        println!("Setting initial value for property 'current_condition'");
        let new_value = connection::payloads::CurrentConditionProperty {
                condition: connection::payloads::WeatherCondition::Sunny,
                description: "apples".to_string(),
        };
        server.set_current_condition(new_value).await;
        
        
        println!("Setting initial value for property 'daily_forecast'");
        let new_value = connection::payloads::DailyForecastProperty {
                monday: connection::payloads::ForecastForDay {high_temperature: 3.14, low_temperature: 3.14, condition: connection::payloads::WeatherCondition::Sunny, start_time: "apples".to_string(), end_time: "apples".to_string()},
                tuesday: connection::payloads::ForecastForDay {high_temperature: 3.14, low_temperature: 3.14, condition: connection::payloads::WeatherCondition::Sunny, start_time: "apples".to_string(), end_time: "apples".to_string()},
                wednesday: connection::payloads::ForecastForDay {high_temperature: 3.14, low_temperature: 3.14, condition: connection::payloads::WeatherCondition::Sunny, start_time: "apples".to_string(), end_time: "apples".to_string()},
        };
        server.set_daily_forecast(new_value).await;
        
        
        println!("Setting initial value for property 'hourly_forecast'");
        let new_value = connection::payloads::HourlyForecastProperty {
                hour_0: connection::payloads::ForecastForHour {temperature: 3.14, starttime: "apples".to_string(), condition: connection::payloads::WeatherCondition::Sunny},
                hour_1: connection::payloads::ForecastForHour {temperature: 3.14, starttime: "apples".to_string(), condition: connection::payloads::WeatherCondition::Sunny},
                hour_2: connection::payloads::ForecastForHour {temperature: 3.14, starttime: "apples".to_string(), condition: connection::payloads::WeatherCondition::Sunny},
                hour_3: connection::payloads::ForecastForHour {temperature: 3.14, starttime: "apples".to_string(), condition: connection::payloads::WeatherCondition::Sunny},
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
        
        server.set_method_handler_for_refresh_current_conditions(refresh_current_conditions_handler);
        
        
        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'current_time'");
        server.emit_current_time("apples".to_string()).await;
        
        
        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'location'");
        let new_value = connection::payloads::LocationProperty {
                latitude: 1.0,
                longitude: 1.0,
        };
        server.set_location(new_value).await;
        
        
        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'current_temperature'");
        server.set_current_temperature(1.0).await;
        
        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'current_condition'");
        let new_value = connection::payloads::CurrentConditionProperty {
                condition: connection::payloads::WeatherCondition::Sunny,
                description: "Joe".to_string(),
        };
        server.set_current_condition(new_value).await;
        
        
        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'daily_forecast'");
        let new_value = connection::payloads::DailyForecastProperty {
                monday: connection::payloads::ForecastForDay {high_temperature: 1.0, low_temperature: 1.0, condition: connection::payloads::WeatherCondition::Sunny, start_time: "Joe".to_string(), end_time: "Joe".to_string()},
                tuesday: connection::payloads::ForecastForDay {high_temperature: 1.0, low_temperature: 1.0, condition: connection::payloads::WeatherCondition::Sunny, start_time: "Joe".to_string(), end_time: "Joe".to_string()},
                wednesday: connection::payloads::ForecastForDay {high_temperature: 1.0, low_temperature: 1.0, condition: connection::payloads::WeatherCondition::Sunny, start_time: "Joe".to_string(), end_time: "Joe".to_string()},
        };
        server.set_daily_forecast(new_value).await;
        
        
        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'hourly_forecast'");
        let new_value = connection::payloads::HourlyForecastProperty {
                hour_0: connection::payloads::ForecastForHour {temperature: 1.0, starttime: "Joe".to_string(), condition: connection::payloads::WeatherCondition::Sunny},
                hour_1: connection::payloads::ForecastForHour {temperature: 1.0, starttime: "Joe".to_string(), condition: connection::payloads::WeatherCondition::Sunny},
                hour_2: connection::payloads::ForecastForHour {temperature: 1.0, starttime: "Joe".to_string(), condition: connection::payloads::WeatherCondition::Sunny},
                hour_3: connection::payloads::ForecastForHour {temperature: 1.0, starttime: "Joe".to_string(), condition: connection::payloads::WeatherCondition::Sunny},
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
        server.receive_loop().await;
        join!(loop_task);
    });
    // Ctrl-C to stop
}