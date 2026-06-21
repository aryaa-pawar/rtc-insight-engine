import pandas as pd
import re

df = pd.read_csv("data/processed/rtc_master_dataset.csv")

records = []

# Look only at impact reports for now
impact_reports = [
    "RTC_Impact_Report_2024",
    "RTC_Impact_Report_2025"
]

for _, row in df.iterrows():

    if row["report_name"] not in impact_reports:
        continue

    text = str(row["text"])

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for i, line in enumerate(lines):

        # Match percentages
        if re.fullmatch(r"\d+(\.\d+)?%", line):

            description = ""

            for j in range(i + 1, min(i + 4, len(lines))):
                description += " " + lines[j]

            records.append({
                "report": row["report_name"],
                "page": row["page_number"],
                "metric_value": line,
                "metric_description": description.strip()
            })

        # Match comma-separated numbers
        elif re.fullmatch(r"\d{1,3}(,\d{3})+", line):

            description = ""

            for j in range(i + 1, min(i + 4, len(lines))):
                description += " " + lines[j]

            records.append({
                "report": row["report_name"],
                "page": row["page_number"],
                "metric_value": line,
                "metric_description": description.strip()
            })

result = pd.DataFrame(records)

result.to_csv(
    "data/processed/named_metrics.csv",
    index=False
)

print(f"Metrics extracted: {len(result)}")
print(result.head(20))