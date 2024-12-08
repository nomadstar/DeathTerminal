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
int main(){
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
    return 0;




}
