/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/
use std::any::Any;

use mqttier::{Connection, MqttierClient, MqttierOptions};
use tokio::time::{sleep, Duration};
use weather_ipc::server::{WeatherMethodHandlers, WeatherServer};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing_subscriber;

use tokio::join;
#[allow(unused_imports)]
use weather_ipc::payloads::{MethodReturnCode, *};

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
    // Initialize tracing subscriber to see log output
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    let mqttier_options = MqttierOptions::new()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-server-demo".to_string())
        .build();
    let mut connection = MqttierClient::new(mqttier_options).unwrap();

    let handlers: Arc<Mutex<Box<dyn WeatherMethodHandlers>>> =
        Arc::new(Mutex::new(Box::new(WeatherMethodImpl::new())));

    let mut server = WeatherServer::new(
        &mut connection,
        handlers.clone(),
        "rust-server-demo:1".to_string(),
    )
    .await;

    let mut looping_server = server.clone();
    let _loop_join_handle = tokio::spawn(async move {
        println!("Starting connection loop");
        let _conn_loop = looping_server.run_loop().await;
    });

    println!("Setting initial value for property 'location'");
    let new_value = LocationProperty {
        latitude: 3.14,
        longitude: 3.14,
    };
    let prop_init_future = server.set_location(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'location': {:?}", e);
    }

    println!("Setting initial value for property 'current_temperature'");
    let prop_init_future = server.set_current_temperature(3.14).await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'current_temperature': {:?}", e);
    }

    println!("Setting initial value for property 'current_condition'");
    let new_value = CurrentConditionProperty {
        condition: WeatherCondition::Snowy,
        description: "apples".to_string(),
    };
    let prop_init_future = server.set_current_condition(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'current_condition': {:?}", e);
    }

    println!("Setting initial value for property 'daily_forecast'");
    let new_value = DailyForecastProperty {
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
    };
    let prop_init_future = server.set_daily_forecast(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'daily_forecast': {:?}", e);
    }

    println!("Setting initial value for property 'hourly_forecast'");
    let new_value = HourlyForecastProperty {
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
    };
    let prop_init_future = server.set_hourly_forecast(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'hourly_forecast': {:?}", e);
    }

    println!("Setting initial value for property 'current_condition_refresh_interval'");
    let prop_init_future = server.set_current_condition_refresh_interval(42).await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'current_condition_refresh_interval': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'hourly_forecast_refresh_interval'");
    let prop_init_future = server.set_hourly_forecast_refresh_interval(42).await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'hourly_forecast_refresh_interval': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'daily_forecast_refresh_interval'");
    let prop_init_future = server.set_daily_forecast_refresh_interval(42).await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'daily_forecast_refresh_interval': {:?}",
            e
        );
    }

    let mut server_clone1 = server.clone();
    let signal_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(9)).await;

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'current_time'");
            let signal_result_future = server_clone1.emit_current_time("apples".to_string()).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'current_time' was sent: {:?}", signal_result);
        }
    });

    let mut server_clone2 = server.clone();
    let property_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(11)).await;

            sleep(Duration::from_secs(1)).await;
            println!("Changing property 'location'");
            let new_value = LocationProperty {
                latitude: 1.0,
                longitude: 1.0,
            };
            let _ = server_clone2.set_location(new_value).await;

            sleep(Duration::from_secs(1)).await;
            println!("Changing property 'current_temperature'");
            let prop_change_future = server_clone2.set_current_temperature(1.0).await;
            if let Err(e) = prop_change_future.await {
                eprintln!("Error changing property 'current_temperature': {:?}", e);
            }

            sleep(Duration::from_secs(1)).await;
            println!("Changing property 'current_condition'");
            let new_value = CurrentConditionProperty {
                condition: WeatherCondition::Sunny,
                description: "foo".to_string(),
            };
            let _ = server_clone2.set_current_condition(new_value).await;

            sleep(Duration::from_secs(1)).await;
            println!("Changing property 'daily_forecast'");
            let new_value = DailyForecastProperty {
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
            let _ = server_clone2.set_daily_forecast(new_value).await;

            sleep(Duration::from_secs(1)).await;
            println!("Changing property 'hourly_forecast'");
            let new_value = HourlyForecastProperty {
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
            let _ = server_clone2.set_hourly_forecast(new_value).await;

            sleep(Duration::from_secs(1)).await;
            println!("Changing property 'current_condition_refresh_interval'");
            let prop_change_future = server_clone2
                .set_current_condition_refresh_interval(2022)
                .await;
            if let Err(e) = prop_change_future.await {
                eprintln!(
                    "Error changing property 'current_condition_refresh_interval': {:?}",
                    e
                );
            }

            sleep(Duration::from_secs(1)).await;
            println!("Changing property 'hourly_forecast_refresh_interval'");
            let prop_change_future = server_clone2
                .set_hourly_forecast_refresh_interval(2022)
                .await;
            if let Err(e) = prop_change_future.await {
                eprintln!(
                    "Error changing property 'hourly_forecast_refresh_interval': {:?}",
                    e
                );
            }

            sleep(Duration::from_secs(1)).await;
            println!("Changing property 'daily_forecast_refresh_interval'");
            let prop_change_future = server_clone2
                .set_daily_forecast_refresh_interval(2022)
                .await;
            if let Err(e) = prop_change_future.await {
                eprintln!(
                    "Error changing property 'daily_forecast_refresh_interval': {:?}",
                    e
                );
            }
        }
    });

    let _ = join!(signal_publish_task, property_publish_task);

    // Ctrl-C to stop
}
