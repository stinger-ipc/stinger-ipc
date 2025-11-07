#[allow(unused_imports)]
use crate::payloads::*;
use derive_builder::Builder;

#[derive(Clone, Builder, Debug)]
pub struct WeatherInitialPropertyValues {
    pub location: LocationProperty,
    pub location_version: u32,

    pub current_temperature: f32,
    pub current_temperature_version: u32,

    pub current_condition: CurrentConditionProperty,
    pub current_condition_version: u32,

    pub daily_forecast: DailyForecastProperty,
    pub daily_forecast_version: u32,

    pub hourly_forecast: HourlyForecastProperty,
    pub hourly_forecast_version: u32,

    pub current_condition_refresh_interval: i32,
    pub current_condition_refresh_interval_version: u32,

    pub hourly_forecast_refresh_interval: i32,
    pub hourly_forecast_refresh_interval_version: u32,

    pub daily_forecast_refresh_interval: i32,
    pub daily_forecast_refresh_interval_version: u32,
}
