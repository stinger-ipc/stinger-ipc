#include "interface_exceptions.hpp"

std::exception_ptr createStingerException(MethodReturnCode code, const std::string& message)
{
    switch (code)
    {
        case MethodReturnCode::SUCCESS:
            return std::make_exception_ptr(SuccessException(message));
            break;

        case MethodReturnCode::CLIENT_ERROR:
            return std::make_exception_ptr(ClientErrorException(message));
            break;

        case MethodReturnCode::SERVER_ERROR:
            return std::make_exception_ptr(ServerErrorException(message));
            break;

        case MethodReturnCode::TRANSPORT_ERROR:
            return std::make_exception_ptr(TransportErrorException(message));
            break;

        case MethodReturnCode::PAYLOAD_ERROR:
            return std::make_exception_ptr(PayloadErrorException(message));
            break;

        case MethodReturnCode::CLIENT_SERIALIZATION_ERROR:
            return std::make_exception_ptr(ClientSerializationErrorException(message));
            break;

        case MethodReturnCode::CLIENT_DESERIALIZATION_ERROR:
            return std::make_exception_ptr(ClientDeserializationErrorException(message));
            break;

        case MethodReturnCode::SERVER_SERIALIZATION_ERROR:
            return std::make_exception_ptr(ServerSerializationErrorException(message));
            break;

        case MethodReturnCode::SERVER_DESERIALIZATION_ERROR:
            return std::make_exception_ptr(ServerDeserializationErrorException(message));
            break;

        case MethodReturnCode::METHOD_NOT_FOUND:
            return std::make_exception_ptr(MethodNotFoundException(message));
            break;

        case MethodReturnCode::UNAUTHORIZED:
            return std::make_exception_ptr(UnauthorizedException(message));
            break;

        case MethodReturnCode::TIMEOUT:
            return std::make_exception_ptr(TimeoutException(message));
            break;

        case MethodReturnCode::OUT_OF_SYNC:
            return std::make_exception_ptr(OutOfSyncException(message));
            break;

        case MethodReturnCode::UNKNOWN_ERROR:
            return std::make_exception_ptr(UnknownErrorException(message));
            break;

        case MethodReturnCode::NOT_IMPLEMENTED:
            return std::make_exception_ptr(NotImplementedException(message));
            break;

        case MethodReturnCode::SERVICE_UNAVAILABLE:
            return std::make_exception_ptr(ServiceUnavailableException(message));
            break;

        default:
            return std::make_exception_ptr(StingerMethodException(code, message));
    }
}