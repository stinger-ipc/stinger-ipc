const clientId = "weather-web-" + new Date().getTime();

const signalSubIdStart = 1;
const propertySubIdStart = 11;

function makeRequestProperties() {
    const correlationData = Math.random().toString(16).substr(2, 8);
    return {
        "contentType": "application/json",
        "correlationData": correlationData,
        "responseTopic": responseTopic + correlationData
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
            "received": [],
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

    client.on('message', function(topic, message, packet) {
        console.log("Message Arrived: " + topic);

        const subid = packet.properties.subscriptionIdentifier;

        for (const key in $scope.signals) {
            if (!$scope.signals.hasOwnProperty(key)) continue;
            const sig = $scope.signals[key];
            if (sig.subscription_id == subid) {
                sig.received.push(obj);
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
        
        const _sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.signals[""].subscription_id = subscription_count;
        client.subscribe("weather/signal/currentTime", _sub_opts);
        console.log("Subscribing to weather/signal/currentTime with id ", subscription_count);
        subscription_count++;
        
        
        const location_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.properties["location"].subscription_id = subscription_count;
        client.subscribe("weather/property/location/value", location_sub_opts);
        console.log("Subscribing to weather/property/location/value with id ", subscription_count);
        subscription_count++;
        
        const current_temperature_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.properties["currentTemperature"].subscription_id = subscription_count;
        client.subscribe("weather/property/currentTemperature/value", current_temperature_sub_opts);
        console.log("Subscribing to weather/property/currentTemperature/value with id ", subscription_count);
        subscription_count++;
        
        const current_condition_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.properties["currentCondition"].subscription_id = subscription_count;
        client.subscribe("weather/property/currentCondition/value", current_condition_sub_opts);
        console.log("Subscribing to weather/property/currentCondition/value with id ", subscription_count);
        subscription_count++;
        
        const daily_forecast_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.properties["dailyForecast"].subscription_id = subscription_count;
        client.subscribe("weather/property/dailyForecast/value", daily_forecast_sub_opts);
        console.log("Subscribing to weather/property/dailyForecast/value with id ", subscription_count);
        subscription_count++;
        
        const hourly_forecast_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.properties["hourlyForecast"].subscription_id = subscription_count;
        client.subscribe("weather/property/hourlyForecast/value", hourly_forecast_sub_opts);
        console.log("Subscribing to weather/property/hourlyForecast/value with id ", subscription_count);
        subscription_count++;
        
        const current_condition_refresh_interval_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.properties["currentConditionRefreshInterval"].subscription_id = subscription_count;
        client.subscribe("weather/property/currentConditionRefreshInterval/value", current_condition_refresh_interval_sub_opts);
        console.log("Subscribing to weather/property/currentConditionRefreshInterval/value with id ", subscription_count);
        subscription_count++;
        
        const hourly_forecast_refresh_interval_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.properties["hourlyForecastRefreshInterval"].subscription_id = subscription_count;
        client.subscribe("weather/property/hourlyForecastRefreshInterval/value", hourly_forecast_refresh_interval_sub_opts);
        console.log("Subscribing to weather/property/hourlyForecastRefreshInterval/value with id ", subscription_count);
        subscription_count++;
        
        const daily_forecast_refresh_interval_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": subscription_count
            }
        };
        $scope.properties["dailyForecastRefreshInterval"].subscription_id = subscription_count;
        client.subscribe("weather/property/dailyForecastRefreshInterval/value", daily_forecast_refresh_interval_sub_opts);
        console.log("Subscribing to weather/property/dailyForecastRefreshInterval/value with id ", subscription_count);
        subscription_count++;
        
        subscription_state = 1;
        $scope.$apply();
    });

 
});