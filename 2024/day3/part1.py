with open("input.txt", "r") as t:
    content = t.read()

import re

pattern = re.compile(r"mul\((\d+,\d+)\)")
ls = re.findall(pattern, content)

result = 0

for mul in range(len(ls)):
    ls[mul] = ls[mul].split(',')
    ls[mul][0] = int(ls[mul][0])
    ls[mul][1] = int(ls[mul][1])
    result += ls[mul][1] * ls[mul][0]

print(result)


