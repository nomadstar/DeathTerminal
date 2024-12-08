#include <iostream>
#include <conio.h>

struct position{
        int x;
        int y;
    };
position move(position pos, char direction){
    switch (direction)
    {
    case 'N':
        pos.y++;
        return pos;
    case 'S':
        pos.y--;
        return pos;
    case 'E':
        pos.x++;
        return pos;
    case 'W':
        pos.x--;
        return pos;
    default:
        return pos;
    }
    }
char wasdadapter(char input){
    switch (input)
    {
    case 'w':
    case 'W':
        return 'N';
    case 'a':
    case 'A':
        return 'W';
    case 's':
    case 'S':
        return 'S';
    case 'd':
    case 'D':
        return 'E';
    default:
        return ' ';
    }


}
void setposition(position pos, int x, int y){
        pos.x = x;
        pos.y = y;
    }

int main(int argc, char const *argv[]){
    if (argv[1] == "Test")
    {
    position pos;
    pos.x = 0;
    pos.y = 0;
    std::cout << "Position: " << pos.x << ", " << pos.y << std::endl;
    while (true)
    {
    char input;
    if (kbhit()) {
        input = _getch();
        if (input == 'q') {
            break;
        }
        else if (wasdadapter(input) != ' ') {
    pos = move(pos, wasdadapter(input));
    std::cout << "Position: " << pos.x << ", " << pos.y << std::endl;
    }
    }
    }
    }
    else if (argc >= 3) {
        position maxmargin;
        maxmargin.x = std::stoi(argv[1]);
        maxmargin.y = std::stoi(argv[2]);
        position pos;
        pos.x = -1;
        pos.y = -1;
        while (pos.x<0 && pos.y<0)
        {   std::cout << "Define player position (x,y): ";
            std::cin >> pos.x; 
            std::cin >> pos.y;
            if (pos.x < 0 || pos.x > maxmargin.x || pos.y < 0 || pos.y > maxmargin.y) {
                std::cout << "Invalid position" << std::endl;
                pos.x = -1;
                pos.y = -1;
            }
        }
        while (true)
        {   bool surround[4];
            printf("Isteppable:");
            std::cin >> surround[0]; //North
            std::cin >> surround[1]; //South
            std::cin >> surround[2]; //East
            std::cin >> surround[3]; //West
            printf("Move:");
            char input;
            std::cin >> input;
            char direction = wasdadapter(input);
            if (direction == 'N' && surround[0] && pos.y < maxmargin.y) {
                pos = move(pos, direction);
            } else if (direction == 'S' && surround[1] && pos.y > 0) {
                pos = move(pos, direction);
            } else if (direction == 'E' && surround[2] && pos.x < maxmargin.x) {
                pos = move(pos, direction);
            } else if (direction == 'W' && surround[3] && pos.x > 0) {
                pos = move(pos, direction);
            } else {
                std::cout << "Invalid move" << std::endl;
            }
            std::cout << "Position: " << pos.x << ", " << pos.y << std::endl;    
        }
        
    }
    else {
        std::cout << "Invalid arguments" << std::endl;
    }
    return 0;

}
