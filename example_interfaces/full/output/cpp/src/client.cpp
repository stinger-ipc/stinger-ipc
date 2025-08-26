
#include <vector>
#include <iostream>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>

#include "client.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"


constexpr const char FullClient::NAME[];
constexpr const char FullClient::INTERFACE_VERSION[];

FullClient::FullClient(std::shared_ptr<IBrokerConnection> broker) : _broker(broker)
{
    _broker->AddMessageCallback([this](const std::string& topic, const std::string& payload, const boost::optional<std::string> optCorrelationId, const boost::optional<std::string> unusedRespTopic, const boost::optional<MethodResultCode> optResultCode)
    {
        _receiveMessage(topic, payload, optCorrelationId, optResultCode);
    });
    _broker->Subscribe("full/signal/todayIs", 1);
    
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/full/method/addNumbers/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/full/method/doSomething/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
}

void FullClient::_receiveMessage(
        const std::string& topic, 
        const std::string& payload, 
        const boost::optional<std::string> optCorrelationId, 
        const boost::optional<MethodResultCode> optResultCode)
{
    if (_broker->TopicMatchesSubscription(topic, "full/signal/todayIs"))
    {
        //Log("Handling todayIs signal");
        rapidjson::Document doc;
        try {
            if (_todayIsCallback)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse todayIs signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                
                int tempdayOfMonth;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dayOfMonth");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        
                        tempdayOfMonth = itr->value.GetInt();
                        
                    } else {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    
                    }
                }
                
                boost::optional<DayOfTheWeek> tempdayOfWeek;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dayOfWeek");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        
                        tempdayOfWeek = static_cast<DayOfTheWeek>(itr->value.GetInt());
                        
                    } else {
                        tempdayOfWeek = boost::none;
                    
                    }
                }
                

                _todayIsCallback(tempdayOfMonth, tempdayOfWeek);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely. 
            // TODO: Log this failure
        }
    }
    if (_broker->TopicMatchesSubscription(topic, "client/+/full/method/addNumbers/response") && optCorrelationId)
    {
        std::cout << "Matched topic for addNumbers response" << std::endl;
        _handleAddNumbersResponse(topic, payload, *optCorrelationId);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/full/method/doSomething/response") && optCorrelationId)
    {
        std::cout << "Matched topic for doSomething response" << std::endl;
        _handleDoSomethingResponse(topic, payload, *optCorrelationId);
    }
}
void FullClient::registerTodayIsCallback(const std::function<void(int, boost::optional<DayOfTheWeek>)>& cb)
{
    _todayIsCallback = cb;
}


boost::future<int> FullClient::addNumbers(int first, int second, boost::optional<int> third)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingAddNumbersMethodCalls[correlationId] = boost::promise<int>();

    rapidjson::Document doc;
    doc.SetObject();
    
    
    doc.AddMember("first",first, doc.GetAllocator());
    
    
    
    doc.AddMember("second",second, doc.GetAllocator());
    
    
    if (third) 
    doc.AddMember("third",*third, doc.GetAllocator());
    
    
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/full/method/addNumbers/response") % _broker->GetClientId();
    _broker->Publish("full/method/addNumbers", buf.GetString(), 2, false, correlationIdStr, responseTopicStringStream.str(), MethodResultCode::SUCCESS);

    return _pendingAddNumbersMethodCalls[correlationId].get_future();
}

void FullClient::_handleAddNumbersResponse(
        const std::string& topic, 
        const std::string& payload, 
        const std::string &correlationId) 
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse addNumbers signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingAddNumbersMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingAddNumbersMethodCalls.end())
    {
        
        // Response has a single value.
        rapidjson::Value::ConstMemberIterator sumItr = doc.FindMember("sum");
        int sum = sumItr->value.GetInt();
        
        promiseItr->second.set_value(sum);
    }

    std::cout << "End of response handler for " << topic << std::endl;
}

boost::future<DoSomethingReturnValue> FullClient::doSomething(const std::string& aString)
{
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingDoSomethingMethodCalls[correlationId] = boost::promise<DoSomethingReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();
    
    
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(aString.c_str(), aString.size(), doc.GetAllocator());
        doc.AddMember("aString", tempStringValue, doc.GetAllocator());
    }
    
    
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    std::stringstream responseTopicStringStream;
    responseTopicStringStream << boost::format("client/%1%/full/method/doSomething/response") % _broker->GetClientId();
    _broker->Publish("full/method/doSomething", buf.GetString(), 2, false, correlationIdStr, responseTopicStringStream.str(), MethodResultCode::SUCCESS);

    return _pendingDoSomethingMethodCalls[correlationId].get_future();
}

void FullClient::_handleDoSomethingResponse(
        const std::string& topic, 
        const std::string& payload, 
        const std::string &correlationId) 
{
    std::cout << "In response handler for " << topic << " with correlationId=" << correlationId << std::endl;
    rapidjson::Document doc;
    rapidjson::ParseResult ok = doc.Parse(payload.c_str());
    if (!ok)
    {
        //Log("Could not JSON parse doSomething signal payload.");
        throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
    }

    if (!doc.IsObject()) {
        throw std::runtime_error("Received payload is not an object");
    }

    boost::uuids::uuid correlationIdUuid = boost::lexical_cast<boost::uuids::uuid>(correlationId);
    auto promiseItr = _pendingDoSomethingMethodCalls.find(correlationIdUuid);
    if (promiseItr != _pendingDoSomethingMethodCalls.end())
    {
        // Response has multiple values.
        
        rapidjson::Value::ConstMemberIterator labelItr = doc.FindMember("label");
        const std::string& label = labelItr->value.GetString();
        
        rapidjson::Value::ConstMemberIterator identifierItr = doc.FindMember("identifier");
        int identifier = identifierItr->value.GetInt();
        
        rapidjson::Value::ConstMemberIterator dayItr = doc.FindMember("day");
        DayOfTheWeek day = static_cast<DayOfTheWeek>(dayItr->value.GetInt());
        
        DoSomethingReturnValue returnValue { //initializer list
        
            label,
            identifier,
            day
        };
        promiseItr->second.set_value(returnValue);
    }

    std::cout << "End of response handler for " << topic << std::endl;
}
