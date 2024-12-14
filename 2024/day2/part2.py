report_list = []
with open("input-1.txt", 'r') as t:
    t = t.readlines()
    for line in t:
        report_list.append([int(x) for x in line.strip().split()])

def incr_decr(report: list) -> tuple[list, list]:
    increasing = [
        1 if report[curr] - report[next] in [-1, -2, -3] else 0
        for curr, next in zip(range(len(report) - 1), range(1, len(report)))
    ]
    decreasing = [
        1 if report[curr] - report[next] in [1, 2, 3] else 0
        for curr, next in zip(range(len(report) - 1), range(1, len(report)))
    ]
    return increasing, decreasing

safe_reports = 0

for report in report_list:
    increasing, decreasing = incr_decr(report)
    if sum(increasing) == len(report) - 1 or sum(decreasing) == len(report) -1:
        safe_reports += 1
    else:
        cp = report[:]
        new = report[:-1] 
        increasing, decreasing = incr_decr(new)
        if sum(increasing) == len(new) - 1 or sum(decreasing) == len(new) -1:
            safe_reports += 1
            continue
        for i in range(len(report) - 1):
            cp = report[:]
            new = cp[:i] + cp[i + 1:]
            increasing, decreasing = incr_decr(new)
            if sum(increasing) == len(new) - 1 or sum(decreasing) == len(new) -1:
                safe_reports += 1
                break

print(f"Safe reports: {safe_reports}")
print(f"Number of reports: {len(report_list)}")