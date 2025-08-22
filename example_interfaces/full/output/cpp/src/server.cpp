
#include <vector>
#include <iostream>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>
#include <rapidjson/document.h>

#include "server.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"


constexpr const char ExampleServer::NAME[];
constexpr const char ExampleServer::INTERFACE_VERSION[];

ExampleServer::ExampleServer(std::shared_ptr<IBrokerConnection> broker) : _broker(broker) {
    _broker->AddMessageCallback([this](const std::string& topic, const std::string& payload, const boost::optional<std::string> optCorrelationId, const boost::optional<std::string> optResponseTopic, const boost::optional<MethodResultCode> unusedRc)
    {
        _receiveMessage(topic, payload, optCorrelationId, optResponseTopic);
    });
    
    _broker->Subscribe("Example/method/addNumbers", 2);
    
    _broker->Subscribe("Example/method/doSomething", 2);
    
}

void ExampleServer::_receiveMessage(
        const std::string& topic, 
        const std::string& payload, 
        const boost::optional<std::string> optCorrelationId, 
        const boost::optional<std::string> optResponseTopic)
{
    
    if (_broker->TopicMatchesSubscription(topic, "Example/method/addNumbers"))
    {
        std::cout << "Message matched topic Example/method/addNumbers\n";
        rapidjson::Document doc;
        try {
            if (_addNumbersHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callAddNumbersHandler(topic, doc, optCorrelationId, optResponseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely. 
            // TODO: Log this failure
        }
    }
    
    if (_broker->TopicMatchesSubscription(topic, "Example/method/doSomething"))
    {
        std::cout << "Message matched topic Example/method/doSomething\n";
        rapidjson::Document doc;
        try {
            if (_doSomethingHandler)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse  signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                _callDoSomethingHandler(topic, doc, optCorrelationId, optResponseTopic);
            }
        }
        catch (const boost::bad_lexical_cast&)
        {
            // We couldn't find an integer out of the string in the topic name,
            // so we are dropping the message completely. 
            // TODO: Log this failure
        }
    }
    
}


boost::future<bool> ExampleServer::emitTodayIsSignal(int dayOfMonth, boost::optional<DayOfTheWeek> dayOfWeek)
{
    rapidjson::Document doc;
    doc.SetObject();
    
    
    doc.AddMember("dayOfMonth",dayOfMonth, doc.GetAllocator());
    
    if (dayOfWeek)
    doc.AddMember("dayOfWeek", static_cast<int>(*dayOfWeek), doc.GetAllocator());
    
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    return _broker->Publish("Example/signal/todayIs", buf.GetString(), 1, false, boost::none, boost::none, boost::none);
}



void ExampleServer::registerAddNumbersHandler(std::function<int(int, int, boost::optional<int>)> func)
{
    std::cout << "Registered method to handle Example/method/addNumbers\n";
    _addNumbersHandler = func;
}

void ExampleServer::registerDoSomethingHandler(std::function<DoSomethingReturnValue(const std::string&)> func)
{
    std::cout << "Registered method to handle Example/method/doSomething\n";
    _doSomethingHandler = func;
}



void ExampleServer::_callAddNumbersHandler(
        const std::string& topic, 
        const rapidjson::Document& doc, 
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic) const
{
    std::cout << "Handling call to addNumbers\n";
    if (_addNumbersHandler) {
        
        int tempFirst;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
            if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                
                tempFirst = itr->value.GetInt();
                
            } else {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }
        
        int tempSecond;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
            if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                
                tempSecond = itr->value.GetInt();
                
            } else {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }
        
        boost::optional<int> tempThird;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("third");
            if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                
                tempThird = itr->value.GetInt();
                
            } else {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }
        

        int ret = _addNumbersHandler(tempFirst, tempSecond, tempThird);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();
            
            
            // add the sum (a/n PRIMITIVE) to the json
            rapidjson::Value returnValueSum;
            returnValueSum.SetInt(ret);  
            responseJson.AddMember("sum", returnValueSum, responseJson.GetAllocator());
            

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, optCorrelationId, boost::none, MethodResultCode::SUCCESS);
        }
    }
}

void ExampleServer::_callDoSomethingHandler(
        const std::string& topic, 
        const rapidjson::Document& doc, 
        const boost::optional<std::string> optCorrelationId,
        const boost::optional<std::string> optResponseTopic) const
{
    std::cout << "Handling call to doSomething\n";
    if (_doSomethingHandler) {
        
        std::string tempAString;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("aString");
            if (itr != doc.MemberEnd() && itr->value.IsString()) {
                
                tempAString = itr->value.GetString();
                
            } else {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }
        

        DoSomethingReturnValue ret = _doSomethingHandler(tempAString);

        if (optResponseTopic)
        {
            rapidjson::Document responseJson;
            responseJson.SetObject();
            
            // Return type is a struct of values that need added to json
            
            // add the label (a/n PRIMITIVE) to the json
            rapidjson::Value returnValueLabel;
            returnValueLabel.SetString(ret.label.c_str(), ret.label.size(), responseJson.GetAllocator());  
            responseJson.AddMember("label", returnValueLabel, responseJson.GetAllocator());
            
            
            // add the identifier (a/n PRIMITIVE) to the json
            rapidjson::Value returnValueIdentifier;
            returnValueIdentifier.Set(ret.identifier);  
            responseJson.AddMember("identifier", returnValueIdentifier, responseJson.GetAllocator());
            
            
            // add the day (a/n ENUM) to the json
            rapidjson::Value returnValueDay;
            returnValueDay.SetInt(static_cast<int>(ret.day)); 
            responseJson.AddMember("day", returnValueDay, responseJson.GetAllocator());
            
            

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            _broker->Publish(*optResponseTopic, buf.GetString(), 2, false, optCorrelationId, boost::none, MethodResultCode::SUCCESS);
        }
    }
}
