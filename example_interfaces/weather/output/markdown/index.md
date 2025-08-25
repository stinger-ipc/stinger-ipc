# _weather_ API Overview 





## Signals

Signals are messages from the server to clients.

```plantuml
@startuml
Client <<- Server : Signal(Parameters)
@enduml
```

### Signal `current_time`

Once in a while (at intervals decided by the provider) the current date
and time will be published.  (Mostly for example purposes).


#### Signal Parameters for `current_time`

| Name          | Type     |Description|
|---------------|----------|-----------|
|  current_time |  string  ||

#### Code Examples

<details>
  <summary>Python Client</summary>

```python
@client.receive_current_time
def on_current_time(current_time: str):
    print(f"Got a 'current_time' signal: current_time={ current_time } ")
```

</details>

<details>
  <summary>Rust Server</summary>

```rust
server.emit_current_time("apples".to_string()).await;
```

</details>


## Methods

Methods are requests from a client to a server and the server provides a response back to the client:

```plantuml
@startuml
Client ->> Server : Request(Parameters)
Client <<-- Server: Response(Parameters)
@enduml
```


### Method `refresh_daily_forecast`

When called, this method will force the retrieval of the daily weather forecast from
the NWS weather API.  

When called, the `daily_forecast` API property will be republished with the latest data.

This method has no arguments and provides no return values.


#### Request Parameters

There are no arguments for this request.

#### Return Parameters

There is no return value for this method call.

### Method `refresh_hourly_forecast`

When called, this method will force the retrieval of the hourly weather forecast from
the NWS weather API.  

When called, the `hourly_forecast` API property will be republished with the latest data.

This method has no arguments and provides no return values.


#### Request Parameters

There are no arguments for this request.

#### Return Parameters

There is no return value for this method call.

### Method `refresh_current_conditions`

When called, this method will force the retrieval of the latest weather conditions
from the nearest weather station.  It also forces a re-calculation of the current
temperature.

When called, the `current_temperature` and `current_condition` API properties are
republished with the latest value.

This method has no arguments and provides no return values.


#### Request Parameters

There are no arguments for this request.

#### Return Parameters

There is no return value for this method call.

## Properties

Properties are values (or a set of values) held by the server.   They are re-published when the value changes. 

```plantuml
@startuml
Server -> Server : Set Property
Client <<- Server: Property Updated
@enduml
```

### Property `location`

Weather will be retrieved for the provided location.


| Name          | Type     |Description|
|---------------|----------|-----------|
|    latitude   |  number  ||
|   longitude   |  number  ||

### Property `current_temperature`

This is the current (estimated) temperature in degrees fahrenheit.  This values
is regularly updated.  The value is extrapolated from the hourly forecast, but
adjusted based on the latest conditions at the nearest weather station.


This property is **read-only**.  It can only be modified by the server.

| Name          | Type     |Description|
|---------------|----------|-----------|
| temperature_f |  number  ||

### Property `current_condition`

This is the current weather outside.  This comes from the hourly forecast and is
updated about once per hour.


This property is **read-only**.  It can only be modified by the server.

| Name          | Type     |Description|
|---------------|----------|-----------|
|   condition   |[Enum WeatherCondition](#enum-WeatherCondition)||
|  description  |  string  ||

### Property `daily_forecast`

This contains the weather forecast for each day of the next few days.  It is updated
a couple of times a day.  The current day may not have the high or low temperature
provided.  This is an example which shows only a few days.  The actual implementation
will have a value for each day of the week.


This property is **read-only**.  It can only be modified by the server.

| Name          | Type     |Description|
|---------------|----------|-----------|
|     monday    |[Struct ForecastForDay](#enum-ForecastForDay)|This is the forecast for Monday.|
|    tuesday    |[Struct ForecastForDay](#enum-ForecastForDay)||
|   wednesday   |[Struct ForecastForDay](#enum-ForecastForDay)||

### Property `hourly_forecast`

This contains the weather forecast for each hour of the next 24 hours.  The data source
us updated a couple of times per day, but this API property is updated every hour on the
hour.


This property is **read-only**.  It can only be modified by the server.

| Name          | Type     |Description|
|---------------|----------|-----------|
|     hour_0    |[Struct ForecastForHour](#enum-ForecastForHour)|This is the forecast for the current hour.|
|     hour_1    |[Struct ForecastForHour](#enum-ForecastForHour)|This is the forecast for the next hour.|
|     hour_2    |[Struct ForecastForHour](#enum-ForecastForHour)||
|     hour_3    |[Struct ForecastForHour](#enum-ForecastForHour)||

### Property `current_condition_refresh_interval`

This is the maximum interval, in seconds, that the latest weather conditions at the nearest weather
station are retrieved.


| Name          | Type     |Description|
|---------------|----------|-----------|
|    seconds    | integer  ||

### Property `hourly_forecast_refresh_interval`

This is the maximum interval, in seconds, that the hourly forecast data is retrieved.


| Name          | Type     |Description|
|---------------|----------|-----------|
|    seconds    | integer  |Interval duration in seconds.|

### Property `daily_forecast_refresh_interval`

This is the maximum interval, in seconds, that the daily forecast data is retrieved.


| Name          | Type     |Description|
|---------------|----------|-----------|
|    seconds    | integer  ||


## Enums

### Enum `WeatherCondition`

<a name="Enum-WeatherCondition"></a>_No description exists for this enumeration._

* rainy (1)
* sunny (2)
* partly_cloudy (3)
* mostly_cloudy (4)
* overcast (5)
* windy (6)
* snowy (7)


## Structures

Structures are a group of values and may be used as an argument in signals, methods, or properties.  Defining a structure allows for easy reuse.

### Struct `ForecastForHour`

<a name="Struct-ForecastForHour"></a>This structure contains the forecast for a single hour.


| Name          | Type     |Description|
|---------------|----------|-----------|
|  temperature  |  number  |Forecasted temperature in degrees fahrenheit.|
|   starttime   |  string  |Forecast is valid for the hour starting at this time.|
|   condition   |[Enum WeatherCondition](#enum-WeatherCondition)||

### Struct `ForecastForDay`

<a name="Struct-ForecastForDay"></a>This structure contains the forecast for a single day.  The high or low temperature
may be missing for the current day.


| Name          | Type     |Description|
|---------------|----------|-----------|
|high_temperature|  number  |High temperature for the day in degrees fahrenheit.|
|low_temperature|  number  |Low temperature for the day in degrees fahrenheit.|
|   condition   |[Enum WeatherCondition](#enum-WeatherCondition)||
|   start_time  |  string  ||
|    end_time   |  string  ||
