# Отчет: глубокий ресерч реальных бренд-цветов упаковок

Период работы: 16–20 июля 2026

## Задача (ТЗ)

Для всех 351 бренд-категории из `SSOT/sku_brand_colors.csv` провести углубленный поиск РЕАЛЬНЫХ цветов упаковки/коробки/логотипа (официальные сайты производителей, FDA/DailyMed, фото на аптечных маркетплейсах, репозитории логотипов, форумы). 29 ранее подтвержденных палитр использовались как отправные точки. Жесткий инвариант: цвета не выдумываются — записывается только то, что реально найдено в источниках (даже если это 1–2 цвета); иначе бренд помечается как «не найдено». Итоговый файл `brand_colors_report.md` в корне проекта.

## Как выполнялось

- 9 раундов фоновых Workflow-прогонов, каждый бренд — отдельный research-субагент со структурированным выводом (`category, found, main_colors, additional_colors, source_note`).
- Параллельность жестко ограничена 3 агентами одновременно (по требованию).
- Раунды 1–7: глубокий поиск с кросс-проверкой по нескольким источникам и пиксельным анализом фото упаковок. Раунды 8–9: облегченный быстрый поиск (1–2 запроса на бренд) — по запросу ускорить работу.
- Результаты раундов сливались скриптом с сопоставлением по имени бренда в тексте ответа и по точному совпадению seed-палитр.
- Работа многократно прерывалась лимитами сессии (~15–90 агентов до срабатывания); раунд 9 остановлен недельным лимитом (сброс 23 июля, 15:00 Киев) — на этом ресерч приостановлен.

## Итоговая статистика

| Показатель | Кол-во |
|---|---|
| Всего брендов | 351 |
| Обработано агентами | 281 |
| Цвета найдены и подтверждены | 91 |
| Обработано, но цвета не найдены (честное «не найдено») | 190 |
| Не обработано (лимиты сессии) | 70 |

Еще ~26 результатов агентов не удалось однозначно привязать к бренду (агент не указал имя бренда в ответе) — они сохранены в `deep_unmatched.json` в скретчпаде, почти все со статусом «не найдено».

## Найденные палитры (91)

Формат: `{Бренд} — {основные цвета} | {дополнительные цвета}`

