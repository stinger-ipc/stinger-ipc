/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use std::any::Any;

use mqttier::{Connection, MqttierClient, MqttierOptionsBuilder};
use test_able_ipc::property::TestAbleInitialPropertyValues;
use test_able_ipc::server::{TestAbleMethodHandlers, TestAbleServer};
use tokio::time::{sleep, Duration};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing_subscriber;

#[allow(unused_imports)]
use test_able_ipc::payloads::{MethodReturnCode, *};
use tokio::join;

struct TestAbleMethodImpl {
    server: Option<TestAbleServer<MqttierClient>>,
}

impl TestAbleMethodImpl {
    fn new() -> Self {
        Self { server: None }
    }
}

#[async_trait]
impl TestAbleMethodHandlers<MqttierClient> for TestAbleMethodImpl {
    async fn initialize(
        &mut self,
        server: TestAbleServer<MqttierClient>,
    ) -> Result<(), MethodReturnCode> {
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
            array_of_integers: vec![42, 2022],
            optional_array_of_integers: Some(vec![42, 2022, 2022]),
            array_of_strings: vec!["apples".to_string(), "foo".to_string()],
            optional_array_of_strings: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: Some(vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(967),
            ]),
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: Some(vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ]),
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: Some(vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ]),
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
            array_of_integers: vec![42, 2022],
            optional_array_of_integers: Some(vec![42, 2022, 2022]),
            array_of_strings: vec!["apples".to_string(), "foo".to_string()],
            optional_array_of_strings: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: Some(vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(967),
            ]),
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: Some(vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ]),
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: Some(vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ]),
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
                array_of_integers: vec![42, 2022],
                optional_array_of_integers: Some(vec![42, 2022, 2022]),
                array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                optional_array_of_strings: Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]),
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: Some(vec![
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                ]),
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                ],
                optional_array_of_durations: Some(vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                    chrono::Duration::seconds(967),
                ]),
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: Some(vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ]),
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ],
                optional_array_of_entry_objects: Some(vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ]),
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
                array_of_integers: vec![42, 2022],
                optional_array_of_integers: Some(vec![42, 2022, 2022]),
                array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                optional_array_of_strings: Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]),
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: Some(vec![
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                ]),
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                ],
                optional_array_of_durations: Some(vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                    chrono::Duration::seconds(967),
                ]),
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: Some(vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ]),
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ],
                optional_array_of_entry_objects: Some(vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ]),
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
                array_of_integers: vec![42, 2022],
                optional_array_of_integers: Some(vec![42, 2022, 2022]),
                array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                optional_array_of_strings: Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]),
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: Some(vec![
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                ]),
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                ],
                optional_array_of_durations: Some(vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                    chrono::Duration::seconds(967),
                ]),
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: Some(vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ]),
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ],
                optional_array_of_entry_objects: Some(vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ]),
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
        Ok(vec![42, 2022])
    }

    async fn handle_call_optional_list_of_floats(
        &self,
        _input1: Option<Vec<f32>>,
    ) -> Result<Option<Vec<f32>>, MethodReturnCode> {
        println!("Handling callOptionalListOfFloats");
        Ok(Some(vec![3.14, 1.0, 1.0]))
    }

    async fn handle_call_two_lists(
        &self,
        _input1: Vec<Numbers>,
        _input2: Option<Vec<String>>,
    ) -> Result<CallTwoListsReturnValues, MethodReturnCode> {
        println!("Handling callTwoLists");
        let rv = CallTwoListsReturnValues {
            output1: vec![Numbers::One, Numbers::One],
            output2: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
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

    // Set up an MQTT client connection.
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-server-demo".to_string())
        .build()
        .unwrap();
    let mut connection = MqttierClient::new(mqttier_options).unwrap();
    let _ = connection.start().await.unwrap();

    let initial_property_values = TestAbleInitialPropertyValues {
        read_write_integer: 42,
        read_write_integer_version: 1,

        read_only_integer: 42,
        read_only_integer_version: 1,

        read_write_optional_integer: Some(42),
        read_write_optional_integer_version: 1,

        read_write_two_integers: ReadWriteTwoIntegersProperty {
            first: 42,
            second: Some(42),
        },
        read_write_two_integers_version: 1,

        read_only_string: "apples".to_string(),
        read_only_string_version: 1,

        read_write_string: "apples".to_string(),
        read_write_string_version: 1,

        read_write_optional_string: Some("apples".to_string()),
        read_write_optional_string_version: 1,

        read_write_two_strings: ReadWriteTwoStringsProperty {
            first: "apples".to_string(),
            second: Some("apples".to_string()),
        },
        read_write_two_strings_version: 1,

        read_write_struct: AllTypes {
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
            array_of_integers: vec![42, 2022],
            optional_array_of_integers: Some(vec![42, 2022, 2022]),
            array_of_strings: vec!["apples".to_string(), "foo".to_string()],
            optional_array_of_strings: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: Some(vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(967),
            ]),
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: Some(vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ]),
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: Some(vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ]),
        },
        read_write_struct_version: 1,

        read_write_optional_struct: Some(AllTypes {
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
            array_of_integers: vec![42, 2022],
            optional_array_of_integers: Some(vec![42, 2022, 2022]),
            array_of_strings: vec!["apples".to_string(), "foo".to_string()],
            optional_array_of_strings: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: Some(vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(967),
            ]),
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: Some(vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ]),
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: Some(vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ]),
        }),
        read_write_optional_struct_version: 1,

        read_write_two_structs: ReadWriteTwoStructsProperty {
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
                array_of_integers: vec![42, 2022],
                optional_array_of_integers: Some(vec![42, 2022, 2022]),
                array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                optional_array_of_strings: Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]),
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: Some(vec![
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                ]),
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                ],
                optional_array_of_durations: Some(vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                    chrono::Duration::seconds(967),
                ]),
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: Some(vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ]),
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ],
                optional_array_of_entry_objects: Some(vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ]),
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
                array_of_integers: vec![42, 2022],
                optional_array_of_integers: Some(vec![42, 2022, 2022]),
                array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                optional_array_of_strings: Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]),
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: Some(vec![
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                ]),
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                ],
                optional_array_of_durations: Some(vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                    chrono::Duration::seconds(967),
                ]),
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: Some(vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ]),
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ],
                optional_array_of_entry_objects: Some(vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ]),
            }),
        },
        read_write_two_structs_version: 1,

        read_only_enum: Numbers::One,
        read_only_enum_version: 1,

        read_write_enum: Numbers::One,
        read_write_enum_version: 1,

        read_write_optional_enum: Some(Numbers::One),
        read_write_optional_enum_version: 1,

        read_write_two_enums: ReadWriteTwoEnumsProperty {
            first: Numbers::One,
            second: Some(Numbers::One),
        },
        read_write_two_enums_version: 1,

        read_write_datetime: chrono::Utc::now(),
        read_write_datetime_version: 1,

        read_write_optional_datetime: Some(chrono::Utc::now()),
        read_write_optional_datetime_version: 1,

        read_write_two_datetimes: ReadWriteTwoDatetimesProperty {
            first: chrono::Utc::now(),
            second: Some(chrono::Utc::now()),
        },
        read_write_two_datetimes_version: 1,

        read_write_duration: chrono::Duration::seconds(3536),
        read_write_duration_version: 1,

        read_write_optional_duration: Some(chrono::Duration::seconds(3536)),
        read_write_optional_duration_version: 1,

        read_write_two_durations: ReadWriteTwoDurationsProperty {
            first: chrono::Duration::seconds(3536),
            second: Some(chrono::Duration::seconds(3536)),
        },
        read_write_two_durations_version: 1,

        read_write_binary: vec![101, 120, 97, 109, 112, 108, 101],
        read_write_binary_version: 1,

        read_write_optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
        read_write_optional_binary_version: 1,

        read_write_two_binaries: ReadWriteTwoBinariesProperty {
            first: vec![101, 120, 97, 109, 112, 108, 101],
            second: Some(vec![101, 120, 97, 109, 112, 108, 101]),
        },
        read_write_two_binaries_version: 1,

        read_write_list_of_strings: vec!["apples".to_string(), "foo".to_string()],
        read_write_list_of_strings_version: 1,

        read_write_lists: ReadWriteListsProperty {
            the_list: vec![Numbers::One, Numbers::One],
            optional_list: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
        },
        read_write_lists_version: 1,
    };

    // Create an object that implements the method handlers.
    let handlers: Arc<Mutex<Box<dyn TestAbleMethodHandlers<MqttierClient>>>> =
        Arc::new(Mutex::new(Box::new(TestAbleMethodImpl::new())));

    // Create the server object.
    let mut server = TestAbleServer::new(
        connection,
        handlers.clone(),
        "rust-server-demo:1".to_string(),
        initial_property_values,
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
            println!("Emitting signal 'empty'");
            let signal_result_future = server_clone1.emit_empty().await;
            let signal_result = signal_result_future.await;
            println!("Signal 'empty' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleInt'");
            let signal_result_future = server_clone1.emit_single_int(42).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleInt' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleOptionalInt'");
            let signal_result_future = server_clone1.emit_single_optional_int(Some(42)).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleOptionalInt' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'threeIntegers'");
            let signal_result_future = server_clone1.emit_three_integers(42, 42, Some(42)).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'threeIntegers' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleString'");
            let signal_result_future = server_clone1.emit_single_string("apples".to_string()).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleString' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleOptionalString'");
            let signal_result_future = server_clone1
                .emit_single_optional_string(Some("apples".to_string()))
                .await;
            let signal_result = signal_result_future.await;
            println!(
                "Signal 'singleOptionalString' was sent: {:?}",
                signal_result
            );

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'threeStrings'");
            let signal_result_future = server_clone1
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
            let signal_result_future = server_clone1.emit_single_enum(Numbers::One).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleEnum' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleOptionalEnum'");
            let signal_result_future = server_clone1
                .emit_single_optional_enum(Some(Numbers::One))
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleOptionalEnum' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'threeEnums'");
            let signal_result_future = server_clone1
                .emit_three_enums(Numbers::One, Numbers::One, Some(Numbers::One))
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'threeEnums' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleStruct'");
            let signal_result_future = server_clone1
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
                    array_of_integers: vec![42, 2022],
                    optional_array_of_integers: Some(vec![42, 2022, 2022]),
                    array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                    optional_array_of_strings: Some(vec![
                        "apples".to_string(),
                        "foo".to_string(),
                        "foo".to_string(),
                    ]),
                    array_of_enums: vec![Numbers::One, Numbers::One],
                    optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                    array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                    optional_array_of_datetimes: Some(vec![
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                    ]),
                    array_of_durations: vec![
                        chrono::Duration::seconds(3536),
                        chrono::Duration::seconds(975),
                    ],
                    optional_array_of_durations: Some(vec![
                        chrono::Duration::seconds(3536),
                        chrono::Duration::seconds(975),
                        chrono::Duration::seconds(967),
                    ]),
                    array_of_binaries: vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ],
                    optional_array_of_binaries: Some(vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ]),
                    array_of_entry_objects: vec![
                        Entry {
                            key: 42,
                            value: "apples".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                    ],
                    optional_array_of_entry_objects: Some(vec![
                        Entry {
                            key: 42,
                            value: "apples".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                    ]),
                })
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleStruct' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleOptionalStruct'");
            let signal_result_future = server_clone1
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
                    array_of_integers: vec![42, 2022],
                    optional_array_of_integers: Some(vec![42, 2022, 2022]),
                    array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                    optional_array_of_strings: Some(vec![
                        "apples".to_string(),
                        "foo".to_string(),
                        "foo".to_string(),
                    ]),
                    array_of_enums: vec![Numbers::One, Numbers::One],
                    optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                    array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                    optional_array_of_datetimes: Some(vec![
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                    ]),
                    array_of_durations: vec![
                        chrono::Duration::seconds(3536),
                        chrono::Duration::seconds(975),
                    ],
                    optional_array_of_durations: Some(vec![
                        chrono::Duration::seconds(3536),
                        chrono::Duration::seconds(975),
                        chrono::Duration::seconds(967),
                    ]),
                    array_of_binaries: vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ],
                    optional_array_of_binaries: Some(vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ]),
                    array_of_entry_objects: vec![
                        Entry {
                            key: 42,
                            value: "apples".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                    ],
                    optional_array_of_entry_objects: Some(vec![
                        Entry {
                            key: 42,
                            value: "apples".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                    ]),
                }))
                .await;
            let signal_result = signal_result_future.await;
            println!(
                "Signal 'singleOptionalStruct' was sent: {:?}",
                signal_result
            );

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'threeStructs'");
            let signal_result_future = server_clone1
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
                        array_of_integers: vec![42, 2022],
                        optional_array_of_integers: Some(vec![42, 2022, 2022]),
                        array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                        optional_array_of_strings: Some(vec![
                            "apples".to_string(),
                            "foo".to_string(),
                            "foo".to_string(),
                        ]),
                        array_of_enums: vec![Numbers::One, Numbers::One],
                        optional_array_of_enums: Some(vec![
                            Numbers::One,
                            Numbers::One,
                            Numbers::One,
                        ]),
                        array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                        optional_array_of_datetimes: Some(vec![
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                        ]),
                        array_of_durations: vec![
                            chrono::Duration::seconds(3536),
                            chrono::Duration::seconds(975),
                        ],
                        optional_array_of_durations: Some(vec![
                            chrono::Duration::seconds(3536),
                            chrono::Duration::seconds(975),
                            chrono::Duration::seconds(967),
                        ]),
                        array_of_binaries: vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ],
                        optional_array_of_binaries: Some(vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ]),
                        array_of_entry_objects: vec![
                            Entry {
                                key: 42,
                                value: "apples".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                        ],
                        optional_array_of_entry_objects: Some(vec![
                            Entry {
                                key: 42,
                                value: "apples".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                        ]),
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
                        array_of_integers: vec![42, 2022],
                        optional_array_of_integers: Some(vec![42, 2022, 2022]),
                        array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                        optional_array_of_strings: Some(vec![
                            "apples".to_string(),
                            "foo".to_string(),
                            "foo".to_string(),
                        ]),
                        array_of_enums: vec![Numbers::One, Numbers::One],
                        optional_array_of_enums: Some(vec![
                            Numbers::One,
                            Numbers::One,
                            Numbers::One,
                        ]),
                        array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                        optional_array_of_datetimes: Some(vec![
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                        ]),
                        array_of_durations: vec![
                            chrono::Duration::seconds(3536),
                            chrono::Duration::seconds(975),
                        ],
                        optional_array_of_durations: Some(vec![
                            chrono::Duration::seconds(3536),
                            chrono::Duration::seconds(975),
                            chrono::Duration::seconds(967),
                        ]),
                        array_of_binaries: vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ],
                        optional_array_of_binaries: Some(vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ]),
                        array_of_entry_objects: vec![
                            Entry {
                                key: 42,
                                value: "apples".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                        ],
                        optional_array_of_entry_objects: Some(vec![
                            Entry {
                                key: 42,
                                value: "apples".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                        ]),
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
                        array_of_integers: vec![42, 2022],
                        optional_array_of_integers: Some(vec![42, 2022, 2022]),
                        array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                        optional_array_of_strings: Some(vec![
                            "apples".to_string(),
                            "foo".to_string(),
                            "foo".to_string(),
                        ]),
                        array_of_enums: vec![Numbers::One, Numbers::One],
                        optional_array_of_enums: Some(vec![
                            Numbers::One,
                            Numbers::One,
                            Numbers::One,
                        ]),
                        array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                        optional_array_of_datetimes: Some(vec![
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                        ]),
                        array_of_durations: vec![
                            chrono::Duration::seconds(3536),
                            chrono::Duration::seconds(975),
                        ],
                        optional_array_of_durations: Some(vec![
                            chrono::Duration::seconds(3536),
                            chrono::Duration::seconds(975),
                            chrono::Duration::seconds(967),
                        ]),
                        array_of_binaries: vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ],
                        optional_array_of_binaries: Some(vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ]),
                        array_of_entry_objects: vec![
                            Entry {
                                key: 42,
                                value: "apples".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                        ],
                        optional_array_of_entry_objects: Some(vec![
                            Entry {
                                key: 42,
                                value: "apples".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                        ]),
                    }),
                )
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'threeStructs' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleDateTime'");
            let signal_result_future = server_clone1
                .emit_single_date_time(chrono::Utc::now())
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleDateTime' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleOptionalDatetime'");
            let signal_result_future = server_clone1
                .emit_single_optional_datetime(Some(chrono::Utc::now()))
                .await;
            let signal_result = signal_result_future.await;
            println!(
                "Signal 'singleOptionalDatetime' was sent: {:?}",
                signal_result
            );

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'threeDateTimes'");
            let signal_result_future = server_clone1
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
            let signal_result_future = server_clone1
                .emit_single_duration(chrono::Duration::seconds(3536))
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleDuration' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleOptionalDuration'");
            let signal_result_future = server_clone1
                .emit_single_optional_duration(Some(chrono::Duration::seconds(3536)))
                .await;
            let signal_result = signal_result_future.await;
            println!(
                "Signal 'singleOptionalDuration' was sent: {:?}",
                signal_result
            );

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'threeDurations'");
            let signal_result_future = server_clone1
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
            let signal_result_future = server_clone1
                .emit_single_binary(vec![101, 120, 97, 109, 112, 108, 101])
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'singleBinary' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleOptionalBinary'");
            let signal_result_future = server_clone1
                .emit_single_optional_binary(Some(vec![101, 120, 97, 109, 112, 108, 101]))
                .await;
            let signal_result = signal_result_future.await;
            println!(
                "Signal 'singleOptionalBinary' was sent: {:?}",
                signal_result
            );

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'threeBinaries'");
            let signal_result_future = server_clone1
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
            let signal_result_future = server_clone1
                .emit_single_array_of_integers(vec![42, 2022])
                .await;
            let signal_result = signal_result_future.await;
            println!(
                "Signal 'singleArrayOfIntegers' was sent: {:?}",
                signal_result
            );

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'singleOptionalArrayOfStrings'");
            let signal_result_future = server_clone1
                .emit_single_optional_array_of_strings(Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]))
                .await;
            let signal_result = signal_result_future.await;
            println!(
                "Signal 'singleOptionalArrayOfStrings' was sent: {:?}",
                signal_result
            );

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'arrayOfEveryType'");
            let signal_result_future = server_clone1
                .emit_array_of_every_type(
                    vec![42, 2022],
                    vec![3.14, 1.0],
                    vec!["apples".to_string(), "foo".to_string()],
                    vec![Numbers::One, Numbers::One],
                    vec![
                        Entry {
                            key: 42,
                            value: "apples".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                    ],
                    vec![chrono::Utc::now(), chrono::Utc::now()],
                    vec![
                        chrono::Duration::seconds(3536),
                        chrono::Duration::seconds(975),
                    ],
                    vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ],
                )
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'arrayOfEveryType' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(67)).await;
        }
    });

    let read_write_integer_property = server.get_read_write_integer_handle();

    let read_only_integer_property = server.get_read_only_integer_handle();

    let read_write_optional_integer_property = server.get_read_write_optional_integer_handle();

    let read_write_two_integers_property = server.get_read_write_two_integers_handle();

    let read_only_string_property = server.get_read_only_string_handle();

    let read_write_string_property = server.get_read_write_string_handle();

    let read_write_optional_string_property = server.get_read_write_optional_string_handle();

    let read_write_two_strings_property = server.get_read_write_two_strings_handle();

    let read_write_struct_property = server.get_read_write_struct_handle();

    let read_write_optional_struct_property = server.get_read_write_optional_struct_handle();

    let read_write_two_structs_property = server.get_read_write_two_structs_handle();

    let read_only_enum_property = server.get_read_only_enum_handle();

    let read_write_enum_property = server.get_read_write_enum_handle();

    let read_write_optional_enum_property = server.get_read_write_optional_enum_handle();

    let read_write_two_enums_property = server.get_read_write_two_enums_handle();

    let read_write_datetime_property = server.get_read_write_datetime_handle();

    let read_write_optional_datetime_property = server.get_read_write_optional_datetime_handle();

    let read_write_two_datetimes_property = server.get_read_write_two_datetimes_handle();

    let read_write_duration_property = server.get_read_write_duration_handle();

    let read_write_optional_duration_property = server.get_read_write_optional_duration_handle();

    let read_write_two_durations_property = server.get_read_write_two_durations_handle();

    let read_write_binary_property = server.get_read_write_binary_handle();

    let read_write_optional_binary_property = server.get_read_write_optional_binary_handle();

    let read_write_two_binaries_property = server.get_read_write_two_binaries_handle();

    let read_write_list_of_strings_property = server.get_read_write_list_of_strings_handle();

    let read_write_lists_property = server.get_read_write_lists_handle();
    let property_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(51)).await;

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_integer'");
                let mut read_write_integer_guard = read_write_integer_property.write().await;
                *read_write_integer_guard = 2022;
                // Value is changed and published when read_write_integer_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_only_integer'");
                let mut read_only_integer_guard = read_only_integer_property.write().await;
                *read_only_integer_guard = 2022;
                // Value is changed and published when read_only_integer_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_optional_integer'");
                let mut read_write_optional_integer_guard =
                    read_write_optional_integer_property.write().await;
                *read_write_optional_integer_guard = Some(2022);
                // Value is changed and published when read_write_optional_integer_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_two_integers'");
                let mut read_write_two_integers_guard =
                    read_write_two_integers_property.write().await;
                let new_read_write_two_integers_value = ReadWriteTwoIntegersProperty {
                    first: 2022,
                    second: Some(2022),
                };
                *read_write_two_integers_guard = new_read_write_two_integers_value;
                // Value is changed and published when read_write_two_integers_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_only_string'");
                let mut read_only_string_guard = read_only_string_property.write().await;
                *read_only_string_guard = "foo".to_string();
                // Value is changed and published when read_only_string_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_string'");
                let mut read_write_string_guard = read_write_string_property.write().await;
                *read_write_string_guard = "foo".to_string();
                // Value is changed and published when read_write_string_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_optional_string'");
                let mut read_write_optional_string_guard =
                    read_write_optional_string_property.write().await;
                *read_write_optional_string_guard = Some("foo".to_string());
                // Value is changed and published when read_write_optional_string_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_two_strings'");
                let mut read_write_two_strings_guard =
                    read_write_two_strings_property.write().await;
                let new_read_write_two_strings_value = ReadWriteTwoStringsProperty {
                    first: "foo".to_string(),
                    second: Some("foo".to_string()),
                };
                *read_write_two_strings_guard = new_read_write_two_strings_value;
                // Value is changed and published when read_write_two_strings_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_struct'");
                let mut read_write_struct_guard = read_write_struct_property.write().await;
                *read_write_struct_guard = AllTypes {
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
                    optional_array_of_integers: Some(vec![2022, 2022, 1955]),
                    array_of_strings: vec!["foo".to_string(), "foo".to_string()],
                    optional_array_of_strings: Some(vec![
                        "foo".to_string(),
                        "foo".to_string(),
                        "bar".to_string(),
                    ]),
                    array_of_enums: vec![Numbers::One, Numbers::One],
                    optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::Three]),
                    array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                    optional_array_of_datetimes: Some(vec![
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                    ]),
                    array_of_durations: vec![
                        chrono::Duration::seconds(975),
                        chrono::Duration::seconds(967),
                    ],
                    optional_array_of_durations: Some(vec![
                        chrono::Duration::seconds(975),
                        chrono::Duration::seconds(967),
                        chrono::Duration::seconds(2552),
                    ]),
                    array_of_binaries: vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ],
                    optional_array_of_binaries: Some(vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ]),
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
                    optional_array_of_entry_objects: Some(vec![
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                        Entry {
                            key: 1955,
                            value: "bar".to_string(),
                        },
                    ]),
                };
                // Value is changed and published when read_write_struct_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_optional_struct'");
                let mut read_write_optional_struct_guard =
                    read_write_optional_struct_property.write().await;
                *read_write_optional_struct_guard = Some(AllTypes {
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
                    optional_array_of_integers: Some(vec![2022, 2022, 1955]),
                    array_of_strings: vec!["foo".to_string(), "foo".to_string()],
                    optional_array_of_strings: Some(vec![
                        "foo".to_string(),
                        "foo".to_string(),
                        "bar".to_string(),
                    ]),
                    array_of_enums: vec![Numbers::One, Numbers::One],
                    optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::Three]),
                    array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                    optional_array_of_datetimes: Some(vec![
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                    ]),
                    array_of_durations: vec![
                        chrono::Duration::seconds(975),
                        chrono::Duration::seconds(967),
                    ],
                    optional_array_of_durations: Some(vec![
                        chrono::Duration::seconds(975),
                        chrono::Duration::seconds(967),
                        chrono::Duration::seconds(2552),
                    ]),
                    array_of_binaries: vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ],
                    optional_array_of_binaries: Some(vec![
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                        vec![101, 120, 97, 109, 112, 108, 101],
                    ]),
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
                    optional_array_of_entry_objects: Some(vec![
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                        Entry {
                            key: 2022,
                            value: "foo".to_string(),
                        },
                        Entry {
                            key: 1955,
                            value: "bar".to_string(),
                        },
                    ]),
                });
                // Value is changed and published when read_write_optional_struct_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_two_structs'");
                let mut read_write_two_structs_guard =
                    read_write_two_structs_property.write().await;
                let new_read_write_two_structs_value = ReadWriteTwoStructsProperty {
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
                        array_of_integers: vec![2022, 1955],
                        optional_array_of_integers: Some(vec![2022, 1955, 1955]),
                        array_of_strings: vec!["foo".to_string(), "bar".to_string()],
                        optional_array_of_strings: Some(vec![
                            "foo".to_string(),
                            "bar".to_string(),
                            "Joe".to_string(),
                        ]),
                        array_of_enums: vec![Numbers::One, Numbers::Three],
                        optional_array_of_enums: Some(vec![
                            Numbers::One,
                            Numbers::Three,
                            Numbers::Three,
                        ]),
                        array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                        optional_array_of_datetimes: Some(vec![
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                        ]),
                        array_of_durations: vec![
                            chrono::Duration::seconds(967),
                            chrono::Duration::seconds(2552),
                        ],
                        optional_array_of_durations: Some(vec![
                            chrono::Duration::seconds(967),
                            chrono::Duration::seconds(2552),
                            chrono::Duration::seconds(3250),
                        ]),
                        array_of_binaries: vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ],
                        optional_array_of_binaries: Some(vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ]),
                        array_of_entry_objects: vec![
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                            Entry {
                                key: 1955,
                                value: "bar".to_string(),
                            },
                        ],
                        optional_array_of_entry_objects: Some(vec![
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                            Entry {
                                key: 1955,
                                value: "bar".to_string(),
                            },
                            Entry {
                                key: 1955,
                                value: "Joe".to_string(),
                            },
                        ]),
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
                        array_of_integers: vec![2022, 1955],
                        optional_array_of_integers: Some(vec![2022, 1955, 1955]),
                        array_of_strings: vec!["foo".to_string(), "bar".to_string()],
                        optional_array_of_strings: Some(vec![
                            "foo".to_string(),
                            "bar".to_string(),
                            "Joe".to_string(),
                        ]),
                        array_of_enums: vec![Numbers::One, Numbers::Three],
                        optional_array_of_enums: Some(vec![
                            Numbers::One,
                            Numbers::Three,
                            Numbers::Three,
                        ]),
                        array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                        optional_array_of_datetimes: Some(vec![
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                            chrono::Utc::now(),
                        ]),
                        array_of_durations: vec![
                            chrono::Duration::seconds(967),
                            chrono::Duration::seconds(2552),
                        ],
                        optional_array_of_durations: Some(vec![
                            chrono::Duration::seconds(967),
                            chrono::Duration::seconds(2552),
                            chrono::Duration::seconds(3250),
                        ]),
                        array_of_binaries: vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ],
                        optional_array_of_binaries: Some(vec![
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                            vec![101, 120, 97, 109, 112, 108, 101],
                        ]),
                        array_of_entry_objects: vec![
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                            Entry {
                                key: 1955,
                                value: "bar".to_string(),
                            },
                        ],
                        optional_array_of_entry_objects: Some(vec![
                            Entry {
                                key: 2022,
                                value: "foo".to_string(),
                            },
                            Entry {
                                key: 1955,
                                value: "bar".to_string(),
                            },
                            Entry {
                                key: 1955,
                                value: "Joe".to_string(),
                            },
                        ]),
                    }),
                };
                *read_write_two_structs_guard = new_read_write_two_structs_value;
                // Value is changed and published when read_write_two_structs_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_only_enum'");
                let mut read_only_enum_guard = read_only_enum_property.write().await;
                *read_only_enum_guard = Numbers::One;
                // Value is changed and published when read_only_enum_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_enum'");
                let mut read_write_enum_guard = read_write_enum_property.write().await;
                *read_write_enum_guard = Numbers::One;
                // Value is changed and published when read_write_enum_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_optional_enum'");
                let mut read_write_optional_enum_guard =
                    read_write_optional_enum_property.write().await;
                *read_write_optional_enum_guard = Some(Numbers::One);
                // Value is changed and published when read_write_optional_enum_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_two_enums'");
                let mut read_write_two_enums_guard = read_write_two_enums_property.write().await;
                let new_read_write_two_enums_value = ReadWriteTwoEnumsProperty {
                    first: Numbers::One,
                    second: Some(Numbers::One),
                };
                *read_write_two_enums_guard = new_read_write_two_enums_value;
                // Value is changed and published when read_write_two_enums_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_datetime'");
                let mut read_write_datetime_guard = read_write_datetime_property.write().await;
                *read_write_datetime_guard = chrono::Utc::now();
                // Value is changed and published when read_write_datetime_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_optional_datetime'");
                let mut read_write_optional_datetime_guard =
                    read_write_optional_datetime_property.write().await;
                *read_write_optional_datetime_guard = Some(chrono::Utc::now());
                // Value is changed and published when read_write_optional_datetime_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_two_datetimes'");
                let mut read_write_two_datetimes_guard =
                    read_write_two_datetimes_property.write().await;
                let new_read_write_two_datetimes_value = ReadWriteTwoDatetimesProperty {
                    first: chrono::Utc::now(),
                    second: Some(chrono::Utc::now()),
                };
                *read_write_two_datetimes_guard = new_read_write_two_datetimes_value;
                // Value is changed and published when read_write_two_datetimes_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_duration'");
                let mut read_write_duration_guard = read_write_duration_property.write().await;
                *read_write_duration_guard = chrono::Duration::seconds(975);
                // Value is changed and published when read_write_duration_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_optional_duration'");
                let mut read_write_optional_duration_guard =
                    read_write_optional_duration_property.write().await;
                *read_write_optional_duration_guard = Some(chrono::Duration::seconds(975));
                // Value is changed and published when read_write_optional_duration_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_two_durations'");
                let mut read_write_two_durations_guard =
                    read_write_two_durations_property.write().await;
                let new_read_write_two_durations_value = ReadWriteTwoDurationsProperty {
                    first: chrono::Duration::seconds(967),
                    second: Some(chrono::Duration::seconds(967)),
                };
                *read_write_two_durations_guard = new_read_write_two_durations_value;
                // Value is changed and published when read_write_two_durations_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_binary'");
                let mut read_write_binary_guard = read_write_binary_property.write().await;
                *read_write_binary_guard = vec![101, 120, 97, 109, 112, 108, 101];
                // Value is changed and published when read_write_binary_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_optional_binary'");
                let mut read_write_optional_binary_guard =
                    read_write_optional_binary_property.write().await;
                *read_write_optional_binary_guard = Some(vec![101, 120, 97, 109, 112, 108, 101]);
                // Value is changed and published when read_write_optional_binary_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_two_binaries'");
                let mut read_write_two_binaries_guard =
                    read_write_two_binaries_property.write().await;
                let new_read_write_two_binaries_value = ReadWriteTwoBinariesProperty {
                    first: vec![101, 120, 97, 109, 112, 108, 101],
                    second: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                };
                *read_write_two_binaries_guard = new_read_write_two_binaries_value;
                // Value is changed and published when read_write_two_binaries_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_list_of_strings'");
                let mut read_write_list_of_strings_guard =
                    read_write_list_of_strings_property.write().await;
                *read_write_list_of_strings_guard = vec!["foo".to_string(), "foo".to_string()];
                // Value is changed and published when read_write_list_of_strings_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'read_write_lists'");
                let mut read_write_lists_guard = read_write_lists_property.write().await;
                let new_read_write_lists_value = ReadWriteListsProperty {
                    the_list: vec![Numbers::One, Numbers::Three],
                    optional_list: Some(vec![
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                        chrono::Utc::now(),
                    ]),
                };
                *read_write_lists_guard = new_read_write_lists_value;
                // Value is changed and published when read_write_lists_guard goes out of scope and is dropped.
            }
        }
    });

    let _ = join!(signal_publish_task, property_publish_task);

    // Ctrl-C to stop
}
