# Blind run matrix-2026-07-31

- 20 case(s), shuffle seed 2026.
- Evaluator/reviewer runs read ONLY `inputs/` + `params/`.
- `.secret/mapping.tsv` maps blind_id -> case_id and is for the COMPARATOR ONLY. Do NOT mount it into an evaluator run.
- Nothing here exposes expected verdicts or class-name directories.
