#pragma once

#include <exception>
#include <string>
#include "ibrokerconnection.hpp"

class StingerMethodException: public std::exception
{
public:
    StingerMethodException(MethodReturnCode code, const std::string& message): _code(code), _message(message) { }

    virtual const char* what() const noexcept override { return _message.c_str(); }

    MethodReturnCode code() const noexcept { return _code; }

private:
    MethodReturnCode _code;
    std::string _message;
};

class SuccessException: public StingerMethodException
{
public:
    SuccessException(const std::string& message): StingerMethodException(MethodReturnCode::SUCCESS, message) { }
};

class ClientErrorException: public StingerMethodException
{
public:
    ClientErrorException(const std::string& message): StingerMethodException(MethodReturnCode::CLIENT_ERROR, message) { }
};

class ServerErrorException: public StingerMethodException
{
public:
    ServerErrorException(const std::string& message): StingerMethodException(MethodReturnCode::SERVER_ERROR, message) { }
};

class TransportErrorException: public StingerMethodException
{
public:
    TransportErrorException(const std::string& message): StingerMethodException(MethodReturnCode::TRANSPORT_ERROR, message) { }
};

class PayloadErrorException: public StingerMethodException
{
public:
    PayloadErrorException(const std::string& message): StingerMethodException(MethodReturnCode::PAYLOAD_ERROR, message) { }
};

class ClientSerializationErrorException: public StingerMethodException
{
public:
    ClientSerializationErrorException(const std::string& message): StingerMethodException(MethodReturnCode::CLIENT_SERIALIZATION_ERROR, message) { }
};

class ClientDeserializationErrorException: public StingerMethodException
{
public:
    ClientDeserializationErrorException(const std::string& message): StingerMethodException(MethodReturnCode::CLIENT_DESERIALIZATION_ERROR, message) { }
};

class ServerSerializationErrorException: public StingerMethodException
{
public:
    ServerSerializationErrorException(const std::string& message): StingerMethodException(MethodReturnCode::SERVER_SERIALIZATION_ERROR, message) { }
};

class ServerDeserializationErrorException: public StingerMethodException
{
public:
    ServerDeserializationErrorException(const std::string& message): StingerMethodException(MethodReturnCode::SERVER_DESERIALIZATION_ERROR, message) { }
};

class MethodNotFoundException: public StingerMethodException
{
public:
    MethodNotFoundException(const std::string& message): StingerMethodException(MethodReturnCode::METHOD_NOT_FOUND, message) { }
};

class UnauthorizedException: public StingerMethodException
{
public:
    UnauthorizedException(const std::string& message): StingerMethodException(MethodReturnCode::UNAUTHORIZED, message) { }
};

class TimeoutException: public StingerMethodException
{
public:
    TimeoutException(const std::string& message): StingerMethodException(MethodReturnCode::TIMEOUT, message) { }
};

class OutOfSyncException: public StingerMethodException
{
public:
    OutOfSyncException(const std::string& message): StingerMethodException(MethodReturnCode::OUT_OF_SYNC, message) { }
};

class UnknownErrorException: public StingerMethodException
{
public:
    UnknownErrorException(const std::string& message): StingerMethodException(MethodReturnCode::UNKNOWN_ERROR, message) { }
};

class NotImplementedException: public StingerMethodException
{
public:
    NotImplementedException(const std::string& message): StingerMethodException(MethodReturnCode::NOT_IMPLEMENTED, message) { }
};

class ServiceUnavailableException: public StingerMethodException
{
public:
    ServiceUnavailableException(const std::string& message): StingerMethodException(MethodReturnCode::SERVICE_UNAVAILABLE, message) { }
};

std::exception_ptr createStingerException(MethodReturnCode code, const std::string& message);