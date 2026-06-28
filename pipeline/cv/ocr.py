import cv2
import numpy as np
from typing import Protocol, List, Dict, Optional
from dataclasses import dataclass
from paddleocr import PaddleOCR
import os

@dataclass
class OCRBlock:
    text: str
    bbox: List[float]  # [y1, x1, y2, x2] normalized
    confidence: float

@dataclass
class OCRResult:
    raw_text: str
    blocks: List[OCRBlock]
    confidence: float

class OCRProvider(Protocol):
    def extract(self, image_np: np.ndarray) -> OCRResult:
        ...

class PaddleProvider:
    def __init__(self):
        # Инициализация PaddleOCR (lang='ru' + use_angle_cls=True)
        self.engine = PaddleOCR(use_angle_cls=True, lang='ru', enable_mkldnn=False)

    def extract(self, image_np: np.ndarray) -> OCRResult:
        if image_np is None or image_np.size == 0:
            return OCRResult("", [], 0.0)

        try:
            results = self.engine.ocr(image_np)
        except Exception as e:
            print(f"   [OCR] PaddleOCR Error: {e}")
            return OCRResult("", [], 0.0)

        blocks = []
        if not results:
            return OCRResult("", [], 0.0)

        # PaddleOCR can return a list of results (one per page/image)
        # or a single result depending on version/config.
        data = results[0] if isinstance(results, list) and len(results) > 0 else results
        
        # Handle dict/object format (new PaddleX style)
        if hasattr(data, 'rec_texts') or (isinstance(data, dict) and 'rec_texts' in data):
            texts = getattr(data, 'rec_texts', data.get('rec_texts', []))
            scores = getattr(data, 'rec_scores', data.get('rec_scores', []))
            boxes = getattr(data, 'dt_polys', data.get('rec_boxes', []))
            
            for i in range(len(texts)):
                text = texts[i]
                conf = float(scores[i])
                box = boxes[i]
                
                # Convert box to [y1, x1, y2, x2]
                if isinstance(box, (list, np.ndarray)) and len(box) == 4 and not isinstance(box[0], (list, np.ndarray)):
                    # Format [x1, y1, x2, y2]
                    bx1, by1, bx2, by2 = box
                else:
                    # Format [[x,y], [x,y], ...]
                    try:
                        xs = [p[0] for p in box]
                        ys = [p[1] for p in box]
                        bx1, by1, bx2, by2 = min(xs), min(ys), max(xs), max(ys)
                    except Exception:
                        continue
                        
                h, w = image_np.shape[:2]
                bbox = [by1/h, bx1/w, by2/h, bx2/w]
                blocks.append(OCRBlock(text=text, bbox=bbox, confidence=conf))
        
        # Handle classic list-of-lists format
        elif isinstance(data, list):
            for line in data:
                try:
                    box, (text, conf) = line
                    xs = [p[0] for p in box]
                    ys = [p[1] for p in box]
                    h, w = image_np.shape[:2]
                    bbox = [min(ys)/h, min(xs)/w, max(ys)/h, max(xs)/w]
                    blocks.append(OCRBlock(text=text, bbox=bbox, confidence=float(conf)))
                except Exception:
                    continue

        raw_text = " ".join([b.text for b in blocks])
        avg_conf = np.mean([b.confidence for b in blocks]) if blocks else 0.0
        
        return OCRResult(raw_text, blocks, avg_conf)

class NemotronProvider:
    """NVIDIA Nemotron OCR Fallback."""
    def __init__(self, api_key: Optional[str] = None):
        from ai_layer.providers.nvidia_provider import NemotronOCRProvider
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        self.client = NemotronOCRProvider(api_key=self.api_key)

    def extract(self, image_np: np.ndarray) -> OCRResult:
        if not self.api_key:
            print("   [OCR] Nemotron API Key missing, skipping fallback.")
            return OCRResult("", [], 0.0)
            
        print("   [OCR] Calling NVIDIA Nemotron OCR Fallback...")
        # Конвертируем numpy в base64 или сохраняем во временный файл
        # Для MVP используем заглушку, но пробрасываем через провайдер
        res = self.client.extract("base64_placeholder")
        
        return OCRResult(
            raw_text=res.get("text", ""), 
            blocks=[], # Nemotron OCR v1 returns structured layout, we'll map it later
            confidence=res.get("confidence", 0.0)
        )

class HybridOCR:
    def __init__(self):
        self.paddle = PaddleProvider()
        self.nemotron = NemotronProvider()
        self.confidence_threshold = 0.72

    def extract(self, image_np: np.ndarray) -> OCRResult:
        primary = self.paddle.extract(image_np)
        
        if primary.confidence < self.confidence_threshold:
            print(f"   [OCR] Low confidence ({primary.confidence:.2f} < {self.confidence_threshold})...")
            fallback = self.nemotron.extract(image_np)
            if fallback.confidence > primary.confidence:
                return fallback
                
        return primary

# --- SINGLETON FOR PIPELINE ---
hybrid_ocr = HybridOCR()

def run_ocr(image_path: str, bbox_norm: list):
    """
    Main entry point for the pipeline.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found: {image_path}")

    h, w = img.shape[:2]
    y1, x1, y2, x2 = [int(bbox_norm[i] * (h if i%2==0 else w)) for i in range(4)]
    
    crop = img[y1:y2, x1:x2]
    result = hybrid_ocr.extract(crop)
    
    return {
        "raw_text": result.raw_text,
        "blocks": [
            {"text": b.text, "bbox": b.bbox, "confidence": b.confidence} 
            for b in result.blocks
        ],
        "confidence": result.confidence
    }
