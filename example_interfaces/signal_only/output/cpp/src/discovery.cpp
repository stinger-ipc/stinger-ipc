#include "discovery.hpp"
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
#include <iostream>
#include <algorithm>
#include <sstream>
#include <boost/format.hpp>

SignalOnlyDiscovery::SignalOnlyDiscovery(std::shared_ptr<IBrokerConnection> broker)
    : _broker(broker)
{
    // Subscribe to the discovery topic
    std::stringstream topicStream;
    topicStream << boost::format("signalOnly/%1%/interface") % "+";
    _broker->Subscribe(topicStream.str(), 2);

    // Register message callback
    _brokerMessageCallbackHandle = _broker->AddMessageCallback([this](
                                                                       const std::string& topic,
                                                                       const std::string& payload,
                                                                       const MqttProperties& mqttProps
                                                               )
                                                               {
                                                                   _onMessage(topic, payload, mqttProps);
                                                               });
}

SignalOnlyDiscovery::~SignalOnlyDiscovery()
{
    if (_broker && _brokerMessageCallbackHandle != 0)
    {
        _broker->RemoveMessageCallback(_brokerMessageCallbackHandle);
        _brokerMessageCallbackHandle = 0;
    }
}

void SignalOnlyDiscovery::SetDiscoveryCallback(const std::function<void(const std::string&)>& cb)
{
    std::lock_guard<std::mutex> lock(_mutex);
    _discovery_callback = cb;
}

boost::future<std::string> SignalOnlyDiscovery::GetSingleton()
{
    std::lock_guard<std::mutex> lock(_mutex);

    // If we already have at least one instance, return it immediately
    if (!_instance_ids.empty())
    {
        boost::promise<std::string> promise;
        promise.set_value(_instance_ids[0]);
        return promise.get_future();
    }

    // Otherwise, create a promise that will be fulfilled when an instance is discovered
    _pending_promises.emplace_back();
    return _pending_promises.back().get_future();
}

std::vector<std::string> SignalOnlyDiscovery::GetInstanceIds() const
{
    std::lock_guard<std::mutex> lock(_mutex);
    return _instance_ids;
}

void SignalOnlyDiscovery::_onMessage(const std::string& topic, const std::string& payload, const MqttProperties& mqttProps)
{
    // Check if this message is for our discovery topic
    std::stringstream topicPattern;
    topicPattern << boost::format("signalOnly/%1%/interface") % "+";

    if (!_broker->TopicMatchesSubscription(topic, topicPattern.str()))
    {
        return;
    }

    // Parse the JSON payload
    rapidjson::Document document;
    document.Parse(payload.c_str());

    if (document.HasParseError())
    {
        std::cerr << "JSON parse error in Discovery: "
                  << rapidjson::GetParseError_En(document.GetParseError())
                  << " at offset " << document.GetErrorOffset() << std::endl;
        return;
    }

    // Extract the "instance" property
    if (!document.IsObject() || !document.HasMember("instance"))
    {
        std::cerr << "Discovery message missing 'instance' property" << std::endl;
        return;
    }

    const auto& instanceValue = document["instance"];
    if (!instanceValue.IsString())
    {
        std::cerr << "Discovery 'instance' property is not a string" << std::endl;
        return;
    }

    std::string instance_id = instanceValue.GetString();

    std::lock_guard<std::mutex> lock(_mutex);

    // Check if this instance is already known
    auto it = std::find(_instance_ids.begin(), _instance_ids.end(), instance_id);
    if (it != _instance_ids.end())
    {
        return; // Already known
    }

    // Add the new instance
    _instance_ids.push_back(instance_id);

    // Fulfill any pending promises
    for (auto& promise: _pending_promises)
    {
        promise.set_value(instance_id);
    }
    _pending_promises.clear();

    // Call the discovery callback if set
    if (_discovery_callback)
    {
        _discovery_callback(instance_id);
    }
}