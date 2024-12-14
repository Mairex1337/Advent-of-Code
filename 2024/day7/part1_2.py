def find_correct_equation(
        solution: int,
        equation: list[int],
        current_total: int,
        index: int = 0
):
    if index == len(equation) - 1:
        return True if current_total == solution else False
    add_result = find_correct_equation(
        solution,
        equation,
        current_total + equation[index + 1],
        index + 1
    )
    mul_result = find_correct_equation(
        solution,
        equation,
        current_total * equation[index + 1],
        index + 1
    )
    concat_result = find_correct_equation(
        solution,
        equation,
        int(str(current_total) + str(equation[index+1])),
        index + 1
    )
    return add_result or mul_result or concat_result


if __name__ == '__main__':
    with open('input.txt', "r") as t:
        content = t.read().strip()
    formatted = []
    for line in content.splitlines():
        f = [int(x) for x in line.replace(':', '').split()]
        formatted.append(f)

    ans = 0
    for equation in formatted:
        correct_eq = find_correct_equation(
            equation[0], equation[1:], equation[1]
        )
        if correct_eq:
            ans += equation[0]
        else:
            print(f'({str(equation[0])}, {equation[1:]}),')
    print(f'Length formatted: {len(formatted)} | Length input: {len(content.splitlines())}')
    print(ans)