# Jev and Laya for auto-insurance document classification

Prepared 2026-09-22. Read the results as a low-cost feasibility pilot. Model documentation and prices can change.

## Recommendation

Start with **Jev as the narrow document-type classifier**, retain a general LLM for ambiguous or compound documents, and test Laya if local deployment is important. Our tiny experiment favors Jev over default English Laya, but does not establish a production winner. Luna matched Jev on these ten examples; complete a representative held-out evaluation before deciding.

Keep three separate jobs in the design: determining a document's type, extracting facts from it, and making a claim-handling decision. A document classification model need not adjudicate coverage or liability to route a medical bill correctly.

## How the mechanisms differ

| Aspect | Jev | Laya | GPT-5.6 Luna |
|---|---|---|---|
| Interface | Text state plus typed question and candidate answers | Similar typed decision interface | Prompt plus generated answer, ideally constrained JSON |
| Output | Choice, score, or boolean-like probability | Choice, score, or boolean-like probability | Generated label/JSON, and optionally an explanation |
| Computation | Vendor describes a non-generative decision model; internals are not fully disclosed | Bidirectional encoder plus trained decision head that scores options | Autoregressive language generation; may use reasoning according to configuration |
| Domain adaptation | Supply definitions, rules, context, examples in each request | Same, plus local fine-tuning is possible | Instructions, definitions, examples, and retrieved context |
| Likely benefit | Cheap, focused decisions and distributions | Local execution and control over weights | Flexible reasoning, extraction, explanation, long context |
| Main caution | Can misclassify; structured output does not guarantee truth | Default truncation and poor transfer can be substantial | Generated JSON does not by itself establish calibrated uncertainty |

Both approaches must read the input. Avoiding output-token generation reduces one source of work; it does not make a very long document free to process. A short label-only LLM answer is already much cheaper than requesting a long explanation. Compare against that efficient baseline.

