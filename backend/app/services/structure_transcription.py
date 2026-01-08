import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # loads GEMINI_API_KEY from .env

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def structure_transcript(raw_text: str) -> str:
    """
    Structures raw transcription text into Interviewer/Participant format.
    Removes filler words, fixes grammar, and organizes speaker turns.
    """

    prompt = f"""
You are formatting interview transcripts for academic research.

Rules:
- There are two speakers: Interviewer and Participant
- Remove filler words (um, uh, you know)
- Fix grammar and punctuation
- Do NOT change meaning
- Group sentences into logical speaker turns
- Use this format exactly:

Interviewer:
<text>

Participant:
<text>

Transcript:
\"\"\"{raw_text}\"\"\"
"""

    # Generate structured transcript using Gemini
    response = client.models.generate_content(
        model="gemini-3-flash-preview",  # latest supported model
        contents=prompt
    )

    return response.text.strip()
