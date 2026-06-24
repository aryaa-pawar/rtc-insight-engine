import os
import pandas as pd
import google.generativeai as genai

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# GEMINI SETUP
# =====================================================
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# =====================================================
# LOAD RTC DATA
# =====================================================

print("Loading RTC Knowledge Base...")

df = pd.read_csv("data/processed/rtc_chunks.csv")

print(f"Loaded {len(df)} chunks")

# =====================================================
# BUILD TF-IDF INDEX
# =====================================================

print("Building Search Index...")

vectorizer = TfidfVectorizer(
    stop_words="english"
)

X = vectorizer.fit_transform(
    df["chunk_text"]
)

print("RTC Chatbot Ready!")
print("Type 'exit' to quit.\n")

# =====================================================
# CHAT LOOP
# =====================================================

while True:

    question = input("Ask RTC: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    # -----------------------------------------
    # Search Relevant Chunks
    # -----------------------------------------

    query_vector = vectorizer.transform(
        [question]
    )

    scores = cosine_similarity(
        query_vector,
        X
    ).flatten()

    top_indices = scores.argsort()[-5:][::-1]

    relevant_chunks = []

    for idx in top_indices:
        if scores[idx] > 0.05:
            relevant_chunks.append(idx)

    # -----------------------------------------
    # No Relevant Results
    # -----------------------------------------

    if len(relevant_chunks) == 0:

        print("\nAnswer:")
        print(
            "I could not find that information "
            "in the RTC reports."
        )
        print("\n" + "=" * 80 + "\n")

        continue

    # -----------------------------------------
    # Build Context
    # -----------------------------------------

    context = ""

    for idx in relevant_chunks:

        context += (
            f"Report: {df.iloc[idx]['report_name']}\n"
            f"Page: {df.iloc[idx]['page_number']}\n"
            f"Text: {df.iloc[idx]['chunk_text']}\n\n"
        )

    # -----------------------------------------
    # Gemini Prompt
    # -----------------------------------------

    prompt = f"""
You are an AI assistant for Rewriting The Code (RTC).

Answer questions ONLY using the information
provided in the context below.

Rules:

1. Give concise answers.
2. Use bullet points when appropriate.
3. If the answer is partially available,
   provide the best answer possible.
4. Do not invent information.
5. If the answer is not present in the context,
   respond exactly with:

I could not find that information in the RTC reports.

CONTEXT:

{context}

QUESTION:

{question}
"""

    # -----------------------------------------
    # Generate Answer
    # -----------------------------------------

    try:

        response = model.generate_content(
            prompt
        )

        print("\nAnswer:\n")
        print(response.text)

        print("\nSources:")

        for idx in relevant_chunks:

            print(
                f"- {df.iloc[idx]['report_name']} "
                f"(Page {df.iloc[idx]['page_number']})"
            )

        print("\n" + "=" * 80 + "\n")

    except Exception as e:

        print("\nError:")
        print(str(e))
        print("\n" + "=" * 80 + "\n")