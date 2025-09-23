/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/
use futures::executor::block_on;
use mqttier::MqttierClient;
use std::any::Any;
use tokio::time::{Duration, sleep};
use weather_server::{WeatherMethodHandlers, WeatherServer};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;

use weather_types::MethodReturnCode;
#[allow(unused_imports)]
use weather_types::payloads::*;

struct WeatherMethodImpl {
    server: Option<WeatherServer>,
}

impl WeatherMethodImpl {
    fn new() -> Self {
        Self { server: None }
    }
}

#[async_trait]
impl WeatherMethodHandlers for WeatherMethodImpl {
    async fn initialize(&mut self, server: WeatherServer) -> Result<(), MethodReturnCode> {
        self.server = Some(server.clone());
        Ok(())
    }

    async fn handle_refresh_daily_forecast(&self) -> Result<(), MethodReturnCode> {
        println!("Handling refresh_daily_forecast");
        Ok(())
    }

    async fn handle_refresh_hourly_forecast(&self) -> Result<(), MethodReturnCode> {
        println!("Handling refresh_hourly_forecast");
        Ok(())
    }

    async fn handle_refresh_current_conditions(&self) -> Result<(), MethodReturnCode> {
        println!("Handling refresh_current_conditions");
        Ok(())
    }

    fn as_any(&self) -> &dyn Any {
        self
    }
}

#[tokio::main]
async fn main() {
    env_logger::Builder::from_default_env()
        .target(env_logger::Target::Stdout)
        .init();

    block_on(async {
        let mut connection = MqttierClient::new("localhost", 1883, None).unwrap();

        let handlers: Arc<Mutex<Box<dyn WeatherMethodHandlers>>> =
            Arc::new(Mutex::new(Box::new(WeatherMethodImpl::new())));
        let mut server = WeatherServer::new(&mut connection, handlers.clone()).await;

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

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'current_time'");
        let signal_result_future = server.emit_current_time("apples".to_string()).await;
        let signal_result = signal_result_future.await;
        println!("Signal 'current_time' was sent: {:?}", signal_result);

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
        let _server_loop_task = server.run_loop().await;
    });
    // Ctrl-C to stop
}
