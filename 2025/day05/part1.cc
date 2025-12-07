#include "main.ih"

struct Range
{
    size_t start = 0;
    size_t end = 0;
};


int main()
{
    ifstream ifs{"real.txt"};
    streampos pos = ifs.tellg();
    string line;
    size_t range_counter = 0;
    while (getline(ifs, line) && !line.empty())
        ++range_counter;
    ifs.seekg(pos);

    Range *ranges = new Range[range_counter];
    // construct range objects
    for (size_t idx = 0; getline(ifs, line) && !line.empty(); ++idx)
    {
        size_t delim = line.find('-');
        ranges[idx].start = stoul(line.substr(0, delim));
        ranges[idx].end = stoul(line.substr(delim + 1));
    }

    size_t result = 0;
    while (getline(ifs, line))
    {
        for (size_t i = 0; i != range_counter; ++i)
        {
            size_t curr = stoul(line);
            if (curr >= ranges[i].start && curr <= ranges[i].end)
            {
                ++result;
                break;
            }
        }
    }
    cout << "Final result: " << result << "\n";
    delete[] ranges;
}
