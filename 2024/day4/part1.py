import re

inp_lst = []
with open('input.test', 'r') as t:
    content = t.readlines()
    for line in range(len(content)):
        inp_lst.append(content[line].strip().strip('\n'))
rev = []
for line in inp_lst:
    rev_line = ''
    for char in range(len(line) - 1, -1, -1):
        rev_line += line[char]
    rev.append(rev_line)


# horizontal and backward
full = ''
for i in content:
    full += i
full += '\n'

# vertical
vertical = ''
for length in range(len(inp_lst[0])):
    temp = ''
    for line in inp_lst:
        temp += line[length]
    temp += '\n'
    vertical += temp

# Diagonal
diag1 = ''
diag2 = ''
# top right half
for length in range(len(inp_lst[0])):
    temp1 = ''
    temp2 = ''
    for i, line in enumerate(inp_lst):
        if not i + length > len(inp_lst[0]) - 1:
            temp1 += line[i + length]
    temp1 += '\n'
    diag1 += temp1
    for i, line in enumerate(rev):
        if not i + length > len(rev[0]) - 1:
            temp2 += line[i + length]
    temp2 += '\n'
    diag2 += temp2

# bottom left half
for lines in range(1, len(inp_lst)):
    temp1 = ''
    temp2 = ''
    for i, line in enumerate(inp_lst[lines:]):
        temp1 += line[i]
    temp1 += '\n'
    diag1 += temp1
    for i, line in enumerate(rev[lines:]):
        temp2 += line[i]
    temp2 += '\n'
    diag2 += temp2

final = full + vertical + diag1 + diag2
print(final)
matches = re.findall(r'XMAS', final)
matches2 = re.findall(r'SAMX', final)
result = len(matches) + len(matches2)
print(result)
