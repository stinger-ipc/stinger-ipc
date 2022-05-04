
#include <exception>
#include <string>
#include <functional>
#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <mosquitto.h>
#include <iostream>

#include "broker.hpp"

using namespace std;


DefaultConnection::DefaultConnection(const std::string& host, int port)
    : _mosq(NULL), _host(host), _port(port)
{
    boost::mutex::scoped_lock lock(_mutex);

    if (mosquitto_lib_init() != MOSQ_ERR_SUCCESS) {
        throw std::runtime_error("Mosquitto lib init problem");   
    };
    _mosq = mosquitto_new(NULL, true, (void*)this);

    mosquitto_connect_callback_set(_mosq, [](struct mosquitto *mosq, void *user, int i)
    {
        DefaultConnection *thisClient = static_cast<DefaultConnection*>(user);
        cout << "Connected to " << thisClient->_host << endl;
        boost::mutex::scoped_lock lock(thisClient->_mutex);
        while(!thisClient->_subscriptions.empty())
        {
            auto sub = thisClient->_subscriptions.front();
            cout << "Subscribing to " << sub._topic << endl;
            mosquitto_subscribe(mosq, NULL, sub._topic.c_str(), sub._qos);
            thisClient->_subscriptions.pop();
        }
        while(!thisClient->_msgQueue.empty())
        {
            auto msg = thisClient->_msgQueue.front();
            cout << "Sending message to " << msg._topic << endl;
            mosquitto_publish(mosq, NULL, msg._topic.c_str(), msg._payload.size(), msg._payload.c_str(), msg._qos, msg._retain);
            thisClient->_msgQueue.pop();
        }
    });

    mosquitto_message_callback_set(_mosq, [](struct mosquitto *mosq, void *user, const struct mosquitto_message *mmsg)
    {
        DefaultConnection *thisClient = static_cast<DefaultConnection*>(user);
        cout << "Fowarding message (" << mmsg->topic << ") to " << thisClient->_messageCallbacks.size() << " callbacks" << endl;
        std::string topic(mmsg->topic);
        std::string payload(static_cast<char*>(mmsg->payload), mmsg->payloadlen);
        for (auto& cb : thisClient->_messageCallbacks)
        {
            cb(topic, payload);
        }
    
    });

    Connect();
    mosquitto_loop_start(_mosq);
}

DefaultConnection::~DefaultConnection()
{
    boost::mutex::scoped_lock lock(_mutex);
    mosquitto_loop_stop(_mosq, true);
    mosquitto_disconnect(_mosq);
    mosquitto_destroy(_mosq);
    mosquitto_lib_cleanup();

}

void DefaultConnection::Connect()
{
    mosquitto_connect(_mosq, _host.c_str(), _port, 120);
}

void DefaultConnection::Publish(const std::string& topic, const std::string& payload, unsigned qos, bool retain)
{
    int rc = mosquitto_publish(_mosq, NULL, topic.c_str(), payload.size(), payload.c_str(), qos, retain);
    if (rc == MOSQ_ERR_NO_CONN)
    {
        DefaultConnection::MqttMessage msg(topic, payload, qos, retain);
        boost::mutex::scoped_lock lock(_mutex);
        _msgQueue.push(msg);
    }
    else if (rc == MOSQ_ERR_SUCCESS)
    {
        //cout << "Published message to " << topic << endl;
    }
}

void DefaultConnection::Subscribe(const std::string& topic, int qos)
{
    int rc = mosquitto_subscribe(_mosq, NULL, topic.c_str(), qos);
    if (rc == MOSQ_ERR_NO_CONN)
    {
        DefaultConnection::MqttSubscription sub(topic, qos);
        boost::mutex::scoped_lock lock(_mutex);
        _subscriptions.push(sub);
    }
    else if (rc == MOSQ_ERR_SUCCESS)
    {
        //cout << "Subscribed to " << topic << endl;
    }
}

void DefaultConnection::AddMessageCallback(const std::function<void(const std::string&, const std::string&)>& cb)
{
    boost::mutex::scoped_lock lock(_mutex);
    _messageCallbacks.push_back(cb);
    //cout << "Message callback set" << endl;
}

bool DefaultConnection::TopicMatchesSubscription(const std::string& topic, const std::string& subscr) const
{
    bool result;
    int rc = mosquitto_topic_matches_sub(subscr.c_str(), topic.c_str(), &result);
    if (rc != MOSQ_ERR_SUCCESS)
    {
        throw std::runtime_error("Mosquitto error");
    }
    return result;

}

