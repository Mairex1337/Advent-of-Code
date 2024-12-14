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
            vec_1_l = coord1[0] - coord2[0]
            vec_1_c = coord1[1] - coord2[1]
            for dir in [1, -1]:
                i = 0 if dir == 1 else -1
                while 0 <= coord1[0] + vec_1_l * i < max_l and 0 <= coord1[1] + vec_1_c * i < max_c:
                    antinodes.append((coord1[0] + vec_1_l * i, coord1[1] + vec_1_c * i))
                    i += 1 if dir == 1 else -1    
    return antinodes

if __name__ == '__main__':
    with open('input.txt', 'r') as t:
        content = t.read().strip()


    antennas = dict()
    for line in range(len(content.splitlines())):
        for col in range(len(content.splitlines()[0])):
            symbol = content.splitlines()[line][col]
            if symbol != '.':
                antennas.setdefault(symbol, []).append((line, col))
    max_l = len(content.splitlines())
    max_c = len(content.splitlines()[0])
    
    antinodes = {
        x for _, v in antennas.items() for x in get_antinodes(v, max_l, max_c)
    }
    print(len(antinodes))
