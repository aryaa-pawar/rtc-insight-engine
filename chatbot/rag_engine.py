import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    import google.generativeai as genai
except ImportError:
    genai = None


BASE_DIR = Path(__file__).resolve().parents[1]
FACTS_PATH = BASE_DIR / "data" / "processed" / "rtc_facts.txt"
CHUNKS_PATH = BASE_DIR / "data" / "processed" / "rtc_chunks.csv"

load_dotenv(BASE_DIR / ".env")


def _load_facts():
    if not FACTS_PATH.exists():
        return ""

    return FACTS_PATH.read_text(encoding="utf-8")


def _load_chunks():
    if not CHUNKS_PATH.exists():
        return pd.DataFrame(columns=["report_name", "page_number", "chunk_text"])

    df = pd.read_csv(CHUNKS_PATH)
    df["chunk_text"] = df["chunk_text"].fillna("").astype(str)
    return df


FACTS = _load_facts()
df = _load_chunks()

if len(df) > 0:
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["chunk_text"])
else:
    vectorizer = None
    X = None


def _get_model():
    api_key = os.getenv("GEMINI_API_KEY")

    if genai is None or not api_key:
        return None

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def _relevant_chunks(question, limit=8, threshold=0.03):
    if vectorizer is None or X is None or len(df) == 0:
        return []

    query_vector = vectorizer.transform([question])
    scores = cosine_similarity(query_vector, X).flatten()
    top_indices = scores.argsort()[-limit:][::-1]

    return [idx for idx in top_indices if scores[idx] > threshold]


def _build_context(indices):
    context_parts = []
    sources = []

    for idx in indices:
        row = df.iloc[idx]
        report_name = row.get("report_name", "RTC report")
        page_number = row.get("page_number", "N/A")
        chunk_text = row.get("chunk_text", "")

        context_parts.append(
            f"Report: {report_name}\n"
            f"Page: {page_number}\n"
            f"Text: {chunk_text}"
        )
        sources.append(f"{report_name} (Page {page_number})")

    return "\n\n".join(context_parts), sources


def _local_answer(question, indices):
    question_lower = question.lower()
    context, sources = _build_context(indices[:4])

    fact_terms = [
        "what is rtc",
        "stand for",
        "mission",
        "founder",
        "sue harnett",
        "what does rtc do",
        "members",
        "programs",
        "community"
    ]

    if any(term in question_lower for term in fact_terms):
        fact_lines = [line.strip() for line in FACTS.splitlines() if line.strip()]
        selected = []

        for line in fact_lines:
            line_lower = line.lower()
            if (
                "rtc stands for" in line_lower
                or "rewriting the code" in line_lower
                or "mission" in line_lower
                or "sue harnett" in line_lower
                or "women in technology" in line_lower
                or "members" in line_lower
                or "mentorship" in line_lower
                or "networking" in line_lower
                or "career development" in line_lower
                or "community" in line_lower
            ):
                selected.append(line)

            if len(selected) == 6:
                break

        return (
            " ".join(selected),
            ["RTC knowledge base"]
        )

    if context:
        snippets = []
        for idx in indices[:3]:
            text = str(df.iloc[idx]["chunk_text"]).strip()
            if len(text) > 360:
                text = text[:357].rsplit(" ", 1)[0] + "..."
            snippets.append(text)

        answer = "Here is what I found in the RTC reports: " + " ".join(snippets)
        return answer, sources

    return (
        "I could not find that information in the RTC reports or knowledge base.",
        []
    )


def ask_rtc(question):
    question = (question or "").strip()

    if not question:
        return {
            "answer": "Please enter a question about RTC reports, programs, recruiting, internships, or outcomes.",
            "sources": []
        }

    relevant_indices = _relevant_chunks(question)
    context, sources = _build_context(relevant_indices)

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

Use both the RTC facts and report information.
Answer naturally and professionally.
Write complete sentences.
Be conversational and helpful.
Combine information from multiple reports when useful.
Explain the meaning of statistics instead of simply repeating them.
Keep answers between 100 to 250 words unless the user explicitly asks for detailed information.
Never mention chunks, retrieval, or report extraction.
If information truly does not exist in either section, say:

I could not find that information in the RTC reports or knowledge base.

ANSWER:
"""

    model = _get_model()

    if model is None:
        answer, local_sources = _local_answer(question, relevant_indices)
        return {
            "answer": answer,
            "sources": local_sources or sources
        }

    try:
        response = model.generate_content(prompt)
        answer = getattr(response, "text", "").strip()

        if not answer:
            answer, local_sources = _local_answer(question, relevant_indices)
            return {
                "answer": answer,
                "sources": local_sources or sources
            }

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as exc:
        error_msg = str(exc)

        if "429" in error_msg or "quota" in error_msg.lower():
            answer, _ = _local_answer(question, relevant_indices)
            return {
                "answer": answer,
                "sources": sources or _build_context(relevant_indices[:4])[1]
            }

        answer, local_sources = _local_answer(question, relevant_indices)
        return {
            "answer": answer,
            "sources": local_sources or sources
        }
