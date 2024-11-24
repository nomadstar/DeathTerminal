#include <iostream>
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

 
