
#include <exception>
#include <string>
#include <functional>
#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <mosquitto.h>
#include <mqtt_protocol.h>
#include <iostream>
#include <cstdarg>
#include <syslog.h>

#include "broker.hpp"

using namespace std;

MqttBrokerConnection::MqttBrokerConnection(const std::string &host, int port, const std::string &clientId)
    : _mosq(NULL)
    , _host(host)
    , _port(port)
    , _clientId(clientId)
    , _logLevel(LOG_NOTICE)
{
    boost::mutex::scoped_lock lock(_mutex);

    if (mosquitto_lib_init() != MOSQ_ERR_SUCCESS)
    {
        throw std::runtime_error("Mosquitto lib init problem");
    };
    _mosq = mosquitto_new(_clientId.c_str(), false, (void *)this);
    mosquitto_int_option(_mosq, MOSQ_OPT_PROTOCOL_VERSION, MQTT_PROTOCOL_V5);

    mosquitto_log_callback_set(_mosq, [](struct mosquitto *mosq, void *user, int level, const char *str)
                               {
                                   MqttBrokerConnection *thisClient = static_cast<MqttBrokerConnection *>(user);
                                   thisClient->Log(level, str);
                               });

    mosquitto_connect_v5_callback_set(_mosq, [](struct mosquitto *mosq, void *user, int rc, int flags, const mosquitto_property *props)
                                      {
                                          MqttBrokerConnection *thisClient = static_cast<MqttBrokerConnection *>(user);

                                          cout << "Connected to " << thisClient->_host << endl;

                                          const mosquitto_property *prop;
                                          for (prop = props; prop != NULL; prop = mosquitto_property_next(prop))
                                          {
                                              if (mosquitto_property_identifier(prop) == MQTT_PROP_REASON_STRING)
                                              {
                                                  char *reasonString = NULL;
                                                  if (mosquitto_property_read_string(prop, MQTT_PROP_REASON_STRING, &reasonString, false))
                                                  {
                                                      thisClient->Log(LOG_INFO, "Connect reason: %s", reasonString);
                                                      free(reasonString);
                                                  }
                                              }
                                          }

                                          boost::mutex::scoped_lock lock(thisClient->_mutex);
                                          while (!thisClient->_subscriptions.empty())
                                          {
                                              auto sub = thisClient->_subscriptions.front();
                                              thisClient->Log(LOG_INFO, "Delayed Subscribing to %s as %d", sub.topic.c_str(), sub.subscriptionId);
                                              mosquitto_property *propList = NULL;
                                              mosquitto_property_add_varint(&propList, MQTT_PROP_SUBSCRIPTION_IDENTIFIER, sub.subscriptionId);
                                              int rc = mosquitto_subscribe_v5(mosq, NULL, sub.topic.c_str(), sub.qos, MQTT_SUB_OPT_NO_LOCAL, propList);
                                              mosquitto_property_free_all(&propList);
                                              thisClient->_subscriptions.pop();
                                          }
                                          while (!thisClient->_msgQueue.empty())
                                          {
                                              MqttMessage &msg = thisClient->_msgQueue.front();
                                              thisClient->Log(LOG_INFO, "Publishing queued message to %s", msg._topic.c_str());
                                              int mid;
                                              mosquitto_property *propList = NULL;
                                              mosquitto_property_add_string(&propList, MQTT_PROP_CONTENT_TYPE, "application/json");
                                              if (msg._optCorrelationId)
                                              {
                                                  mosquitto_property_add_string(&propList, MQTT_PROP_CORRELATION_DATA, msg._optCorrelationId->c_str());
                                              }
                                              if (msg._optResponseTopic)
                                              {
                                                  mosquitto_property_add_string(&propList, MQTT_PROP_RESPONSE_TOPIC, msg._optResponseTopic->c_str());
                                              }
                                              mosquitto_publish_v5(mosq, &mid, msg._topic.c_str(), msg._payload.size(), msg._payload.c_str(), msg._qos, msg._retain, propList);
                                              mosquitto_property_free_all(&propList);
                                              thisClient->_sendMessages[mid] = msg._pSentPromise;
                                              thisClient->_msgQueue.pop();
                                          }

                                          { // Send online message
                                              auto onlineTopic = thisClient->GetOnlineTopic();
                                              int mid;
                                              mosquitto_property *propList = NULL;
                                              mosquitto_property_add_string(&propList, MQTT_PROP_CONTENT_TYPE, "application/json");
                                              const char *onlinePayload = "{\"status\":\"online\"}";
                                              mosquitto_publish_v5(mosq, &mid, onlineTopic.c_str(), sizeof(onlinePayload), onlinePayload, 1, true, propList);
                                              mosquitto_property_free_all(&propList);
                                          }
                                      });

    mosquitto_disconnect_v5_callback_set(_mosq, [](struct mosquitto *mosq, void *user, int rc, const mosquitto_property *props)
                                         {
                                             MqttBrokerConnection *thisClient = static_cast<MqttBrokerConnection *>(user);
                                             thisClient->Log(LOG_WARNING, "Disconnected from %s with reason code: %d", thisClient->_host.c_str(), rc);

                                             // Log any disconnect reason from MQTT v5 properties
                                             const mosquitto_property *prop;
                                             for (prop = props; prop != NULL; prop = mosquitto_property_next(prop))
                                             {
                                                 if (mosquitto_property_identifier(prop) == MQTT_PROP_REASON_STRING)
                                                 {
                                                     char *reasonString = NULL;
                                                     if (mosquitto_property_read_string(prop, MQTT_PROP_REASON_STRING, &reasonString, false))
                                                     {
                                                         thisClient->Log(LOG_WARNING, "Disconnect reason: %s", reasonString);
                                                         free(reasonString);
                                                     }
                                                 }
                                             }
                                         });

    mosquitto_message_v5_callback_set(_mosq, [](struct mosquitto *mosq, void *user, const struct mosquitto_message *mmsg, const mosquitto_property *props)
                                      {
                                          MqttBrokerConnection *thisClient = static_cast<MqttBrokerConnection *>(user);
                                          thisClient->Log(LOG_DEBUG, "Forwarding message (%s) to %zu callbacks", mmsg->topic, thisClient->_messageCallbacks.size());
                                          std::string topic(mmsg->topic);
                                          std::string payload(static_cast<char *>(mmsg->payload), mmsg->payloadlen);
                                          MqttProperties mqttProps;
                                          const mosquitto_property *prop;
                                          for (prop = props; prop != NULL; prop = mosquitto_property_next(prop))
                                          {
                                              if (mosquitto_property_identifier(prop) == MQTT_PROP_CORRELATION_DATA)
                                              {
                                                  void *correlation_data;
                                                  uint16_t correlation_data_len;
                                                  if (mosquitto_property_read_binary(prop, MQTT_PROP_CORRELATION_DATA, &correlation_data, &correlation_data_len, false))
                                                  {
                                                      mqttProps.correlationId = std::string(static_cast<char *>(correlation_data), correlation_data_len);
                                                      free(correlation_data);
                                                  }
                                              }
                                              else if (mosquitto_property_identifier(prop) == MQTT_PROP_RESPONSE_TOPIC)
                                              {
                                                  char *responseTopic = NULL;
                                                  if (mosquitto_property_read_string(prop, MQTT_PROP_RESPONSE_TOPIC, &responseTopic, false))
                                                  {
                                                      mqttProps.responseTopic = std::string(responseTopic);
                                                      free(responseTopic);
                                                  }
                                              }
                                              else if (mosquitto_property_identifier(prop) == MQTT_PROP_USER_PROPERTY)
                                              {
                                                  char *name = NULL;
                                                  char *value = NULL;
                                                  if (mosquitto_property_read_string_pair(prop, MQTT_PROP_USER_PROPERTY, &name, &value, false))
                                                  {
                                                      if (strcmp(name, "ReturnValue") == 0)
                                                      {
                                                          int returnValueInt = boost::lexical_cast<int>(value);
                                                          mqttProps.returnCode = static_cast<MethodReturnCode>(returnValueInt);
                                                      }
                                                      else if (strcmp(name, "PropertyVersion") == 0)
                                                      {
                                                          int propertyVersionInt = boost::lexical_cast<int>(value);
                                                          mqttProps.propertyVersion = propertyVersionInt;
                                                      }
                                                      free(name);
                                                      free(value);
                                                  }
                                              }
                                              else if (mosquitto_property_identifier(prop) == MQTT_PROP_SUBSCRIPTION_IDENTIFIER)
                                              {
                                                  uint32_t subscriptionId;
                                                  if (mosquitto_property_read_varint(prop, MQTT_PROP_SUBSCRIPTION_IDENTIFIER, &subscriptionId, false))
                                                  {
                                                      mqttProps.subscriptionId = static_cast<int>(subscriptionId);
                                                  }
                                              }
                                          }
                                          for (const auto &entry: thisClient->_messageCallbacks)
                                          {
                                              thisClient->Log(LOG_DEBUG, "Calling callback (handle=%d) for topic: %s", static_cast<int>(entry.first), topic.c_str());
                                              const auto &cb = entry.second;
                                              cb(topic, payload, mqttProps);
                                          }
                                      });

    mosquitto_publish_v5_callback_set(_mosq, [](struct mosquitto *mosq, void *user, int mid, int reason_code, const mosquitto_property *props)
                                      {
                                          MqttBrokerConnection *thisClient = static_cast<MqttBrokerConnection *>(user);
                                          auto found = thisClient->_sendMessages.find(mid);
                                          if (found != thisClient->_sendMessages.end())
                                          {
                                              found->second->set_value(true);
                                              thisClient->_sendMessages.erase(found);
                                          }
                                          thisClient->Log(LOG_DEBUG, "Publish completed for mid=%d, reason_code=%d", mid, reason_code);
                                      });

    Connect();
    mosquitto_loop_start(_mosq);
}

