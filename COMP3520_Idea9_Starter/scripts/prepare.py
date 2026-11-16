import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
PROMPTS = ROOT / 'prompts'

def git_diff(commit):
    command = ['git', '-C', str(ROOT), 'show', '--format=', '--no-ext-diff', commit, '--', 'sample-project/']
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(f'Cannot read commit {commit}: {result.stderr.strip()}')
    if not result.stdout.strip():
        raise ValueError(f'Commit {commit} has no changes in sample-project/.')
    return result.stdout

def main():
    with (DATA / 'cases.csv').open(newline='', encoding='utf-8-sig') as f:
        cases = list(csv.DictReader(f))
    selected = [x for x in cases if x['commit_hash'].strip()]
    if not selected:
        raise ValueError('Fill in commit_hash and issue_context in data/cases.csv first.')
    PROMPTS.mkdir(exist_ok=True)
    outputs = []
    for x in selected:
        case = x['case_id'].strip()
        issue = x['issue_context'].strip()
        if not issue:
            raise ValueError(f'{case} is missing issue_context.')
        diff = git_diff(x['commit_hash'].strip())
        if len(diff) > 30000:
            raise ValueError(f'{case}: Git diff is too big; use smaller changes.')
        intro = ('Write one concise, factual Git commit message (subject line only, maximum 72 characters) '
                 'for the code change shown below. Do not invent changes or motivations. '
                 'Return only the commit message.\n\n')
        (PROMPTS / f'{case}_A.txt').write_text(intro + 'Git diff:\n' + diff, encoding='utf-8')
        (PROMPTS / f'{case}_B.txt').write_text(intro + 'Issue/task context:\n' + issue + '\n\nGit diff:\n' + diff, encoding='utf-8')
        outputs += [{'case_id': case, 'condition': cond, 'generated_message': ''} for cond in ('A', 'B')]
    with (DATA / 'outputs.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['case_id', 'condition', 'generated_message'])
        writer.writeheader(); writer.writerows(outputs)
    print(f'Created {2*len(selected)} prompt files and data/outputs.csv. Run AI prompts manually, then fill in its messages.')
    print('IMPORTANT: Running prepare.py again overwrites outputs.csv; do not rerun after filling results.')

if __name__ == '__main__':
    main()
