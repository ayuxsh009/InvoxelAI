from pathlib import Path

import cv2
import fitz
import numpy as np


def preprocess_image(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Unable to read image")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    denoise = cv2.fastNlMeansDenoising(blur)
    thresh = cv2.adaptiveThreshold(
        denoise, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
    )
    return thresh


def convert_pdf_first_page_to_image(pdf_path: str) -> str:
    path = Path(pdf_path)
    doc = fitz.open(pdf_path)
    if len(doc) == 0:
        raise ValueError("PDF has no pages")
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_path = str(path.with_suffix(".page1.png"))
    pix.save(img_path)
    doc.close()
    return img_path
