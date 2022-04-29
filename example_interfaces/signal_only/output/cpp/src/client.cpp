
#include <vector>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/functional/hash.hpp>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/writer.h>
#include <rapidjson/error/en.h>

#include "client.hpp"
#include "enums.hpp"
#include "ibrokerconnection.hpp"


constexpr char SignalOnlyClient::NAME[];
constexpr char SignalOnlyClient::INTERFACE_VERSION[];

SignalOnlyClient::SignalOnlyClient(std::shared_ptr<IBrokerConnection> broker) : _broker(broker)
{
    _broker->AddMessageCallback([this](const std::string& topic, const std::string& payload)
    {
        ReceiveMessage(topic, payload);
    });
}

void SignalOnlyClient::ReceiveMessage(const std::string& topic, const std::string& payload)
{
    if (_broker->TopicMatchesSubscription(topic, "SignalOnly/signal/anotherSignal"))
    {
        //Log("Handling anotherSignal signal");
        rapidjson::Document doc;
        try {
            if (_anotherSignalCallback)
            {
                rapidjson::ParseResult ok = doc.Parse(payload.c_str());
                if (!ok)
                {
                    //Log("Could not JSON parse anotherSignal signal payload.");
                    throw std::runtime_error(rapidjson::GetParseError_En(ok.Code()));
                }

                if (!doc.IsObject()) {
                    throw std::runtime_error("Received payload is not an object");
                }

                
                double tempone;
                { // Scoping
                    Value::ConstMemberIterator itr = doc.FindMember("one");
                    if (itr != doc.MemberEnd() && itr->value.IsDouble()) {
                        
                        tempone = itr->value.GetDouble();
                        
                    } else {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }
                
                bool temptwo;
                { // Scoping
                    Value::ConstMemberIterator itr = doc.FindMember("two");
                    if (itr != doc.MemberEnd() && itr->value.IsBool()) {
                        
                        temptwo = itr->value.GetBool();
                        
                    } else {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }
                
                const std::string& tempthree;
                { // Scoping
                    Value::ConstMemberIterator itr = doc.FindMember("three");
                    if (itr != doc.MemberEnd() && itr->value.IsString()) {
                        
                        tempthree = itr->value.GetString();
                        
                    } else {
                        throw std::runtime_error("Received payload doesn't have required value/type");
                    }
                }
                

                _anotherSignalCallback(tempone, temptwo, tempthree);
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
void SignalOnlyClient::registerAnotherSignalCallback(const std::function<void(double, bool, const std::string&)>& cb) {
    _anotherSignalCallback = cb;
}