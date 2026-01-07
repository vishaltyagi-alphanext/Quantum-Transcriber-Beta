import whisper
from fpdf import FPDF
import os

# Load model once (local Whisper)
model = whisper.load_model("base")  # options: tiny, base, small, medium, large

UPLOAD_FOLDER = "app/uploads"
DOWNLOAD_FOLDER = "app/downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file to text using Whisper.
    """
    result = model.transcribe(file_path)
    return result["text"]

def save_transcription_pdf(text: str, filename: str) -> str:
    """
    Saves transcription text as a PDF.
    Returns the path to the PDF file.
    """
    pdf_path = os.path.join(DOWNLOAD_FOLDER, f"{filename}.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(pdf_path)
    return pdf_path
