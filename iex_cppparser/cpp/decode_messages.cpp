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
#include "logger.h"
using namespace std;
Log logger;

// This file contains functions to decode messages from the binary format used by the IEX DEEP feed.
// The functions in this file are used by the main program to decode messages and write them to the output file.
// Currently, the program can decode trade reports and price level updates.
// You can add additional functions to decode other message types as needed.

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
    // Input validation - minimum required payload size for trade report
    if (payload.size() < 38) {
        cout << "Error: Trade report payload too short (" << payload.size() << " bytes)" << endl;
        logger.write("Error: Trade report payload too short");
        return make_pair("", "");
    }

    char sale_condition_flags;
    unsigned long long timestamp_raw;
    char symbol_raw[8];
    unsigned int size;
    unsigned long long price_raw;
    unsigned long long trade_id;

    // Unpack the data from the payload with bounds checking
    memcpy(&sale_condition_flags, &payload[1], sizeof(char));
    memcpy(&timestamp_raw, &payload[2], sizeof(unsigned long long));
    memcpy(symbol_raw, &payload[10], 8);
    memcpy(&size, &payload[18], sizeof(unsigned int));
    memcpy(&price_raw, &payload[22], sizeof(unsigned long long));
    memcpy(&trade_id, &payload[30], sizeof(unsigned long long));

    // Convert symbol from raw bytes to string with proper null-termination handling
    string symbol;
    for (int i = 0; i < 8; i++) {
        if (symbol_raw[i] == '\0' || symbol_raw[i] == ' ') {
            break;
        }
        symbol += symbol_raw[i];
    }
    
    // Validate symbol is not empty
    if (symbol.empty()) {
        cout << "Error: Empty symbol in trade report" << endl;
        logger.write("Error: Empty symbol in trade report");
        return make_pair("", "");
    }

    // Calculate price with validation
    double price = static_cast<double>(price_raw) * 1e-4;
    
    // Validate trade data ranges
    if (price <= 0 || price > 1000000) {
        cout << "Warning: Unusual price value in trade: " << price << endl;
        logger.write("Warning: Unusual price value in trade report");
    }
    
    if (size == 0) {
        cout << "Warning: Zero size trade detected" << endl;
        logger.write("Warning: Zero size trade detected");
    }

    // Convert sale condition flags to string
    string saleConditionString = convert_trade_sale_condition_to_string(sale_condition_flags);

    // Create the message string
    string parsed_string = to_string(timestamp_raw) + "," + "T," + symbol + "," + to_string(size) + ","
                            + to_string(price) + "," + to_string(trade_id) + "," + saleConditionString ;

    return make_pair(parsed_string, symbol);
}

// Function to parse a price level update message
pair<string, string> parse_price_level_update(const vector<char>& payload) {
    // Input validation - minimum required payload size
    if (payload.size() < 26) {
        cout << "Error: Price level update payload too short (" << payload.size() << " bytes)" << endl;
        logger.write("Error: Price level update payload too short");
        return make_pair("", "");
    }

    char event_flags;
    uint64_t timestamp_raw;
    char symbol_raw[8];
    uint32_t size;
    uint32_t price_raw;  // Fixed: Changed from int32_t to uint32_t to match memcpy size

    // Unpack the data from the payload with bounds checking
    memcpy(&event_flags, &payload[1], sizeof(char));
    memcpy(&timestamp_raw, &payload[2], sizeof(uint64_t));
    memcpy(symbol_raw, &payload[10], sizeof(symbol_raw));
    memcpy(&size, &payload[18], sizeof(uint32_t));
    memcpy(&price_raw, &payload[22], sizeof(uint32_t));  // Fixed: Now consistent with declaration

    // Convert price from raw to double with validation
    double price = static_cast<double>(price_raw) * 1e-4;
    
    // Validate price range (reasonable bounds for financial data)
    if (price < 0 || price > 1000000) {
        cout << "Warning: Unusual price value: " << price << endl;
        logger.write("Warning: Unusual price value detected");
    }

    // Convert symbol from raw bytes to string with proper null-termination handling
    string symbol;
    for (int i = 0; i < 8; i++) {
        if (symbol_raw[i] == '\0' || symbol_raw[i] == ' ') {
            break;
        }
        symbol += symbol_raw[i];
    }
    
    // Validate symbol is not empty
    if (symbol.empty()) {
        cout << "Error: Empty symbol in price level update" << endl;
        logger.write("Error: Empty symbol in price level update");
        return make_pair("", "");
    }

    // Determine record type based on size
    string record_type;
    if (size == 0) {
        record_type = "Z";
    } else {
        record_type = "R";
    }

    // Check event flags and construct event output string with better error handling
    string flag;
    if (event_flags == '\x01') {
        flag = "1";
    } else if (event_flags == '\x00') {
        flag = "0";
    } else {
        // Handle unexpected event flags more gracefully
        cout << "Warning: Unexpected event flag (0x" << hex << static_cast<int>(event_flags) << ") in price level update, treating as flag 0" << dec << endl;
        logger.write("Warning: Unexpected event flag in price level update message");
        flag = "0";  // Default to flag 0 instead of failing
    }
    
    string event_output_string = to_string(timestamp_raw) + "," + "PRL," + symbol + "," + to_string(price) + ","
                                  + to_string(size) + "," + record_type + "," + flag;
    return make_pair(event_output_string, symbol);
}

// Function to parse a system event message
char parse_system_event_message(const vector<char>& payload) {
    // Input validation - minimum required payload size for system event
    if (payload.size() < 10) {
        cout << "Error: System event payload too short (" << payload.size() << " bytes)" << endl;
        logger.write("Error: System event payload too short");
        return '\0';
    }

    char system_event;
    uint64_t timestamp_raw;

    // Unpack the data from the payload with bounds checking
    memcpy(&system_event, &payload[1], sizeof(char));
    memcpy(&timestamp_raw, &payload[2], sizeof(uint64_t));

    // Log the system event for debugging
    cout << "System Event: '" << system_event << "' (0x" << hex << static_cast<int>(system_event) << ") at timestamp " << dec << timestamp_raw << endl;
    
    switch(system_event) {
        case 'O': // Start of Messages
            cout << "Market: Start of Messages" << endl;
            break;
        case 'S': // Start of System Hours
            cout << "Market: Start of System Hours" << endl;
            break;
        case 'R': // Start of Regular Market Hours
            cout << "Market: Start of Regular Market Hours" << endl;
            break;
        case 'M': // End of Regular Market Hours
            cout << "Market: End of Regular Market Hours" << endl;
            break;
        case 'E': // End of System Hours
            cout << "Market: End of System Hours" << endl;
            break;
        case 'C': // End of Messages - This is the true end of trading session
            cout << "Market: End of Messages - Trading session complete" << endl;
            break;
        default:
            cout << "Market: Unknown system event '" << system_event << "'" << endl;
            break;
    }
    
    logger.write("System event processed: " + string(1, system_event));
    return system_event;
}

// If you want to parse a different message type, you can add a new function here
