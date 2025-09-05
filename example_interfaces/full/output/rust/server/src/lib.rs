/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Full interface.
*/

use mqttier::{MqttierClient, ReceivedMessage};

#[allow(unused_imports)]
use full_types::payloads::{MethodResultCode, *};
use std::sync::{Arc, Mutex};

use serde_json;
use tokio::sync::mpsc;

use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct FullServerSubscriptionIds {
    add_numbers_method_req: usize,
    do_something_method_req: usize,

    favorite_number_property_update: usize,

    favorite_foods_property_update: usize,

    lunch_menu_property_update: usize,
}

struct FullServerMethodHandlers<T> {
    /// Pointer to a function to handle the addNumbers method request.
    method_handler_for_add_numbers: Arc<
        Mutex<
            Box<
                dyn Fn(
                        i32,
                        i32,
                        Option<i32>,
                        Arc<Mutex<Option<T>>>,
                    ) -> Result<i32, MethodResultCode>
                    + Send,
            >,
        >,
    >,
    /// Pointer to a function to handle the doSomething method request.
    method_handler_for_do_something: Arc<
        Mutex<
            Box<
                dyn Fn(
                        String,
                        Arc<Mutex<Option<T>>>,
                    ) -> Result<DoSomethingReturnValue, MethodResultCode>
                    + Send,
            >,
        >,
    >,
}

impl<T> Clone for WeatherForecastsServerMethodHandlers<T> {
    fn clone(&self) -> Self {
        WeatherForecastsServerMethodHandlers {
            method_handler_for_refresh_daily_forecast: self
                .method_handler_for_refresh_daily_forecast
                .clone(),
            method_handler_for_refresh_hourly_forecast: self
                .method_handler_for_refresh_hourly_forecast
                .clone(),
            method_handler_for_refresh_current_conditions: self
                .method_handler_for_refresh_current_conditions
                .clone(),
        }
    }
}

#[derive(Clone)]
struct FullProperties {
    favorite_number_topic: Arc<String>,
    favorite_number: Arc<Mutex<Option<i32>>>,
    favorite_foods_topic: Arc<String>,
    favorite_foods: Arc<Mutex<Option<FavoriteFoodsProperty>>>,
    lunch_menu_topic: Arc<String>,
    lunch_menu: Arc<Mutex<Option<LunchMenuProperty>>>,
}

#[derive(Clone)]
pub struct FullServer<T>
where
    T: Send + Clone + 'static,
{
    mqttier_client: MqttierClient,

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<mpsc::Receiver<ReceivedMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Struct contains all the handlers for the various methods.
    method_handlers: FullServerMethodHandlers<T>,

    /// Struct contains all the properties.
    properties: FullProperties,

    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: FullServerSubscriptionIds,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,
}

