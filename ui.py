import streamlit as st
import requests

st.title("SAP Invoice AI System")

uploaded_file = st.file_uploader("Upload Invoice PDF", type=["pdf"])

if uploaded_file:
    st.write("Processing...")

    try:
        response = requests.post(
            "http://127.0.0.1:8000/process",
            files={"file": uploaded_file}
        )

        result = response.json()

        st.subheader("Result")
        st.json(result)
        

    except Exception as e:
        st.error(f"Error: {e}")
