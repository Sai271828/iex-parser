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
#include <thread>
#include <mutex>
#include "logger.h"
#include "decode_messages.h"
using namespace std;

class BasicPcapParser {
private:
    string filename; 
    string output_filename;
    bool write_flag;
    string symbols_of_interest_file;
    int cur_packet_message_count;
    int total_num_messages_processed;
    std::fstream symbols_file;
    string trade_messages = "";
    std::thread writerThread;
    vector<char> unparsedprl_messages;
    vector<string> timestamps;
    char raw_symbol[8];
    ofstream output_filenames;
    time_t start_parse_time;
    time_t stop_parse_time;
    string message_buffer = "";
    ifstream input_file;
    Log logger;
    mutex mtx;
    std::vector<std::string> symbols_list;
    vector<int> symbols_of_interest_indices;
    ofstream trades_output_file;
    ofstream prl_output_file;
    
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
        total_num_messages_processed = 0;
    }

    // Function to unpack the pcap packet header
    void unpackPcapPacketHeader(const std::vector<uint8_t>& buffer, PcapPacketHeader& header) {
        if (buffer.size() < sizeof(PcapPacketHeader)) {
            cerr << "Error: Insufficient data in buffer for unpacking." << endl;
            return;
        }

        memcpy(&header, buffer.data(), sizeof(PcapPacketHeader));
    }
    

    // Function to parse and write price level updates to an output file
    void prlwrite(const vector<char>& messages, ofstream& output_file, const vector<string>& timestamps) {
        string output = "";  // Initialize the output string
        std::size_t chunk_size = 30;  // Define the size of each chunk
        std::size_t data_size = messages.size();  // Get the total size of the messages

        // Process messages in chunks
        for (std::size_t i = 0; i < data_size; i += chunk_size) {
            // Determine the end of the current chunk
            std::size_t end = std::min(i + chunk_size, data_size);
            
            // Extract the current chunk from messages
            std::vector<char> chunk(messages.begin() + i, messages.begin() + end);
            
            // Parse the current chunk and append the result to the output string
            output += timestamps[i / chunk_size] + "," + parse_price_level_update(chunk).first + "\n";
        }

        // Write the output string to the output file
        output_file << output;
        

        // Reset the write flag
        write_flag = false;
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

    // Open the symbols of interest file
    symbols_file.open(symbols_of_interest_file, std::ios::in);
    if (symbols_of_interest_file == "ALL") {
        cout << "Parsing all symbols" << endl;
        symbols_list = {};
    } else if (symbols_file.is_open()) {
        // Read each line from the file and add to the symbols list
        std::string line;
        while (std::getline(symbols_file, line)) {
            symbols_list.push_back(line.substr(0, line.size() - 1)); // Remove newline character
        }
        std::cout << "Read " << symbols_list.size() << " symbols from the file.\n";
        symbols_file.close(); // Close the file
    } else {
        std::cout << "Error opening symbols of interest file";
        return -1;
    }

    // Get symbol indices
    symbols_of_interest_indices = get_symbol_first_letter_indices(symbols_list);

    // Get the current time as the start time for parsing
    start_parse_time = time(nullptr);
    cout << "Starting parsing @ " << put_time(std::localtime(&start_parse_time), "%c") << endl;
    logger.write("Started parsing");

    // Skip the pcap global header which is 24 bytes long
    int pcap_global_header_len = 24;
    input_file.ignore(pcap_global_header_len);

    int num_packets = 0;

    // Open output files for each message type
    trades_output_file.open(output_filename + "_trd.csv");
    prl_output_file.open(output_filename + "_prl.csv");

    // Write headers to the output files
    trades_output_file << "Packet Capture Time,Send Time,Exchange Timestamp,Tick Type,Symbol,Size,Price,Trade ID,Sale Condition\n";
    prl_output_file << "Packet Capture Time,Send Time, Buy_Ask Flag,Exchange Timestamp,Tick Type,Symbol,Price,Size,Record Type,Event Flag\n";

    // Main loop to read and process packets
    while (true) {
        // Read a packet and get its timestamp
        double time_float = read_packet();
        num_packets++;

        // Check if the maximum number of packets to parse is reached or end of file is reached
        if ((max_packets_to_parse != -1 && num_packets > max_packets_to_parse) || time_float == -1) {
            // Write remaining messages to output files and close them
            write_flag = true;
            std::thread writerThread([this]() {
                prlwrite(unparsedprl_messages, prl_output_file, timestamps);
            });

            trades_output_file << trade_messages;

            while (write_flag) {
                // Wait for the writer thread to complete
                cout << "Waiting for writer thread to complete" << endl;
                std::this_thread::sleep_for(std::chrono::seconds(1));
            }

            writerThread.join();
            trades_output_file.close();
            prl_output_file.close();

            // Get the current time as the stop time for parsing
            stop_parse_time = time(nullptr);
            cout << "Stopped parsing @ " << put_time(localtime(&stop_parse_time), "%c") << endl;
            double parsing_time = difftime(stop_parse_time, start_parse_time);
            cout << "Parsed in " << parsing_time << " seconds" << endl;

            exit(0); // Exit the program
        }

        // Output progress every 20 million packets
        if (num_packets % 20000000 == 0) {
            if (num_packets > 20000000) {
                while (write_flag) {
                    // Wait for the writer thread to complete
                    cout << "Waiting for writer thread to complete" << endl;
                    std::this_thread::sleep_for(std::chrono::seconds(5));
                }
            }

            vector<char> write_prl_messages = unparsedprl_messages;
            string write_trade_messages = trade_messages;
            vector<string> write_timestamps = timestamps;

            write_flag = true;
            std::thread writerThread([this, write_prl_messages, write_timestamps]() {
                prlwrite(write_prl_messages, prl_output_file, write_timestamps);
            });
            writerThread.detach();

            trades_output_file << trade_messages;

            trade_messages = "";
            unparsedprl_messages.clear();
            timestamps.clear();

            // Output progress
            cout << "Parsed " << num_packets << " packets " << endl;
        }
    }

    input_file.close(); // Close the file
}


    // Read a packet from the input file
