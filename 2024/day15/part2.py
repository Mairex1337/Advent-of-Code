def check_valid(
        pos: tuple,
        walls: set[tuple],
        row_dim: int,
        col_dim: int
) -> bool:
    if pos in walls:
        return False
    if not (pos[0] in range(1, row_dim - 1) and pos[1] in range(2, col_dim - 2)):
        return False
    return True


def horizontal_move(
        boxes: dict[tuple],
        robot_pos: tuple,
        new_pos: tuple,
        walls: set[tuple],
        move: tuple,
        row_dim: int,
        col_dim: int,
) -> dict:
    seen_boxes = {new_pos}
    temp = dict()
    push = True
    while True:
        new_pos = (new_pos[0] + move[0], new_pos[1] + move[1])
        if not check_valid(new_pos, walls, row_dim, col_dim):
            push = False
            break
        if new_pos not in boxes.keys():
            break
        seen_boxes.add(new_pos)
    if push:
        robot_pos = (robot_pos[0] + move[0], robot_pos[1] + move[1])
        for box in seen_boxes:
            val = boxes.pop(box)
            temp[(box[0] + move[0], box[1] + move[1])] = (val[0] + move[0], val[1] + move[1])
        boxes.update(temp)
    return boxes, robot_pos


def vertical_move(
        boxes: dict[tuple],
        robot_pos: tuple,
        new_pos: tuple,
        walls: set[tuple],
        move: tuple,
        row_dim: int,
        col_dim: int,
) -> dict:
    seen_boxes = {new_pos, boxes[new_pos]}
    temp = dict()
    push = True
    while True:
        seen_len = len(seen_boxes)
        buffer_seen = set()
        empty = 0
        print(seen_boxes)
        for box in seen_boxes:
            next_pos = (box[0] + move[0], box[1] + move[1])
            if not check_valid(next_pos, walls, row_dim, col_dim):
                push = False
                break        
            if next_pos not in boxes.keys() or next_pos in seen_boxes:
                empty += 1
                continue
            buffer_seen.add(next_pos)
            buffer_seen.add(boxes[next_pos])
        seen_boxes |= buffer_seen
        if not push:
            break
        print(f'empty: {empty} | seen_len: {seen_len}')
        if empty == seen_len:
            robot_pos = (robot_pos[0] + move[0], robot_pos[1] + move[1])
            for box in seen_boxes:
                val = boxes.pop(box)
                temp[(box[0] + move[0], box[1] + move[1])] = (val[0] + move[0], val[1] + move[1])
            boxes.update(temp)
            break
    return boxes, robot_pos


def get_box_layout(
        boxes: dict[tuple],
        robot: tuple,
        walls: set[tuple],
        move: tuple,
        row_dim: int,
        col_dim: int,
) -> tuple[dict, tuple]:
    new_pos = (robot[0] + move[0], robot[1] + move[1])
    if not check_valid(new_pos, walls, row_dim, col_dim):
        return boxes, robot
    if new_pos not in boxes.keys():
        return boxes, new_pos
    if move[0] == 0: # horizontal dir
        return horizontal_move(boxes, robot_pos, new_pos, walls, move, row_dim, col_dim)
    else: # vertical dir
        return vertical_move(boxes, robot_pos, new_pos, walls, move, row_dim, col_dim)


def calculat_gps(boxes: list[tuple], row_dim: int, col_dim: int) -> int:
    gps = 0
    for box in range(0, len(boxes), 2):
        gps += 100 * boxes[box][0] + boxes[box][1]
    return gps


if __name__ == "__main__":
    with open('input.txt', 'r') as t:
        loc, moves = t.read().split('\n\n')
    loc = loc.splitlines()
    moves = moves.replace('\n', '')

    row_dim = len(loc)
    col_dim = len(loc[0])
    walls = set()
    boxes = dict()
    for row in range(1, row_dim - 1):
        for col in range(1, col_dim - 1):
            box = []
            if loc[row][col] == '@':
                robot_pos = (row, col * 2)
            if loc[row][col] == 'O':
                boxes[(row, col * 2)] = (row, col * 2 + 1)
                boxes[(row, col * 2 + 1)] = (row, col * 2)
            if loc[row][col] == '#':
                walls.add((row, col * 2))
                walls.add((row, col * 2 + 1))
    mapping = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    moves = [mapping[x] for x in moves]
    col_dim = col_dim * 2
    for move in moves:
        new_boxes, robot_pos = get_box_layout(boxes, robot_pos, walls, move, row_dim, col_dim)
    print(calculat_gps(sorted(list(new_boxes)), row_dim, col_dim))

