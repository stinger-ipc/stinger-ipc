const clientId = "Full-web-" + new Date().getTime();

const signalSubIdStart = 1;
const propertySubIdStart = 11;

function makeRequestProperties(response_topic) {
    const correlationData = Math.random().toString(16).substr(2, 8);
    return {
        "contentType": "application/json",
        "correlationData": correlationData,
        "responseTopic": response_topic
    }
}

var app = angular.module("myApp", []);

app.controller("myCtrl", function ($scope, $filter, $location) {

    console.log("Running app");

    var subscription_state = 0;

    $scope.timePattern = new RegExp("^[0-2][0-9]:[0-5][0-9]$");
    $scope.online = false;
    $scope.signals = {
        "todayIs": {
            "subscription_id": null,
            "name": "todayIs",
            "received": null,
            "received_time": null,
            "mqtt_topic": "full/signal/todayIs"
        }
    };

    $scope.properties = {
        "favoriteNumber": {
            "subscription_id": null,
            "name": "favorite_number",
            "received": null,
            "mqtt_topic": "full/property/favoriteNumber/value"
        },
    
        "favoriteFoods": {
            "subscription_id": null,
            "name": "favorite_foods",
            "received": null,
            "mqtt_topic": "full/property/favoriteFoods/value"
        },
    
        "lunchMenu": {
            "subscription_id": null,
            "name": "lunch_menu",
            "received": null,
            "mqtt_topic": "full/property/lunchMenu/value"
        }
    };

    $scope.methods = {
        "addNumbers": {
            "subscription_id": null,
            "name": "addNumbers",
            "mqtt_topic": "full/method/addNumbers",
            "response_topic": "client/"+clientId+"/full/method/addNumbers/response",
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
            "subscription_id": null,
            "name": "doSomething",
            "mqtt_topic": "full/method/doSomething",
            "response_topic": "client/"+clientId+"/full/method/doSomething/response",
            "pending_correlation_id": null,
            "args": {
                "aString": {
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
        props 
        $scope.console.requests.unshift({"name":name, "correlationData":props.correlationData, "topic": topic, "payload": payload, "response": null, "requestTime": Date.now()});
        client.publish(topic, payload, { "qos": qos, retain: false, properties: props});
        return props.correlationData;
    }
    
    $scope.addNumbersMethodCall = function(form) {
        var prop = $scope.methods["addNumbers"];
        const publish_properties = makeRequestProperties(prop.response_topic);
        prop.pending_correlation_id = publish_properties.correlationData;
        
    };
    
    $scope.doSomethingMethodCall = function(form) {
        var prop = $scope.methods["doSomething"];
        const publish_properties = makeRequestProperties(prop.response_topic);
        prop.pending_correlation_id = publish_properties.correlationData;
        
    };
    
    client.on('message', function(topic, message, packet) {
        console.log("Message Arrived: " + topic);

        const subid = packet.properties.subscriptionIdentifier;

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
            }
        }

        var obj;
        if (message.toString().length == 0) {
            obj = null;
        } else {
            obj = JSON.parse(message.toString());
        }
        console.log(obj);

        $scope.$apply();
    });

    client.on('connect', function() {
        var subscription_count = 10;
        console.log("Connected with ", client);
        
        const today_is_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["todayIs"].subscription_id = subscription_count;
        client.subscribe("full/signal/todayIs", today_is_sub_opts);
        console.log("Subscribing to full/signal/todayIs with id ", subscription_count);
        subscription_count++;
        

        for (const key in $scope.properties) {
            if (!$scope.properties.hasOwnProperty(key)) continue;
            const prop = $scope.properties[key];
            var sub_id = subscription_count++;
            const prop_sub_opts = {
                "qos": 1,
                "properties": {
                    "subscriptionIdentifier": sub_id
                }
            };
            prop.subscription_id = sub_id;
            client.subscribe(prop.mqtt_topic, prop_sub_opts);
            console.log("Subscribing to " + prop.mqtt_topic + " with id ", sub_id);
        }

        subscription_state = 1;
        $scope.$apply();
    });

 
});