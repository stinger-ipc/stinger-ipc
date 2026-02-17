const clientId = "testable-web-" + new Date().getTime();

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

function getInstanceIdFromHash() {
    // Return everything after the last '#' and strip an AngularJS hashbang ('!') if present.
    if (typeof location === 'undefined' || !location || !location.hash) return null;
    const hash = location.hash;
    // Find last '#' in case there are multiple hashes; include support for '#!' (hashbang)
    const lastHashIdx = hash.lastIndexOf('#');
    if (lastHashIdx === -1 || lastHashIdx === hash.length - 1) return null;
    let val = hash.substring(lastHashIdx + 1);
    // Strip leading '!' used by AngularJS hashbang URLs (#!)
    if (val.startsWith('!')) val = val.substring(1);
    if (!val) return null;
    // Convert '+' to space (common in URL-encoding) before decode
    const plusConverted = val.replace(/\+/g, ' ');
    try {
        return decodeURIComponent(plusConverted);
    } catch (e) {
        // If decode fails (malformed percent-encoding), return the raw plus-converted string
        return plusConverted;
    }
}

const instanceId = getInstanceIdFromHash();

// Replace '+' tokens in topics with the instance id (if present)
function resolveTopic(topic) {
    if (!instanceId) return topic;
    return topic.replace(/\+/g, instanceId);
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
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb0fb0>>"
        },
    
        "singleInt": {
            "subscription_id": null,
            "name": "singleInt",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcd9ef00>>"
        },
    
        "singleOptionalInt": {
            "subscription_id": null,
            "name": "singleOptionalInt",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb1dc0>>"
        },
    
        "threeIntegers": {
            "subscription_id": null,
            "name": "threeIntegers",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb2660>>"
        },
    
        "singleString": {
            "subscription_id": null,
            "name": "singleString",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb2e70>>"
        },
    
        "singleOptionalString": {
            "subscription_id": null,
            "name": "singleOptionalString",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb2f90>>"
        },
    
        "threeStrings": {
            "subscription_id": null,
            "name": "threeStrings",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3170>>"
        },
    
        "singleEnum": {
            "subscription_id": null,
            "name": "singleEnum",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3320>>"
        },
    
        "singleOptionalEnum": {
            "subscription_id": null,
            "name": "singleOptionalEnum",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb33e0>>"
        },
    
        "threeEnums": {
            "subscription_id": null,
            "name": "threeEnums",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb2ff0>>"
        },
    
        "singleStruct": {
            "subscription_id": null,
            "name": "singleStruct",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3920>>"
        },
    
        "singleOptionalStruct": {
            "subscription_id": null,
            "name": "singleOptionalStruct",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb36b0>>"
        },
    
        "threeStructs": {
            "subscription_id": null,
            "name": "threeStructs",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb39e0>>"
        },
    
        "singleDateTime": {
            "subscription_id": null,
            "name": "singleDateTime",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbdbe08c0>>"
        },
    
        "singleOptionalDatetime": {
            "subscription_id": null,
            "name": "singleOptionalDatetime",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3d70>>"
        },
    
        "threeDateTimes": {
            "subscription_id": null,
            "name": "threeDateTimes",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb34a0>>"
        },
    
        "singleDuration": {
            "subscription_id": null,
            "name": "singleDuration",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3680>>"
        },
    
        "singleOptionalDuration": {
            "subscription_id": null,
            "name": "singleOptionalDuration",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3ef0>>"
        },
    
        "threeDurations": {
            "subscription_id": null,
            "name": "threeDurations",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb35f0>>"
        },
    
        "singleBinary": {
            "subscription_id": null,
            "name": "singleBinary",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3350>>"
        },
    
        "singleOptionalBinary": {
            "subscription_id": null,
            "name": "singleOptionalBinary",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3cb0>>"
        },
    
        "threeBinaries": {
            "subscription_id": null,
            "name": "threeBinaries",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3bc0>>"
        },
    
        "singleArrayOfIntegers": {
            "subscription_id": null,
            "name": "singleArrayOfIntegers",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb8350>>"
        },
    
        "singleOptionalArrayOfStrings": {
            "subscription_id": null,
            "name": "singleOptionalArrayOfStrings",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb8710>>"
        },
    
        "arrayOfEveryType": {
            "subscription_id": null,
            "name": "arrayOfEveryType",
            "received": null,
            "received_time": null,
            "mqtt_topic": "<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb0cb0>>"
        }
    };

    $scope.properties = {
        "readWriteInteger": {
            "subscription_id": null,
            "name": "read_write_integer",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5aa80>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5aa80>>",
            "property_version": -1
        },
    
        "readOnlyInteger": {
            "subscription_id": null,
            "name": "read_only_integer",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5af60>>",
            "property_version": -1
        },
    
        "readWriteOptionalInteger": {
            "subscription_id": null,
            "name": "read_write_optional_integer",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5b0b0>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5b0b0>>",
            "property_version": -1
        },
    
        "readWriteTwoIntegers": {
            "subscription_id": null,
            "name": "read_write_two_integers",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5b0e0>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5b0e0>>",
            "property_version": -1
        },
    
        "readOnlyString": {
            "subscription_id": null,
            "name": "read_only_string",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5af30>>",
            "property_version": -1
        },
    
        "readWriteString": {
            "subscription_id": null,
            "name": "read_write_string",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5b470>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5b470>>",
            "property_version": -1
        },
    
        "readWriteOptionalString": {
            "subscription_id": null,
            "name": "read_write_optional_string",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5acc0>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5acc0>>",
            "property_version": -1
        },
    
        "readWriteTwoStrings": {
            "subscription_id": null,
            "name": "read_write_two_strings",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5b710>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5b710>>",
            "property_version": -1
        },
    
        "readWriteStruct": {
            "subscription_id": null,
            "name": "read_write_struct",
            "received": { 
                "value": { 
                    "the_bool": "",
                
                    "the_int": "",
                
                    "the_number": "",
                
                    "the_str": "",
                
                    "the_enum": "",
                
                    "an_entry_object": "",
                
                    "date_and_time": "",
                
                    "time_duration": "",
                
                    "data": "",
                
                    "OptionalInteger": "",
                
                    "OptionalString": "",
                
                    "OptionalEnum": "",
                
                    "optionalEntryObject": "",
                
                    "OptionalDateTime": "",
                
                    "OptionalDuration": "",
                
                    "OptionalBinary": "",
                
                    "array_of_integers": "",
                
                    "optional_array_of_integers": "",
                
                    "array_of_strings": "",
                
                    "optional_array_of_strings": "",
                
                    "array_of_enums": "",
                
                    "optional_array_of_enums": "",
                
                    "array_of_datetimes": "",
                
                    "optional_array_of_datetimes": "",
                
                    "array_of_durations": "",
                
                    "optional_array_of_durations": "",
                
                    "array_of_binaries": "",
                
                    "optional_array_of_binaries": "",
                
                    "array_of_entry_objects": "",
                
                    "optional_array_of_entry_objects": ""
                 }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5b650>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5b650>>",
            "property_version": -1
        },
    
        "readWriteOptionalStruct": {
            "subscription_id": null,
            "name": "read_write_optional_struct",
            "received": { 
                "value": { 
                    "the_bool": "",
                
                    "the_int": "",
                
                    "the_number": "",
                
                    "the_str": "",
                
                    "the_enum": "",
                
                    "an_entry_object": "",
                
                    "date_and_time": "",
                
                    "time_duration": "",
                
                    "data": "",
                
                    "OptionalInteger": "",
                
                    "OptionalString": "",
                
                    "OptionalEnum": "",
                
                    "optionalEntryObject": "",
                
                    "OptionalDateTime": "",
                
                    "OptionalDuration": "",
                
                    "OptionalBinary": "",
                
                    "array_of_integers": "",
                
                    "optional_array_of_integers": "",
                
                    "array_of_strings": "",
                
                    "optional_array_of_strings": "",
                
                    "array_of_enums": "",
                
                    "optional_array_of_enums": "",
                
                    "array_of_datetimes": "",
                
                    "optional_array_of_datetimes": "",
                
                    "array_of_durations": "",
                
                    "optional_array_of_durations": "",
                
                    "array_of_binaries": "",
                
                    "optional_array_of_binaries": "",
                
                    "array_of_entry_objects": "",
                
                    "optional_array_of_entry_objects": ""
                 }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5b770>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5b770>>",
            "property_version": -1
        },
    
        "readWriteTwoStructs": {
            "subscription_id": null,
            "name": "read_write_two_structs",
            "received": { 
                "first": { 
                    "the_bool": "",
                
                    "the_int": "",
                
                    "the_number": "",
                
                    "the_str": "",
                
                    "the_enum": "",
                
                    "an_entry_object": "",
                
                    "date_and_time": "",
                
                    "time_duration": "",
                
                    "data": "",
                
                    "OptionalInteger": "",
                
                    "OptionalString": "",
                
                    "OptionalEnum": "",
                
                    "optionalEntryObject": "",
                
                    "OptionalDateTime": "",
                
                    "OptionalDuration": "",
                
                    "OptionalBinary": "",
                
                    "array_of_integers": "",
                
                    "optional_array_of_integers": "",
                
                    "array_of_strings": "",
                
                    "optional_array_of_strings": "",
                
                    "array_of_enums": "",
                
                    "optional_array_of_enums": "",
                
                    "array_of_datetimes": "",
                
                    "optional_array_of_datetimes": "",
                
                    "array_of_durations": "",
                
                    "optional_array_of_durations": "",
                
                    "array_of_binaries": "",
                
                    "optional_array_of_binaries": "",
                
                    "array_of_entry_objects": "",
                
                    "optional_array_of_entry_objects": ""
                 },
            
                "second": { 
                    "the_bool": "",
                
                    "the_int": "",
                
                    "the_number": "",
                
                    "the_str": "",
                
                    "the_enum": "",
                
                    "an_entry_object": "",
                
                    "date_and_time": "",
                
                    "time_duration": "",
                
                    "data": "",
                
                    "OptionalInteger": "",
                
                    "OptionalString": "",
                
                    "OptionalEnum": "",
                
                    "optionalEntryObject": "",
                
                    "OptionalDateTime": "",
                
                    "OptionalDuration": "",
                
                    "OptionalBinary": "",
                
                    "array_of_integers": "",
                
                    "optional_array_of_integers": "",
                
                    "array_of_strings": "",
                
                    "optional_array_of_strings": "",
                
                    "array_of_enums": "",
                
                    "optional_array_of_enums": "",
                
                    "array_of_datetimes": "",
                
                    "optional_array_of_datetimes": "",
                
                    "array_of_durations": "",
                
                    "optional_array_of_durations": "",
                
                    "array_of_binaries": "",
                
                    "optional_array_of_binaries": "",
                
                    "array_of_entry_objects": "",
                
                    "optional_array_of_entry_objects": ""
                 }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5bd40>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5bd40>>",
            "property_version": -1
        },
    
        "readOnlyEnum": {
            "subscription_id": null,
            "name": "read_only_enum",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5aba0>>",
            "property_version": -1
        },
    
        "readWriteEnum": {
            "subscription_id": null,
            "name": "read_write_enum",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcbbba70>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcbbba70>>",
            "property_version": -1
        },
    
        "readWriteOptionalEnum": {
            "subscription_id": null,
            "name": "read_write_optional_enum",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbd696bd0>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbd696bd0>>",
            "property_version": -1
        },
    
        "readWriteTwoEnums": {
            "subscription_id": null,
            "name": "read_write_two_enums",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5ba10>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5ba10>>",
            "property_version": -1
        },
    
        "readWriteDatetime": {
            "subscription_id": null,
            "name": "read_write_datetime",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbd814500>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbd814500>>",
            "property_version": -1
        },
    
        "readWriteOptionalDatetime": {
            "subscription_id": null,
            "name": "read_write_optional_datetime",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5ba70>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5ba70>>",
            "property_version": -1
        },
    
        "readWriteTwoDatetimes": {
            "subscription_id": null,
            "name": "read_write_two_datetimes",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5a5d0>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5a5d0>>",
            "property_version": -1
        },
    
        "readWriteDuration": {
            "subscription_id": null,
            "name": "read_write_duration",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcb5baa0>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcb5baa0>>",
            "property_version": -1
        },
    
        "readWriteOptionalDuration": {
            "subscription_id": null,
            "name": "read_write_optional_duration",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcba4500>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcba4500>>",
            "property_version": -1
        },
    
        "readWriteTwoDurations": {
            "subscription_id": null,
            "name": "read_write_two_durations",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcba4470>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcba4470>>",
            "property_version": -1
        },
    
        "readWriteBinary": {
            "subscription_id": null,
            "name": "read_write_binary",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcba48f0>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcba48f0>>",
            "property_version": -1
        },
    
        "readWriteOptionalBinary": {
            "subscription_id": null,
            "name": "read_write_optional_binary",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcba4590>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcba4590>>",
            "property_version": -1
        },
    
        "readWriteTwoBinaries": {
            "subscription_id": null,
            "name": "read_write_two_binaries",
            "received": { 
                "first": {  },
            
                "second": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcba4b90>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcba4b90>>",
            "property_version": -1
        },
    
        "readWriteListOfStrings": {
            "subscription_id": null,
            "name": "read_write_list_of_strings",
            "received": { 
                "value": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcba4b60>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcba4b60>>",
            "property_version": -1
        },
    
        "readWriteLists": {
            "subscription_id": null,
            "name": "read_write_lists",
            "received": { 
                "the_list": {  },
            
                "optionalList": {  }
             },
            "mqtt_topic": "<bound method Property.value_topic of <stingeripc.components.Property object at 0x701bbcba4530>>",
            "update_topic": "<bound method Property.update_topic of <stingeripc.components.Property object at 0x701bbcba4530>>",
            "property_version": -1
        }
    };

    var interface_name = "testable";
    var client_id = clientId;
    // TODO: support all the topic params

    $scope.methods = {
        "callWithNothing": {
            "name": "callWithNothing",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
            "pending_correlation_id": null,
            "args": {},
            "received": null,
            "received_time": null
        },
        "callOneInteger": {
            "name": "callOneInteger",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOptionalInteger": {
            "name": "callOptionalInteger",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callThreeIntegers": {
            "name": "callThreeIntegers",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOneString": {
            "name": "callOneString",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOptionalString": {
            "name": "callOptionalString",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callThreeStrings": {
            "name": "callThreeStrings",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOneEnum": {
            "name": "callOneEnum",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOptionalEnum": {
            "name": "callOptionalEnum",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callThreeEnums": {
            "name": "callThreeEnums",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOneStruct": {
            "name": "callOneStruct",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOptionalStruct": {
            "name": "callOptionalStruct",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callThreeStructs": {
            "name": "callThreeStructs",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOneDateTime": {
            "name": "callOneDateTime",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOptionalDateTime": {
            "name": "callOptionalDateTime",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callThreeDateTimes": {
            "name": "callThreeDateTimes",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOneDuration": {
            "name": "callOneDuration",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOptionalDuration": {
            "name": "callOptionalDuration",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callThreeDurations": {
            "name": "callThreeDurations",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOneBinary": {
            "name": "callOneBinary",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOptionalBinary": {
            "name": "callOptionalBinary",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callThreeBinaries": {
            "name": "callThreeBinaries",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOneListOfIntegers": {
            "name": "callOneListOfIntegers",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callOptionalListOfFloats": {
            "name": "callOptionalListOfFloats",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
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
        "callTwoLists": {
            "name": "callTwoLists",
            "mqtt_topic": "",
            "response_topic": `client/${client_id}/testable/responses`,
            "pending_correlation_id": null,
            "args": {
                "input1": {
                    "type": "",
                    "value": null
                },
            
                "input2": {
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

    function publish_property_update(name, topic, payload, property_version) {
        console.log(name + " Sending to " + topic);
        console.log(payload);
        let props = {
            "contentType": "application/json",
            "userProperties": {
                "PropertyVersion": property_version.toString()
            }
        };
        $scope.console.requests.unshift({"name":name, "correlationData":null, "topic": topic, "payload": payload, "response": null, "requestTime": Date.now()});
        client.publish(topic, payload, { "qos": 1, retain: false, properties: props});
        return;
    }

    client.on('message', function(topic, message, packet) {
        
        const subid = packet.properties.subscriptionIdentifier;

        console.log("Message Arrived: " + topic + " (" + subid + ")");

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
                console.log("Set property '" + prop.name + "' received object to ", prop.received);
                prop.property_version = packet.properties.userProperties.PropertyVersion;
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
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb0fb0>>");
        client.subscribe(resolvedTopic, empty_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_int_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleInt"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcd9ef00>>");
        client.subscribe(resolvedTopic, single_int_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_optional_int_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleOptionalInt"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb1dc0>>");
        client.subscribe(resolvedTopic, single_optional_int_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const three_integers_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["threeIntegers"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb2660>>");
        client.subscribe(resolvedTopic, three_integers_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_string_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleString"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb2e70>>");
        client.subscribe(resolvedTopic, single_string_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_optional_string_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleOptionalString"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb2f90>>");
        client.subscribe(resolvedTopic, single_optional_string_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const three_strings_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["threeStrings"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3170>>");
        client.subscribe(resolvedTopic, three_strings_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_enum_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleEnum"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3320>>");
        client.subscribe(resolvedTopic, single_enum_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_optional_enum_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleOptionalEnum"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb33e0>>");
        client.subscribe(resolvedTopic, single_optional_enum_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const three_enums_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["threeEnums"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb2ff0>>");
        client.subscribe(resolvedTopic, three_enums_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_struct_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleStruct"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3920>>");
        client.subscribe(resolvedTopic, single_struct_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_optional_struct_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleOptionalStruct"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb36b0>>");
        client.subscribe(resolvedTopic, single_optional_struct_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const three_structs_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["threeStructs"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb39e0>>");
        client.subscribe(resolvedTopic, three_structs_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_date_time_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleDateTime"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbdbe08c0>>");
        client.subscribe(resolvedTopic, single_date_time_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_optional_datetime_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleOptionalDatetime"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3d70>>");
        client.subscribe(resolvedTopic, single_optional_datetime_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const three_date_times_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["threeDateTimes"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb34a0>>");
        client.subscribe(resolvedTopic, three_date_times_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_duration_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleDuration"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3680>>");
        client.subscribe(resolvedTopic, single_duration_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_optional_duration_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleOptionalDuration"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3ef0>>");
        client.subscribe(resolvedTopic, single_optional_duration_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const three_durations_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["threeDurations"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb35f0>>");
        client.subscribe(resolvedTopic, three_durations_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_binary_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleBinary"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3350>>");
        client.subscribe(resolvedTopic, single_binary_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_optional_binary_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleOptionalBinary"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3cb0>>");
        client.subscribe(resolvedTopic, single_optional_binary_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const three_binaries_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["threeBinaries"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb3bc0>>");
        client.subscribe(resolvedTopic, three_binaries_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_array_of_integers_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleArrayOfIntegers"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb8350>>");
        client.subscribe(resolvedTopic, single_array_of_integers_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const single_optional_array_of_strings_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["singleOptionalArrayOfStrings"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb8710>>");
        client.subscribe(resolvedTopic, single_optional_array_of_strings_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
        subscription_count++;
        
        const array_of_every_type_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["arrayOfEveryType"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("<bound method Signal.topic of <stingeripc.components.Signal object at 0x701bbcbb0cb0>>");
        client.subscribe(resolvedTopic, array_of_every_type_sub_opts);
        console.log("Subscribing to signal " + resolvedTopic + " with id ", subscription_count);
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
            var resolvedTopic = resolveTopic($scope.properties[key].mqtt_topic);
            client.subscribe(resolvedTopic, prop_sub_opts);
            console.log("Subscribing to property " + resolvedTopic + " with id " + $scope.properties[key].subscription_id);
        }

        subscription_state = 1;
        $scope.$apply();
    });

    $scope.updateProperty = function(prop) {
        const payload = JSON.stringify(prop.received);
        publish_property_update("Property Update", prop.update_topic, payload, 1);
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