MqttBrokerConnection::~MqttBrokerConnection()
{
    boost::mutex::scoped_lock lock(_mutex);
    mosquitto_loop_stop(_mosq, true);
    mosquitto_disconnect(_mosq);
    mosquitto_destroy(_mosq);
    mosquitto_lib_cleanup();
}

void MqttBrokerConnection::Connect()
{
    auto onlineTopic = GetOnlineTopic();
    mosquitto_property *propList = NULL;
    mosquitto_property_add_string(&propList, MQTT_PROP_CONTENT_TYPE, "application/json");
    const char *offlinePayload = "{\"status\":\"offline\"}";
    int will_rc = mosquitto_will_set_v5(
            _mosq,
            onlineTopic.c_str(),
            sizeof(offlinePayload),
            offlinePayload,
            1, // qos
            true, // retain
            propList
    );

    // If will_set failed, free the properties we created. On success the
    // mosquitto library takes ownership of the property list, so do not free it.
    if (will_rc != MOSQ_ERR_SUCCESS)
    {
        Log(LOG_ERR, "Failed to set will message: %d", will_rc);
        if (propList)
        {
            mosquitto_property_free_all(&propList);
            propList = NULL;
        }
    }

    int rc = mosquitto_connect_bind_v5(_mosq, _host.c_str(), _port, 120, NULL, NULL);
    if (rc != MOSQ_ERR_SUCCESS)
    {
        Log(LOG_ERR, "Failed to connect to MQTT broker: %d", rc);
    }
}

