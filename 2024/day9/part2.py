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
            free = int(content[num])
            free_indicies.append([curr_index, curr_index + free])
            curr_index += int(content[num])
  
    for busy in range(len(busy_indices) - 1, -1, -1):
        starting_index = busy_indices[busy][0]
        stop_index = busy_indices[busy][1]
        i_d = busy_indices[busy][2]
        found_option = False
        for free in range(len(free_indicies)):
            if free_indicies[free][0] > starting_index:
                continue
            if free_indicies[free][1] - free_indicies[free][0] == stop_index - starting_index:
                for i in range(free_indicies[free][0], free_indicies[free][1]):
                    result += i_d * i
                free_indicies.pop(free)
                found_option = True
                break
            elif free_indicies[free][1] - free_indicies[free][0] >= stop_index - starting_index:
                free_lst = list(range(free_indicies[free][0], free_indicies[free][1]))
                for g in range(stop_index - starting_index):
                    result += i_d * free_lst[g]
                free_indicies[free][0] += (stop_index - starting_index)
                found_option = True
                break
        if not found_option:
            for ind in range(starting_index, stop_index):
                result += ind * i_d
    return result


if __name__ == '__main__':
    with open('input.txt', 'r') as t:
        content = t.read().strip()
    print(solve(content))
