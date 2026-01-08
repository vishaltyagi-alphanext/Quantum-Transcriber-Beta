from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transcription

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcription.router, prefix="/transcription")


@app.get("/")
def read_root():
    return {"message": "FastAPI Quantum AI Transcriber is running!"}
