from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def home():
    html = """
<!DOCTYPE html>
<html>

<head>
    <title>RTC Insight Engine</title>
</head>

<body>

    <h1>RTC Insight Engine</h1>

    <h2>RTC Dashboard</h2>

    <p>Looker Studio Dashboard will go here</p>

    <hr>

    <h2>RTC AI Assistant</h2>

    <input
        id="question"
        type="text"
        placeholder="Ask RTC..."
        style="width:400px;padding:10px;"
    >

    <button onclick="askRTC()">
        Ask
    </button>

    <div id="response"></div>

    <script>

    async function askRTC() {

        let question =
        document.getElementById("question").value;

        let response =
        await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        let data =
        await response.json();

        document.getElementById("response").innerHTML =
        "<h3>Answer</h3><p>" +
        data.answer +
        "</p>";
    }

    </script>

</body>

</html>
"""
    return html

@app.post("/ask")
def ask(question: Question):

    return {
    "answer":
    "RTC chatbot connection successful. Gemini will be connected next."
}