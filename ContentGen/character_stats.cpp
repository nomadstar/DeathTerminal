#include <string>
#include <iostream>
#include <vector>
#include <nlohmann/json.hpp>

#include <algorithm>
#include <iterator>

struct effect{
    std::string name;
    std::string description;
    std::string effect; // DamageBoost, HealthBoost, HealthLost, QuickRecovery...
    std::string affects; // Self, Target, Enemy, Ally, All
    int duration;
    int type[2]; // {Element Source, Kind of effect}
    float power; // percentage of power
    bool isactive = false;
};
struct perks
{   std::string name;
    std::string description;
    int level;
    std::vector<effect> effects;
};
class character
{       
private:
    //-- Atributos Basicos
    std::string name;
    char sexualidad[2]; // {Sexo, Orientación sexual}
    std::string rol;
    // -- Atributos de habilidad - combate
    std::vector<perks> perks; // {Nombre, Descripcion, Nivel, Efectos}
    std::vector<effect> effectStatus; // {Nombre, Descripcion, Efectos, Duracion, Tipo, Potencia, Activo}
    // -- Propiedades fisicas
    int health[2];// 1. Salud 2. Salud maxima
    int mana[2];// 1. Mana 2. Mana maximo
    int stamina[2];// 1. Stamina 2. Stamina maxima
    int level;
    bool incombat = false;
    // -- Propiedades de movimiento y carga
    int maxcarryweight; // Peso maximo que puede cargar
    std::vector<int[2]> items; // {Numeros negativos items de combate, Numeros positivos items de interacción, peso}

public:
    // -- Constructores
    character(nlohmann::json data){
        name = data["name"];
        rol = data["rol"];
        sexualidad[0] = data["sexualidad"].get<std::string>()[0];
        sexualidad[1] = data["atraccion"].get<std::string>()[1];
        level = data["level"];
        health[0] = data["health"][0];
        health[1] = data["max_health"][1];
        mana[0] = data["mana"][0];
        mana[1] = data["max_mana"][1];
        stamina[0] = data["stamina"][0];
        stamina[1] = data["max_stamina"][1];
        maxcarryweight = data["maxcarryweight"];   
    }
    // -- Metodos
    std::string getname(){
        return name;
    }
    std::string getrol(){
        return rol;
    }
    char getsexo(int property){
        if (property < 1 || property > 2) throw std::out_of_range("Property index out of range");
        return sexualidad[property];
    }
    int getlevel(){
        return level;
    }
    void setsexo(char value, int property){
        sexualidad[property] = value;
    }
    void setlevel(int value){
        level = value;
    }
    // -- Metodos de propiedades fisicas (1. Actual 2. Maxima)
    int gethealth(int property){
        if (property < 1 || property > 2) throw std::out_of_range("Property index out of range");
        return health[property];
    }
    int getmana(int property){
        if (property < 1 || property > 2) throw std::out_of_range("Property index out of range");
        return mana[property];
    }
    int getstamina(int property){
        if (property < 1 || property > 2) throw std::out_of_range("Property index out of range");
        return stamina[property];
    }
    
    // Retorna un string que describe el estado de la propiedad fisica sin decir el resultado exacto (1. Salud 2. Mana 3. Stamina)
    std::string seestatus(int property){
        if (property < 1 || property > 3) return "Propiedad no encontrada";
        float percentege;
        if(property==1){
            percentege = (static_cast<float>(health[0]) / health[1]) * 100;
            switch(static_cast<int>(percentege) / 10) {
                case 10:
                case 9:
                return "Excelente";
                case 8:
                case 7:
                return "Normal";
                case 6:
                case 5:
                return "Dañado";
                case 4:
                case 3:
                return "Herido";
                case 2:
                case 1:
                return "Agónico";
                case 0:
                return "Delirante";
                default:
                return "Estado desconocido";
            }
        }
        if (property==2){
            percentege = (static_cast<float>(mana[0]) / mana[1]) * 100;
            switch(static_cast<int>(percentege) / 10) {
                case 10:
                case 9:
                return "Poderoso";
                case 8:
                case 7:
                return "Con energia";
                case 6:
                case 5:
                return "Normal";
                case 4:
                case 3:
                return "Sudadado";
                case 2:
                case 1:
                return "Cansado";
                case 0:
                return "Sin Magia";
                default:
                return "Estado desconocido";
            }
        }
        if (property==3)
        {   
            percentege = (static_cast<float>(stamina[0]) / stamina[1]) * 100;
            switch(static_cast<int>(percentege) / 10) {
                case 10:
                case 9:
                return "Energico";
                case 8:
                case 7:
                return "Con fuerza";
                case 6:
                case 5:
                return "Normal";
                case 4:
                case 3:
                return "Cansado";
                case 2:
                case 1:
                return "Agotado";
                case 0:
                return "Exhausto";
                default:
                return "Estado desconocido";
            }
            
        } 
    }
    
       
    // usa puntos cardinales para moverse (N = Norte, S = Sur, E = Este, W = Oeste)
  
