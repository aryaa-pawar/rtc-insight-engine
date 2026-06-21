import pdfplumber
import pandas as pd
from pathlib import Path

pdf_folder = Path("data/raw_pdfs")
output_folder = Path("data/processed")

output_folder.mkdir(exist_ok=True)

for pdf_file in pdf_folder.glob("*.pdf"):

    all_pages = []

    print(f"Processing {pdf_file.name}")

    with pdfplumber.open(pdf_file) as pdf:

        for page_num, page in enumerate(pdf.pages, start=1):

            text = page.extract_text()

            all_pages.append({
                "page_number": page_num,
                "text": text if text else ""
            })

    df = pd.DataFrame(all_pages)

    output_file = output_folder / f"{pdf_file.stem}.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved -> {output_file}")