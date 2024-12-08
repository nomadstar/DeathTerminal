
#include <thread>
#include <chrono>
#include <nlohmann/json.hpp>
#include <string>
#include "busme.cpp"





void makechoice(std::string json_string){
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
/*struct DataStructureRecieveBUS
{
    unsigned int busmessagelenght : 17;
    char source[5];
    char solstatus[2];
    char msg[99997];
};*/
DataStructureRecieveBUS interpeter(std::string message){
    if (sizeof(message) > 100000) {
        std::cerr << "Message is too long" << std::endl;
        return;
    }
    DataStructureRecieveBUS data;
    // Extract busmessagelenght
    data.busmessagelenght = std::stoi(message.substr(0, 17));

    // Extract source
    std::strncpy(data.source, message.substr(17, 5).c_str(), 5);
    data.source[4] = '\0'; // Ensure null-termination

    // Extract solstatus
    std::strncpy(data.solstatus, message.substr(22, 2).c_str(), 2);
    data.solstatus[1] = '\0'; // Ensure null-termination

    // Extract msg
    std::strncpy(data.msg, message.substr(24).c_str(), sizeof(data.msg) - 1);
    data.msg[sizeof(data.msg) - 1] = '\0'; // Ensure null-termination

    return data;
}
int main(int argc, char const *argv[])
{   
     
     
    }
     

