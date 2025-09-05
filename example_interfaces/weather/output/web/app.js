const clientId = "weather-web-" + new Date().getTime();

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
        "currentTime": {
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
            "received": null,
            "mqtt_topic": "weather/property/location/value"
        },
    
        "currentTemperature": {
            "subscription_id": null,
            "name": "current_temperature",
            "received": null,
            "mqtt_topic": "weather/property/currentTemperature/value"
        },
    
        "currentCondition": {
            "subscription_id": null,
            "name": "current_condition",
            "received": null,
            "mqtt_topic": "weather/property/currentCondition/value"
        },
    
        "dailyForecast": {
            "subscription_id": null,
            "name": "daily_forecast",
            "received": null,
            "mqtt_topic": "weather/property/dailyForecast/value"
        },
    
        "hourlyForecast": {
            "subscription_id": null,
            "name": "hourly_forecast",
            "received": null,
            "mqtt_topic": "weather/property/hourlyForecast/value"
        },
    
        "currentConditionRefreshInterval": {
            "subscription_id": null,
            "name": "current_condition_refresh_interval",
            "received": null,
            "mqtt_topic": "weather/property/currentConditionRefreshInterval/value"
        },
    
        "hourlyForecastRefreshInterval": {
            "subscription_id": null,
            "name": "hourly_forecast_refresh_interval",
            "received": null,
            "mqtt_topic": "weather/property/hourlyForecastRefreshInterval/value"
        },
    
        "dailyForecastRefreshInterval": {
            "subscription_id": null,
            "name": "daily_forecast_refresh_interval",
            "received": null,
            "mqtt_topic": "weather/property/dailyForecastRefreshInterval/value"
        }
    };

    $scope.methods = {
        "refreshDailyForecast": {
            "subscription_id": null,
            "name": "refresh_daily_forecast",
            "mqtt_topic": "weather/method/refreshDailyForecast",
            "response_topic": "client/"+clientId+"/weather/method/refreshDailyForecast/response",
            "pending_correlation_id": null,
            "args": {},
            "received": null,
            "received_time": null
        },
        "refreshHourlyForecast": {
            "subscription_id": null,
            "name": "refresh_hourly_forecast",
            "mqtt_topic": "weather/method/refreshHourlyForecast",
            "response_topic": "client/"+clientId+"/weather/method/refreshHourlyForecast/response",
            "pending_correlation_id": null,
            "args": {},
            "received": null,
            "received_time": null
        },
        "refreshCurrentConditions": {
            "subscription_id": null,
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
        props 
        $scope.console.requests.unshift({"name":name, "correlationData":props.correlationData, "topic": topic, "payload": payload, "response": null, "requestTime": Date.now()});
        client.publish(topic, payload, { "qos": qos, retain: false, properties: props});
        return props.correlationData;
    }
    
    $scope.refreshDailyForecastMethodCall = function(form) {
        var prop = $scope.methods["refreshDailyForecast"];
        const publish_properties = makeRequestProperties(prop.response_topic);
        prop.pending_correlation_id = publish_properties.correlationData;
        
    };
    
    $scope.refreshHourlyForecastMethodCall = function(form) {
        var prop = $scope.methods["refreshHourlyForecast"];
        const publish_properties = makeRequestProperties(prop.response_topic);
        prop.pending_correlation_id = publish_properties.correlationData;
        
    };
    
    $scope.refreshCurrentConditionsMethodCall = function(form) {
        var prop = $scope.methods["refreshCurrentConditions"];
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
        
        const current_time_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals["currentTime"].subscription_id = subscription_count;
        client.subscribe("weather/signal/currentTime", current_time_sub_opts);
        console.log("Subscribing to weather/signal/currentTime with id ", subscription_count);
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