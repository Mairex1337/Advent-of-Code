#include "main.ih"

size_t gen_answer(char *arr, size_t size)
{
    size_t result = 0;
    for (size_t idx = size; idx--; )
        result = result * 10 + (arr[idx] - '0');
    return result;

}

size_t find_highest_joltage(string const &line)
{
    size_t const arr_len = 12;
    char arr[arr_len];
    fill(arr, arr + arr_len, '0');
    size_t idx = 0, str_len = line.length();
    for (char const &ch: line)
    {
        for (size_t digit = arr_len; digit--; )
        {
            if (ch > arr[digit] && idx < str_len - digit)
            {
                arr[digit] = ch;
                fill(arr, arr + digit, '0');
                break;
            }
        }
        ++idx;
    }
    size_t answer = gen_answer(arr, arr_len);
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

