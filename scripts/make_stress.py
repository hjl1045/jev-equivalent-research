"""Diagnostic length/position variants, not independent accuracy samples."""
import json,os,argparse
from pathlib import Path
os.environ['HF_HUB_OFFLINE']='1'
ROOT=Path(__file__).resolve().parents[1]
from transformers import AutoTokenizer
path=next((ROOT/'.cache/huggingface/hub/models--convaiinnovations--laya/snapshots').glob('*/tokenizer'))
tok=AutoTokenizer.from_pretrained(path)
base=json.loads((ROOT/'data/documents.jsonl').read_text().splitlines()[0])
filler='Administrative archive continuation. This section records routine file handling only. A copy was received, indexed, and retained. No new claim decision, medical service, vehicle transaction, or settlement term is stated here. '
baseids=tok(base['text'],add_special_tokens=False)['input_ids']
parser=argparse.ArgumentParser();parser.add_argument('--targets',nargs='+',type=int,default=[1024,4096,16384]);parser.add_argument('--out',default='data/length_stress.jsonl');args=parser.parse_args()
rows=[]
for target in args.targets:
 padding=tok(filler*((target//30)+1),add_special_tokens=False)['input_ids'][:target-len(baseids)]
 for position in ['start','middle','end']:
  split={'start':0,'middle':len(padding)//2,'end':len(padding)}[position]
  text=tok.decode(padding[:split])+'\n\n'+base['text']+'\n\n'+tok.decode(padding[split:])
  rows.append({'id':f'stress_{target}_{position}','expected_label':base['expected_label'],'text':text,'base_id':base['id'],'split':'length_diagnostic','evidence_position':position,'target_laya_tokens':target,'actual_laya_tokens':len(tok(text,add_special_tokens=False)['input_ids'])})
(ROOT/args.out).write_text(''.join(json.dumps(r)+'\n' for r in rows))
print([(r['id'],r['actual_laya_tokens']) for r in rows])