Accutane — #007AC2 | #FFC0CB; #800000; #4169E1
Acetaminophen — #CC0000 | #808080; #FFD700; #1C4E9C; #F48FB1; #FF8C00
Aciphex — #1B7DA7; #ED7D2B; #104C65; #F8F9FA
Acivir — #A80000; #B03050 | #1F9E7A; #30C0C0
Adalat — #C8102E
Addyi — #E40589; #FCEAF7; #1A1A1A; #60515B
Adipex — #0072BC
Advair Diskus Generic Inhaler — #7B4397 | #800080
Advil — #002D62; #FFC72C; #C8102E
Alavert —  | #6B3FA0
Alesse — #4A90D9; #F4A6C6 | #A8D5A8
Aleve — #FFC72C; #0057A0; #1A1A1A
Alli — #1B4F8C; #2FA8B8
Ambien — #F4A7B9 | #4169B2
Amoxil — #003DA5; #F49AC1 | #E4007C
Ampicillin — #003366; #0D5FB8
Anacin — #0B1E60; #FDDB00; #FF6C0C | #1B4D2E
Androgel — #00446c | #00447c
Apcalis — #1E3A9C; #8B1A1A | #F5A623
Aralen — #1E88E5; #B935A6 | #468FF1; #5D5D99
Aricept — #FFD700 | #B22222
Arimidex — #FFC0CB
Aspirin — #E30613; #00A887; #FFAD00; #CD6FEF
Atarax —  | #FFA500; #008000; #FFFF00
Aurogra — #1E3A8A | #4169E1
Avodart — #F0D060 | #E81E23; #F25D18
Benadryl — #E91E8C; #1B3E8C | #4CAF50
Benzac — #7058B8 | #F5C4BC; #C8C8D0
Cardizem — #1F4E9C | #5DADE2; #F4D03F
Caverta — #1E5AA8 | #B22222
Celebrex — #D4AF37 | #0070BF; #00AFF0
Cepacol — #005A9A; #D0021B; #FFC72C
Cialis — #D4A017 | #1B3A6B; #F2C94C
Claritin — #0072BC; #4CAF50; #E31E24
Cortaid — #1E2E78; #0A8CDC | #64C864; #141E64
Cozaar — #007A73 | #4CAF50
Crestor — #FFD966; #F4A6C6
Cymbalta — #3CB371; #1E5AA8; #4A7C59
Cytotec — #A9C6DE; #C2185B
Danocrine — #FFA500
Deca Durabolin — #28B1DF | #A80018
Detrol — #0057A0 | #3AA6A6
Diamox — #FFA500
Diflucan — #0072B5; #3EB6E0 | #0070BF; #00AFF0
Dilantin — #F37321; #0C3F63 | #F4A0B5
Ditropan — #A7C7E7 | #FDF5A6; #F7C6D9
Dramamine — #00A0E0; #F0D000; #E02010; #201020
Dulcolax — #E6007E | #F589B4
Duricef — #FFA500 | #800000
Dyrenium — #CC0000 | #FFCC00
Effexor — #FFCBA4; #FF8C42 | #B0AEA5
Endogest — #C8324B; #7C8F6C | #9070B0
Eulexin — #5C4033 | #8B5A2B
Female Viagra — #FFC0CB | #FF69B4; #0047AB
Flomax — #F58220 | #8B4513
Fosamax — #0A5E3C; #F5C828 | #90A898
Gestanin — #FFE8C4; #FCBC00
Glucophage — #469f6d; #ad0b47
Glycomet — #8B0E0C; #0577C9 | #96100B
Halcion — #1E4B9C | #C8CCD1
Hoodia — #F07824 | #00B454
HUCOG-10000 HP — #E63C2E; #00A31A | #66B0D6; #5A5A64; #F9C9C9
HUCOG-2000 HP — #358f93; #829729; #1f2a3b | #d2d1eb
HUCOG-5000 HP — #1E8DD4
Hyzaar — #231F20; #6D3528 | #E90B2A; #F1BC48
Ibuprofen — #144089; #F07800; #FAE210 | #0C679E; #CC0000; #786C48; #0C1824
Imitrex — #003C84; #FCC000 | #A80060; #808080
Imovane — #0000c8 | #d2506e; #9b7a90
Inderal — #FF80D8; #380850 | #00C860; #FBFBFE
Indocin — #1D5A4A; #C5DA71
Isoptin — #e8180f | #802840; #d08888
Isordil — #0293D5
Kamagra — #0B2E92; #1C93AC | #143128; #C06F6C; #CCB57F
Keflex — #08BC05 | #FCEB00; #039CFF; #FD1515
Klonopin — #9678E6; #F8F945
Ladygra — #D6146E; #0F7377 | #E2508F; #931E45
Lamictal — #003593; #FF6C0C | #009EE5; #95D600
Lamisil — #182454; #009CCC | #C0E020; #F0D824
Lasix — #0040D0; #F8B010; #A81050
Lida Daidaihua — #90C695; #A9A9A9 | #0047AB; #8B00FF
Meldonium — #D01060 | #900040
Minoxidil — #DA291C; #FFD100 | #84754E
Mounjaro — #7B2D8E | #2E5FA3; #4A8C3C; #F2C230; #E8792B; #8C8C8C
Nandrolone Decanoate — #0033A0 | #5A3A29; #5397E7; #E6BC1A
Nexium — #8A4FA3 | #FFD100
Nizoral — #D32B2B; #1F5FA8
Prednisolone — #182865; #0078b4 | #0c6ab8
Prednisone — #FFC0CB; #FFCBA4 | #4FA73C; #27518C; #893A65
Rybelsus — #2E8540; #C8102E; #0066B3
Silagra — #CC0000 | #0066B3; #009639
Strattera — #800000

## Обработано, новых цветов не найдено (190)

Агент честно завершил поиск без результата (чаще всего: в открытых источниках есть только цвет таблетки, а не упаковки; препарат снят с производства; фото упаковки недоступны).

