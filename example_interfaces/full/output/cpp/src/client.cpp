
#include <vector>
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


constexpr const char ExampleClient::NAME[];
constexpr const char ExampleClient::INTERFACE_VERSION[];

ExampleClient::ExampleClient(std::shared_ptr<IBrokerConnection> broker) : _broker(broker)
{
    _broker->AddMessageCallback([this](const std::string& topic, const std::string& payload)
    {
        _receiveMessage(topic, payload);
    });
    _broker->Subscribe("Example/signal/todayIs", 1);
    
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/Example/method/addNumbers/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
    { // Restrict scope
        std::stringstream responseTopicStringStream;
        responseTopicStringStream << boost::format("client/%1%/Example/method/doSomething/response") % _broker->GetClientId();
        _broker->Subscribe(responseTopicStringStream.str(), 2);
    }
}

void ExampleClient::_receiveMessage(const std::string& topic, const std::string& payload)
{
    if (_broker->TopicMatchesSubscription(topic, "Example/signal/todayIs"))
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
                
                DayOfTheWeek tempdayOfWeek;
                { // Scoping
                    rapidjson::Value::ConstMemberIterator itr = doc.FindMember("dayOfWeek");
                    if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                        
                        tempdayOfWeek = static_cast<DayOfTheWeek>(itr->value.GetInt());
                        
                    } else {
                        throw std::runtime_error("Received payload doesn't have required value/type");
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
     if (_broker->TopicMatchesSubscription(topic, "client/+/Example/method/addNumbers/response"))
    {
        _handleAddNumbersResponse(topic, payload);
    }
    else if (_broker->TopicMatchesSubscription(topic, "client/+/Example/method/doSomething/response"))
    {
        _handleDoSomethingResponse(topic, payload);
    }
}
void ExampleClient::registerTodayIsCallback(const std::function<void(int, DayOfTheWeek)>& cb) {
    _todayIsCallback = cb;
}


boost::future<int> ExampleClient::addNumbers(int first, int second) {
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingAddNumbersMethodCalls[correlationId] = boost::promise<int>();

    rapidjson::Document doc;
    doc.SetObject();
    rapidjson::Value correlationIdValue;
    correlationIdValue.SetString(correlationIdStr.c_str(), correlationIdStr.size(), doc.GetAllocator());
    doc.AddMember("correlationId", correlationIdValue, doc.GetAllocator());
    
    
    
    doc.AddMember("first", first, doc.GetAllocator());
    
    
    
    doc.AddMember("second", second, doc.GetAllocator());
    
    
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    _broker->Publish("Example/method/addNumbers", buf.GetString(), 2, false);

    return _pendingAddNumbersMethodCalls[correlationId].get_future();
}

void ExampleClient::_handleAddNumbersResponse(const std::string& topic, const std::string& payload)
{

}

boost::future<DoSomethingReturnValue> ExampleClient::doSomething(const std::string& aString) {
    auto correlationId = boost::uuids::random_generator()();
    const std::string correlationIdStr = boost::lexical_cast<std::string>(correlationId);
    _pendingDoSomethingMethodCalls[correlationId] = boost::promise<DoSomethingReturnValue>();

    rapidjson::Document doc;
    doc.SetObject();
    rapidjson::Value correlationIdValue;
    correlationIdValue.SetString(correlationIdStr.c_str(), correlationIdStr.size(), doc.GetAllocator());
    doc.AddMember("correlationId", correlationIdValue, doc.GetAllocator());
    
    
    
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(aString.c_str(), aString.size(), doc.GetAllocator());
        doc.AddMember("aString", tempStringValue, doc.GetAllocator());
    }
    
    
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> writer(buf);
    doc.Accept(writer);
    _broker->Publish("Example/method/doSomething", buf.GetString(), 2, false);

    return _pendingDoSomethingMethodCalls[correlationId].get_future();
}

void ExampleClient::_handleDoSomethingResponse(const std::string& topic, const std::string& payload)
{

}
