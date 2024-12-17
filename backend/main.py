from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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