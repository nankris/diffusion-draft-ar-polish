# 028r — Diffusion drafts versus AR direct

## Preregistered hypothesis and decision rule (before execution)
H1: DiffusionGemma draft → Gemma AR polish (A) beats Gemma AR direct (B) on synthetic Substack Notes.
Round 1 uses 150 new synthetic topics, the original prompts and model settings, on Colab L4. Each note receives four blind judgments: Gemma and Codex each see both candidate orders. A note is an A win if at least three judgments favor A, a B win if at least three favor B; 2–2 is a tie. The independent unit is the note, never the individual judgment. Exclude ties from the exact two-sided binomial test against p=0.5 and report exact binomial confidence intervals, ties and order agreement separately. PROVEN if A wins significantly; DISPROVEN if B wins significantly; otherwise STILL INCONCLUSIVE. To control two possible looks, each round uses alpha=.025 (97.5% exact CI; also report 95% CI).
If round 1 is inconclusive, redesign once: 150 additional harder synthetic topics requiring a concrete example and counterargument. Analyze this independent round with the same rule. Stop after two rounds. No retries selected by quality, no private data. Infrastructure failure is not evidence against H1 and must be reported honestly.

## Compute budget
At most 5 CU total. GPU requested: L4. Usage will be checked before/after; only this experiment's session will be stopped. No completed runs yet.

## Provenance
Copied pipeline.sh, setup_l4.sh, extract.py and topics.json from ../028-claude-diffusion-drafts/work/scripts. Original remains unchanged. The gap index says 028 was excluded while running; user supplies its final inconclusive result (23/39).

## Execution outcome
**STILL INCONCLUSIVE — infrastructure blocked, no new observations.** Two L4 allocation attempts were refused with `precondition failed` (capacity or active-session limit). These were allocation attempts, not statistical rounds. Neither round ran. Requested GPU: L4; allocated GPU: none. CU used: **0.00**; account balance before/after **181.30 / 181.30**. Other assignments were untouched. Explicit cleanup returned session not found. See results/allocation.txt.

The revised pipeline defaults to 150 topics and produces both AB and BA Gemma judgment prompts/output files. Codex judgments and statistical analysis remain unexecuted; no results are fabricated. Round 2 preparation currently reuses topic families with harder constraints and must be treated as a separate replication rather than pooled with round 1.
