import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CreativeBrief(BaseModel):
    brief: str

class Script(BaseModel):
    brief: str
    script: str

@app.post("/validate-brief")
async def validate_brief(brief: CreativeBrief):
    return {"valid": len(brief.brief.strip()) > 0}

@app.post("/generate-feedback")
async def generate_feedback(script: Script):
    return {"feedback": f"Feedback for script based on brief: '{script.brief}'. Your script seems well-structured and aligns with the creative brief."}