Laya's implementation builds a sequence containing instructions, candidate labels/descriptions, and document text. It scores option markers and normalizes those scores. New category names are provided at inference time, unlike a traditional classifier with a permanently fixed output label set. However, understanding a new category and being accurate on it are different claims. The upstream model card explicitly cautions that its strongest typed-decisions results use a specialized checkpoint and are not the base model's general zero-shot performance. [Laya model card](https://huggingface.co/convaiinnovations/laya), [source repository](https://github.com/NandhaKishorM/laya).

Jev exposes these decisions through its own endpoint and OpenRouter's separate Decisions API. The first general text-model catalog lookup omitted it; the user-provided alias correctly identified it. We verified the actual route and successfully called it. [OpenRouter Jev listing](https://openrouter.ai/typesafe/jev-1.13), [OpenRouter Decisions implementation](https://github.com/OpenRouterTeam/typescript-sdk/blob/main/src/funcs/alphaDecisionsCreate.ts).

## Where the knowledge comes from

These models do not start from an empty collection of your ten examples. They already have learned language representations and decision behavior encoded in their weights. Your request supplies the document and the meaning of each allowed category. For example, `demand_letter` means a request to settle an injury claim; `subrogation_notice` means recovery of money an insurer already paid. This gives the model a boundary to apply.

TypeSafe describes Jev as using **reinforcement learning for calibrated decisions (RLCD)** on pretrained language-model capabilities. Its public material does not identify a complete training corpus, exact base model, or every internal architectural detail. It would be unjustified to claim that it is a specific BERT architecture or that it was trained on insurance files. TypeSafe says the same Jev weights serve all accounts; customer specialization currently happens through the request rather than per-account fine-tuning. [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer), [models and customization](https://docs.typesafe.ai/models).

Laya discloses an English ModernBERT-large backbone and a decision head, with additional decision training. Broad pretraining supplies language patterns; later training shapes how options and uncertainty are scored. Neither model automatically knows your private document taxonomy or proprietary claims procedures. Supply those definitions explicitly, or train a suitable local model on a separate labeled training split.

**The ten synthetic documents here are evaluation examples, not training data.** No model was fine-tuned, no prediction was corrected by changing a prompt after inspection, and gold labels were excluded from the inference payloads. If examples are later used to tune prompts or weights, reserve new documents for evaluation.

A probability distribution is useful but is not proof of calibration on claims documents. Jev's `confidence` is a separate field from a class probability. Laya's implementation also derives its confidence field from the distribution. Do not assume the same numeric threshold has the same meaning across providers. Our Laya runtime warned that a shipped temperature for 11+ options was outside its accepted range and clamped it; treat the reported probabilities as uncalibrated here.

## The ten examples

| ID | Expected category | Identifying purpose |
|---|---|---|
| doc_01 | police_report | Officer records scene observations, statements, and citation |
| doc_02 | demand_letter | Attorney proposes $28,000 settlement with a response date |
| doc_03 | medical_bill | Provider lists services, charges, adjustments, and balance |
| doc_04 | medical_record | Clinician records symptoms, examination, assessment, and plan |
| doc_05 | repair_estimate | Body shop proposes parts, labor, and repair costs |
| doc_06 | rental_invoice | Rental company bills temporary transportation dates and rates |
| doc_07 | witness_statement | Independent witness recounts the collision in first person |
| doc_08 | coverage_letter | Insurer communicates a reservation of rights |
| doc_09 | subrogation_notice | Insurer requests recovery of a prior payment and deductible |
| doc_10 | settlement_release | Signed agreement releases specified injury claims |

Full text is in `data/documents/`; labels and rationale are in `data/documents.jsonl`. The names and numbers are fictional; these documents are not legal or medical templates. All examples are English and text-only. Some contain unusually explicit purpose statements and distinctions from neighboring document types, making this an easy first integration test. There is just one example per positive category, no positive `other`, no OCR corruption, and no mixed packet.

Measured smoke results:

| Model / route | Correct | Median observed time | API charge |
|---|---:|---:|---:|
| Jev 1.13 through OpenRouter | 10/10 | 0.251 s/document | $0.000342846 total |
| Laya English default, local CPU, four threads | 7/10 | 0.389 s/document | None; local compute still has a cost |
| GPT-5.6 Luna through Codex, reasoning none | 10/10 | Not comparable: one batch | Codex allowance, no OpenRouter calls |

Laya predicted `settlement_release` for the demand, `police_report` for the witness account, and `demand_letter` for the insurer recovery request. These are semantically neighboring classes worth oversampling in a real evaluation. Warmup and model loading were excluded from local per-document latency; network round trip was included in Jev latency. These are single observations on different infrastructure, not an intrinsic speed ranking. Raw predictions, distributions, durations, token usage, and actual Jev costs are preserved in `results/`.

## Long input: the thresholds are very different

| Model/configuration | Published or observed capacity | Meaning for documents |
|---|---|---|
| Jev 1.13 direct API | 64k tokens across the request; 32k for state plus the longest question | A single long document cannot use the entire 64k allowance |
| Jev via OpenRouter | Endpoint metadata lists 32,000 context | Leave space for question and options; don't design around a 64k document |
| Laya English default | 512 total; actual document allowance **324 tokens** with this question | Longer documents are silently clipped at the end by the installed SDK |
| Laya multilingual / typed-decisions defaults | Model card lists 1,024 total, approximately 768 for state | Different checkpoints/configurations; not tested here |
| GPT-5.6 Luna | Official documentation lists 1,050,000 context | Reserve space for instructions and output; long context does not guarantee accurate retrieval |

Sources: [TypeSafe limits](https://docs.typesafe.ai/models), [OpenRouter endpoint](https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints), [Laya configurations](https://huggingface.co/convaiinnovations/laya), [Luna model documentation](https://developers.openai.com/api/docs/models/gpt-5.6-luna). Our 324-token value was computed from the actual installed tokenizer and sequence builder, not a word-count approximation.

There is **no universal short-input requirement for decision models**. It is a property of the particular model and implementation. Count tokens with the relevant tokenizer; word counts and page counts are only rough proxies. Laya's backbone can support configurations longer than the packaged decision default, but increasing a config value does not demonstrate reliable long-context behavior. Validate the decision head, supported positions, memory, and quality together.

The nine length probes embed the same police-report example among neutral administrative filler, at the beginning, middle, or end of approximately 1,024, 4,096, and 16,384 Laya tokens. This category was chosen because both models recognized the short original. Jev recognized all nine. Prefix-only Laya recognized the three beginning-position cases and returned `other` for the six middle/end cases. The latter cases are input-loss failures: the informative section never reached the model. These nine variants are correlated diagnostics, not nine independent documents or an estimate of general long-document accuracy. Repeated neutral filler is much easier than real, conflicting exhibits.

Chunked Laya recovered all nine cases, taking about 1.6–1.7 seconds at 1k tokens, 6.4–6.5 seconds at 4k, and 25.2–25.4 seconds at 16k on this CPU configuration. The chunk experiment is recorded separately in `results/length-comparison.md`. It preserves all text in overlapping windows and pools evidence, with more computation per document. Max-evidence pooling can also latch onto an irrelevant quoted document or one overconfident chunk. A demand packet containing real medical bills, records, and a police report needs **document boundaries and a packet-level policy**, not a blind majority vote across pages. TypeSafe also warns that irrelevant long context and adversarial content can degrade Jev's answers even within supported length. [Jev limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13).

## Implementation sequence

1. **Define the classification unit and taxonomy.** Begin with one standalone document and exactly one primary type. Give each category a definition and hard boundary examples, retain `other`, and record the taxonomy version. For packets, split documents or return multiple document segments before assigning any packet-level label.
2. **Normalize and budget inputs.** Preserve page/section boundaries, remove repeated headers cautiously, compute token counts, and prohibit silent truncation in the production wrapper. Record whether each decision used a full document, excerpt, or chunks. Text-only input avoids an OCR confound during the first pilot.
3. **Run the three adapters against identical held-out documents.** Use Jev's Choice endpoint; use Laya with recorded checkpoint and token configuration; use Luna with label-only structured output and explicitly recorded reasoning effort. The prepared Codex batch is a cheap correctness baseline; use independent API calls later for a controlled serving comparison if authorized.
4. **Evaluate complete processing strategies.** Compare full Jev/Luna input, Laya prefix control, Laya chunks, and optionally a longer Laya configuration. An LLM-generated summary plus Laya must be reported as a combined pipeline, including summary cost, latency, and evidence loss—not as Laya alone.
5. **Measure useful errors.** On a larger set, report macro-F1, per-category precision/recall, confusion matrix, invalid outputs, abstention/review rate, and correctness among automatically accepted decisions. Measure warm/cold latency, throughput at realistic concurrency, and cost per document and per correctly routed document. Evaluate probability calibration on a separate validation set; ten examples cannot establish it.
6. **Calibrate escalation.** Tune thresholds on validation data to the operational error/review target. Escalate insufficient evidence, disagreement between sections, mixed packets, and weak classifications to Luna or a reviewer. Keep arithmetic/date rules in code. Preserve input hashes, model versions, taxonomy, evidence locations, predictions, and costs for audit.
7. **Expand beyond the pilot.** Target 20–50 examples per document category, including overlapping terminology, missing headings, OCR damage, unknown types, empty text, quoted classification instructions, medical-record/bill confusion, demand/release confusion, and varying evidence positions. Split by claim and document template so paraphrases of one source do not cross training and test partitions. Include real de-identified, expert-labeled documents when available; synthetic examples alone miss deployment conditions.

A suitable application flow is:

```text
text intake -> document segmentation -> token/quality checks
            -> full-document Jev OR validated Laya chunks
            -> accepted category OR escalation to Luna/reviewer
            -> category-specific extraction and deterministic business rules
```

The first reusable deliverable is a small Python classifier function returning `{label, probabilities, model_version, input_strategy, evidence_location, needs_review}`. Do not manufacture a calibrated probability for chunk aggregation. Return raw chunk evidence or an explicitly named heuristic score until validated.

## Other suitable uses

These are candidate use cases, not performance claims established by this test:

- Route correspondence to the right team, identify communication intent, or flag that a reply is needed.
- Check whether a bounded requirement is present, such as a signature, payment request, or referenced attachment; document presence and actual attachment existence are separate questions.
- Select a relevant passage or candidate extraction from a supplied shortlist.
- Flag urgency or a mention of a deadline; parse and compare actual dates in code.
- Screen a model-produced answer against an explicit rubric, with human validation of that evaluator.
- Choose a workflow branch or tool from a small menu when the needed facts are already in context.

Use a general LLM when you need open-ended extraction, an explanation, document synthesis, or reasoning across contradictory evidence. Use deterministic code for exact balances, sums, dates, and policy-rule calculations. Jev and Laya are best considered components for bounded semantic decisions; their speed and structured interfaces do not eliminate classification mistakes.

## Cost and completed baseline

The 30 Jev calls cost **$0.004183704**, roughly **0.418 cents**, according to returned `usage.cost`. No automatic retries were used, and the cumulative guard remains $0.05. Laya downloaded one English checkpoint and ran locally; package/runtime and checkpoint setup consume disk and compute, not OpenRouter inference credits.

The authorized GPT-5.6 Luna baseline ran through the existing Codex ChatGPT login with reasoning set to `none`, in an empty temporary working directory. It saw shuffled documents and the shared taxonomy, not gold labels or competing predictions. Its event log records zero tool calls and 10/10 correct labels. It used 14,756 input tokens (including Codex overhead), 134 output tokens, and zero reasoning output tokens. No dollar charge is claimed for subscription-allowance usage. The model id requested was `gpt-5.6-luna`; this route does not expose a separately verified backend snapshot in the captured event stream. Luna subsequently classified all 12 independent long probes correctly (1k, 4k, 5k, 16k × start/middle/end), with no tools or reasoning output. Its documented maximum context was not tested.

## Completed long-input follow-up

All three models received identical text for 12 probes at about 1k, 4k, 5k, and 16k Laya tokens, each with evidence at the start, middle, and end. Jev and Luna scored 12/12; default Laya scored 4/12; chunked Laya scored 12/12. The 5k probes were 5,003–5,004 tokens: Jev and Luna 3/3, default Laya 1/3, chunked Laya 3/3 (18 chunks). Luna used 12 independent Codex calls, reasoning none, empty working directories, no tools, and no gold labels or competing predictions. See `results/luna-length.jsonl`, its per-call logs, and `results/length-comparison.md`. CLI timings include overhead and are not intrinsic model latency. These probes reuse one police report in repeated neutral filler and do not establish production accuracy.

## Boundary and confidence follow-up

Eight additional short boundary cases scored Jev 8/8, Luna 8/8, Laya 4/8. Complete inputs and frozen gold labels: BOUNDARY_DOCUMENTS.md. These are targeted diagnostics designed after initial errors, not a random held-out evaluation. Native confidence, selected-label probability, full distributions, and Laya action fields are exported in results/confidence-details.json and .md; native confidence is not validated correctness probability. All Laya inputs fit without truncation. Total cumulative Jev spend is $0.004183704 across 30 calls, under the $0.05 cap.

## Published capabilities and evaluation boundaries

Verified 22 September 2026. Published service limits, encoder capacity, and measured usable document budget are different quantities. No additional inference was performed.

| Model | Supported inputs | Published or architectural limit | Tested scope |
|---|---|---|---|
| Jev 1.13 | Text: string, JSON object, or array of text values. No native image, audio or video. [S1] | Direct API: 64k total request; state + longest question limited to 32k. OpenRouter: 32,000 context. These are service limits, not a disclosed architectural maximum. [S1, S2] | Full text through about 16k document tokens. No image or binary ingestion tested. |
| Laya English | Text and JSON serialized as text. Text encoder; no documented native image, audio or video path. [S3] | 512-token default sequence. ModernBERT backbone config lists 8,192 positions; that is not a validated Laya end-to-end limit. Multilingual default 1,024; its card states encoder capacity up to 8,192. [S3, S4] | 324 document tokens after this question. Longer documents used windows. No expanded-context checkpoint evaluation. |
| GPT-5.6 Luna | Text and image input; text output. Audio and video unsupported in the model specification. [S5] | Published context: 1,050,000 tokens; maximum output: 128,000. Budget input, instructions and output within the context; Codex route availability/settings may differ. [S5] | Text only through about 16k document tokens. Images and published maximum context not tested. |

A PDF or DOCX file is a container, not a model modality. Jev and Laya need extracted text (OCR for scans). Luna supports images, but file acceptance and PDF conversion depend on the serving API; native PDF upload was not verified here. Backbone capacity alone does not validate a fine-tuned decision head at that length. Tokenizers differ.

## Evidence

- [S1: TypeSafe model limits and modalities](https://docs.typesafe.ai/models)
- [S2: OpenRouter Jev route](https://openrouter.ai/typesafe/jev-1.13)
- [S3: Laya model card and configurations](https://huggingface.co/convaiinnovations/laya)
- [S4: ModernBERT encoder configuration](https://huggingface.co/answerdotai/ModernBERT-large/blob/main/config.json)
- [S5: OpenAI Luna model specification](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
