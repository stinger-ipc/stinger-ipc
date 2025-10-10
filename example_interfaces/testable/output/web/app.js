const clientId = "Test Able-web-" + new Date().getTime();

const responseTopic = "client/" + clientId + "/responses";
var responseSubscriptionId = null;

function makeRequestProperties() {
    const correlationData = Math.random().toString(16).substr(2, 8);
    return {
        "contentType": "application/json",
        "correlationData": correlationData,
        "responseTopic": responseTopic
    }
}

var app = angular.module("myApp", []);

app.controller("myCtrl", function ($scope, $filter, $location) {

    console.log("Running app");

    var subscription_state = 0;

    $scope.timePattern = new RegExp("^[0-2][0-9]:[0-5][0-9]$");
    $scope.online = false;

    $scope.enums = {
        "numbers": [
            {"name": "one", "id": 1 },
            
            {"name": "two", "id": 2 },
            
            {"name": "three", "id": 3 }
            ]
    };

    $scope.signals = {
        "empty": {
            "subscription_id": null,
            "name": "empty",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/empty"
        },
    
        "single_int": {
            "subscription_id": null,
            "name": "singleInt",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleInt"
        },
    
        "single_optional_int": {
            "subscription_id": null,
            "name": "singleOptionalInt",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleOptionalInt"
        },
    
        "three_integers": {
            "subscription_id": null,
            "name": "threeIntegers",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/threeIntegers"
        },
    
        "single_string": {
            "subscription_id": null,
            "name": "singleString",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleString"
        },
    
        "single_optional_string": {
            "subscription_id": null,
            "name": "singleOptionalString",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleOptionalString"
        },
    
        "three_strings": {
            "subscription_id": null,
            "name": "threeStrings",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/threeStrings"
        },
    
        "single_enum": {
            "subscription_id": null,
            "name": "singleEnum",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleEnum"
        },
    
        "single_optional_enum": {
            "subscription_id": null,
            "name": "singleOptionalEnum",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleOptionalEnum"
        },
    
        "three_enums": {
            "subscription_id": null,
            "name": "threeEnums",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/threeEnums"
        },
    
        "single_struct": {
            "subscription_id": null,
            "name": "singleStruct",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleStruct"
        },
    
        "single_optional_struct": {
            "subscription_id": null,
            "name": "singleOptionalStruct",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleOptionalStruct"
        },
    
        "three_structs": {
            "subscription_id": null,
            "name": "threeStructs",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/threeStructs"
        },
    
        "single_date_time": {
            "subscription_id": null,
            "name": "singleDateTime",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleDateTime"
        },
    
        "single_optional_datetime": {
            "subscription_id": null,
            "name": "singleOptionalDatetime",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleOptionalDatetime"
        },
    
        "three_date_times": {
            "subscription_id": null,
            "name": "threeDateTimes",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/threeDateTimes"
        },
    
        "single_duration": {
            "subscription_id": null,
            "name": "singleDuration",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleDuration"
        },
    
        "single_optional_duration": {
            "subscription_id": null,
            "name": "singleOptionalDuration",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleOptionalDuration"
        },
    
        "three_durations": {
            "subscription_id": null,
            "name": "threeDurations",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/threeDurations"
        },
    
        "single_binary": {
            "subscription_id": null,
            "name": "singleBinary",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleBinary"
        },
    
        "single_optional_binary": {
            "subscription_id": null,
            "name": "singleOptionalBinary",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/singleOptionalBinary"
        },
    
        "three_binaries": {
            "subscription_id": null,
            "name": "threeBinaries",
            "received": null,
            "received_time": null,
            "mqtt_topic": "testAble/{}/signal/threeBinaries"
        }
    };

    $scope.properties = {
        "read_write_integer": {
            "subscription_id": null,
            "name": "read_write_integer",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteInteger/value",
            "update_topic": "testAble/{}/property/readWriteInteger/setValue"
        },
    
        "read_only_integer": {
            "subscription_id": null,
            "name": "read_only_integer",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readOnlyInteger/value"
        },
    
        "read_write_optional_integer": {
            "subscription_id": null,
            "name": "read_write_optional_integer",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteOptionalInteger/value",
            "update_topic": "testAble/{}/property/readWriteOptionalInteger/setValue"
        },
    
        "read_write_two_integers": {
            "subscription_id": null,
            "name": "read_write_two_integers",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteTwoIntegers/value",
            "update_topic": "testAble/{}/property/readWriteTwoIntegers/setValue"
        },
    
        "read_only_string": {
            "subscription_id": null,
            "name": "read_only_string",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readOnlyString/value"
        },
    
        "read_write_string": {
            "subscription_id": null,
            "name": "read_write_string",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteString/value",
            "update_topic": "testAble/{}/property/readWriteString/setValue"
        },
    
        "read_write_optional_string": {
            "subscription_id": null,
            "name": "read_write_optional_string",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteOptionalString/value",
            "update_topic": "testAble/{}/property/readWriteOptionalString/setValue"
        },
    
        "read_write_two_strings": {
            "subscription_id": null,
            "name": "read_write_two_strings",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteTwoStrings/value",
            "update_topic": "testAble/{}/property/readWriteTwoStrings/setValue"
        },
    
        "read_write_struct": {
            "subscription_id": null,
            "name": "read_write_struct",
            "received": { 
                "value": { 
                    "the_bool": "",
                
                    "the_int": "",
                
                    "the_number": "",
                
                    "the_str": "",
                
                    "the_enum": "",
                
                    "date_and_time": "",
                
                    "time_duration": "",
                
                    "data": "",
                
                    "optional_integer": "",
                
                    "optional_string": "",
                
                    "optional_enum": "",
                
                    "optional_date_time": "",
                
                    "optional_duration": "",
                
                    "optional_binary": ""
                 }
             },
            "mqtt_topic": "testAble/{}/property/readWriteStruct/value",
            "update_topic": "testAble/{}/property/readWriteStruct/setValue"
        },
    
        "read_write_optional_struct": {
            "subscription_id": null,
            "name": "read_write_optional_struct",
            "received": { 
                "value": { 
                    "the_bool": "",
                
                    "the_int": "",
                
                    "the_number": "",
                
                    "the_str": "",
                
                    "the_enum": "",
                
                    "date_and_time": "",
                
                    "time_duration": "",
                
                    "data": "",
                
                    "optional_integer": "",
                
                    "optional_string": "",
                
                    "optional_enum": "",
                
                    "optional_date_time": "",
                
                    "optional_duration": "",
                
                    "optional_binary": ""
                 }
             },
            "mqtt_topic": "testAble/{}/property/readWriteOptionalStruct/value",
            "update_topic": "testAble/{}/property/readWriteOptionalStruct/setValue"
        },
    
        "read_write_two_structs": {
            "subscription_id": null,
            "name": "read_write_two_structs",
            "received": { 
                "first": { 
                    "the_bool": "",
                
                    "the_int": "",
                
                    "the_number": "",
                
                    "the_str": "",
                
                    "the_enum": "",
                
                    "date_and_time": "",
                
                    "time_duration": "",
                
                    "data": "",
                
                    "optional_integer": "",
                
                    "optional_string": "",
                
                    "optional_enum": "",
                
                    "optional_date_time": "",
                
                    "optional_duration": "",
                
                    "optional_binary": ""
                 },
            
                "second": { 
                    "the_bool": "",
                
                    "the_int": "",
                
                    "the_number": "",
                
                    "the_str": "",
                
                    "the_enum": "",
                
                    "date_and_time": "",
                
                    "time_duration": "",
                
                    "data": "",
                
                    "optional_integer": "",
                
                    "optional_string": "",
                
                    "optional_enum": "",
                
                    "optional_date_time": "",
                
                    "optional_duration": "",
                
                    "optional_binary": ""
                 }
             },
            "mqtt_topic": "testAble/{}/property/readWriteTwoStructs/value",
            "update_topic": "testAble/{}/property/readWriteTwoStructs/setValue"
        },
    
        "read_only_enum": {
            "subscription_id": null,
            "name": "read_only_enum",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readOnlyEnum/value"
        },
    
        "read_write_enum": {
            "subscription_id": null,
            "name": "read_write_enum",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteEnum/value",
            "update_topic": "testAble/{}/property/readWriteEnum/setValue"
        },
    
        "read_write_optional_enum": {
            "subscription_id": null,
            "name": "read_write_optional_enum",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteOptionalEnum/value",
            "update_topic": "testAble/{}/property/readWriteOptionalEnum/setValue"
        },
    
        "read_write_two_enums": {
            "subscription_id": null,
            "name": "read_write_two_enums",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteTwoEnums/value",
            "update_topic": "testAble/{}/property/readWriteTwoEnums/setValue"
        },
    
        "read_write_datetime": {
            "subscription_id": null,
            "name": "read_write_datetime",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteDatetime/value",
            "update_topic": "testAble/{}/property/readWriteDatetime/setValue"
        },
    
        "read_write_optional_datetime": {
            "subscription_id": null,
            "name": "read_write_optional_datetime",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteOptionalDatetime/value",
            "update_topic": "testAble/{}/property/readWriteOptionalDatetime/setValue"
        },
    
        "read_write_two_datetimes": {
            "subscription_id": null,
            "name": "read_write_two_datetimes",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteTwoDatetimes/value",
            "update_topic": "testAble/{}/property/readWriteTwoDatetimes/setValue"
        },
    
        "read_write_duration": {
            "subscription_id": null,
            "name": "read_write_duration",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteDuration/value",
            "update_topic": "testAble/{}/property/readWriteDuration/setValue"
        },
    
        "read_write_optional_duration": {
            "subscription_id": null,
            "name": "read_write_optional_duration",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteOptionalDuration/value",
            "update_topic": "testAble/{}/property/readWriteOptionalDuration/setValue"
        },
    
        "read_write_two_durations": {
            "subscription_id": null,
            "name": "read_write_two_durations",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteTwoDurations/value",
            "update_topic": "testAble/{}/property/readWriteTwoDurations/setValue"
        },
    
        "read_write_binary": {
            "subscription_id": null,
            "name": "read_write_binary",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteBinary/value",
            "update_topic": "testAble/{}/property/readWriteBinary/setValue"
        },
    
        "read_write_optional_binary": {
            "subscription_id": null,
            "name": "read_write_optional_binary",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteOptionalBinary/value",
            "update_topic": "testAble/{}/property/readWriteOptionalBinary/setValue"
        },
    
        "read_write_two_binaries": {
            "subscription_id": null,
            "name": "read_write_two_binaries",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "testAble/{}/property/readWriteTwoBinaries/value",
            "update_topic": "testAble/{}/property/readWriteTwoBinaries/setValue"
        }
    };

    $scope.methods = {
        "call_with_nothing": {
            "name": "callWithNothing",
            "mqtt_topic": "testAble/{}/method/callWithNothing",
            "response_topic": "client/"+clientId+"/callWithNothing/response",
            "pending_correlation_id": null,
            "args": {},
            "received": null,
            "received_time": null
        },
        "call_one_integer": {
            "name": "callOneInteger",
            "mqtt_topic": "testAble/{}/method/callOneInteger",
            "response_topic": "client/"+clientId+"/callOneInteger/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "ArgPrimitiveType.INTEGER",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_optional_integer": {
            "name": "callOptionalInteger",
            "mqtt_topic": "testAble/{}/method/callOptionalInteger",
            "response_topic": "client/"+clientId+"/callOptionalInteger/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "ArgPrimitiveType.INTEGER",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_three_integers": {
            "name": "callThreeIntegers",
            "mqtt_topic": "testAble/{}/method/callThreeIntegers",
            "response_topic": "client/"+clientId+"/callThreeIntegers/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "ArgPrimitiveType.INTEGER",
                    "value": null
                },
            
                "input2": {
                    "type": "ArgPrimitiveType.INTEGER",
                    "value": null
                },
            
                "input3": {
                    "type": "ArgPrimitiveType.INTEGER",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_one_string": {
            "name": "callOneString",
            "mqtt_topic": "testAble/{}/method/callOneString",
            "response_topic": "client/"+clientId+"/callOneString/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "ArgPrimitiveType.STRING",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_optional_string": {
            "name": "callOptionalString",
            "mqtt_topic": "testAble/{}/method/callOptionalString",
            "response_topic": "client/"+clientId+"/callOptionalString/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "ArgPrimitiveType.STRING",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_three_strings": {
            "name": "callThreeStrings",
            "mqtt_topic": "testAble/{}/method/callThreeStrings",
            "response_topic": "client/"+clientId+"/callThreeStrings/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "ArgPrimitiveType.STRING",
                    "value": null
                },
            
                "input2": {
                    "type": "ArgPrimitiveType.STRING",
                    "value": null
                },
            
                "input3": {
                    "type": "ArgPrimitiveType.STRING",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_one_enum": {
            "name": "callOneEnum",
            "mqtt_topic": "testAble/{}/method/callOneEnum",
            "response_topic": "client/"+clientId+"/callOneEnum/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_optional_enum": {
            "name": "callOptionalEnum",
            "mqtt_topic": "testAble/{}/method/callOptionalEnum",
            "response_topic": "client/"+clientId+"/callOptionalEnum/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_three_enums": {
            "name": "callThreeEnums",
            "mqtt_topic": "testAble/{}/method/callThreeEnums",
            "response_topic": "client/"+clientId+"/callThreeEnums/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                },
            
                "input2": {
                    "type": "",
                    "value": null
                },
            
                "input3": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_one_struct": {
            "name": "callOneStruct",
            "mqtt_topic": "testAble/{}/method/callOneStruct",
            "response_topic": "client/"+clientId+"/callOneStruct/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_optional_struct": {
            "name": "callOptionalStruct",
            "mqtt_topic": "testAble/{}/method/callOptionalStruct",
            "response_topic": "client/"+clientId+"/callOptionalStruct/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_three_structs": {
            "name": "callThreeStructs",
            "mqtt_topic": "testAble/{}/method/callThreeStructs",
            "response_topic": "client/"+clientId+"/callThreeStructs/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                },
            
                "input2": {
                    "type": "",
                    "value": null
                },
            
                "input3": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_one_date_time": {
            "name": "callOneDateTime",
            "mqtt_topic": "testAble/{}/method/callOneDateTime",
            "response_topic": "client/"+clientId+"/callOneDateTime/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_optional_date_time": {
            "name": "callOptionalDateTime",
            "mqtt_topic": "testAble/{}/method/callOptionalDateTime",
            "response_topic": "client/"+clientId+"/callOptionalDateTime/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_three_date_times": {
            "name": "callThreeDateTimes",
            "mqtt_topic": "testAble/{}/method/callThreeDateTimes",
            "response_topic": "client/"+clientId+"/callThreeDateTimes/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                },
            
                "input2": {
                    "type": "",
                    "value": null
                },
            
                "input3": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_one_duration": {
            "name": "callOneDuration",
            "mqtt_topic": "testAble/{}/method/callOneDuration",
            "response_topic": "client/"+clientId+"/callOneDuration/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_optional_duration": {
            "name": "callOptionalDuration",
            "mqtt_topic": "testAble/{}/method/callOptionalDuration",
            "response_topic": "client/"+clientId+"/callOptionalDuration/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_three_durations": {
            "name": "callThreeDurations",
            "mqtt_topic": "testAble/{}/method/callThreeDurations",
            "response_topic": "client/"+clientId+"/callThreeDurations/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                },
            
                "input2": {
                    "type": "",
                    "value": null
                },
            
                "input3": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_one_binary": {
            "name": "callOneBinary",
            "mqtt_topic": "testAble/{}/method/callOneBinary",
            "response_topic": "client/"+clientId+"/callOneBinary/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_optional_binary": {
            "name": "callOptionalBinary",
            "mqtt_topic": "testAble/{}/method/callOptionalBinary",
            "response_topic": "client/"+clientId+"/callOptionalBinary/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "call_three_binaries": {
            "name": "callThreeBinaries",
            "mqtt_topic": "testAble/{}/method/callThreeBinaries",
            "response_topic": "client/"+clientId+"/callThreeBinaries/response",
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                },
            
                "input2": {
                    "type": "",
                    "value": null
                },
            
                "input3": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        }
    };

    $scope.console = {
        showing: false,
        requests: []
    }

    $scope.showoutput = false;
    $scope.linuxoutput = '';

    const brokerUrl = 'ws://' + location.hostname + ':' + location.port + '/ws'

    const connectOptions = {
        keepAlive: 60,
        clientId: clientId,
        protocolId: 'MQTT',
        protocolVersion: 5,
        clean: true
    };

    var client = mqtt.connect(brokerUrl, connectOptions);

    client.on('close', function() {
        console.log("Connection Lost");
    });

    function publish(name, topic, payload, qos) {
        console.log(name + " Sending to " + topic);
        console.log(payload);
        let props = makeRequestProperties();
        $scope.console.requests.unshift({"name":name, "correlationData":props.correlationData, "topic": topic, "payload": payload, "response": null, "requestTime": Date.now()});
        client.publish(topic, payload, { "qos": qos, retain: false, properties: props});
        return props.correlationData;
    }

    client.on('message', function(topic, message, packet) {
        
        const subid = packet.properties.subscriptionIdentifier;

        console.log("Message Arrived: " + topic + " (" + subid + ")");
        console.log($scope.properties);

        var obj;
        if (message.toString().length == 0) {
            obj = null;
        } else {
            obj = JSON.parse(message.toString());
        }
        console.log(obj);

        for (const key in $scope.signals) {
            if (!$scope.signals.hasOwnProperty(key)) continue;
            const sig = $scope.signals[key];
            if (sig.subscription_id == subid) {
                sig.received = obj;
                sig.received_time = new Date();
            }
        }
        for (const key in $scope.properties) {
            if (!$scope.properties.hasOwnProperty(key)) continue;
            const prop = $scope.properties[key];
            if (prop.subscription_id == subid) {
                prop.received = obj;
                console.log("Set property received object to ", prop.received);
            }
        }
        for (const key in $scope.methods) {
            if (!$scope.methods.hasOwnProperty(key)) continue;
            const method = $scope.methods[key];
            if (responseSubscriptionId == subid) {
                if (packet.properties.correlationData && method.pending_correlation_id == packet.properties.correlationData) {
                    method.received = obj;
                    method.received_time = new Date();
                    for (let i=0; i<$scope.console.requests.length; i++) {
                        const req = $scope.console.requests[i];
                        if (req.correlationData == packet.properties.correlationData) {
                            req.response = obj;
                            req.responseTime = Date.now();
                        }
                    }
                }
            }
        }

        $scope.$apply();
    });

    client.on('connect', function() {
        $scope.online = true;

        var subscription_count = 10;
        console.log("Connected with ", client);

        var responseSubscriptionId = subscription_count++;
        const responseSubOpts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": responseSubscriptionId
            }
        };
        client.subscribe(responseTopic, responseSubOpts);
        console.log("Subscribing to response topic " + responseTopic + " with id " + responseSubscriptionId);
        
        
        const empty_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["empty"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/empty", empty_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/empty with id ", subscription_count);
        subscription_count++;
        
        const single_int_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleInt"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleInt", single_int_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleInt with id ", subscription_count);
        subscription_count++;
        
        const single_optional_int_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleOptionalInt"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleOptionalInt", single_optional_int_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleOptionalInt with id ", subscription_count);
        subscription_count++;
        
        const three_integers_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["threeIntegers"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/threeIntegers", three_integers_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/threeIntegers with id ", subscription_count);
        subscription_count++;
        
        const single_string_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleString"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleString", single_string_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleString with id ", subscription_count);
        subscription_count++;
        
        const single_optional_string_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleOptionalString"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleOptionalString", single_optional_string_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleOptionalString with id ", subscription_count);
        subscription_count++;
        
        const three_strings_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["threeStrings"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/threeStrings", three_strings_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/threeStrings with id ", subscription_count);
        subscription_count++;
        
        const single_enum_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleEnum"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleEnum", single_enum_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleEnum with id ", subscription_count);
        subscription_count++;
        
        const single_optional_enum_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleOptionalEnum"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleOptionalEnum", single_optional_enum_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleOptionalEnum with id ", subscription_count);
        subscription_count++;
        
        const three_enums_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["threeEnums"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/threeEnums", three_enums_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/threeEnums with id ", subscription_count);
        subscription_count++;
        
        const single_struct_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleStruct"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleStruct", single_struct_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleStruct with id ", subscription_count);
        subscription_count++;
        
        const single_optional_struct_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleOptionalStruct"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleOptionalStruct", single_optional_struct_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleOptionalStruct with id ", subscription_count);
        subscription_count++;
        
        const three_structs_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["threeStructs"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/threeStructs", three_structs_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/threeStructs with id ", subscription_count);
        subscription_count++;
        
        const single_date_time_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleDateTime"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleDateTime", single_date_time_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleDateTime with id ", subscription_count);
        subscription_count++;
        
        const single_optional_datetime_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleOptionalDatetime"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleOptionalDatetime", single_optional_datetime_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleOptionalDatetime with id ", subscription_count);
        subscription_count++;
        
        const three_date_times_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["threeDateTimes"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/threeDateTimes", three_date_times_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/threeDateTimes with id ", subscription_count);
        subscription_count++;
        
        const single_duration_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleDuration"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleDuration", single_duration_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleDuration with id ", subscription_count);
        subscription_count++;
        
        const single_optional_duration_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleOptionalDuration"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleOptionalDuration", single_optional_duration_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleOptionalDuration with id ", subscription_count);
        subscription_count++;
        
        const three_durations_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["threeDurations"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/threeDurations", three_durations_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/threeDurations with id ", subscription_count);
        subscription_count++;
        
        const single_binary_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleBinary"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleBinary", single_binary_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleBinary with id ", subscription_count);
        subscription_count++;
        
        const single_optional_binary_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["singleOptionalBinary"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/singleOptionalBinary", single_optional_binary_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/singleOptionalBinary with id ", subscription_count);
        subscription_count++;
        
        const three_binaries_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["threeBinaries"].subscription_id = subscription_count;
        client.subscribe("testAble/{}/signal/threeBinaries", three_binaries_sub_opts);
        console.log("Subscribing to signal testAble/{}/signal/threeBinaries with id ", subscription_count);
        subscription_count++;
        

        for (const key in $scope.properties) {
            if (!$scope.properties.hasOwnProperty(key)) continue;
            var sub_id = subscription_count++;
            const prop_sub_opts = {
                "qos": 1,
                "properties": {
                    "subscriptionIdentifier": sub_id
                }
            };
            $scope.properties[key].subscription_id = sub_id;
            client.subscribe($scope.properties[key].mqtt_topic, prop_sub_opts);
            console.log("Subscribing to property " + $scope.properties[key].mqtt_topic + " with id " + $scope.properties[key].subscription_id);
        }

        subscription_state = 1;
        $scope.$apply();
    });

    $scope.updateProperty = function(prop) {
        const payload = JSON.stringify(prop.received);
        publish("Property Update", prop.update_topic, payload, 1);
    };
 
    $scope.callMethod = function(method) {
        const payload = {};
        for (const key in method.args) {
            if (!method.args.hasOwnProperty(key)) continue;
            payload[key] = method.args[key].value;
        }
        const payload_str = JSON.stringify(payload);
        console.log("Method Call", method.mqtt_topic, payload_str, 1);
        method.pending_correlation_id = publish("Method Call", method.mqtt_topic, payload_str, 1);
    };
});