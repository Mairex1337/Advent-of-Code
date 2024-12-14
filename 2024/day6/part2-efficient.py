"""
Optimized solution using a directed graph.
"""
import sys

sys.setrecursionlimit(10000)

def read_input() -> tuple[list]:
    with open('input.txt', 'r') as t:
        content = t.read().strip().splitlines()

    blocked = set()
    dy, dx = (len(content), len(content[0]))
    guard = None

    directions = {
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1),
        '^': (-1, 0),
    }

    for line in range(len(content)):
        for column in range(len(content[0])):
            blocked.add((line, column)) if content[line][column] == '#' else None
            if content[line][column] in ['>', '<', '^', 'v']:
                if guard:
                    raise ValueError("WTF")
                guard = (line, column, directions[content[line][column]][0], directions[content[line][column]][1])
    return content, blocked, guard, dy, dx


def create_directed_graph(
        blocked: set,
        dy: int,
        dx: int
) -> dict:
    g = dict() # (y, x, dy, dx): (ny, nx, ndy, ndx)
    next_dir = {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1)
    }
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for y in range(dy):
        for x in range(dx):
            if (y, x) in blocked:
                continue
            for diry, dirx in directions:
                ny, nx = y + diry, x + dirx
                if not (0 <= ny < dy and 0 <= nx < dx):
                    g[(y, x, diry, dirx)] = tuple()
                    continue
                if (ny, nx) in blocked:
                    ndy, ndx = next_dir[(diry, dirx)]
                    g[(y, x, diry, dirx)] = (y, x, ndy, ndx)
                else:
                    g[(y, x, diry, dirx)] = (ny, nx, diry, dirx)
    return g

def find_uniquely_visited(g: dict, guard: tuple, visited: set = set()):
    if guard not in g.keys():
        return visited
    visited.add((guard[0], guard[1]))
    return find_uniquely_visited(g, g[guard], visited)


def find_scc(g: dict, guard: tuple, blockade: tuple, next_dir, vis: set):
    if guard in vis:
        return True
    next_state = g[guard]
    if next_state == ():
        return False

    vis.add(guard)
    ny, nx, ndy, ndx = next_state

    if (ny, nx) == blockade:
        y, x, dy, dx = guard
        turned_dy, turned_dx = next_dir[(dy, dx)]
        guard = (y, x, turned_dy, turned_dx)
    else:
        guard = (ny, nx, ndy, ndx)
    return find_scc(g, guard, blockade, next_dir, vis)
    

def get_number_of_loops(g: dict, visited: set, guard: tuple) -> int:
    next_dir = {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1)
    }
    ans = 0
    for blockade in visited:
        ans += 1 if find_scc(g, guard, blockade, next_dir, set()) else 0
    return ans


if __name__ == '__main__':
    import time
    start = time.time()
    content, blocked, guard, dy, dx = read_input()
    g = create_directed_graph(blocked, dy, dx)
    visited = find_uniquely_visited(g, guard)
    print(f" The number of uniquely visited states is: {len(list(visited))}")
    print(get_number_of_loops(g, visited, guard))
    
    stop = time.time()
    print(f"Time taken: {(stop - start):.4f}s")
    
"""
Old approach:
1516
Time taken: 92.46490335464478s

New approach:
The number of uniquely visited states is: 4433
1516
Time taken: 5.7113s
"""