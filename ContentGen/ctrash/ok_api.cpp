#include <thread>
#include <chrono>
#include <nlohmann/json.hpp>
#include <string>
#include "busme.cpp"

    void runDaemon() {
        while (true) {
            Server();
            std::this_thread::sleep_for(std::chrono::seconds(5)); // Sleep for 10 seconds
        }
    }

    int main(int argc, char const *argv[]) {
        std::thread daemonThread(runDaemon);
        daemonThread.detach(); // Detach the thread to run independently
        while (true) {
            std::this_thread::sleep_for(std::chrono::seconds(1)); // Sleep for 1 second
            printf("Main thread is running\n");
            printf("Send a message [Service]Message:\n");
            std::string message;
            std::cin >> message;
            nlohmann::json data;
            data["message"] = message;
            Client(data, "MAIN");


        }

        return 0;
    }