impl<T: Send + Sync + Clone + 'static> FullServer<T> {
    pub async fn new(connection: &mut MqttierClient) -> Self {
        // Create a channel for messages to get from the MqttierClient object to this FullServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel::<ReceivedMessage>(64);

        // Create method handler struct
        let subscription_id_add_numbers_method_req = connection
            .subscribe(
                "full/method/addNumbers".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_add_numbers_method_req =
            subscription_id_add_numbers_method_req.unwrap_or_else(|_| usize::MAX);
        let subscription_id_do_something_method_req = connection
            .subscribe(
                "full/method/doSomething".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_do_something_method_req =
            subscription_id_do_something_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_favorite_number_property_update = connection
            .subscribe(
                "full/property/favoriteNumber/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_number_property_update =
            subscription_id_favorite_number_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_favorite_foods_property_update = connection
            .subscribe(
                "full/property/favoriteFoods/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_foods_property_update =
            subscription_id_favorite_foods_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_lunch_menu_property_update = connection
            .subscribe(
                "full/property/lunchMenu/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_lunch_menu_property_update =
            subscription_id_lunch_menu_property_update.unwrap_or_else(|_| usize::MAX);

        // Create structure for method handlers.
        let method_handlers = FullServerMethodHandlers {
            method_handler_for_add_numbers: Arc::new(Mutex::new(Box::new(
                |_1, _2, _3, _state: Arc<Mutex<Option<T>>>| Err(MethodResultCode::ServerError),
            ))),
            method_handler_for_do_something: Arc::new(Mutex::new(Box::new(
                |_1, _state: Arc<Mutex<Option<T>>>| Err(MethodResultCode::ServerError),
            ))),
        };

        // Create structure for subscription ids.
        let sub_ids = FullServerSubscriptionIds {
            add_numbers_method_req: subscription_id_add_numbers_method_req,
            do_something_method_req: subscription_id_do_something_method_req,

            favorite_number_property_update: subscription_id_favorite_number_property_update,

            favorite_foods_property_update: subscription_id_favorite_foods_property_update,

            lunch_menu_property_update: subscription_id_lunch_menu_property_update,
        };

        let property_values = FullProperties {
            favorite_number_topic: Arc::new(String::from("full/property/favoriteNumber/value")),

            favorite_number: Arc::new(Mutex::new(None)),
            favorite_foods_topic: Arc::new(String::from("full/property/favoriteFoods/value")),
            favorite_foods: Arc::new(Mutex::new(None)),

            lunch_menu_topic: Arc::new(String::from("full/property/lunchMenu/value")),
            lunch_menu: Arc::new(Mutex::new(None)),
        };

        FullServer {
            mqttier_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            method_handlers: method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,

            client_id: connection.client_id.to_string(),
        }
    }

    /// Emits the todayIs signal with the given arguments.
    pub async fn emit_today_is(&mut self, day_of_month: i32, day_of_week: Option<DayOfTheWeek>) {
        let data = TodayIsSignalPayload {
            dayOfMonth: day_of_month,

            dayOfWeek: day_of_week,
        };
        let _ = self
            .mqttier_client
            .publish_structure("full/signal/todayIs".to_string(), &data)
            .await;
    }

    /// Sets the function to be called when a request for the addNumbers method is received.
    pub fn set_method_handler_for_add_numbers(
        &mut self,
        cb: impl Fn(i32, i32, Option<i32>, T) -> Result<i32, MethodResultCode> + 'static + Send,
    ) {
        self.method_handlers.method_handler_for_add_numbers =
            Arc::new(Mutex::new(Box::new(move |state: Arc<Mutex<Option<T>>>| {
                if let Some(state_value) = state.lock().unwrap().as_ref() {
                    cb(state_value.clone())
                } else {
                    Err(MethodResultCode::ServerError)
                }
            })));
    }
    /// Sets the function to be called when a request for the doSomething method is received.
    pub fn set_method_handler_for_do_something(
        &mut self,
        cb: impl Fn(String, T) -> Result<DoSomethingReturnValue, MethodResultCode> + 'static + Send,
    ) {
        self.method_handlers.method_handler_for_do_something =
            Arc::new(Mutex::new(Box::new(move |state: Arc<Mutex<Option<T>>>| {
                if let Some(state_value) = state.lock().unwrap().as_ref() {
                    cb(state_value.clone())
                } else {
                    Err(MethodResultCode::ServerError)
                }
            })));
    }

    /// Handles a request message for the addNumbers method.
    async fn handle_add_numbers_request(
        publisher: MqttierClient,
        handlers: &mut FullServerMethodHandlers<T>,
        msg: ReceivedMessage,
        state: Arc<Mutex<Option<T>>>,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload = serde_json::from_slice::<AddNumbersRequestObject>(&payload_vec).unwrap();

        // call the method handler
        let rv: Result<i32, MethodResultCode> = {
            let func_guard = handlers.method_handler_for_add_numbers.lock().unwrap();
            (*func_guard)(payload.first, payload.second, payload.third, state)
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rv {
                Ok(retval) => {
                    let retval = AddNumbersReturnValue { sum: retval };

                    publisher
                        .publish_response(resp_topic, &retval, corr_data)
                        .await
                        .expect("Failed to publish response structure");
                }
                Err(err) => {
                    eprintln!(
                        "Error occurred while handling {}: {:?}",
                        stringify!(addNumbers),
                        err
                    );
                }
            }
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }
    /// Handles a request message for the doSomething method.
    async fn handle_do_something_request(
        publisher: MqttierClient,
        handlers: &mut FullServerMethodHandlers<T>,
        msg: ReceivedMessage,
        state: Arc<Mutex<Option<T>>>,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload = serde_json::from_slice::<DoSomethingRequestObject>(&payload_vec).unwrap();

        // call the method handler
        let rv: Result<DoSomethingReturnValue, MethodResultCode> = {
            let func_guard = handlers.method_handler_for_do_something.lock().unwrap();
            (*func_guard)(payload.aString, state)
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rv {
                Ok(retval) => {
                    publisher
                        .publish_response(resp_topic, &retval, corr_data)
                        .await
                        .expect("Failed to publish response structure");
                }
                Err(err) => {
                    eprintln!(
                        "Error occurred while handling {}: {:?}",
                        stringify!(doSomething),
                        err
                    );
                }
            }
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }

    async fn publish_favorite_number_value(publisher: MqttierClient, topic: String, data: i32) {
        let new_data = FavoriteNumberProperty { number: data };
        println!("Publishing to topic {}", topic);
        let _pub_result = publisher.publish_state(topic, &new_data, 1).await;
    }

    async fn update_favorite_number_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<i32>>>,
        msg: ReceivedMessage,
        _state: Arc<Mutex<Option<T>>>,
    ) {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_data: FavoriteNumberProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.number);
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.number;
        let _ = tokio::spawn(async move {
            FullServer::<T>::publish_favorite_number_value(publisher2, topic2, data2).await;
        });
    }

    pub async fn set_favorite_number(&mut self, data: i32) {
        println!("Setting favorite_number of type i32");
        let prop = self.properties.favorite_number.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.favorite_number_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property favorite_number of type i32 to {}",
                topic2
            );
            FullServer::<T>::publish_favorite_number_value(publisher2, topic2, data).await;
        });
    }

    async fn publish_favorite_foods_value(
        publisher: MqttierClient,
        topic: String,
        data: FavoriteFoodsProperty,
    ) {
        let _pub_result = publisher.publish_state(topic, &data, 1).await;
    }

    async fn update_favorite_foods_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<FavoriteFoodsProperty>>>,
        msg: ReceivedMessage,
        _state: Arc<Mutex<Option<T>>>,
    ) {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_data: FavoriteFoodsProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.clone());

        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data;

        let _ = tokio::spawn(async move {
            FullServer::<T>::publish_favorite_foods_value(publisher2, topic2, data2).await;
        });
    }

    pub async fn set_favorite_foods(&mut self, data: FavoriteFoodsProperty) {
        println!("Setting favorite_foods of type FavoriteFoodsProperty");
        let prop = self.properties.favorite_foods.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.favorite_foods_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property favorite_foods of type FavoriteFoodsProperty to {}",
                topic2
            );
            FullServer::<T>::publish_favorite_foods_value(publisher2, topic2, data).await;
        });
    }

    async fn publish_lunch_menu_value(
        publisher: MqttierClient,
        topic: String,
        data: LunchMenuProperty,
    ) {
        let _pub_result = publisher.publish_state(topic, &data, 1).await;
    }

    async fn update_lunch_menu_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<LunchMenuProperty>>>,
        msg: ReceivedMessage,
        _state: Arc<Mutex<Option<T>>>,
    ) {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_data: LunchMenuProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.clone());

        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data;

        let _ = tokio::spawn(async move {
            FullServer::<T>::publish_lunch_menu_value(publisher2, topic2, data2).await;
        });
    }

    pub async fn set_lunch_menu(&mut self, data: LunchMenuProperty) {
        println!("Setting lunch_menu of type LunchMenuProperty");
        let prop = self.properties.lunch_menu.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.lunch_menu_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property lunch_menu of type LunchMenuProperty to {}",
                topic2
            );
            FullServer::<T>::publish_lunch_menu_value(publisher2, topic2, data).await;
        });
    }

    /// Starts the tasks that process messages received.
    /// In the task, it loops over messages received from the rx side of the message_receiver channel.
    /// Based on the subscription id of the received message, it will call a function to handle the
    /// received message.
    pub async fn receive_loop(&mut self, state: Arc<Mutex<Option<T>>>) -> Result<(), JoinError> {
        // Make sure the MqttierClient is connected and running.
        let _ = self.mqttier_client.run_loop().await;

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            self.msg_streamer_rx
                .lock()
                .unwrap()
                .take()
                .expect("msg_streamer_rx should be Some")
        };

        let mut method_handlers = self.method_handlers.clone();
        let sub_ids = self.subscription_ids.clone();
        let publisher = self.mqttier_client.clone();

        let properties = self.properties.clone();

        let loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                if msg.subscription_id == sub_ids.add_numbers_method_req {
                    FullServer::handle_add_numbers_request(
                        publisher.clone(),
                        &mut method_handlers,
                        msg,
                        state.clone(),
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.do_something_method_req {
                    FullServer::handle_do_something_request(
                        publisher.clone(),
                        &mut method_handlers,
                        msg,
                        state.clone(),
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.favorite_number_property_update {
                    FullServer::update_favorite_number_value(
                        publisher.clone(),
                        properties.favorite_number_topic.clone(),
                        properties.favorite_number.clone(),
                        msg,
                        state.clone(),
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.favorite_foods_property_update {
                    FullServer::update_favorite_foods_value(
                        publisher.clone(),
                        properties.favorite_foods_topic.clone(),
                        properties.favorite_foods.clone(),
                        msg,
                        state.clone(),
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.lunch_menu_property_update {
                    FullServer::update_lunch_menu_value(
                        publisher.clone(),
                        properties.lunch_menu_topic.clone(),
                        properties.lunch_menu.clone(),
                        msg,
                        state.clone(),
                    )
                    .await;
                }
            }
            println!("No more messages from message_receiver channel");
        });
        let _ = tokio::join!(loop_task);

        println!("Server receive loop completed [error?]");
        Ok(())
    }
}
