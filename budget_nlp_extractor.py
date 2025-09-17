# budget_nlp_extractor.py

import pdfplumber
import spacy
from spacy.matcher import Matcher
import re
import os
import pandas as pd

# ----------------------
# CONFIGURATION
# ----------------------
PDF_FOLDER = "budget"          # Folder containing budget PDFs
OUTPUT_FOLDER = "output_csv" # Folder to save CSVs
KEY_TERMS = ["GDP", "inflation", "deficit", "government expenditure", 
             "tax revenue", "public debt", "fiscal deficit", "revenue collection"]

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ----------------------
# LOAD NLP MODEL
# ----------------------
nlp = spacy.load("en_core_web_sm")

# ----------------------
# SPAcy MATCHER SETUP
# ----------------------
matcher = Matcher(nlp.vocab)
for term in KEY_TERMS:
    pattern = [{"LOWER": token.lower()} for token in term.split()]
    matcher.add(term.upper(), [pattern])

# ----------------------
# FUNCTIONS
# ----------------------
def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF using pdfplumber."""
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"
    return all_text

def extract_tables_from_pdf(pdf_path):
    """Extract all tables from a PDF into a list of DataFrames."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df)
    return tables

def extract_sentences_with_terms(text):
    """Extract sentences containing key budget terms."""
    doc = nlp(text)
    matches = matcher(doc)
    results = {term: [] for term in KEY_TERMS}
    for match_id, start, end in matches:
        span = doc[start:end]
        sentence = span.sent.text.strip()
        # Map to original key term (case-insensitive match)
        for term in KEY_TERMS:
            if span.text.lower() == term.lower():
                results[term].append(sentence)
    return results

def extract_numbers_around_terms(text, terms):
    """Extract numeric values (percentages or numbers) near key terms."""
    data = {}
    for term in terms:
        # Match patterns like "GDP is 3.5%" or "deficit of K10 billion"
        pattern = rf"{term}\s*(?:is|was|projected|estimated|of|at)?\s*([\d,.]+%?)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        data[term] = matches
    return data

def process_pdf(pdf_path):
    """Process a single PDF and return structured data."""
    filename = os.path.basename(pdf_path)
    print(f"Processing {filename}...")

    # Extract text and tables
    text = extract_text_from_pdf(pdf_path)
    tables = extract_tables_from_pdf(pdf_path)

    # NLP extraction
    sentences = extract_sentences_with_terms(text)
    numbers = extract_numbers_around_terms(text, KEY_TERMS)

    # Save tables to CSV
    for i, table in enumerate(tables):
        table_csv_path = os.path.join(OUTPUT_FOLDER, f"{filename}_table_{i+1}.csv")
        table.to_csv(table_csv_path, index=False)

    # Save sentences and numbers to CSV
    sentences_df = pd.DataFrame([(k, s) for k, v in sentences.items() for s in v],
                                columns=["Term", "Sentence"])
    numbers_df = pd.DataFrame([(k, n) for k, v in numbers.items() for n in v],
                              columns=["Term", "Value"])

    sentences_csv_path = os.path.join(OUTPUT_FOLDER, f"{filename}_sentences.csv")
    numbers_csv_path = os.path.join(OUTPUT_FOLDER, f"{filename}_numbers.csv")

    sentences_df.to_
