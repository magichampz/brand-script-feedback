# Script Feedback Application

This project contains both the frontend (Next.js) and backend (FastAPI) for the Script Feedback application.

## Structure

- `/frontend`: Contains the Next.js application
- `/backend`: Contains the FastAPI application

## Setup

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

- Frontend: Deploy to Vercel
- Backend: Deploy to Render

Remember to set the appropriate environment variables for both frontend and backend deployments.