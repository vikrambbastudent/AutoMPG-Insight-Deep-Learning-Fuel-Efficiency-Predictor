import os, re, io, pdfplumber, pytesseract, pandas as pd
from PIL import Image

PDF_DIR      = r"C:\Users\HP\Downloads\IOAGPL NOVEMBER 16-31 2025"
OUTPUT_CSV   = "IOAGPL_invoices_NovemberSFN.csv"

# ---------- Regex patterns (two‑way) ----------
RX_INV   = re.compile(r"(?:Invoice\s*No\.?\s*[:\-]?\s*|)(\d{7,})\s*(?:Invoice\s*No\.?|)", re.I)
RX_DATE  = re.compile(r"\bDate\s*[:\-]?\s*(\d{2}[./-]\d{2}[./-]\d{4})", re.I)

# --- NEW, MORE ROBUST REGEX FOR THE LINE ITEM ---
# This single regex captures the rate (group 1) and quantity (group 2) at the same time.
# It looks for the pattern: [number] [number] KG, which is how the data appears in the table.
# This is much more reliable than trying to match the header text.
RX_LINE_ITEM = re.compile(r"([\d\.,]+)\s+([\d,]+(?:\.\d+)?)\s+KG", re.I)

RX_VAL   = re.compile(r"Assessable\s*Value\s*[:\-]?\s*([\d,]+\.\d{2})", re.I)

def ocr_page(page) -> str:
    """OCR a pdfplumber page → text (slow, only if needed)."""
    image = Image.open(io.BytesIO(page.to_image(resolution=300).original))
    return pytesseract.image_to_string(image, lang="eng")

def extract_fields(text: str) -> dict:
    """Return dict with invoice_no, date, quantity, assess_value (or None)."""
    inv  = RX_INV.search(text)
    dat  = RX_DATE.search(text)
    line_item = RX_LINE_ITEM.search(text) # Use the new combined regex
    val  = RX_VAL.search(text)

    def clean_num(x):
        return float(x.replace(',', '')) if x else None

    # Extract rate and quantity from the new regex match
    rate = line_item.group(1) if line_item else None
    qty = line_item.group(2) if line_item else None

    # Add the fields to the output dictionary
    return {
        "invoice_no"       : inv.group(1) if inv else None,
        "date"             : dat.group(1) if dat else None,
        "rate_per_kg"      : clean_num(rate),
        "quantity_kg"      : clean_num(qty),
        "assessable_value" : clean_num(val.group(1)) if val else None,
    }

records = []

# Make sure the PDF_DIR exists before trying to list its contents
if not os.path.isdir(PDF_DIR):
    print(f"Error: Directory not found at {PDF_DIR}")
else:
    for pdf_name in os.listdir(PDF_DIR):
        if not pdf_name.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(PDF_DIR, pdf_name)
        full_text = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # Using a small tolerance can help with layout issues
                    txt = page.extract_text(x_tolerance=2) or ""
                    if not txt.strip(): # if scanned, OCR it
                        txt = ocr_page(page)
                    full_text.append(txt)
        except Exception as e:
            print(f"Error processing {pdf_name}: {e}")
            continue

        merged_text = "\n".join(full_text)
        data = extract_fields(merged_text)
        data["filename"] = pdf_name
        records.append(data)

    # --------- Save to CSV ---------
    if records:
        df = pd.DataFrame(records)
        # Reorder columns for clarity and add the new rate_per_kg column
        df = df[["filename", "invoice_no", "date", "rate_per_kg", "quantity_kg", "assessable_value"]]
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Finished.  CSV saved as: {OUTPUT_CSV}")
        print(df.head())
    else:
        print("No PDF files found or processed in the directory.")