# Published capabilities and evaluation boundaries

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

## OpenJev addition

[OpenJev](https://huggingface.co/openjev/openjev) supports text, JSON/DOM and screenshots in its official GPU helper; 16,384 prompt tokens, one image per request and 52 options per pass. MLX variants are text-only. Its weights use CC BY-NC 4.0. Our community-demo attempt used FP8 dequantized to BF16, text only, and stopped after two scored examples because quota was exhausted. No long-input capacity was measured.
