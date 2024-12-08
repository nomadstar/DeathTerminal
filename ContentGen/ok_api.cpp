#include <iostream>
#include <thread>
#include <chrono>
#include <nlohmann/json.hpp>

void makechoice(){
 std::string json_string;
    nlohmann::json json_data;

    while (true) {
        std::cout << "Waiting for JSON input: ";
        std::getline(std::cin, json_string);

        try {
            json_data = nlohmann::json::parse(json_string);
            break; // Exit loop if JSON is successfully parsed
        } catch (nlohmann::json::parse_error& e) {
            std::cerr << "Invalid JSON: " << e.what() << std::endl;
        }
    }
    std::thread json_thread([&]() {
        while (true) {
            std::cout << "Waiting for JSON input: ";
            std::getline(std::cin, json_string);

            try {
                json_data = nlohmann::json::parse(json_string);
                std::cout << "Received valid JSON: " << json_data.dump() << std::endl;

                // Process the JSON data
                if (json_data.contains("mode")) {
                    std::string mode = json_data["mode"];

                    if (mode == "M") { // Stands for Manual mode
                        execlp("ContentGen/readygens/maps_content.cpp", "ContentGen/readygens/maps_content.cpp", "Game", NULL);
                    } else {
                        std::cerr << "Unknown mode: " << mode << std::endl;
                    }
                } else {
                    std::cerr << "JSON does not contain 'mode' key." << std::endl;
                }
            } catch (nlohmann::json::parse_error& e) {
                std::cerr << "Invalid JSON: " << e.what() << std::endl;
            }
        }
    });

    json_thread.detach();

    // Keep the main thread alive
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
};

int main(int argc, char const *argv[])
{   
   
}
