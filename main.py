from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/analyze")
async def analyze(audio: UploadFile = File(...)):
    try:
        from thymia_sentinel import ThymiaSentinel
        sentinel = ThymiaSentinel(api_key=os.environ["THYMIA_API_KEY"])
        audio_bytes = await audio.read()
        result = sentinel.analyze(audio_bytes, policy="passthrough")
        scores = result.get("biomarkers", {})
        return {
            "stress": round(scores.get("stress", 0.5) * 100),
            "fatigue": round(scores.get("fatigue", 0.5) * 100),
            "energy": round((1 - scores.get("fatigue", 0.5)) * 100),
            "focus": round((1 - scores.get("distress", 0.5)) * 100)
        }
    except Exception as e:
        return {"error": str(e), "stress": 52, "fatigue": 58, "energy": 45, "focus": 48}

@app.get("/health")
def health():
    return {"status": "ok"}
