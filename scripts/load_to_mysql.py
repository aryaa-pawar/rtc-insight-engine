import pandas as pd
import mysql.connector

# -------------------------
# MySQL Connection
# -------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="arya123",
    database="rtc_db"
)

cursor = conn.cursor()

# -------------------------
# Load Reports
# -------------------------

reports_df = pd.read_csv(
    "data/processed/rtc_master_dataset.csv"
)

for _, row in reports_df.iterrows():

    cursor.execute(
        """
        INSERT INTO reports
        (report_name, page_number, text_content)
        VALUES (%s, %s, %s)
        """,
        (
            row["report_name"],
            int(row["page_number"]),
            str(row["text"])
        )
    )

conn.commit()

print(f"Loaded Reports: {len(reports_df)}")

# -------------------------
# Load Chunks
# -------------------------

chunks_df = pd.read_csv(
    "data/processed/rtc_chunks.csv"
)

for _, row in chunks_df.iterrows():

    cursor.execute(
        """
        INSERT INTO chunks
        (chunk_id, report_name, page_number, chunk_text)
        VALUES (%s, %s, %s, %s)
        """,
        (
            int(row["chunk_id"]),
            row["report_name"],
            int(row["page_number"]),
            str(row["chunk_text"])
        )
    )

conn.commit()

print(f"Loaded Chunks: {len(chunks_df)}")

# -------------------------
# Load Metrics
# -------------------------

metrics_df = pd.read_csv(
    "data/processed/rtc_metrics.csv"
)

for _, row in metrics_df.iterrows():

    cursor.execute(
        """
        INSERT INTO metrics
        (report_name, page_number, metric_value, metric_description)
        VALUES (%s, %s, %s, %s)
        """,
        (
            row["report"],
            int(row["page"]),
            str(row["metric_value"]),
            str(row["metric_description"])
        )
    )

conn.commit()

print(f"Loaded Metrics: {len(metrics_df)}")

cursor.close()
conn.close()

print("\nData Loaded Successfully!")