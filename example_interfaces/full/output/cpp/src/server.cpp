
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
    _broker->AddMessageCallback([this](const std::string& topic, const std::string& payload)
    {
        _receiveMessage(topic, payload);
    });
    
    _broker->Subscribe("Example/method/addNumbers", 2);
    
    _broker->Subscribe("Example/method/doSomething", 2);
    
}

void ExampleServer::_receiveMessage(const std::string& topic, const std::string& payload)
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
                boost::optional<std::string> optClientId;
                boost::optional<std::string> optCorrelationId;

                if (doc.HasMember("clientId") && doc["clientId"].IsString())
                {
                    optClientId = doc["clientId"].GetString();
                }

                if (doc.HasMember("correlationId") && doc["correlationId"].IsString())
                {
                    optCorrelationId = doc["correlationId"].GetString();
                }

                _calladdNumbersHandler(topic, doc, optClientId, optCorrelationId);
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
                boost::optional<std::string> optClientId;
                boost::optional<std::string> optCorrelationId;

                if (doc.HasMember("clientId") && doc["clientId"].IsString())
                {
                    optClientId = doc["clientId"].GetString();
                }

                if (doc.HasMember("correlationId") && doc["correlationId"].IsString())
                {
                    optCorrelationId = doc["correlationId"].GetString();
                }

                _calldoSomethingHandler(topic, doc, optClientId, optCorrelationId);
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


boost::future<bool> ExampleServer::emitTodayIsSignal(int dayOfMonth, DayOfTheWeek dayOfWeek)
{
    rapidjson::Document doc;
    doc.SetObject();
    
    
    
    doc.AddMember("dayOfMonth", dayOfMonth, doc.GetAllocator());
    
    
    
    doc.AddMember("dayOfWeek", static_cast<int>(dayOfWeek), doc.GetAllocator());
    
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    return _broker->Publish("Example/signal/todayIs", buf.GetString(), 1, false);
}



void ExampleServer::registerAddNumbersHandler(std::function<int(int, int)> func)
{
    std::cout << "Registered method to handle Example/method/addNumbers\n";
    _addNumbersHandler = func;
}

void ExampleServer::registerDoSomethingHandler(std::function<DoSomethingReturnValue(const std::string&)> func)
{
    std::cout << "Registered method to handle Example/method/doSomething\n";
    _doSomethingHandler = func;
}



void ExampleServer::_calladdNumbersHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const
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
        

        int ret = _addNumbersHandler(tempFirst, tempSecond);

        if (clientId)
        {
            std::stringstream ss;
            ss << boost::format("client/%1%/Example/method/addNumbers/response") % *clientId;
            std::string responseTopic = ss.str();

            rapidjson::Document responseJson;
            responseJson.SetObject();

            rapidjson::Value resultValue;
            resultValue.SetInt(0);
            responseJson.AddMember("result", resultValue, responseJson.GetAllocator());

            if (correlationId) {
                rapidjson::Value correlationIdValue;
                correlationIdValue.SetString(correlationId->c_str(), correlationId->size(), responseJson.GetAllocator());
                responseJson.AddMember("correlationId", correlationIdValue, responseJson.GetAllocator());
            }
            
            
            // add the sum (a/n VALUE) to the json
            rapidjson::Value returnValueSum;
            returnValueSum.SetInt(ret);  
            responseJson.AddMember("sum", returnValueSum, responseJson.GetAllocator());
            

            rapidjson::StringBuffer buf;
            rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
            responseJson.Accept(writer);
            _broker->Publish(responseTopic, buf.GetString(), 2, true);
        }
    }
}

void ExampleServer::_calldoSomethingHandler(const std::string& topic, const rapidjson::Document& doc, boost::optional<std::string> clientId, boost::optional<std::string> correlationId) const
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

        if (clientId)
        {
            std::stringstream ss;
            ss << boost::format("client/%1%/Example/method/doSomething/response") % *clientId;
            std::string responseTopic = ss.str();

            rapidjson::Document responseJson;
            responseJson.SetObject();

            rapidjson::Value resultValue;
            resultValue.SetInt(0);
            responseJson.AddMember("result", resultValue, responseJson.GetAllocator());

            if (correlationId) {
                rapidjson::Value correlationIdValue;
                correlationIdValue.SetString(correlationId->c_str(), correlationId->size(), responseJson.GetAllocator());
                responseJson.AddMember("correlationId", correlationIdValue, responseJson.GetAllocator());
            }
            
            // Return type is a struct of values that need added to json
            
            // add the label (a/n VALUE) to the json
            rapidjson::Value returnValueLabel;
            returnValueLabel.SetString(ret.label.c_str(), ret.label.size(), responseJson.GetAllocator());  
            responseJson.AddMember("label", returnValueLabel, responseJson.GetAllocator());
            
            
            // add the identifier (a/n VALUE) to the json
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
            _broker->Publish(responseTopic, buf.GetString(), 2, true);
        }
    }
}
