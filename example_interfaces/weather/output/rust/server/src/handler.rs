use weather_types::payloads::MethodResultCode;

/// Method handlers for the WeatherServer server.
/// This trait must be implemented by the user of the server to handle incoming method requests.
pub trait WeatherMethodHandlers: Send + Sync {
    /// Pointer to a function to handle the refresh_daily_forecast method request.
    fn handle_refresh_daily_forecast(&self) -> Result<(), MethodResultCode>;

    /// Pointer to a function to handle the refresh_hourly_forecast method request.
    fn handle_refresh_hourly_forecast(&self) -> Result<(), MethodResultCode>;

    /// Pointer to a function to handle the refresh_current_conditions method request.
    fn handle_refresh_current_conditions(&self) -> Result<(), MethodResultCode>;

    fn as_any(&self) -> &dyn Any;
}
