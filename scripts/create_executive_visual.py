"""One-page factual executive comparison, derived from retained evaluation results."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
S=json.loads((ROOT/'results/summary.json').read_text())
rows=lambda name:[json.loads(x) for x in (ROOT/'results'/name).read_text().splitlines()]
cost=json.loads((ROOT/'results/openrouter-spend.json').read_text())['charged_or_reserved_usd']
out=ROOT/'reports/2026-09-22-Classification-Executive-One-Page.pdf'
c=canvas.Canvas(str(out),pagesize=(1320,1010));c.setTitle('Auto Claims Document Classification - Model Comparison');c.setAuthor('')
navy='#153346';muted='#586B77';teal='#087F8C';purple='#6554A4';gold='#A86A16'
def box(x,y,w,h,fill,r=8):
 c.setFillColor(HexColor(fill));c.roundRect(x,1010-y-h,w,h,r,stroke=0,fill=1)
def text(x,y,t,size=11,color=navy,bold=False):
 c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,1010-y-size,t)
def para(x,y,w,t,size=10,color=muted):
 p=Paragraph(t,ParagraphStyle('p',fontName='Helvetica',fontSize=size,leading=size*1.38,textColor=HexColor(color)))
 _,h=p.wrap(w,200);p.drawOn(c,x,1010-y-h);return h
box(0,0,1320,1010,'#F3F6F8',0)
text(34,23,'AUTO CLAIMS  /  SYNTHETIC EVALUATION',10,teal,True)
text(34,43,'Auto Claims Document Classification - Model Comparison',26,navy,True)
text(34,82,'18 short documents + 12 length probes  |  Updated 23 September 2026  |  OpenJev run incomplete: anonymous demo quota',10,muted)
models=[('Jev','Hosted decision model / OpenRouter',teal,'jev-smoke','jev-boundary'),('Laya','English checkpoint / local CPU',gold,'laya-smoke','laya-boundary'),('GPT-5.6 Luna','General LLM / Codex login',purple,'luna-smoke','luna-boundary'),('OpenJev FP8','Community demo / partial run','#3068A0',None,None)]
for i,(name,sub,color,short,boundary) in enumerate(models):
 x=34+i*316;box(x,113,300,422,'#FFFFFF');box(x,113,300,5,color,0)
 text(x+18,130,name,22,color,True);text(x+18,160,sub,9,muted)
 def bar(y,label,n,d):
  text(x+18,y,label,10,muted);text(x+225,y,f'{n}/{d}',12,navy,True)
  box(x+18,y+22,264,6,'#E8EEF1',3);box(x+18,y+22,264*n/d,6,color,3)
 if name=='OpenJev FP8':
  text(x+18,189,'Initial documents: 2/2 completed',12,navy,True)
  text(x+18,215,'8 of 10 not run',10,muted)
  text(x+18,239,'Boundary cases: not run',11,muted)
  text(x+18,289,'Long probes: not run',11,muted)
  text(x+18,326,'Quota blocked the third document',10,color,True)
  text(x+18,356,'PERFORMANCE NOT ESTABLISHED',8,muted,True)
  para(x+18,377,260,'Only two scored requests completed.<br/>No meaningful speed comparison.',11,navy)
  text(x+18,418,'OBSERVED INFERENCE COST',8,muted,True)
  text(x+18,436,'No paid API calls',22,color,True)
  para(x+18,473,263,'Free quota exhausted; no paid fallback.<br/>Demo differs from official helper. [S6]')
  continue
 bar(189,'Initial documents',S[short]['correct'],10)
 bar(239,'Confusing category cases',S[boundary]['correct'],8)
 if name=='Laya':
  bar(289,'Long probes / chunked',12,12)
  text(x+18,326,'Prefix-only control: 4/12 correct',10,color,True)
 else:bar(289,'Long probes / full input',12,12)
 text(x+18,356,'BOUNDARY CASE LATENCY',8,muted,True)
 text(x+18,373,f"{S[boundary]['median_seconds']:.2f} s",25,navy,True)
 text(x+112,384,'median / document',9,muted)
 text(x+18,418,'API-EQUIVALENT COST ESTIMATE' if name=='GPT-5.6 Luna' else 'OBSERVED INFERENCE COST',8,muted,True)
 if name=='Jev':
  text(x+18,436,f'${cost:.6f}',24,color,True)
  para(x+18,473,263,'30 total calls; 0.418 cents.<br/>All tests stayed within the $0.05 cap.')
 elif name=='Laya':
  text(x+18,436,'Local compute',22,color,True)
  para(x+18,473,263,'No API fee. CPU, memory and setup costs<br/>were not monetized in this pilot.')
 else:
  text(x+18,436,'~$0.049 estimated',22,color,True)
  para(x+18,473,263,'API-equivalent estimate, not a Codex bill.<br/>21 calls / 30 docs; includes overhead. [S5]')
box(34,548,1252,74,'#E4EDF1')
text(50,559,'AT YOUR 5k DOCUMENT LENGTH',9,navy,True)
para(50,579,360,'<b>Jev + Luna: 3/3 each.</b> Both received full text. Evidence was tested at start, middle and end.',10,navy)
para(445,559,365,'<b>Laya chunked: 3/3 correct.</b><br/>324 document-token allowance in this setup; 18 chunks covered each 5k input.',10,navy)
para(865,559,385,'<b>5k observed response times</b><br/>Jev 0.30-0.46 s; Luna 3.22-3.46 s;<br/>Laya chunks 7.73-7.74 s.',10,navy)
text(34,635,'PUBLISHED CAPABILITIES / DISTINCT FROM TESTED LIMITS',9,navy,True)
for i,(title,body) in enumerate([
 ('Jev','<b>Text only:</b> strings, JSON, text arrays. No image/audio/video. [S1]<br/><b>Direct:</b> 64k total request; state + longest question 32k. <b>OpenRouter:</b> 32k. Service limits, not disclosed architecture. [S1,S2]'),
 ('Laya','<b>Text / JSON-as-text.</b> No documented native image/audio/video path. [S3]<br/><b>Default:</b> 512 total; 324 document tokens here. Backbone: 8,192 positions, not validated Laya capacity. Multilingual: 1,024 default, up to 8,192 encoder. [S3,S4]'),
 ('GPT-5.6 Luna','<b>Text + image input;</b> text output. No audio/video. [S5]<br/><b>Published:</b> 1,050,000 context; 128,000 max output. Codex route may differ. Only text to ~16k document tokens tested. [S5]'),
 ('OpenJev','<b>Official:</b> text, JSON/DOM and one screenshot; 16,384-token prompt limit; 52 choices/pass. MLX: text only. [S6]<br/><b>Demo:</b> text, up to 26 labels; FP8 dequantized to BF16, raw softmax probabilities. CC BY-NC weights; commercial restriction.')]):
 x=34+i*316
 box(x,654,300,132,'#FFFFFF')
 text(x+12,663,title,11,[teal,gold,purple,'#3068A0'][i],True)
 para(x+12,683,276,body,9)
para(34,797,605,'<b>Confidence is not accuracy.</b> Laya returned native confidence 0.9999 and 0.9943 on two wrong boundary labels. Scores were not calibrated on representative claims.',10,navy)
para(685,797,605,'<b>Limits of the comparison.</b> Long probes reuse one police report in repeated filler at 1k, 4k, 5k and 16k Laya tokens. Synthetic results do not estimate production accuracy.',10,navy)
text(34,861,'Text-only evaluation; OCR/images not tested. Timing includes each serving stack: Jev network, Laya CPU, Luna CLI/Codex overhead. Not an intrinsic speed or dollar-cost ranking.',8,muted)
text(34,876,'Luna estimate: 232,898 uncached + 99,840 cached input; 471 output. Rates / 1M: $0.20 / $0.02 / $1.20. No-cache estimate: $0.067. [S5]',8,muted)
text(34,897,'PRIMARY EVIDENCE / ORIGINAL SOURCES 22 SEPTEMBER; OPENJEV 23 SEPTEMBER 2026',8,navy,True)
text(34,912,'S1  https://docs.typesafe.ai/models',8,muted)
c.linkURL('https://docs.typesafe.ai/models',(34,1010-912-11,950,1010-912+1),relative=0)
text(34,928,'S2  https://openrouter.ai/typesafe/jev-1.13',8,muted)
c.linkURL('https://openrouter.ai/typesafe/jev-1.13',(34,1010-928-11,950,1010-928+1),relative=0)
text(34,944,'S3  https://huggingface.co/convaiinnovations/laya',8,muted)
c.linkURL('https://huggingface.co/convaiinnovations/laya',(34,1010-944-11,950,1010-944+1),relative=0)
text(34,960,'S4  https://huggingface.co/answerdotai/ModernBERT-large/blob/main/config.json',8,muted)
c.linkURL('https://huggingface.co/answerdotai/ModernBERT-large/blob/main/config.json',(34,1010-960-11,950,1010-960+1),relative=0)
text(34,976,'S5  https://developers.openai.com/api/docs/models/gpt-5.6-luna',8,muted)
c.linkURL('https://developers.openai.com/api/docs/models/gpt-5.6-luna',(34,1010-976-11,950,1010-976+1),relative=0)
text(705,912,'S6  https://huggingface.co/openjev/openjev',8,muted)
c.linkURL('https://huggingface.co/openjev/openjev',(705,1010-923,1290,1010-911),relative=0)
text(705,928,'Demo: https://huggingface.co/spaces/chanoian/openjev-mlx-demo',8,muted)
c.linkURL('https://huggingface.co/spaces/chanoian/openjev-mlx-demo',(705,1010-939,1290,1010-927),relative=0)
para(705,950,580,'OpenJev: pilot excluded; 2 scored successes, third call quota-rejected. Different prompt/serving stack. No calibrated native confidence returned. Full benchmark remains incomplete.',9,muted)
c.showPage();c.save();assert len(PdfReader(out).pages)==1;print(out)
