
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
        

        auto ret = _addNumbersHandler(tempFirst, tempSecond);

        if (clientId)
        {
            std::stringstream ss;
            ss << boost::format("client/%1%/Example/method/addNumbers/response") % *clientId;
            std::string responseTopic = ss.str();

            rapidjson::Document responseJson;
            responseJson.SetObject();
            if (correlationId) {
                rapidjson::Value correlationIdValue;
                correlationIdValue.SetString(correlationId->c_str(), correlationId->size(), responseJson.GetAllocator());
                responseJson.AddMember("correlationId", correlationIdValue, responseJson.GetAllocator());
            }
            
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
