import csv
import statistics
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
RESULTS = DATA.parent / 'results'
RESULTS.mkdir(exist_ok=True)
def read(name):
    with (DATA / name).open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))
key = {x['message_id']: x for x in read('condition_key.csv')}
ratings = defaultdict(list)
for name in ('ratings_Jimmy.csv', 'ratings_Terrence.csv'):
    for row in read(name):
        fields = ['accuracy_0to2','completeness_0to2','unsupported_claims_count','omitted_changes_count']
        if not any(row[f].strip() for f in fields):
            continue
        if not all(row[f].strip() for f in fields):
            raise ValueError(f'Incomplete score in {name}: {row["message_id"]}')
        if row['message_id'] not in key:
            raise ValueError('Unknown message ID.')
        scores = {f: int(row[f]) for f in fields}
        if any(scores[f] not in (0,1,2) for f in fields[:2]) or any(scores[f] < 0 for f in fields[2:]):
            raise ValueError(f'Invalid scores: {name}, {row["message_id"]}')
        ratings[row['message_id']].append(scores)
if not ratings:
    raise SystemExit('Fill in your ratings sheets first.')
case_data = defaultdict(dict)
for message_id, scored in ratings.items():
    case = key[message_id]['case_id']; cond = key[message_id]['condition']
    avg = {field: statistics.mean(x[field] for x in scored) for field in scored[0]}
    case_data[case][cond] = avg
metrics = ['accuracy_0to2','completeness_0to2','unsupported_claims_count','omitted_changes_count']
with (RESULTS / 'per_case_summary.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['case_id','condition','number_of_raters',*metrics])
    for case in sorted(case_data):
        for cond in ('A','B'):
            if cond not in case_data[case]: continue
            mid = next(k for k,v in key.items() if v['case_id']==case and v['condition']==cond)
            w.writerow([case,cond,len(ratings[mid]),*[case_data[case][cond][m] for m in metrics]])
paired = {case: x for case,x in case_data.items() if 'A' in x and 'B' in x}
print(f'Complete pairs: {len(paired)}; scored messages: {len(ratings)}')
with (RESULTS / 'comparison_summary.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['metric','n_paired_cases','mean_A','mean_B','mean_B_minus_A'])
    for metric in metrics:
        a = [x['A'][metric] for x in paired.values()]
        b = [x['B'][metric] for x in paired.values()]
        if not a: continue
        row = [metric,len(a),round(statistics.mean(a),3),round(statistics.mean(b),3),round(statistics.mean(y-x for x,y in zip(a,b)),3)]
        w.writerow(row); print(row)
print('Saved results/per_case_summary.csv and results/comparison_summary.csv. Positive B-A means B scored higher; for error counts, LOWER is better.')
