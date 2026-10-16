# 028r results

Verdict: **STILL INCONCLUSIVE**.

The requested rerun could not start: Colab refused both attempts to allocate a new L4 session with `precondition failed`. There were already two account assignments; neither was touched. This is an infrastructure failure, not evidence that either writing method is better.

| Measure | Result |
|---|---:|
| Planned notes, first round | 150 |
| Completed notes | 0 |
| Gemma judgments | 0 |
| Codex judgments | 0 |
| A/B wins, ties | unavailable |
| Exact binomial p-value | undefined |
| 95% / 97.5% confidence intervals | undefined (no trials) |
| Statistical rounds executed | 0 of at most 2 |
| Allocated GPU | none (L4 requested) |
| Experiment compute units | 0.00 |

The original result, 23/39, is historical context only and is not reused as new evidence. The preregistered note-level aggregation avoids counting four correlated judgments as four independent samples. Both presentation orders and the second judge were prepared but not executed. Swapping order balances presentation; it cannot guarantee all position effects disappear. Tied notes are explicitly reported and excluded from the conditional binomial win-rate test.

README.md records the hypothesis and rule written before allocation. Scripts copied from the original remain available, alongside synthetic topic generation and the two-order judge prompt. No private data were used. Both allocation failures, before/after usage and cleanup are recorded in results/allocation.txt. The same 181.30 CU balance and unchanged two assignments support zero usage by this experiment.

The requested scientific outcome remains unfinished. A fresh L4 allocation is needed to run the prepared pipeline, collect Codex judgments blind, and apply the preregistered rule; a statistical redesign round has not been consumed by allocation failures.
