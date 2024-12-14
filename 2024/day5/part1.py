import re

with open('input.txt', 'r') as t:
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

for report in pages:
    page_nums = []
    for page in report:
        if page in rules.keys():
            if any([x in page_nums for x in rules[page]]):
                page_nums = []
                break
        page_nums.append(page)
    result += int(report[len(report) // 2]) if page_nums else 0
print(result)
