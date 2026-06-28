import os
from schemas.analysis_passport import AnalysisPassport, ObservedZone
from schemas.common import UVBox, ObservedPalette

# CV СЛОИ (Extraction)
from cv.detect import detect_object
from cv.geometry_classifier import classify_geometry
from cv.ocr import run_ocr
from cv.merger import merge_ocr_blocks
from cv.ocr_post import process_ocr_blocks
from cv.zone_classifier import classify_zones
from skills.kb import load_kb

# Загрузка базы знаний для подсказок OCR (опционально)
KB_PATH = "data/master_product_list.csv"
KB_DATA = load_kb(KB_PATH)
KB_NAMES = [v["name"] for v in KB_DATA.values() if v.get("name")]

def extract_visual_passport(image_path: str) -> AnalysisPassport:
    """
    STRICT CV LAYER: Объективная фиксация увиденного без ИИ-интерпретаций.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # --- CV EXTRACTION ---
    detection = detect_object(image_path)
    if not detection["object_detected"]:
        raise ValueError("DETECTION_FAILURE: Packaging object not found.")

    source_geo = classify_geometry(image_path, detection["bbox"])
    ocr_raw = run_ocr(image_path, detection["bbox"])
    merged_blocks = merge_ocr_blocks(ocr_raw["blocks"])
    kb_hints = process_ocr_blocks(merged_blocks, KB_NAMES)
    
    # Семантическая классификация зон (Observation)
    classification = classify_zones(merged_blocks, kb_hints=kb_hints)
    source_layout = classification.get("source_layout")
    raw_telemetry = classification.get("telemetry", {})
    
    if source_layout is None:
        source_layout = {}

    # Создаем АНАЛИТИЧЕСКИЙ ПАСПОРТ (Объективная реальность)
    extracted_zones = {}
    
    # Вспомогательная функция для безопасного извлечения зон
    def add_zone(zone_id, layout_key):
        if source_layout is None:
            return
        layout_item = source_layout.get(layout_key)
        if not layout_item:
            return
        data = layout_item.get("primary", {})
        bbox = data.get("bbox", [0, 0, 0, 0])
        if bbox[2] > bbox[0] and bbox[3] > bbox[1]:
            extracted_zones[zone_id] = ObservedZone(
                raw_text=data.get("text"),
                bbox=UVBox(y1=bbox[0], x1=bbox[1], y2=bbox[2], x2=bbox[3]),
                ocr_confidence=data.get("ocr_confidence", 0),
                visual_score=min(1.0, float(data.get("confidence", 0)))
            )

    add_zone("brand_zone", "brand")
    add_zone("dosage_zone", "dosage")

    passport = AnalysisPassport(
        source_image_path=image_path,
        geometry_type=source_geo.get("package_type", "unknown"),
        geometry_confidence=source_geo.get("confidence", 0.0),
        observed_palette=ObservedPalette(
            dominant_colors=raw_telemetry.get("palette_colors", ["#FFFFFF"]),
            detected_background="#FFFFFF"
        ),
        extracted_zones=extracted_zones
    )
    
    return passport
