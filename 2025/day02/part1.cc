#include "main.ih"

// palindrome - ish exercise

size_t is_invalid(string const &curr)
{
    size_t first = 0, second = curr.length() / 2;
    for (size_t stop = second; first != stop; ++first, ++second)
    {
        if (curr[first] != curr[second])
            return 0;
    }
    return stoul(curr);
}

size_t find_invalid(size_t start, size_t end)
{
    size_t sum = 0;
    for (string curr; start <= end; ++start)
    {
        curr = to_string(start);
        if (size_t n_start = curr.length(); n_start % 2 != 0)
        {
            if (size_t n_end = to_string(end).length(); n_start == n_end)
                return sum;
            else
            {
                start = static_cast<size_t>(pow(10, n_start));
                continue;
            }
        }
        sum += is_invalid(curr);
    }
    return sum;
}

int main()
{
    ifstream ifs{"inp.txt"};
    string str;
    size_t result = 0, idx = 0;
    while (getline(ifs, str, ','))
    {
        cout << str << "\n";
        idx = str.find('-');
        result += find_invalid(stoul(str.substr(0, idx)), stoul(str.substr(idx + 1)));
    }
    cout << "Final result: " << result << "\n";
}
