/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/


#pragma once

#include <functional>
#include <string>

#define BOOST_THREAD_PROVIDES_FUTURE
#include <boost/thread/future.hpp>
#include <boost/optional.hpp> // Include the Boost.Optional header

enum class MethodResultCode
{
    SUCCESS = 0,
    CLIENT_ERROR = 1,
    SERVER_ERROR = 2,
    TRANSPORT_ERROR = 3,
    PAYLOAD_ERROR = 4,
    TIMEOUT = 5,
    UNKNOWN_ERROR = 6,
    NOT_IMPLEMENTED = 7
};

class IBrokerConnection
{
public:
    /*! Publish to a topic.
     * Implementations should queue up messages when not connected.
     */
    virtual boost::future<bool> Publish(const std::string& topic, const std::string& payload, unsigned qos, bool retain, boost::optional<std::string> optCorrelationId, boost::optional<std::string> optResponseTopic, boost::optional<MethodResultCode> optResultCode) = 0;
    
    /*! Subscribe to a topic.
     * Implementation should queue up subscriptions when not connected.
     */
    virtual void Subscribe(const std::string& topic, int qos) = 0;

    /*! Provide a callback to be called on an incoming message.
     * Implementation should accept this at any time, even when not connected.
     */
    virtual void AddMessageCallback(const std::function<void(const std::string&, const std::string&, const boost::optional<std::string>, const boost::optional<std::string>, const boost::optional<MethodResultCode>)>& cb) = 0;

    /*! Utility for matching topics.
     * This probably should be a wrapper around `mosquitto_topic_matches_sub` or similar
     */
    virtual bool TopicMatchesSubscription(const std::string& topic, const std::string& subscr) const = 0;

    virtual std::string GetClientId() const = 0;
}; 