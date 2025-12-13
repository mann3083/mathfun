from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from math_utils import MathGenerator
import uvicorn
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static files if needed (e.g., for custom JS/CSS)
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    generator = MathGenerator()
    questions = generator.generate_all()
    # Hide correct answers from user, but pass them for JS validation
    for q in questions:
        if isinstance(q['correct_answer'], float):
            q['correct_answer'] = round(q['correct_answer'], 4)
    return templates.TemplateResponse("index.html", {"request": request, "questions": questions})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
