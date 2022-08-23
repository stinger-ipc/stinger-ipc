/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
*/

use futures::StreamExt;
use connection::Connection;

pub struct ExampleServer {
    connection: Connection,
}

impl ExampleServer {
    pub fn new(connection: Connection) -> ExampleServer {

        ExampleServer{
            connection: connection,
        }
    }

    pub fn emit_today_is(&mut self, day_of_month: i32, day_of_week: connection::enums::DayOfTheWeek) {

    }
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {

            }
        }
    }
}