inp_lst = []
with open('input2.test', 'r') as t:
    content = t.readlines()
    for line in range(len(content)):
        inp_lst.append(content[line].strip().strip('\n'))
result = 0
for line in range(2, len(inp_lst)):
    for n in range(2, len(inp_lst[line])):
        l1e1 = inp_lst[line - 2][n - 2]
        l1e3 = inp_lst[line - 2][n]
        l2e2 = inp_lst[line - 1][n - 1]
        l3e1 = inp_lst[line][n - 2]
        l3e3 = inp_lst[line][n]
        if l2e2 == 'A':
            val = ord('M') + ord('S')
            if ord(l1e1) + ord(l3e3) == val and ord(l3e1) + ord(l1e3) == val:
                result += 1
print(result)
