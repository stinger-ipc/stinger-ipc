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

enum class MethodReturnCode
{
    SUCCESS = 0,
    CLIENT_ERROR = 1,
    SERVER_ERROR = 2,
    TRANSPORT_ERROR = 3,
    PAYLOAD_ERROR = 4,
    CLIENT_SERIALIZATION_ERROR = 5,
    CLIENT_DESERIALIZATION_ERROR = 6,
    SERVER_SERIALIZATION_ERROR = 7,
    SERVER_DESERIALIZATION_ERROR = 8,
    METHOD_NOT_FOUND = 9,
    UNAUTHORIZED = 10,
    TIMEOUT = 11,
    OUT_OF_SYNC = 12,
    UNKNOWN_ERROR = 13,
    NOT_IMPLEMENTED = 14,
    SERVICE_UNAVAILABLE = 15
};

struct MqttProperties
{
    MqttProperties():
        correlationId(boost::none),
        responseTopic(boost::none),
        returnCode(boost::none),
        subscriptionId(boost::none),
        propertyVersion(boost::none),
        messageExpiryInterval(boost::none)
    {
    }

    boost::optional<std::string> correlationId;
    boost::optional<std::string> responseTopic;
    boost::optional<MethodReturnCode> returnCode;
    boost::optional<int> subscriptionId;
    boost::optional<int> propertyVersion;
    boost::optional<int> messageExpiryInterval;
};

typedef std::function<void(int, const char*)> LogFunctionType;
typedef int CallbackHandleType;

class IBrokerConnection
{
public:
    /*! Publish to a topic.
     * Implementations should queue up messages when not connected.
     */
    virtual boost::future<bool> Publish(const std::string& topic, const std::string& payload, unsigned qos, bool retain, const MqttProperties& mqttProps) = 0;

    /*! Subscribe to a topic.
     * Implementation should queue up subscriptions when not connected.
     */
    virtual int Subscribe(const std::string& topic, int qos) = 0;

    virtual void Unsubscribe(const std::string& topic) = 0;

    /*! Provide a callback to be called on an incoming message.
     * Implementation should accept this at any time, even when not connected.
     */
    virtual CallbackHandleType AddMessageCallback(const std::function<void(const std::string&, const std::string&, const MqttProperties&)>& cb) = 0;

    virtual void RemoveMessageCallback(CallbackHandleType handle) = 0;

    /*! Utility for matching topics.
     * This probably should be a wrapper around `mosquitto_topic_matches_sub` or similar
     */
    virtual bool TopicMatchesSubscription(const std::string& topic, const std::string& subscr) const = 0;

    virtual std::string GetClientId() const = 0;

    virtual std::string GetOnlineTopic() const = 0;

    virtual void SetLogFunction(const LogFunctionType& logFunc) = 0;

    virtual void SetLogLevel(int level) = 0;

    virtual void Log(int level, const char* fmt, ...) const = 0;
};