from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Any
from datetime import datetime
import json
import os
import uvicorn
from math_utils import MathGenerator

app = FastAPI()

templates = Jinja2Templates(directory="templates")

if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- DATA MODELS ---

class QuizSummary(BaseModel):
    score_obtained: int
    total_questions: int
    percentage: float
    total_time_seconds: int

class QuestionResult(BaseModel):
    question_id: int
    question_text: str
    question_type: str
    category: str = "General"  # <--- NEW FIELD (Default ensures compatibility)
    user_answer: Any
    correct_answer: Any
    is_correct: bool
    time_spent: int

class QuizSubmission(BaseModel):
    summary: QuizSummary
    details: List[QuestionResult]

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
def quiz_view(request: Request):
    generator = MathGenerator()
    questions = generator.generate_all()
    
    for q in questions:
        if isinstance(q['correct_answer'], float):
            q['correct_answer'] = round(q['correct_answer'], 4)
            
    return templates.TemplateResponse("quiz.html", {"request": request, "questions": questions})

@app.get("/api/history")
def get_history():
    file_path = "results.json"
    if not os.path.exists(file_path):
        return {}
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        return {}

@app.post("/api/submit")
async def submit_quiz(submission: QuizSubmission):
    timestamp_key = datetime.now().strftime("%d-%m-%y-%H-%M")
    file_path = "results.json"
    db = {}
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                db = json.load(f)
        except json.JSONDecodeError:
            db = {}

    db[timestamp_key] = submission.model_dump()

    with open(file_path, "w") as f:
        json.dump(db, f, indent=4)

    return JSONResponse(content={"status": "success", "key": timestamp_key})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)