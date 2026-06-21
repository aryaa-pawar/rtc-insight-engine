import pandas as pd

df = pd.read_csv("data/processed/rtc_master_dataset.csv")

chunks = []
chunk_id = 1

for _, row in df.iterrows():

    report = row["report_name"]
    page = row["page_number"]
    text = str(row["text"])

    if text == "nan":
        continue

    paragraphs = text.split("\n")

    current_chunk = ""

    for para in paragraphs:

        para = para.strip()

        if not para:
            continue

        if len(current_chunk) + len(para) < 1000:
            current_chunk += " " + para

        else:

            chunks.append({
                "chunk_id": chunk_id,
                "report_name": report,
                "page_number": page,
                "chunk_text": current_chunk.strip()
            })

            chunk_id += 1
            current_chunk = para

    if current_chunk:

        chunks.append({
            "chunk_id": chunk_id,
            "report_name": report,
            "page_number": page,
            "chunk_text": current_chunk.strip()
        })

        chunk_id += 1

chunks_df = pd.DataFrame(chunks)

chunks_df.to_csv(
    "data/processed/rtc_chunks.csv",
    index=False
)

print(f"Total Smart Chunks: {len(chunks_df)}")
print(chunks_df.head())