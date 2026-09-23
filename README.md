# Auto-claims classification: Jev, Laya, and a Luna baseline

Research and implementation pilot, 2026-09-22. All people, identifiers, organizations, events, and documents are fictional. OpenRouter is used **only for Jev**. The cumulative OpenRouter test budget is **$0.05**; measured spend so far is **$0.004183704** across 30 successful calls. No paid LLM inference was made through OpenRouter.

**Initial result:** Jev correctly classified 10/10 short examples; default English Laya classified 7/10. This is a smoke test, not evidence of production accuracy or a general ranking. GPT-5.6 Luna also classified 10/10 correctly through the existing Codex ChatGPT login, with no tool calls. The current assistant's own labels are not presented as independent Luna predictions.

- [Published input types and context limits with evidence](MODEL_CAPABILITIES.md)
- [One-page executive comparison including model constraints](reports/2026-09-22-Classification-Executive-One-Page.pdf)
- [Executive report with findings, confidence scores, and sample documents](reports/2026-09-22-Auto-Claims-Classification-Executive-Report.docx)
- [Complete confusing-category examples](BOUNDARY_DOCUMENTS.md)
- [Native confidence and probability results](results/confidence-details.md)
- [Full implementation plan and explanation](RESEARCH_PLAN.md)
- [Ten readable synthetic documents with expected categories](SYNTHETIC_DOCUMENTS.md), also individually available in `data/documents/`
- [Short-document comparison](results/comparison.md)
- [Long-document comparison](results/length-comparison.md)
- [Machine-readable summary](results/summary.json)
- [Budget ledger](results/openrouter-spend.json)

## What is implemented

`scripts/benchmark.py` calls the OpenRouter Decisions endpoint for pinned `typesafe/jev-1.13`, or local `convaiinnovations/laya`. Both receive the same document text, category definitions, and classification question. Gold labels and document ids are not sent to either model. There are 10 document categories plus an `other` fallback. The fallback has no positive example in this tiny smoke set.

The Jev adapter checks the advertised price before running, restricts routing to TypeSafe with price ceilings, reserves $0.002688 before every call (64k input tokens at the published rate), logs actual reported costs, and stops before the next reservation would exceed $0.05. It makes no automatic retries. An uncertain request retains its reservation. One process at a time can spend against the ledger. This is an application budget guard, not a change to the account-wide OpenRouter spending limit; leave the ledger in place.

The Laya prefix mode deliberately preserves the package's default truncation behavior and reports it. Chunk mode uses 316-token windows with 32-token overlap and validates that each re-encoded chunk fits the 324-token document allowance for our question. It selects the strongest non-`other` winning chunk, falling back to `other` if every chunk returns `other`. This is an exploratory evidence-pooling heuristic, not a calibrated document probability or a production-ready packet classifier.

## Reproduce

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements-lock.txt
python3 scripts/make_data.py

# env. or .env: OPENROUTER_API_KEY=... (never commit this file)
.venv/bin/python scripts/benchmark.py jev --out results/jev-smoke.jsonl

