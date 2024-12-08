#include <iostream>
#include <boost/asio.hpp>
#include <nlohmann/json.hpp>





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
 
int ip[4]={};
int portin = 0;
int portout = 0;

const boost::asio::ip::udp::endpoint SERVER_ENDPOINT(
    boost::asio::ip::address::from_string(std::to_string(ip[0]) + "." + std::to_string(ip[1]) + "." + std::to_string(ip[2]) + "." + std::to_string(ip[3])),  // IP address
    portin  // Port number
);

void Server(){
    using namespace boost::asio;
    io_context ctx;
    ip::udp::socket socket(ctx, SERVER_ENDPOINT);
    char data[9999];
    socket.async_receive(buffer(data,9999),[&](std::error_code ec, std::size_t bytes_recvd){
        if(!ec){
            std::cout << "Received: " << data << std::endl;
        }
        else{
            std::cerr << "Error: " << ec.message() << std::endl;
        }
    });
    
    ctx.run();
};

void Client(){
    using namespace boost::asio;
    io_context ctx;
    ip::udp::socket cltsocket(ctx, ip::udp::endpoint(ip::udp::v4(), portout));
    DataStructureSentoBUS data = builder(nlohmann::json::parse("{\"msg\":\"Hello Bus!\"}"), "BUS");
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