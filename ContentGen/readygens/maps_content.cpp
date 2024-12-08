#include <iostream>
#include <vector>
#include <string>

struct element
{   char elementletter;
    std::string elementname;
    bool colides=false;
    bool issteppable=false;
    bool isvisible=false;
    std::string description = " ";
};


class map
{
private:
    const int width;
    const int height;
    std::vector<std::vector<char>> mapdist;
    std::vector<std::vector<int[2]>> playerpos;
    std::vector<element> mapelements;
public:
    map(int width, int height) : width(width), height(height)
    {
        mapdist = std::vector<std::vector<char>>(height, std::vector<char>(width, ' '));
    }
    void defineelement(char elementletter, std::string elementname, bool colides, bool issteppable, bool isvisible, std::string description)
    {
        element newelement;
        newelement.elementletter = elementletter;
        newelement.elementname = elementname;
        newelement.colides = colides;
        newelement.issteppable = issteppable;
        newelement.isvisible = isvisible;
        newelement.description = description;
        mapelements.push_back(newelement);
    }
    void defineelement(char elementletter, std::string elementname, bool colides, bool issteppable, bool isvisible)
    {
        element newelement;
        newelement.elementletter = elementletter;
        newelement.elementname = elementname;
        newelement.colides = colides;
        newelement.issteppable = issteppable;
        newelement.isvisible = isvisible;
        mapelements.push_back(newelement);
    }
    void setelement(int x, int y, char elementletter)
    {
        mapdist[y][x] = elementletter;
    }
    void printmap()
    {
        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {
                std::cout << mapdist[i][j];
            }
            std::cout << std::endl;
        }
    }
    void printelementinfo(char elementletter)
    {
        for (int i = 0; i < mapelements.size(); i++)
        {
            if (mapelements[i].elementletter == elementletter)
            {
                std::cout << "Element name: " << mapelements[i].elementname << std::endl;
                std::cout << "Element description: " << mapelements[i].description << std::endl;
                return;
            }
        }
        std::cout << "Element not found" << std::endl;
    }
    void printelements()
    {
        for (int i = 0; i < mapelements.size(); i++)
        {
            std::cout << "Element name: " << mapelements[i].elementname << std::endl;
            std::cout << "Element description: " << mapelements[i].description << std::endl;
        }
    }
    element getelements(char elementletter)
    {
        for (int i = 0; i < mapelements.size(); i++)
        {
            if (mapelements[i].elementletter == elementletter)
            {
                return mapelements[i];
            }
        }
        element notfound;
        notfound.elementletter = ' ';
        return notfound;
    }
    element getelements(int index)
    {
        return mapelements[index];
    }
    element getelements(std::string elementname)
    {
        for (int i = 0; i < mapelements.size(); i++)
        {
            if (mapelements[i].elementname == elementname)
            {
                return mapelements[i];
            }
        }
        element notfound;
        notfound.elementletter = ' ';
        return notfound;
    }
    std::vector<element> getelements(){
        return mapelements;
    }
    int getwidth(){
        return width;
    }
    int getheight(){
        return height;
    }
    std::vector<std::vector<char>> getmapdist(){
        return mapdist;
    }
    void setmapdist(std::vector<std::vector<char>> mapdist){
        this->mapdist = mapdist;
    }
    std::vector<element> getmapelements(){
        return mapelements;
    }
    void setmapelements(std::vector<element> mapelements){
        this->mapelements = mapelements;
    }
    
};

