/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use std::any::Any;

use mqttier::{Connection, MqttierClient, MqttierOptionsBuilder};
use tokio::time::{sleep, Duration};
use weather_ipc::property::WeatherInitialPropertyValues;
use weather_ipc::server::{WeatherMethodHandlers, WeatherServer};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing_subscriber;

use tokio::join;
#[allow(unused_imports)]
use weather_ipc::payloads::{MethodReturnCode, *};

struct WeatherMethodImpl {
    server: Option<WeatherServer<MqttierClient>>,
}

impl WeatherMethodImpl {
    fn new() -> Self {
        Self { server: None }
    }
}

#[async_trait]
impl WeatherMethodHandlers<MqttierClient> for WeatherMethodImpl {
    async fn initialize(
        &mut self,
        server: WeatherServer<MqttierClient>,
    ) -> Result<(), MethodReturnCode> {
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
    // Initialize tracing subscriber to see log output
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    // Set up an MQTT client connection.
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-server-demo".to_string())
        .build()
        .unwrap();
    let mut connection = MqttierClient::new(mqttier_options).unwrap();
    let _ = connection.start().await.unwrap();

    let initial_property_values = WeatherInitialPropertyValues {
        location: LocationProperty {
            latitude: 3.14,
            longitude: 3.14,
        },
        location_version: 1,

        current_temperature: 3.14,
        current_temperature_version: 1,

        current_condition: CurrentConditionProperty {
            condition: WeatherCondition::Snowy,
            description: "apples".to_string(),
        },
        current_condition_version: 1,

        daily_forecast: DailyForecastProperty {
            monday: ForecastForDay {
                high_temperature: 3.14,
                low_temperature: 3.14,
                condition: WeatherCondition::Snowy,
                start_time: "apples".to_string(),
                end_time: "apples".to_string(),
            },
            tuesday: ForecastForDay {
                high_temperature: 3.14,
                low_temperature: 3.14,
                condition: WeatherCondition::Snowy,
                start_time: "apples".to_string(),
                end_time: "apples".to_string(),
            },
            wednesday: ForecastForDay {
                high_temperature: 3.14,
                low_temperature: 3.14,
                condition: WeatherCondition::Snowy,
                start_time: "apples".to_string(),
                end_time: "apples".to_string(),
            },
        },
        daily_forecast_version: 1,

        hourly_forecast: HourlyForecastProperty {
            hour_0: ForecastForHour {
                temperature: 3.14,
                starttime: chrono::Utc::now(),
                condition: WeatherCondition::Snowy,
            },
            hour_1: ForecastForHour {
                temperature: 3.14,
                starttime: chrono::Utc::now(),
                condition: WeatherCondition::Snowy,
            },
            hour_2: ForecastForHour {
                temperature: 3.14,
                starttime: chrono::Utc::now(),
                condition: WeatherCondition::Snowy,
            },
            hour_3: ForecastForHour {
                temperature: 3.14,
                starttime: chrono::Utc::now(),
                condition: WeatherCondition::Snowy,
            },
        },
        hourly_forecast_version: 1,

        current_condition_refresh_interval: 42,
        current_condition_refresh_interval_version: 1,

        hourly_forecast_refresh_interval: 42,
        hourly_forecast_refresh_interval_version: 1,

        daily_forecast_refresh_interval: 42,
        daily_forecast_refresh_interval_version: 1,
    };

    // Create an object that implements the method handlers.
    let handlers: Arc<Mutex<Box<dyn WeatherMethodHandlers<MqttierClient>>>> =
        Arc::new(Mutex::new(Box::new(WeatherMethodImpl::new())));

    // Create the server object.
    let mut server = WeatherServer::new(
        connection,
        handlers.clone(),
        "rust-server-demo:1".to_string(),
        initial_property_values,
        "example".to_string(),
    )
    .await;

    // Start the server connection loop in a separate task.
    let mut looping_server = server.clone();
    let _loop_join_handle = tokio::spawn(async move {
        println!("Starting connection loop");
        let _conn_loop = looping_server.run_loop().await;
    });

    let mut server_clone1 = server.clone();
    let signal_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'current_time'");
            let signal_result_future = server_clone1.emit_current_time("apples".to_string()).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'current_time' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(67)).await;
        }
    });

    // Provide property handles to the property_publish_task which will use them to continuously update property values.

    let location_property = server.get_location_handle();

    let current_temperature_property = server.get_current_temperature_handle();

    let current_condition_property = server.get_current_condition_handle();

    let daily_forecast_property = server.get_daily_forecast_handle();

    let hourly_forecast_property = server.get_hourly_forecast_handle();

    let current_condition_refresh_interval_property =
        server.get_current_condition_refresh_interval_handle();

    let hourly_forecast_refresh_interval_property =
        server.get_hourly_forecast_refresh_interval_handle();

    let daily_forecast_refresh_interval_property =
        server.get_daily_forecast_refresh_interval_handle();
    let property_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(51)).await;

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'location'");
                let mut location_guard = location_property.write().await;
                let new_location_value = LocationProperty {
                    latitude: 1.0,
                    longitude: 1.0,
                };
                *location_guard = new_location_value;
                // Value is changed and published when location_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'current_temperature'");
                let mut current_temperature_guard = current_temperature_property.write().await;
                *current_temperature_guard = 1.0;
                // Value is changed and published when current_temperature_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'current_condition'");
                let mut current_condition_guard = current_condition_property.write().await;
                let new_current_condition_value = CurrentConditionProperty {
                    condition: WeatherCondition::Sunny,
                    description: "foo".to_string(),
                };
                *current_condition_guard = new_current_condition_value;
                // Value is changed and published when current_condition_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'daily_forecast'");
                let mut daily_forecast_guard = daily_forecast_property.write().await;
                let new_daily_forecast_value = DailyForecastProperty {
                    monday: ForecastForDay {
                        high_temperature: 1.0,
                        low_temperature: 1.0,
                        condition: WeatherCondition::Sunny,
                        start_time: "foo".to_string(),
                        end_time: "foo".to_string(),
                    },
                    tuesday: ForecastForDay {
                        high_temperature: 1.0,
                        low_temperature: 1.0,
                        condition: WeatherCondition::Sunny,
                        start_time: "foo".to_string(),
                        end_time: "foo".to_string(),
                    },
                    wednesday: ForecastForDay {
                        high_temperature: 1.0,
                        low_temperature: 1.0,
                        condition: WeatherCondition::Sunny,
                        start_time: "foo".to_string(),
                        end_time: "foo".to_string(),
                    },
                };
                *daily_forecast_guard = new_daily_forecast_value;
                // Value is changed and published when daily_forecast_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'hourly_forecast'");
                let mut hourly_forecast_guard = hourly_forecast_property.write().await;
                let new_hourly_forecast_value = HourlyForecastProperty {
                    hour_0: ForecastForHour {
                        temperature: 1.0,
                        starttime: chrono::Utc::now(),
                        condition: WeatherCondition::Sunny,
                    },
                    hour_1: ForecastForHour {
                        temperature: 1.0,
                        starttime: chrono::Utc::now(),
                        condition: WeatherCondition::Sunny,
                    },
                    hour_2: ForecastForHour {
                        temperature: 1.0,
                        starttime: chrono::Utc::now(),
                        condition: WeatherCondition::Sunny,
                    },
                    hour_3: ForecastForHour {
                        temperature: 1.0,
                        starttime: chrono::Utc::now(),
                        condition: WeatherCondition::Sunny,
                    },
                };
                *hourly_forecast_guard = new_hourly_forecast_value;
                // Value is changed and published when hourly_forecast_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'current_condition_refresh_interval'");
                let mut current_condition_refresh_interval_guard =
                    current_condition_refresh_interval_property.write().await;
                *current_condition_refresh_interval_guard = 2022;
                // Value is changed and published when current_condition_refresh_interval_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'hourly_forecast_refresh_interval'");
                let mut hourly_forecast_refresh_interval_guard =
                    hourly_forecast_refresh_interval_property.write().await;
                *hourly_forecast_refresh_interval_guard = 2022;
                // Value is changed and published when hourly_forecast_refresh_interval_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'daily_forecast_refresh_interval'");
                let mut daily_forecast_refresh_interval_guard =
                    daily_forecast_refresh_interval_property.write().await;
                *daily_forecast_refresh_interval_guard = 2022;
                // Value is changed and published when daily_forecast_refresh_interval_guard goes out of scope and is dropped.
            }
        }
    });

    let _ = join!(signal_publish_task, property_publish_task);

    // Ctrl-C to stop
}
