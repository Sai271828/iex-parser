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
#include <algorithm>
#include "logger.h"
#include "decode_messages.h"
using namespace std;

class BasicPcapParser {
private:
    string filename; 
    string output_filename;
    string symbols_of_interest_file;
    int cur_packet_message_count;
    // int total_num_messages_processed;
    std::fstream symbols_file;
    string trade_messages[26];
    string prl_messages[26];
    ofstream output_filenames;
    time_t start_parse_time;
    time_t stop_parse_time;
    string message_buffer = "";
    ifstream input_file;
    Log logger;
    std::vector<std::string> symbols_list;
    vector<int> symbols_of_interest_indices;
    vector<ofstream> trades_output_file;
    vector<ofstream> prl_output_file;
    
    struct PcapPacketHeader {
        uint32_t ts_sec;
        uint32_t ts_usec;
        uint32_t incl_len;
        uint32_t orig_len;
    };
    
public:
    BasicPcapParser(std::string filename, std::string output_filename, std::string symbols_of_interest_file) : filename(filename), output_filename(output_filename),symbols_of_interest_file(symbols_of_interest_file) {
    // Initialization of variables
        cur_packet_message_count = 0;
        // total_num_messages_processed = 0;
    }

    // Function to unpack the pcap packet header
    void unpackPcapPacketHeader(const std::vector<uint8_t>& buffer, PcapPacketHeader& header) {
        if (buffer.size() < sizeof(PcapPacketHeader)) {
            cerr << "Error: Insufficient data in buffer for unpacking." << endl;
            return;
        }

        memcpy(&header, buffer.data(), sizeof(PcapPacketHeader));
    }


    // Function to parse the pcap file  

    int parse(int max_packets_to_parse) {
        // Open the input file
        input_file.open(filename, ios::binary);

        // Check if the file is opened successfully
        if (!input_file.is_open()) {
            cerr << "Error: Unable to open file " << filename << endl;
            return -1;
        }

        
        symbols_file.open(symbols_of_interest_file, std::ios::in); // open file in read mode
        if (symbols_of_interest_file=="ALL")
        {
            cout << "Parsing all symbols" << endl;
            symbols_list = {};
        }
        else if (symbols_file.is_open()) {
            
            std::string line;

            while (std::getline(symbols_file, line)) { // read each line from the file
                symbols_list.push_back(line.substr(0, line.size() - 1)); // add the line to the vector without the newline character
            }

            std::cout << "Read " << symbols_list.size() << " symbols from the file.\n";

            symbols_file.close(); // don't forget to close the file when you're done
        } else {
            std::cout << "Error opening symbols of interest file";
            return -1;
        }

        symbols_of_interest_indices = get_symbol_first_letter_indices(symbols_list);

        // Get the current time as the start time for parsing
        start_parse_time = time(nullptr);
        cout << "Starting parsing @ " << put_time(std::localtime(&start_parse_time), "%c") << endl;
        logger.write("Started parsing");

        // Skip the pcap global header which is 24 bytes long
        int pcap_global_header_len = 24;
        input_file.ignore(pcap_global_header_len);

        int num_packets = 0;

        // Open a file to store output filenames
        output_filenames.open(output_filename + ".txt");

        for (int i = 0; i < 26; i++) {
            ofstream file;
            string output_file = output_filename + "_trd_" + char('a' + i) + ".csv";
            output_filenames << output_file << endl;
            file.open(output_file);
            file << "Packet Capture Time,Send Time,Raw Timestamp,Tick Type,Symbol,Size,Price,Trade ID,Sale Condition\n";
            trades_output_file.push_back(std::move(file));
        }

        for (int i = 0; i < 26; i++) {
            ofstream file;
            string output_file = output_filename + "_prl_" + char('a' + i) + ".csv";
            output_filenames << output_file << endl;
            file.open(output_file);
            file << "Packet Capture Time,Send Time,Raw Timestamp,Tick Type,Symbol,Price,Size,Record Type,Flag,ASK\n";
            prl_output_file.push_back(std::move(file));
        }

        output_filenames.close();

        // Main loop to read and process packets
        while (true) {
            // Read a packet and get its timestamp
            double time_float = read_packet();
            num_packets++;

            // Check if the maximum number of packets to parse is reached or end of file is reached
            if ((max_packets_to_parse != -1 && num_packets > max_packets_to_parse) || time_float == -1) {
                // Write remaining messages to output files and close them

                for (int i = 0; i < 26; i++) {
                    trades_output_file[i] << trade_messages[i];
                    prl_output_file[i] << prl_messages[i];
                    trades_output_file[i].close();
                    prl_output_file[i].close();
                }

                // Check if end of file is reached
                if (time_float != -1) {
                    // Get the current time as the stop time for parsing
                    time_t packet_time = static_cast<time_t>(time_float);
                    cout << std::put_time(localtime(&packet_time), "%c") << ": " << num_packets << " packets processed" << endl;
                    stop_parse_time = time(nullptr);
                    cout << "Stopped parsing @ " << put_time(localtime(&stop_parse_time), "%c") << endl;
                    double parsing_time = difftime(stop_parse_time, start_parse_time);
                    cout << "Parsed in " << parsing_time << " seconds" << endl;
                    cout << "Closing all output files" << endl;
                    //close_all_files();
                }
                exit(0); // Exit the program
            }

            // Output progress every 10 million packets
            if (num_packets % 10000000 == 0) {

                for (int i = 0; i < 26; i++) {
                    trades_output_file[i] << trade_messages[i];
                    prl_output_file[i] << prl_messages[i];
                    trade_messages[i] = "";
                    prl_messages[i] = "";
                }

                // Output progress
                time_t packet_time = static_cast<time_t>(time_float);
                cout << "Parsed " << num_packets << " packets: " << put_time(localtime(&packet_time), "%c") << endl;
            }
        }
        input_file.close(); // Close the file
    }


