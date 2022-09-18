
#include <vector>
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
}

void ExampleServer::_receiveMessage(const std::string& topic, const std::string& payload)
{
    
    if (_broker->TopicMatchesSubscription(topic, "Example/method/addNumbers"))
    {
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

                _calladdNumbersHandler(topic, doc);
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
    _addNumbersHandler = func;
}



void ExampleServer::_calladdNumbersHandler(const std::string& topic, const rapidjson::Document& doc)
{
    if (_addNumbersHandler) {
        
        int tempFirst;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("first");
            if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                
                tempfirst = itr->value.GetInt();
                
            } else {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }
        
        int tempSecond;
        { // Scoping
            rapidjson::Value::ConstMemberIterator itr = doc.FindMember("second");
            if (itr != doc.MemberEnd() && itr->value.IsInt()) {
                
                tempsecond = itr->value.GetInt();
                
            } else {
                throw std::runtime_error("Received payload doesn't have required value/type");
            }
        }
        

        _addNumbersHandler(tempFirst, tempSecond);
    }