double read_packet() {
    // Length of the packet header in bytes
    int packet_header_len = 16; // 4 + 4 + 4 + 4

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
        cout << "End of file reached... stopping reading!" << endl;
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
    int offset_into_iex_payload = 42; // 14 + 20 + 8
    input_file.ignore(offset_into_iex_payload);

    // Check if the packet length is less than 42 bytes
    if (incl_len < 42) {
        cout << "Invalid packet length: " << incl_len << endl;
        return time_float;
    }

    // Read the IEX payload
    vector<char> iex_payload(incl_len - 42);
    input_file.read(iex_payload.data(), incl_len - 42);

    // Parse the IEX payload
    auto start = iex_payload.begin();
    auto end = iex_payload.begin() + 40;
    vector<char> sliced_payload(start, end);

    uint16_t payload_len;
    uint16_t message_count;
    long long send_time;

    // Extract the fields from the IEX header
    memcpy(&send_time, &sliced_payload[32], 8);
    memcpy(&payload_len, &sliced_payload[12], 2);
    memcpy(&message_count, &sliced_payload[14], 2);

    // Check if the size of the payload matches the reported length in the header
    if (iex_payload.size() != payload_len + 40) {
        throw runtime_error("Invalid parser state; the length of UDP packet payload should be forty plus the payload_len within IEX header");
    }

    // Extract message bytes from the payload
    const vector<char> message_bytes(iex_payload.begin() + 40, iex_payload.end());

    size_t cur_offset = 0;
    cur_packet_message_count = message_count;

    // Iterate through each message in the payload
    for (size_t i = 0; i < message_count; ++i) {
        total_num_messages_processed++;

        // Extract the length of the current message
        uint16_t tuple_message_len;
        memcpy(&tuple_message_len, &message_bytes[cur_offset], sizeof(uint16_t));
        size_t message_len = tuple_message_len;

        // Extract the bytes of the current message
        vector<char> message_bytes_sliced(message_bytes.begin() + cur_offset + 2, message_bytes.begin() + cur_offset + 2 + message_len);
        char message_type_byte = message_bytes_sliced[0];
        string message_type(1, message_type_byte);

        // Process different message types
        if (message_type == "T") {
            // Parse the trade report message
            pair<string, string> parsed_message = parse_trade_report_message(message_bytes_sliced);

            // Append the message string to the appropriate messages array entry
            if (symbols_of_interest_file == "ALL" || std::find(symbols_list.begin(), symbols_list.end(), parsed_message.second) != symbols_list.end()) {
                string message_string = to_string(packet_capture_time_in_nanoseconds) + "," + to_string(send_time) + "," + parsed_message.first + "\n";
                trade_messages += message_string;
            }

        } else if (message_type == "8") {
            // For bid messages, set the bid flag to 0
            const string bid = "0";

            // Parse the price level update message
            memcpy(raw_symbol, &message_bytes_sliced[10], sizeof(raw_symbol));
            string symbol(raw_symbol, 8);
            symbol = symbol.substr(0, symbol.find(' '));

            if (symbols_of_interest_file == "ALL" || std::find(symbols_list.begin(), symbols_list.end(), symbol) != symbols_list.end()) {
                string timestamps_string = to_string(packet_capture_time_in_nanoseconds) + "," + to_string(send_time) + "," + bid;
                timestamps.push_back(timestamps_string);
                unparsedprl_messages.insert(unparsedprl_messages.end(), message_bytes_sliced.begin(), message_bytes_sliced.end());
            }
        } else if (message_type == "5") {
            // For ask messages, set the ask flag to 1
            const string ask = "1";

            // Parse the price level update message
            memcpy(raw_symbol, &message_bytes_sliced[10], sizeof(raw_symbol));
            string symbol(raw_symbol, 8);
            symbol = symbol.substr(0, symbol.find(' '));

            if (symbols_of_interest_file == "ALL" || std::find(symbols_list.begin(), symbols_list.end(), symbol) != symbols_list.end()) {
                string timestamps_string = to_string(packet_capture_time_in_nanoseconds) + "," + to_string(send_time) + "," + ask;
                timestamps.push_back(timestamps_string);
                unparsedprl_messages.insert(unparsedprl_messages.end(), message_bytes_sliced.begin(), message_bytes_sliced.end());
            }
        }

        // Move the offset to the next message
        cur_offset += 2 + message_len;
    }

    // Check if the offset matches the payload length
    if (cur_offset != payload_len) {
        throw runtime_error("Invalid parser state; cur_offset after parsing all messages within packet should be equal to IEX header reported payload_len");
    }

    return time_float;
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

    
    int max_packets_to_parse = 150000000;
    //int max_packets_to_parse = 10000000;

    BasicPcapParser parser(iex_pcap_file_to_parse, trades_output_file_name,symbols_of_interest_file);
    
    parser.parse(max_packets_to_parse);

    cout << "Finished parsing " << iex_pcap_file_to_parse << "; closing all output files" << endl;
    
    //parser.close_all_files();

    return 0;
}
