from __future__ import annotations

from typing import Any


class EasyOCREngine:
    def __init__(self, languages: list[str]) -> None:
        self.languages = languages
        self._engine = None

    def _get_engine(self):
        if self._engine is not None:
            return self._engine
        import easyocr

        self._engine = easyocr.Reader(self.languages, gpu=False)
        return self._engine

    def extract(self, image_path: str) -> dict[str, Any]:
        reader = self._get_engine()
        result = reader.readtext(image_path)

        lines: list[str] = []
        confidences: list[float] = []
        for _, text, conf in result:
            lines.append(text)
            confidences.append(float(conf))

        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
        return {"text": "\n".join(lines), "confidence": avg_conf, "engine": "easyocr"}
