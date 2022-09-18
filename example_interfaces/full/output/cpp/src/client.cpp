
#include <vector>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
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
}
void ExampleClient::registerTodayIsCallback(const std::function<void(int, DayOfTheWeek)>& cb) {
    _todayIsCallback = cb;
}