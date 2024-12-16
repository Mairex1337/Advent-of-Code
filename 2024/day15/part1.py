def get_box_pos(
        robot: tuple,
        boxes: set[tuple],
        walls: set[tuple],
        moves: list[tuple],
        row_dim: int,
        col_dim: int
) -> set[tuple]:
    for move in moves:
        new_pos = (robot[0] + move[0], robot[1] + move[1])
        if new_pos in walls:
            continue
        if new_pos[0] in range(1, row_dim - 1) and new_pos[1] in range(1, col_dim - 1):
            if new_pos in boxes:
                boxes_in_dir = {new_pos}
                skip = False
                next_pos = new_pos
                while True:
                    next_pos = (next_pos[0] + move[0], next_pos[1] + move[1])
                    if not (next_pos[0] in range(1, row_dim - 1) and next_pos[1] in range(1, col_dim - 1)):
                        skip = True
                        break
                    if next_pos in walls:
                        skip = True
                        break
                    if not next_pos in boxes:
                        break
                    boxes_in_dir.add(next_pos)
                if skip:
                    continue
                for box in boxes_in_dir:
                    boxes.remove(box)
                for box in boxes_in_dir:
                    boxes.add((box[0] + move[0], box[1] + move[1]))
                robot = new_pos
            else:
                robot = new_pos
    return boxes


def calculat_gps(boxes: set[tuple], row_dim: int, col_dim: int) -> int:
    gps = 0
    for row, col in boxes:
        gps += 100 * row + col
    return gps


if __name__ == "__main__":
    with open('input.txt', 'r') as t:
        loc, moves = t.read().split('\n\n')
    loc = loc.splitlines()
    moves = moves.replace('\n', '')

    row_dim = len(loc)
    col_dim = len(loc[0])
    walls = set()
    boxes = set()
    for row in range(1, row_dim - 1):
        for col in range(1, col_dim - 1):
            if loc[row][col] == '@':
                robot_pos = (row, col)
            if loc[row][col] == 'O':
                boxes.add((row, col))
            if loc[row][col] == '#':
                walls.add((row, col))
    mapping = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    moves = [mapping[x] for x in moves]
    final_box_locations = get_box_pos(robot_pos, boxes, walls, moves, row_dim, col_dim)
    print(calculat_gps(final_box_locations, row_dim, col_dim))
