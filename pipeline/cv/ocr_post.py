import re
from rapidfuzz import process, fuzz

# Паттерн для поиска дозировок и упаковочных единиц
UNITS_PATTERN = r'(\d+)\s*(мг|г|ml|мл|таблеток|капсул|мкг|mcg|mg|g|pcs|шт)'

def process_ocr_blocks(blocks, pharma_kb):
    """
    Пост-обработка OCR блоков:
    - Поиск дозировок через Regex.
    - Поиск кандидатов на бренд через нечеткий поиск в базе знаний (KB).
    """
    result = {
        "dosages": [],
        "brand_candidates": [],
    }

    # Собираем уникальные тексты из блоков
    seen_texts = set()
    
    for block in blocks:
        text = block["text"].strip()
        if not text or text in seen_texts:
            continue
        seen_texts.add(text)

        # 1. Поиск дозировок (DOSAGE)
        matches = re.findall(UNITS_PATTERN, text, re.IGNORECASE)
        for val, unit in matches:
            dosage = f"{val} {unit.lower()}"
            if dosage not in result["dosages"]:
                result["dosages"].append(dosage)

        # 2. Нечеткий поиск бренда (BRAND FUZZY)
        # pharma_kb должен быть списком названий брендов из мастер-листа
        if pharma_kb:
            match = process.extractOne(text, pharma_kb, scorer=fuzz.WRatio)

            if match and match[1] >= 85:
                # Проверяем, нет ли уже такого кандидата (чтобы не дублировать)
                candidate_text = match[0]
                if not any(c["text"] == candidate_text for c in result["brand_candidates"]):
                    result["brand_candidates"].append({
                        "text": candidate_text,
                        "confidence": float(match[1] / 100)
                    })

    return result
