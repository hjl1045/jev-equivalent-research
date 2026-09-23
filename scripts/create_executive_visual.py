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
c=canvas.Canvas(str(out),pagesize=(1000,880));c.setTitle('Auto claims classification | Executive comparison');c.setAuthor('')
navy='#153346';muted='#586B77';teal='#087F8C';purple='#6554A4';gold='#A86A16'
def box(x,y,w,h,fill,r=8):
 c.setFillColor(HexColor(fill));c.roundRect(x,880-y-h,w,h,r,stroke=0,fill=1)
def text(x,y,t,size=11,color=navy,bold=False):
 c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,880-y-size,t)
def para(x,y,w,t,size=10,color=muted):
 p=Paragraph(t,ParagraphStyle('p',fontName='Helvetica',fontSize=size,leading=size*1.38,textColor=HexColor(color)))
 _,h=p.wrap(w,200);p.drawOn(c,x,880-y-h);return h
box(0,0,1000,880,'#F3F6F8',0)
text(34,23,'AUTO CLAIMS  /  SYNTHETIC EVALUATION',10,teal,True)
text(34,43,'Three models. Measured results.',28,navy,True)
text(34,82,'18 short documents + 12 length probes  |  22 September 2026  |  No additional inference for this visual',10,muted)
models=[('Jev','Hosted decision model / OpenRouter',teal,'jev-smoke','jev-boundary'),('Laya','English checkpoint / local CPU',gold,'laya-smoke','laya-boundary'),('GPT-5.6 Luna','General LLM / Codex login',purple,'luna-smoke','luna-boundary')]
for i,(name,sub,color,short,boundary) in enumerate(models):
 x=34+i*316;box(x,113,300,422,'#FFFFFF');box(x,113,300,5,color,0)
 text(x+18,130,name,22,color,True);text(x+18,160,sub,9,muted)
 def bar(y,label,n,d):
  text(x+18,y,label,10,muted);text(x+225,y,f'{n}/{d}',12,navy,True)
  box(x+18,y+22,264,6,'#E8EEF1',3);box(x+18,y+22,264*n/d,6,color,3)
 bar(189,'Initial documents',S[short]['correct'],10)
 bar(239,'Confusing category cases',S[boundary]['correct'],8)
 if name=='Laya':
  bar(289,'Long probes / default prefix',4,12)
  text(x+18,326,'With chunking: 12/12 correct',10,color,True)
 else:bar(289,'Long probes / full input',12,12)
 text(x+18,356,'BOUNDARY CASE LATENCY',8,muted,True)
 text(x+18,373,f"{S[boundary]['median_seconds']:.2f} s",25,navy,True)
 text(x+112,384,'median / document',9,muted)
 text(x+18,418,'OBSERVED INFERENCE COST',8,muted,True)
 if name=='Jev':
  text(x+18,436,f'${cost:.6f}',24,color,True)
  para(x+18,473,263,'30 total calls; 0.418 cents.<br/>All tests stayed within the $0.05 cap.')
 elif name=='Laya':
  text(x+18,436,'Local compute',22,color,True)
  para(x+18,473,263,'No API fee. CPU, memory and setup costs<br/>were not monetized in this pilot.')
 else:
  text(x+18,436,'Codex allowance',22,color,True)
  para(x+18,473,263,'No OpenRouter use. Subscription usage<br/>was not converted to a dollar cost.')
box(34,548,932,74,'#E4EDF1')
text(50,559,'AT YOUR 5k DOCUMENT LENGTH',9,navy,True)
para(50,579,285,'<b>Jev + Luna: 3/3 each.</b> Both received full text. Evidence was tested at start, middle and end.',10,navy)
para(353,559,283,'<b>Laya: 1/3 prefix; 3/3 chunked.</b><br/>324 document-token allowance in this setup; 18 chunks covered each 5k input.',10,navy)
para(661,559,288,'<b>5k observed response times</b><br/>Jev 0.30-0.46 s; Luna 3.22-3.46 s;<br/>Laya chunks 7.73-7.74 s.',10,navy)
text(34,635,'INPUT AND OUTPUT CONSTRAINTS',9,navy,True)
for i,(title,body) in enumerate([
 ('Jev','<b>Text documents tested.</b> OpenRouter lists 32k context tokens; reserve room for question and labels. Returns choice, class probabilities and confidence.'),
 ('Laya','<b>Text documents tested.</b> Default 512 total tokens left 324 for the document. Later text is silently clipped. Chunking adds compute; pooled confidence is not calibrated.'),
 ('GPT-5.6 Luna','<b>Text documents tested.</b> Published model context: 1.05M tokens; this Codex route was tested only to ~16k document tokens. Returned JSON label; no native score in this run.')]):
 x=34+i*316
 box(x,654,300,102,'#FFFFFF')
 text(x+12,663,title,11,[teal,gold,purple][i],True)
 para(x+12,683,276,body,9)
para(34,769,455,'<b>Confidence is not accuracy.</b> Laya returned native confidence 0.9999 and 0.9943 on two wrong boundary labels. Scores were not calibrated on representative claims.',10,navy)
para(511,769,455,'<b>Limits of the comparison.</b> Long probes reuse one police report in repeated filler at 1k, 4k, 5k and 16k Laya tokens. Synthetic results do not estimate production accuracy.',10,navy)
text(34,833,'Text-only evaluation; OCR/images not tested. Timing includes each serving stack: Jev network, Laya CPU, Luna CLI/Codex overhead. Not an intrinsic speed or dollar-cost ranking.',8,muted)
text(34,848,'Sources: retained results + report references for published limits. Tokenizers differ. Boundary cases were designed after initial errors; labels frozen before inference.',8,muted)
c.showPage();c.save();assert len(PdfReader(out).pages)==1;print(out)