int main(int argc, char const *argv[])
{   if (argc == 1) {
        map mymap(2, 2);
        mymap.defineelement(' ', "Empty space", false, true, false);
        mymap.defineelement('X', "Wall", true, false, false);
        mymap.defineelement('F', "Floor", false, true, false);
        mymap.setelement(0, 0, 'X');
        mymap.setelement(0, 1, 'F');
        mymap.setelement(1, 0, 'X');
        mymap.setelement(1, 1, 'F');
        mymap.printmap();
    } else {
       if (argv[1] == "Game"){

        printf("Define map Width: ");
        int width;
        std::cin >> width;
        printf("Define map Height: ");
        int height;
        std::cin >> height;
        map mymap(width, height);
        char choice = ' ';
        while (choice !='q')
        {
            printf("1. Define element\n");
            printf("2. Set element\n");
            printf("3. Edit elements\n");
            printf("4. Print elements\n");
            printf("5. Print element info\n");
            printf("6. Set map elements\n");
            printf("7. Print map\n");
            printf("q. Quit\n");
            std::cin >> choice;
            switch (choice){
            case '1':
                {
                    system("clear");
                    printf("Define element letter: ");
                    char elementletter;
                    std::cin >> elementletter;
                    printf("Define element name: ");
                    std::string elementname;
                    std::cin >> elementname;
                    printf("Define a 0 or 1 no x position depending of the case \n");
                    printf("Position 1: Does the element colide? \n");
                    printf("Position 2: Is the element steppable? \n");
                    printf("Position 3: Is the element visible? \n");
                    printf("Example: 101 \n");
                    int properties;
                    std::cin >> properties;
                    bool colides = properties / 100;
                    bool issteppable = (properties % 100) / 10;
                    bool isvisible = properties % 10;
                    printf("Now some lore, define element description: ");
                    std::string description;
                    std::cin >> description;
                    mymap.defineelement(elementletter, elementname, colides, issteppable, isvisible, description);
                    break;
                }
            case '2':
                {
                    system("clear");
                    printf("Define position (press enter when number is ready) \n");
                    int pos[2];
                    printf("X: ");
                    std::cin >> pos[0];
                    printf("Y: ");
                    std::cin >> pos[1];
                    system("clear");
                    printf("Elements Available: \n");
                    mymap.printelements();
                    printf("Define element letter: ");
                    char elementletter;
                    std::cin >> elementletter;
                    mymap.setelement(pos[0], pos[1], elementletter);
                    break;
                }
            case '3':
                {
                    system("clear");
                    printf("1. Edit element\n");
                    printf("2. Delete element\n");
                    char choice2;
                    std::cin >> choice2;
                    switch (choice2){
                    case '1':
                        {
                            system("clear");
                            printf("Define element letter: ");
                            char elementletter;
                            std::cin >> elementletter;
                            printf("Define element name: ");
                            std::string elementname;
                            std::cin >> elementname;
                            printf("Define a 0 or 1 no x position depending of the case \n");
                            printf("Position 1: Does the element colide? \n");
                            printf("Position 2: Is the element steppable? \n");
                            printf("Position 3: Is the element visible? \n");
                            printf("Example: 101 \n");
                            int properties;
                            std::cin >> properties;
                            bool colides = properties / 100;
                            bool issteppable = (properties % 100) / 10;
                            bool isvisible = properties % 10;
                            printf("Now some lore, define element description: ");
                            std::string description;
                            std::cin >> description;
                            for (int i = 0; i < mymap.getmapelements().size(); i++)
                            {
                                if (mymap.getmapelements()[i].elementletter == elementletter)
                                {
                                    mymap.getmapelements()[i].elementname = elementname;
                                    mymap.getmapelements()[i].colides = colides;
                                    mymap.getmapelements()[i].issteppable = issteppable;
                                    mymap.getmapelements()[i].isvisible = isvisible;
                                    mymap.getmapelements()[i].description = description;
                                    break;
                                }
                            }
                            break;
                        }
                    case '2':
                        {
                            system("clear");
                            printf("Define element letter: ");
                            char elementletter;
                            std::cin >> elementletter;
                            for (int i = 0; i < mymap.getmapelements().size(); i++)
                            {
                                if (mymap.getmapelements()[i].elementletter == elementletter)
                                {
                                    mymap.getmapelements().erase(mymap.getmapelements().begin() + i);
                                    break;
                
                                }

                            }
                            break;
                        }

       
                    }
                }
            case '4':
                {
                    system("clear");
                    mymap.printelements();
                    break;
                }
            case '5':
                {
                    system("clear");
                    printf("Define element letter: ");
                    char elementletter;
                    std::cin >> elementletter;
                    mymap.printelementinfo(elementletter);
                    break;
                }
            case '6':
                {
                    system("clear");
                    printf("Define element pos \n X:");
                    int x;
                    std::cin >> x;
                    printf(" Y:");
                    int y;
                    std::cin >> y;
                    printf("Define element letter: ");
                    char elementletter;
                    std::cin >> elementletter;
                    mymap.setelement(x, y, elementletter);
                    break;
                }
            case '7':
                {
                    system("clear");
                    mymap.printmap();
                    break;
                }
            }
        }

       }
    }
    return 0;
}


