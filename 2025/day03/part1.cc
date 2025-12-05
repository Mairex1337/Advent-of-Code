#include "main.ih"


size_t find_highest_joltage(string &line)
{
    char first = '0', second = '0';
    size_t idx = 0, len = line.length();
    for (char &ch: line)
    {
        if (ch > first && idx != len - 1)
        {
            first = ch;
            second = '0';
        }
        else if (ch > second)
            second = ch;
        ++idx;
    }
    size_t answer = (first - '0') * 10 + second - '0';
    cout << "Answer found: " << answer << "\n\n";
    return answer;
    
}

int main()
{
    ifstream ifs{"inp.txt"};
    string line;
    size_t result = 0;
    while (getline(ifs, line))
    {
        cout << "Current line: " << line << "\n";
        result += find_highest_joltage(line);
    }
    cout << "Final Result: " << result << "\n";
}
