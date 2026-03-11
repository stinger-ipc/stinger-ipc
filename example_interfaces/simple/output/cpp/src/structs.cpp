

#include "structs.hpp"

namespace stinger {

namespace gen {
namespace simple {

Person Person::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    Person person;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("name");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            person.name = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'name' argument doesn't have required value/type");
        }
    }
    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("gender");
        if (itr != jsonObj.MemberEnd() && itr->value.IsInt()) {
            person.gender = static_cast<Gender>(itr->value.GetInt());

        } else {
            throw std::runtime_error("Received payload for the 'gender' argument doesn't have required value/type");
        }
    }

    return person;
};

void Person::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(name.c_str(), name.size(), allocator);
        parent.AddMember("name", tempStringValue, allocator);
    }

    parent.AddMember("gender", static_cast<int>(gender), allocator);
}

} // namespace simple

} // namespace gen

} // namespace stinger
