#include "main.ih"

struct Range
{
    size_t start = 0;
    size_t end = 0;
    bool active = true;
};

void expand_range(Range *ranges, size_t len, size_t pos)
{
    while (true)
    {
        bool restart = false;
        size_t start = ranges[pos].start, end = ranges[pos].end;
        for (size_t idx = 0; idx != len; ++idx)
        {
            size_t other_start = ranges[idx].start, other_end = ranges[idx].end;
            // if its our current range, or removed range -> skip
            if (pos == idx || !ranges[idx].active)
                continue;
            // if other range is overlapping or adjacent to current range
            // merge it with current range, mark other range as inactive
            // repeat until no more merges possible
            if (other_start <= end + 1 && other_end + 1 >= start)
            {
                ranges[pos].start = min(start, other_start);
                ranges[pos].end = max(end, other_end);
                ranges[idx].active = false;
                restart = true;
                break;
            }
        }
        if (!restart)
            return;
    }
}

size_t compute_result(Range *ranges, size_t len)
{
    size_t result = 0;
    for (size_t idx = 0; idx != len; ++idx)
    {
        if (ranges[idx].active)
            result += ranges[idx].end + 1 - ranges[idx].start;
    }
    return result;
}

void construct_ranges(Range *ranges, ifstream &ifs)
{
    // construct range objects
    string line;
    for (size_t idx = 0; getline(ifs, line) && !line.empty(); ++idx)
    {
        size_t delim = line.find('-');
        ranges[idx].start = stoul(line.substr(0, delim));
        ranges[idx].end = stoul(line.substr(delim + 1));
    }
}

size_t n_ranges(ifstream &ifs)
{
    streampos pos = ifs.tellg();
    string line;
    size_t num_ranges = 0;
    while (getline(ifs, line) && !line.empty())
        ++num_ranges;
    ifs.clear();
    ifs.seekg(pos);
    return num_ranges;
}

int main()
{
    ifstream ifs{"real.txt"};
    size_t num_ranges = n_ranges(ifs);

    Range *ranges = new Range[num_ranges];
    construct_ranges(ranges, ifs);

    // expand (active) ranges
    for (size_t range = 0; range != num_ranges; ++range)
    {
        if (ranges[range].active)
            expand_range(ranges, num_ranges, range);
    }
    // result is the sum of the length of all ranges, as none overlap now
    cout << "Final result: " << compute_result(ranges, num_ranges) << "\n";
    delete[] ranges;
}
