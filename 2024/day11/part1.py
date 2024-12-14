def find_num_stones(stone: str, depth: int = 25) -> int:
    result = 0
    if depth == 0:
        return 1
    if stone == '0':
        result += find_num_stones('1', depth - 1)
    elif len(stone) % 2 == 0:
        new1, new2 = stone[:len(stone) // 2], stone[len(stone) // 2:]
        while new2.startswith('0') and len(new2) > 1:
            new2 = new2[1:]
        result += find_num_stones(new1, depth - 1)
        if new2 != '':
            result += find_num_stones(new2, depth - 1)
    else:
        new = str(int(stone) * 2024)
        result += find_num_stones(new, depth - 1)
    return result    
        

if __name__ == '__main__':
    import time
    start = time.time()
    with open('input.txt', 'r') as t:
        stones = t.read().split()
    result = 0
    for stone in stones:
        result += find_num_stones(stone)
    stop = time.time()
    print(result)
    print(f"Time taken: {(stop - start):.2f}")