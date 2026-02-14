#pragma once

#include <stinger/error/return_codes.hpp>

// Use the exception classes from stinger-cpp-utils
using stinger::error::ClientDeserializationErrorException;
using stinger::error::ClientErrorException;
using stinger::error::ClientSerializationErrorException;
using stinger::error::createStingerException;
using stinger::error::MethodNotFoundException;
using stinger::error::MethodReturnCode;
using stinger::error::NotImplementedException;
using stinger::error::OutOfSyncException;
using stinger::error::PayloadErrorException;
using stinger::error::ServerDeserializationErrorException;
using stinger::error::ServerErrorException;
using stinger::error::ServerSerializationErrorException;
using stinger::error::ServiceUnavailableException;
using stinger::error::StingerMethodException;
using stinger::error::SuccessException;
using stinger::error::TimeoutException;
using stinger::error::TransportErrorException;
using stinger::error::UnauthorizedException;
using stinger::error::UnknownErrorException;
