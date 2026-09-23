"""Offline tests for the spend guard; never contact a model."""
import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import benchmark as b
META={'data':{'endpoints':[{'pricing':{'prompt':'0.000000042','completion':'0'}}]}}
ROW={'id':'fixture','text':'Fictional scene narrative.','expected_label':'police_report'}
class BudgetTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'results').mkdir()
  self.rootpatch=patch.object(b,'ROOT',self.root);self.rootpatch.start()
  self.keypatch=patch.object(b,'load_key',return_value='test-only-not-a-real-key');self.keypatch.start()
 def tearDown(self): self.keypatch.stop();self.rootpatch.stop();self.tmp.cleanup()
 def test_refuses_before_inference_if_budget_too_small(self):
  with patch.object(b,'request',return_value=META) as request:
   with self.assertRaisesRegex(RuntimeError,'Budget guard'): b.jev([ROW],self.root/'out.jsonl',.001)
   self.assertEqual(request.call_count,1) # metadata read only
 def test_uses_jev_only_and_excludes_gold(self):
  calls=[]
  def request(url,body=None,key=None):
   calls.append((url,body))
   if body is None:return META
   return {'model':'typesafe/jev-1.13','answers':{'document_type':{'choice':'police_report'}},'usage':{'cost':.00003}}
  with patch.object(b,'request',side_effect=request):b.jev([ROW],self.root/'out.jsonl',.05)
  payload=calls[1][1]
  self.assertEqual(payload['model'],'typesafe/jev-1.13');self.assertEqual(payload['state'],ROW['text'])
  self.assertNotIn('expected_label',payload);self.assertNotIn('fixture',json.dumps(payload))
  ledger=json.loads((self.root/'results/openrouter-spend.json').read_text())
  self.assertAlmostEqual(ledger['charged_or_reserved_usd'],.00003)
 def test_unknown_cost_keeps_full_reservation(self):
  answer={'answers':{'document_type':{'choice':'police_report'}},'usage':{}}
  with patch.object(b,'request',side_effect=[META,answer]): b.jev([ROW],self.root/'out.jsonl',.05)
  ledger=json.loads((self.root/'results/openrouter-spend.json').read_text())
  self.assertAlmostEqual(ledger['charged_or_reserved_usd'],.002688)
 def test_price_increase_stops_before_inference(self):
  with patch.object(b,'request',return_value={'data':{'endpoints':[{'pricing':{'prompt':'0.1','completion':'0'}}]}}) as request:
   with self.assertRaisesRegex(AssertionError,'Price changed'):b.jev([ROW],self.root/'out.jsonl',.05)
   self.assertEqual(request.call_count,1)
if __name__=='__main__':unittest.main()