    // Read a packet from the input file
    double read_packet() {
        // Length of the packet header in bytes
        int packet_header_len = 4 + 4 + 4 + 4;
        
        // Check if the input file is open
        if (!input_file.is_open()) {
            cerr << "Error: Unable to open file " << filename << endl;
            return 1;
        }

        char packet_header[16];
        // Read the packet header from the input file
        input_file.read(packet_header, packet_header_len);

        // Check if the end of file is reached or if the packet header is incomplete
        if (input_file.eof() || input_file.gcount() != 16) {
            cout << "End of file reached... terminating!" << endl;
            stop_parse_time = time(nullptr);
            cout << "Stopped parsing @ " << put_time(localtime(&stop_parse_time), "%c") << endl;
            double parsing_time = difftime(stop_parse_time, start_parse_time);
            cout << "Parsed in " << parsing_time << " seconds" << endl;
            //close_all_files();
            return -1;
        }

        // Unpack the pcap packet header
        PcapPacketHeader pcap_packet_header;
        unpackPcapPacketHeader(std::vector<uint8_t>(packet_header, packet_header + 16), pcap_packet_header);

        // Extract timestamp and packet length from the pcap packet header
        auto ts_sec = pcap_packet_header.ts_sec;
        auto ts_usec = pcap_packet_header.ts_usec;
        auto incl_len = pcap_packet_header.incl_len;

        // Calculate the packet timestamp in seconds
        double time_float = ts_sec + (ts_usec * 1e-6);
        uint64_t packet_capture_time_in_nanoseconds = (ts_sec * 1e9) + (ts_usec * 1e3);

        // Skip the Ethernet, IP, and UDP headers to get to the IEX payload. The total length of these headers is 42 bytes.
        int offset_into_iex_payload = 14 + 20 + 8;
        input_file.ignore(offset_into_iex_payload);
        
        // Check if the packet length is less than 42 bytes
        if (incl_len < 42) {
            cout << "Invalid packet length: " << incl_len << endl;
            return time_float;
        }
        
        vector<char> iex_payload(incl_len - 42);
        input_file.read(iex_payload.data(), incl_len - 42);

        // Parse the IEX payload
        parse_iex_payload(iex_payload, packet_capture_time_in_nanoseconds);

        return time_float;
    }

    // Parse the IEX payload to extract individual messages
    void parse_iex_payload(const std::vector<char>& payload, uint64_t packet_capture_time_in_nanoseconds) {
        // Extract the first 40 bytes of the payload
        auto start = payload.begin();
        auto end = payload.begin() + 40;
        vector<char> sliced_payload(start, end);

        uint16_t payload_len;
        uint16_t message_count;
        long long send_time;
        // Extract the fields from the IEX header
        memcpy(&send_time, &sliced_payload[32], 8);
        memcpy(&payload_len, &sliced_payload[12], 2);
        memcpy(&message_count, &sliced_payload[14], 2);

        // Check if the size of the payload matches the reported length in the header
        if (payload.size() != payload_len + 40) {
            throw runtime_error("Invalid parser state; the length of UDP packet payload should be forty plus the payload_len within IEX header");
        }

        // Extract message bytes from the payload
        const vector<char> message_bytes(payload.begin() + 40, payload.end());

        size_t cur_offset = 0;
        cur_packet_message_count = message_count;

        // Iterate through each message in the payload
        for (size_t i = 0; i < message_count; ++i) {
            // total_num_messages_processed++;
            // size_t message_id = total_num_messages_processed;

            // Extract the length of the current message
            uint16_t tuple_message_len;
            memcpy(&tuple_message_len, &message_bytes[cur_offset], sizeof(uint16_t));
            size_t message_len = tuple_message_len;

            // Extract the bytes of the current message
            vector<char> message_bytes_sliced(message_bytes.begin() + cur_offset + 2, message_bytes.begin() + cur_offset + 2 + message_len);
            // Parse the current message
            parse_iex_message(message_bytes_sliced, packet_capture_time_in_nanoseconds, send_time);

            // Move the offset to the next message
            cur_offset += 2 + message_len;
        }

        // Check if the offset matches the payload length
        if (cur_offset != payload_len) {
            throw runtime_error("Invalid parser state; cur_offset after parsing all messages within packet should be equal to IEX header reported payload_len");
        }
    }


