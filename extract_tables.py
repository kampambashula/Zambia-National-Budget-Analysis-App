import os
import pdfplumber
import pandas as pd

# Paths
PDF_DIR = "budget"
CSV_DIR = "csv_output"

os.makedirs(CSV_DIR, exist_ok=True)

def extract_tables_from_pdf(pdf_file, output_dir=CSV_DIR):
    """Extract tables from a budget speech PDF and save them to CSV."""
    pdf_path = os.path.join(PDF_DIR, pdf_file)
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return

    try:
        with pdfplumber.open(pdf_path) as pdf:
            table_count = 0
            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        table_count += 1
                        csv_filename = f"{os.path.splitext(pdf_file)[0]}_table{table_count}.csv"
                        csv_path = os.path.join(output_dir, csv_filename)
                        df.to_csv(csv_path, index=False)
                        print(f"✅ Saved table {table_count} from page {page_num} → {csv_filename}")

        if table_count == 0:
            print(f"⚠️ No tables found in {pdf_file}")
    except Exception as e:
        print(f"❌ Error processing {pdf_file}: {e}")

def batch_extract():
    """Extract tables from all PDFs in the data folder."""
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            print(f"\n📄 Processing {file}...")
            extract_tables_from_pdf(file)

if __name__ == "__main__":
    batch_extract()
