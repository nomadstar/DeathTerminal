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

        // Main thread can perform other tasks or just wait
        while (true) {
            std::this_thread::sleep_for(std::chrono::seconds(1)); // Sleep for 1 second
        }

        return 0;
    }

