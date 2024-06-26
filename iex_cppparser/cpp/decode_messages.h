#ifndef PARSER_H
#define PARSER_H

#include <vector>
#include <string>
#include <utility> // For std::pair

using namespace std;

pair<string, string> parse_trade_report_message(const vector<char>& payload);
string convert_trade_sale_condition_to_string(char sale_condition_flags);
pair<string, string> parse_price_level_update(const vector<char>& payload) ;
#endif // PARSER_H
