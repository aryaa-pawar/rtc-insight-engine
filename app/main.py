from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from chatbot.rag_engine import ask_rtc

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>

<head>

    <title>RTC Insight Engine</title>

    <style>

        body{
            font-family:Arial;
            max-width:1200px;
            margin:auto;
            padding:20px;
            background:#f5f5f5;
        }

        iframe{
            width:100%;
            height:700px;
            border:none;
            background:white;
        }

        .card{
            background:white;
            padding:20px;
            border-radius:12px;
            margin-top:20px;
        }

        input{
            width:70%;
            padding:12px;
            font-size:16px;
        }

        button{
            padding:12px;
            cursor:pointer;
        }

        #response{
            margin-top:20px;
            line-height:1.7;
        }

    </style>

</head>

<body>

    <h1>RTC Insight Engine</h1>

    <div class="card">

        <h2>RTC Dashboard</h2>

        <iframe
        src="PASTE_LOOKER_EMBED_URL_HERE">
        </iframe>

    </div>

    <div class="card">

        <h2>RTC AI Assistant</h2>

        <input
        id="question"
        type="text"
        placeholder="Ask anything about RTC..."
        >

        <button
        onclick="askRTC()">
        Ask
        </button>

        <div id="response"></div>

    </div>

    <script>

    async function askRTC(){

        let question =
        document.getElementById(
            "question"
        ).value;

        document.getElementById(
            "response"
        ).innerHTML =
        "<p>Thinking...</p>";

        let response =
        await fetch(
            "/ask",
            {
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({
                    question:question
                })
            }
        );

        let data =
        await response.json();

        document.getElementById(
            "response"
        ).innerHTML =

        "<h3>Answer</h3>" +

        "<p>" +
        data.answer +
        "</p>" +

        "<h4>Sources</h4>" +

        "<p>" +
        data.sources.join("<br>") +
        "</p>";
    }

    </script>

</body>

</html>
"""

@app.post("/ask")
def ask(question: Question):

    result = ask_rtc(
        question.question
    )

    print("\nRESULT:")
    print(result)

    return result