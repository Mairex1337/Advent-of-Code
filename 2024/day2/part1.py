"""
- each line a report
- each report is a list of 'levels' that are seperated by spaces
- Check if reports are safe
A report is safe if:
- The levels are either all increasing or all decreasing
- Any two adjacent levels differ by alt least one and at most three
"""
report_list = []
with open("input-1.txt", 'r') as t:
    t = t.readlines()
    for line in t:
        report_list.append([int(x) for x in line.strip().split()])

safe_reports = 0

for report in report_list:
    increasing = all(report[curr] - report[next] in [-1, -2, -3] for curr, next in zip(range(len(report) - 1), range(1, len(report))))
    decreasing = all(report[curr] - report[next] in [1, 2, 3] for curr, next in zip(range(len(report) - 1), range(1, len(report))))
    if increasing or decreasing:
        safe_reports += 1
        print(report)

print(f"Safe reports: {safe_reports}")
print(f"Number of reports: {len(report_list)}")