from fastapi import APIRouter, UploadFile, File, HTTPException
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF (IMPORTANT for PDFs)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
router = APIRouter()

def clean_text(text: str) -> str:
    return " ".join(text.split())

# 🔍 Function to extract text from PDF using OCR
def extract_text_from_pdf(contents: bytes) -> str:
    text = ""

    try:
        # Open PDF from bytes
        pdf = fitz.open(stream=contents, filetype="pdf")

        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)

            # Convert PDF page to image
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")

            # Convert to PIL Image
            image = Image.open(io.BytesIO(img_bytes))

            # OCR using Tesseract
            page_text = pytesseract.image_to_string(image)

            text += page_text + "\n"

        return text.strip()

    except Exception as e:
        raise Exception(f"OCR Extraction Failed: {str(e)}")


# 🚀 API Endpoint
@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()   # ✅ correct async read

        print("File received:", file.filename)

        # Extract text using OCR
        text = extract_text_from_pdf(contents)
        cleaned_text = clean_text(text)
        print("Extracted text:", text)

        return {
            "filename": file.filename,
            "extracted_text": cleaned_text
        }

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))