
def calculate_robot_dim(robots: list[list], row_dim: int, col_dim: int) -> tuple:
    with open('log.txt', 'a') as log:
        for iteration in range(100000):
            seen = set()
            for robot in range(len(robots)):
                x, y, dx, dy = robots[robot]
                x += dx
                y += dy
                if x >= col_dim:
                    x -= col_dim
                if y >= row_dim:
                    y -= row_dim
                if x < 0:
                    x += col_dim
                if y < 0:
                    y += row_dim
                robots[robot] = [x, y, dx, dy]
                seen.add((x, y))
            if len(seen) == len(robots):
                robot_positions = {tuple(z[:2]) for z in robots}
                i = f'Current Iteration: {iteration + 1}\n'
                s = '\n'.join([" ".join([' ' if (x, y) not in robot_positions else '#' for x in range(col_dim)]) for y in range(row_dim)])
                print(i + s)
                break
    return

if __name__ == '__main__':
    import re
    with open('input.txt', 'r') as t:
        content = t.read()
    robots = []
    for robot in content.split('\n'):
        robots.append([int(x) for x in re.findall(r'(\-?\d+)', robot)])
    row_dim = 103
    col_dim = 101
    calculate_robot_dim(robots, row_dim, col_dim)
        