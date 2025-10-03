const clientId = "SignalOnly-web-" + new Date().getTime();

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

    $scope.enums = {};

    $scope.signals = {
        "another_signal": {
            "subscription_id": null,
            "name": "anotherSignal",
            "received": null,
            "received_time": null,
            "mqtt_topic": "signalOnly/signal/anotherSignal"
        },
    
        "bark": {
            "subscription_id": null,
            "name": "bark",
            "received": null,
            "received_time": null,
            "mqtt_topic": "signalOnly/signal/bark"
        },
    
        "maybe_number": {
            "subscription_id": null,
            "name": "maybe_number",
            "received": null,
            "received_time": null,
            "mqtt_topic": "signalOnly/signal/maybeNumber"
        },
    
        "maybe_name": {
            "subscription_id": null,
            "name": "maybe_name",
            "received": null,
            "received_time": null,
            "mqtt_topic": "signalOnly/signal/maybeName"
        },
    
        "now": {
            "subscription_id": null,
            "name": "now",
            "received": null,
            "received_time": null,
            "mqtt_topic": "signalOnly/signal/now"
        }
    };

    $scope.properties = {};

    $scope.methods = {
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
        
        
        const another_signal_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["anotherSignal"].subscription_id = subscription_count;
        client.subscribe("signalOnly/signal/anotherSignal", another_signal_sub_opts);
        console.log("Subscribing to signal signalOnly/signal/anotherSignal with id ", subscription_count);
        subscription_count++;
        
        const bark_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["bark"].subscription_id = subscription_count;
        client.subscribe("signalOnly/signal/bark", bark_sub_opts);
        console.log("Subscribing to signal signalOnly/signal/bark with id ", subscription_count);
        subscription_count++;
        
        const maybe_number_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["maybeNumber"].subscription_id = subscription_count;
        client.subscribe("signalOnly/signal/maybeNumber", maybe_number_sub_opts);
        console.log("Subscribing to signal signalOnly/signal/maybeNumber with id ", subscription_count);
        subscription_count++;
        
        const maybe_name_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["maybeName"].subscription_id = subscription_count;
        client.subscribe("signalOnly/signal/maybeName", maybe_name_sub_opts);
        console.log("Subscribing to signal signalOnly/signal/maybeName with id ", subscription_count);
        subscription_count++;
        
        const now_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["now"].subscription_id = subscription_count;
        client.subscribe("signalOnly/signal/now", now_sub_opts);
        console.log("Subscribing to signal signalOnly/signal/now with id ", subscription_count);
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