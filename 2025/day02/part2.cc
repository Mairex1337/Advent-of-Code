#include "main.ih"

// Now, number consists of repeating digits that appear at least twice.

bool is_repeating(string const &curr)
{
    size_t len = curr.length();
    for (size_t idx = len / 2; idx != 0; --idx)
    {
        if (len % idx != 0)
            continue;
        bool repeating = true;
        for (size_t num = idx; num < len; num += idx)
        {
            if (!equal(curr.begin(), curr.begin() + idx, curr.begin() + num))
            {
                repeating = false;
                break;
            }
        }
        if (repeating)
            return true;
    }
    return false;
}

size_t find_invalid(size_t start, size_t end)
{
    size_t sum = 0;
    for (string curr; start <= end; ++start)
    {
        curr = to_string(start);
        sum += is_repeating(curr) ? start : 0;
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
        idx = str.find('-');
        result += find_invalid(stoul(str.substr(0, idx)), stoul(str.substr(idx + 1)));
    }
    cout << "Final result: " << result << "\n";
}
