"""
- intergers 0-9
- Hiking trail: starts at 0 and ends at 9 (no diagonals)
- Trailhead: starts n hiking trails
- Trailhead score: number of 9 height positions reachable via hiking trails
- Result: sum of all trailhead scores

"""

def find_hiking_trails(
        tmap: list[str],
        position: tuple[int],
        directions: list[tuple[int]],
        seen: set,
        height: int = 0
) -> int:
    result = 0
    if position in seen:
        return 0
    if int(tmap[position[0]][position[1]]) != height:
        return 0
    if height == 9:
        return 1
    for dir in directions:
        pos = (position[0] + dir[0], position[1] + dir[1])
        if not (0 <= pos[0] < len(tmap) and 0 <= pos[1] < len(tmap[0])):
            continue
        result += find_hiking_trails(
            tmap,
            pos,
            directions,
            seen,
            height + 1
        )
    return result

if __name__ == '__main__':
    with open('input.txt', 'r') as t:
        content = t.read().strip()
    tmap = content.splitlines()
    trailheads = []
    for l in range(len(tmap)):
        for c in range(len(tmap[0])):
            if tmap[l][c] == '0':
                trailheads.append((l, c))
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    res = 0
    for trail in trailheads:
        res += find_hiking_trails(tmap, trail, directions, set())
    print(res)