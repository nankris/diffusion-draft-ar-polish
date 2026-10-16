import json,pathlib
r=pathlib.Path(__file__).resolve().parents[1];s=json.loads((r/'results/summary.json').read_text());rows=json.loads((r/'results/notes.json').read_text());l=s.get('latency');counts=s['counts']
fmt=lambda ci:'unavailable' if ci is None else f'[{ci[0]:.4f}, {ci[1]:.4f}]'
text=f'''# Experiment 028 round 3

Verdict: **{s['verdict']}**. The endpoint is quality preference for DiffusionGemma draft → Gemma AR polish (A) against Gemma AR direct (B), with one note-level majority from Grok and Codex judging both orders.

| Measure | Result |
|---|---:|
| Planned notes | 150 |
| Completed generation pairs | {s['generated']} |
| A wins / B wins / 2–2 ties | {counts.get('A',0)} / {counts.get('B',0)} / {counts.get('tie',0)} |
| Incomplete or invalid notes | {counts.get('incomplete',0)} |
| Decisive notes | {s['decisive']} |
| A win rate among decisive notes | {s.get('win_rate','unavailable')} |
| Exact two-sided binomial p | {s.get('pvalue','unavailable')} |
| 95% exact confidence interval | {fmt(s.get('ci95'))} |
| 90% exact interval for equivalence | {fmt(s.get('ci90'))} |
| Exact TOST p, 45–55% band | {s.get('tost_pvalue','unavailable')} |
| Final notes in 60–100 words, A / B | {sum(60<=x['A_words']<=100 for x in rows)} / {sum(60<=x['B_words']<=100 for x in rows)} |
'''
if l:
 text+=f'''| Mean A latency | {l['A_mean']:.2f} s |
| Mean B latency | {l['B_mean']:.2f} s |
| Paired mean difference, 95% bootstrap CI | {l['difference']:.2f} s {fmt(l['difference_ci95'])} |
| Ratio of means, 95% bootstrap CI | {l['ratio']:.3f} {fmt(l['ratio_ci95'])} |
'''
for e in ['grok','codex']:
 a=s[e+'_order_agreement'];text+=f"| {e} agreement across reversed orders | {a['agree']} / {a['n']} |\n"
text+='''
The independent unit is the note. Four correlated votes are never counted as four trials. A 2–2 note is reported as tied and excluded from the conditional binomial preference estimand. Missing or malformed judgments are not imputed. The exact test is a single final look after generation ends, with no quality-based regeneration or selection. The 95% Clopper–Pearson interval describes preference among decisive notes; it does not describe unconditional preference across all topics.

The requested equivalence band is preserved. At 150 decisive notes, zero possible win counts pass exact 5% TOST for 45–55% equivalence. Exact superiority power at a true 60% preference is 66.3%; at 65% it is 95.5%. About 900 decisive notes give 80.6% equivalence power at a true 50% preference. The fixed n=150 and narrow equivalence band cannot deliver likely conclusive outcomes in both directions. Nonsignificance is not evidence of equivalence. Any residual uncertainty is reported rather than relabeled.

Latency includes CLI startup, model loading, and generation; A adds both draft and polish. It excludes synchronization and external judging. The paired bootstrap resamples notes 10,000 times with seed 2803. Its intervals are conditional on this run and do not estimate hardware-session variability. Timing comparisons may also reflect cold caches and recovered sessions; generation order alternates by note.

The first saved round-3 run had 32 complete pairs and was interrupted; it was recovered from durable outputs, not pooled with earlier experiments. The original topic list and seeded generation settings were restored from the preregistered Git revision. Prior raw outputs remain in results/raw and resumed copies are in results/raw/r3028. The interim replacement topic list generated no observations. The recovery used additional sequential L4 allocations because earlier runtimes ended; this deviates from completing all 150 notes in one uninterrupted session. Control errors, kernel restart, build recovery, and batch copies are retained in the logs. The old and resumed code revision is recorded in results/metadata.json and results/raw/setup_logs/commit.txt.

Judges see anonymous X/Y candidates, topic, and rubric, with mapping stored separately. Both orders are judged. The same two model families can have shared preferences, and reversing order exposes rather than eliminates order sensitivity. Synthetic topics and hypothetical examples are public-only data; results apply to this task, prompting, models, quantizations, and judges.

![Results and latency](chart.png)
'''
if (r/'results/compute.json').exists():
 c=json.loads((r/'results/compute.json').read_text());text+=f"\nGPU: {c['gpu']}. Conservative experiment CU estimate: **{c['estimated_cu']:.3f}**, from this experiment's session lifetimes × 1.54 CU/hour; account-wide balance changes include other work and are not attributed to this experiment. All own sessions have been stopped.\n"
if s['generated']<150:text+='\nThe 150-note target was not reached before the remaining time/compute budget ended after runtime failures. Incomplete generation is visible in the counts; no missing observations were fabricated.\n'
(r/'writeup.md').write_text(text)
