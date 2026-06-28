import re
from typing import List, Dict, Any

DOSAGE_PATTERN = re.compile(
    r'(\d+(?:[.,]\d+)?)\s*(mg|g|mcg|ml|мг|г|мл|таблеток|капсул)',
    re.IGNORECASE
)

def area(bbox):
    y1, x1, y2, x2 = bbox
    return max(0.0, (y2 - y1) * (x2 - x1))

def center_y(bbox):
    return (bbox[0] + bbox[2]) / 2

def center_x(bbox):
    return (bbox[1] + bbox[3]) / 2

class ZoneClassifier:
    """
    Классификатор семантических зон с детальным скорингом (Telemetry-ready).
    """

    def classify(self, merged_blocks, geometry=None, kb_hints=None):
        if not merged_blocks: return self.empty_result()

        kb_brand_candidates = kb_hints.get("brand_candidates", []) if kb_hints else []
        max_area = max(area(b["bbox"]) for b in merged_blocks)

        scored_blocks = []
        for block in merged_blocks:
            analysis = self.analyze_block(block, max_area, kb_brand_candidates)
            scored_blocks.append({
                "block": block,
                "analysis": analysis
            })

        zones_raw = {
            "brand": self.extract(scored_blocks, "brand"),
            "dosage": self.extract(scored_blocks, "dosage"),
            "logo": self.extract(scored_blocks, "logo")
        }

        return {
            "source_layout": self.select_best(zones_raw),
            "telemetry": zones_raw
        }

    def analyze_block(self, block, max_area, kb_brands):
        text = block.get("text", "")
        bbox = block.get("bbox", [0, 0, 0, 0])
        conf = block.get("confidence", 0.5)
        
        block_area = area(bbox)
        cy = center_y(bbox)
        
        # Развернутый скоринг для бренда
        brand_breakdown = {
            "size_score": round((block_area / max_area) * 0.4, 2),
            "position_score": round((1.0 - cy) * 0.2, 2) if cy < 0.5 else 0.0,
            "ocr_score": round(conf * 0.1, 2),
            "kb_match_score": 0.0
        }
        
        lowered = text.lower()
        for kb in kb_brands:
            if kb.get("text", "").lower() in lowered:
                brand_breakdown["kb_match_score"] = 0.4
                break
        
        final_brand = sum(brand_breakdown.values())

        # Скоринг для дозировки
        dosage_score = 0.85 if DOSAGE_PATTERN.search(text) else 0.0
        dosage_score += (0.1 if 0.3 < cy < 0.7 else 0.0)

        return {
            "brand": {"score": round(final_brand, 2), "breakdown": brand_breakdown},
            "dosage": {"score": round(dosage_score, 2)},
            "logo": {"score": 0.55 if block_area < 0.01 and cy < 0.3 else 0.0}
        }

    def extract(self, scored_blocks, zone_type):
        candidates = []
        for item in scored_blocks:
            res = item["analysis"].get(zone_type)
            score = res["score"] if isinstance(res, dict) else res
            if score < 0.2: continue
            
            candidates.append({
                "text": item["block"]["text"],
                "bbox": item["block"]["bbox"],
                "confidence": score,
                "breakdown": res.get("breakdown") if isinstance(res, dict) else None
            })
        return sorted(candidates, key=lambda x: x["confidence"], reverse=True)

    def select_best(self, zones):
        final = {}
        for k, v in zones.items():
            if not v: final[k] = None
            else: final[k] = {"primary": v[0], "alternatives": v[1:3]}
        return final

    def empty_result(self):
        return {"source_layout": {}, "telemetry": {}}

def classify_zones(merged_blocks, geometry=None, kb_hints=None):
    return ZoneClassifier().classify(merged_blocks, geometry, kb_hints)
