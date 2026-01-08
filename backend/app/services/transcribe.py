import os
import whisper
from fpdf import FPDF

UPLOAD_FOLDER = "app/uploads"
DOWNLOAD_FOLDER = "app/downloads"
FONT_PATH = "app/fonts/DejaVuSans.ttf"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

model = whisper.load_model("base")  # load once

def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(file_path)
    return result["text"]


def save_transcription_pdf(text: str, filename: str) -> str:
    pdf_path = os.path.join(DOWNLOAD_FOLDER, f"{filename}.pdf")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add the TTF font file
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.multi_cell(0, 10, text)
    pdf.output(pdf_path, dest='F')

    return pdf_path
