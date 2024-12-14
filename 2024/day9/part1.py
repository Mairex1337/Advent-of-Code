"""
Alternating:
- Length of file (ID == Index)
- Length of free space
"""
# 2333133121414131402
# 00...111...2...333.44.5555.6666.777.888899


def solve(content: str) -> int:
    result = 0
    free_indicies = []
    busy_indices = []
    curr_index = 0
    for num in range(len(content)):
        if num % 2 == 0:
            i_d = num // 2
            if not free_indicies:
                for length in range(int(content[num])):
                    result += i_d * (length + curr_index)
            else:
                busy_indices.append((curr_index, int(content[num]) + curr_index, i_d))
            curr_index += int(content[num])
        else:
            for free in range(int(content[num])):
                free_indicies.append(free + curr_index)
            curr_index += int(content[num])
  
    for busy in range(len(busy_indices) - 1, -1, -1):
        starting_index = busy_indices[busy][0]
        stop_index = busy_indices[busy][1]
        i_d = busy_indices[busy][2]

        for i in range(stop_index - 1, starting_index - 1, -1):
            if free_indicies and free_indicies[0] <= i:
                result += free_indicies.pop(0) * i_d
            else:
                result += i * i_d
    return result


if __name__ == '__main__':
    with open('input.txt', 'r') as t:
        content = t.read().strip()
    print(solve(content))