# First run downloads the Laya checkpoint; following runs use the local cache.
.venv/bin/python scripts/benchmark.py laya --out results/laya-smoke.jsonl
HF_HUB_OFFLINE=1 .venv/bin/python scripts/make_stress.py
.venv/bin/python scripts/benchmark.py jev --data data/length_stress.jsonl --out results/jev-stress.jsonl
HF_HUB_OFFLINE=1 .venv/bin/python scripts/benchmark.py laya --data data/length_stress.jsonl --out results/laya-stress-head.jsonl
HF_HUB_OFFLINE=1 .venv/bin/python scripts/benchmark.py laya --mode chunks --data data/length_stress.jsonl --out results/laya-stress-chunks.jsonl
python3 scripts/summarize.py
```

Existing output ids are skipped. Use a new output filename for a new experiment; the spend ledger remains cumulative. Do not reuse output files after changing the input or taxonomy. `requirements-lock.txt` captures the installed packages; `results/run-manifest.json` records the downloaded checkpoint revision. The current Laya loader resolves the latest checkpoint on first download, so use the recorded cached snapshot path when exact weight reproducibility matters.

## Completed Luna baseline

`python3 scripts/prepare_luna.py` creates a shuffled, blinded prompt and output schema without invoking a model. The prepared ten-document batch keeps Codex usage small. It asks for labels only and forbids tools or access to gold labels/results. Batched Codex output can compare correctness, but its total wall time includes Codex startup and a different serving stack; it is not a fair per-document latency comparison with Jev.

The completed baseline used this invocation, with an empty temporary directory supplied via `--cd /tmp/jev-luna-blind`:

```bash
codex exec --ignore-user-config --ephemeral --skip-git-repo-check \
  --sandbox read-only --model gpt-5.6-luna \
  -c model_reasoning_effort='"none"' \
  --output-schema data/luna-output-schema.json \
  --output-last-message results/luna-predictions.json \
  - < data/luna-blind-prompt.txt
```

This uses the existing Codex authentication and allowance, not the OpenRouter key. The baseline completed with 14,756 input tokens, 134 output tokens, and no reasoning output tokens. The input count includes Codex overhead. No dollar charge is asserted for this subscription-allowance usage. A production harness should enforce tool restrictions mechanically, use one document per independent request, and record the serving model/version rather than relying only on a prompt.

## Verification

Four offline spend-guard tests passed (`python3 scripts/test_budget.py`), covering budget exhaustion, price increases, credential-free payload checks, and unknown-cost reservations. Result scoring, unique ids, all 30 actual Jev charges, and the absence of Luna tool calls were also verified.

## Completed long-input follow-up

All three models received identical text for 12 probes at about 1k, 4k, 5k, and 16k Laya tokens, each with evidence at the start, middle, and end. Jev and Luna scored 12/12; default Laya scored 4/12; chunked Laya scored 12/12. The 5k probes were 5,003–5,004 tokens: Jev and Luna 3/3, default Laya 1/3, chunked Laya 3/3 (18 chunks). Luna used 12 independent Codex calls, reasoning none, empty working directories, no tools, and no gold labels or competing predictions. See `results/luna-length.jsonl`, its per-call logs, and `results/length-comparison.md`. CLI timings include overhead and are not intrinsic model latency. These probes reuse one police report in repeated neutral filler and do not establish production accuracy.

## Boundary and confidence follow-up

Eight additional short boundary cases scored Jev 8/8, Luna 8/8, Laya 4/8. Complete inputs and frozen gold labels: BOUNDARY_DOCUMENTS.md. These are targeted diagnostics designed after initial errors, not a random held-out evaluation. Native confidence, selected-label probability, full distributions, and Laya action fields are exported in results/confidence-details.json and .md; native confidence is not validated correctness probability. All Laya inputs fit without truncation. Total cumulative Jev spend is $0.004183704 across 30 calls, under the $0.05 cap.

## Public evidence package

Provider request identifiers and Codex task identifiers have been removed from retained response logs. Predictions, confidence values, usage totals, input hashes, and model versions are preserved. Git authorship uses a GitHub noreply address.

Luna API-equivalent cost estimate: **$0.049142** using recorded cached usage, or **$0.067113** without cache discounts. This is not an actual Codex charge. Calculation and pricing source: `results/luna-cost-estimate.json`.

## OpenJev follow-up on 23 September

OpenJev FP8 community demo: **2/2 scored initial documents correct; run incomplete**. The third call hit anonymous ZeroGPU quota. Boundary and length probes remain untested. This route uses a different prompt and uncalibrated letter softmax, not the official helper. No paid fallback was used. See [method and constraints](OPENJEV_EVALUATION.md), `results/openjev-demo.jsonl`, and `results/openjev-demo-errors.jsonl`. The executive visual now prominently shows **chunked Laya 12/12 correct** on long probes, with prefix-only behavior as a control.
