import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
with (DATA / 'outputs.csv').open(newline='', encoding='utf-8-sig') as f:
    outputs = list(csv.DictReader(f))
if not outputs or any(not x['generated_message'].strip() for x in outputs):
    raise SystemExit('First complete every generated_message in data/outputs.csv.')
# Opaque IDs and deterministic shuffled order help reduce condition-order bias.
items = []
for x in outputs:
    opaque = hashlib.sha256(f"COMP3520-study-{x['case_id']}-{x['condition']}".encode()).hexdigest()[:12]
    items.append((opaque, x))
items.sort(key=lambda pair: pair[0])
with (DATA / 'blind_messages.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['message_id', 'case_id', 'generated_message'])
    w.writeheader()
    for opaque, x in items:
        w.writerow({'message_id': opaque, 'case_id': x['case_id'], 'generated_message': x['generated_message']})
with (DATA / 'condition_key.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['message_id', 'case_id', 'condition'])
    w.writeheader()
    for opaque, x in items:
        w.writerow({'message_id': opaque, 'case_id': x['case_id'], 'condition': x['condition']})
for rater in ('Jimmy', 'Terrence'):
    with (DATA / f'ratings_{rater}.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['message_id', 'accuracy_0to2', 'completeness_0to2', 'unsupported_claims_count', 'omitted_changes_count', 'notes'])
        w.writeheader()
        for opaque, _ in items:
            w.writerow({'message_id': opaque, 'accuracy_0to2': '', 'completeness_0to2': '', 'unsupported_claims_count': '', 'omitted_changes_count': '', 'notes': ''})
print('Created blind_messages.csv, condition_key.csv, and separate rating sheets. Hide condition_key.csv from raters until scores are finalized.')
