from fastapi import APIRouter, UploadFile, File, HTTPException
import pytesseract
from PIL import Image
import io
import pymupdf

from app.services.resume_parser import parse_resume_with_ai

# Windows Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

router = APIRouter()


# Clean extracted text
def clean_text(text: str) -> str:
    return " ".join(text.split())


# 1. Direct text extraction
def extract_text_with_pymupdf(contents: bytes) -> str:
    text = ""
    pdf = pymupdf.open(stream=contents, filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text.strip()


# 2. OCR extraction
def extract_text_with_ocr(contents: bytes) -> str:
    text = ""
    pdf = pymupdf.open(stream=contents, filetype="pdf")

    for page in pdf:
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")

        image = Image.open(io.BytesIO(img_bytes))
        page_text = pytesseract.image_to_string(image)

        text += page_text + "\n"

    return text.strip()


# 3. Hybrid extraction
def extract_text(contents: bytes) -> str:
    text = extract_text_with_pymupdf(contents)

    if len(text.strip()) > 50:
        return text
    else:
        return extract_text_with_ocr(contents)


# API endpoint
@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # ✅ File validation
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        contents = await file.read()

        # Step 1: Extract text
        text = extract_text(contents)
        cleaned_text = clean_text(text)

        # Step 2: AI parsing
        parsed_data = parse_resume_with_ai(cleaned_text)

        return {
            "filename": file.filename,
            "parsed_data": parsed_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))