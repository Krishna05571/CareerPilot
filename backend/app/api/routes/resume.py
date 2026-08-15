from fastapi import APIRouter, UploadFile, File, HTTPException
import pytesseract
from PIL import Image
import io
import os
import pymupdf
from dotenv import load_dotenv
from pydantic import BaseModel  
from google import genai

from app.services.resume_parser import parse_resume_with_ai
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# Windows Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

router = APIRouter()

class ImproveRequest(BaseModel):
    text: str


# Clean extracted text
import re

def clean_text(text: str) -> str:
    # 1. Remove extra spaces and newlines
    text = " ".join(text.split())

    # 2. Remove obvious OCR noise while preserving
    #    characters commonly used in resumes
    text = re.sub(
        r"[^a-zA-Z0-9.,:/()\-+@#&%_ ]",
        "",
        text
    )

    # 3. Fix common OCR mistakes
    corrections = {
        "Ceicl": "Critical",
        "Adptity": "Adaptability",
        "Structres": "Structures",
        "Databse": "Database",
        "Engneer": "Engineer",
        "Developr": "Developer",
        "Communicaton": "Communication",
        "Experince": "Experience",
        "Projecs": "Projects",
    }

    for wrong, correct in corrections.items():
        text = re.sub(
            rf"\b{wrong}\b",
            correct,
            text,
            flags=re.IGNORECASE
        )

    return text


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
            "resume_text": cleaned_text,
            "parsed_data": parsed_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/improve-resume")
async def improve_resume(data: ImproveRequest):
    prompt = f"""
You are an expert resume reviewer and career coach.

Improve the following resume content:
- Use strong action verbs
- Add measurable impact
- Fix grammar and clarity
- Make it ATS-friendly

Return ONLY the improved version.

Resume:
{data.text}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return {"improved": response.text}        