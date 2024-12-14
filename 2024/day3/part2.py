with open("input.txt", "r") as t:
    content = t.read()

import re

pattern = re.compile(r"mul\((\d+,\d+)\)|(do\(\))|(don't\(\))")
ls = re.findall(pattern, content)

parsed = []

for tu in ls:
    for item in tu:
        if item != '':
            parsed.append(item)

result = 0
status = True

print(parsed)

for mul in range(len(parsed)):
    if parsed[mul][0].isnumeric() and status:
        parsed[mul] = parsed[mul].split(',')
        parsed[mul][0] = int(parsed[mul][0])
        parsed[mul][1] = int(parsed[mul][1])
        result += parsed[mul][1] * parsed[mul][0]
    elif parsed[mul] == "don't()":
        status = False
    elif parsed[mul] == "do()":
        status = True


print(result)


