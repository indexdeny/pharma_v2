def merge_ocr_blocks(blocks, y_threshold=0.02, x_threshold=0.05):
    """
    Группирует OCR блоки в строки и объединяет близко расположенные по горизонтали фрагменты.
    blocks: [{"text": str, "bbox": [y1, x1, y2, x2], "confidence": float}]
    """
    if not blocks:
        return []

    # 1. Сортировка всех блоков по вертикали (Y)
    blocks = sorted(blocks, key=lambda b: b["bbox"][0])

    lines = []
    if not blocks: return []
    
    current_line = [blocks[0]]

    # 2. Группировка в строки на основе y_threshold
    for i in range(1, len(blocks)):
        prev = blocks[i - 1]
        curr = blocks[i]

        # Если разница по Y невелика, считаем одной строкой
        if abs(curr["bbox"][0] - prev["bbox"][0]) < y_threshold:
            current_line.append(curr)
        else:
            lines.append(current_line)
            current_line = [curr]
    lines.append(current_line)

    merged_blocks = []

    # 3. Объединение блоков внутри каждой строки по горизонтали
    for line in lines:
        # Сортируем блоки в строке по горизонтали (X)
        line = sorted(line, key=lambda b: b["bbox"][1])

        current = line[0]

        for i in range(1, len(line)):
            prev = current
            curr = line[i]

            # Дистанция между концом предыдущего и началом текущего блока
            # prev[3] - x2, curr[1] - x1
            dist_x = curr["bbox"][1] - prev["bbox"][3]

            if dist_x < x_threshold:
                # Объединяем текст
                new_text = prev["text"].strip() + " " + curr["text"].strip()

                # Объединяем bbox (минимальный охватывающий прямоугольник)
                y1 = min(prev["bbox"][0], curr["bbox"][0])
                x1 = min(prev["bbox"][1], curr["bbox"][1])
                y2 = max(prev["bbox"][2], curr["bbox"][2])
                x2 = max(prev["bbox"][3], curr["bbox"][3])

                # Усредняем уверенность
                conf = (prev["confidence"] + curr["confidence"]) / 2

                current = {
                    "text": new_text,
                    "bbox": [y1, x1, y2, x2],
                    "confidence": conf
                }
            else:
                merged_blocks.append(current)
                current = curr

        merged_blocks.append(current)

    return merged_blocks
