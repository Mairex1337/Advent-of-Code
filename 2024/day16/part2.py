class Edge:
    def __init__(self, node1: tuple, node2: tuple, weight: int) -> None:
        self._node1 = node1
        self._node2 = node2
        self._weight = weight
    
    def _is_member(self, node: tuple) -> bool:
        return node == self._node1 or node == self._node2
    
    def get_other(self, node: tuple) -> tuple:
        if self._is_member(node):
            return self._node2 if node == self._node1 else self._node1
        else:
            raise ValueError('No edges.')
    
    def get_weight(self) -> int:
        return self._weight

class WeightedGraph:
    def __init__(self) -> None:
        self.graph = dict()
    
    def add_edge(self, node1: tuple, node2: tuple, weight: int) -> None:
        new_edge = Edge(node1, node2, weight)
        self.graph.setdefault(node1, []).append(new_edge)

class MinHeap:
    def __init__(self) -> None:
        self._heap = [0]

    def __len__(self) -> int:
        return len(self._heap) - 1

    def enqueue(self, value) -> None:
        self._heap.append(value)
        self._upheap(len(self))

    def _upheap(self, index: int) -> None:
        while index // 2 > 0:
            if self._heap[index] < self._heap[index // 2]:
                self._heap[index], self._heap[index // 2] = self._heap[index // 2], self._heap[index]
            index //= 2

    def _downheap(self, index: int) -> None:
        if len(self) >= index * 2:
            node = self._heap[index]
            l_child = self._heap[index * 2]
            if len(self) >= index * 2 + 1:  # 2 children
                r_child = self._heap[index * 2 + 1]  # right child
            else:  # one child
                r_child = self._heap[index * 2]  # left child

            if l_child < node and l_child <= r_child:
                self._heap[index], self._heap[index * 2] = self._heap[index * 2], self._heap[index]
                self._downheap(index * 2)
            elif r_child < node:
                self._heap[index], self._heap[index * 2 + 1] = self._heap[index * 2 + 1], self._heap[index]
                self._downheap(index * 2 + 1)

    def dequeue(self):
        if len(self) == 0:
            raise ValueError('WE ARE EMPY, AHHHHH')
        min_value = self._heap[1]
        if len(self) > 1:
            self._heap[1] = self._heap.pop()  # make the last node the root node
            self._downheap(1)
        else:
            self._heap.pop()
        return min_value
    pass


def add_edges(g: WeightedGraph, node: tuple, directions: list, grid: list) -> None:
    row, col = node
    for i in range(len(directions)):
        dx, dy = directions[i]
        ndx, ndy = directions[i + 1 if i <= 2 else 0]
        npx, npy = directions[i - 1 if i >= 1 else 3]
        g.add_edge((row, col, dx, dy), (row, col, ndx, ndy), 1000)
        g.add_edge((row, col, dx, dy), (row, col, npx, npy), 1000)
        nx, ny = row + dx, col + dy
        char = grid[nx][ny]
        if char == '#':
            continue
        if char == 'E':
            g.add_edge((row, col, dx, dy), (nx, ny), 1) # do not add directions for goal
            continue
        else:
            g.add_edge((row, col, dx, dy), (nx, ny, dx, dy), 1)


def dijkstras(
        g: WeightedGraph,
        start: tuple,
        goal: tuple,
        prev_visited: set = {},
        optimal_cost: int = 10000000
) -> tuple[int, set]:
    heap = MinHeap()
    heap.enqueue((0, start, {start}))
    seen = set() if prev_visited == {} else prev_visited
    while len(heap) > 0:
        cost, node, tiles = heap.dequeue()
        if node in seen:
            continue
        if cost > optimal_cost:
            return -1, {}
        if node == goal:
            return cost, tiles
        seen.add(node)  # increment by one later the total
        for neighbors in g.graph[node]:
            other = neighbors.get_other(node)
            if other not in seen:
                new_cost = cost + neighbors.get_weight()
                heap.enqueue((new_cost, other, tiles | {other}))
    return -1, {}


def get_all_locations(g: WeightedGraph, start: tuple, goal: tuple) -> set:
    optimal_cost, tiles = dijkstras(g, start, goal)
    i = 0
    while i < 1:
        to_be_added = set()
        z = 0
        for location in tiles:
            print(f'Current iteration at depth {i}: {z}')
            if location == start:
                continue
            new_cost, new_tiles = dijkstras(
                g, start, goal, {location}, optimal_cost
            )
            z += 1
            if new_cost != optimal_cost:
                continue
            to_be_added |= new_tiles
        tiles |= to_be_added
        i += 1
    return tiles

if __name__ == "__main__":
    import time
    from copy import deepcopy
    with open('input.txt', 'r') as t:
        grid = t.read().strip().splitlines()

    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    begin_g = time.time()
    g = WeightedGraph()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'S':
                start = (row, col, 0, 1)
                add_edges(g, (row, col), directions, grid)
            if grid[row][col] == 'E':
                goal = (row, col)
            elif grid[row][col] == '.':
                add_edges(g, (row, col), directions, grid)

    stop_g = time.time()
    print(f" Graph edges setup time: {stop_g - begin_g:.4f}")
    start_d = time.time()

    tiles = get_all_locations(g, start, goal)
    stop_d = time.time()
    print(f" Dijkstras search time: {stop_d - start_d:.4f}.")

    tiles_unique = {(node[0], node[1]) for node in tiles}
    print(f'Number of unique tiles found: {len(tiles_unique)}')

    print('\n'.join(
        ''.join('O' if (row, col) in tiles_unique else '.' for col in range(1, len(grid[0]) - 1))
        for row in range(1, len(grid) - 1)
    ))