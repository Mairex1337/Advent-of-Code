#include "main.ih"

// 1 instruction per line of type 'R0' - 'R99' (or L)
// Dial initially points at 50
// count number of times it hits '0'

size_t process_turn(string const &inst)
{
    static int status = 50;
    int direction = (inst[0] == 'L') ? -1 : 1;

    int magnitude = stoi(inst.substr(1)) % 100;

    status = (status + direction * magnitude) % 100;
    if (status < 0) status += 100;

    cout << "Status: " << status << "\n\n";
    return status == 0 ? 1 : 0;
}

int main()
{
    ifstream file{"inp.txt"};
    string input;
    size_t result = 0;
    while (getline(file, input))
    {
        cout << "Current Input: " << input << "\n";
        result += process_turn(input);    
    }
    cout << "Final result: " << result << "\n";
}
