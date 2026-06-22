import pandas as pd
import mysql.connector

# ------------------------
# Read CSV
# ------------------------

df = pd.read_csv(
    "data/processed/rtc_business_metrics.csv"
)

print(df.head())

# ------------------------
# MySQL Connection
# ------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="arya123",
    database="rtc_db"
)

cursor = conn.cursor()

# ------------------------
# Insert Records
# ------------------------

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO business_metrics
        (year, category, metric_name, metric_value)
        VALUES (%s, %s, %s, %s)
        """,
        (
            int(row["year"]),
            row["category"],
            row["metric_name"],
            float(row["metric_value"])
        )
    )

conn.commit()

print(f"{len(df)} rows loaded successfully!")

cursor.close()
conn.close()