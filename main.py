from fastapi import FastAPI, UploadFile, File
import shutil
import json

from extractor import extract_text, get_structured_data
from validator import validate_invoice

app = FastAPI()

import json
import os

def load_po():
    base_dir = os.path.dirname(__file__)   # gets current folder
    file_path = os.path.join(base_dir, "po.json")  # full path

    with open(file_path, "r") as f:
        content = f.read()
        print("DEBUG CONTENT:", content)   
        return json.loads(content)


@app.post("/process")
async def process(file: UploadFile = File(...)):
    content = await file.read()

    invoice_data = extract_invoice(content)

    print("INVOICE DATA:", invoice_data)   

    po_data = load_po()

    errors = validate_invoice(invoice_data, po_data)

    return {"status": "FAILED" if errors else "SUCCESS", "errors": errors}
