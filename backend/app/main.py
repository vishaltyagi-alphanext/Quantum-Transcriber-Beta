# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transcription  # make sure this path is correct

app = FastAPI()

# CORS middleware — must be BEFORE include_router
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routes
app.include_router(transcription.router, prefix="/transcription")

@app.get("/")
def read_root():
    return {"message": "FastAPI Quantum AI Transcriber is running!"}
