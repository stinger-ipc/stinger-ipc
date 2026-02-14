/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the testable interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#pragma once
#include <string>
#include <cstddef>
#include <chrono>
#include <vector>

namespace stinger {

namespace gen {
namespace testable {

// Utility function to convert ISO timestamp string to time_point
std::chrono::time_point<std::chrono::system_clock> stinger::utils::parseIsoTimestamp(const std::string& isoTimestamp);

// Utility function to convert time_point to ISO timestamp string
std::string stinger::utils::timePointToIsoString(const std::chrono::time_point<std::chrono::system_clock>& timePoint);

std::string stinger::utils::durationToIsoString(const std::chrono::duration<double>& duration);

std::chrono::duration<double> stinger::utils::parseIsoDuration(const std::string& isoDuration);

// Base64 encode binary data; takes a vector of unsigned bytes and returns std::string
std::string stinger::utils::base64Encode(const std::vector<unsigned char>& data);

// Decode a base64 encoded string into a vector of bytes
std::vector<unsigned char> stinger::utils::base64Decode(const std::string& b64input);

} // namespace testable

} // namespace gen

} // namespace stinger
