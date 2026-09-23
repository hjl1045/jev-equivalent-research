# OpenJev evaluation route

The requested model is [openjev/openjev](https://huggingface.co/openjev/openjev). Its published local builds require approximately 54 GB (BF16), 29 GB (FP8), 27 GB (MLX 8-bit), or 15 GB (MLX 4-bit). Local free disk at preparation was 9.6 GiB, insufficient for the smallest build. No weights were downloaded.

The model-card-linked [community demo](https://huggingface.co/spaces/chanoian/openjev-mlx-demo) is available and serves `openjev/openjev-FP8`, dequantized to BF16 on ZeroGPU. Its [source](https://huggingface.co/spaces/chanoian/openjev-mlx-demo/blob/037a94430fdeda9956e97b8c0f30aea0652bced6/app.py) uses candidate-letter logits with softmax; it does not apply the official helper's choice temperature of 0.85. This is a different serving implementation, not an exact reproduction of the official helper.

The same synthetic text, expected labels, and taxonomy are used. The adapter prepends the shared instructions to the document and appends category definitions to candidate names. Commas inside definitions become semicolons because the demo accepts comma-separated options. Neither gold labels nor other model predictions are sent. One initial connectivity pilot was excluded from scored results. There are no automatic retries. Demo quota or service errors stop the run and are retained separately.

The Gradio field named `confidence` is a candidate probability, not a separately computed native confidence statistic. Probabilities may reflect low-precision arithmetic. Do not treat them as empirically calibrated correctness probabilities. Client timings include network, allocation, and queue overhead, and cannot establish intrinsic speed rankings. No paid API charge is incurred; hosted compute is not economically free.

## Published capabilities

The [model card](https://huggingface.co/openjev/openjev) and [serving guide](https://huggingface.co/openjev/openjev/blob/main/serve/SERVE.md) describe text, JSON/DOM and screenshot input; one image per request; a 16,384-token prompt serving limit; and up to 52 choices in one pass. Larger option sets require multiple passes. MLX builds are text-only. The hosted community demo exposes only text and up to 26 candidate labels. Our 11-label task fits its option limit. The model's published 16k prompt budget includes instructions and options, so the 16k-document probes may exceed that budget depending on tokenizer; a demo result does not validate the official helper at that length.

Weights are CC BY-NC 4.0, for research/noncommercial use with attribution; commercial use requires resolving licensing with the publisher. The helper code is Apache 2.0. OpenJev is independent of TypeSafe.

## Laya presentation correction

The executive visual now leads its long-input row with **chunked Laya: 12/12 correct**. The prefix-only 4/12 result is retained as a truncation control. The 7/10 initial and 4/8 boundary results concern short inputs that fit one window; chunking does not change those observed results.
