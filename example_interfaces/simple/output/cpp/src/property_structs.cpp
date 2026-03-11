

#include "property_structs.hpp"
#include <rapidjson/document.h>

namespace stinger {

namespace gen {
namespace simple {

SchoolProperty SchoolProperty::FromRapidJsonObject(const rapidjson::Value& jsonObj)
{
    SchoolProperty school;

    { // Scoping
        rapidjson::Value::ConstMemberIterator itr = jsonObj.FindMember("name");
        if (itr != jsonObj.MemberEnd() && itr->value.IsString()) {
            school.name = itr->value.GetString();

        } else {
            throw std::runtime_error("Received payload for the 'name' argument doesn't have required value/type");
        }
    }

    return school;
};

void SchoolProperty::AddToRapidJsonObject(rapidjson::Value& parent, rapidjson::Document::AllocatorType& allocator) const
{
    { // restrict scope
        rapidjson::Value tempStringValue;
        tempStringValue.SetString(name.c_str(), name.size(), allocator);
        parent.AddMember("name", tempStringValue, allocator);
    }
}

} // namespace simple

} // namespace gen

} // namespace stinger
