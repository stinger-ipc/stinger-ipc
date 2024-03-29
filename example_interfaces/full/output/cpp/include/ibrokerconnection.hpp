
#pragma once

#include <functional>
#include <string>

#define BOOST_THREAD_PROVIDES_FUTURE
#include <boost/thread/future.hpp>


class IBrokerConnection
{
public:
    /*! Publish to a topic.
     * Implementations should queue up messages when not connected.
     */
    virtual boost::future<bool> Publish(const std::string& topic, const std::string& payload, unsigned qos, bool retain) = 0;
    
    /*! Subscribe to a topic.
     * Implementation should queue up subscriptions when not connected.
     */
    virtual void Subscribe(const std::string& topic, int qos) = 0;

    /*! Provide a callback to be called on an incoming message.
     * Implementation should accept this at any time, even when not connected.
     */
    virtual void AddMessageCallback(const std::function<void(const std::string&, const std::string&)>& cb) = 0;

    /*! Utility for matching topics.
     * This probably should be a wrapper around `mosquitto_topic_matches_sub` or similar
     */
    virtual bool TopicMatchesSubscription(const std::string& topic, const std::string& subscr) const = 0;
}; 