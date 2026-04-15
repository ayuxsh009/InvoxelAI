from __future__ import annotations

from typing import Any


class PaddleOCREngine:
    def __init__(self, languages: list[str], use_gpu: bool = False) -> None:
        self.languages = languages
        self.use_gpu = use_gpu
        self._engine = None

    def _get_engine(self):
        if self._engine is not None:
            return self._engine
        from paddleocr import PaddleOCR

        lang = "en" if "en" in self.languages else self.languages[0]
        self._engine = PaddleOCR(use_angle_cls=True, lang=lang, use_gpu=self.use_gpu)
        return self._engine

    def extract(self, image_path: str) -> dict[str, Any]:
        ocr = self._get_engine()
        result = ocr.ocr(image_path, cls=True)

        lines: list[str] = []
        confidences: list[float] = []
        for block in result or []:
            for line in block:
                text, conf = line[1][0], float(line[1][1])
                lines.append(text)
                confidences.append(conf)

        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
        return {"text": "\n".join(lines), "confidence": avg_conf, "engine": "paddleocr"}
