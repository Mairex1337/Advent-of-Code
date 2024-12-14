"""
Optimized solution using a directed graph.
"""
import sys

sys.setrecursionlimit(5000)

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
        guard: tuple[tuple[int, int], tuple[int, int]],
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

def dfs(g: dict, guard: tuple, visited: set = set()):
    if guard not in g.keys():
        return len(list(visited))
    visited.add((guard[0], guard[1]))
    return dfs(g, g[guard], visited)

if __name__ == '__main__':
    import time
    start = time.time()
    content, blocked, guard, dy, dx = read_input()
    g = create_directed_graph(blocked, guard, dy, dx)
    print(dfs(g, guard))
    stop = time.time()
    print(f"Time taken: {(stop - start):.4f}s")
    