    int getmaxcarryweight(){
        return maxcarryweight;
    }
    std::vector<int[2]> getitems(){
        return items;
    }
    int getweight(){
        int weight = 0;
        int totalitems = items.size();
        for (int i = 0; i < totalitems; i++)
        {   weight += items[i][1];
        }
        return weight;
    }
    void additem(int item, int weight){
        int totalitems = items.size();
        if (getweight() + weight > maxcarryweight) throw std::runtime_error("No puedes cargar mas peso");
        items.push_back({item,weight});
    }
    void removeitem(int item, int weight){
        for (int i = 0; i < items.size(); i++)
        if (items[i][0] == item && items[i][1] == weight){items.erase(items.begin() + i); return;}
        throw std::runtime_error("Item no encontrado");  
    };
    void modproperty(int property, int value){
        if (property < 1 || property > 3) throw std::out_of_range("Property index out of range");
        if (property == 1) health[0] += value;
        if (property == 2) mana[0] += value;
        if (property == 3) stamina[0] += value;
    }
    void setproperty(int property, int value){
        if (property < 1 || property > 3) throw std::out_of_range("Property index out of range");
        if (property == 1) health[0] = value;
        if (property == 2) mana[0] = value;
        if (property == 3) stamina[0] = value;
    }
    void setmaxproperty(int property, int value){
        if (property < 1 || property > 3) throw std::out_of_range("Property index out of range");
        if (property == 1) health[1] = value;
        if (property == 2) mana[1] = value;
        if (property == 3) stamina[1] = value;
    }
    void levelup(int values[3]){
        level++;
        setmaxproperty(1,values[0]);
        setmaxproperty(2,values[1]);
        setmaxproperty(3,values[2]);
        setproperty(1,values[0]);
        setproperty(2,values[1]);
        setproperty(3,values[2]);
    }
    void setincombat(bool value){
        incombat = value;
    }
    bool getincombat(){
        return incombat;
    }
    void addperk(nlohmann::json data){
        struct perks newperk;
        newperk.name = data["name"];
        newperk.description = data["description"];
        newperk.level = data["level"];
        for (int i = 0; i < data["effects"].size(); i++)
        {
            struct effect neweffect;
            neweffect.name = data["effects"][i]["name"];
            neweffect.description = data["effects"][i]["description"];
            neweffect.duration = data["effects"][i]["duration"];
            neweffect.type[0] = data["effects"][i]["type"][0];
            neweffect.type[1] = data["effects"][i]["type"][1];
            neweffect.power = data["effects"][i]["power"];
            newperk.effects.push_back(neweffect);
        }
        perks.push_back(newperk);
    };
    void removeperk(std::string name){
        for (int i = 0; i < perks.size(); i++)
        if (perks[i].name == name){perks.erase(perks.begin() + i); return;}
        throw std::runtime_error("Perk no encontrado");
    };
    void addstatus(nlohmann::json data){
        struct effect neweffect;
        neweffect.name = data["name"];
        neweffect.description = data["description"];
        neweffect.duration = data["duration"];
        neweffect.type[0] = data["type"][0];
        neweffect.type[1] = data["type"][1];
        neweffect.power = data["power"];
        neweffect.isactive = true;
        effectStatus.push_back(neweffect);
    };
    void removestatus(std::string name){
        for (int i = 0; i < effectStatus.size(); i++)
        if (effectStatus[i].name == name){effectStatus.erase(effectStatus.begin() + i); return;}
        throw std::runtime_error("Status no encontrado");
    };
    void setefectactive(std::string name, bool value){
        for (int i = 0; i < effectStatus.size(); i++)
        if (effectStatus[i].name == name){effectStatus[i].isactive = value; return;}
        throw std::runtime_error("Status no encontrado");
    };
    std::vector<effect> geteffectsbytype(std::string type){
        std::vector<effect> activeeffects;
        for (int i = 0; i < effectStatus.size(); i++)
        if (effectStatus[i].effect == type) activeeffects.push_back(effectStatus[i]);
        for (int i = 0; i < perks.size(); i++)
        for (int j = 0; j < perks[i].effects.size(); j++)
        if (perks[i].effects[j].effect == type) activeeffects.push_back(perks[i].effects[j]);
        return activeeffects;
    };
        

};
class npc : public character
{
private:
    character self;
    std::string description;
     // -- Atributos Sociales
    uint32_t status; // 0.Muerto 1. Agresivo 2. Amigable 3. Neutral 4. Hostil 5. Amistoso 6. Enemigo 7. Aliado 8. Neutral 9. Indiferente 10. Amable 11. Desconfiado 12. Confiable 13. Inseguro 14. Valiente 15. Cobarde 16. Astuto 17. Tonto 18. Honesto 19. Mentiroso 20. Leal 21. Traicionero 22. Justo 23. Injusto 24. Bueno 25. Malvado 26. Neutral 27. Legal 28. Ilegal 29. Ordenado 30. Caotico 31. Pacifista 32. Violento 33. Aventurero 
    std::string actual_emotion;
    std::vector<std::string,int> familia; // {Nombre del NPC o jugador, parentesco}
    std::vector <std::string,uint8_t> afinidad; // {Nombre del NPC o jugador, porcentaje de afinidad}  0-10 Enemigo 11-25 Rival 25-30 No confiable - Renegado 31-40 Neutral 41-50 Conocido 51-60 Amistoso 61-70 Amigo 71-80 Buen amigo  81-85 Mejor amigo -Familiar Lejano 86-90 Pareja - Familiar 91-100 Familiar - Conyuge - Hermano - Padre - Hijo
    std::vector<int[2]> actions; // {Numeros positivos asociados a interacciones no agresivas y numeros negativos a interacciones de combate, porcentaje de exito}

