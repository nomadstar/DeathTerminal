#include <iostream>
#include <boost/asio.hpp>
#include <nlohmann/json.hpp>


 
unsigned int ip[4]={0,0,0,0}; //ip adress
unsigned int port[2] = {0,0}; //port in and out


struct DataStructureSentoBUS
{
    unsigned int busmessagelenght : 17;
    char desitnation[5];
    char msg[99999];

};

struct DataStructureRecieveBUS
{
    unsigned int busmessagelenght : 17;
    char source[5];
    char solstatus[2];
    char msg[99997];
};

DataStructureRecieveBUS builder(char data[99999]){
    DataStructureRecieveBUS datastruct;
    char breakchar[5] = {data[0], data[1], data[2], data[3], data[4]};
    try
    {   datastruct.busmessagelenght = std::stoi(std::string(breakchar, 5));
        for (int i = 5; i < datastruct.busmessagelenght; i++) {
            if (i<5) {data[i]=datastruct.source[i];}
            else if (i<7) {data[i]=datastruct.solstatus[i];}
            else {data[i]=datastruct.msg[i];}
        }
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
    }
    return datastruct;   
};

 bool validateData(DataStructureSentoBUS data)
 {  
    for (int i = 0; i < sizeof(data.msg); i++) if (data.msg[i] == '\0' && i == data.busmessagelenght) break; else return false;
    return data.busmessagelenght<10000 ? true : false;
 };

 bool validateData(const nlohmann::json& data)
 {  // parse data to a char array
    std::string dataString = data.dump();
    //check if lengh is less than 10000
    return dataString.length() < 10000 ? true : false;
 };

DataStructureSentoBUS builder(const nlohmann::json& jsonData, char destination[5]){   
    try
{   if(!validateData(jsonData)) throw std::runtime_error("Data is too long");
    DataStructureSentoBUS data;
    std::string dataString = jsonData.dump();
    data.busmessagelenght = dataString.length();
    data.desitnation[5] = *destination;
    data.msg[data.busmessagelenght] = *dataString.c_str();
    return validateData(data) ? data : throw std::runtime_error("Somemthing seems odd: Perhaps the data is too long or buslenght != data.lenght");
}
catch(const std::exception& e)
{
    std::cerr << e.what() << '\n';
}
};

//web part


const boost::asio::ip::udp::endpoint SERVER_ENDPOINT(
    boost::asio::ip::address::from_string(std::to_string(ip[0]) + "." + std::to_string(ip[1]) + "." + std::to_string(ip[2]) + "." + std::to_string(ip[3])),  // IP address
    port[0]  // Port number
);

DataStructureRecieveBUS Server(){
    using namespace boost::asio;
    io_context ctx;
    ip::udp::socket socket(ctx, SERVER_ENDPOINT);
    char data[9999];
    socket.async_receive(buffer(data,9999),[&](std::error_code ec, std::size_t bytes_recvd){
        if(!ec){
            std::cout << "Received: " << data << std::endl;
            return builder(data);
        }
        else{
            std::cerr << "Error: " << ec.message() << std::endl;
        }
    });
    ctx.run();
};

void Client(DataStructureSentoBUS data){
    if(!validateData(data)) throw std::runtime_error("Data is too long");
    using namespace boost::asio;
    io_context ctx;
    ip::udp::socket cltsocket(ctx, ip::udp::endpoint(ip::udp::v4(), port[1]));
    cltsocket.async_send_to(buffer(data.msg, data.busmessagelenght), SERVER_ENDPOINT, [&](std::error_code ec, std::size_t bytes_sent){
        if(!ec){
            std::cout << "Sent " << bytes_sent << " bytes" << std::endl;
        }
        else{
            std::cerr << "Error: " << ec.message() << std::endl;
        }
    });
    ctx.run();
};

void Client(nlohmann::json data, char destination[5]){
    DataStructureSentoBUS datastruct = builder(data, destination);
    if(!validateData(datastruct)) throw std::runtime_error("Data is too long");
    using namespace boost::asio;
    io_context ctx;
    ip::udp::socket cltsocket(ctx, ip::udp::endpoint(ip::udp::v4(), port[1]));
    cltsocket.async_send_to(buffer(datastruct.msg, datastruct.busmessagelenght), SERVER_ENDPOINT, [&](std::error_code ec, std::size_t bytes_sent){
        if(!ec){
            std::cout << "Sent " << bytes_sent << " bytes" << std::endl;
        }
        else{
            std::cerr << "Error: " << ec.message() << std::endl;
        }
    });
    ctx.run();
};