    // Parse an IEX message from its payload
    void parse_iex_message(const std::vector<char>& message_payload, long long packet_capture_time_in_nanoseconds, long long send_time) {
        // Extract the message type byte
        char message_type_byte = message_payload[0];
        // Convert the message type byte to a string
        string message_type(1, message_type_byte);
        // Get the message ID
        // int message_id = total_num_messages_processed;

        // Process different message types
        if (message_type == "T") {
            // Parse the trade report message
            pair<string, string> parsed_message = parse_trade_report_message(message_payload);

            // Append the message string to the appropriate messages array entry
            if (symbols_of_interest_file=="ALL" || std::find(symbols_list.begin(), symbols_list.end(), parsed_message.second) != symbols_list.end())
            {

                // Construct the message string
                string message_string = to_string(packet_capture_time_in_nanoseconds) + "," + to_string(send_time) + ","  + parsed_message.first + "\n";
                trade_messages[getAlphabetOrderIndex(parsed_message.second)] += message_string;
            }

        } 
        else if (message_type == "8") {
            // For bid messages, set the bid flag to 0
            const string bid = "0";
            // Parse the price level update message
            pair<string, string> parsed_message = parse_price_level_update(message_payload);
            
            if (symbols_of_interest_file=="ALL" || std::find(symbols_list.begin(), symbols_list.end(), parsed_message.second) != symbols_list.end())
            {
                // Construct the message string
                string message_string = to_string(packet_capture_time_in_nanoseconds) + "," + to_string(send_time) + "," + parsed_message.first + "," + bid + "\n";
                prl_messages[getAlphabetOrderIndex(parsed_message.second)] += message_string;
            }
        } 
        else if (message_type == "5") {
            // For ask messages, set the ask flag to 1
            const string ask = "1";
            // Parse the price level update message
            pair<string, string> parsed_message = parse_price_level_update(message_payload);

            if (symbols_of_interest_file=="ALL" || std::find(symbols_list.begin(), symbols_list.end(), parsed_message.second) != symbols_list.end())
            {
                // Construct the message string
                string message_string = to_string(packet_capture_time_in_nanoseconds) + "," + to_string(send_time) + "," + parsed_message.first + "," + ask + "\n";

                prl_messages[getAlphabetOrderIndex(parsed_message.second)] += message_string;
            }
        } 
    }

    // Get the first part of a string before a delimiter
    string getFirstPart(const string& str, const string& delimiter) {
        size_t pos = str.find(delimiter);
        if (pos == string::npos) {
            // Return the original string if the delimiter is not found
            return str;
        }
        // Return the substring before the delimiter
        return str.substr(0, pos);
    }

    // Convert an integer to a zero-padded string
    string intToZeroPaddedString(int num) {
        // Convert integer to zero-padded string
        ostringstream oss;
        oss << setw(2) << setfill('0') << num;
        return oss.str();
    }

    // Get the alphabet order index of the first letter of a string
    int getAlphabetOrderIndex(const string& str) {
        if (!str.empty()) {
            char firstLetter = str[0];
            if (isalpha(firstLetter)) {
                // Convert the first letter to lowercase
                char lowercaseLetter = tolower(firstLetter);
                // Calculate the index in the alphabet (0 for 'a', 1 for 'b', ..., 25 for 'z')
                int index = lowercaseLetter - 'a';
                return index;
            }
        }
        // Return -1 if the string is empty or the first character is not a letter
        return -1;
    }

    vector<int> get_symbol_first_letter_indices(const vector<string>& symbols) {
        vector<int> indices;
        for (const string& symbol : symbols) {
            int index = getAlphabetOrderIndex(symbol);
            if (index != -1) {
                indices.push_back(index);
            }
        }
        return indices;
    } 

};



int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <input_pcap_file> <output.csv_file> <symbols_of_interest.txt_file>" << std::endl;
        return 1;
    }

    string iex_pcap_file_to_parse = argv[1];
    string trades_output_file_name = argv[2];
    string symbols_of_interest_file = argv[3];

    
    int max_packets_to_parse = 1000000000;
    //int max_packets_to_parse = 10000000;

    BasicPcapParser parser(iex_pcap_file_to_parse, trades_output_file_name,symbols_of_interest_file);
    
    parser.parse(max_packets_to_parse);

    cout << "Finished parsing " << iex_pcap_file_to_parse << "; closing all output files" << endl;

    return 0;
}
