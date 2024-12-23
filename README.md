# Script Feedback Application

View the live application [here](https://brand-script-feedback.vercel.app).

This project contains both the frontend (Next.js) and backend (FastAPI) for the Script Feedback application. 

## Structure

- `/script-feedback-app`: Contains the Next.js application
- `/backend`: Contains the FastAPI backend powering it

## About the project
Aim was to develop a feedback generation system for video scripts. The crux of the system was extracting key points to look out for when generating feedback. To do this, two methods were attempted.
1. Extracting the key points from a Creator Brief document.
2. Extracting key points from client's history of feedbacks given to other partners.

### Feedback Generator 1: Using the creative brief document
1. Client submits their creative brief.
   1. `extract_key_points(brief_guidelines)`: extracts all the key points to check for when evaluating the script.
2. Chained LLM prompting for processing. Refer to [main.py](backend/main.py).
   1. `compare_script_to_key_points(script, key_points)`: uses each key point as a prompt to generate feedback for each point
   2. `combine_feedback`: generates a cohesive feedback message based on all the key point feedbacks

This method performed better in producing feedback, but did not quite nail the approval rejection process.

### Feedback Generator 2: Using the client's history of feedbacks
1. Client can add up to 10 previous feedback messages they have previously given.
   1. For each message:
    1. `split_feedback(feedback)`: splits the feedback message into different components to isolate the feedback relevant to the script.
    2. `extract_script_key_points_2(splits["script_feedback"], splits["decision"])`: extract key script feedback points from that message, together with the final decision to approve or rejects
2. Processing all feedback messages together. Refer to [main.py](backend/main.py) and [feedback_processors_2.py](backend/feedback_processors_2.py)
   1. `consolidate_feedback and summarize_feedback`: put all feedback together, simplify it to remove repetitions and make it more concise
   2. `generate_feedback_2`: generates a cohesive feedback message for the script based on the summarised feedback key points

This method needs a bit more prompt engineering to use the LLM to more effectively realise what the client is looking for, rather than getting too specific. Again, the approval and rejection process did not perform well so it was omitted from the final result.

### Information for you to test out the webapp
Check [web-app-test.md](web-app-test.md).


### Testing and debugging
Refer to [experimentation.ipynb](experimentation.ipynb) for some demonstrations.




## Setup and Development

### Frontend

1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

### Backend

1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the development server: `uvicorn main:app --reload`

## Deployment

- Frontend: Deployed to Vercel
- Backend: Deployed to Render

Remember to set the appropriate environment variables for both frontend and backend deployments.
