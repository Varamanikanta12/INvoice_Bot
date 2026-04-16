from unstructured.partition.pdf import partition_pdf
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import json


llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)


def extract_text(file_path):
    
    elements = partition_pdf(filename=file_path, strategy="hi_res")

    text = ""
    for el in elements:
        if el.text:
            text += el.text + "\n"

    print("Text extracted...")
    return text
def get_structured_data(text):
    
    prompt = f"""
Extract invoice details.

Return JSON only:
{{
  "items": [{{"description": "", "amount": number}}],
  "base_amount": number,
  "grand_total": number
}}

Invoice:
{text}
"""

    res = llm.invoke([HumanMessage(content=prompt)])

    try:
        data = json.loads(res.content)
        print("Structured data ready")
        return data
    except:
        print("JSON parsing failed")
        return {"error": res.content}

