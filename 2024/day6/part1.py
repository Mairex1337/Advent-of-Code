
def read_input() -> tuple[list]:
    with open('input.txt', 'r') as t:
        content = t.read().strip()
    split = content.splitlines()

    blocked = []
    dy, dx = (len(split), len(split[0]))
    guard = None

    directions = {
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1),
        '^': (-1, 0),
    }

    for line in range(len(split)):
        for column in range(len(split[0])):
            blocked.append((line, column)) if split[line][column] == '#' else None
            if split[line][column] in ['>', '<', '^', 'v']:
                if guard:
                    raise ValueError("WTF")
                guard = ((line, column), directions[split[line][column]])
    return blocked, guard, dy, dx


def get_distinct_positions(
        blocked: list[tuple],
        guard: tuple[tuple],
        dy: int,
        dx: int
) -> int:
    guard_pos, guard_dir = guard
    visited = {guard_pos}
    next_dir = {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1)
    }
    counter = 1
    while 0 <= guard_pos[0] < dy - 1 and 0 <= guard_pos[1] < dx - 1:
        new_pos = (guard_pos[0] + guard_dir[0], guard_pos[1] + guard_dir[1])
        if new_pos in blocked:
            guard_dir = next_dir[guard_dir]
            continue
        counter += 1 if (new_pos not in visited) else 0
        visited.add(new_pos)
        guard_pos = new_pos
    return counter



if __name__ == '__main__':
    import time
    start = time.time()
    blocked, guard, dy, dx = read_input()
    print(get_distinct_positions(blocked, guard, dy, dx))
    stop = time.time()
    print(f"Time taken: {stop - start:.4f}s")