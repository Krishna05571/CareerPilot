from pdf2image import convert_from_path
import pytesseract

# ✅ Tell Python where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text using OCR (for image-based PDFs)
    """

    images = convert_from_path(file_path)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text