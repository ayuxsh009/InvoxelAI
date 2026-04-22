import os

import pdfplumber

from app.core.config import settings
from app.ocr.easy_engine import EasyOCREngine
from app.ocr.paddle_engine import PaddleOCREngine
from app.ocr.preprocess import convert_pdf_first_page_to_image, preprocess_image
from app.utils.parser import parse_invoice_fields


class OCRService:
    def __init__(self) -> None:
        langs = [lang.strip() for lang in settings.ocr_langs.split(",") if lang.strip()]
        self.paddle = PaddleOCREngine(languages=langs, use_gpu=settings.paddle_use_gpu)
        self.easy = EasyOCREngine(languages=langs)

    def _extract_text_from_pdf(self, file_path: str) -> str:
        text_chunks: list[str] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages[:3]:
                txt = page.extract_text() or ""
                if txt.strip():
                    text_chunks.append(txt)
        return "\n".join(text_chunks)

    def run(self, file_path: str) -> dict:
        ext = os.path.splitext(file_path)[1].lower()
        base_text = ""
        image_path = file_path

        if ext == ".pdf":
            base_text = self._extract_text_from_pdf(file_path)
            image_path = convert_pdf_first_page_to_image(file_path)

        preprocess_image(image_path)

        raw = None
        errors: list[str] = []
        for engine_name in ["paddle", "easy"]:
            try:
                engine = self.paddle if engine_name == "paddle" else self.easy
                raw = engine.extract(image_path)
                if raw.get("text"):
                    break
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{engine_name}: {exc}")

        raw_text = "\n".join([base_text, raw.get("text", "") if raw else ""]).strip()
        parsed = parse_invoice_fields(raw_text)

        return {
            "parsed": parsed,
            "raw": {
                "text": raw_text,
                "confidence": raw.get("confidence", 0.0) if raw else 0.0,
                "engine": raw.get("engine", "none") if raw else "none",
                "errors": errors,
            },
        }
