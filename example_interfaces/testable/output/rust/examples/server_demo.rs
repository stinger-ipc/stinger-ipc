/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.
*/
use std::any::Any;

use mqttier::{Connection, MqttierClient, MqttierOptions};
use test_able_ipc::server::{TestAbleMethodHandlers, TestAbleServer};
use tokio::time::{sleep, Duration};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing_subscriber;

#[allow(unused_imports)]
use test_able_ipc::payloads::{MethodReturnCode, *};

struct TestAbleMethodImpl {
    server: Option<TestAbleServer>,
}

impl TestAbleMethodImpl {
    fn new() -> Self {
        Self { server: None }
    }
}

#[async_trait]
impl TestAbleMethodHandlers for TestAbleMethodImpl {
    async fn initialize(&mut self, server: TestAbleServer) -> Result<(), MethodReturnCode> {
        self.server = Some(server.clone());
        Ok(())
    }

    async fn handle_call_with_nothing(&self) -> Result<(), MethodReturnCode> {
        println!("Handling callWithNothing");
        Ok(())
    }

    async fn handle_call_one_integer(&self, _input1: i32) -> Result<i32, MethodReturnCode> {
        println!("Handling callOneInteger");
        Ok(42)
    }

    async fn handle_call_optional_integer(
        &self,
        _input1: Option<i32>,
    ) -> Result<Option<i32>, MethodReturnCode> {
        println!("Handling callOptionalInteger");
        Ok(Some(42))
    }

    async fn handle_call_three_integers(
        &self,
        _input1: i32,
        _input2: i32,
        _input3: Option<i32>,
    ) -> Result<CallThreeIntegersReturnValues, MethodReturnCode> {
        println!("Handling callThreeIntegers");
        let rv = CallThreeIntegersReturnValues {
            output1: 42,
            output2: 42,
            output3: Some(42),
        };
        Ok(rv)
    }

    async fn handle_call_one_string(&self, _input1: String) -> Result<String, MethodReturnCode> {
        println!("Handling callOneString");
        Ok("apples".to_string())
    }

    async fn handle_call_optional_string(
        &self,
        _input1: Option<String>,
    ) -> Result<Option<String>, MethodReturnCode> {
        println!("Handling callOptionalString");
        Ok(Some("apples".to_string()))
    }

    async fn handle_call_three_strings(
        &self,
        _input1: String,
        _input2: Option<String>,
        _input3: String,
    ) -> Result<CallThreeStringsReturnValues, MethodReturnCode> {
        println!("Handling callThreeStrings");
        let rv = CallThreeStringsReturnValues {
            output1: "apples".to_string(),
            output2: Some("apples".to_string()),
            output3: "apples".to_string(),
        };
        Ok(rv)
    }

    async fn handle_call_one_enum(&self, _input1: Numbers) -> Result<Numbers, MethodReturnCode> {
        println!("Handling callOneEnum");
        Ok(Numbers::One)
    }

    async fn handle_call_optional_enum(
        &self,
        _input1: Option<Numbers>,
    ) -> Result<Option<Numbers>, MethodReturnCode> {
        println!("Handling callOptionalEnum");
        Ok(Some(Numbers::One))
    }

    async fn handle_call_three_enums(
        &self,
        _input1: Numbers,
        _input2: Numbers,
        _input3: Option<Numbers>,
    ) -> Result<CallThreeEnumsReturnValues, MethodReturnCode> {
        println!("Handling callThreeEnums");
        let rv = CallThreeEnumsReturnValues {
            output1: Numbers::One,
            output2: Numbers::One,
            output3: Some(Numbers::One),
        };
        Ok(rv)
    }

