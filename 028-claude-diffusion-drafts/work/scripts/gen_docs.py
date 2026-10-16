import json
d=json.load(open("results/summary.json")); S=d["summary"]; rows=d["rows"]; N=S["N"]
gpu_min=float(open("results/gpu_minutes.txt").read().split()[0])
cu=gpu_min*1.54/60
pipeA=S["t_C"]+S["t_A"]
ex=json.load(open("results/raw/colab_r028_pull.json"))["notes"]
tbl="\n".join(f"| {r['id']} | {r['winner']} | {r['wc_C']} | {r['wc_A']} | {r['wc_B']} | {r['t_C']:.1f} | {r['t_A']:.1f} | {r['t_B']:.1f} |" for r in rows)
open("README.md","w").write(f"""# #028 — Diffusion drafts + AR polish vs AR direct (Substack Notes)

## Question
Does drafting a short Substack Note with a diffusion LM (DiffusionGemma, `llama-diffusion-cli`) and then having an
autoregressive model polish it beat simply asking the autoregressive model to write the note directly?

## Setup
- **GPU:** Google Colab **L4** (session `claude-028`), llama.cpp built from source, all layers on GPU (`-ngl 99`).
- **Models:** DiffusionGemma GGUF (draft, 48 diffusion steps, `-n 512`); Gemma-4-26B-A4B-it UD-Q4_K_M (polish, direct write, judge).
- **Arms per topic** (topics in `work/scripts/topics.json`, prompt: 60–100 word plain-text Substack Note):
  - **A** = DG draft (C) → AR polish
  - **B** = AR direct
  - **Judge:** same AR model, blind pairwise A vs B, order randomized per note (seeded), `WINNER: X|Y`.
- AR settings: `--chat-template gemma` (avoids thinking output), temp 0.7, `-n 300`.
- Pipeline: `work/scripts/pipeline.sh`; analysis: `work/scripts/analyze.py`; raw pulled outputs: `results/raw/colab_r028_pull.json`.
- Run was planned for 50 notes and cut off at the time budget: **{N} notes completed**.

## Compute
- L4 session allocated 04:02–05:00 IST = **~{gpu_min:.0f} min** (setup/build ~12 min, 3 aborted launches ~13 min, final pipeline run 04:27–05:00 = 33 min).
- **CU estimate = {gpu_min:.0f} min × 1.54 / 60 ≈ {cu:.2f} CU** (whole session).

## Results (n={N})
| Metric | A: DG draft → AR polish | B: AR direct |
|---|---|---|
| Judge wins | **{S['A_wins']}** ({100*S['A_wins']/N:.0f}%) | **{S['B_wins']}** ({100*S['B_wins']/N:.0f}%) |
| Mean words (final) | {S['wc_A']:.1f} | {S['wc_B']:.1f} |
| In 60–100 word range | {S['inr_A']}/{N} | {S['inr_B']}/{N} |
| Mean wall time / note (s) | {pipeA:.1f} (draft {S['t_C']:.1f} + polish {S['t_A']:.1f}) | {S['t_B']:.1f} |

Unparsed judge verdicts: {S['unparsed']}. Judge picked position X {S['x_picks']}/{N} times (no strong position bias).
DG drafts alone: mean {S['wc_C']:.1f} words, {S['inr_C']}/{N} in range.

![chart](results/chart.png)

See `writeup.md` for discussion and caveats.

### Per-note
| id | winner | words C | words A | words B | t C (s) | t A (s) | t B (s) |
|---|---|---|---|---|---|---|---|
{tbl}
""")
print("README ok", round(cu,2))
