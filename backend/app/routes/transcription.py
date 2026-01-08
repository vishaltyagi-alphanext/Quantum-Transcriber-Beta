import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse

from app.services.transcribe import transcribe_audio, save_transcription_pdf
from app.services.structure_transcription import structure_transcript

router = APIRouter()

UPLOAD_FOLDER = "app/uploads"
DOWNLOAD_FOLDER = "app/downloads"

@router.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        raw_text = transcribe_audio(file_path)
        structured_text = structure_transcript(raw_text)
        pdf_path = save_transcription_pdf(structured_text, file.filename)

        return {
            "filename": file.filename,
            "transcription_text": structured_text,
            "raw_text": raw_text,
            "pdf_download": f"/transcription/download/{os.path.basename(pdf_path)}"
        }

    except Exception as e:
        print("🔥 ERROR:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/download/{pdf_file}")
def download_pdf(pdf_file: str):
    file_path = os.path.join(DOWNLOAD_FOLDER, pdf_file)

    if not os.path.exists(file_path):
        return JSONResponse({"error": "File not found"}, status_code=404)

    return FileResponse(file_path, media_type="application/pdf", filename=pdf_file)
