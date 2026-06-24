import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/processed/rtc_chunks.csv")

print("Building search index...")

vectorizer = TfidfVectorizer(stop_words="english")

X = vectorizer.fit_transform(df["chunk_text"])

print("Ready!")

while True:

    query = input("\nAsk a question (or exit): ")

    if query.lower() == "exit":
        break

    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(
        query_vector,
        X
    ).flatten()

    top_indices = scores.argsort()[-3:][::-1]

    print("\nTop Matches:\n")

    for idx in top_indices:

        print("=" * 80)
        print("Report:", df.iloc[idx]["report_name"])
        print("Page:", df.iloc[idx]["page_number"])
        print("Score:", round(scores[idx], 3))
        print()
        print(df.iloc[idx]["chunk_text"][:500])
        print()