    async fn handle_call_one_struct(
        &self,
        _input1: AllTypes,
    ) -> Result<AllTypes, MethodReturnCode> {
        println!("Handling callOneStruct");
        let rv = AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 42],
            optional_array_of_integers: vec![42, 42],
            array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
        };

        Ok(rv)
    }

    async fn handle_call_optional_struct(
        &self,
        _input1: Option<AllTypes>,
    ) -> Result<Option<AllTypes>, MethodReturnCode> {
        println!("Handling callOptionalStruct");
        let rv = AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 42],
            optional_array_of_integers: vec![42, 42],
            array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
        };

        Ok(Some(rv))
    }

    async fn handle_call_three_structs(
        &self,
        _input1: Option<AllTypes>,
        _input2: AllTypes,
        _input3: AllTypes,
    ) -> Result<CallThreeStructsReturnValues, MethodReturnCode> {
        println!("Handling callThreeStructs");
        let rv = CallThreeStructsReturnValues {
            output1: Some(AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 42],
                optional_array_of_integers: vec![42, 42],
                array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: vec![Numbers::One, Numbers::One],
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                optional_array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
                optional_array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
            }),
            output2: AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 42],
                optional_array_of_integers: vec![42, 42],
                array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: vec![Numbers::One, Numbers::One],
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                optional_array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
                optional_array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
            },
            output3: AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 42],
                optional_array_of_integers: vec![42, 42],
                array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: vec![Numbers::One, Numbers::One],
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                optional_array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
                optional_array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
            },
        };
        Ok(rv)
    }

    async fn handle_call_one_date_time(
        &self,
        _input1: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> {
        println!("Handling callOneDateTime");
        Ok(chrono::Utc::now())
    }

    async fn handle_call_optional_date_time(
        &self,
        _input1: Option<chrono::DateTime<chrono::Utc>>,
    ) -> Result<Option<chrono::DateTime<chrono::Utc>>, MethodReturnCode> {
        println!("Handling callOptionalDateTime");
        Ok(Some(chrono::Utc::now()))
    }

    async fn handle_call_three_date_times(
        &self,
        _input1: chrono::DateTime<chrono::Utc>,
        _input2: chrono::DateTime<chrono::Utc>,
        _input3: Option<chrono::DateTime<chrono::Utc>>,
    ) -> Result<CallThreeDateTimesReturnValues, MethodReturnCode> {
        println!("Handling callThreeDateTimes");
        let rv = CallThreeDateTimesReturnValues {
            output1: chrono::Utc::now(),
            output2: chrono::Utc::now(),
            output3: Some(chrono::Utc::now()),
        };
        Ok(rv)
    }

    async fn handle_call_one_duration(
        &self,
        _input1: chrono::Duration,
    ) -> Result<chrono::Duration, MethodReturnCode> {
        println!("Handling callOneDuration");
        Ok(chrono::Duration::seconds(3536))
    }

    async fn handle_call_optional_duration(
        &self,
        _input1: Option<chrono::Duration>,
    ) -> Result<Option<chrono::Duration>, MethodReturnCode> {
        println!("Handling callOptionalDuration");
        Ok(Some(chrono::Duration::seconds(3536)))
    }

    async fn handle_call_three_durations(
        &self,
        _input1: chrono::Duration,
        _input2: chrono::Duration,
        _input3: Option<chrono::Duration>,
    ) -> Result<CallThreeDurationsReturnValues, MethodReturnCode> {
        println!("Handling callThreeDurations");
        let rv = CallThreeDurationsReturnValues {
            output1: chrono::Duration::seconds(3536),
            output2: chrono::Duration::seconds(3536),
            output3: Some(chrono::Duration::seconds(3536)),
        };
        Ok(rv)
    }

    async fn handle_call_one_binary(&self, _input1: Vec<u8>) -> Result<Vec<u8>, MethodReturnCode> {
        println!("Handling callOneBinary");
        Ok(vec![101, 120, 97, 109, 112, 108, 101])
    }

    async fn handle_call_optional_binary(
        &self,
        _input1: Option<Vec<u8>>,
    ) -> Result<Option<Vec<u8>>, MethodReturnCode> {
        println!("Handling callOptionalBinary");
        Ok(Some(vec![101, 120, 97, 109, 112, 108, 101]))
    }

    async fn handle_call_three_binaries(
        &self,
        _input1: Vec<u8>,
        _input2: Vec<u8>,
        _input3: Option<Vec<u8>>,
    ) -> Result<CallThreeBinariesReturnValues, MethodReturnCode> {
        println!("Handling callThreeBinaries");
        let rv = CallThreeBinariesReturnValues {
            output1: vec![101, 120, 97, 109, 112, 108, 101],
            output2: vec![101, 120, 97, 109, 112, 108, 101],
            output3: Some(vec![101, 120, 97, 109, 112, 108, 101]),
        };
        Ok(rv)
    }

    async fn handle_call_one_list_of_integers(
        &self,
        _input1: Vec<i32>,
    ) -> Result<Vec<i32>, MethodReturnCode> {
        println!("Handling callOneListOfIntegers");
        Ok(vec![42, 42])
    }

    async fn handle_call_optional_list_of_floats(
        &self,
        _input1: Option<Vec<f32>>,
    ) -> Result<Option<Vec<f32>>, MethodReturnCode> {
        println!("Handling callOptionalListOfFloats");
        Ok(vec![3.14, 3.14])
    }

    async fn handle_call_two_lists(
        &self,
        _input1: Vec<Numbers>,
        _input2: Option<Vec<String>>,
    ) -> Result<CallTwoListsReturnValues, MethodReturnCode> {
        println!("Handling callTwoLists");
        let rv = CallTwoListsReturnValues {
            output1: vec![Numbers::One, Numbers::One],
            output2: vec!["apples".to_string(), "apples".to_string()],
        };
        Ok(rv)
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

    let handlers: Arc<Mutex<Box<dyn TestAbleMethodHandlers>>> =
        Arc::new(Mutex::new(Box::new(TestAbleMethodImpl::new())));

    let mut server = TestAbleServer::new(
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

    println!("Setting initial value for property 'read_write_integer'");
    let prop_init_future = server.set_read_write_integer(42).await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_write_integer': {:?}", e);
    }

    println!("Setting initial value for property 'read_only_integer'");
    let prop_init_future = server.set_read_only_integer(42).await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_only_integer': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_optional_integer'");
    let prop_init_future = server.set_read_write_optional_integer(Some(42)).await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_optional_integer': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_two_integers'");
    let new_value = ReadWriteTwoIntegersProperty {
        first: 42,
        second: Some(42),
    };
    let prop_init_future = server.set_read_write_two_integers(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_two_integers': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_only_string'");
    let prop_init_future = server.set_read_only_string("apples".to_string()).await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_only_string': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_string'");
    let prop_init_future = server.set_read_write_string("apples".to_string()).await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_write_string': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_optional_string'");
    let prop_init_future = server
        .set_read_write_optional_string(Some("apples".to_string()))
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_optional_string': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_two_strings'");
    let new_value = ReadWriteTwoStringsProperty {
        first: "apples".to_string(),
        second: Some("apples".to_string()),
    };
    let prop_init_future = server.set_read_write_two_strings(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_two_strings': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_struct'");
    let prop_init_future = server
        .set_read_write_struct(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 42],
            optional_array_of_integers: vec![42, 42],
            array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
        })
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_write_struct': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_optional_struct'");
    let prop_init_future = server
        .set_read_write_optional_struct(Some(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 42],
            optional_array_of_integers: vec![42, 42],
            array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
        }))
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_optional_struct': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_two_structs'");
    let new_value = ReadWriteTwoStructsProperty {
        first: AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 42],
            optional_array_of_integers: vec![42, 42],
            array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
        },
        second: Some(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 42],
            optional_array_of_integers: vec![42, 42],
            array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
        }),
    };
    let prop_init_future = server.set_read_write_two_structs(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_two_structs': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_only_enum'");
    let prop_init_future = server.set_read_only_enum(Numbers::One).await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_only_enum': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_enum'");
    let prop_init_future = server.set_read_write_enum(Numbers::One).await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_write_enum': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_optional_enum'");
    let prop_init_future = server
        .set_read_write_optional_enum(Some(Numbers::One))
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_optional_enum': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_two_enums'");
    let new_value = ReadWriteTwoEnumsProperty {
        first: Numbers::One,
        second: Some(Numbers::One),
    };
    let prop_init_future = server.set_read_write_two_enums(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_two_enums': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_datetime'");
    let prop_init_future = server.set_read_write_datetime(chrono::Utc::now()).await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_write_datetime': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_optional_datetime'");
    let prop_init_future = server
        .set_read_write_optional_datetime(Some(chrono::Utc::now()))
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_optional_datetime': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_two_datetimes'");
    let new_value = ReadWriteTwoDatetimesProperty {
        first: chrono::Utc::now(),
        second: Some(chrono::Utc::now()),
    };
    let prop_init_future = server.set_read_write_two_datetimes(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_two_datetimes': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_duration'");
    let prop_init_future = server
        .set_read_write_duration(chrono::Duration::seconds(3536))
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_write_duration': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_optional_duration'");
    let prop_init_future = server
        .set_read_write_optional_duration(Some(chrono::Duration::seconds(3536)))
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_optional_duration': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_two_durations'");
    let new_value = ReadWriteTwoDurationsProperty {
        first: chrono::Duration::seconds(3536),
        second: Some(chrono::Duration::seconds(3536)),
    };
    let prop_init_future = server.set_read_write_two_durations(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_two_durations': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_binary'");
    let prop_init_future = server
        .set_read_write_binary(vec![101, 120, 97, 109, 112, 108, 101])
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_write_binary': {:?}", e);
    }

    println!("Setting initial value for property 'read_write_optional_binary'");
    let prop_init_future = server
        .set_read_write_optional_binary(Some(vec![101, 120, 97, 109, 112, 108, 101]))
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_optional_binary': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_two_binaries'");
    let new_value = ReadWriteTwoBinariesProperty {
        first: vec![101, 120, 97, 109, 112, 108, 101],
        second: Some(vec![101, 120, 97, 109, 112, 108, 101]),
    };
    let prop_init_future = server.set_read_write_two_binaries(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_two_binaries': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_list_of_strings'");
    let prop_init_future = server
        .set_read_write_list_of_strings(vec!["apples".to_string(), "apples".to_string()])
        .await;
    if let Err(e) = prop_init_future.await {
        eprintln!(
            "Error initializing property 'read_write_list_of_strings': {:?}",
            e
        );
    }

    println!("Setting initial value for property 'read_write_lists'");
    let new_value = ReadWriteListsProperty {
        the_list: vec![Numbers::One, Numbers::One],
        optionalList: vec![chrono::Utc::now(), chrono::Utc::now()],
    };
    let prop_init_future = server.set_read_write_lists(new_value).await;

    if let Err(e) = prop_init_future.await {
        eprintln!("Error initializing property 'read_write_lists': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'empty'");
    let signal_result_future = server.emit_empty().await;
    let signal_result = signal_result_future.await;
    println!("Signal 'empty' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleInt'");
    let signal_result_future = server.emit_single_int(42).await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleInt' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleOptionalInt'");
    let signal_result_future = server.emit_single_optional_int(Some(42)).await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleOptionalInt' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'threeIntegers'");
    let signal_result_future = server.emit_three_integers(42, 42, Some(42)).await;
    let signal_result = signal_result_future.await;
    println!("Signal 'threeIntegers' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleString'");
    let signal_result_future = server.emit_single_string("apples".to_string()).await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleString' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleOptionalString'");
    let signal_result_future = server
        .emit_single_optional_string(Some("apples".to_string()))
        .await;
    let signal_result = signal_result_future.await;
    println!(
        "Signal 'singleOptionalString' was sent: {:?}",
        signal_result
    );

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'threeStrings'");
    let signal_result_future = server
        .emit_three_strings(
            "apples".to_string(),
            "apples".to_string(),
            Some("apples".to_string()),
        )
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'threeStrings' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleEnum'");
    let signal_result_future = server.emit_single_enum(Numbers::One).await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleEnum' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleOptionalEnum'");
    let signal_result_future = server.emit_single_optional_enum(Some(Numbers::One)).await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleOptionalEnum' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'threeEnums'");
    let signal_result_future = server
        .emit_three_enums(Numbers::One, Numbers::One, Some(Numbers::One))
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'threeEnums' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleStruct'");
    let signal_result_future = server
        .emit_single_struct(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 42],
            optional_array_of_integers: vec![42, 42],
            array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
        })
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleStruct' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleOptionalStruct'");
    let signal_result_future = server
        .emit_single_optional_struct(Some(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 42],
            optional_array_of_integers: vec![42, 42],
            array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
        }))
        .await;
    let signal_result = signal_result_future.await;
    println!(
        "Signal 'singleOptionalStruct' was sent: {:?}",
        signal_result
    );

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'threeStructs'");
    let signal_result_future = server
        .emit_three_structs(
            AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 42],
                optional_array_of_integers: vec![42, 42],
                array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: vec![Numbers::One, Numbers::One],
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                optional_array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
                optional_array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
            },
            AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 42],
                optional_array_of_integers: vec![42, 42],
                array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: vec![Numbers::One, Numbers::One],
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                optional_array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
                optional_array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
            },
            Some(AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 42],
                optional_array_of_integers: vec![42, 42],
                array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                optional_array_of_strings: vec!["apples".to_string(), "apples".to_string()],
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: vec![Numbers::One, Numbers::One],
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                optional_array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(3536),
                ],
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
                optional_array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                ],
            }),
        )
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'threeStructs' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleDateTime'");
    let signal_result_future = server.emit_single_date_time(chrono::Utc::now()).await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleDateTime' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleOptionalDatetime'");
    let signal_result_future = server
        .emit_single_optional_datetime(Some(chrono::Utc::now()))
        .await;
    let signal_result = signal_result_future.await;
    println!(
        "Signal 'singleOptionalDatetime' was sent: {:?}",
        signal_result
    );

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'threeDateTimes'");
    let signal_result_future = server
        .emit_three_date_times(
            chrono::Utc::now(),
            chrono::Utc::now(),
            Some(chrono::Utc::now()),
        )
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'threeDateTimes' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleDuration'");
    let signal_result_future = server
        .emit_single_duration(chrono::Duration::seconds(3536))
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleDuration' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleOptionalDuration'");
    let signal_result_future = server
        .emit_single_optional_duration(Some(chrono::Duration::seconds(3536)))
        .await;
    let signal_result = signal_result_future.await;
    println!(
        "Signal 'singleOptionalDuration' was sent: {:?}",
        signal_result
    );

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'threeDurations'");
    let signal_result_future = server
        .emit_three_durations(
            chrono::Duration::seconds(3536),
            chrono::Duration::seconds(3536),
            Some(chrono::Duration::seconds(3536)),
        )
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'threeDurations' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleBinary'");
    let signal_result_future = server
        .emit_single_binary(vec![101, 120, 97, 109, 112, 108, 101])
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'singleBinary' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleOptionalBinary'");
    let signal_result_future = server
        .emit_single_optional_binary(Some(vec![101, 120, 97, 109, 112, 108, 101]))
        .await;
    let signal_result = signal_result_future.await;
    println!(
        "Signal 'singleOptionalBinary' was sent: {:?}",
        signal_result
    );

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'threeBinaries'");
    let signal_result_future = server
        .emit_three_binaries(
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
            Some(vec![101, 120, 97, 109, 112, 108, 101]),
        )
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'threeBinaries' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleArrayOfIntegers'");
    let signal_result_future = server.emit_single_array_of_integers(vec![42, 42]).await;
    let signal_result = signal_result_future.await;
    println!(
        "Signal 'singleArrayOfIntegers' was sent: {:?}",
        signal_result
    );

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'singleOptionalArrayOfStrings'");
    let signal_result_future = server
        .emit_single_optional_array_of_strings(vec![42, 42])
        .await;
    let signal_result = signal_result_future.await;
    println!(
        "Signal 'singleOptionalArrayOfStrings' was sent: {:?}",
        signal_result
    );

    sleep(Duration::from_secs(1)).await;
    println!("Emitting signal 'arrayOfEveryType'");
    let signal_result_future = server
        .emit_array_of_every_type(
            vec![42, 42],
            vec![3.14, 3.14],
            vec!["apples".to_string(), "apples".to_string()],
            vec![Numbers::One, Numbers::One],
            vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
            ],
            vec![chrono::Utc::now(), chrono::Utc::now()],
            vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(3536),
            ],
            vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
        )
        .await;
    let signal_result = signal_result_future.await;
    println!("Signal 'arrayOfEveryType' was sent: {:?}", signal_result);

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_integer'");
    let prop_change_future = server.set_read_write_integer(2022).await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_write_integer': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_only_integer'");
    let prop_change_future = server.set_read_only_integer(2022).await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_only_integer': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_optional_integer'");
    let prop_change_future = server.set_read_write_optional_integer(Some(2022)).await;
    if let Err(e) = prop_change_future.await {
        eprintln!(
            "Error changing property 'read_write_optional_integer': {:?}",
            e
        );
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_two_integers'");
    let new_value = ReadWriteTwoIntegersProperty {
        first: 2022,
        second: Some(2022),
    };
    let _ = server.set_read_write_two_integers(new_value).await;

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_only_string'");
    let prop_change_future = server.set_read_only_string("foo".to_string()).await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_only_string': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_string'");
    let prop_change_future = server.set_read_write_string("foo".to_string()).await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_write_string': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_optional_string'");
    let prop_change_future = server
        .set_read_write_optional_string(Some("foo".to_string()))
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!(
            "Error changing property 'read_write_optional_string': {:?}",
            e
        );
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_two_strings'");
    let new_value = ReadWriteTwoStringsProperty {
        first: "foo".to_string(),
        second: Some("foo".to_string()),
    };
    let _ = server.set_read_write_two_strings(new_value).await;

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_struct'");
    let prop_change_future = server
        .set_read_write_struct(AllTypes {
            the_bool: true,
            the_int: 2022,
            the_number: 1.0,
            the_str: "foo".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 2022,
                value: "foo".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(975),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(2022),
            optional_string: Some("foo".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 2022,
                value: "foo".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(975)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![2022, 2022],
            optional_array_of_integers: vec![2022, 2022],
            array_of_strings: vec!["foo".to_string(), "foo".to_string()],
            optional_array_of_strings: vec!["foo".to_string(), "foo".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(975),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
        })
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_write_struct': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_optional_struct'");
    let prop_change_future = server
        .set_read_write_optional_struct(Some(AllTypes {
            the_bool: true,
            the_int: 2022,
            the_number: 1.0,
            the_str: "foo".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 2022,
                value: "foo".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(975),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(2022),
            optional_string: Some("foo".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 2022,
                value: "foo".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(975)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![2022, 2022],
            optional_array_of_integers: vec![2022, 2022],
            array_of_strings: vec!["foo".to_string(), "foo".to_string()],
            optional_array_of_strings: vec!["foo".to_string(), "foo".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(975),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
        }))
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!(
            "Error changing property 'read_write_optional_struct': {:?}",
            e
        );
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_two_structs'");
    let new_value = ReadWriteTwoStructsProperty {
        first: AllTypes {
            the_bool: true,
            the_int: 2022,
            the_number: 1.0,
            the_str: "foo".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 2022,
                value: "foo".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(967),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(2022),
            optional_string: Some("foo".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 2022,
                value: "foo".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(967)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![2022, 2022],
            optional_array_of_integers: vec![2022, 2022],
            array_of_strings: vec!["foo".to_string(), "foo".to_string()],
            optional_array_of_strings: vec!["foo".to_string(), "foo".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(967),
                chrono::Duration::seconds(967),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(967),
                chrono::Duration::seconds(967),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
        },
        second: Some(AllTypes {
            the_bool: true,
            the_int: 2022,
            the_number: 1.0,
            the_str: "foo".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 2022,
                value: "foo".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(967),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(2022),
            optional_string: Some("foo".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 2022,
                value: "foo".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(967)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![2022, 2022],
            optional_array_of_integers: vec![2022, 2022],
            array_of_strings: vec!["foo".to_string(), "foo".to_string()],
            optional_array_of_strings: vec!["foo".to_string(), "foo".to_string()],
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: vec![Numbers::One, Numbers::One],
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            array_of_durations: vec![
                chrono::Duration::seconds(967),
                chrono::Duration::seconds(967),
            ],
            optional_array_of_durations: vec![
                chrono::Duration::seconds(967),
                chrono::Duration::seconds(967),
            ],
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            array_of_entry_objects: vec![
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: vec![
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
        }),
    };
    let _ = server.set_read_write_two_structs(new_value).await;

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_only_enum'");
    let prop_change_future = server.set_read_only_enum(Numbers::One).await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_only_enum': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_enum'");
    let prop_change_future = server.set_read_write_enum(Numbers::One).await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_write_enum': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_optional_enum'");
    let prop_change_future = server
        .set_read_write_optional_enum(Some(Numbers::One))
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!(
            "Error changing property 'read_write_optional_enum': {:?}",
            e
        );
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_two_enums'");
    let new_value = ReadWriteTwoEnumsProperty {
        first: Numbers::One,
        second: Some(Numbers::One),
    };
    let _ = server.set_read_write_two_enums(new_value).await;

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_datetime'");
    let prop_change_future = server.set_read_write_datetime(chrono::Utc::now()).await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_write_datetime': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_optional_datetime'");
    let prop_change_future = server
        .set_read_write_optional_datetime(Some(chrono::Utc::now()))
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!(
            "Error changing property 'read_write_optional_datetime': {:?}",
            e
        );
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_two_datetimes'");
    let new_value = ReadWriteTwoDatetimesProperty {
        first: chrono::Utc::now(),
        second: Some(chrono::Utc::now()),
    };
    let _ = server.set_read_write_two_datetimes(new_value).await;

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_duration'");
    let prop_change_future = server
        .set_read_write_duration(chrono::Duration::seconds(975))
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_write_duration': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_optional_duration'");
    let prop_change_future = server
        .set_read_write_optional_duration(Some(chrono::Duration::seconds(975)))
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!(
            "Error changing property 'read_write_optional_duration': {:?}",
            e
        );
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_two_durations'");
    let new_value = ReadWriteTwoDurationsProperty {
        first: chrono::Duration::seconds(967),
        second: Some(chrono::Duration::seconds(967)),
    };
    let _ = server.set_read_write_two_durations(new_value).await;

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_binary'");
    let prop_change_future = server
        .set_read_write_binary(vec![101, 120, 97, 109, 112, 108, 101])
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!("Error changing property 'read_write_binary': {:?}", e);
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_optional_binary'");
    let prop_change_future = server
        .set_read_write_optional_binary(Some(vec![101, 120, 97, 109, 112, 108, 101]))
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!(
            "Error changing property 'read_write_optional_binary': {:?}",
            e
        );
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_two_binaries'");
    let new_value = ReadWriteTwoBinariesProperty {
        first: vec![101, 120, 97, 109, 112, 108, 101],
        second: Some(vec![101, 120, 97, 109, 112, 108, 101]),
    };
    let _ = server.set_read_write_two_binaries(new_value).await;

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_list_of_strings'");
    let prop_change_future = server
        .set_read_write_list_of_strings(vec!["foo".to_string(), "foo".to_string()])
        .await;
    if let Err(e) = prop_change_future.await {
        eprintln!(
            "Error changing property 'read_write_list_of_strings': {:?}",
            e
        );
    }

    sleep(Duration::from_secs(1)).await;
    println!("Changing property 'read_write_lists'");
    let new_value = ReadWriteListsProperty {
        the_list: vec![Numbers::One, Numbers::One],
        optionalList: vec![chrono::Utc::now(), chrono::Utc::now()],
    };
    let _ = server.set_read_write_lists(new_value).await;

    // Ctrl-C to stop
}
