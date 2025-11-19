const clientId = "Full-web-" + new Date().getTime();

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
        "dayOfTheWeek": [
            {"name": "Sunday", "id": 1 },
            
            {"name": "Monday", "id": 2 },
            
            {"name": "Tuesday", "id": 3 },
            
            {"name": "Wednesday", "id": 4 },
            
            {"name": "Thursday", "id": 5 },
            
            {"name": "Friday", "id": 6 },
            
            {"name": "Saturday", "id": 7 }
            ]
    };

    $scope.signals = {
        "todayIs": {
            "subscription_id": null,
            "name": "todayIs",
            "received": null,
            "received_time": null,
            "mqtt_topic": "full/+/signal/todayIs"
        }
    };

    $scope.properties = {
        "favoriteNumber": {
            "subscription_id": null,
            "name": "favorite_number",
            "received": { 
                "number": {  }
             },
            "mqtt_topic": "full/+/property/favoriteNumber/value",
            "update_topic": "full/+/property/favoriteNumber/setValue",
            "property_version": -1
        },
    
        "favoriteFoods": {
            "subscription_id": null,
            "name": "favorite_foods",
            "received": { 
                "drink": {  },
            
                "slices_of_pizza": {  },
            
                "breakfast": {  }
             },
            "mqtt_topic": "full/+/property/favoriteFoods/value",
            "update_topic": "full/+/property/favoriteFoods/setValue",
            "property_version": -1
        },
    
        "lunchMenu": {
            "subscription_id": null,
            "name": "lunch_menu",
            "received": { 
                "monday": { 
                    "drink": "",
                
                    "sandwich": "",
                
                    "crackers": "",
                
                    "day": "",
                
                    "order_number": "",
                
                    "time_of_lunch": "",
                
                    "duration_of_lunch": ""
                 },
            
                "tuesday": { 
                    "drink": "",
                
                    "sandwich": "",
                
                    "crackers": "",
                
                    "day": "",
                
                    "order_number": "",
                
                    "time_of_lunch": "",
                
                    "duration_of_lunch": ""
                 }
             },
            "mqtt_topic": "full/+/property/lunchMenu/value",
            "update_topic": "full/+/property/lunchMenu/setValue",
            "property_version": -1
        },
    
        "familyName": {
            "subscription_id": null,
            "name": "family_name",
            "received": { 
                "family_name": {  }
             },
            "mqtt_topic": "full/+/property/familyName/value",
            "update_topic": "full/+/property/familyName/setValue",
            "property_version": -1
        },
    
        "lastBreakfastTime": {
            "subscription_id": null,
            "name": "last_breakfast_time",
            "received": { 
                "timestamp": {  }
             },
            "mqtt_topic": "full/+/property/lastBreakfastTime/value",
            "update_topic": "full/+/property/lastBreakfastTime/setValue",
            "property_version": -1
        },
    
        "breakfastLength": {
            "subscription_id": null,
            "name": "breakfast_length",
            "received": { 
                "length": {  }
             },
            "mqtt_topic": "full/+/property/breakfastLength/value",
            "update_topic": "full/+/property/breakfastLength/setValue",
            "property_version": -1
        },
    
        "lastBirthdays": {
            "subscription_id": null,
            "name": "last_birthdays",
            "received": { 
                "mom": {  },
            
                "dad": {  },
            
                "sister": {  },
            
                "brothers_age": {  }
             },
            "mqtt_topic": "full/+/property/lastBirthdays/value",
            "update_topic": "full/+/property/lastBirthdays/setValue",
            "property_version": -1
        }
    };

    $scope.methods = {
        "addNumbers": {
            "name": "addNumbers",
            "mqtt_topic": "full/+/method/addNumbers",
            "response_topic": "client/"+clientId+"/addNumbers/methodResponse",
            "pending_correlation_id": null,
            "args": {
                "first": {
                    "type": "ArgPrimitiveType.INTEGER",
                    "value": null
                },
            
                "second": {
                    "type": "ArgPrimitiveType.INTEGER",
                    "value": null
                },
            
                "third": {
                    "type": "ArgPrimitiveType.INTEGER",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "doSomething": {
            "name": "doSomething",
            "mqtt_topic": "full/+/method/doSomething",
            "response_topic": "client/"+clientId+"/doSomething/methodResponse",
            "pending_correlation_id": null,
            "args": {
                "aString": {
                    "type": "ArgPrimitiveType.STRING",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "echo": {
            "name": "echo",
            "mqtt_topic": "full/+/method/echo",
            "response_topic": "client/"+clientId+"/echo/methodResponse",
            "pending_correlation_id": null,
            "args": {
                "message": {
                    "type": "ArgPrimitiveType.STRING",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "whatTimeIsIt": {
            "name": "what_time_is_it",
            "mqtt_topic": "full/+/method/whatTimeIsIt",
            "response_topic": "client/"+clientId+"/whatTimeIsIt/methodResponse",
            "pending_correlation_id": null,
            "args": {
                "the_first_time": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "setTheTime": {
            "name": "set_the_time",
            "mqtt_topic": "full/+/method/setTheTime",
            "response_topic": "client/"+clientId+"/setTheTime/methodResponse",
            "pending_correlation_id": null,
            "args": {
                "the_first_time": {
                    "type": "",
                    "value": null
                },
            
                "the_second_time": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "forwardTime": {
            "name": "forward_time",
            "mqtt_topic": "full/+/method/forwardTime",
            "response_topic": "client/"+clientId+"/forwardTime/methodResponse",
            "pending_correlation_id": null,
            "args": {
                "adjustment": {
                    "type": "",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "howOffIsTheClock": {
            "name": "how_off_is_the_clock",
            "mqtt_topic": "full/+/method/howOffIsTheClock",
            "response_topic": "client/"+clientId+"/howOffIsTheClock/methodResponse",
            "pending_correlation_id": null,
            "args": {
                "actual_time": {
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
        
        
        const today_is_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };

        $scope.signals["todayIs"].subscription_id = subscription_count;
        var resolvedTopic = resolveTopic("full/+/signal/todayIs");
        client.subscribe(resolvedTopic, today_is_sub_opts);
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