import pandas as pd
from pathlib import Path

processed = Path("data/processed")

report_files = [
    "RTC_Impact_Report_2023.csv",
    "RTC_Impact_Report_2024.csv",
    "RTC_Impact_Report_2025.csv",
    "RTC_Internship_Report_2024.csv",
    "RTC_Recruiting_Report_2025.csv",
    "RTC-Impact-Report-2023-Press-Release.csv"
]

all_dfs = []

for file in report_files:

    file_path = processed / file

    if not file_path.exists():
        print(f"Missing: {file}")
        continue

    df = pd.read_csv(file_path)

    df["report_name"] = file.replace(".csv", "")

    all_dfs.append(df)

master = pd.concat(all_dfs, ignore_index=True)

master.to_csv(
    processed / "rtc_master_dataset.csv",
    index=False
)

print("\nShape:")
print(master.shape)

print("\nReports:")
print(master["report_name"].value_counts())