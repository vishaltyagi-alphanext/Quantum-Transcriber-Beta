from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from app.services.transcribe import transcribe_audio, save_transcription_pdf
import os

router = APIRouter()

UPLOAD_FOLDER = "app/uploads"
DOWNLOAD_FOLDER = "app/downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@router.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = transcribe_audio(file_path)
    pdf_path = save_transcription_pdf(text, file.filename)

    return JSONResponse({
        "filename": file.filename,
        "transcription_text": text,
        "pdf_download": f"/transcription/download/{os.path.basename(pdf_path)}"
    })

@router.get("/download/{pdf_file}")
def download_pdf(pdf_file: str):
    file_path = os.path.join(DOWNLOAD_FOLDER, pdf_file)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf", filename=pdf_file)
    return JSONResponse({"error": "File not found"}, status_code=404)
