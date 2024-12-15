def calculate_robot_dim(robot: list, row_dim: int, col_dim: int) -> tuple:
    x, y, dx, dy = robot

    for _ in range(100):
        x += dx
        y += dy
        # If its out-of bounds, just scale it back in
        if x >= col_dim:
            x -= col_dim
        if y >= row_dim:
            y -= row_dim
        if x < 0:
            x += col_dim
        if y < 0:
            y += row_dim
    return (x, y)

if __name__ == '__main__':
    import re
    with open('input.txt', 'r') as t:
        content = t.read()
    robots = []
    for robot in content.split('\n'):
        robots.append([int(x) for x in re.findall(r'(\-?\d+)', robot)])
    
    row_dim = 103
    col_dim = 101
    result_positions = []
    for robot in robots:
        result_positions.append(calculate_robot_dim(robot, row_dim, col_dim))
    quadrants = {'0': 0, '1': 0, '2': 0, '3': 0}
    for x, y in result_positions:
        if x == col_dim // 2 or y == row_dim // 2:
            continue
        if x < col_dim // 2 and y < row_dim // 2:
            quadrants['0'] += 1
        if x > col_dim // 2 and y < row_dim // 2:
            quadrants['1'] += 1
        if x > col_dim // 2 and y > row_dim // 2:
            quadrants['2'] += 1
        if x < col_dim // 2 and y > row_dim // 2:
            quadrants['3'] += 1
    print(quadrants['0'] * quadrants['1'] * quadrants['2'] * quadrants['3'])
        