Abilify, Acticin, Actos, Adderall, Albenza, Aldactone, Aldara, Allopurinol, Altace, Amaryl, Anafranil, Analgin, Anaridex, Antabuse, Arcoxia, Aristocort, Artane, Artvigil, Asacol, Ativan, Atomoxetine, Augmentin, Avalide, Avana, Avapro, Aygestin, Azithromycin, Baclofen, Bactrim, Beconase AQ, Beloc, Benicar, Betablock, Boldenone, Buspar, Cabgolin, Cafergot, Calan, Catapres, Celexa, Centrex, Cephalexin, Champix, Chloromycetin, Chloroquine, Ciplactin, Cipro, Clarinex, Cleocin, Clomid, Clozaril, Codeine, Colchicine, Cordarone, Coumadin, Cytoxan, Decadron, Deltasone, Desyrel, Dexanil, Dostinex, Doxycycline, Dutas, Elavil, Eldepryl, Emsam, Endep, Erythromycin, Estrace, Etizest, Evista, Evorel, Fasigyn, Femalefil, Fildena, Flagyl, Fliban, Flormidal, Floxin, Hydrocodone, Hyzyd, Latisse, Levaquin, Levitra, Levlen, Lexapro, Lexotanil, Lioresal, Lipitor, Lisinopril, Lopressor, Lotrisone, Lovegra, Loxitane, Lumigan, Lunesta, Lyrica, Macrobid, Malegra, Masteron, Maxalt, Medrol, Meridia, Methandienone, Methenolone, Microzide, Minipress, Minocin, Mobic, Modafinil, Modalert, Modvigil, Mogadon, Morphine, Motilium, Motrin, Nandrolone Phenylpropionate, Naprosyn, Neurontin, Nitroglycerin, Nolvadex, Nootropil, Noroxin, Norplant-72, Norvasc, Omez, Onax, Original Test pack L-VC, Oxandrolone, Oxycodone, Oxymetholone, Oxytrol, Ozempic, Pamelor, Pariet, Parlodel, Paxil, Penegra, Penicillin, Pepcid, Percocet, Periactin, Phenergan, Plaquenil, Plavix, Ponstel, Premarin, Prevacid, Priligy, Prilosec, Pristiq, Procardia, Progesterone, Propecia, Protonix, Proventil, Provera, Provigil, Prozac, Qutan, Remeron, Restomed, Restoril, Retin-A, Revia, Risperdal, Ritalin, Rivotril, Robaxin, Roxicodone M30, Sarafem, Selgin, Seroquel, Shallaki, Sibutramine, Sildalis, Singulair, Sofosbuvir, Soma, Sominex, Sonata, Sovaldi, Stanozolol, Stendra, Stilnox, Stromectol, Sumycin, Super Avana, Super P Force, Suprax

У 12 из них уже есть ранее подтвержденные палитры (сохраняются из `sku_brand_colors.csv` без изменений): Latisse, Levitra, Lumigan, Macrobid, Motrin, Prevacid, Prilosec, Proventil, Prozac, Ritalin, Rivotril, Sarafem.

## Не обработано из-за лимитов (70)

Slimex, Super Kamagra, Sustanon, Sustaviron-250, Sustiva, Symmetrel, Synthroid, Tadacip, Tadalis SX, Tadapox, Tapentadol, Tegretol, Tenormin, Test Pack L-VC, Test Pack L-VL, Test Pack Mini-VCL, Test Pack XXL-VCL, Testorapid, Testosterone Cypionate, Testosterone Enanthate, Tofranil, Topamax, Toprol, Toradol, Torsemide, Tramadol, Trenbolone Acetate, Trenbolone Enanthate, Trexall, Trinex, Tylenol, Ultram, Unisom, Urispas, Uroxatral, Valium, Valtrex, Vaniqa, Venlor, Ventolin, Verapamil, Vermox, Viagra, Victoza, Vilafinil, Viprogra, VOLINI, Voltaren, Voveran, Waklert, Wegovy, Wellbutrin, Xalatan, Xanax, Xenical, Yasmin, Zanaflex, Zantac, Zebeta, Zenegra, Zepbound, Zithromax, Ziverdo Kit, Zocor, Zofran, Zoloft, Zovirax, Zyban, Zyprexa, Zyrtec

У 5 из них уже есть ранее подтвержденные палитры (сохраняются из `sku_brand_colors.csv` без изменений): Sustanon, Viagra, VOLINI, Voltaren, Xalatan.

## Состояние и следующие шаги

- Итоговый файл `brand_colors_report.md` (по ТЗ — в корне проекта) пока НЕ создан: 151 бренд еще не обработан.
- Все промежуточные данные для возобновления сохранены: `deep_matched.json`, `deep_remaining.json`, `merge_rounds.js`, скрипт раунда — в скретчпаде сессии.
- Возобновить можно после сброса недельного лимита (23 июля, 15:00 Киев): запустить следующий раунд по `deep_remaining.json`, затем слить результаты и сгенерировать финальный отчет.
