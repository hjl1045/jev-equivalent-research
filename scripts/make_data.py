"""Deterministic, wholly fictional smoke-test documents; no model-generated gold labels."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LABELS={
'police_report':'Officer collision investigation, observations and driver accounts',
'demand_letter':'Attorney request for settlement payment resolving an injury claim',
'medical_bill':'Provider itemized charges, balances and request for payment',
'medical_record':'Clinical history, examination, diagnosis and treatment plan',
'repair_estimate':'Vehicle repair parts, labor and estimated repair costs',
'rental_invoice':'Rental vehicle dates, daily rates and billed charges',
'witness_statement':'First-person non-officer account of the collision',
'coverage_letter':'Insurer communication about policy coverage or reservation of rights',
'subrogation_notice':'Insurer recovery request for amounts already paid',
'settlement_release':'Agreement releasing claims in exchange for settlement',
'other':'Unrelated content or insufficient evidence of any listed type'}
DOCS=[
('police_report',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Cedar Crossing Public Safety Department. Incident CC-26-0418. Reporting officer: A. Vale, badge 417.
On April 18, 2026, at 16:42 I responded to the intersection of Finch Road and Harbor Avenue. The roadway was dry and visibility clear. Vehicle one, a blue sedan driven by Morgan Reed, showed front-end damage. Vehicle two, a gray hatchback driven by Casey North, showed rear bumper damage. Both vehicles had been moved to the curb before my arrival.
Reed stated that traffic slowed unexpectedly and that braking did not prevent contact. North stated that the hatchback was stationary at the red signal. Witness Ellis Park reported seeing the blue vehicle approaching while the signal was red. I observed debris within the eastbound through lane. No measurement of pre-impact speed was available.
North reported neck discomfort and accepted transport by ambulance. No medical diagnosis is made in this report. A citation for following too closely was issued to Reed. The diagram depicts reported positions and is not to scale. Scene photographs were logged under attachments 1 through 4. This narrative records the investigation and does not determine insurance coverage."""),
('demand_letter',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Cedar Legal Group | September 3, 2026
To: Alder Mutual, bodily injury desk. Claim DEMO-204.
We represent Casey North concerning the April 18 collision involving your insured Morgan Reed. Please direct settlement communications to this office.
Our client was stopped for a red light when struck from behind. Treatment included an emergency evaluation and a course of physical therapy. The enclosed records describe a cervical strain, continuing discomfort during desk work, and a gradual improvement. Documented medical charges total $6,480; claimed lost wages are $1,120. These amounts are supporting damages, not a request from a medical provider to pay an account balance.
Considering the reported liability, treatment course, and disruption of daily activities, our client offers to resolve the bodily injury claim for $28,000 in exchange for a mutually acceptable release. Please provide your written response by September 24. This offer does not purport to resolve a separate property damage claim.
Enclosures referenced: officer incident narrative, treatment notes, and itemized statements. Those documents are supporting exhibits; this correspondence communicates our settlement proposal. Sincerely, Avery Bell, attorney."""),
('medical_bill',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Willow Outpatient Center | Patient account DEMO-803 | Statement date May 9, 2026
Patient: Casey North. Referring event: motor vehicle collision, April 18. Bill to: Alder Mutual claims department.
Date of service | Service description | Units | Charge
April 19 | New patient evaluation | 1 | $240.00
April 19 | Cervical spine radiograph, two views | 1 | $180.00
April 26 | Therapeutic exercise | 2 | $160.00
April 26 | Manual therapy | 1 | $95.00
May 3 | Therapeutic exercise | 2 | $160.00
May 3 | Manual therapy | 1 | $95.00
Total charges: $930.00. Payments posted: $100.00. Contractual adjustments: $80.00. Remaining balance: $750.00.
Please include the account identifier with payment. Questions about individual charges should be directed to the billing office. The brief service descriptions identify billed services; this statement does not contain a clinical examination or a treatment plan. No settlement of an injury claim is offered by accepting payment of this balance. Duplicate copy supplied at the patient's request."""),
('medical_record',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Willow Outpatient Center. Encounter May 3, 2026. Patient Casey North. Clinician Jordan Ash, PT.
Subjective: Patient reports stiffness when turning the head after the April 18 rear-end collision. Pain today is 3 of 10, improved from 5 of 10 at the first visit. Sleep is occasionally interrupted. Patient denies arm numbness or new weakness and has returned to modified desk duties.
Objective: Cervical rotation is mildly restricted bilaterally. Upper extremity strength is symmetric. Tenderness is present over the upper trapezius. Patient tolerated supervised range-of-motion exercises without an increase in symptoms.
Assessment: Improving cervical strain with residual mobility limitation. Progress is consistent with the treatment goals established at the initial visit. No new red-flag symptoms were reported during this encounter.
Plan: Continue home mobility exercises, pacing, and two additional therapy visits over the next fortnight. Reassess functional tolerance and discharge if goals are met. Patient verbalized understanding.
This signed encounter note documents clinical care. Billing is handled in a separate statement; no amount is requested for payment here. Electronically signed Jordan Ash on May 3."""),
('repair_estimate',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Juniper Auto Body. Estimate E-441. Vehicle: 2022 gray hatchback, synthetic VIN TEST0000000000441. Owner: Casey North.
Inspection found a distorted rear bumper cover, damaged absorber, and misaligned reinforcement bracket. No structural measurement has yet been completed. The following work is proposed, subject to disassembly and customer authorization.
Replace rear bumper cover: part $420.00, body labor 1.8 hours at $75.00 = $135.00.
Replace absorber: part $110.00, labor 0.5 hours at $75.00 = $37.50.
Repair bracket alignment: labor 1.2 hours at $75.00 = $90.00.
Refinish bumper: paint labor 2.5 hours at $75.00 = $187.50; materials $145.00.
Subtotal before taxes: $1,125.00. Estimated completion: three working days after parts arrive. Additional damage may require a supplement with photographs.
This document estimates prospective repair work and is not a paid invoice. It does not include a rental car or treatment expenses. No work has been authorized by this estimate alone. Prepared by Rowan Birch, estimator, April 22, 2026."""),
('rental_invoice',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Harbor Mobility Rentals | Agreement R-712 | Final billing copy
Renter: Casey North. Replacement vehicle: compact four-door sedan. Referring claim DEMO-204. Pickup April 22, 2026 at 09:00; return April 27, 2026 at 09:00. Vehicle returned with the same fuel level recorded at pickup. No additional damage was noted at return.
Five rental days at $42.00 per day: $210.00. Local facility fee, five days at $3.00: $15.00. Tax: $18.00. Total: $243.00. Amount paid: $0.00. Balance due: $243.00.
Direct billing requested to Alder Mutual subject to its authorization. If direct billing is declined, responsibility remains with the renter under the rental agreement. Please reference R-712 with remittance.
The renter indicated that a personal vehicle was undergoing collision repair. This invoice covers temporary transportation only and does not estimate the cost of repairing that vehicle. Optional damage waiver was declined; no charge for it is included. Billing contact: accounts desk."""),
('witness_statement',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Recorded account transcribed April 21, 2026. Speaker: Ellis Park. Interviewer: claim intake associate.
Q: Where were you when the vehicles made contact?
A: I was on the sidewalk near the bakery at Finch and Harbor. I had a clear view of the eastbound lane but could not see either driver's phone or dashboard.
Q: Please describe what you personally observed.
A: The gray hatchback was waiting at the light. The blue sedan came up behind it and hit the rear. I heard braking just before the sound of the impact. I cannot estimate its speed. I crossed after the vehicles stopped and asked whether anyone needed help.
Q: Did either driver say anything about being hurt?
A: The person in the gray car said their neck was sore. That is what I heard; I do not know what the hospital found. I gave my contact details to the officer who arrived later.
I reviewed this transcript and confirm it reflects my recollection. I am not related to either driver and have no financial interest in the claim. Signed Ellis Park."""),
('coverage_letter',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Alder Mutual | May 12, 2026 | To Morgan Reed
Re: Claim DEMO-204; policy DEMO-A17; reported collision April 18.
We acknowledge your report and are continuing our investigation. The declarations supplied with your policy identify the insured vehicle and the stated coverage period. We need further information about who was operating the vehicle and its use at the time of the reported loss.
We will investigate and handle the matter subject to a reservation of rights. Providing an adjuster, obtaining records, or discussing resolution does not waive any policy terms. No final coverage decision is made in this correspondence. Please provide the requested vehicle-use questionnaire and any relevant permission-to-drive information within fourteen days.
The applicable policy wording and endorsements will govern our determination. This letter concerns the insurer's position on coverage; it is not a demand that another insurer reimburse a payment, and it does not offer a settlement to an injured person.
Please contact the assigned coverage specialist with questions. Keep copies of materials you submit. Sincerely, Taylor Moss, coverage unit."""),
('subrogation_notice',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Bracken Insurance Recovery Unit | June 16, 2026
To Alder Mutual recovery desk. Our insured: Casey North. Your insured: Morgan Reed. Loss date April 18. Reference REC-51.
Bracken Insurance paid $3,860 under its insured's collision coverage for damage arising from the reported rear-end impact. We seek reimbursement of that payment and the insured's $500 deductible, for a total recovery request of $4,360. Payment support and repair documentation are available for review.
Our recovery position is based on the driver accounts and scene information presently in the file. If you dispute responsibility or any amount, please identify the disputed item and send the supporting information to the assigned recovery examiner. Please acknowledge this recovery request within thirty days.
This is an insurer-to-insurer request to recover a payment already made. It is not an attorney's proposal to settle a bodily injury claim. No treatment charges, pain-and-suffering amount, or bodily injury release is included. Remittance should identify REC-51 so the deductible portion can be allocated correctly. Prepared by Jamie Elm, recovery examiner."""),
('settlement_release',"""SYNTHETIC TRAINING DOCUMENT — NO REAL PERSON OR EVENT
Agreement concerning the April 18, 2026 motor vehicle occurrence
In consideration of payment of $24,000, receipt and sufficiency of which are acknowledged subject to clearance of funds, Casey North agrees to release Morgan Reed and Alder Mutual from the bodily injury claims described in this agreement arising from the identified occurrence.
The parties intend this agreement to compromise disputed claims. It is not an admission of fault. The releasor states that the terms have been read and that an opportunity to consult counsel has been provided. This agreement resolves only the bodily injury claim identified here; previously handled vehicle damage is outside its scope.
No additional payment is promised except as expressly stated in this document. Each signatory affirms authority to enter this agreement. A copy bearing electronic signatures may be retained as evidence of execution.
Releasor: Casey North. Signature: [synthetic signature]. Date: September 20, 2026.
Witness: Avery Bell. Signature: [synthetic signature].
This executed instrument records acceptance of settlement and release of claims. It is not an opening proposal or a request for a response to negotiations.""")]
def main():
 rows=[]
 for i,(label,text) in enumerate(DOCS,1):
  id=f'doc_{i:02}'
  (ROOT/'data/documents'/f'{id}.txt').write_text(text+'\n')
  rows.append(dict(id=id,expected_label=label,text=text,split='smoke',gold_basis='Author-assigned document purpose; fictional example'))
 (ROOT/'data/labels.json').write_text(json.dumps(LABELS,indent=2)+'\n')
 (ROOT/'data/documents.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
 print(f'Created {len(rows)} synthetic documents; {len(LABELS)} candidate labels including other.')
if __name__=='__main__': main()
