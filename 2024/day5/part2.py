import re

with open('input2.txt', 'r') as t:
    content = t.read()


rules = {}

rule_lst = re.findall(r'(\d+)\|(\d+)', content)

for i in rule_lst:
    if i[0] not in rules.keys():
        rules[i[0]] = [i[1]]
    else:
        rules[i[0]].append(i[1])

pages = [x.split(',') for x in content.splitlines() if ',' in x]

result = 0
reordered = []

for report in pages:
    page_nums = []
    reorder = False
    for page in range(len(report)):
        temp = []
        page_nums.append(report[page])
        if report[page] in rules.keys():
            matches = [x for x in page_nums if x in rules[report[page]]]
            if matches:
                reorder = True
                old_indices = [page_nums.index(ind) for ind in matches]
                temp = page_nums[:old_indices[0]] + [page_nums[page]] + [page_nums[i] for i in old_indices]
                page_nums = temp
    if reorder:
        reordered.append(page_nums)
        result += int(page_nums[len(page_nums) // 2])

print(reordered)
print(f"result: {result}")
