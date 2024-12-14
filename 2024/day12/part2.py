def calculate_sides(
        coords: list,
        diag_directions: list,
        directions: list
) -> int:
    """Very disgusting way of checking for corners. Corners == Sides"""
    sides = 0
    for coord in coords:
        down_right = (coord[0] + diag_directions[0][0], coord[1] + diag_directions[0][1])
        down_left = (coord[0] + diag_directions[1][0], coord[1] + diag_directions[1][1])
        up_left = (coord[0] + diag_directions[2][0], coord[1] + diag_directions[2][1])
        up_right = (coord[0] + diag_directions[3][0], coord[1] + diag_directions[3][1])
        right = (coord[0] + directions[0][0], coord[1] + directions[0][1])
        down = (coord[0] + directions[1][0], coord[1] + directions[1][1])
        left = (coord[0] + directions[2][0], coord[1] + directions[2][1])
        up = (coord[0] + directions[3][0], coord[1] + directions[3][1])

        # 'Outward' corners
        if down_right not in coords and down not in coords and right not in coords:
            sides += 1
        if down_left not in coords and down not in coords and left not in coords:
            sides += 1
        if up_left not in coords and up not in coords and left not in coords:
            sides += 1
        if up_right not in coords and up not in coords and right not in coords:
            sides += 1
        
        # 'Inward' corners
        if up in coords and left in coords and up_left not in coords:
            sides += 1
        if up in coords and right in coords and up_right not in coords:
            sides += 1
        if down in coords and right in coords and down_right not in coords:
            sides += 1
        if left in coords and down in coords and down_left not in coords:
            sides += 1

        # 'Loop' corners
        if up_left in coords and up not in coords and left not in coords:
            sides += 2
        if up_right in coords and up not in coords and right not in coords:
            sides += 2
    return sides

def traverse_graph(
        graph: dict,
        seen: set,
        plant: tuple[int],
        region_coords: list
) -> list:
    for next in graph[plant]:
        if next[0] == plant[0] and next not in seen:
            seen.add(next)
            region_coords.append(next)
            traverse_graph(graph, seen, next, region_coords)
    return region_coords
    

def find_fence_price(graph: dict, diag_directions: list, directions: list) -> int:
    seen = set()
    result = 0
    for k in graph.keys():
        if k not in seen:
            seen.add(k)
            region_coords = [x[1:] for x in traverse_graph(graph, seen, k, [k])]
            area = len(region_coords)
            sides = calculate_sides(region_coords, diag_directions, directions)
            result += area * sides
    return result

if __name__ == '__main__':
    with open('input.txt', 'r') as t:
        content = t.read().strip().splitlines()
    print('\n'.join(x for x in content))
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    diag_directions = [
        (1, 1),
        (1, -1),
        (-1, -1),
        (-1, 1)
    ]
    # directed graph
    graph = {}
    l = len(content)
    c = len(content[0])
    for line in range(len(content)):
        for col in range(len(content[0])):
            graph[(content[line][col], line, col)] = []
            for direction in directions:
                new = (line + direction[0], col + direction[1])
                if 0 <= new[0] < l and 0 <= new[1] < c:
                    graph[(content[line][col], line, col)].append((content[new[0]][new[1]], new[0], new[1]))
    print(find_fence_price(graph, diag_directions, directions))
