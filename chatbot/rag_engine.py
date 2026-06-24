import os
import pandas as pd
import google.generativeai as genai

from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#LOAD ENVIRONMENT VARIABLES

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


#GEMINI MODEL


model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


#LOAD FACTS FILE

with open(
    "data/processed/rtc_facts.txt",
    "r",
    encoding="utf-8"
) as f:
    FACTS = f.read()

#LOAD RTC REPORT CHUNKS


df = pd.read_csv(
    "data/processed/rtc_chunks.csv"
)


#BUILD SEARCH INDEX


vectorizer = TfidfVectorizer(
    stop_words="english"
)

X = vectorizer.fit_transform(
    df["chunk_text"]
)


#MAIN FUNCTION

def ask_rtc(question):
    query_vector = vectorizer.transform(
        [question]
    )

    scores = cosine_similarity(
        query_vector,
        X
    ).flatten()

    top_indices = scores.argsort()[-8:][::-1]

    relevant_chunks = []

    for idx in top_indices:

        if scores[idx] > 0.03:

            relevant_chunks.append(idx)

    context = ""

    sources = []

    for idx in relevant_chunks:

        context += (
            f"Report: {df.iloc[idx]['report_name']}\n"
            f"Page: {df.iloc[idx]['page_number']}\n"
            f"Text: {df.iloc[idx]['chunk_text']}\n\n"
        )

        sources.append(
            f"{df.iloc[idx]['report_name']} "
            f"(Page {df.iloc[idx]['page_number']})"
        )

    prompt = f"""

You are RTC Assistant.

RTC stands for Rewriting The Code.

GENERAL RTC FACTS:

{FACTS}

REPORT INFORMATION:

{context}

QUESTION:

{question}

INSTRUCTIONS:

Use BOTH the RTC facts and report information.
Answer naturally and professionally.
Write complete sentences.
Be conversational and helpful.
Combine information from multiple reports when useful.
Explain the meaning of statistics instead of simply repeating them.

If the question asks about:

Founder
Mission
History
What RTC is
What RTC stands for

use the RTC FACTS section.

If the question asks about:

Programs
Members
Growth
Metrics
Outcomes
Recruiting
Community impact

use the REPORT INFORMATION section.

Keep answers between 100 to 250 words unless the user explicitly asks for detailed information.

For simple questions, provide concise answers.

For analytical or report-related questions, provide detailed answers.

Never mention chunks, retrieval, or report extraction.
If information truly does not exist in either section, say:

I could not find that information in the RTC reports or knowledge base.

STYLE:

Professional
Friendly
Website-ready
Clear and concise

ANSWER:
"""
    
    try:
        response = model.generate_content(
            prompt
        )
        return {
            "answer": response.text,
            "sources": sources
        }
    except Exception as e:
        error_msg = str(e)

    if "429" in error_msg or "quota" in error_msg.lower():

        return {
            "answer":
            "The AI service is temporarily busy. Please wait about a minute and try again.",
            "sources": sources
        }

    return {
        "answer": f"ERROR: {error_msg}",
        "sources": []
    }
