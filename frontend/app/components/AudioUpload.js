"use client";
import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

export default function AudioTranscriber() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);
  const [pdfLink, setPdfLink] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select an audio file!");
      return;
    }

    setLoading(true);
    setTranscript("");
    setPdfLink("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/transcription/upload/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setTranscript(data.transcription_text);
      setPdfLink(`http://127.0.0.1:8000${data.pdf_download}`);
    } catch (err) {
      console.error(err);
      alert("Error uploading file or processing transcription.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-5">
      <div className="card shadow p-4 mx-auto" style={{ maxWidth: "600px" }}>
        <h2 className="text-center mb-4">🎙️ AI Audio Transcriber</h2>

        <form onSubmit={handleUpload}>
          <div className="mb-3">
            <input
              type="file"
              accept="audio/*"
              className="form-control"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary w-100"
            disabled={loading}
          >
            {loading ? "⏳ Processing..." : "Upload & Transcribe"}
          </button>
        </form>

        {transcript && (
          <div className="mt-4">
            <h5>📝 Transcribed Text:</h5>
            <div
              className="p-3 bg-light rounded"
              style={{ maxHeight: "300px", overflowY: "auto", whiteSpace: "pre-wrap" }}
            >
              {transcript}
            </div>

            {pdfLink && (
              <a
                href={pdfLink}
                className="btn btn-success mt-3"
                target="_blank"
                rel="noopener noreferrer"
              >
                📄 Download PDF
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
