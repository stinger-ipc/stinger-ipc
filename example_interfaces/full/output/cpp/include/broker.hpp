/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions.
You may use, modify, and distribute it under any license of your choosing.
*/

#pragma once

#include <mosquitto.h>
#include <queue>
#include <string>
#include <map>
#include <utility>
#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/core/noncopyable.hpp>

#define BOOST_THREAD_PROVIDES_FUTURE
#include <boost/thread/future.hpp>

#include "ibrokerconnection.hpp"

/*! This class presents a connection to a MQTT broker.
 */
class MqttBrokerConnection: public IBrokerConnection
{
public:
    /*! Constructor for a MqttBrokerConnection.
     * \param hostname IP address or hostname of the MQTT broker server.
     * \param port Port where the MQTT broker is running (often 1883).
     */
    MqttBrokerConnection(const std::string& host, int port, const std::string& clientId);

    virtual ~MqttBrokerConnection();

    /*! Publish a message to the MQTT broker.
     * \param topic the topic of the message.
     * \param payload is the payload body of the message.
     * \param qos the MQTT quality of service value between 0 and 2 inclusive.
     * \param retain an indicator that the MQTT broker should retain the message.
     * \param optCorrelationId Optional correlation ID string that will be used to associate responses to requests.
     * \param optResponseTopic Optional MQTT topic used for publishing responses to requests.
     * \param optReturnValue Optional (predetermined) value for the result of a method call.
     * \return A future which is resolved to true when the message has been published to the MQTT broker.
     */
    virtual boost::future<bool> Publish(
            const std::string& topic,
            const std::string& payload,
            unsigned qos,
            bool retain,
            const MqttProperties& properties
    );

    /*! Subscribe to a topic.
     * \param topic the subscription topic.
     * \param qos an MQTT quality of service value between 0 and 2 inclusive.
     * \return the MQTT subscription ID.
     */
    virtual int Subscribe(const std::string& topic, int qos);

    virtual void Unsubscribe(const std::string& topic);

    /*! Add a function that is called on the receipt of a message.
     * Many callbacks can be added, and each will be called in the order in which the callbacks were added.
     * \param cb the callback function.
     */
    virtual CallbackHandleType AddMessageCallback(const std::function<void(const std::string&, const std::string&, const MqttProperties&)>& cb);

    virtual void RemoveMessageCallback(CallbackHandleType handle);

    /*! Determines if a topic string matches a subscription topic.
     * \param topic a topic to match against a subscription.
     * \param subscr the subscription topic string to match against.
     * \return true if it is a match.
     */
    virtual bool TopicMatchesSubscription(const std::string& topic, const std::string& subscr) const;

    virtual std::string GetClientId() const;

    virtual std::string GetOnlineTopic() const;

    virtual void SetLogFunction(const LogFunctionType& logFunc);
    virtual void SetLogLevel(int level);
    virtual void Log(int level, const char* fmt, ...) const;

protected:
    /*! Establishes the connection to the broker.
     */
    virtual void Connect();

private:
    class MqttMessage: private boost::noncopyable
    {
    public:
        MqttMessage(const std::string& topic, const std::string& payload, int qos, bool retain, boost::optional<std::string> optCorrelationId, boost::optional<std::string> optResponseTopic, boost::optional<int> optMessageExpiryInterval):
            _topic(topic), _payload(payload), _qos(qos), _retain(retain), _optCorrelationId(optCorrelationId), _optResponseTopic(optResponseTopic), _optMessageExpiryInterval(optMessageExpiryInterval) { }

        MqttMessage(const MqttMessage& other):
            _topic(other._topic), _payload(other._payload), _qos(other._qos), _retain(other._retain), _pSentPromise(other._pSentPromise), _optCorrelationId(other._optCorrelationId), _optResponseTopic(other._optResponseTopic), _optMessageExpiryInterval(other._optMessageExpiryInterval) { }

        virtual ~MqttMessage() = default;

        boost::future<bool> getFuture() { return _pSentPromise->get_future(); };

        std::string _topic;
        std::string _payload;
        int _qos;
        bool _retain;
        std::shared_ptr<boost::promise<bool>> _pSentPromise;
        boost::optional<std::string> _optCorrelationId;
        boost::optional<std::string> _optResponseTopic;
        boost::optional<int> _optMessageExpiryInterval;
    };

    struct MqttSubscription
    {
        MqttSubscription(const std::string& topic, int qos, int subscriptionId):
            topic(topic), qos(qos), subscriptionId(subscriptionId) { }

        ~MqttSubscription() = default;
        std::string topic;
        int qos;
        int subscriptionId;
    };

    mosquitto* _mosq;
    std::string _host;
    int _port;
    std::string _clientId;
    int _nextSubscriptionId = 1;
    std::queue<MqttSubscription> _subscriptions;
    boost::mutex _mutex;
    CallbackHandleType _nextCallbackHandle = 1;
    std::map<CallbackHandleType, std::function<void(const std::string&, const std::string&, const MqttProperties&)>> _messageCallbacks;
    std::queue<MqttMessage> _msgQueue;
    std::map<int, std::shared_ptr<boost::promise<bool>>> _sendMessages;

    // Track subscription reference counts: topic -> (count, subscriptionId)
    std::map<std::string, std::pair<int, int>> _subscriptionRefCounts;

    LogFunctionType _logger;
    int _logLevel = 0;
};