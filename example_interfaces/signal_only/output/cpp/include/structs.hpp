/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/

#pragma once
#include <string>
#include <cstddef>
#include <chrono>
#include <vector>
#include <boost/optional.hpp>
#include <rapidjson/document.h>
#include "enums.hpp"

// Utility function to convert ISO timestamp string to time_point
std::chrono::time_point<std::chrono::system_clock> parseIsoTimestamp(const std::string& isoTimestamp);

// Utility function to convert time_point to ISO timestamp string
std::string timePointToIsoString(const std::chrono::time_point<std::chrono::system_clock>& timePoint);

std::string durationToIsoString(const std::chrono::duration<double>& duration);

std::chrono::duration<double> parseIsoDuration(const std::string& isoDuration);

// Base64 encode binary data using Boost; takes a vector of unsigned bytes and returns std::string
std::string base64Encode(const std::vector<unsigned char>& data);

// Decode a base64 encoded string into a vector of bytes
std::vector<unsigned char> base64Decode(const std::string& b64input);
