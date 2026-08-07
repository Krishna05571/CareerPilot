from fastapi import APIRouter, UploadFile, File, HTTPException
import pytesseract
from PIL import Image # Pillow lib 
import io
import fitz  # PyMuPDF

# Required for Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

router = APIRouter()


#  Clean extracted text
def clean_text(text: str) -> str:
    return " ".join(text.split())


#  1. Direct text extraction (for normal PDFs)
def extract_text_with_pymupdf(contents: bytes) -> str:
    text = ""
    pdf = fitz.open(stream=contents, filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text.strip()


#  2. OCR extraction (for scanned PDFs)
def extract_text_with_ocr(contents: bytes) -> str:
    text = ""

    pdf = fitz.open(stream=contents, filetype="pdf")

    for page in pdf:
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")

        image = Image.open(io.BytesIO(img_bytes))
        page_text = pytesseract.image_to_string(image)

        text += page_text + "\n"

    return text.strip()


#  3. Hybrid function (BEST PRACTICE)
def extract_text(contents: bytes) -> str:
    # Try direct extraction first
    text = extract_text_with_pymupdf(contents)

    if text.strip():
        return text
    else:
        return extract_text_with_ocr(contents)


#  API Endpoint
@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Use hybrid extraction
        text = extract_text(contents)
        cleaned_text = clean_text(text)

        return {
            "filename": file.filename,
            "extracted_text": cleaned_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))