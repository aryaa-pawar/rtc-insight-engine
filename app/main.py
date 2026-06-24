from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from chatbot.rag_engine import ask_rtc

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)

class Question(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/ask")
def ask(question: Question):

    try:
        return ask_rtc(
            question.question
        )
    except Exception:
        return {
            "answer": "I could not process that question right now. Please try another RTC question.",
            "sources": []
        }
