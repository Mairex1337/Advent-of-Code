def solve_equations(equation1: tuple, equation2: tuple) -> int:
    cost_a = 3
    cost_b = 1
    rx, ax, bx = equation1
    ry, ay, by = equation2
    d = ax * by - ay * bx
    if d == 0:
        return 0
    a = (rx * by - ry * bx) / d
    b = (ax * ry - ay * rx) / d 
    if a % 1 != 0 or b % 1 != 0:
        return 0
    return int(a * cost_a + b * cost_b)

if __name__ == '__main__':
    import re
    with open('input.txt', 'r') as t:
        content = t.read()
    pattern_a = r"Button A: X\+(\d+), Y\+(\d+)"
    pattern_b = r"Button B: X\+(\d+), Y\+(\d+)"
    pattern_p = r"Prize: X\=(\d+), Y\=(\d+)"
    a = [tuple([int(x) for x in z]) for z in re.findall(pattern_a, content)]
    b = [tuple([int(x) for x in z]) for z in re.findall(pattern_b, content)]
    p = [tuple([int(x) for x in z]) for z in re.findall(pattern_p, content)]

    equations = []
    for (ax, ay),(bx, by), (rx, ry) in zip(a, b, p):
        eq1 = (rx + 10000000000000, ax, bx)
        eq2 = (ry + 10000000000000, ay, by)
        equations.append([eq1, eq2])

    total_cost = 0
    for equation_pair in equations:
        print(equation_pair)
        total_cost += solve_equations(equation_pair[0], equation_pair[1])
    print(total_cost)