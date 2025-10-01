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

var app = angular.module("myApp", []);

app.controller("myCtrl", function ($scope, $filter, $location) {

    console.log("Running app");

    var subscription_state = 0;

    $scope.timePattern = new RegExp("^[0-2][0-9]:[0-5][0-9]$");
    $scope.online = false;

    $scope.enums = {
        "day_of_the_week": [
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
        "today_is": {
            "subscription_id": null,
            "name": "todayIs",
            "received": null,
            "received_time": null,
            "mqtt_topic": "full/{}/signal/todayIs"
        }
    };

    $scope.properties = {
        "favorite_number": {
            "subscription_id": null,
            "name": "favorite_number",
            "received": { 
                "number": {  }
             },
            "mqtt_topic": "full/{}/property/favoriteNumber/value",
            "update_topic": "full/{}/property/favoriteNumber/setValue"
        },
    
        "favorite_foods": {
            "subscription_id": null,
            "name": "favorite_foods",
            "received": { 
                "drink": {  },
            
                "slices_of_pizza": {  },
            
                "breakfast": {  }
             },
            "mqtt_topic": "full/{}/property/favoriteFoods/value",
            "update_topic": "full/{}/property/favoriteFoods/setValue"
        },
    
        "lunch_menu": {
            "subscription_id": null,
            "name": "lunch_menu",
            "received": { 
                "monday": { 
                    "drink": "",
                
                    "sandwich": "",
                
                    "crackers": "",
                
                    "day": "",
                
                    "order_number": ""
                 },
            
                "tuesday": { 
                    "drink": "",
                
                    "sandwich": "",
                
                    "crackers": "",
                
                    "day": "",
                
                    "order_number": ""
                 }
             },
            "mqtt_topic": "full/{}/property/lunchMenu/value",
            "update_topic": "full/{}/property/lunchMenu/setValue"
        },
    
        "family_name": {
            "subscription_id": null,
            "name": "family_name",
            "received": { 
                "family_name": {  }
             },
            "mqtt_topic": "full/{}/property/familyName/value",
            "update_topic": "full/{}/property/familyName/setValue"
        }
    };

    $scope.methods = {
        "add_numbers": {
            "name": "addNumbers",
            "mqtt_topic": "full/{}/method/addNumbers",
            "response_topic": "client/"+clientId+"/full/{}/method/addNumbers/response",
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
        "do_something": {
            "name": "doSomething",
            "mqtt_topic": "full/{}/method/doSomething",
            "response_topic": "client/"+clientId+"/full/{}/method/doSomething/response",
            "pending_correlation_id": null,
            "args": {
                "a_string": {
                    "type": "ArgPrimitiveType.STRING",
                    "value": null
                }
            },
            "received": null,
            "received_time": null
        },
        "echo": {
            "name": "echo",
            "mqtt_topic": "full/{}/method/echo",
            "response_topic": "client/"+clientId+"/full/{}/method/echo/response",
            "pending_correlation_id": null,
            "args": {
                "message": {
                    "type": "ArgPrimitiveType.STRING",
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
        
        
        const today_is_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["todayIs"].subscription_id = subscription_count;
        client.subscribe("full/{}/signal/todayIs", today_is_sub_opts);
        console.log("Subscribing to signal full/{}/signal/todayIs with id ", subscription_count);
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