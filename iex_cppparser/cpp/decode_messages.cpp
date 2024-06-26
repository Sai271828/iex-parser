#include "decode_messages.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <ctime>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <iomanip>
#include <string>
#include "/vagrant/utils/logger.h"
using namespace std;
Log logger;


// Function to convert trade sale condition flags to a string
string convert_trade_sale_condition_to_string(char sale_condition_flags) {
    // Convert char to int for bitwise operations
    int sale_condition_flags_int = static_cast<int>(sale_condition_flags);

    // Vector to store sale condition strings
    std::vector<std::string> sale_condition_strings;

    // Check each bit in the sale_condition_flags_int and add corresponding strings to the vector
    if (sale_condition_flags_int & 0x80) {
        sale_condition_strings.push_back("INTERMARKET_SWEEP");
    }
    if (sale_condition_flags_int & 0x40) {
        sale_condition_strings.push_back("EXTENDED_HOURS");
    } else {
        sale_condition_strings.push_back("REGULAR_HOURS");
    }
    if (sale_condition_flags_int & 0x20) {
        sale_condition_strings.push_back("ODD_LOT");
    }
    if (sale_condition_flags_int & 0x10) {
        sale_condition_strings.push_back("TRADE_THROUGH_EXEMPT");
    }
    if (sale_condition_flags_int & 0x08) {
        sale_condition_strings.push_back("SINGLE_PRICE_CROSS");
    }

    // Generate a single string containing all encoded fields within sale_condition_flags, separated by '|'
    std::string sale_condition_string = "";
    for (const auto& condition : sale_condition_strings) {
        sale_condition_string += condition + "|";
    }

    // Remove the trailing '|'
    if (!sale_condition_string.empty()) {
        sale_condition_string.pop_back();
    }

    return sale_condition_string;
}

// Function to parse a trade report message
pair<string, string> parse_trade_report_message(const vector<char>& payload) {
    char sale_condition_flags;
    unsigned long long timestamp_raw;
    char symbol_raw[8];
    unsigned int size;
    unsigned long long price_raw;
    unsigned long long trade_id;

    // Unpack the data from the payload
    memcpy(&sale_condition_flags, &payload[1], sizeof(char));
    memcpy(&timestamp_raw, &payload[2], sizeof(unsigned long long));
    memcpy(symbol_raw, &payload[10], 8);
    memcpy(&size, &payload[18], sizeof(unsigned int));
    memcpy(&price_raw, &payload[22], sizeof(unsigned long long));
    memcpy(&trade_id, &payload[30], sizeof(unsigned long long));

    // Convert symbol from raw bytes to string
    string symbol(symbol_raw, symbol_raw + 8);
    symbol = symbol.substr(0, symbol.find(' ')); // Remove trailing null characters

    // Calculate price
    double price = static_cast<double>(price_raw) * 1e-4;

    // Convert sale condition flags to string
    string saleConditionString = convert_trade_sale_condition_to_string(sale_condition_flags);

    // Create the message string
    string parsed_string = to_string(timestamp_raw) + "," + "T," + symbol + "," + to_string(size) + ","
                            + to_string(price) + "," + to_string(trade_id) + "," + saleConditionString ;

    return make_pair(parsed_string, symbol);
}

// Function to parse a price level update message
pair<string, string> parse_price_level_update(const vector<char>& payload) {
    char event_flags;
    uint64_t timestamp_raw;
    char symbol_raw[8];
    uint32_t size;
    int32_t price_raw;

    // Unpack the data from the payload
    memcpy(&event_flags, &payload[1], sizeof(char));
    memcpy(&timestamp_raw, &payload[2], sizeof(uint64_t));
    memcpy(symbol_raw, &payload[10], sizeof(symbol_raw));
    memcpy(&size, &payload[18], sizeof(uint32_t));
    memcpy(&price_raw, &payload[22], sizeof(uint32_t));

    // Convert price from raw to double
    double price = price_raw * 1e-4;

    // Convert symbol from raw bytes to string
    string symbol(symbol_raw, 8);
    symbol = symbol.substr(0, symbol.find(' '));

    // Determine record type based on size
    string record_type;
    if (size == 0) {
        record_type = "Z";
    } else {
        record_type = "R";
    }

    // Check event flags and construct event output string
    if (event_flags == '\x01') {
        string flag = "1";
        string event_output_string = to_string(timestamp_raw) + "," + "PRL," + symbol + "," + to_string(price) + ","
                                      + to_string(size) + "," + record_type + "," + flag;
        return make_pair(event_output_string, symbol);
    } else if (event_flags == '\x00') {
        string flag = "0";
        string event_output_string = to_string(timestamp_raw) + "," + "PRL," + symbol + "," + to_string(price) + ","
                                      + to_string(size) + "," + record_type + "," + flag;
        return make_pair(event_output_string, symbol);
    } else {
        cout << "Error: Invalid event flag encountered in price level update message" << endl;
        logger.write("Error: Invalid event flag encountered in price level update message");
        return make_pair("", "");
    }
}

// If you want to parse a different message type, you can add a new function here
