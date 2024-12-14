def calculate_perimeter(coords: list, directions: list) -> int:
    perimeter = 0
    for plant in coords:
        neighbors = 0
        for direction in directions:
            new = (plant[0], plant[1] + direction[0], plant[2] + direction[1])
            neighbors += 1 if new in coords else 0
        perimeter += 4 - neighbors
    return perimeter

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
    

def find_fence_price(graph: dict, directions: list) -> int:
    seen = set()
    result = 0
    for k in graph.keys():
        if k not in seen:
            seen.add(k)
            region_coords = traverse_graph(graph, seen, k, [k])
            area = len(region_coords)
            perimeter = calculate_perimeter(region_coords, directions)
            result += area * perimeter
    return result

if __name__ == '__main__':
    with open('input.txt', 'r') as t:
        content = t.read().strip().splitlines()
    print('\n'.join(x for x in content))
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
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
    
    print(find_fence_price(graph, directions))