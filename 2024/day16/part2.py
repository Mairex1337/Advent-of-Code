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
) -> dict:
    heap = MinHeap()
    heap.enqueue((0, start))
    optimal_paths = dict()
    optimal_cost = None
    costs = dict()
    while len(heap) > 0:
        cost, node = heap.dequeue()
        if node == goal:
            if optimal_cost is None:
                optimal_cost = cost
            continue
        if optimal_cost is not None and cost > optimal_cost:
            break
        for neighbors in g.graph[node]:
            other = neighbors.get_other(node)
            new_cost = neighbors.get_weight() + cost
            if new_cost < costs.get(other, float('inf')):
                heap.enqueue((new_cost, other))
                costs[other] = new_cost
                optimal_paths[other] = {node}
            elif new_cost == costs.get(other, float('inf')):
                optimal_paths[other].add(node)
    
    return optimal_paths

def get_unique_locations(g: WeightedGraph, start: tuple, goal: tuple) -> int:
    optimal_paths = dijkstras(g, start, goal)
    stack = [goal]
    tiles_with_dir = set()
    while stack:
        current = stack.pop()
        if current in tiles_with_dir:
            continue
        tiles_with_dir.add(current)
        for node in optimal_paths[current]:
            stack.append(node)
    tiles_unique = {(x[0], x[1]) for x in tiles_with_dir}
    return len(tiles_unique)

if __name__ == "__main__":
    import time
    with open('input.txt', 'r') as t:
        grid = t.read().strip().splitlines()

    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    start_g = time.time()
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
    print(f" Graph edges setup time: {stop_g - start_g:.4f}")
    start_d = time.time()

    print(get_unique_locations(g, start, goal))
    stop_d = time.time()
    print(f" Dijkstras search time: {stop_d - start_d:.4f}.")
