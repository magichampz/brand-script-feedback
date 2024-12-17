from openai import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from typing import List
from dotenv import load_dotenv

from feedback_processors_2 import (
    consolidate_feedbacks,
    summarize_feedback,
    generate_feedback_2nd
)

load_dotenv()

# Initialize OpenAI client with the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API Key not found. Set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

key_points_storage = {}

# Input Models
class CreativeBrief(BaseModel):
    brief: str

class Script(BaseModel):
    script: str

# Processing Functions for the main (first) feedback generation system
def extract_key_points(brief_guidelines):
    system_prompt_extract = """
    You are an AI assistant that extracts the key points from a creative brief to be used to generate feedback on submitted scripts.
    Each point should be a single string which details what needs to be checked for.
    Each point should be put into a JSON structure as shown in the following example:

    Input:
    Animal Guidelines
    Milanote does not sponsor video content that includes:
    - pictures or videos of animals

    Plant Guidelines
    Milanote recommends that sponsor video content includes:
    - pictures or videos of plants

    Output:
    {
    "Key points": [
        "Check that the script does not contain any pictures or videos of animals.",
        "Check that the script contains pictures or videos of plants."
        ]
    }

    """
    user_prompt_extract = f"""
    Creative Brief: {brief_guidelines}
    """

    prompt = [
            {"role": "system", "content": system_prompt_extract},
            {"role": "user", "content": user_prompt_extract}
        ]
    response_extract = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    key_points = response_extract.choices[0].message.content.strip()
    
    return key_points

def compare_script_to_key_points(script, key_points):
    key_points_json = json.loads(key_points)
    feedbacks = []
    for key, value in key_points_json.items():
        for point in value:
            system_prompt_compare = f"""
            Guideline:{point}. 
            Keep all feedback concise and within 1 sentence. Don't hallucinate anything.
            If the script already follows the guideline, don't repeat the guideline
            """
            user_prompt_compare = f"""

            Script: {script}

            """

            prompt = [
                {"role": "system", "content": system_prompt_compare},
                {"role": "user", "content": user_prompt_compare}
            ]
            response_compare = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=prompt
            )
            feedback = response_compare.choices[0].message.content.strip()
            feedbacks.append(feedback)
    
    return feedbacks

def combine_feedback(feedbacks):
    feedback_combined_prompt = f"""
    Combine the following feedback messages into a single, cohesive feedback report. Ensure no information is repeated and put it into one paragraph.

    Feedbacks:
    {json.dumps(feedbacks, indent=2)}

    Output the combined feedback.
    """
    response_combined = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": feedback_combined_prompt}]
    )

    combined_feedback = response_combined.choices[0].message.content.strip()
    
    return combined_feedback


# endpoints for the first feedback generation system
# Endpoint to validate the creative brief
@app.post("/validate-brief")
async def validate_brief(brief: CreativeBrief):
    # Process the brief and extract key points
    key_points = extract_key_points(brief.brief)
    key_points_storage["key_points"] = key_points  # Store key points temporarily
    return {"valid": len(brief.brief.strip()) > 0, "key_points": key_points}

# Endpoint to generate feedback based on script
@app.post("/generate-feedback")
async def generate_feedback(script: Script):
    # Retrieve key points from temporary storage
    key_points = key_points_storage.get("key_points")
    if not key_points:
        return {"error": "Key points not found. Please validate the brief first."}
    
    # Compare the script with the stored key points
    feedback_list = compare_script_to_key_points(script.script, key_points)
    combined_feedback = combine_feedback(feedback_list)
    return {"feedback": combined_feedback}



# ENDPOINTS FOR THE SECOND FEEDBACK GENERATION SYSTEM
feedback_storage = {}


# Input Models
class FeedbackEntries(BaseModel):
    feedbacks: List[str]

class ScriptInput(BaseModel):
    script: str
    

# Endpoint to process multiple feedback entries
@app.post("/process-feedbacks")
async def process_feedbacks(feedback_entries: FeedbackEntries):
    consolidated = consolidate_feedbacks(feedback_entries.feedbacks)
    summarized = summarize_feedback(consolidated)
    feedback_storage["summarized_feedback"] = summarized
    return {"summarized_feedback": summarized}

# Endpoint to generate script feedback
@app.post("/generate-feedback-2")
async def generate_feedback_2(script_input: ScriptInput):
    summarized_feedback = feedback_storage.get("summarized_feedback")
    feedback = generate_feedback_2nd(script_input.script, summarized_feedback)
    return {"feedback": feedback}