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
    visited = {(guard)}
    next_dir = {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1)
    }
    while 0 <= guard_pos[0] < dy - 1 and 0 <= guard_pos[1] < dx - 1:
        new_pos = (guard_pos[0] + guard_dir[0], guard_pos[1] + guard_dir[1])
        if new_pos in blocked:
            guard_dir = next_dir[guard_dir]
            visited.add((guard_pos, guard_dir))
            continue
        guard_pos = new_pos
        visited.add((guard_pos, guard_dir))
    return list(visited)

def calculate_worthwile_blocks(visited: list, blocked: list, dy: int, dx: int):
    next_dir = {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1)
    }
    worthwile_blocks = set()
    for position, orientation in visited:
        for blockade in blocked:
            if (
                position[0] == blockade[0] and position[1] < blockade[1] and next_dir[orientation][1] == 1
            ) or(
                position[0] == blockade[0] and position[1] > blockade[1] and next_dir[orientation][1] == -1
            ) or (
                position[1] == blockade[1] and position[0] < blockade[0] and next_dir[orientation][0] == 1
            ) or (
                position[1] == blockade[1] and position[0] > blockade[0] and next_dir[orientation][0] == -1
            ):
                block = (position[0] + orientation[0], position[1] + orientation[1])
                if block in blocked:
                    continue
                if (0 <= block[0] < dy and 0 <= block[1] < dx):
                    worthwile_blocks.add(block)
    print(f"Visited: {len(visited)}, worth blocks: {len(worthwile_blocks)}")
    return list(worthwile_blocks)

def possible_obstruction_positions(
        visited: list,
        blocked: list,
        guard: tuple,
        dy: int,
        dx: int,
):
    counter = 0
    next_dir = {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1)
    }
    worthwile_blocks = calculate_worthwile_blocks(
        visited, blocked, dy, dx
    )
    for coordinate in worthwile_blocks:
        orientations = set(guard)
        temp_blocked = blocked + [coordinate]
        temp_pos, temp_dir = guard
        while 0 <= temp_pos[0] < dy - 1 and 0 <= temp_pos[1] < dx - 1:
            new_pos = (temp_pos[0] + temp_dir[0], temp_pos[1] + temp_dir[1])
            if (new_pos, temp_dir) in orientations:
                counter += 1
                break
            if new_pos in temp_blocked:
                temp_dir = next_dir[temp_dir]
                orientations.add((temp_pos, temp_dir))  # Fix
                continue
            temp_pos = new_pos
            orientations.add((temp_pos, temp_dir))
    return counter


if __name__ == '__main__':
    import time
    start = time.time()
    blocked, guard, dy, dx = read_input()

    visited = get_distinct_positions(blocked, guard, dy, dx)

    print(possible_obstruction_positions(visited, blocked, guard, dy, dx))

    stop = time.time()
    print(f"Time taken: {stop - start}s")
"""
Wow this was slow!

1516
Time taken: 102.71882653236389s

After adding worthwile blocks function:

Visited: 4823, worth blocks: 3946
1482
Time taken: 90.84196639060974s

After fixing bug:

Visited: 4960, worth blocks: 4040
1516
Time taken: 92.46490335464478s
"""