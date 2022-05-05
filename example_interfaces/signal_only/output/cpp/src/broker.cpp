
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

MqttConnection::MqttConnection(const std::string& host, int port)
    : _mosq(NULL), _host(host), _port(port)
{
    boost::mutex::scoped_lock lock(_mutex);

    if (mosquitto_lib_init() != MOSQ_ERR_SUCCESS) {
        throw std::runtime_error("Mosquitto lib init problem");   
    };
    _mosq = mosquitto_new(NULL, true, (void*)this);

    mosquitto_connect_callback_set(_mosq, [](struct mosquitto *mosq, void *user, int i)
    {
        MqttConnection *thisClient = static_cast<MqttConnection*>(user);
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
            auto msg_promise = thisClient->_msgQueue.front();
            cout << "Sending message to " << msg_promise.first._topic << endl;
            int mid;
            mosquitto_publish(mosq, &mid, msg_promise.first._topic.c_str(), msg_promise.first._payload.size(), msg_promise.first._payload.c_str(), msg_promise.first._qos, msg_promise.first._retain);
            thisClient->_sendMessages.insert({mid, std::move(msg_promise.second))
            thisClient->_msgQueue.pop();
        }
    });

    mosquitto_message_callback_set(_mosq, [](struct mosquitto *mosq, void *user, const struct mosquitto_message *mmsg)
    {
        MqttConnection *thisClient = static_cast<MqttConnection*>(user);
        cout << "Fowarding message (" << mmsg->topic << ") to " << thisClient->_messageCallbacks.size() << " callbacks" << endl;
        std::string topic(mmsg->topic);
        std::string payload(static_cast<char*>(mmsg->payload), mmsg->payloadlen);
        for (auto& cb : thisClient->_messageCallbacks)
        {
            cb(topic, payload);
        }
    
    });

    mosquitto_publish_callback_set(_mosq, [](struct mosquitto *mosq, void *user, int mid)
    {
        MqttConnection *thisClient = static_cast<MqttConnection*>(user);
        auto found = thisClient->_sendMessages.find(mid);
        if (found != thisClient->_sendMessages.end())
        {
            found->second.set_value(true);
            thisClient->_sendMessages.erase(found);
        }
    });

    Connect();
    mosquitto_loop_start(_mosq);
}

MqttConnection::~MqttConnection()
{
    boost::mutex::scoped_lock lock(_mutex);
    mosquitto_loop_stop(_mosq, true);
    mosquitto_disconnect(_mosq);
    mosquitto_destroy(_mosq);
    mosquitto_lib_cleanup();

}

void MqttConnection::Connect()
{
    mosquitto_connect(_mosq, _host.c_str(), _port, 120);
}

boost::future<bool> MqttConnection::Publish(const std::string& topic, const std::string& payload, unsigned qos, bool retain)
{
    int mid;
    int rc = mosquitto_publish(_mosq, &mid, topic.c_str(), payload.size(), payload.c_str(), qos, retain);
    auto promise = boost::promise<bool>();
    auto future = promise.get_future();
    if (rc == MOSQ_ERR_NO_CONN)
    {
        MqttConnection::MqttMessage msg(topic, payload, qos, retain);
        boost::mutex::scoped_lock lock(_mutex);
        _msgQueue.push(std::make_pair<MqttConnection::MqttMessage, boost::future<bool>>(msg, std::move(future)));
    }
    else if (rc == MOSQ_ERR_SUCCESS)
    {
        boost::mutex::scoped_lock lock(_mutex);
        _sendMessages.insert({mid, std::move(promise)});
    }
    return future;
}

void MqttConnection::Subscribe(const std::string& topic, int qos)
{
    int rc = mosquitto_subscribe(_mosq, NULL, topic.c_str(), qos);
    if (rc == MOSQ_ERR_NO_CONN)
    {
        MqttConnection::MqttSubscription sub(topic, qos);
        boost::mutex::scoped_lock lock(_mutex);
        _subscriptions.push(sub);
    }
    else if (rc == MOSQ_ERR_SUCCESS)
    {
        //cout << "Subscribed to " << topic << endl;
    }
}

void MqttConnection::AddMessageCallback(const std::function<void(const std::string&, const std::string&)>& cb)
{
    boost::mutex::scoped_lock lock(_mutex);
    _messageCallbacks.push_back(cb);
    //cout << "Message callback set" << endl;
}

bool MqttConnection::TopicMatchesSubscription(const std::string& topic, const std::string& subscr) const
{
    bool result;
    int rc = mosquitto_topic_matches_sub(subscr.c_str(), topic.c_str(), &result);
    if (rc != MOSQ_ERR_SUCCESS)
    {
        throw std::runtime_error("Mosquitto error");
    }
    return result;

}


DefaultConnection::DefaultConnection(const std::string& host, int port)
    :  MqttConnection(host, port)
{

}

