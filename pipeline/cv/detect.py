from ultralytics import YOLO
import cv2
import os
import numpy as np

# загружаем модель один раз
model = YOLO("yolov8n.pt") 

def detect_object(image_path: str) -> dict:
    """
    Находит основной объект (упаковку) на изображении.
    Возвращает нормализованный bbox [ymin, xmin, ymax, xmax] и уверенность.
    """
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Image not found: {image_path}")

    h, w = img.shape[:2]

    # Запуск инференса
    results = model(img)[0]

    if len(results.boxes) == 0:
        # Fallback: assume the whole image is the package if detection fails
        return {
            "object_detected": True,
            "bbox": [0.0, 0.0, 1.0, 1.0],
            "confidence": 0.1
        }

    # берем самый уверенный bbox
    boxes = results.boxes
    best_idx = boxes.conf.argmax().item()

    box = boxes.xyxy[best_idx].tolist()
    conf = boxes.conf[best_idx].item()

    x1, y1, x2, y2 = box

    # нормализация [ymin, xmin, ymax, xmax] (0–1)
    bbox_norm = [
        y1 / h,
        x1 / w,
        y2 / h,
        x2 / w
    ]

    return {
        "object_detected": True,
        "bbox": bbox_norm,
        "confidence": conf
    }

def crop_object(image_path: str, bbox_norm: list):
    """
    Обрезает изображение по нормализованному bbox [ymin, xmin, ymax, xmax].
    Обеспечивает 2048x2048 1:1 aspect ratio (с паддингом).
    """
    img = cv2.imread(image_path)
    if img is None:
        return None

    h, w = img.shape[:2]

    ymin = int(bbox_norm[0] * h)
    xmin = int(bbox_norm[1] * w)
    ymax = int(bbox_norm[2] * h)
    xmax = int(bbox_norm[3] * w)

    # Ограничиваем координаты
    xmin, ymin = max(0, xmin), max(0, ymin)
    xmax, ymax = min(w, xmax), min(h, ymax)

    crop = img[ymin:ymax, xmin:xmax]
    ch, cw = crop.shape[:2]

    # Делаем квадратным (паддинг белым цветом)
    side = max(ch, cw)
    canvas = np.ones((side, side, 3), dtype=np.uint8) * 255
    
    y_off = (side - ch) // 2
    x_off = (side - cw) // 2
    canvas[y_off:y_off+ch, x_off:x_off+cw] = crop

    # Ресайз до 2048x2048
    final_img = cv2.resize(canvas, (2048, 2048), interpolation=cv2.INTER_LANCZOS4)

    return final_img
