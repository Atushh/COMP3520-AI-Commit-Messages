# COMP 3520 — Idea #9 beginner starter kit

This is a **starter**, not a completed assignment. You must perform real commits, run real AI prompts, assess actual messages, review genuine scholarly sources, and write an honest paper.

## Question and conditions

**Question:** Does providing issue/task context alongside a Git diff improve the factual accuracy and completeness of AI-generated commit messages compared with providing the same diff alone?

- **A (baseline):** Git diff only.
- **B (treatment):** Same Git diff and a short issue/task description.
- Evaluate identical commits for both conditions, using the same AI model and comparable settings.

## Install tools

- Git for Windows (includes Git Bash)
- Python 3 (check with `python --version` or `py --version`)
- VS Code (optional, but helpful)
- A free AI chat tool, with its name/model recorded. No API key is needed.

## GitHub setup and sample changes

1. Extract this kit and open the `COMP3520_Idea9_Starter` directory in VS Code.
2. Open terminal in that directory (the one containing `README.md`).
3. Run `git init`, `git branch -M main`, `git add .`, `git commit -m "Start research project"`.
4. Create a **private or public** GitHub repository; make sure the instructor can access it. Link the repo as a remote with `git remote add origin YOUR_URL`; then `git push -u origin main` (authenticate as prompted).
5. Before each source-code change, write a short task/issue description and intended change; keep it as independent reference information.
6. Edit one or a few lines under `sample-project/`, run a basic sanity check, then commit each coherent change separately (e.g. `git add sample-project/ && git commit -m "Handle divide by zero"`). Make sure every commit in your dataset actually changes files under `sample-project/`.
7. Find source commit hashes using `git log --oneline -- sample-project/` and enter each relevant hash (short unique hash works) in `data/cases.csv` with its **case_id**, **issue_context**, **expected_changes**, and **author**. Do not include the starter commit unless it is a genuine eligible change.
8. Aim for 30 small, purposeful commits; each person can contribute 15. Do not artificially duplicate the same edit to inflate the sample. You can add Java classes or methods for realistic tasks. Document sampling choices and limitations. Keep `issue_context` as a genuine task description, not a description rewritten after seeing generated messages.

## Generate the prompt files

From this directory run:

```bash
python scripts/prepare.py
```

If `python` is not recognized on Windows, try `py scripts/prepare.py` instead.

This creates `prompts/C01_A.txt`, `prompts/C01_B.txt`, etc., plus `data/outputs.csv`. **It will overwrite outputs.csv if rerun**. Do not rerun it after collecting responses.

## Manually collect actual AI responses

1. Use the SAME model for all prompts, recording its name/version, date, and settings if available.
2. For each prompt `.txt`, start a fresh AI conversation or a controlled fresh context; paste the entire prompt unchanged.
3. Copy the actual generated subject line into the matching `generated_message` cell in `data/outputs.csv`.
4. Record failures, refusals, noncompliant formatting, and any corrections; **never secretly edit an output to improve it**.
5. Record time/cost only if you can reliably measure them. Manual responses are valid if your study clearly calls this a *semi-automated, reproducible workflow* with human-operated AI access; disclose reproducibility limitations and save all original prompts and outputs.

## Create anonymous evaluation sheets

After every output is filled in, run:

```bash
python scripts/make_rating_sheet.py
```

This produces:
- `data/blind_messages.csv` — message IDs, case IDs, and raw AI messages, **without condition labels**
- `data/condition_key.csv` — condition labels. Hide from raters until all ratings are final.
- `data/ratings_Jimmy.csv` and `data/ratings_Terrence.csv` — separate sheets.

For EACH case, consult its actual Git diff and your independent `issue_context` and `expected_changes` from `data/cases.csv`. For example, view the diff with:

```bash
git show --format= COMMIT_HASH -- sample-project/
```

Use the **same ground truth** for A and B. Define a clear rubric before scoring:
- `accuracy_0to2`: 0 = inaccurate, 1 = partly accurate, 2 = accurate.
- `completeness_0to2`: 0 = misses main change, 1 = partial, 2 = covers essential change(s).
- `unsupported_claims_count`: number of specific claims unsupported by actual diff and task evidence.
- `omitted_changes_count`: number of important intended changes missed.

Fill **all four** scoring columns for each rated message; zero is valid. Each member should independently score at least a shared subset (e.g. 10 cases × 2 messages) and discuss disagreements **after** recording independent ratings. Score more cases if feasible. If only one rater scores other cases, disclose that in the paper. Recording independent ratings for all 60 messages per rater is preferable and feasible for short changes.

## Analyze measured results

Run:

```bash
python scripts/analyze.py
```

Outputs:
- `results/per_case_summary.csv`
- `results/comparison_summary.csv`

The analysis averages multiple rater scores per message where both scored it; then computes paired case comparisons. For accuracy and completeness, **higher is better**. For unsupported claims and omissions, **lower is better**. The results script does not compute statistical significance; do not claim statistical significance without additional justified testing. Keep raw ratings.

## Research paper / submission

Required PDF sections: title/authors, abstract/keywords, introduction and industry relevance, research question, background/related studies with a literature comparison table, methodology, implementation, results/discussion, limitations and threats to validity, conclusion/future work, references, team contributions, AI-use disclosure, clickable repo URL, and **final Git commit hash**.

Search scholarly work published 2010–2026, **read and verify** papers, compare methods/datasets/results/limitations, and cite consistently. No mandatory number of papers is stated. Make a credible, sufficiently broad survey.

Submit **three items** by **November 18, 2026**: research paper PDF, accessible GitHub repo link, and ZIP containing the **same commit snapshot** with code, data, prompts, raw ratings, analysis, instructions and results. Exclude credentials/downloaded dependencies. Verify the ZIP extracts and scripts run on a second machine or fresh folder. Include the final commit hash in the paper. Record when the AI model/tool was used and its role.

**Important limitations:** Human-operated AI calls are not fully automatic; AI tools may change between runs; your small, self-created code changes cannot support broad industry-wide claims. Declare these openly.
