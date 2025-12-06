#include "main.ih"

// accessible iff less than four '@' in sourrounding 8 squares

bool check_element(string *grid, int line, int col, int lines, int cols)
{
    size_t counter = 0;
    for (int l = line - 1; l <= line + 1; ++l)
    {
        if (l < 0 || l >= lines)
            continue;
        for (int c = col - 1; c <= col + 1; ++c)
        {
            if ((l == line && c == col) || c < 0 || c >= cols)
                continue;

            counter += grid[l][c] == '@' ? 1 : 0;
        }
    }
    return counter < 4;
}

size_t accessible_paper(string *grid, size_t lines, size_t cols)
{
    size_t result = 0;
    for (size_t line = 0; line != lines; ++line)
    {
        for (size_t col = 0; col != cols; ++col)
        {
            if (grid[line][col] != '@')
                continue;
            if (check_element(grid, line, col, lines, cols))
            {
                grid[line][col] = '.';
                ++result;
            }
        }
    }
    return result;
}

size_t multi_remover(string *grid, size_t lines, size_t cols)
{
    size_t result = 0, tmp = 1;
    while (tmp != 0)
    {
        tmp = accessible_paper(grid, lines, grid[0].length());
        result += tmp;
    }
    return result;
}


int main()
{
    size_t lines = 0;
    cin >> lines; // pipe `wc -l` into stdin
    string *grid = new string[lines];
    ifstream ifs{"inp.txt"};
    for (size_t idx = 0; idx != lines; ++idx)
    {
        getline(ifs, grid[idx]);
        cout << grid[idx] << "\n";
    }
    cout << "Final result: " << multi_remover(grid, lines, grid[0].length()) << "\n";

}
