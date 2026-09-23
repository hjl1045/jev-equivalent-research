"""Preserve native scores without treating confidence as accuracy."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=[]
for path in sorted((ROOT/'results').glob('*.jsonl')):
 if not path.name.startswith(('jev-','laya-')):continue
 for line in path.read_text().splitlines():
  r=json.loads(line)
  if 'raw' not in r:continue
  raw=r['raw'];selected=r.get('selected_chunk',0)
  ans=(raw[selected] if isinstance(raw,list) else raw)['answers']['document_type']
  probs=ans['probabilities'];ranked=sorted(probs.items(),key=lambda kv:-kv[1])
  records.append(dict(source=path.name,id=r['id'],expected_label=r['expected_label'],prediction=r['prediction'],correct=r['correct'],confidence=ans.get('confidence'),selected_probability=probs[r['prediction']],runner_up_labels=[k for k,v in ranked[1:] if v==ranked[1][1]],runner_up_probability=ranked[1][1],top_two_margin=ranked[0][1]-ranked[1][1],probabilities=probs,action=ans.get('action'),scope='selected chunk only' if r.get('chunks',1)>1 else 'single input',selected_chunk=selected,document_tokens=r.get('document_tokens'),truncated=r.get('truncated'),input_sha256=r['input_sha256']))
(ROOT/'results/confidence-details.json').write_text(json.dumps(records,indent=2)+'\n')
lines=['# Native model scores','', 'C = native confidence; P = probability assigned to selected label. Values are not empirically measured correctness probabilities. Chunk rows describe the selected chunk, not calibrated document confidence. Full distributions and Laya action fields are in confidence-details.json.','', '| Source | ID | Expected | Prediction | Correct | C | P | Margin | Scope |','|---|---|---|---|---|---:|---:|---:|---|']
for r in records:lines.append(f"| {r['source']} | {r['id']} | {r['expected_label']} | {r['prediction']} | {r['correct']} | {r['confidence']:.4f} | {r['selected_probability']:.4f} | {r['top_two_margin']:.4f} | {r['scope']} |")
(ROOT/'results/confidence-details.md').write_text('\n'.join(lines)+'\n')
for r in records:
 if 'boundary' in r['source'] or (not r['correct'] and 'smoke' in r['source']):print(r['source'],r['id'],r['prediction'],r['confidence'],r['selected_probability'],r['runner_up_probability'],r['action'])
