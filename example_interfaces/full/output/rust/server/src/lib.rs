/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
*/

extern crate paho_mqtt as mqtt;
use connection::{MessagePublisher, Connection, ReceivedMessage};

use futures::StreamExt;
use connection::Connection;
use connection::payloads::MethodResultCode;


pub struct ExampleServer {
    /// Pointer to a function to handle the addNumbers method request.
    method_handler_for_add_numbers: Box<dyn FnMut(i32, i32)->Result<i32, MethodResultCode>>,
    /// Pointer to a function to handle the doSomething method request.
    method_handler_for_do_something: Box<dyn FnMut(String)->Result<connection::payloads::DoSomethingReturnValue, MethodResultCode>>,
    
    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Option<mpsc::Receiver<ReceivedMessage>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Through this MessagePublisher object, we can publish messages to MQTT.
    msg_publisher: MessagePublisher,

    /// Copy of MQTT Client ID
    client_id: String,
}

impl ExampleServer {
    pub async fn new(mut connection: Connection) -> Self {
        let _ = connection.connect().await.expect("Could not connect to MQTT broker");

        //let interface_info = String::from(r#"{"name": "Example", "summary": "Example StingerAPI interface which demonstrates most features.", "title": "Fully Featured Example Interface", "version": "0.0.1"}"#);
        //connection.publish("Example/interface".to_string(), interface_info, 1).await;

        // Create a channel for messages to get from the Connection object to this ExampleClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        let publisher = connection.get_publisher();

        // Subscribe to all the topics needed for method requests.
        let subscription_id_add_numbers_method_req = connection.subscribe("Example/method/addNumbers", message_received_tx.clone()).await;
        let subscription_id_add_numbers_method_req = subscription_id_add_numbers_method_req.unwrap_or_else(|_| -1);
        let subscription_id_do_something_method_req = connection.subscribe("Example/method/doSomething", message_received_tx.clone()).await;
        let subscription_id_do_something_method_req = subscription_id_do_something_method_req.unwrap_or_else(|_| -1);
        

        // Create structure for subscription ids.
        let sub_ids = ExampleSubscriptionIds {
            add_numbers_method_req: subscription_id_add_numbers_method_req,
            do_something_method_req: subscription_id_do_something_method_req,
            
        };

        ExampleServer {
            method_handler_for_add_numbers: Box::new( |_1, _2| { Err(MethodResultCode::ServerError) } ),
            method_handler_for_do_something: Box::new( |_1| { Err(MethodResultCode::ServerError) } ),
            
            msg_streamer_rx: Some(message_received_rx),
            msg_streamer_tx: message_received_tx,
            msg_publisher: publisher,
            subscription_ids: sub_ids,
            client_id: connection.client_id.to_string(),
        }
    }

    pub async fn emit_today_is(&mut self, day_of_month: i32, day_of_week: connection::payloads::DayOfTheWeek) {
        let data = connection::payloads::TodayIsSignalPayload {
            
            dayOfMonth: day_of_month,
            
            dayOfWeek: day_of_week,
            
        };
        self.publisher.publish_simple("Example/signal/todayIs".to_string(), data).await;
    }
    

    pub fn set_method_handler_for_add_numbers(&mut self, cb: impl FnMut(i32, i32)->Result<i32, MethodResultCode> + 'static) {
        self.method_handler_for_add_numbers = Box::new(cb);
    }
    pub fn set_method_handler_for_do_something(&mut self, cb: impl FnMut(String)->Result<connection::payloads::DoSomethingReturnValue, MethodResultCode> + 'static) {
        self.method_handler_for_do_something = Box::new(cb);
    }
    

    async fn handle_add_numbers_request(&mut self, msg: mqtt::Message) {
        let props = msg.properties();
        let opt_corr_id_bin: Option<Vec<u8>> = Some(msg_props.get_binary(mqtt::PropertyCode::CorrelationData));
        let opt_resp_topic = msg_props.get_string(mqtt::PropertyCode::ResponseTopic);

        let payload = serde_json::from_str::<AddNumbersRequestObject>(msg.payload_str().unwrap()).unwrap();

        // call the method handler
        let rv: i32 = (self.method_handler_for_add_numbers)(payload.first, payload.second);
        
        if let Some(resp_topic) = opt_resp_topic {
            self.publisher.publish_response_structure(resp_topic, &rv, opt_corr_id_bin).await.expect("Failed to publish response structure");
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }
    async fn handle_do_something_request(&mut self, msg: mqtt::Message) {
        let props = msg.properties();
        let opt_corr_id_bin: Option<Vec<u8>> = Some(msg_props.get_binary(mqtt::PropertyCode::CorrelationData));
        let opt_resp_topic = msg_props.get_string(mqtt::PropertyCode::ResponseTopic);

        let payload = serde_json::from_str::<DoSomethingRequestObject>(msg.payload_str().unwrap()).unwrap();

        // call the method handler
        let rv: connection::payloads::DoSomethingReturnValue = (self.method_handler_for_do_something)(payload.a_string);
        
        if let Some(resp_topic) = opt_resp_topic {
            self.publisher.publish_response_structure(resp_topic, &rv, opt_corr_id_bin).await.expect("Failed to publish response structure");
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }
    

     /// Starts the tasks that process messages received.
    pub async fn receive_loop(&mut self) -> Result<(), JoinError> {

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = self.msg_streamer_rx.take().expect("msg_streamer_rx should be Some");

        let sub_ids = self.subscription_ids.clone();

        let loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                if msg.subscription_id == sub_ids.add_numbers_method_resp {
                    ExampleClient.handle_add_numbers_request(msg.message).await;
                }
                else if msg.subscription_id == sub_ids.do_something_method_resp {
                    ExampleClient.handle_do_something_request(msg.message).await;
                }
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}