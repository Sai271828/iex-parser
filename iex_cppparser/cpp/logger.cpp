#include "logger.h"
#include <fstream>
#include <iostream>
#include <ctime>

void Log::write(const std::string& message) {
    std::ofstream file("/vagrant/logfile.log", std::ios_base::app);
    if (file.is_open()) {
        std::time_t now = std::time(nullptr);
        file << std::ctime(&now) << " - " << message << "\n";
        file.close();
    } else {
        std::cerr << "Unable to open file\n";
    }
}
