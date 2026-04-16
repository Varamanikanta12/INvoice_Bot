from unstructured.partition.pdf import partition_pdf
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import json
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")


llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=api_key
)


def extract_text(file_path):
   
    elements = partition_pdf(filename=file_path, strategy="hi_res")

    text = ""
    for el in elements:
        if el.text:
            text += el.text + "\n"

    print("Text extracted...")
    return text



def get_structured_data(text):
    
    text = text[:4000]

    prompt = f"""
Extract invoice details.

Return ONLY valid JSON. No explanation.

Format:
{{
  "items": [{{"description": "", "amount": number}}],
  "base_amount": number,
  "grand_total": number
}}

Invoice:
{text}
"""

    res = llm.invoke([HumanMessage(content=prompt)])

    raw = res.content.strip()

    try:
        
        start = raw.find("{")
        end = raw.rfind("}") + 1
        clean_json = raw[start:end]

        data = json.loads(clean_json)

        print("Structured data ready")
        return data

    except Exception as e:
        print("JSON parsing failed:", e)
        return {"error": raw}