boost::future<bool> MqttBrokerConnection::Publish(
        const std::string &topic,
        const std::string &payload,
        unsigned qos,
        bool retain,
        const MqttProperties &mqttProps
)
{
    int mid;
    mosquitto_property *propList = NULL;
    mosquitto_property_add_string(&propList, MQTT_PROP_CONTENT_TYPE, "application/json");
    if (mqttProps.correlationId)
    {
        mosquitto_property_add_binary(&propList, MQTT_PROP_CORRELATION_DATA, (void *)mqttProps.correlationId->c_str(), mqttProps.correlationId->size());
    }
    if (mqttProps.responseTopic)
    {
        mosquitto_property_add_string(&propList, MQTT_PROP_RESPONSE_TOPIC, mqttProps.responseTopic->c_str());
    }
    if (mqttProps.returnCode)
    {
        std::string returnCodeStr = std::to_string(static_cast<int>(*mqttProps.returnCode));
        mosquitto_property_add_string_pair(&propList, MQTT_PROP_USER_PROPERTY, "ReturnValue", returnCodeStr.c_str());
    }
    int rc = mosquitto_publish_v5(_mosq, &mid, topic.c_str(), payload.size(), payload.c_str(), qos, retain, propList);
    if (propList)
    {
        mosquitto_property_free_all(&propList);
    }
    if (rc == MOSQ_ERR_NO_CONN)
    {
        Log(LOG_DEBUG, "Delayed published queued to: %s", topic.c_str());
        MqttBrokerConnection::MqttMessage msg(topic, payload, qos, retain, mqttProps.correlationId, mqttProps.responseTopic);
        auto future = msg.getFuture();
        boost::mutex::scoped_lock lock(_mutex);
        _msgQueue.push(std::move(msg));
        return future;
    }
    else if (rc == MOSQ_ERR_SUCCESS)
    {
        Log(LOG_INFO, "Published to: %s | %s", topic.c_str(), payload.c_str());
        auto pPromise = std::make_shared<boost::promise<bool>>();
        auto future = pPromise->get_future();
        boost::mutex::scoped_lock lock(_mutex);
        _sendMessages[mid] = std::move(pPromise);
        return future;
    }
    else
    {
        Log(LOG_ERR, "Failed to publish to %s: rc=%d", topic.c_str(), rc);
    }
    throw std::runtime_error("Unhandled rc");
}

