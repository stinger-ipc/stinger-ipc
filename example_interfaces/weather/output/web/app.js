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

        if (subid >= signalSubIdStart && subid < propertySubIdStart) {
            const signal_index = subid - signalSubIdStart;
            console.log("Signal index: " + signal_index);
            $scope.data.signals[signal_index] = JSON.parse(message.toString());
        } else if (subid >= propertySubIdStart && subid < propertySubIdStart + 8) {
            const prop_index = subid - propertySubIdStart;
            console.log("Property index: " + prop_index);
            $scope.data.properties[prop_index] = JSON.parse(message.toString());
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
        console.log("Connected with ", client);
        
        const _sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (signalSubIdStart + 1)
            }
        };
        client.subscribe("weather/signal/currentTime", _sub_opts);
        console.log("Subscribing to weather/signal/currentTime with id 1");
        
        
        const location_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (propertySubIdStart + 1)
            }
        };
        client.subscribe("weather/property/location/value", location_sub_opts);
        console.log("Subscribing to weather/property/location/value with id 2");
        
        const current_temperature_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (propertySubIdStart + 2)
            }
        };
        client.subscribe("weather/property/currentTemperature/value", current_temperature_sub_opts);
        console.log("Subscribing to weather/property/currentTemperature/value with id 3");
        
        const current_condition_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (propertySubIdStart + 3)
            }
        };
        client.subscribe("weather/property/currentCondition/value", current_condition_sub_opts);
        console.log("Subscribing to weather/property/currentCondition/value with id 4");
        
        const daily_forecast_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (propertySubIdStart + 4)
            }
        };
        client.subscribe("weather/property/dailyForecast/value", daily_forecast_sub_opts);
        console.log("Subscribing to weather/property/dailyForecast/value with id 5");
        
        const hourly_forecast_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (propertySubIdStart + 5)
            }
        };
        client.subscribe("weather/property/hourlyForecast/value", hourly_forecast_sub_opts);
        console.log("Subscribing to weather/property/hourlyForecast/value with id 6");
        
        const current_condition_refresh_interval_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (propertySubIdStart + 6)
            }
        };
        client.subscribe("weather/property/currentConditionRefreshInterval/value", current_condition_refresh_interval_sub_opts);
        console.log("Subscribing to weather/property/currentConditionRefreshInterval/value with id 7");
        
        const hourly_forecast_refresh_interval_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (propertySubIdStart + 7)
            }
        };
        client.subscribe("weather/property/hourlyForecastRefreshInterval/value", hourly_forecast_refresh_interval_sub_opts);
        console.log("Subscribing to weather/property/hourlyForecastRefreshInterval/value with id 8");
        
        const daily_forecast_refresh_interval_sub_opts = {
            "qos": 1,
            "properties": {
                "subscriptionIdentifier": (propertySubIdStart + 8)
            }
        };
        client.subscribe("weather/property/dailyForecastRefreshInterval/value", daily_forecast_refresh_interval_sub_opts);
        console.log("Subscribing to weather/property/dailyForecastRefreshInterval/value with id 9");
        
        subscription_state = 1;
        $scope.$apply();
    });

 
});