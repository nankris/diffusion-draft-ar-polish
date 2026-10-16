# #028 writeup: diffusion drafts → AR polish

## What I tested
For each short-form topic (Substack Note, 60–100 words), I compared two arms:
- **A:** DiffusionGemma writes a draft with `llama-diffusion-cli` (48 steps), then Gemma-4-26B-A4B (AR) polishes it.
- **B:** Gemma-4-26B-A4B writes the note directly.

The same AR model judged A against B blind, with the order of the two notes shuffled per note. Everything ran on one
Colab **L4**. The run was planned for 50 topics and stopped at the time budget after **39**.

## Results
- **Preference:** A won **23/39 (59%)** and B won 16/39. A two-sided sign test gives p ≈ 0.34, so the difference
  **is not significant** at this n. Read it as "polishing a diffusion draft is at least not worse", not as a win.
- **Position bias:** the judge picked slot X in 18/39 cases, so there is no obvious bias.
- **Length:** A's notes averaged 87 words and B's 81. The longer note won only 19/39, so length does not explain the result.
- **Format compliance (60–100 words):** A 36/39, B 38/39, raw DG drafts 31/39. The drafts tend to run short (68 words on average),
  and the polish step mostly fixes that.
- **Cost:** A takes ~30.9 s per note (DG draft 21.0 s + polish 9.8 s) and B takes ~9.6 s, so **A is about 3.2× slower**. The DG time
  includes loading the model on every call, and that is likely a large share of the 21 s. A persistent diffusion server
  would narrow the gap, but this run did not measure it.

## Qualitative
With the gemma chat template, the DG drafts were coherent and on-topic (for example, n05 on SQLite and n13 on rewrites) and needed little
cleanup. Earlier launches (#1–#3) produced garbled or "thinking"-channel output until `--chat-template gemma` was used
for the AR calls. `extract.py` also handles unclosed thought blocks on the DG canvas.

## Caveats
- Single judge, and the judge is the same model that wrote B and polished A (self-preference could cut either way).
- One sample per arm per topic, temperature 0.7, and n=39.
- Wall times are per CLI invocation and include model load, not steady-state throughput.
- The sandbox rebooted at ~04:28 IST and killed the local driver. The Colab pipeline kept running independently, and all 39
  results were pulled from the session at 05:00 IST (`results/raw/colab_r028_pull.json`).

## Compute
L4 session from 04:02 to 05:00 IST ≈ 58 min → **≈ 1.49 CU** (58 × 1.54 / 60). The final pipeline run itself took 33 min.

## Verdict
Diffusion-drafting followed by AR polish produced notes the judge slightly preferred (59%, not significant) at about 3× the wall time.
For this task it is not worth the extra latency unless the diffusion model's load cost is amortized. A follow-up would use more
topics, an independent judge, and a resident DG process.