int MqttBrokerConnection::Subscribe(const std::string &topic, int qos)
{
    boost::mutex::scoped_lock lock(_mutex);

    // Check if we already have a subscription for this topic
    auto it = _subscriptionRefCounts.find(topic);
    if (it != _subscriptionRefCounts.end())
    {
        // Topic already subscribed - increment reference count
        it->second.first++;
        Log(LOG_DEBUG, "Incremented subscription count for %s to %d", topic.c_str(), it->second.first);
        return it->second.second; // Return existing subscription ID
    }

    // New subscription - create it
    int subscriptionId = _nextSubscriptionId++;
    mosquitto_property *propList = NULL;
    mosquitto_property_add_varint(&propList, MQTT_PROP_SUBSCRIPTION_IDENTIFIER, subscriptionId);
    int rc = mosquitto_subscribe_v5(_mosq, NULL, topic.c_str(), qos, MQTT_SUB_OPT_NO_LOCAL, propList);
    mosquitto_property_free_all(&propList);

    if (rc == MOSQ_ERR_NO_CONN)
    {
        Log(LOG_DEBUG, "Subscription %d queued for: %s", subscriptionId, topic.c_str());
        MqttBrokerConnection::MqttSubscription sub(topic, qos, subscriptionId);
        _subscriptions.push(sub);
        // Store ref count as 1 for queued subscription
        _subscriptionRefCounts[topic] = std::make_pair(1, subscriptionId);
    }
    else if (rc == MOSQ_ERR_SUCCESS)
    {
        Log(LOG_INFO, "Online Subscribed to %s as %d", topic.c_str(), subscriptionId);
        // Store ref count as 1 for active subscription
        _subscriptionRefCounts[topic] = std::make_pair(1, subscriptionId);
    }

    return subscriptionId;
}

void MqttBrokerConnection::Unsubscribe(const std::string &topic)
{
    boost::mutex::scoped_lock lock(_mutex);

    auto it = _subscriptionRefCounts.find(topic);
    if (it == _subscriptionRefCounts.end())
    {
        Log(LOG_WARNING, "Attempted to unsubscribe from topic %s that was never subscribed", topic.c_str());
        return;
    }

    // Decrement reference count
    it->second.first--;

    if (it->second.first > 0)
    {
        // Still have active references - just decrement
        Log(LOG_DEBUG, "Decremented subscription count for %s to %d", topic.c_str(), it->second.first);
        return;
    }

    // Reference count reached 0 - perform actual unsubscription
    Log(LOG_DEBUG, "Unsubscribing from %s (ref count reached 0)", topic.c_str());
    int rc = mosquitto_unsubscribe(_mosq, NULL, topic.c_str());

    if (rc != MOSQ_ERR_SUCCESS)
    {
        Log(LOG_WARNING, "Failed to unsubscribe from %s: rc=%d", topic.c_str(), rc);
    }

    // Remove from tracking map
    _subscriptionRefCounts.erase(it);
}

CallbackHandleType MqttBrokerConnection::AddMessageCallback(
        const std::function<void(
                const std::string &,
                const std::string &,
                const MqttProperties &
        )> &cb
)
{
    boost::mutex::scoped_lock lock(_mutex);
    CallbackHandleType handle = _nextCallbackHandle++;
    _messageCallbacks[handle] = cb;
    Log(LOG_DEBUG, "Message callback set with handle %d", handle);
    return handle;
}

void MqttBrokerConnection::RemoveMessageCallback(CallbackHandleType handle)
{
    if (handle > 0)
    {
        boost::mutex::scoped_lock lock(_mutex);
        auto found = _messageCallbacks.find(handle);
        if (found != _messageCallbacks.end())
        {
            _messageCallbacks.erase(found);
            Log(LOG_DEBUG, "Removed message callback with handle %d", handle);
        }
        else
        {
            Log(LOG_WARNING, "No message callback found with handle %d", handle);
        }
    }
}

bool MqttBrokerConnection::TopicMatchesSubscription(const std::string &topic, const std::string &subscr) const
{
    bool result;
    int rc = mosquitto_topic_matches_sub(subscr.c_str(), topic.c_str(), &result);
    if (rc != MOSQ_ERR_SUCCESS)
    {
        throw std::runtime_error("Mosquitto error");
    }
    return result;
}

std::string MqttBrokerConnection::GetClientId() const
{
    return _clientId;
}

std::string MqttBrokerConnection::GetOnlineTopic() const
{
    return boost::str(boost::format("client/%1%/online") % _clientId);
}

void MqttBrokerConnection::SetLogFunction(const LogFunctionType &logFunc)
{
    _logger = logFunc;
}

void MqttBrokerConnection::SetLogLevel(int level)
{
    _logLevel = level;
}

void MqttBrokerConnection::Log(int level, const char *fmt, ...) const
{
    if (_logger && (level <= _logLevel))
    {
        va_list args;
        va_start(args, fmt);
        char buf[256];
        vsnprintf(buf, sizeof(buf), fmt, args);
        std::string msg(buf);
        va_end(args);
        _logger(level, msg.c_str());
    }
}