"""Create a blinded Codex prompt: excludes labels, filenames, and other model outputs."""
import json
from pathlib import Path
from benchmark import ROOT,QUESTION,read_data
rows=read_data(ROOT/'data/documents.jsonl')
payload={'task':QUESTION,'documents':[{'id':r['id'],'text':r['text']} for r in rows]}
instruction='Classify each document independently using the provided categories. Do not use tools, files, web, prior work, or other models. Output only the requested JSON. Do not infer labels from document order. Provide one result per id. Do not output confidence scores or explanations.\n'
# Fixed permutation to avoid label-list order matching document order.
order=[6,2,9,0,7,4,1,8,5,3]
payload['documents']=[payload['documents'][i] for i in order]
(ROOT/'data/luna-blind-prompt.txt').write_text(instruction+json.dumps(payload,indent=2))
schema={'type':'object','properties':{'predictions':{'type':'array','items':{'type':'object','properties':{'id':{'type':'string'},'label':{'type':'string','enum':list(QUESTION['criteria'])}},'required':['id','label'],'additionalProperties':False}}},'required':['predictions'],'additionalProperties':False}
(ROOT/'data/luna-output-schema.json').write_text(json.dumps(schema,indent=2))
print('Prepared blinded Luna input and strict output schema; no model invoked.')
