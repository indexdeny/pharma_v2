# RENDER QA REPORT
> Generated: 2026-06-04 23:44:08 | Pipeline: P12.0

## Summary

| Metric | Value |
|---|---|
| Total images checked | 389 |
| OK (all checks pass) | 32 |
| SOFT_FAIL (brand missing/duplicated only) | 27 |
| HARD_FAIL (critical numbers missing / empty) | 330 |
| OCR UNAVAILABLE | 0 |

## HARD_FAIL — Prioritized Manual Review List
These SKUs failed critical numeric checks (dosage or unit count) or returned empty OCR text.

| SKU | Dosage Found | Count Found | Details |
|---|---|---|---|
| 101-min | FAIL | OK | MISSING brand/ingredient from ['celebrex', 'celecoxib'] · MISSING dosage value '100' (from '100 mg') |
| 102-min | FAIL | FAIL | MISSING brand/ingredient from ['isordil', 'isosorbide dinitrate'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 103-min | FAIL | FAIL | MISSING brand/ingredient from ['maxalt', 'rizatriptan'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '10' (from '10 Pills') |
| 104-min | OK | FAIL | MISSING brand/ingredient from ['meloxicam', 'mobic'] · MISSING unit count value '30' (from '30 Pills') |
| 106-min | FAIL | FAIL | MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 108-min | FAIL | OK | MISSING brand/ingredient from ['acetaminophen', 'tylenol'] · MISSING dosage value '500' (from '500 mg') |
| 109-min | FAIL | FAIL | MISSING brand/ingredient from ['tramadol', 'ultram'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 11-min | FAIL | FAIL | MISSING brand/ingredient from ['amoxicillin', 'amoxil'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 110-min | FAIL | FAIL | MISSING brand/ingredient from ['accutane', 'isotretinoin'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 112-min | FAIL | OK | MISSING brand/ingredient from ['champix', 'varenicline tartrate'] · MISSING dosage value '1' (from '1 mg') |
| 113-min | FAIL | OK | MISSING brand/ingredient from ['bupropion', 'zyban'] · MISSING dosage value '150' (from '150 mg') |
| 114-min | FAIL | OK | MISSING dosage value '100' (from '100 mcg') |
| 115-min | FAIL | FAIL | MISSING dosage value '60' (from '60 mg') · MISSING unit count value '30' (from '30 Pills') |
| 117-min | FAIL | OK | MISSING dosage value '10' (from '10 mg') |
| 118-min | FAIL | FAIL | MISSING dosage value '120' (from '120 mg') · MISSING unit count value '30' (from '30 Pills') |
| 119-min | FAIL | OK | MISSING dosage value '1' (from '1 mg') |
| 12-min | FAIL | FAIL | MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 120-min | OK | FAIL | MISSING brand/ingredient from ['evista', 'raloxifene'] · MISSING unit count value '30' (from '30 Pills') |
| 121-min | FAIL | FAIL | MISSING brand/ingredient from ['alendronic acid', 'fosamax'] · MISSING dosage value '70' (from '70 mg') · MISSING unit count value '30' (from '30 Pills') |
| 124-min | OK | FAIL | MISSING unit count value '30' (from '30 Implants') |
| 125-min | FAIL | FAIL | MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 126-min | OK | FAIL | MISSING brand/ingredient from ['medroxyprogesterone', 'provera'] · MISSING unit count value '30' (from '30 Pills') |
| 127-min | OK | FAIL | MISSING unit count value '1' (from '1 Pills') |
| 128-min | FAIL | FAIL | MISSING brand/ingredient from ['aygestin', 'norethindrone acetate'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 129-min | FAIL | OK | MISSING brand/ingredient from ['clomid', 'clomiphene'] · MISSING dosage value '50' (from '50 mg') |
| 13-min | FAIL | OK | MISSING dosage value '500' (from '500 mg') |
| 130-min | FAIL | FAIL | MISSING brand/ingredient from ['danazol', 'danocrine'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 131-min | FAIL | FAIL | MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 133-min | FAIL | FAIL | MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 134-min | FAIL | FAIL | MISSING brand/ingredient from ['atarax', 'hydroxyzine'] · MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 135-min | FAIL | FAIL | MISSING brand/ingredient from ['ativan', 'lorazepam'] · MISSING dosage value '1' (from '1 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 136-min | OK | FAIL | MISSING brand/ingredient from ['buspar', 'buspirone'] · MISSING unit count value '30' (from '30 Pills') |
| 138-min | FAIL | OK | MISSING dosage value '30' (from '30mg/500mg') |
| 141-min | FAIL | OK | MISSING brand/ingredient from ['deca durabolin', 'testosterone'] · MISSING dosage value '50' (from '50 mg/mL') |
| 143-min | FAIL | OK | MISSING dosage value '1.62' (from '1.62%') |
| 144-min | OK | FAIL | MISSING unit count value '10' (from '10 Pills') |
| 145-min | OK | FAIL | MISSING unit count value '10' (from '10 Pills') |
| 146-min | FAIL | FAIL | MISSING brand/ingredient from ['hucog-10000 hp', 'human chorionic gonadotropin'] · MISSING dosage value '10000' (from '10000 IU') · MISSING unit count value '10' (from '10 Pills') |
| 147-min | FAIL | FAIL | MISSING brand/ingredient from ['sustaviron-250', 'testosterone blend'] · MISSING dosage value '250' (from '250 mg/mL') · MISSING unit count value '10' (from '10 Pills') |
| 148-min | FAIL | FAIL | MISSING brand/ingredient from ['drostanolone propionate', 'masteron'] · MISSING dosage value '100' (from '100 mg/mL') · MISSING unit count value '1' (from '1 Pills') |
| 149-min | FAIL | FAIL | MISSING brand/ingredient from ['modafinil', 'modalert'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 15-min | FAIL | FAIL | MISSING brand/ingredient from ['cipro', 'ciprofloxacin'] · MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 150-min | FAIL | FAIL | MISSING dosage value '150' (from '150 mg') · MISSING unit count value '30' (from '30 Pills') |
| 151-min | FAIL | FAIL | MISSING brand/ingredient from ['modafinil', 'provigil'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 152-min | FAIL | OK | MISSING brand/ingredient from ['armodafinil', 'artvigil'] · MISSING dosage value '150' (from '150 mg') |
| 156-min | FAIL | FAIL | MISSING dosage value '0.5' (from '0.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 157-min | FAIL | OK | MISSING brand/ingredient from ['diazepam', 'valium'] · MISSING dosage value '5' (from '5 mg') |
| 158-min | FAIL | OK | MISSING brand/ingredient from ['clonazepam', 'klonopin'] · MISSING dosage value '1' (from '1 mg') |
| 16-min | FAIL | OK | MISSING brand/ingredient from ['doxycycline', 'doxycycline hyclate'] · MISSING dosage value '100' (from '100 mg') |
| 160-min | FAIL | FAIL | MISSING brand/ingredient from ['avanafil', 'stendra'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 161-min | OK | FAIL | MISSING brand/ingredient from ['apcalis oral jelly', 'tadalafil'] · MISSING unit count value '7' (from '7 Pills') |
| 162-min | OK | FAIL | MISSING brand/ingredient from ['tadalafil + dapoxetine hcl', 'tadapox'] · MISSING unit count value '10' (from '10 Pills') |
| 164-min | FAIL | FAIL | MISSING brand/ingredient from ['anastrozole', 'arimidex'] · MISSING dosage value '1' (from '1 mg') · MISSING unit count value '30' (from '30 Pills') |
| 165-min | FAIL | FAIL | MISSING brand/ingredient from ['claritin', 'loratadine'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '60' (from '60 Pills') |
| 166-min | FAIL | FAIL | MISSING brand/ingredient from ['clarinex', 'desloratadine'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 17-min | FAIL | OK | MISSING brand/ingredient from ['flagyl', 'metronidazole'] · MISSING dosage value '500' (from '500 mg') |
| 170-min | FAIL | FAIL | MISSING brand/ingredient from ['fliban', 'flibanserin'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 171-min | FAIL | OK | MISSING brand/ingredient from ['hydrochlorothiazide', 'microzide'] · MISSING dosage value '25' (from '25 mg') |
| 172-min | FAIL | FAIL | MISSING brand/ingredient from ['quetiapine', 'qutan'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 173-min | FAIL | FAIL | MISSING dosage value '40' (from '40 mg') · MISSING unit count value '30' (from '30 Pills') |
| 175-min | FAIL | FAIL | MISSING brand/ingredient from ['nolvadex', 'tamoxifen'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 176-min | FAIL | FAIL | MISSING brand/ingredient from ['sertraline', 'zoloft'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 177-min | FAIL | OK | MISSING dosage value '250' (from '250 mg') |
| 178-min | FAIL | FAIL | MISSING brand/ingredient from ['aciphex', 'rabeprazole'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '20' (from '20 Pills') |
| 18-min | FAIL | OK | MISSING brand/ingredient from ['efavirenz', 'sustiva'] · MISSING dosage value '600' (from '600 mg') |
| 180-min | FAIL | OK | MISSING dosage value '25' (from '25 mg') |
| 181-min | FAIL | FAIL | MISSING brand/ingredient from ['alesse', 'levonorgestrel + ethinylestradiol'] · MISSING dosage value '20' (from '20 mcg') · MISSING unit count value '30' (from '30 Pills') |
| 183-min | FAIL | FAIL | MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 184-min | FAIL | OK | MISSING brand/ingredient from ['amaryl', 'glimepiride'] · MISSING dosage value '2' (from '2 mg') |
| 186-min | FAIL | FAIL | MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 187-min | FAIL | FAIL | MISSING brand/ingredient from ['antabuse', 'disulfiram'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 189-min | FAIL | OK | MISSING brand/ingredient from ['aricept', 'donepezil'] · MISSING dosage value '10' (from '10 mg') |
| 19-min | FAIL | FAIL | MISSING brand/ingredient from ['azithromycin', 'zithromax'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 192-min | FAIL | FAIL | MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 194-min | FAIL | FAIL | MISSING brand/ingredient from ['celexa', 'citalopram'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 195-min | FAIL | OK | MISSING brand/ingredient from ['cleocin', 'clindamycin'] · MISSING dosage value '150' (from '150 mg') |
| 197-min | FAIL | FAIL | MISSING brand/ingredient from ['catapres', 'clonidine'] · MISSING dosage value '0.1' (from '0.1 mg') · MISSING unit count value '30' (from '30 Pills') |
| 198-min | OK | FAIL | MISSING brand/ingredient from ['colchicine'] · MISSING unit count value '30' (from '30 Pills') |
| 199-min | FAIL | FAIL | MISSING brand/ingredient from ['cozaar', 'losartan'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 2-min | FAIL | OK | MISSING brand/ingredient from ['atomoxetine', 'strattera'] · MISSING dosage value '40' (from '40 mg') |
| 20-min | FAIL | FAIL | MISSING brand/ingredient from ['abilify', 'aripiprazole'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 200-min | FAIL | FAIL | MISSING brand/ingredient from ['crestor', 'rosuvastatin'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 201-min | FAIL | FAIL | MISSING brand/ingredient from ['desyrel', 'trazodone'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 203-min | FAIL | FAIL | MISSING brand/ingredient from ['acetazolamide', 'diamox'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 204-min | OK | FAIL | MISSING unit count value '30' (from '30 Pills') |
| 206-min | FAIL | FAIL | MISSING brand/ingredient from ['cabergoline', 'dostinex'] · MISSING dosage value '0.5' (from '0.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 207-min | FAIL | OK | MISSING brand/ingredient from ['dimenhydrinate', 'dramamine'] · MISSING dosage value '50' (from '50 mg') |
| 208-min | FAIL | OK | MISSING brand/ingredient from ['bisacodyl', 'dulcolax'] · MISSING dosage value '5' (from '5 mg') |
| 209-min | FAIL | OK | MISSING brand/ingredient from ['erythromycin'] · MISSING dosage value '250' (from '250 mg') |
| 210-min | FAIL | OK | MISSING dosage value '0.4' (from '0.4 mg') |
| 211-min | FAIL | FAIL | MISSING brand/ingredient from ['glucophage', 'metformin'] · MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 213-min | FAIL | OK | MISSING brand/ingredient from ['malegra dxt', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg/30 mg') |
| 214-min | FAIL | OK | MISSING brand/ingredient from ['malegra dxt plus', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg/60 mg') |
| 215-min | FAIL | FAIL | MISSING brand/ingredient from ['malegra fxt', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg/20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 216-min | FAIL | FAIL | MISSING dosage value '100' (from '100 mg/40 mg') · MISSING unit count value '30' (from '30 Pills') |
| 217-min | OK | FAIL | MISSING brand/ingredient from ['medrol', 'methylprednisolone'] · MISSING unit count value '30' (from '30 Pills') |
| 218-min | FAIL | FAIL | MISSING brand/ingredient from ['silagra', 'sildenafil'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 22-min | FAIL | FAIL | MISSING brand/ingredient from ['effexor', 'venlafaxine'] · MISSING dosage value '75' (from '75 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 220-min | FAIL | OK | MISSING brand/ingredient from ['sildenafil', 'zenegra'] · MISSING dosage value '100' (from '100 mg') |
| 222-min | FAIL | FAIL | MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 223-min | FAIL | FAIL | MISSING brand/ingredient from ['levitra soft tabs', 'vardenafil hcl'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '10' (from '10 Pills') |
| 224-min | FAIL | OK | MISSING brand/ingredient from ['caverta', 'sildenafil'] · MISSING dosage value '100' (from '100 mg') |
| 225-min | FAIL | FAIL | MISSING brand/ingredient from ['cabergoline', 'cabgolin'] · MISSING dosage value '0.5' (from '0.5 mg') · MISSING unit count value '10' (from '10 Pills') |
| 226-min | FAIL | FAIL | MISSING brand/ingredient from ['aciclovir', 'zovirax'] · MISSING dosage value '400' (from '400 mg') · MISSING unit count value '1' (from '1 Pills') |
| 227-min | FAIL | OK | MISSING brand/ingredient from ['deltasone', 'prednisolone'] · MISSING dosage value '20' (from '20 mg') |
| 228-min | FAIL | FAIL | MISSING brand/ingredient from ['ketoconazole', 'nizoral'] · MISSING dosage value '2' (from '2%') · MISSING unit count value '1' (from '1 Pills') |
| 229-min | FAIL | FAIL | MISSING dosage value '0.01' (from '0.01%') · MISSING unit count value '1' (from '1 Bottle') |
| 230-min | FAIL | FAIL | MISSING dosage value '15' (from '15 mg') · MISSING unit count value '30' (from '30 Pills') |
| 231-min | OK | FAIL | MISSING brand/ingredient from ['acticin', 'permethrin'] · MISSING unit count value '1' (from '1 Pills') |
| 232-min | FAIL | FAIL | MISSING dosage value '5' (from '5%') · MISSING unit count value '1' (from '1 Pills') |
| 233-min | FAIL | OK | MISSING brand/ingredient from ['asacol', 'mesalazine'] · MISSING dosage value '400' (from '400 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 234-min | OK | FAIL | MISSING brand/ingredient from ['avapro', 'irbesartan'] · MISSING unit count value '30' (from '30 Pills') |
| 235-min | FAIL | FAIL | MISSING dosage value '2' (from '2 mg') · MISSING unit count value '30' (from '30 Pills') |
| 237-min | FAIL | OK | MISSING dosage value '100' (from '100 mg') |
| 239-min | FAIL | OK | MISSING brand/ingredient from ['cafergot', 'caffeine/ergotamine'] · MISSING dosage value '1' (from '1 mg/100 mg') |
| 240-min | FAIL | FAIL | MISSING brand/ingredient from ['fildena', 'sildenafil'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '10' (from '10 Pills') |
| 242-min | FAIL | FAIL | MISSING brand/ingredient from ['lamictal', 'lamotrigine'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 243-min | FAIL | OK | MISSING brand/ingredient from ['lamisil', 'terbinafine'] · MISSING dosage value '250' (from '250 mg') |
| 244-min | OK | FAIL | MISSING brand/ingredient from ['lamisil', 'terbinafine'] · MISSING unit count value '3' (from '3 Pills') |
| 245-min | FAIL | OK | MISSING brand/ingredient from ['levaquin', 'levofloxacin'] · MISSING dosage value '500' (from '500 mg') |
| 246-min | OK | FAIL | MISSING brand/ingredient from ['escitalopram', 'lexapro'] · MISSING unit count value '30' (from '30 Pills') |
| 247-min | FAIL | FAIL | MISSING brand/ingredient from ['metoprolol', 'toprol xl'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 248-min | FAIL | OK | MISSING dosage value '15' (from '15 g') |
| 249-min | FAIL | FAIL | MISSING brand/ingredient from ['minipress', 'prazosin'] · MISSING dosage value '2' (from '2 mg') · MISSING unit count value '30' (from '30 Pills') |
| 25-min | FAIL | FAIL | MISSING brand/ingredient from ['paroxetine', 'paxil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 250-min | FAIL | FAIL | MISSING brand/ingredient from ['domperidone', 'motilium'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 251-min | FAIL | FAIL | MISSING brand/ingredient from ['gabapentin', 'neurontin'] · MISSING dosage value '300' (from '300 mg') · MISSING unit count value '30' (from '30 Pills') |
| 252-min | FAIL | OK | MISSING brand/ingredient from ['nitroglycerin'] · MISSING dosage value '0.4' (from '0.4 mg') |
| 253-min | FAIL | OK | MISSING dosage value '800' (from '800 mg') |
| 254-min | FAIL | FAIL | MISSING brand/ingredient from ['norfloxacin', 'noroxin'] · MISSING dosage value '400' (from '400 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 255-min | FAIL | OK | MISSING dosage value '10' (from '10 mg') |
| 257-min | FAIL | OK | MISSING dosage value '10' (from '10 mg') |
| 258-min | FAIL | FAIL | MISSING dosage value '3' (from '3 mg') · MISSING unit count value '30' (from '30 Pills') |
| 26-min | FAIL | FAIL | MISSING brand/ingredient from ['fluoxetine', 'prozac'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 260-min | FAIL | OK | MISSING dosage value '50' (from '50 mg') |
| 261-min | FAIL | FAIL | MISSING brand/ingredient from ['topamax', 'topiramate'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 262-min | OK | FAIL | MISSING brand/ingredient from ['torsemide'] · MISSING unit count value '30' (from '30 Pills') |
| 263-min | OK | FAIL | MISSING brand/ingredient from ['ketorolac', 'toradol'] · MISSING unit count value '30' (from '30 Pills') |
| 265-min | FAIL | FAIL | MISSING brand/ingredient from ['benadryl', 'diphenhydramine'] · MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 266-min | FAIL | OK | MISSING brand/ingredient from ['diphenhydramine', 'sominex'] · MISSING dosage value '50' (from '50 mg') |
| 267-min | FAIL | OK | MISSING brand/ingredient from ['diphenhydramine', 'unisom'] · MISSING dosage value '50' (from '50 mg') |
| 268-min | FAIL | OK | MISSING dosage value '90' (from '90 mcg/puff') |
| 269-min | FAIL | FAIL | MISSING brand/ingredient from ['latanoprost', 'xalatan'] · MISSING dosage value '0.005' (from '0.005%') · MISSING unit count value '1' (from '1 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 270-min | FAIL | FAIL | MISSING brand/ingredient from ['bisoprolol', 'zebeta'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 271-min | FAIL | FAIL | MISSING brand/ingredient from ['ondansetron', 'zofran'] · MISSING dosage value '8' (from '8 mg') · MISSING unit count value '30' (from '30 Pills') |
| 272-min | FAIL | OK | MISSING dosage value '5' (from '5 mg') |
| 277-min | FAIL | OK | MISSING dosage value '30' (from '30 mg') |
| 278-min | FAIL | FAIL | MISSING dosage value '150' (from '150 mg/12.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 279-min | FAIL | OK | MISSING brand/ingredient from ['lopressor', 'metoprolol'] · MISSING dosage value '50' (from '50 mg') |
| 28-min | OK | FAIL | MISSING brand/ingredient from ['diflucan', 'fluconazole'] · MISSING unit count value '30' (from '30 Pills') |
| 281-min | FAIL | FAIL | MISSING dosage value '50' (from '50 mg/12.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 283-min | FAIL | FAIL | MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 284-min | FAIL | OK | MISSING dosage value '25' (from '25 mg') |
| 285-min | OK | FAIL | MISSING unit count value '60' (from '60 Pills') |
| 286-min | FAIL | FAIL | MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 288-min | FAIL | FAIL | MISSING brand/ingredient from ['aleve', 'naproxen'] · MISSING dosage value '220' (from '220 mg') · MISSING unit count value '30' (from '30 Pills') |
| 29-min | FAIL | FAIL | MISSING brand/ingredient from ['ketoconazole', 'nizoral'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '1' (from '1 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 290-min | FAIL | FAIL | MISSING dosage value '20' (from '20 mg') · MISSING unit count value '60' (from '60 Pills') |
| 291-min | FAIL | FAIL | MISSING brand/ingredient from ['avana', 'avanafil'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '4' (from '4 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 293-min | OK | FAIL | MISSING brand/ingredient from ['albuterol', 'proventil'] · MISSING unit count value '1' (from '1 Pills') |
| 295-min | FAIL | OK | MISSING dosage value '150' (from '150 mg') |
| 296-min | FAIL | FAIL | MISSING brand/ingredient from ['dexanil', 'escitalopram'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 297-min | FAIL | FAIL | MISSING dosage value '5' (from '5 mg') · MISSING unit count value '60' (from '60 Pills') |
| 298-min | FAIL | OK | MISSING brand/ingredient from ['anaridex', 'anastrozole'] · MISSING dosage value '1' (from '1 mg') |
| 299-min | FAIL | OK | MISSING brand/ingredient from ['dutas', 'dutasteride'] · MISSING dosage value '0.5' (from '0.5 mg') |
| 3-min | FAIL | OK | MISSING brand/ingredient from ['alavert', 'loratadine'] · MISSING dosage value '10' (from '10 mg') |
| 30-min | FAIL | FAIL | MISSING brand/ingredient from ['loxapine', 'loxitane'] · MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 300-min | OK | FAIL | MISSING unit count value '30' (from '30 Pills') |
| 301-min | FAIL | FAIL | MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 302-min | FAIL | OK | MISSING dosage value '100' (from '100 mg') |
| 303-min | FAIL | OK | MISSING dosage value '3' (from '3 mg') |
| 304-min | FAIL | FAIL | MISSING brand/ingredient from ['sonata', 'zaleplon'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 305-min | FAIL | OK | MISSING brand/ingredient from ['progesterone', 'utrogestan'] · MISSING dosage value '100' (from '100 mg') |
| 307-min | OK | FAIL | MISSING brand/ingredient from ['centrex', 'valacyclovir'] · MISSING unit count value '30' (from '30 Pills') |
| 308-min | FAIL | FAIL | MISSING brand/ingredient from ['bromazepam', 'lexotanil'] · MISSING dosage value '3' (from '3 mg') · MISSING unit count value '30' (from '30 Pills') |
| 309-min | FAIL | OK | MISSING brand/ingredient from ['estradiol', 'evorel'] · MISSING dosage value '50' (from '50 mcg/day') |
| 31-min | FAIL | FAIL | MISSING brand/ingredient from ['risperdal', 'risperidone'] · MISSING dosage value '2' (from '2 mg') · MISSING unit count value '30' (from '30 Pills') |
| 310-min | FAIL | OK | MISSING brand/ingredient from ['kamagra', 'kamagra soft tabs', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg') |
| 311-min | FAIL | FAIL | MISSING brand/ingredient from ['kamagra gold', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 312-min | FAIL | FAIL | MISSING brand/ingredient from ['cialis', 'cialis strips', 'tadalafil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '1' (from '1 Pills') |
| 313-min | FAIL | FAIL | MISSING brand/ingredient from ['sildenafil citrate', 'viagra', 'viagra strips'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '1' (from '1 Pills') |
| 314-min | FAIL | OK | MISSING brand/ingredient from ['avanafil + dapoxetine hcl', 'super avana'] · MISSING dosage value '200' (from '200 mg/60 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 315-min | FAIL | FAIL | MISSING brand/ingredient from ['amantadine', 'symmetrel'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 316-min | FAIL | FAIL | MISSING brand/ingredient from ['beclomethasone dipropionate', 'beconase aq'] · MISSING dosage value '50' (from '50 mcg/spray') · MISSING unit count value '1' (from '1 Pills') |
| 317-min | FAIL | OK | MISSING brand/ingredient from ['benzac', 'benzoyl'] · MISSING dosage value '5' (from '5%') |
| 319-min | FAIL | OK | MISSING brand/ingredient from ['chloramphenicol', 'chloromycetin'] · MISSING dosage value '250' (from '250 mg') |
| 320-min | FAIL | OK | MISSING brand/ingredient from ['clozapine', 'clozaril'] · MISSING dosage value '100' (from '100 mg') |
| 322-min | FAIL | FAIL | MISSING brand/ingredient from ['eulexin', 'flutamide'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 323-min | FAIL | OK | MISSING dosage value '400' (from '400 mg') |
| 324-min | FAIL | FAIL | MISSING brand/ingredient from ['hyzyd', 'isoniazid'] · MISSING dosage value '300' (from '300 mg') · MISSING unit count value '30' (from '30 Pills') |
| 325-min | FAIL | OK | MISSING brand/ingredient from ['methotrexate', 'trexall'] · MISSING dosage value '2.5' (from '2.5 mg') |
| 326-min | FAIL | FAIL | MISSING brand/ingredient from ['minocin', 'minocycline'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 327-min | FAIL | FAIL | MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 328-min | FAIL | OK | MISSING dosage value '400' (from '400 mg') |
| 329-min | FAIL | FAIL | MISSING brand/ingredient from ['penegra', 'sildenafil'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '10' (from '10 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 330-min | FAIL | OK | MISSING brand/ingredient from ['fasigyn', 'tinidazole'] · MISSING dosage value '500' (from '500 mg') |
| 331-min | FAIL | OK | MISSING dosage value '100' (from '100 mg') |
| 332-min | FAIL | OK | MISSING dosage value '10' (from '10 mg') |
| 333-min | FAIL | OK | MISSING dosage value '3' (from '3 mg') |
| 334-min | FAIL | FAIL | MISSING dosage value '5' (from '5 mg') · MISSING unit count value '60' (from '60 Pills') |
| 335-min | FAIL | FAIL | MISSING brand/ingredient from ['stilnox', 'stilnox brand', 'zolpidem tartrate'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 336-min | FAIL | FAIL | MISSING brand/ingredient from ['conjugated estrogens', 'premarin'] · MISSING dosage value '0.625' (from '0.625 mg') · MISSING unit count value '30' (from '30 Pills') |
| 337-min | FAIL | OK | MISSING brand/ingredient from ['kamagra effervescent', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg') |
| 340-min | FAIL | FAIL | MISSING dosage value '0.5' (from '0.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 341-min | OK | FAIL | MISSING brand/ingredient from ['etizest', 'etizolam'] · MISSING unit count value '30' (from '30 Pills') |
| 344-min | FAIL | FAIL | MISSING brand/ingredient from ['modafinil'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 347-min | — | FAIL | MISSING brand/ingredient from ['sildenafil / tadalafil / vardenafil', 'test pack l-vc'] · MISSING unit count value '1' (from '1 Pills') |
| 348-min | — | FAIL | MISSING brand/ingredient from ['sildenafil / tadalafil / vardenafil / avanafil', 'test pack l-vl'] · MISSING unit count value '1' (from '1 Pills') |
| 35-min | FAIL | OK | MISSING brand/ingredient from ['albendazole', 'albenza'] · MISSING dosage value '200' (from '200 mg') |
| 351-min | OK | FAIL | MISSING unit count value '1' (from '1 Pills') |
| 352-min | OK | FAIL | MISSING brand/ingredient from ['aleve', 'naproxen sodium'] · MISSING unit count value '30' (from '30 Pills') |
| 353-min | FAIL | OK | MISSING brand/ingredient from ['benzocaine + cetylpyridinium chloride', 'cepacol'] · MISSING dosage value '1.4' (from '1.4 mg') |
| 354-min | FAIL | OK | MISSING dosage value '200' (from '200 mg') |
| 356-min | FAIL | FAIL | MISSING brand/ingredient from ['morphine', 'morphine sulfate'] · MISSING dosage value '30' (from '30 mg') · MISSING unit count value '30' (from '30 Pills') |
| 359-min | FAIL | FAIL | MISSING dosage value '2' (from '2 mg') · MISSING unit count value '30' (from '30 Pills') |
| 36-min | OK | FAIL | MISSING unit count value '30' (from '30 Pills') |
| 360-min | FAIL | FAIL | MISSING brand/ingredient from ['restoril', 'temazepam'] · MISSING dosage value '15' (from '15 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 362-min | FAIL | OK | MISSING brand/ingredient from ['hydrocodone', 'hydrocodone bitartrate'] · MISSING dosage value '10' (from '10 mg') |
| 363-min | FAIL | FAIL | MISSING brand/ingredient from ['oxycodone hcl 30mg', 'roxicodone', 'roxicodone m30'] · MISSING dosage value '30' (from '30 mg') · MISSING unit count value '30' (from '30 Pills') |
| 364-min | FAIL | OK | MISSING dosage value '10' (from '10 mg') |
| 365-min | FAIL | OK | MISSING brand/ingredient from ['tapentadol', 'tapentadol hcl'] · MISSING dosage value '50' (from '50 mg') |
| 366-min | OK | FAIL | MISSING brand/ingredient from ['acivir cream', 'acivir cream by cipla 5%', 'acyclovir 5%'] · MISSING unit count value '1' (from '1 Pills') |
| 367-min | FAIL | FAIL | MISSING dosage value '400' (from '400 mg') · MISSING unit count value '1' (from '1 Pills') |
| 369-min | FAIL | OK | MISSING dosage value '4' (from '4 mg') |
| 37-min | OK | FAIL | MISSING unit count value '1' (from '1 Pills') |
| 370-min | FAIL | FAIL | MISSING brand/ingredient from ['albuterol', 'ventolin', 'ventolin generic'] · MISSING dosage value '100' (from '100 mcg') · MISSING unit count value '1' (from '1 Pills') |
| 371-min | FAIL | OK | MISSING brand/ingredient from ['imipramine', 'tofranil', 'tofranil generic'] · MISSING dosage value '25' (from '25 mg') |
| 372-min | FAIL | FAIL | MISSING dosage value '37.5' (from '37.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 373-min | FAIL | OK | MISSING brand/ingredient from ['azithromycin', 'azithromycin generic'] · MISSING dosage value '250' (from '250 mg') |
| 374-min | FAIL | FAIL | MISSING brand/ingredient from ['cephalexin', 'cephalexin generic'] · MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 375-min | FAIL | OK | MISSING dosage value '200' (from '200 mg') |
| 376-min | FAIL | FAIL | MISSING brand/ingredient from ['lisinopril'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 377-min | FAIL | OK | MISSING dosage value '80' (from '80 mg') |
| 378-min | FAIL | FAIL | MISSING brand/ingredient from ['amiodarone', 'cordarone', 'cordarone generic'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 379-min | OK | FAIL | MISSING unit count value '1' (from '1 Bottle') |
| 38-min | FAIL | FAIL | MISSING brand/ingredient from ['prednisone'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 380-min | FAIL | FAIL | MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 382-min | FAIL | FAIL | MISSING brand/ingredient from ['allopurinol', 'allopurinol generic'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 383-min | FAIL | OK | MISSING brand/ingredient from ['chloroquine', 'chloroquine generic'] · MISSING dosage value '250' (from '250 mg') |
| 384-min | FAIL | FAIL | MISSING brand/ingredient from ['ibuprofen', 'ibuprofen generic'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 385-min | FAIL | FAIL | MISSING dosage value '0.05' (from '0.05%') · MISSING unit count value '1' (from '1 Pills') |
| 386-min | FAIL | FAIL | MISSING dosage value '0.1' (from '0.1%') · MISSING unit count value '1' (from '1 Pills') |
| 387-min | FAIL | OK | MISSING brand/ingredient from ['addyi', 'flibanserin'] · MISSING dosage value '100' (from '100 mg') |
| 388-min | FAIL | FAIL | MISSING brand/ingredient from ['female cialis', 'femalefil'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '10' (from '10 Pills') |
| 390-min | FAIL | FAIL | MISSING brand/ingredient from ['diclofenac', 'volini gel'] · MISSING dosage value '1' (from '1%') · MISSING unit count value '1' (from '1 Pills') |
| 391-min | FAIL | OK | MISSING brand/ingredient from ['analgin', 'analgin generic'] · MISSING dosage value '500' (from '500 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 393-min | FAIL | FAIL | MISSING dosage value '250' (from '250 mcg/100 mcg') · MISSING unit count value '1' (from '1 Inhaler') |
| 395-min | FAIL | FAIL | MISSING brand/ingredient from ['endogest', 'progesterone'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 398-min | FAIL | FAIL | MISSING brand/ingredient from ['testorapid', 'testosterone propionate'] · MISSING dosage value '100' (from '100 mg/ml') · MISSING unit count value '10' (from '10 Pills') |
| 4-min | FAIL | FAIL | MISSING dosage value '4' (from '4 mg') · MISSING unit count value '30' (from '30 Pills') |
| 40-min | FAIL | FAIL | MISSING brand/ingredient from ['amlodipine', 'norvasc'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 400-min | OK | FAIL | MISSING brand/ingredient from ['zinc acetate + doxycycline + ivermectin', 'ziverdo', 'ziverdo kit'] · MISSING unit count value '1' (from '1 Pills') |
| 402-min | FAIL | FAIL | MISSING brand/ingredient from ['ozempic', 'semaglutide'] · MISSING dosage value '2' (from '2 mg') · MISSING unit count value '1' (from '1 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 403-min | FAIL | FAIL | MISSING brand/ingredient from ['rybelsus', 'semaglutide'] · MISSING dosage value '7' (from '7 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 404-min | FAIL | FAIL | MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 405-min | FAIL | OK | MISSING dosage value '15' (from '15 mg') |
| 406-min | FAIL | OK | MISSING dosage value '15' (from '15 mg') |
| 407-min | OK | FAIL | MISSING unit count value '1' (from '1 Pills') |
| 408-min | FAIL | OK | MISSING brand/ingredient from ['semaglutide', 'wegovy'] · MISSING dosage value '2.4' (from '2.4 mg') |
| 41-min | FAIL | FAIL | MISSING brand/ingredient from ['esomeprazole', 'nexium'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 410-min | FAIL | FAIL | MISSING brand/ingredient from ['sustanon', 'testosterone blend'] · MISSING dosage value '250' (from '250 mg/ml') · MISSING unit count value '1' (from '1 Pills') |
| 411-min | OK | FAIL | MISSING brand/ingredient from ['testosterone cypionate'] · MISSING unit count value '1' (from '1 Pills') |
| 412-min | FAIL | FAIL | MISSING brand/ingredient from ['testosterone enanthate'] · MISSING dosage value '250' (from '250 mg/ml') · MISSING unit count value '1' (from '1 Pills') |
| 413-min | FAIL | FAIL | MISSING brand/ingredient from ['boldenone', 'boldenone undecylenate'] · MISSING dosage value '200' (from '200 mg/ml') · MISSING unit count value '10' (from '10 Pills') |
| 414-min | FAIL | FAIL | MISSING dosage value '100' (from '100 mg/ml') · MISSING unit count value '10' (from '10 Vials') |
| 415-min | OK | FAIL | MISSING unit count value '10' (from '10 Vials') |
| 417-min | FAIL | FAIL | MISSING brand/ingredient from ['drostanolone propionate', 'masteron'] · MISSING dosage value '100' (from '100 mg/ml') · MISSING unit count value '1' (from '1 Pills') |
| 418-min | FAIL | FAIL | MISSING brand/ingredient from ['methandienone'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '100' (from '100 Pills') |
| 419-min | OK | FAIL | MISSING unit count value '100' (from '100 Pills') |
| 42-min | FAIL | FAIL | MISSING dosage value '200' (from '200 mcg') · MISSING unit count value '30' (from '30 Pills') |
| 422-min | FAIL | OK | MISSING dosage value '10' (from '10 mg') |
| 423-min | FAIL | FAIL | MISSING brand/ingredient from ['halcion', 'triazolam'] · MISSING dosage value '0.25' (from '0.25 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 424-min | FAIL | FAIL | MISSING brand/ingredient from ['tirzepatide', 'zepbound'] · MISSING dosage value '2.5' (from '2.5 mg') · MISSING unit count value '1' (from '1 Pills') |
| 425-min | FAIL | OK | MISSING brand/ingredient from ['mounjaro', 'tirzepatide'] · MISSING dosage value '5' (from '5 mg') |
| 426-min | FAIL | FAIL | MISSING brand/ingredient from ['cialis oral jelly', 'tadalafil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '7' (from '7 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 427-min | FAIL | FAIL | MISSING brand/ingredient from ['kamagra chewable', 'soft'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 428-min | OK | FAIL | MISSING unit count value '1' (from '1 Pills') |
| 429-min | FAIL | FAIL | MISSING brand/ingredient from ['levitra', 'levitra oral jelly', 'vardenafil hcl'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '4' (from '4 Pills') |
| 43-min | FAIL | FAIL | MISSING brand/ingredient from ['lansoprazole', 'prevacid'] · MISSING dosage value '15' (from '15 mg') · MISSING unit count value '30' (from '30 Pills') |
| 430-min | FAIL | OK | MISSING brand/ingredient from ['pantoprazole', 'protonix'] · MISSING dosage value '40' (from '40 mg') |
| 431-min | OK | FAIL | MISSING unit count value '30' (from '30 Pills') |
| 432-min | FAIL | OK | MISSING dosage value '50' (from '50 mg') |
| 433-min | FAIL | FAIL | MISSING brand/ingredient from ['bimatoprost', 'latisse'] · MISSING dosage value '3' (from '3 ml') · MISSING unit count value '1' (from '1 Bottle') |
| 434-min | FAIL | OK | MISSING dosage value '100' (from '100 mg') |
| 44-min | FAIL | FAIL | MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 45-min | FAIL | FAIL | MISSING dosage value '150' (from '150 mg') · MISSING unit count value '30' (from '30 Pills') |
| 46-min | OK | FAIL | MISSING brand/ingredient from ['finasteride', 'propecia'] · MISSING unit count value '30' (from '30 Pills') |
| 47-min | FAIL | OK | MISSING brand/ingredient from ['coumadin', 'warfarin'] · MISSING dosage value '5' (from '5 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 49-min | FAIL | OK | MISSING brand/ingredient from ['clopidogrel', 'plavix'] · MISSING dosage value '75' (from '75 mg') |
| 5-min | FAIL | FAIL | MISSING dosage value '4' (from '4 mg') · MISSING unit count value '30' (from '30 Pills') |
| 50-min | FAIL | OK | MISSING dosage value '40' (from '40 mg') |
| 51-min | FAIL | FAIL | MISSING brand/ingredient from ['sofosbuvir'] · MISSING dosage value '400' (from '400 mg') · MISSING unit count value '28' (from '28 Pills') |
| 52-min | FAIL | FAIL | MISSING dosage value '400' (from '400 mg') · MISSING unit count value '28' (from '28 Pills') |
| 58-min | FAIL | OK | MISSING dosage value '5' (from '5 mg') |
| 59-min | FAIL | OK | MISSING dosage value '20' (from '20 mg') |
| 6-min | FAIL | OK | MISSING dosage value '4' (from '4 mg') |
| 60-min | FAIL | FAIL | MISSING brand/ingredient from ['cialis professional', 'tadalafil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '10' (from '10 Pills') |
| 61-min | FAIL | FAIL | MISSING brand/ingredient from ['cialis soft tabs', 'tadalafil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '10' (from '10 Pills') |
| 62-min | OK | FAIL | MISSING unit count value '10' (from '10 Pills') |
| 63-min | FAIL | FAIL | MISSING brand/ingredient from ['dapoxetine', 'priligy'] · MISSING dosage value '30' (from '30 mg') · MISSING unit count value '10' (from '10 Pills') |
| 64-min | FAIL | OK | MISSING brand/ingredient from ['kamagra', 'sildenafil'] · MISSING dosage value '100' (from '100 mg') |
| 65-min | OK | FAIL | MISSING brand/ingredient from ['kamagra oral jelly', 'sildenafil citrate'] · MISSING unit count value '7' (from '7 Pills') |
| 66-min | OK | FAIL | MISSING brand/ingredient from ['levitra', 'vardenafil'] · MISSING unit count value '4' (from '4 Pills') |
| 67-min | FAIL | FAIL | MISSING brand/ingredient from ['levitra brand', 'vardenafil hcl'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '4' (from '4 Pills') |
| 70-min | FAIL | FAIL | MISSING brand/ingredient from ['sildenafil citrate + dapoxetine hcl', 'super kamagra'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '4' (from '4 Pills') |
| 71-min | FAIL | FAIL | MISSING brand/ingredient from ['sildenafil citrate + dapoxetine hcl', 'super p force'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '4' (from '4 Pills') |
| 72-min | OK | FAIL | MISSING unit count value '10' (from '10 Pills') |
| 74-min | FAIL | FAIL | MISSING brand/ingredient from ['sildenafil', 'viagra'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '1' (from '1 Pills') |
| 75-min | FAIL | FAIL | MISSING brand/ingredient from ['sildenafil citrate', 'viagra gold'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 76-min | FAIL | OK | MISSING dosage value '100' (from '100 mg') |
| 77-min | FAIL | OK | MISSING dosage value '100' (from '100 mg') |
| 8-min | FAIL | FAIL | MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 80-min | FAIL | OK | MISSING brand/ingredient from ['sildenafil', 'viprogra'] · MISSING dosage value '100' (from '100 mg') |
| 81-min | FAIL | FAIL | MISSING brand/ingredient from ['eldepryl', 'selegiline'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 82-min | FAIL | OK | MISSING brand/ingredient from ['bromocriptine mesylate', 'parlodel'] · MISSING dosage value '2.5' (from '2.5 mg') |
| 83-min | FAIL | OK | MISSING brand/ingredient from ['baclofen'] · MISSING dosage value '20' (from '20 mg') |
| 86-min | OK | FAIL | MISSING unit count value '10' (from '10 Pills') |
| 88-min | FAIL | FAIL | MISSING brand/ingredient from ['methocarbamol', 'robaxin'] · MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 89-min | FAIL | OK | MISSING brand/ingredient from ['boswellia serrata extract', 'shallaki'] · MISSING dosage value '500' (from '500 mg') |
| 9-min | FAIL | FAIL | MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 90-min | FAIL | OK | MISSING dosage value '100' (from '100 mg') |
| 91-min | FAIL | OK | MISSING dosage value '250' (from '250 mg') |
| 92-min | FAIL | OK | MISSING dosage value '20' (from '20 mg') |
| 93-min | FAIL | FAIL | MISSING brand/ingredient from ['carbamazepine', 'tegretol'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 94-min | FAIL | FAIL | MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 95-min | FAIL | OK | MISSING brand/ingredient from ['diclofenac', 'voltaren'] · MISSING dosage value '25' (from '25 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 96-min | FAIL | FAIL | MISSING brand/ingredient from ['diclofenac sodium', 'voveran'] · MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 97-min | FAIL | OK | MISSING brand/ingredient from ['diclofenac sodium', 'voveran sr'] · MISSING dosage value '100' (from '100 mg') |
| 98-min | FAIL | FAIL | MISSING brand/ingredient from ['tizanidine', 'zanaflex'] · MISSING dosage value '4' (from '4 mg') · MISSING unit count value '30' (from '30 Pills') |
| 99-min | FAIL | OK | MISSING brand/ingredient from ['acetaminophen'] · MISSING dosage value '500' (from '500 mg') |

## Results

| SKU | Brand/Ingr Found | Brand Dup | Dosage Found | Count Found | Status |
|---|---|---|---|---|---|
| 1-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['atomoxetine'] |
| 10-min | OK | OK | OK | OK | OK |
| 100-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['arcoxia', 'etoricoxib'] |
| 101-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['celebrex', 'celecoxib'] · MISSING dosage value '100' (from '100 mg') |
| 102-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['isordil', 'isosorbide dinitrate'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 103-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['maxalt', 'rizatriptan'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '10' (from '10 Pills') |
| 104-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['meloxicam', 'mobic'] · MISSING unit count value '30' (from '30 Pills') |
| 105-min | OK | OK | OK | OK | OK |
| 106-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 107-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['tramadol', 'tramadol hcl'] |
| 108-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['acetaminophen', 'tylenol'] · MISSING dosage value '500' (from '500 mg') |
| 109-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['tramadol', 'ultram'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 11-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['amoxicillin', 'amoxil'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 110-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['accutane', 'isotretinoin'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 111-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['retin-a cream', 'retin-a cream 0.025%', 'tretinoin'] |
| 112-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['champix', 'varenicline tartrate'] · MISSING dosage value '1' (from '1 mg') |
| 113-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['bupropion', 'zyban'] · MISSING dosage value '150' (from '150 mg') |
| 114-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '100' (from '100 mcg') |
| 115-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '60' (from '60 mg') · MISSING unit count value '30' (from '30 Pills') |
| 116-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['lida daidaihua', 'sibutramine hcl'] |
| 117-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') |
| 118-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '120' (from '120 mg') · MISSING unit count value '30' (from '30 Pills') |
| 119-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '1' (from '1 mg') |
| 12-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 120-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['evista', 'raloxifene'] · MISSING unit count value '30' (from '30 Pills') |
| 121-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['alendronic acid', 'fosamax'] · MISSING dosage value '70' (from '70 mg') · MISSING unit count value '30' (from '30 Pills') |
| 122-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['allylestrenol', 'gestanin'] |
| 124-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '30' (from '30 Implants') |
| 125-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 126-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['medroxyprogesterone', 'provera'] · MISSING unit count value '30' (from '30 Pills') |
| 127-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '1' (from '1 Pills') |
| 128-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['aygestin', 'norethindrone acetate'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 129-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['clomid', 'clomiphene'] · MISSING dosage value '50' (from '50 mg') |
| 13-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '500' (from '500 mg') |
| 130-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['danazol', 'danocrine'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 131-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 132-min | OK | OK | OK | OK | OK |
| 133-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 134-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['atarax', 'hydroxyzine'] · MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 135-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['ativan', 'lorazepam'] · MISSING dosage value '1' (from '1 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 136-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['buspar', 'buspirone'] · MISSING unit count value '30' (from '30 Pills') |
| 138-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '30' (from '30mg/500mg') |
| 139-min | OK | OK | OK | OK | OK |
| 14-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['bactrim', 'trimethoprim'] |
| 141-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['deca durabolin', 'testosterone'] · MISSING dosage value '50' (from '50 mg/mL') |
| 143-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '1.62' (from '1.62%') |
| 144-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '10' (from '10 Pills') |
| 145-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '10' (from '10 Pills') |
| 146-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['hucog-10000 hp', 'human chorionic gonadotropin'] · MISSING dosage value '10000' (from '10000 IU') · MISSING unit count value '10' (from '10 Pills') |
| 147-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sustaviron-250', 'testosterone blend'] · MISSING dosage value '250' (from '250 mg/mL') · MISSING unit count value '10' (from '10 Pills') |
| 148-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['drostanolone propionate', 'masteron'] · MISSING dosage value '100' (from '100 mg/mL') · MISSING unit count value '1' (from '1 Pills') |
| 149-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['modafinil', 'modalert'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 15-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cipro', 'ciprofloxacin'] · MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 150-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '150' (from '150 mg') · MISSING unit count value '30' (from '30 Pills') |
| 151-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['modafinil', 'provigil'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 152-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['armodafinil', 'artvigil'] · MISSING dosage value '150' (from '150 mg') |
| 155-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['imovane', 'zopiclone'] |
| 156-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '0.5' (from '0.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 157-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['diazepam', 'valium'] · MISSING dosage value '5' (from '5 mg') |
| 158-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['clonazepam', 'klonopin'] · MISSING dosage value '1' (from '1 mg') |
| 159-min | OK | OK | OK | OK | OK |
| 16-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['doxycycline', 'doxycycline hyclate'] · MISSING dosage value '100' (from '100 mg') |
| 160-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['avanafil', 'stendra'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 161-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['apcalis oral jelly', 'tadalafil'] · MISSING unit count value '7' (from '7 Pills') |
| 162-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['tadalafil + dapoxetine hcl', 'tadapox'] · MISSING unit count value '10' (from '10 Pills') |
| 164-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['anastrozole', 'arimidex'] · MISSING dosage value '1' (from '1 mg') · MISSING unit count value '30' (from '30 Pills') |
| 165-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['claritin', 'loratadine'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '60' (from '60 Pills') |
| 166-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['clarinex', 'desloratadine'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 17-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['flagyl', 'metronidazole'] · MISSING dosage value '500' (from '500 mg') |
| 170-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['fliban', 'flibanserin'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 171-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['hydrochlorothiazide', 'microzide'] · MISSING dosage value '25' (from '25 mg') |
| 172-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['quetiapine', 'qutan'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 173-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '40' (from '40 mg') · MISSING unit count value '30' (from '30 Pills') |
| 175-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['nolvadex', 'tamoxifen'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 176-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sertraline', 'zoloft'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 177-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '250' (from '250 mg') |
| 178-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['aciphex', 'rabeprazole'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '20' (from '20 Pills') |
| 179-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['actos', 'pioglitazone'] |
| 18-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['efavirenz', 'sustiva'] · MISSING dosage value '600' (from '600 mg') |
| 180-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '25' (from '25 mg') |
| 181-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['alesse', 'levonorgestrel + ethinylestradiol'] · MISSING dosage value '20' (from '20 mcg') · MISSING unit count value '30' (from '30 Pills') |
| 183-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 184-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['amaryl', 'glimepiride'] · MISSING dosage value '2' (from '2 mg') |
| 185-min | OK | OK | OK | OK | OK |
| 186-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 187-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['antabuse', 'disulfiram'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 188-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['aralen', 'chloroquine'] |
| 189-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['aricept', 'donepezil'] · MISSING dosage value '10' (from '10 mg') |
| 19-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['azithromycin', 'zithromax'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 190-min | OK | OK | OK | OK | OK |
| 191-min | OK | OK | OK | OK | OK |
| 192-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 194-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['celexa', 'citalopram'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 195-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['cleocin', 'clindamycin'] · MISSING dosage value '150' (from '150 mg') |
| 196-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['cleocin', 'clindamycin'] |
| 197-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['catapres', 'clonidine'] · MISSING dosage value '0.1' (from '0.1 mg') · MISSING unit count value '30' (from '30 Pills') |
| 198-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['colchicine'] · MISSING unit count value '30' (from '30 Pills') |
| 199-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cozaar', 'losartan'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 2-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['atomoxetine', 'strattera'] · MISSING dosage value '40' (from '40 mg') |
| 20-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['abilify', 'aripiprazole'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 200-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['crestor', 'rosuvastatin'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 201-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['desyrel', 'trazodone'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 202-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['detrol', 'tolterodine'] |
| 203-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['acetazolamide', 'diamox'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 204-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '30' (from '30 Pills') |
| 205-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['ditropan', 'oxybutynin'] |
| 206-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cabergoline', 'dostinex'] · MISSING dosage value '0.5' (from '0.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 207-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['dimenhydrinate', 'dramamine'] · MISSING dosage value '50' (from '50 mg') |
| 208-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['bisacodyl', 'dulcolax'] · MISSING dosage value '5' (from '5 mg') |
| 209-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['erythromycin'] · MISSING dosage value '250' (from '250 mg') |
| 21-min | OK | OK | OK | OK | OK |
| 210-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '0.4' (from '0.4 mg') |
| 211-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['glucophage', 'metformin'] · MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 212-min | OK | OK | OK | OK | OK |
| 213-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['malegra dxt', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg/30 mg') |
| 214-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['malegra dxt plus', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg/60 mg') |
| 215-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['malegra fxt', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg/20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 216-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg/40 mg') · MISSING unit count value '30' (from '30 Pills') |
| 217-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['medrol', 'methylprednisolone'] · MISSING unit count value '30' (from '30 Pills') |
| 218-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['silagra', 'sildenafil'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 219-min | OK | OK | OK | OK | OK |
| 22-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['effexor', 'venlafaxine'] · MISSING dosage value '75' (from '75 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 220-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil', 'zenegra'] · MISSING dosage value '100' (from '100 mg') |
| 221-min | OK | OK | OK | OK | OK |
| 222-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 223-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['levitra soft tabs', 'vardenafil hcl'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '10' (from '10 Pills') |
| 224-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['caverta', 'sildenafil'] · MISSING dosage value '100' (from '100 mg') |
| 225-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cabergoline', 'cabgolin'] · MISSING dosage value '0.5' (from '0.5 mg') · MISSING unit count value '10' (from '10 Pills') |
| 226-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['aciclovir', 'zovirax'] · MISSING dosage value '400' (from '400 mg') · MISSING unit count value '1' (from '1 Pills') |
| 227-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['deltasone', 'prednisolone'] · MISSING dosage value '20' (from '20 mg') |
| 228-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['ketoconazole', 'nizoral'] · MISSING dosage value '2' (from '2%') · MISSING unit count value '1' (from '1 Pills') |
| 229-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '0.01' (from '0.01%') · MISSING unit count value '1' (from '1 Bottle') |
| 23-min | OK | OK | OK | OK | OK |
| 230-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '15' (from '15 mg') · MISSING unit count value '30' (from '30 Pills') |
| 231-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['acticin', 'permethrin'] · MISSING unit count value '1' (from '1 Pills') |
| 232-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '5' (from '5%') · MISSING unit count value '1' (from '1 Pills') |
| 233-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['asacol', 'mesalazine'] · MISSING dosage value '400' (from '400 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 234-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['avapro', 'irbesartan'] · MISSING unit count value '30' (from '30 Pills') |
| 235-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '2' (from '2 mg') · MISSING unit count value '30' (from '30 Pills') |
| 237-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') |
| 238-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['olanzapine', 'zyprexa'] |
| 239-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['cafergot', 'caffeine/ergotamine'] · MISSING dosage value '1' (from '1 mg/100 mg') |
| 24-min | OK | OK | OK | OK | OK |
| 240-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['fildena', 'sildenafil'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '10' (from '10 Pills') |
| 241-min | OK | OK | OK | OK | OK |
| 242-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['lamictal', 'lamotrigine'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 243-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['lamisil', 'terbinafine'] · MISSING dosage value '250' (from '250 mg') |
| 244-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['lamisil', 'terbinafine'] · MISSING unit count value '3' (from '3 Pills') |
| 245-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['levaquin', 'levofloxacin'] · MISSING dosage value '500' (from '500 mg') |
| 246-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['escitalopram', 'lexapro'] · MISSING unit count value '30' (from '30 Pills') |
| 247-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['metoprolol', 'toprol xl'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 248-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '15' (from '15 g') |
| 249-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['minipress', 'prazosin'] · MISSING dosage value '2' (from '2 mg') · MISSING unit count value '30' (from '30 Pills') |
| 25-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['paroxetine', 'paxil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 250-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['domperidone', 'motilium'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 251-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['gabapentin', 'neurontin'] · MISSING dosage value '300' (from '300 mg') · MISSING unit count value '30' (from '30 Pills') |
| 252-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['nitroglycerin'] · MISSING dosage value '0.4' (from '0.4 mg') |
| 253-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '800' (from '800 mg') |
| 254-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['norfloxacin', 'noroxin'] · MISSING dosage value '400' (from '400 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 255-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') |
| 256-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['mirtazapine', 'remeron'] |
| 257-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') |
| 258-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '3' (from '3 mg') · MISSING unit count value '30' (from '30 Pills') |
| 259-min | OK | OK | OK | OK | OK |
| 26-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['fluoxetine', 'prozac'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 260-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '50' (from '50 mg') |
| 261-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['topamax', 'topiramate'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 262-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['torsemide'] · MISSING unit count value '30' (from '30 Pills') |
| 263-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['ketorolac', 'toradol'] · MISSING unit count value '30' (from '30 Pills') |
| 265-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['benadryl', 'diphenhydramine'] · MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 266-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['diphenhydramine', 'sominex'] · MISSING dosage value '50' (from '50 mg') |
| 267-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['diphenhydramine', 'unisom'] · MISSING dosage value '50' (from '50 mg') |
| 268-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '90' (from '90 mcg/puff') |
| 269-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['latanoprost', 'xalatan'] · MISSING dosage value '0.005' (from '0.005%') · MISSING unit count value '1' (from '1 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 27-min | OK | OK | OK | OK | OK |
| 270-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['bisoprolol', 'zebeta'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 271-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['ondansetron', 'zofran'] · MISSING dosage value '8' (from '8 mg') · MISSING unit count value '30' (from '30 Pills') |
| 272-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '5' (from '5 mg') |
| 275-min | OK | OK | OK | OK | OK |
| 277-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '30' (from '30 mg') |
| 278-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '150' (from '150 mg/12.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 279-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['lopressor', 'metoprolol'] · MISSING dosage value '50' (from '50 mg') |
| 28-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['diflucan', 'fluconazole'] · MISSING unit count value '30' (from '30 Pills') |
| 281-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '50' (from '50 mg/12.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 282-min | OK | OK | OK | OK | OK |
| 283-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '50' (from '50 mg') · MISSING unit count value '30' (from '30 Pills') |
| 284-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '25' (from '25 mg') |
| 285-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '60' (from '60 Pills') |
| 286-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 287-min | OK | OK | OK | OK | OK |
| 288-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['aleve', 'naproxen'] · MISSING dosage value '220' (from '220 mg') · MISSING unit count value '30' (from '30 Pills') |
| 29-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['ketoconazole', 'nizoral'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '1' (from '1 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 290-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '20' (from '20 mg') · MISSING unit count value '60' (from '60 Pills') |
| 291-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['avana', 'avanafil'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '4' (from '4 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 293-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['albuterol', 'proventil'] · MISSING unit count value '1' (from '1 Pills') |
| 295-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '150' (from '150 mg') |
| 296-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['dexanil', 'escitalopram'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 297-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '5' (from '5 mg') · MISSING unit count value '60' (from '60 Pills') |
| 298-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['anaridex', 'anastrozole'] · MISSING dosage value '1' (from '1 mg') |
| 299-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['dutas', 'dutasteride'] · MISSING dosage value '0.5' (from '0.5 mg') |
| 3-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['alavert', 'loratadine'] · MISSING dosage value '10' (from '10 mg') |
| 30-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['loxapine', 'loxitane'] · MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 300-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '30' (from '30 Pills') |
| 301-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 302-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') |
| 303-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '3' (from '3 mg') |
| 304-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sonata', 'zaleplon'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 305-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['progesterone', 'utrogestan'] · MISSING dosage value '100' (from '100 mg') |
| 307-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['centrex', 'valacyclovir'] · MISSING unit count value '30' (from '30 Pills') |
| 308-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['bromazepam', 'lexotanil'] · MISSING dosage value '3' (from '3 mg') · MISSING unit count value '30' (from '30 Pills') |
| 309-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['estradiol', 'evorel'] · MISSING dosage value '50' (from '50 mcg/day') |
| 31-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['risperdal', 'risperidone'] · MISSING dosage value '2' (from '2 mg') · MISSING unit count value '30' (from '30 Pills') |
| 310-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['kamagra', 'kamagra soft tabs', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg') |
| 311-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['kamagra gold', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 312-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cialis', 'cialis strips', 'tadalafil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '1' (from '1 Pills') |
| 313-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil citrate', 'viagra', 'viagra strips'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '1' (from '1 Pills') |
| 314-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['avanafil + dapoxetine hcl', 'super avana'] · MISSING dosage value '200' (from '200 mg/60 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 315-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['amantadine', 'symmetrel'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 316-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['beclomethasone dipropionate', 'beconase aq'] · MISSING dosage value '50' (from '50 mcg/spray') · MISSING unit count value '1' (from '1 Pills') |
| 317-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['benzac', 'benzoyl'] · MISSING dosage value '5' (from '5%') |
| 318-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['cefadroxil', 'duricef'] |
| 319-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['chloramphenicol', 'chloromycetin'] · MISSING dosage value '250' (from '250 mg') |
| 320-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['clozapine', 'clozaril'] · MISSING dosage value '100' (from '100 mg') |
| 321-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['cardizem', 'diltiazem'] |
| 322-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['eulexin', 'flutamide'] · MISSING dosage value '250' (from '250 mg') · MISSING unit count value '30' (from '30 Pills') |
| 323-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '400' (from '400 mg') |
| 324-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['hyzyd', 'isoniazid'] · MISSING dosage value '300' (from '300 mg') · MISSING unit count value '30' (from '30 Pills') |
| 325-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['methotrexate', 'trexall'] · MISSING dosage value '2.5' (from '2.5 mg') |
| 326-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['minocin', 'minocycline'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 327-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 328-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '400' (from '400 mg') |
| 329-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['penegra', 'sildenafil'] · MISSING dosage value '50' (from '50 mg') · MISSING unit count value '10' (from '10 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 330-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['fasigyn', 'tinidazole'] · MISSING dosage value '500' (from '500 mg') |
| 331-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') |
| 332-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') |
| 333-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '3' (from '3 mg') |
| 334-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '5' (from '5 mg') · MISSING unit count value '60' (from '60 Pills') |
| 335-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['stilnox', 'stilnox brand', 'zolpidem tartrate'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 336-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['conjugated estrogens', 'premarin'] · MISSING dosage value '0.625' (from '0.625 mg') · MISSING unit count value '30' (from '30 Pills') |
| 337-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['kamagra effervescent', 'sildenafil citrate'] · MISSING dosage value '100' (from '100 mg') |
| 34-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['adalat', 'nifedipine'] |
| 340-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '0.5' (from '0.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 341-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['etizest', 'etizolam'] · MISSING unit count value '30' (from '30 Pills') |
| 344-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['modafinil'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 345-min | OK | OK | OK | OK | OK |
| 346-min | OK | OK | OK | OK | OK |
| 347-min | FAIL | OK | — | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil / tadalafil / vardenafil', 'test pack l-vc'] · MISSING unit count value '1' (from '1 Pills') |
| 348-min | FAIL | OK | — | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil / tadalafil / vardenafil / avanafil', 'test pack l-vl'] · MISSING unit count value '1' (from '1 Pills') |
| 349-min | OK | OK | — | OK | OK |
| 35-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['albendazole', 'albenza'] · MISSING dosage value '200' (from '200 mg') |
| 350-min | OK | OK | OK | OK | OK |
| 351-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '1' (from '1 Pills') |
| 352-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['aleve', 'naproxen sodium'] · MISSING unit count value '30' (from '30 Pills') |
| 353-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['benzocaine + cetylpyridinium chloride', 'cepacol'] · MISSING dosage value '1.4' (from '1.4 mg') |
| 354-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '200' (from '200 mg') |
| 355-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['cortaid', 'hydrocortisone acetate 1%'] |
| 356-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['morphine', 'morphine sulfate'] · MISSING dosage value '30' (from '30 mg') · MISSING unit count value '30' (from '30 Pills') |
| 357-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['adderall', 'amphetamine / dextroamphetamine salts'] |
| 359-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '2' (from '2 mg') · MISSING unit count value '30' (from '30 Pills') |
| 36-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '30' (from '30 Pills') |
| 360-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['restoril', 'temazepam'] · MISSING dosage value '15' (from '15 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 362-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['hydrocodone', 'hydrocodone bitartrate'] · MISSING dosage value '10' (from '10 mg') |
| 363-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['oxycodone hcl 30mg', 'roxicodone', 'roxicodone m30'] · MISSING dosage value '30' (from '30 mg') · MISSING unit count value '30' (from '30 Pills') |
| 364-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') |
| 365-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['tapentadol', 'tapentadol hcl'] · MISSING dosage value '50' (from '50 mg') |
| 366-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['acivir cream', 'acivir cream by cipla 5%', 'acyclovir 5%'] · MISSING unit count value '1' (from '1 Pills') |
| 367-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '400' (from '400 mg') · MISSING unit count value '1' (from '1 Pills') |
| 369-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '4' (from '4 mg') |
| 37-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '1' (from '1 Pills') |
| 370-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['albuterol', 'ventolin', 'ventolin generic'] · MISSING dosage value '100' (from '100 mcg') · MISSING unit count value '1' (from '1 Pills') |
| 371-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['imipramine', 'tofranil', 'tofranil generic'] · MISSING dosage value '25' (from '25 mg') |
| 372-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '37.5' (from '37.5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 373-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['azithromycin', 'azithromycin generic'] · MISSING dosage value '250' (from '250 mg') |
| 374-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cephalexin', 'cephalexin generic'] · MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 375-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '200' (from '200 mg') |
| 376-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['lisinopril'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 377-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '80' (from '80 mg') |
| 378-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['amiodarone', 'cordarone', 'cordarone generic'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 379-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '1' (from '1 Bottle') |
| 38-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['prednisone'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 380-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 381-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['famotidine', 'pepcid', 'pepcid generic'] |
| 382-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['allopurinol', 'allopurinol generic'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '30' (from '30 Pills') |
| 383-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['chloroquine', 'chloroquine generic'] · MISSING dosage value '250' (from '250 mg') |
| 384-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['ibuprofen', 'ibuprofen generic'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 385-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '0.05' (from '0.05%') · MISSING unit count value '1' (from '1 Pills') |
| 386-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '0.1' (from '0.1%') · MISSING unit count value '1' (from '1 Pills') |
| 387-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['addyi', 'flibanserin'] · MISSING dosage value '100' (from '100 mg') |
| 388-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['female cialis', 'femalefil'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '10' (from '10 Pills') |
| 390-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['diclofenac', 'volini gel'] · MISSING dosage value '1' (from '1%') · MISSING unit count value '1' (from '1 Pills') |
| 391-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['analgin', 'analgin generic'] · MISSING dosage value '500' (from '500 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 392-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['aspirin', 'aspirin generic'] |
| 393-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '250' (from '250 mcg/100 mcg') · MISSING unit count value '1' (from '1 Inhaler') |
| 395-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['endogest', 'progesterone'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 396-min | OK | OK | OK | OK | OK |
| 398-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['testorapid', 'testosterone propionate'] · MISSING dosage value '100' (from '100 mg/ml') · MISSING unit count value '10' (from '10 Pills') |
| 399-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['meldonium'] |
| 4-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '4' (from '4 mg') · MISSING unit count value '30' (from '30 Pills') |
| 40-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['amlodipine', 'norvasc'] · MISSING dosage value '5' (from '5 mg') · MISSING unit count value '30' (from '30 Pills') |
| 400-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['zinc acetate + doxycycline + ivermectin', 'ziverdo', 'ziverdo kit'] · MISSING unit count value '1' (from '1 Pills') |
| 401-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['oxycodone'] |
| 402-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['ozempic', 'semaglutide'] · MISSING dosage value '2' (from '2 mg') · MISSING unit count value '1' (from '1 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 403-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['rybelsus', 'semaglutide'] · MISSING dosage value '7' (from '7 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 404-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 405-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '15' (from '15 mg') |
| 406-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '15' (from '15 mg') |
| 407-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '1' (from '1 Pills') |
| 408-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['semaglutide', 'wegovy'] · MISSING dosage value '2.4' (from '2.4 mg') |
| 409-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['nandrolone decanoate'] |
| 41-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['esomeprazole', 'nexium'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 410-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sustanon', 'testosterone blend'] · MISSING dosage value '250' (from '250 mg/ml') · MISSING unit count value '1' (from '1 Pills') |
| 411-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['testosterone cypionate'] · MISSING unit count value '1' (from '1 Pills') |
| 412-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['testosterone enanthate'] · MISSING dosage value '250' (from '250 mg/ml') · MISSING unit count value '1' (from '1 Pills') |
| 413-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['boldenone', 'boldenone undecylenate'] · MISSING dosage value '200' (from '200 mg/ml') · MISSING unit count value '10' (from '10 Pills') |
| 414-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg/ml') · MISSING unit count value '10' (from '10 Vials') |
| 415-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '10' (from '10 Vials') |
| 416-min | OK | OK | OK | OK | OK |
| 417-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['drostanolone propionate', 'masteron'] · MISSING dosage value '100' (from '100 mg/ml') · MISSING unit count value '1' (from '1 Pills') |
| 418-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['methandienone'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '100' (from '100 Pills') |
| 419-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '100' (from '100 Pills') |
| 42-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '200' (from '200 mcg') · MISSING unit count value '30' (from '30 Pills') |
| 420-min | OK | OK | OK | OK | OK |
| 421-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['stanozolol'] |
| 422-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') |
| 423-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['halcion', 'triazolam'] · MISSING dosage value '0.25' (from '0.25 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 424-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['tirzepatide', 'zepbound'] · MISSING dosage value '2.5' (from '2.5 mg') · MISSING unit count value '1' (from '1 Pills') |
| 425-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['mounjaro', 'tirzepatide'] · MISSING dosage value '5' (from '5 mg') |
| 426-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cialis oral jelly', 'tadalafil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '7' (from '7 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 427-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['kamagra chewable', 'soft'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') |
| 428-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '1' (from '1 Pills') |
| 429-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['levitra', 'levitra oral jelly', 'vardenafil hcl'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '4' (from '4 Pills') |
| 43-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['lansoprazole', 'prevacid'] · MISSING dosage value '15' (from '15 mg') · MISSING unit count value '30' (from '30 Pills') |
| 430-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['pantoprazole', 'protonix'] · MISSING dosage value '40' (from '40 mg') |
| 431-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '30' (from '30 Pills') |
| 432-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '50' (from '50 mg') |
| 433-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['bimatoprost', 'latisse'] · MISSING dosage value '3' (from '3 ml') · MISSING unit count value '1' (from '1 Bottle') |
| 434-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') |
| 44-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '20' (from '20 mg') · MISSING unit count value '30' (from '30 Pills') |
| 45-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '150' (from '150 mg') · MISSING unit count value '30' (from '30 Pills') |
| 46-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['finasteride', 'propecia'] · MISSING unit count value '30' (from '30 Pills') |
| 47-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['coumadin', 'warfarin'] · MISSING dosage value '5' (from '5 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 48-min | OK | OK | OK | OK | OK |
| 49-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['clopidogrel', 'plavix'] · MISSING dosage value '75' (from '75 mg') |
| 5-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '4' (from '4 mg') · MISSING unit count value '30' (from '30 Pills') |
| 50-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '40' (from '40 mg') |
| 51-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sofosbuvir'] · MISSING dosage value '400' (from '400 mg') · MISSING unit count value '28' (from '28 Pills') |
| 52-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '400' (from '400 mg') · MISSING unit count value '28' (from '28 Pills') |
| 58-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '5' (from '5 mg') |
| 59-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '20' (from '20 mg') |
| 6-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '4' (from '4 mg') |
| 60-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cialis professional', 'tadalafil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '10' (from '10 Pills') |
| 61-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['cialis soft tabs', 'tadalafil'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '10' (from '10 Pills') |
| 62-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '10' (from '10 Pills') |
| 63-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['dapoxetine', 'priligy'] · MISSING dosage value '30' (from '30 mg') · MISSING unit count value '10' (from '10 Pills') |
| 64-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['kamagra', 'sildenafil'] · MISSING dosage value '100' (from '100 mg') |
| 65-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['kamagra oral jelly', 'sildenafil citrate'] · MISSING unit count value '7' (from '7 Pills') |
| 66-min | FAIL | OK | OK | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['levitra', 'vardenafil'] · MISSING unit count value '4' (from '4 Pills') |
| 67-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['levitra brand', 'vardenafil hcl'] · MISSING dosage value '20' (from '20 mg') · MISSING unit count value '4' (from '4 Pills') |
| 70-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil citrate + dapoxetine hcl', 'super kamagra'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '4' (from '4 Pills') |
| 71-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil citrate + dapoxetine hcl', 'super p force'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '4' (from '4 Pills') |
| 72-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '10' (from '10 Pills') |
| 73-min | OK | OK | OK | OK | OK |
| 74-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil', 'viagra'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '1' (from '1 Pills') |
| 75-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil citrate', 'viagra gold'] · MISSING dosage value '100' (from '100 mg') · MISSING unit count value '10' (from '10 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 76-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') |
| 77-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') |
| 78-min | OK | OK | OK | OK | OK |
| 79-min | OK | OK | OK | OK | OK |
| 8-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 80-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['sildenafil', 'viprogra'] · MISSING dosage value '100' (from '100 mg') |
| 81-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['eldepryl', 'selegiline'] · MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 82-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['bromocriptine mesylate', 'parlodel'] · MISSING dosage value '2.5' (from '2.5 mg') |
| 83-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['baclofen'] · MISSING dosage value '20' (from '20 mg') |
| 85-min | OK | OK | OK | OK | OK |
| 86-min | OK | OK | OK | FAIL | **HARD_FAIL** — MISSING unit count value '10' (from '10 Pills') |
| 87-min | FAIL | OK | OK | OK | **SOFT_FAIL** — MISSING brand/ingredient from ['baclofen', 'lioresal'] |
| 88-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['methocarbamol', 'robaxin'] · MISSING dosage value '500' (from '500 mg') · MISSING unit count value '30' (from '30 Pills') |
| 89-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['boswellia serrata extract', 'shallaki'] · MISSING dosage value '500' (from '500 mg') |
| 9-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '10' (from '10 mg') · MISSING unit count value '30' (from '30 Pills') |
| 90-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '100' (from '100 mg') |
| 91-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '250' (from '250 mg') |
| 92-min | OK | OK | FAIL | OK | **HARD_FAIL** — MISSING dosage value '20' (from '20 mg') |
| 93-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['carbamazepine', 'tegretol'] · MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 94-min | OK | OK | FAIL | FAIL | **HARD_FAIL** — MISSING dosage value '200' (from '200 mg') · MISSING unit count value '30' (from '30 Pills') |
| 95-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['diclofenac', 'voltaren'] · MISSING dosage value '25' (from '25 mg') · EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical |
| 96-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['diclofenac sodium', 'voveran'] · MISSING dosage value '25' (from '25 mg') · MISSING unit count value '30' (from '30 Pills') |
| 97-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['diclofenac sodium', 'voveran sr'] · MISSING dosage value '100' (from '100 mg') |
| 98-min | FAIL | OK | FAIL | FAIL | **HARD_FAIL** — MISSING brand/ingredient from ['tizanidine', 'zanaflex'] · MISSING dosage value '4' (from '4 mg') · MISSING unit count value '30' (from '30 Pills') |
| 99-min | FAIL | OK | FAIL | OK | **HARD_FAIL** — MISSING brand/ingredient from ['acetaminophen'] · MISSING dosage value '500' (from '500 mg') |

## Flagged SKUs (Manual Review Recommended)

### 1-min (SOFT_FAIL)
- MISSING brand/ingredient from ['atomoxetine']

### 100-min (SOFT_FAIL)
- MISSING brand/ingredient from ['arcoxia', 'etoricoxib']

### 101-min (HARD_FAIL)
- MISSING brand/ingredient from ['celebrex', 'celecoxib']
- MISSING dosage value '100' (from '100 mg')

### 102-min (HARD_FAIL)
- MISSING brand/ingredient from ['isordil', 'isosorbide dinitrate']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 103-min (HARD_FAIL)
- MISSING brand/ingredient from ['maxalt', 'rizatriptan']
- MISSING dosage value '5' (from '5 mg')
- MISSING unit count value '10' (from '10 Pills')

### 104-min (HARD_FAIL)
- MISSING brand/ingredient from ['meloxicam', 'mobic']
- MISSING unit count value '30' (from '30 Pills')

### 106-min (HARD_FAIL)
- MISSING dosage value '500' (from '500 mg')
- MISSING unit count value '30' (from '30 Pills')

### 107-min (SOFT_FAIL)
- MISSING brand/ingredient from ['tramadol', 'tramadol hcl']

### 108-min (HARD_FAIL)
- MISSING brand/ingredient from ['acetaminophen', 'tylenol']
- MISSING dosage value '500' (from '500 mg')

### 109-min (HARD_FAIL)
- MISSING brand/ingredient from ['tramadol', 'ultram']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')

### 11-min (HARD_FAIL)
- MISSING brand/ingredient from ['amoxicillin', 'amoxil']
- MISSING dosage value '250' (from '250 mg')
- MISSING unit count value '30' (from '30 Pills')

### 110-min (HARD_FAIL)
- MISSING brand/ingredient from ['accutane', 'isotretinoin']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 111-min (SOFT_FAIL)
- MISSING brand/ingredient from ['retin-a cream', 'retin-a cream 0.025%', 'tretinoin']

### 112-min (HARD_FAIL)
- MISSING brand/ingredient from ['champix', 'varenicline tartrate']
- MISSING dosage value '1' (from '1 mg')

### 113-min (HARD_FAIL)
- MISSING brand/ingredient from ['bupropion', 'zyban']
- MISSING dosage value '150' (from '150 mg')

### 114-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mcg')

### 115-min (HARD_FAIL)
- MISSING dosage value '60' (from '60 mg')
- MISSING unit count value '30' (from '30 Pills')

### 116-min (SOFT_FAIL)
- MISSING brand/ingredient from ['lida daidaihua', 'sibutramine hcl']

### 117-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')

### 118-min (HARD_FAIL)
- MISSING dosage value '120' (from '120 mg')
- MISSING unit count value '30' (from '30 Pills')

### 119-min (HARD_FAIL)
- MISSING dosage value '1' (from '1 mg')

### 12-min (HARD_FAIL)
- MISSING dosage value '250' (from '250 mg')
- MISSING unit count value '30' (from '30 Pills')

### 120-min (HARD_FAIL)
- MISSING brand/ingredient from ['evista', 'raloxifene']
- MISSING unit count value '30' (from '30 Pills')

### 121-min (HARD_FAIL)
- MISSING brand/ingredient from ['alendronic acid', 'fosamax']
- MISSING dosage value '70' (from '70 mg')
- MISSING unit count value '30' (from '30 Pills')

### 122-min (SOFT_FAIL)
- MISSING brand/ingredient from ['allylestrenol', 'gestanin']

### 124-min (HARD_FAIL)
- MISSING unit count value '30' (from '30 Implants')

### 125-min (HARD_FAIL)
- MISSING dosage value '250' (from '250 mg')
- MISSING unit count value '30' (from '30 Pills')

### 126-min (HARD_FAIL)
- MISSING brand/ingredient from ['medroxyprogesterone', 'provera']
- MISSING unit count value '30' (from '30 Pills')

### 127-min (HARD_FAIL)
- MISSING unit count value '1' (from '1 Pills')

### 128-min (HARD_FAIL)
- MISSING brand/ingredient from ['aygestin', 'norethindrone acetate']
- MISSING dosage value '5' (from '5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 129-min (HARD_FAIL)
- MISSING brand/ingredient from ['clomid', 'clomiphene']
- MISSING dosage value '50' (from '50 mg')

### 13-min (HARD_FAIL)
- MISSING dosage value '500' (from '500 mg')

### 130-min (HARD_FAIL)
- MISSING brand/ingredient from ['danazol', 'danocrine']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')

### 131-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '10' (from '10 Pills')

### 133-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 134-min (HARD_FAIL)
- MISSING brand/ingredient from ['atarax', 'hydroxyzine']
- MISSING dosage value '25' (from '25 mg')
- MISSING unit count value '30' (from '30 Pills')

### 135-min (HARD_FAIL)
- MISSING brand/ingredient from ['ativan', 'lorazepam']
- MISSING dosage value '1' (from '1 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 136-min (HARD_FAIL)
- MISSING brand/ingredient from ['buspar', 'buspirone']
- MISSING unit count value '30' (from '30 Pills')

### 138-min (HARD_FAIL)
- MISSING dosage value '30' (from '30mg/500mg')

### 14-min (SOFT_FAIL)
- MISSING brand/ingredient from ['bactrim', 'trimethoprim']

### 141-min (HARD_FAIL)
- MISSING brand/ingredient from ['deca durabolin', 'testosterone']
- MISSING dosage value '50' (from '50 mg/mL')

### 143-min (HARD_FAIL)
- MISSING dosage value '1.62' (from '1.62%')

### 144-min (HARD_FAIL)
- MISSING unit count value '10' (from '10 Pills')

### 145-min (HARD_FAIL)
- MISSING unit count value '10' (from '10 Pills')

### 146-min (HARD_FAIL)
- MISSING brand/ingredient from ['hucog-10000 hp', 'human chorionic gonadotropin']
- MISSING dosage value '10000' (from '10000 IU')
- MISSING unit count value '10' (from '10 Pills')

### 147-min (HARD_FAIL)
- MISSING brand/ingredient from ['sustaviron-250', 'testosterone blend']
- MISSING dosage value '250' (from '250 mg/mL')
- MISSING unit count value '10' (from '10 Pills')

### 148-min (HARD_FAIL)
- MISSING brand/ingredient from ['drostanolone propionate', 'masteron']
- MISSING dosage value '100' (from '100 mg/mL')
- MISSING unit count value '1' (from '1 Pills')

### 149-min (HARD_FAIL)
- MISSING brand/ingredient from ['modafinil', 'modalert']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')

### 15-min (HARD_FAIL)
- MISSING brand/ingredient from ['cipro', 'ciprofloxacin']
- MISSING dosage value '500' (from '500 mg')
- MISSING unit count value '30' (from '30 Pills')

### 150-min (HARD_FAIL)
- MISSING dosage value '150' (from '150 mg')
- MISSING unit count value '30' (from '30 Pills')

### 151-min (HARD_FAIL)
- MISSING brand/ingredient from ['modafinil', 'provigil']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')

### 152-min (HARD_FAIL)
- MISSING brand/ingredient from ['armodafinil', 'artvigil']
- MISSING dosage value '150' (from '150 mg')

### 155-min (SOFT_FAIL)
- MISSING brand/ingredient from ['imovane', 'zopiclone']

### 156-min (HARD_FAIL)
- MISSING dosage value '0.5' (from '0.5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 157-min (HARD_FAIL)
- MISSING brand/ingredient from ['diazepam', 'valium']
- MISSING dosage value '5' (from '5 mg')

### 158-min (HARD_FAIL)
- MISSING brand/ingredient from ['clonazepam', 'klonopin']
- MISSING dosage value '1' (from '1 mg')

### 16-min (HARD_FAIL)
- MISSING brand/ingredient from ['doxycycline', 'doxycycline hyclate']
- MISSING dosage value '100' (from '100 mg')

### 160-min (HARD_FAIL)
- MISSING brand/ingredient from ['avanafil', 'stendra']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '10' (from '10 Pills')

### 161-min (HARD_FAIL)
- MISSING brand/ingredient from ['apcalis oral jelly', 'tadalafil']
- MISSING unit count value '7' (from '7 Pills')

### 162-min (HARD_FAIL)
- MISSING brand/ingredient from ['tadalafil + dapoxetine hcl', 'tadapox']
- MISSING unit count value '10' (from '10 Pills')

### 164-min (HARD_FAIL)
- MISSING brand/ingredient from ['anastrozole', 'arimidex']
- MISSING dosage value '1' (from '1 mg')
- MISSING unit count value '30' (from '30 Pills')

### 165-min (HARD_FAIL)
- MISSING brand/ingredient from ['claritin', 'loratadine']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '60' (from '60 Pills')

### 166-min (HARD_FAIL)
- MISSING brand/ingredient from ['clarinex', 'desloratadine']
- MISSING dosage value '5' (from '5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 17-min (HARD_FAIL)
- MISSING brand/ingredient from ['flagyl', 'metronidazole']
- MISSING dosage value '500' (from '500 mg')

### 170-min (HARD_FAIL)
- MISSING brand/ingredient from ['fliban', 'flibanserin']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '10' (from '10 Pills')

### 171-min (HARD_FAIL)
- MISSING brand/ingredient from ['hydrochlorothiazide', 'microzide']
- MISSING dosage value '25' (from '25 mg')

### 172-min (HARD_FAIL)
- MISSING brand/ingredient from ['quetiapine', 'qutan']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')

### 173-min (HARD_FAIL)
- MISSING dosage value '40' (from '40 mg')
- MISSING unit count value '30' (from '30 Pills')

### 175-min (HARD_FAIL)
- MISSING brand/ingredient from ['nolvadex', 'tamoxifen']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 176-min (HARD_FAIL)
- MISSING brand/ingredient from ['sertraline', 'zoloft']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')

### 177-min (HARD_FAIL)
- MISSING dosage value '250' (from '250 mg')

### 178-min (HARD_FAIL)
- MISSING brand/ingredient from ['aciphex', 'rabeprazole']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '20' (from '20 Pills')

### 179-min (SOFT_FAIL)
- MISSING brand/ingredient from ['actos', 'pioglitazone']

### 18-min (HARD_FAIL)
- MISSING brand/ingredient from ['efavirenz', 'sustiva']
- MISSING dosage value '600' (from '600 mg')

### 180-min (HARD_FAIL)
- MISSING dosage value '25' (from '25 mg')

### 181-min (HARD_FAIL)
- MISSING brand/ingredient from ['alesse', 'levonorgestrel + ethinylestradiol']
- MISSING dosage value '20' (from '20 mcg')
- MISSING unit count value '30' (from '30 Pills')

### 183-min (HARD_FAIL)
- MISSING dosage value '5' (from '5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 184-min (HARD_FAIL)
- MISSING brand/ingredient from ['amaryl', 'glimepiride']
- MISSING dosage value '2' (from '2 mg')

### 186-min (HARD_FAIL)
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')

### 187-min (HARD_FAIL)
- MISSING brand/ingredient from ['antabuse', 'disulfiram']
- MISSING dosage value '250' (from '250 mg')
- MISSING unit count value '30' (from '30 Pills')

### 188-min (SOFT_FAIL)
- MISSING brand/ingredient from ['aralen', 'chloroquine']

### 189-min (HARD_FAIL)
- MISSING brand/ingredient from ['aricept', 'donepezil']
- MISSING dosage value '10' (from '10 mg')

### 19-min (HARD_FAIL)
- MISSING brand/ingredient from ['azithromycin', 'zithromax']
- MISSING dosage value '250' (from '250 mg')
- MISSING unit count value '30' (from '30 Pills')

### 192-min (HARD_FAIL)
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 194-min (HARD_FAIL)
- MISSING brand/ingredient from ['celexa', 'citalopram']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 195-min (HARD_FAIL)
- MISSING brand/ingredient from ['cleocin', 'clindamycin']
- MISSING dosage value '150' (from '150 mg')

### 196-min (SOFT_FAIL)
- MISSING brand/ingredient from ['cleocin', 'clindamycin']

### 197-min (HARD_FAIL)
- MISSING brand/ingredient from ['catapres', 'clonidine']
- MISSING dosage value '0.1' (from '0.1 mg')
- MISSING unit count value '30' (from '30 Pills')

### 198-min (HARD_FAIL)
- MISSING brand/ingredient from ['colchicine']
- MISSING unit count value '30' (from '30 Pills')

### 199-min (HARD_FAIL)
- MISSING brand/ingredient from ['cozaar', 'losartan']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')

### 2-min (HARD_FAIL)
- MISSING brand/ingredient from ['atomoxetine', 'strattera']
- MISSING dosage value '40' (from '40 mg')

### 20-min (HARD_FAIL)
- MISSING brand/ingredient from ['abilify', 'aripiprazole']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 200-min (HARD_FAIL)
- MISSING brand/ingredient from ['crestor', 'rosuvastatin']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 201-min (HARD_FAIL)
- MISSING brand/ingredient from ['desyrel', 'trazodone']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')

### 202-min (SOFT_FAIL)
- MISSING brand/ingredient from ['detrol', 'tolterodine']

### 203-min (HARD_FAIL)
- MISSING brand/ingredient from ['acetazolamide', 'diamox']
- MISSING dosage value '250' (from '250 mg')
- MISSING unit count value '30' (from '30 Pills')

### 204-min (HARD_FAIL)
- MISSING unit count value '30' (from '30 Pills')

### 205-min (SOFT_FAIL)
- MISSING brand/ingredient from ['ditropan', 'oxybutynin']

### 206-min (HARD_FAIL)
- MISSING brand/ingredient from ['cabergoline', 'dostinex']
- MISSING dosage value '0.5' (from '0.5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 207-min (HARD_FAIL)
- MISSING brand/ingredient from ['dimenhydrinate', 'dramamine']
- MISSING dosage value '50' (from '50 mg')

### 208-min (HARD_FAIL)
- MISSING brand/ingredient from ['bisacodyl', 'dulcolax']
- MISSING dosage value '5' (from '5 mg')

### 209-min (HARD_FAIL)
- MISSING brand/ingredient from ['erythromycin']
- MISSING dosage value '250' (from '250 mg')

### 210-min (HARD_FAIL)
- MISSING dosage value '0.4' (from '0.4 mg')

### 211-min (HARD_FAIL)
- MISSING brand/ingredient from ['glucophage', 'metformin']
- MISSING dosage value '500' (from '500 mg')
- MISSING unit count value '30' (from '30 Pills')

### 213-min (HARD_FAIL)
- MISSING brand/ingredient from ['malegra dxt', 'sildenafil citrate']
- MISSING dosage value '100' (from '100 mg/30 mg')

### 214-min (HARD_FAIL)
- MISSING brand/ingredient from ['malegra dxt plus', 'sildenafil citrate']
- MISSING dosage value '100' (from '100 mg/60 mg')

### 215-min (HARD_FAIL)
- MISSING brand/ingredient from ['malegra fxt', 'sildenafil citrate']
- MISSING dosage value '100' (from '100 mg/20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 216-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg/40 mg')
- MISSING unit count value '30' (from '30 Pills')

### 217-min (HARD_FAIL)
- MISSING brand/ingredient from ['medrol', 'methylprednisolone']
- MISSING unit count value '30' (from '30 Pills')

### 218-min (HARD_FAIL)
- MISSING brand/ingredient from ['silagra', 'sildenafil']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '10' (from '10 Pills')

### 22-min (HARD_FAIL)
- MISSING brand/ingredient from ['effexor', 'venlafaxine']
- MISSING dosage value '75' (from '75 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 220-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil', 'zenegra']
- MISSING dosage value '100' (from '100 mg')

### 222-min (HARD_FAIL)
- MISSING dosage value '25' (from '25 mg')
- MISSING unit count value '30' (from '30 Pills')

### 223-min (HARD_FAIL)
- MISSING brand/ingredient from ['levitra soft tabs', 'vardenafil hcl']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '10' (from '10 Pills')

### 224-min (HARD_FAIL)
- MISSING brand/ingredient from ['caverta', 'sildenafil']
- MISSING dosage value '100' (from '100 mg')

### 225-min (HARD_FAIL)
- MISSING brand/ingredient from ['cabergoline', 'cabgolin']
- MISSING dosage value '0.5' (from '0.5 mg')
- MISSING unit count value '10' (from '10 Pills')

### 226-min (HARD_FAIL)
- MISSING brand/ingredient from ['aciclovir', 'zovirax']
- MISSING dosage value '400' (from '400 mg')
- MISSING unit count value '1' (from '1 Pills')

### 227-min (HARD_FAIL)
- MISSING brand/ingredient from ['deltasone', 'prednisolone']
- MISSING dosage value '20' (from '20 mg')

### 228-min (HARD_FAIL)
- MISSING brand/ingredient from ['ketoconazole', 'nizoral']
- MISSING dosage value '2' (from '2%')
- MISSING unit count value '1' (from '1 Pills')

### 229-min (HARD_FAIL)
- MISSING dosage value '0.01' (from '0.01%')
- MISSING unit count value '1' (from '1 Bottle')

### 230-min (HARD_FAIL)
- MISSING dosage value '15' (from '15 mg')
- MISSING unit count value '30' (from '30 Pills')

### 231-min (HARD_FAIL)
- MISSING brand/ingredient from ['acticin', 'permethrin']
- MISSING unit count value '1' (from '1 Pills')

### 232-min (HARD_FAIL)
- MISSING dosage value '5' (from '5%')
- MISSING unit count value '1' (from '1 Pills')

### 233-min (HARD_FAIL)
- MISSING brand/ingredient from ['asacol', 'mesalazine']
- MISSING dosage value '400' (from '400 mg')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 234-min (HARD_FAIL)
- MISSING brand/ingredient from ['avapro', 'irbesartan']
- MISSING unit count value '30' (from '30 Pills')

### 235-min (HARD_FAIL)
- MISSING dosage value '2' (from '2 mg')
- MISSING unit count value '30' (from '30 Pills')

### 237-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')

### 238-min (SOFT_FAIL)
- MISSING brand/ingredient from ['olanzapine', 'zyprexa']

### 239-min (HARD_FAIL)
- MISSING brand/ingredient from ['cafergot', 'caffeine/ergotamine']
- MISSING dosage value '1' (from '1 mg/100 mg')

### 240-min (HARD_FAIL)
- MISSING brand/ingredient from ['fildena', 'sildenafil']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '10' (from '10 Pills')

### 242-min (HARD_FAIL)
- MISSING brand/ingredient from ['lamictal', 'lamotrigine']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '30' (from '30 Pills')

### 243-min (HARD_FAIL)
- MISSING brand/ingredient from ['lamisil', 'terbinafine']
- MISSING dosage value '250' (from '250 mg')

### 244-min (HARD_FAIL)
- MISSING brand/ingredient from ['lamisil', 'terbinafine']
- MISSING unit count value '3' (from '3 Pills')

### 245-min (HARD_FAIL)
- MISSING brand/ingredient from ['levaquin', 'levofloxacin']
- MISSING dosage value '500' (from '500 mg')

### 246-min (HARD_FAIL)
- MISSING brand/ingredient from ['escitalopram', 'lexapro']
- MISSING unit count value '30' (from '30 Pills')

### 247-min (HARD_FAIL)
- MISSING brand/ingredient from ['metoprolol', 'toprol xl']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')

### 248-min (HARD_FAIL)
- MISSING dosage value '15' (from '15 g')

### 249-min (HARD_FAIL)
- MISSING brand/ingredient from ['minipress', 'prazosin']
- MISSING dosage value '2' (from '2 mg')
- MISSING unit count value '30' (from '30 Pills')

### 25-min (HARD_FAIL)
- MISSING brand/ingredient from ['paroxetine', 'paxil']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 250-min (HARD_FAIL)
- MISSING brand/ingredient from ['domperidone', 'motilium']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 251-min (HARD_FAIL)
- MISSING brand/ingredient from ['gabapentin', 'neurontin']
- MISSING dosage value '300' (from '300 mg')
- MISSING unit count value '30' (from '30 Pills')

### 252-min (HARD_FAIL)
- MISSING brand/ingredient from ['nitroglycerin']
- MISSING dosage value '0.4' (from '0.4 mg')

### 253-min (HARD_FAIL)
- MISSING dosage value '800' (from '800 mg')

### 254-min (HARD_FAIL)
- MISSING brand/ingredient from ['norfloxacin', 'noroxin']
- MISSING dosage value '400' (from '400 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 255-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')

### 256-min (SOFT_FAIL)
- MISSING brand/ingredient from ['mirtazapine', 'remeron']

### 257-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')

### 258-min (HARD_FAIL)
- MISSING dosage value '3' (from '3 mg')
- MISSING unit count value '30' (from '30 Pills')

### 26-min (HARD_FAIL)
- MISSING brand/ingredient from ['fluoxetine', 'prozac']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 260-min (HARD_FAIL)
- MISSING dosage value '50' (from '50 mg')

### 261-min (HARD_FAIL)
- MISSING brand/ingredient from ['topamax', 'topiramate']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 262-min (HARD_FAIL)
- MISSING brand/ingredient from ['torsemide']
- MISSING unit count value '30' (from '30 Pills')

### 263-min (HARD_FAIL)
- MISSING brand/ingredient from ['ketorolac', 'toradol']
- MISSING unit count value '30' (from '30 Pills')

### 265-min (HARD_FAIL)
- MISSING brand/ingredient from ['benadryl', 'diphenhydramine']
- MISSING dosage value '25' (from '25 mg')
- MISSING unit count value '30' (from '30 Pills')

### 266-min (HARD_FAIL)
- MISSING brand/ingredient from ['diphenhydramine', 'sominex']
- MISSING dosage value '50' (from '50 mg')

### 267-min (HARD_FAIL)
- MISSING brand/ingredient from ['diphenhydramine', 'unisom']
- MISSING dosage value '50' (from '50 mg')

### 268-min (HARD_FAIL)
- MISSING dosage value '90' (from '90 mcg/puff')

### 269-min (HARD_FAIL)
- MISSING brand/ingredient from ['latanoprost', 'xalatan']
- MISSING dosage value '0.005' (from '0.005%')
- MISSING unit count value '1' (from '1 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 270-min (HARD_FAIL)
- MISSING brand/ingredient from ['bisoprolol', 'zebeta']
- MISSING dosage value '5' (from '5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 271-min (HARD_FAIL)
- MISSING brand/ingredient from ['ondansetron', 'zofran']
- MISSING dosage value '8' (from '8 mg')
- MISSING unit count value '30' (from '30 Pills')

### 272-min (HARD_FAIL)
- MISSING dosage value '5' (from '5 mg')

### 277-min (HARD_FAIL)
- MISSING dosage value '30' (from '30 mg')

### 278-min (HARD_FAIL)
- MISSING dosage value '150' (from '150 mg/12.5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 279-min (HARD_FAIL)
- MISSING brand/ingredient from ['lopressor', 'metoprolol']
- MISSING dosage value '50' (from '50 mg')

### 28-min (HARD_FAIL)
- MISSING brand/ingredient from ['diflucan', 'fluconazole']
- MISSING unit count value '30' (from '30 Pills')

### 281-min (HARD_FAIL)
- MISSING dosage value '50' (from '50 mg/12.5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 283-min (HARD_FAIL)
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '30' (from '30 Pills')

### 284-min (HARD_FAIL)
- MISSING dosage value '25' (from '25 mg')

### 285-min (HARD_FAIL)
- MISSING unit count value '60' (from '60 Pills')

### 286-min (HARD_FAIL)
- MISSING dosage value '500' (from '500 mg')
- MISSING unit count value '30' (from '30 Pills')

### 288-min (HARD_FAIL)
- MISSING brand/ingredient from ['aleve', 'naproxen']
- MISSING dosage value '220' (from '220 mg')
- MISSING unit count value '30' (from '30 Pills')

### 29-min (HARD_FAIL)
- MISSING brand/ingredient from ['ketoconazole', 'nizoral']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '1' (from '1 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 290-min (HARD_FAIL)
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '60' (from '60 Pills')

### 291-min (HARD_FAIL)
- MISSING brand/ingredient from ['avana', 'avanafil']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '4' (from '4 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 293-min (HARD_FAIL)
- MISSING brand/ingredient from ['albuterol', 'proventil']
- MISSING unit count value '1' (from '1 Pills')

### 295-min (HARD_FAIL)
- MISSING dosage value '150' (from '150 mg')

### 296-min (HARD_FAIL)
- MISSING brand/ingredient from ['dexanil', 'escitalopram']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 297-min (HARD_FAIL)
- MISSING dosage value '5' (from '5 mg')
- MISSING unit count value '60' (from '60 Pills')

### 298-min (HARD_FAIL)
- MISSING brand/ingredient from ['anaridex', 'anastrozole']
- MISSING dosage value '1' (from '1 mg')

### 299-min (HARD_FAIL)
- MISSING brand/ingredient from ['dutas', 'dutasteride']
- MISSING dosage value '0.5' (from '0.5 mg')

### 3-min (HARD_FAIL)
- MISSING brand/ingredient from ['alavert', 'loratadine']
- MISSING dosage value '10' (from '10 mg')

### 30-min (HARD_FAIL)
- MISSING brand/ingredient from ['loxapine', 'loxitane']
- MISSING dosage value '25' (from '25 mg')
- MISSING unit count value '30' (from '30 Pills')

### 300-min (HARD_FAIL)
- MISSING unit count value '30' (from '30 Pills')

### 301-min (HARD_FAIL)
- MISSING dosage value '250' (from '250 mg')
- MISSING unit count value '30' (from '30 Pills')

### 302-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')

### 303-min (HARD_FAIL)
- MISSING dosage value '3' (from '3 mg')

### 304-min (HARD_FAIL)
- MISSING brand/ingredient from ['sonata', 'zaleplon']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 305-min (HARD_FAIL)
- MISSING brand/ingredient from ['progesterone', 'utrogestan']
- MISSING dosage value '100' (from '100 mg')

### 307-min (HARD_FAIL)
- MISSING brand/ingredient from ['centrex', 'valacyclovir']
- MISSING unit count value '30' (from '30 Pills')

### 308-min (HARD_FAIL)
- MISSING brand/ingredient from ['bromazepam', 'lexotanil']
- MISSING dosage value '3' (from '3 mg')
- MISSING unit count value '30' (from '30 Pills')

### 309-min (HARD_FAIL)
- MISSING brand/ingredient from ['estradiol', 'evorel']
- MISSING dosage value '50' (from '50 mcg/day')

### 31-min (HARD_FAIL)
- MISSING brand/ingredient from ['risperdal', 'risperidone']
- MISSING dosage value '2' (from '2 mg')
- MISSING unit count value '30' (from '30 Pills')

### 310-min (HARD_FAIL)
- MISSING brand/ingredient from ['kamagra', 'kamagra soft tabs', 'sildenafil citrate']
- MISSING dosage value '100' (from '100 mg')

### 311-min (HARD_FAIL)
- MISSING brand/ingredient from ['kamagra gold', 'sildenafil citrate']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 312-min (HARD_FAIL)
- MISSING brand/ingredient from ['cialis', 'cialis strips', 'tadalafil']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '1' (from '1 Pills')

### 313-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil citrate', 'viagra', 'viagra strips']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '1' (from '1 Pills')

### 314-min (HARD_FAIL)
- MISSING brand/ingredient from ['avanafil + dapoxetine hcl', 'super avana']
- MISSING dosage value '200' (from '200 mg/60 mg')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 315-min (HARD_FAIL)
- MISSING brand/ingredient from ['amantadine', 'symmetrel']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '30' (from '30 Pills')

### 316-min (HARD_FAIL)
- MISSING brand/ingredient from ['beclomethasone dipropionate', 'beconase aq']
- MISSING dosage value '50' (from '50 mcg/spray')
- MISSING unit count value '1' (from '1 Pills')

### 317-min (HARD_FAIL)
- MISSING brand/ingredient from ['benzac', 'benzoyl']
- MISSING dosage value '5' (from '5%')

### 318-min (SOFT_FAIL)
- MISSING brand/ingredient from ['cefadroxil', 'duricef']

### 319-min (HARD_FAIL)
- MISSING brand/ingredient from ['chloramphenicol', 'chloromycetin']
- MISSING dosage value '250' (from '250 mg')

### 320-min (HARD_FAIL)
- MISSING brand/ingredient from ['clozapine', 'clozaril']
- MISSING dosage value '100' (from '100 mg')

### 321-min (SOFT_FAIL)
- MISSING brand/ingredient from ['cardizem', 'diltiazem']

### 322-min (HARD_FAIL)
- MISSING brand/ingredient from ['eulexin', 'flutamide']
- MISSING dosage value '250' (from '250 mg')
- MISSING unit count value '30' (from '30 Pills')

### 323-min (HARD_FAIL)
- MISSING dosage value '400' (from '400 mg')

### 324-min (HARD_FAIL)
- MISSING brand/ingredient from ['hyzyd', 'isoniazid']
- MISSING dosage value '300' (from '300 mg')
- MISSING unit count value '30' (from '30 Pills')

### 325-min (HARD_FAIL)
- MISSING brand/ingredient from ['methotrexate', 'trexall']
- MISSING dosage value '2.5' (from '2.5 mg')

### 326-min (HARD_FAIL)
- MISSING brand/ingredient from ['minocin', 'minocycline']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '30' (from '30 Pills')

### 327-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '30' (from '30 Pills')

### 328-min (HARD_FAIL)
- MISSING dosage value '400' (from '400 mg')

### 329-min (HARD_FAIL)
- MISSING brand/ingredient from ['penegra', 'sildenafil']
- MISSING dosage value '50' (from '50 mg')
- MISSING unit count value '10' (from '10 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 330-min (HARD_FAIL)
- MISSING brand/ingredient from ['fasigyn', 'tinidazole']
- MISSING dosage value '500' (from '500 mg')

### 331-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')

### 332-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')

### 333-min (HARD_FAIL)
- MISSING dosage value '3' (from '3 mg')

### 334-min (HARD_FAIL)
- MISSING dosage value '5' (from '5 mg')
- MISSING unit count value '60' (from '60 Pills')

### 335-min (HARD_FAIL)
- MISSING brand/ingredient from ['stilnox', 'stilnox brand', 'zolpidem tartrate']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 336-min (HARD_FAIL)
- MISSING brand/ingredient from ['conjugated estrogens', 'premarin']
- MISSING dosage value '0.625' (from '0.625 mg')
- MISSING unit count value '30' (from '30 Pills')

### 337-min (HARD_FAIL)
- MISSING brand/ingredient from ['kamagra effervescent', 'sildenafil citrate']
- MISSING dosage value '100' (from '100 mg')

### 34-min (SOFT_FAIL)
- MISSING brand/ingredient from ['adalat', 'nifedipine']

### 340-min (HARD_FAIL)
- MISSING dosage value '0.5' (from '0.5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 341-min (HARD_FAIL)
- MISSING brand/ingredient from ['etizest', 'etizolam']
- MISSING unit count value '30' (from '30 Pills')

### 344-min (HARD_FAIL)
- MISSING brand/ingredient from ['modafinil']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 347-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil / tadalafil / vardenafil', 'test pack l-vc']
- MISSING unit count value '1' (from '1 Pills')

### 348-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil / tadalafil / vardenafil / avanafil', 'test pack l-vl']
- MISSING unit count value '1' (from '1 Pills')

### 35-min (HARD_FAIL)
- MISSING brand/ingredient from ['albendazole', 'albenza']
- MISSING dosage value '200' (from '200 mg')

### 351-min (HARD_FAIL)
- MISSING unit count value '1' (from '1 Pills')

### 352-min (HARD_FAIL)
- MISSING brand/ingredient from ['aleve', 'naproxen sodium']
- MISSING unit count value '30' (from '30 Pills')

### 353-min (HARD_FAIL)
- MISSING brand/ingredient from ['benzocaine + cetylpyridinium chloride', 'cepacol']
- MISSING dosage value '1.4' (from '1.4 mg')

### 354-min (HARD_FAIL)
- MISSING dosage value '200' (from '200 mg')

### 355-min (SOFT_FAIL)
- MISSING brand/ingredient from ['cortaid', 'hydrocortisone acetate 1%']

### 356-min (HARD_FAIL)
- MISSING brand/ingredient from ['morphine', 'morphine sulfate']
- MISSING dosage value '30' (from '30 mg')
- MISSING unit count value '30' (from '30 Pills')

### 357-min (SOFT_FAIL)
- MISSING brand/ingredient from ['adderall', 'amphetamine / dextroamphetamine salts']

### 359-min (HARD_FAIL)
- MISSING dosage value '2' (from '2 mg')
- MISSING unit count value '30' (from '30 Pills')

### 36-min (HARD_FAIL)
- MISSING unit count value '30' (from '30 Pills')

### 360-min (HARD_FAIL)
- MISSING brand/ingredient from ['restoril', 'temazepam']
- MISSING dosage value '15' (from '15 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 362-min (HARD_FAIL)
- MISSING brand/ingredient from ['hydrocodone', 'hydrocodone bitartrate']
- MISSING dosage value '10' (from '10 mg')

### 363-min (HARD_FAIL)
- MISSING brand/ingredient from ['oxycodone hcl 30mg', 'roxicodone', 'roxicodone m30']
- MISSING dosage value '30' (from '30 mg')
- MISSING unit count value '30' (from '30 Pills')

### 364-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')

### 365-min (HARD_FAIL)
- MISSING brand/ingredient from ['tapentadol', 'tapentadol hcl']
- MISSING dosage value '50' (from '50 mg')

### 366-min (HARD_FAIL)
- MISSING brand/ingredient from ['acivir cream', 'acivir cream by cipla 5%', 'acyclovir 5%']
- MISSING unit count value '1' (from '1 Pills')

### 367-min (HARD_FAIL)
- MISSING dosage value '400' (from '400 mg')
- MISSING unit count value '1' (from '1 Pills')

### 369-min (HARD_FAIL)
- MISSING dosage value '4' (from '4 mg')

### 37-min (HARD_FAIL)
- MISSING unit count value '1' (from '1 Pills')

### 370-min (HARD_FAIL)
- MISSING brand/ingredient from ['albuterol', 'ventolin', 'ventolin generic']
- MISSING dosage value '100' (from '100 mcg')
- MISSING unit count value '1' (from '1 Pills')

### 371-min (HARD_FAIL)
- MISSING brand/ingredient from ['imipramine', 'tofranil', 'tofranil generic']
- MISSING dosage value '25' (from '25 mg')

### 372-min (HARD_FAIL)
- MISSING dosage value '37.5' (from '37.5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 373-min (HARD_FAIL)
- MISSING brand/ingredient from ['azithromycin', 'azithromycin generic']
- MISSING dosage value '250' (from '250 mg')

### 374-min (HARD_FAIL)
- MISSING brand/ingredient from ['cephalexin', 'cephalexin generic']
- MISSING dosage value '500' (from '500 mg')
- MISSING unit count value '30' (from '30 Pills')

### 375-min (HARD_FAIL)
- MISSING dosage value '200' (from '200 mg')

### 376-min (HARD_FAIL)
- MISSING brand/ingredient from ['lisinopril']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 377-min (HARD_FAIL)
- MISSING dosage value '80' (from '80 mg')

### 378-min (HARD_FAIL)
- MISSING brand/ingredient from ['amiodarone', 'cordarone', 'cordarone generic']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 379-min (HARD_FAIL)
- MISSING unit count value '1' (from '1 Bottle')

### 38-min (HARD_FAIL)
- MISSING brand/ingredient from ['prednisone']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 380-min (HARD_FAIL)
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 381-min (SOFT_FAIL)
- MISSING brand/ingredient from ['famotidine', 'pepcid', 'pepcid generic']

### 382-min (HARD_FAIL)
- MISSING brand/ingredient from ['allopurinol', 'allopurinol generic']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '30' (from '30 Pills')

### 383-min (HARD_FAIL)
- MISSING brand/ingredient from ['chloroquine', 'chloroquine generic']
- MISSING dosage value '250' (from '250 mg')

### 384-min (HARD_FAIL)
- MISSING brand/ingredient from ['ibuprofen', 'ibuprofen generic']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 385-min (HARD_FAIL)
- MISSING dosage value '0.05' (from '0.05%')
- MISSING unit count value '1' (from '1 Pills')

### 386-min (HARD_FAIL)
- MISSING dosage value '0.1' (from '0.1%')
- MISSING unit count value '1' (from '1 Pills')

### 387-min (HARD_FAIL)
- MISSING brand/ingredient from ['addyi', 'flibanserin']
- MISSING dosage value '100' (from '100 mg')

### 388-min (HARD_FAIL)
- MISSING brand/ingredient from ['female cialis', 'femalefil']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '10' (from '10 Pills')

### 390-min (HARD_FAIL)
- MISSING brand/ingredient from ['diclofenac', 'volini gel']
- MISSING dosage value '1' (from '1%')
- MISSING unit count value '1' (from '1 Pills')

### 391-min (HARD_FAIL)
- MISSING brand/ingredient from ['analgin', 'analgin generic']
- MISSING dosage value '500' (from '500 mg')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 392-min (SOFT_FAIL)
- MISSING brand/ingredient from ['aspirin', 'aspirin generic']

### 393-min (HARD_FAIL)
- MISSING dosage value '250' (from '250 mcg/100 mcg')
- MISSING unit count value '1' (from '1 Inhaler')

### 395-min (HARD_FAIL)
- MISSING brand/ingredient from ['endogest', 'progesterone']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')

### 398-min (HARD_FAIL)
- MISSING brand/ingredient from ['testorapid', 'testosterone propionate']
- MISSING dosage value '100' (from '100 mg/ml')
- MISSING unit count value '10' (from '10 Pills')

### 399-min (SOFT_FAIL)
- MISSING brand/ingredient from ['meldonium']

### 4-min (HARD_FAIL)
- MISSING dosage value '4' (from '4 mg')
- MISSING unit count value '30' (from '30 Pills')

### 40-min (HARD_FAIL)
- MISSING brand/ingredient from ['amlodipine', 'norvasc']
- MISSING dosage value '5' (from '5 mg')
- MISSING unit count value '30' (from '30 Pills')

### 400-min (HARD_FAIL)
- MISSING brand/ingredient from ['zinc acetate + doxycycline + ivermectin', 'ziverdo', 'ziverdo kit']
- MISSING unit count value '1' (from '1 Pills')

### 401-min (SOFT_FAIL)
- MISSING brand/ingredient from ['oxycodone']

### 402-min (HARD_FAIL)
- MISSING brand/ingredient from ['ozempic', 'semaglutide']
- MISSING dosage value '2' (from '2 mg')
- MISSING unit count value '1' (from '1 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 403-min (HARD_FAIL)
- MISSING brand/ingredient from ['rybelsus', 'semaglutide']
- MISSING dosage value '7' (from '7 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 404-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 405-min (HARD_FAIL)
- MISSING dosage value '15' (from '15 mg')

### 406-min (HARD_FAIL)
- MISSING dosage value '15' (from '15 mg')

### 407-min (HARD_FAIL)
- MISSING unit count value '1' (from '1 Pills')

### 408-min (HARD_FAIL)
- MISSING brand/ingredient from ['semaglutide', 'wegovy']
- MISSING dosage value '2.4' (from '2.4 mg')

### 409-min (SOFT_FAIL)
- MISSING brand/ingredient from ['nandrolone decanoate']

### 41-min (HARD_FAIL)
- MISSING brand/ingredient from ['esomeprazole', 'nexium']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 410-min (HARD_FAIL)
- MISSING brand/ingredient from ['sustanon', 'testosterone blend']
- MISSING dosage value '250' (from '250 mg/ml')
- MISSING unit count value '1' (from '1 Pills')

### 411-min (HARD_FAIL)
- MISSING brand/ingredient from ['testosterone cypionate']
- MISSING unit count value '1' (from '1 Pills')

### 412-min (HARD_FAIL)
- MISSING brand/ingredient from ['testosterone enanthate']
- MISSING dosage value '250' (from '250 mg/ml')
- MISSING unit count value '1' (from '1 Pills')

### 413-min (HARD_FAIL)
- MISSING brand/ingredient from ['boldenone', 'boldenone undecylenate']
- MISSING dosage value '200' (from '200 mg/ml')
- MISSING unit count value '10' (from '10 Pills')

### 414-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg/ml')
- MISSING unit count value '10' (from '10 Vials')

### 415-min (HARD_FAIL)
- MISSING unit count value '10' (from '10 Vials')

### 417-min (HARD_FAIL)
- MISSING brand/ingredient from ['drostanolone propionate', 'masteron']
- MISSING dosage value '100' (from '100 mg/ml')
- MISSING unit count value '1' (from '1 Pills')

### 418-min (HARD_FAIL)
- MISSING brand/ingredient from ['methandienone']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '100' (from '100 Pills')

### 419-min (HARD_FAIL)
- MISSING unit count value '100' (from '100 Pills')

### 42-min (HARD_FAIL)
- MISSING dosage value '200' (from '200 mcg')
- MISSING unit count value '30' (from '30 Pills')

### 421-min (SOFT_FAIL)
- MISSING brand/ingredient from ['stanozolol']

### 422-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')

### 423-min (HARD_FAIL)
- MISSING brand/ingredient from ['halcion', 'triazolam']
- MISSING dosage value '0.25' (from '0.25 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 424-min (HARD_FAIL)
- MISSING brand/ingredient from ['tirzepatide', 'zepbound']
- MISSING dosage value '2.5' (from '2.5 mg')
- MISSING unit count value '1' (from '1 Pills')

### 425-min (HARD_FAIL)
- MISSING brand/ingredient from ['mounjaro', 'tirzepatide']
- MISSING dosage value '5' (from '5 mg')

### 426-min (HARD_FAIL)
- MISSING brand/ingredient from ['cialis oral jelly', 'tadalafil']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '7' (from '7 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 427-min (HARD_FAIL)
- MISSING brand/ingredient from ['kamagra chewable', 'soft']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '10' (from '10 Pills')

### 428-min (HARD_FAIL)
- MISSING unit count value '1' (from '1 Pills')

### 429-min (HARD_FAIL)
- MISSING brand/ingredient from ['levitra', 'levitra oral jelly', 'vardenafil hcl']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '4' (from '4 Pills')

### 43-min (HARD_FAIL)
- MISSING brand/ingredient from ['lansoprazole', 'prevacid']
- MISSING dosage value '15' (from '15 mg')
- MISSING unit count value '30' (from '30 Pills')

### 430-min (HARD_FAIL)
- MISSING brand/ingredient from ['pantoprazole', 'protonix']
- MISSING dosage value '40' (from '40 mg')

### 431-min (HARD_FAIL)
- MISSING unit count value '30' (from '30 Pills')

### 432-min (HARD_FAIL)
- MISSING dosage value '50' (from '50 mg')

### 433-min (HARD_FAIL)
- MISSING brand/ingredient from ['bimatoprost', 'latisse']
- MISSING dosage value '3' (from '3 ml')
- MISSING unit count value '1' (from '1 Bottle')

### 434-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')

### 44-min (HARD_FAIL)
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '30' (from '30 Pills')

### 45-min (HARD_FAIL)
- MISSING dosage value '150' (from '150 mg')
- MISSING unit count value '30' (from '30 Pills')

### 46-min (HARD_FAIL)
- MISSING brand/ingredient from ['finasteride', 'propecia']
- MISSING unit count value '30' (from '30 Pills')

### 47-min (HARD_FAIL)
- MISSING brand/ingredient from ['coumadin', 'warfarin']
- MISSING dosage value '5' (from '5 mg')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 49-min (HARD_FAIL)
- MISSING brand/ingredient from ['clopidogrel', 'plavix']
- MISSING dosage value '75' (from '75 mg')

### 5-min (HARD_FAIL)
- MISSING dosage value '4' (from '4 mg')
- MISSING unit count value '30' (from '30 Pills')

### 50-min (HARD_FAIL)
- MISSING dosage value '40' (from '40 mg')

### 51-min (HARD_FAIL)
- MISSING brand/ingredient from ['sofosbuvir']
- MISSING dosage value '400' (from '400 mg')
- MISSING unit count value '28' (from '28 Pills')

### 52-min (HARD_FAIL)
- MISSING dosage value '400' (from '400 mg')
- MISSING unit count value '28' (from '28 Pills')

### 58-min (HARD_FAIL)
- MISSING dosage value '5' (from '5 mg')

### 59-min (HARD_FAIL)
- MISSING dosage value '20' (from '20 mg')

### 6-min (HARD_FAIL)
- MISSING dosage value '4' (from '4 mg')

### 60-min (HARD_FAIL)
- MISSING brand/ingredient from ['cialis professional', 'tadalafil']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '10' (from '10 Pills')

### 61-min (HARD_FAIL)
- MISSING brand/ingredient from ['cialis soft tabs', 'tadalafil']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '10' (from '10 Pills')

### 62-min (HARD_FAIL)
- MISSING unit count value '10' (from '10 Pills')

### 63-min (HARD_FAIL)
- MISSING brand/ingredient from ['dapoxetine', 'priligy']
- MISSING dosage value '30' (from '30 mg')
- MISSING unit count value '10' (from '10 Pills')

### 64-min (HARD_FAIL)
- MISSING brand/ingredient from ['kamagra', 'sildenafil']
- MISSING dosage value '100' (from '100 mg')

### 65-min (HARD_FAIL)
- MISSING brand/ingredient from ['kamagra oral jelly', 'sildenafil citrate']
- MISSING unit count value '7' (from '7 Pills')

### 66-min (HARD_FAIL)
- MISSING brand/ingredient from ['levitra', 'vardenafil']
- MISSING unit count value '4' (from '4 Pills')

### 67-min (HARD_FAIL)
- MISSING brand/ingredient from ['levitra brand', 'vardenafil hcl']
- MISSING dosage value '20' (from '20 mg')
- MISSING unit count value '4' (from '4 Pills')

### 70-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil citrate + dapoxetine hcl', 'super kamagra']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '4' (from '4 Pills')

### 71-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil citrate + dapoxetine hcl', 'super p force']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '4' (from '4 Pills')

### 72-min (HARD_FAIL)
- MISSING unit count value '10' (from '10 Pills')

### 74-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil', 'viagra']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '1' (from '1 Pills')

### 75-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil citrate', 'viagra gold']
- MISSING dosage value '100' (from '100 mg')
- MISSING unit count value '10' (from '10 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 76-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')

### 77-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')

### 8-min (HARD_FAIL)
- MISSING dosage value '25' (from '25 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 80-min (HARD_FAIL)
- MISSING brand/ingredient from ['sildenafil', 'viprogra']
- MISSING dosage value '100' (from '100 mg')

### 81-min (HARD_FAIL)
- MISSING brand/ingredient from ['eldepryl', 'selegiline']
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 82-min (HARD_FAIL)
- MISSING brand/ingredient from ['bromocriptine mesylate', 'parlodel']
- MISSING dosage value '2.5' (from '2.5 mg')

### 83-min (HARD_FAIL)
- MISSING brand/ingredient from ['baclofen']
- MISSING dosage value '20' (from '20 mg')

### 86-min (HARD_FAIL)
- MISSING unit count value '10' (from '10 Pills')

### 87-min (SOFT_FAIL)
- MISSING brand/ingredient from ['baclofen', 'lioresal']

### 88-min (HARD_FAIL)
- MISSING brand/ingredient from ['methocarbamol', 'robaxin']
- MISSING dosage value '500' (from '500 mg')
- MISSING unit count value '30' (from '30 Pills')

### 89-min (HARD_FAIL)
- MISSING brand/ingredient from ['boswellia serrata extract', 'shallaki']
- MISSING dosage value '500' (from '500 mg')

### 9-min (HARD_FAIL)
- MISSING dosage value '10' (from '10 mg')
- MISSING unit count value '30' (from '30 Pills')

### 90-min (HARD_FAIL)
- MISSING dosage value '100' (from '100 mg')

### 91-min (HARD_FAIL)
- MISSING dosage value '250' (from '250 mg')

### 92-min (HARD_FAIL)
- MISSING dosage value '20' (from '20 mg')

### 93-min (HARD_FAIL)
- MISSING brand/ingredient from ['carbamazepine', 'tegretol']
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')

### 94-min (HARD_FAIL)
- MISSING dosage value '200' (from '200 mg')
- MISSING unit count value '30' (from '30 Pills')

### 95-min (HARD_FAIL)
- MISSING brand/ingredient from ['diclofenac', 'voltaren']
- MISSING dosage value '25' (from '25 mg')
- EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical

### 96-min (HARD_FAIL)
- MISSING brand/ingredient from ['diclofenac sodium', 'voveran']
- MISSING dosage value '25' (from '25 mg')
- MISSING unit count value '30' (from '30 Pills')

### 97-min (HARD_FAIL)
- MISSING brand/ingredient from ['diclofenac sodium', 'voveran sr']
- MISSING dosage value '100' (from '100 mg')

### 98-min (HARD_FAIL)
- MISSING brand/ingredient from ['tizanidine', 'zanaflex']
- MISSING dosage value '4' (from '4 mg')
- MISSING unit count value '30' (from '30 Pills')

### 99-min (HARD_FAIL)
- MISSING brand/ingredient from ['acetaminophen']
- MISSING dosage value '500' (from '500 mg')


---
*render_qa.py v1.1 — PharmaGen PRO P12.0*