    // -- Atributos de habilidad - combate
     int attackspeed[2]; // Entre cuanto tiempo puede atacar {minimo, maximo} 
public:
    std::string getdes(std::string property){
        if (property == "description") return description;
        return "Propiedad no encontrada";
    }
    uint32_t getstatus(){
        return status;
    }
    std::string getemotion(){
        return actual_emotion;
    }
    std::vector<std::string,int> getfamilia(){
        return familia;
    }
    std::vector <std::string,uint8_t> getafinidad(){
        return afinidad;
    }
    std::vector<int[2]> getactions(){
        return actions;
    }
    int getattackspeed(int property){
        if (property < 1 || property > 2) throw std::out_of_range("Property index out of range");
        return attackspeed[property];
    }
    void setdes(std::string value){
        description = value;
    }
    void setstatus(uint32_t value){
        status = value;
    }
    void nowdead(){
        status = 0;
    }
    void setemotion(std::string value){
        actual_emotion = value;
    }
    void setfamilia(std::string name, int parentesco){
        familia.push_back({name,parentesco});
    }
    void setafinidad(std::string name, uint8_t porcentaje){
        afinidad.push_back({name,porcentaje});
    }
    void changeafinidad(std::string name, uint8_t porcentaje){
        for (int i = 0; i < afinidad.size(); i++)
        if (afinidad[i] == name){afinidad[i][1] = porcentaje; return;}
        throw std::runtime_error("No se encontro el NPC o jugador");
    }
    void actionlearned(int action, int porcentaje){
        actions.push_back({action,porcentaje});
    }
    void actionforgotten(int action){
        for (int i = 0; i < actions.size(); i++)
        if (actions[i][0] == action){actions.erase(actions.begin() + i); return;}
        throw std::runtime_error("No se encontro la accion");
    }
    void setattackspeed(int value, int property){
        if (property < 1 || property > 2) throw std::out_of_range("Property index out of range");
        attackspeed[property] = value;
    }
    
};