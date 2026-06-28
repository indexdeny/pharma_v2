import cv2
import numpy as np

def classify_geometry(image_path, bbox_norm):
    """
    Классифицирует тип упаковки (Box, Bottle, Tube, Blister, Ampoule)
    и определяет геометрические параметры для рендера.
    """
    img = cv2.imread(image_path)
    if img is None:
        return {"type": "box", "aspect_ratio": 1.0}

    h, w = img.shape[:2]
    ymin, xmin, ymax, xmax = bbox_norm
    real_w = (xmax - xmin) * w
    real_h = (ymax - ymin) * h
    
    aspect_ratio = real_w / real_h if real_h > 0 else 1.0
    
    # 1. Анализ силуэта через контуры (внутри кропа)
    crop = img[int(ymin*h):int(ymax*h), int(xmin*w):int(xmax*w)]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    hull_area = 0
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        rect_area = (real_w * real_h)
        solidity = hull_area / rect_area if rect_area > 0 else 1.0
    else:
        solidity = 1.0

    # 2. Эвристика классификации (Canonical Taxonomy)
    pkg_type = "box_vertical_standard"
    
    if aspect_ratio > 2.0:
        if solidity < 0.8:
            pkg_type = "foil_strip"
        else:
            pkg_type = "box_horizontal_flat"
    elif aspect_ratio < 0.5:
        if solidity < 0.7:
            pkg_type = "tube_standard"
        elif aspect_ratio < 0.3:
            pkg_type = "vial_glass_small"
        else:
            pkg_type = "bottle_plastic_tall"
    elif 0.5 <= aspect_ratio <= 0.85:
        if solidity > 0.9:
            pkg_type = "bottle_plastic_round"
        else:
            pkg_type = "box_vertical_slim"
    elif 0.85 < aspect_ratio < 1.15:
        pkg_type = "box_square"
    elif solidity < 0.6:
        pkg_type = "sachet_flat"
    elif solidity < 0.8:
        pkg_type = "blister_card"
    else:
        pkg_type = "box_vertical_standard"
        
    return {
        "package_type": pkg_type,
        "aspect_ratio": round(aspect_ratio, 2),
        "orientation": "vertical" if aspect_ratio < 0.9 else "horizontal",
        "solidity": round(solidity, 2),
        "confidence": 0.85, # Default confidence for heuristic classification
        "render_params": {
            "safe_margin": 0.05,
            "edge_rounding": 0.02 if "box" in pkg_type else 1.0
        }
    }
