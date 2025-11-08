# Qt generator

## What is done
1. CMakeLists + cmake config file
2. ibrokerconnection.hpp / broker.hpp
3. enums.hpp
4. structs.hpp
5. property_structs.hpp

## What is partially done
1. args. QDuration is not a thing, need to find a way to represent time duration as a QML property

## What is not done
1. client and server. Server will probably remain C++ only, and only serve as a way to test clients
2. discovery
3. signal payloads
4. exceptions

## Intent
1. Replacement of boost for Qt analogs
2. Expose all of the client data via properties. Each client would be a QML_SINGELTON. Each Property struct is exposed as Q_PROPERTY pointer to a QObject class. This allows easy scoped access via ?.
3. Expose all of the defined structs as QML types. Each struct will be a QObject. Each field will be a Q_PROPERTY. Optional fields will be stored as std::optional and generate a field and a fieldValid Q_PROPERTY.
4. Enums will be exposed as Q_NAMESPACE enums.
5. Replace the callback system with Qt signals/slots.
