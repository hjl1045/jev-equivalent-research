"""OpenJev FP8 community-demo evaluation. No OpenRouter or paid inference.
The demo differs from the official calibrated helper; see metadata.
"""
import hashlib,json,time,urllib.request,os
from pathlib import Path
from benchmark import ROOT,QUESTION,read_data
URL='https://chanoian-openjev-mlx-demo.hf.space/gradio_api/call/classify'
OUT=ROOT/'results/openjev-demo.jsonl'
# Optional authentication is sent only to the fixed Hugging Face Space endpoint.
headers={'Content-Type':'application/json'}
token=os.environ.get('HF_TOKEN','')
for env_path in [ROOT/'env.',ROOT/'.env']:
 if env_path.exists():
  for line in env_path.read_text().splitlines():
   if '=' in line and line.split('=',1)[0].strip()=='HF_TOKEN':
    token=line.split('=',1)[1].strip().strip(chr(34)+chr(39))
if token: headers['Authorization']='Bearer '+token

labels=[k+': '+v.replace(',',';') for k,v in QUESTION['criteria'].items()]
metadata={'model':'openjev/openjev-FP8','route':'community Gradio ZeroGPU demo, FP8 checkpoint dequantized to bf16','space_revision':'037a94430fdeda9956e97b8c0f30aea0652bced6','source':'https://huggingface.co/spaces/chanoian/openjev-mlx-demo/blob/main/app.py','calibration':'demo raw candidate-letter softmax; official helper T=0.85 not applied','native_confidence':None,'input_adaptation':'Shared instructions prepended to document. Label definitions appended to label names; commas replaced by semicolons for CSV transport. Different prompt from official helper.','latency':'client round trip including ZeroGPU queue/allocation','pilot':'One preliminary doc_01 call succeeded; excluded from scored run.','paid_api_cost_usd':0,'license':'CC-BY-NC-4.0; research/noncommercial','truncation':'No truncation in inspected demo source; serving maximum not independently verified.'}
(ROOT/'results/openjev-demo.metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
allrows=read_data(ROOT/'data/documents.jsonl')+read_data(ROOT/'data/boundary_documents.jsonl')+read_data(ROOT/'data/length_5k.jsonl')+read_data(ROOT/'data/length_stress.jsonl')
done={r['id'] for r in read_data(OUT)} if OUT.exists() else set()
for row in allrows:
 if row['id'] in done:continue
 body={'data':[QUESTION['instructions']+'\nDOCUMENT:\n'+row['text'],', '.join(labels),False]}
 start=time.perf_counter()
 try:
  req=urllib.request.Request(URL,data=json.dumps(body).encode(),headers=headers)
  event=json.load(urllib.request.urlopen(req,timeout=30))['event_id']
  stream=urllib.request.urlopen(urllib.request.Request(URL+'/'+event,headers=headers),timeout=150)
  event_type=None;payload=None
  for line in stream:
   line=line.decode().strip()
   if line.startswith('event:'):event_type=line[6:].strip()
   if line.startswith('data:') and event_type in ['complete','error']:
    payload=json.loads(line[5:]);break
  if event_type!='complete':raise RuntimeError('Demo returned '+str(event_type)+': '+str(payload))
  ans=payload[0];probs={v['label'].split(':',1)[0]:v['confidence'] for v in ans['confidences']};pred=ans['label'].split(':',1)[0]
  assert set(probs)==set(QUESTION['criteria']) and pred in probs
  result={'id':row['id'],'expected_label':row['expected_label'],'prediction':pred,'correct':pred==row['expected_label'],'elapsed_s':time.perf_counter()-start,'input_sha256':hashlib.sha256(row['text'].encode()).hexdigest(),'question_sha256':hashlib.sha256(json.dumps(QUESTION).encode()).hexdigest(),'transport_payload_sha256':hashlib.sha256(json.dumps(body).encode()).hexdigest(),'probabilities':probs,'selected_probability':probs[pred],'native_confidence':None,'raw':ans,'api_cost_usd':0}
  with OUT.open('a') as f:f.write(json.dumps(result)+'\n')
  print(row['id'],pred,result['correct'],round(result['elapsed_s'],2),flush=True)
 except Exception as exc:
  error={'id':row['id'],'status':'failed','error':str(exc),'elapsed_s':time.perf_counter()-start}
  with (ROOT/'results/openjev-demo-errors.jsonl').open('a') as f:f.write(json.dumps(error)+'\n')
  print(error,flush=True)
  break # No automatic retries or repeated calls after quota/service errors.
