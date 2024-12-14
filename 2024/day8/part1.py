import math


def get_antinodes(
        coords: list[tuple[int]],
        max_l: int,
        max_c: int
) -> list[tuple[int]]:
    antinodes = []
    for coord1 in coords:
        for coord2 in coords:
            if coord1 == coord2:
                continue
            antinode1 = (
                coord1[0] + (coord1[0] - coord2[0]),
                coord1[1] + (coord1[1] - coord2[1])
            )
            antinode2 = (
                coord2[0] + (coord2[0] - coord1[0]),
                coord2[1] + (coord2[1] - coord1[1]),
            )
            condition1 = 0 <= antinode1[0] < max_l and 0 <= antinode1[1] < max_c
            condition2 = 0 <= antinode2[0] < max_l and 0 <= antinode2[1] < max_c
            antinodes.append(antinode1) if condition1 else None
            antinodes.append(antinode2) if condition2 else None
    return antinodes

if __name__ == '__main__':
    with open('input.test', 'r') as t:
        content = t.read().strip()


    antennas = dict()
    for line in range(len(content.splitlines())):
        for col in range(len(content.splitlines()[0])):
            symbol = content.splitlines()[line][col]
            if symbol != '.':
                antennas.setdefault(symbol, []).append((line, col))
    print(antennas)
    max_l = len(content.splitlines())
    max_c = len(content.splitlines()[0])
    
    antinodes = {x for _, v in antennas.items() for x in get_antinodes(v, max_l, max_c)}
    print(list(antinodes))

"""
{
'0': [(1, 8), (2, 5), (3, 7), (4, 4)],
'A': [(5, 6), (8, 8), (9, 9)]
}
"""