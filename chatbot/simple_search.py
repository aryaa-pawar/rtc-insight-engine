import pandas as pd

df = pd.read_csv("data/processed/rtc_chunks.csv")

while True:
    query = input("\nAsk a question (or type exit): ")

    if query.lower() == "exit":
        break

    results = df[
        df["chunk_text"].str.contains(
            query,
            case=False,
            na=False
        )
    ]

    if len(results) == 0:
        print("\nNo matches found.")
    else:
        print("\nTop Results:\n")

        for _, row in results.head(3).iterrows():
            print("=" * 80)
            print("Report:", row["report_name"])
            print("Page:", row["page_number"])
            print()
            print(row["chunk_text"][:500])
            print()