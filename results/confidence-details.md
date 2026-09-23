# Native model scores

C = native confidence; P = probability assigned to selected label. Values are not empirically measured correctness probabilities. Chunk rows describe the selected chunk, not calibrated document confidence. Full distributions and Laya action fields are in confidence-details.json.

| Source | ID | Expected | Prediction | Correct | C | P | Margin | Scope |
|---|---|---|---|---|---:|---:|---:|---|
| jev-5k.jsonl | stress_5000_start | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-5k.jsonl | stress_5000_middle | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-5k.jsonl | stress_5000_end | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-boundary.jsonl | boundary_01 | demand_letter | demand_letter | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-boundary.jsonl | boundary_02 | settlement_release | settlement_release | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-boundary.jsonl | boundary_03 | medical_bill | medical_bill | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-boundary.jsonl | boundary_04 | medical_record | medical_record | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-boundary.jsonl | boundary_05 | witness_statement | witness_statement | True | 0.7800 | 0.8100 | 0.6200 | single input |
| jev-boundary.jsonl | boundary_06 | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-boundary.jsonl | boundary_07 | subrogation_notice | subrogation_notice | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-boundary.jsonl | boundary_08 | other | other | True | 0.4900 | 0.5400 | 0.3400 | single input |
| jev-smoke.jsonl | doc_01 | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_02 | demand_letter | demand_letter | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_03 | medical_bill | medical_bill | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_04 | medical_record | medical_record | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_05 | repair_estimate | repair_estimate | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_06 | rental_invoice | rental_invoice | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_07 | witness_statement | witness_statement | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_08 | coverage_letter | coverage_letter | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_09 | subrogation_notice | subrogation_notice | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-smoke.jsonl | doc_10 | settlement_release | settlement_release | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_1024_start | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_1024_middle | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_1024_end | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_4096_start | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_4096_middle | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_4096_end | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_16384_start | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_16384_middle | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| jev-stress.jsonl | stress_16384_end | police_report | police_report | True | 0.9900 | 0.9900 | 0.9800 | single input |
| laya-5k-chunks.jsonl | stress_5000_start | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-5k-chunks.jsonl | stress_5000_middle | police_report | police_report | True | 0.9999 | 1.0000 | 1.0000 | selected chunk only |
| laya-5k-chunks.jsonl | stress_5000_end | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-5k-head.jsonl | stress_5000_start | police_report | police_report | True | 0.9999 | 1.0000 | 1.0000 | single input |
| laya-5k-head.jsonl | stress_5000_middle | police_report | other | False | 0.4007 | 0.4785 | 0.1707 | single input |
| laya-5k-head.jsonl | stress_5000_end | police_report | other | False | 0.4007 | 0.4785 | 0.1707 | single input |
| laya-boundary.jsonl | boundary_01 | demand_letter | settlement_release | False | 0.9999 | 1.0000 | 1.0000 | single input |
| laya-boundary.jsonl | boundary_02 | settlement_release | settlement_release | True | 1.0000 | 1.0000 | 1.0000 | single input |
| laya-boundary.jsonl | boundary_03 | medical_bill | medical_bill | True | 0.9999 | 1.0000 | 1.0000 | single input |
| laya-boundary.jsonl | boundary_04 | medical_record | medical_record | True | 0.9723 | 0.9886 | 0.9782 | single input |
| laya-boundary.jsonl | boundary_05 | witness_statement | police_report | False | 0.9943 | 0.9985 | 0.9977 | single input |
| laya-boundary.jsonl | boundary_06 | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| laya-boundary.jsonl | boundary_07 | subrogation_notice | demand_letter | False | 0.5957 | 0.6738 | 0.4912 | single input |
| laya-boundary.jsonl | boundary_08 | other | demand_letter | False | 0.8623 | 0.9310 | 0.8882 | single input |
| laya-smoke.jsonl | doc_01 | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | single input |
| laya-smoke.jsonl | doc_02 | demand_letter | settlement_release | False | 0.7282 | 0.6439 | 0.2878 | single input |
| laya-smoke.jsonl | doc_03 | medical_bill | medical_bill | True | 0.9983 | 0.9996 | 0.9993 | single input |
| laya-smoke.jsonl | doc_04 | medical_record | medical_record | True | 0.9998 | 1.0000 | 1.0000 | single input |
| laya-smoke.jsonl | doc_05 | repair_estimate | repair_estimate | True | 1.0000 | 1.0000 | 1.0000 | single input |
| laya-smoke.jsonl | doc_06 | rental_invoice | rental_invoice | True | 0.9991 | 0.9998 | 0.9997 | single input |
| laya-smoke.jsonl | doc_07 | witness_statement | police_report | False | 0.7278 | 0.7846 | 0.6026 | single input |
| laya-smoke.jsonl | doc_08 | coverage_letter | coverage_letter | True | 0.9905 | 0.9969 | 0.9943 | single input |
| laya-smoke.jsonl | doc_09 | subrogation_notice | demand_letter | False | 0.4908 | 0.6620 | 0.5348 | single input |
| laya-smoke.jsonl | doc_10 | settlement_release | settlement_release | True | 1.0000 | 1.0000 | 1.0000 | single input |
| laya-stress-chunks.jsonl | stress_1024_start | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-stress-chunks.jsonl | stress_1024_middle | police_report | police_report | True | 0.9994 | 0.9999 | 0.9998 | selected chunk only |
| laya-stress-chunks.jsonl | stress_1024_end | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-stress-chunks.jsonl | stress_4096_start | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-stress-chunks.jsonl | stress_4096_middle | police_report | police_report | True | 0.9998 | 1.0000 | 1.0000 | selected chunk only |
| laya-stress-chunks.jsonl | stress_4096_end | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-stress-chunks.jsonl | stress_16384_start | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-stress-chunks.jsonl | stress_16384_middle | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-stress-chunks.jsonl | stress_16384_end | police_report | police_report | True | 1.0000 | 1.0000 | 1.0000 | selected chunk only |
| laya-stress-head.jsonl | stress_1024_start | police_report | police_report | True | 0.9999 | 1.0000 | 1.0000 | single input |
| laya-stress-head.jsonl | stress_1024_middle | police_report | other | False | 0.4007 | 0.4785 | 0.1707 | single input |
| laya-stress-head.jsonl | stress_1024_end | police_report | other | False | 0.4007 | 0.4785 | 0.1707 | single input |
| laya-stress-head.jsonl | stress_4096_start | police_report | police_report | True | 0.9999 | 1.0000 | 1.0000 | single input |
| laya-stress-head.jsonl | stress_4096_middle | police_report | other | False | 0.4007 | 0.4785 | 0.1707 | single input |
| laya-stress-head.jsonl | stress_4096_end | police_report | other | False | 0.4007 | 0.4785 | 0.1707 | single input |
| laya-stress-head.jsonl | stress_16384_start | police_report | police_report | True | 0.9999 | 1.0000 | 1.0000 | single input |
| laya-stress-head.jsonl | stress_16384_middle | police_report | other | False | 0.4007 | 0.4785 | 0.1707 | single input |
| laya-stress-head.jsonl | stress_16384_end | police_report | other | False | 0.4007 | 0.4785 | 0.1707 | single input |
