import json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
labels=json.loads((ROOT/'data/labels.json').read_text())
def rows(name):
 p=ROOT/'results'/name
 return [json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []
def describe(rs):
 times=[r['elapsed_s'] for r in rs]
 return {'n':len(rs),'correct':sum(r['correct'] for r in rs),'accuracy':sum(r['correct'] for r in rs)/len(rs),'median_seconds':statistics.median(times),'api_cost_usd':sum(r.get('raw',{}).get('usage',{}).get('cost',0) for r in rs) if isinstance(rs[0].get('raw'),dict) else None}
def rows_data():
 return [json.loads(s) for s in (ROOT/'data/documents.jsonl').read_text().splitlines()]
def main():
 names=['jev-smoke','laya-smoke','jev-stress','laya-stress-head','laya-stress-chunks','jev-5k','laya-5k-head','laya-5k-chunks','luna-length','jev-boundary','laya-boundary','luna-boundary']
 result={name:describe(rows(name+'.jsonl')) for name in names if rows(name+'.jsonl')}
 luna_path=ROOT/'results/luna-predictions.json'
 if luna_path.exists():
  gold={r['id']:r['expected_label'] for r in rows_data()}
  predictions=json.loads(luna_path.read_text())['predictions']
  assert len(predictions)==len(gold) and {r['id'] for r in predictions}==set(gold)
  result['luna-smoke']={'n':len(predictions),'correct':sum(gold[r['id']]==r['label'] for r in predictions),'accuracy':sum(gold[r['id']]==r['label'] for r in predictions)/len(predictions),'route':'Codex ChatGPT login','api_cost_usd':None,'latency_comparable':False}
 oj=rows('openjev-demo.jsonl')
 if oj: result['openjev-demo']={'n':len(oj),'correct':sum(r['correct'] for r in oj),'planned_n':30,'status':'partial_quota_exhausted' if len(oj)<30 else 'completed','api_cost_usd':0,'comparability':'Different community-demo prompt and raw softmax; no native confidence'}
 (ROOT/'results/summary.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
 j={r['id']:r for r in rows('jev-smoke.jsonl')}; l={r['id']:r for r in rows('laya-smoke.jsonl')}
 luna={r['id']:r['label'] for r in json.loads(luna_path.read_text())['predictions']} if luna_path.exists() else {}
 table=['| Document | Expected | Jev | Laya | GPT-5.6 Luna (Codex) |','|---|---|---|---|---|']
 for r in j.values(): table.append(f"| {r['id']} | {r['expected_label']} | {r['prediction']} | {l.get(r['id'],{}).get('prediction','pending')} | {luna.get(r['id'],'pending')} |")
 (ROOT/'results/comparison.md').write_text('\n'.join(table)+'\n')
 groups={'Jev':rows('jev-stress.jsonl')+rows('jev-5k.jsonl'),'Laya prefix':rows('laya-stress-head.jsonl')+rows('laya-5k-head.jsonl'),'Laya chunks':rows('laya-stress-chunks.jsonl')+rows('laya-5k-chunks.jsonl'),'Luna':rows('luna-length.jsonl')}
 mapped={name:{r['id']:r for r in rs} for name,rs in groups.items()}
 table=['| Length / evidence position | Jev | Laya prefix | Laya chunks | Luna |','|---|---|---|---|---|']
 for id in mapped['Jev']:
  assert len({mapped[n][id]['input_sha256'] for n in mapped})==1
  table.append('| '+id+' | '+' | '.join(mapped[n][id]['prediction'] for n in mapped)+' |')
 (ROOT/'results/length-comparison.md').write_text('\n'.join(table)+'\n')
if __name__=='__main__':main()
