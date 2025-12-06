#include "main.ih"


size_t process_turn(string const &inst)
{
    static int status = 50;
    int direction = (inst[0] == 'L') ? -1 : 1;
    int magnitude = stoi(inst.substr(1));

    size_t clicks = 0;
    if (direction == -1)
        clicks += (abs(status - 100) % 100 + magnitude) / 100;
    if (direction == 1)
        clicks += (magnitude + status) / 100;

    status = ((status + direction * magnitude) % 100 + 100) % 100;

    return clicks;
}

int main()
{
    ifstream file{"inp.txt"};
    string input;
    size_t result = 0;
    while (getline(file, input))
        result += process_turn(input);    

    cout << "Final result: " << result << "\n";
}
