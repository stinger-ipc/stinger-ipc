const clientId = "weather-web-" + new Date().getTime();

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
        // <stingeripc.components.InterfaceEnum object at 0x7c0a4f4f6450>
        "weather_condition": [
            {"name": "rainy", "id": 1 },
            
            {"name": "sunny", "id": 2 },
            
            {"name": "partly_cloudy", "id": 3 },
            
            {"name": "mostly_cloudy", "id": 4 },
            
            {"name": "overcast", "id": 5 },
            
            {"name": "windy", "id": 6 },
            
            {"name": "snowy", "id": 7 }
            ]
    };

    $scope.signals = {
        "current_time": {
            "subscription_id": null,
            "name": "current_time",
            "received": null,
            "received_time": null,
            "mqtt_topic": "weather/signal/currentTime"
        }
    };

    $scope.properties = {
        "location": {
            "subscription_id": null,
            "name": "location",
            "received": { 
                "latitude": {  },
            
                "longitude": {  }
             },
            "mqtt_topic": "weather/property/location/value",
            "update_topic": "weather/property/location/setValue"
        },
    
        "current_temperature": {
            "subscription_id": null,
            "name": "current_temperature",
            "received": { 
                "temperature_f": {  }
             },
            "mqtt_topic": "weather/property/currentTemperature/value"
        },
    
        "current_condition": {
            "subscription_id": null,
            "name": "current_condition",
            "received": { 
                "condition": {  },
            
                "description": {  }
             },
            "mqtt_topic": "weather/property/currentCondition/value"
        },
    
        "daily_forecast": {
            "subscription_id": null,
            "name": "daily_forecast",
            "received": { 
                "monday": { 
                    "high_temperature": "",
                
                    "low_temperature": "",
                
                    "condition": "",
                
                    "start_time": "",
                
                    "end_time": ""
                 },
            
                "tuesday": { 
                    "high_temperature": "",
                
                    "low_temperature": "",
                
                    "condition": "",
                
                    "start_time": "",
                
                    "end_time": ""
                 },
            
                "wednesday": { 
                    "high_temperature": "",
                
                    "low_temperature": "",
                
                    "condition": "",
                
                    "start_time": "",
                
                    "end_time": ""
                 }
             },
            "mqtt_topic": "weather/property/dailyForecast/value"
        },
    
        "hourly_forecast": {
            "subscription_id": null,
            "name": "hourly_forecast",
            "received": { 
                "hour_0": { 
                    "temperature": "",
                
                    "starttime": "",
                
                    "condition": ""
                 },
            
                "hour_1": { 
                    "temperature": "",
                
                    "starttime": "",
                
                    "condition": ""
                 },
            
                "hour_2": { 
                    "temperature": "",
                
                    "starttime": "",
                
                    "condition": ""
                 },
            
                "hour_3": { 
                    "temperature": "",
                
                    "starttime": "",
                
                    "condition": ""
                 }
             },
            "mqtt_topic": "weather/property/hourlyForecast/value"
        },
    
        "current_condition_refresh_interval": {
            "subscription_id": null,
            "name": "current_condition_refresh_interval",
            "received": { 
                "seconds": {  }
             },
            "mqtt_topic": "weather/property/currentConditionRefreshInterval/value",
            "update_topic": "weather/property/currentConditionRefreshInterval/setValue"
        },
    
        "hourly_forecast_refresh_interval": {
            "subscription_id": null,
            "name": "hourly_forecast_refresh_interval",
            "received": { 
                "seconds": {  }
             },
            "mqtt_topic": "weather/property/hourlyForecastRefreshInterval/value",
            "update_topic": "weather/property/hourlyForecastRefreshInterval/setValue"
        },
    
        "daily_forecast_refresh_interval": {
            "subscription_id": null,
            "name": "daily_forecast_refresh_interval",
            "received": { 
                "seconds": {  }
             },
            "mqtt_topic": "weather/property/dailyForecastRefreshInterval/value",
            "update_topic": "weather/property/dailyForecastRefreshInterval/setValue"
        }
    };

    $scope.methods = {
        "refresh_daily_forecast": {
            "name": "refresh_daily_forecast",
            "mqtt_topic": "weather/method/refreshDailyForecast",
            "response_topic": "client/"+clientId+"/weather/method/refreshDailyForecast/response",
            "pending_correlation_id": null,
            "args": {},
            "received": null,
            "received_time": null
        },
        "refresh_hourly_forecast": {
            "name": "refresh_hourly_forecast",
            "mqtt_topic": "weather/method/refreshHourlyForecast",
            "response_topic": "client/"+clientId+"/weather/method/refreshHourlyForecast/response",
            "pending_correlation_id": null,
            "args": {},
            "received": null,
            "received_time": null
        },
        "refresh_current_conditions": {
            "name": "refresh_current_conditions",
            "mqtt_topic": "weather/method/refreshCurrentConditions",
            "response_topic": "client/"+clientId+"/weather/method/refreshCurrentConditions/response",
            "pending_correlation_id": null,
            "args": {},
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
        
        
        const current_time_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["currentTime"].subscription_id = subscription_count;
        client.subscribe("weather/signal/currentTime", current_time_sub_opts);
        console.log("Subscribing to signal weather/signal/currentTime with id ", subscription_count);
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