import os

import streamlit as st
from json_extractor import JSONExtractor
from response_parser import ResponseParser

st.title("Materials Science Data Extractor")

uploaded_files = st.file_uploader(
    "Upload PDFs", accept_multiple_files=True, type=["pdf"]
)
properties_file = st.text_input("Path to Properties JSON File")
output_path = st.text_input("Output Folder Path")
output_file_name = st.text_input("Output File Name (e.g., extracted_data.csv)")

if st.button("Extract Data"):
    if uploaded_files and properties_file and output_path and output_file_name:
        # Save uploaded files locally
        temp_folder = "temp_pdfs"
        os.makedirs(temp_folder, exist_ok=True)
        for file in uploaded_files:
            with open(f"{temp_folder}/{file.name}", "wb") as f:
                f.write(file.getbuffer())

        # Extract data
        extracted_data = JSONExtractor.extract(temp_folder, properties_file)

        # Save to CSV
        ResponseParser.save_to_csv(extracted_data, output_path, output_file_name)
        st.success("Data extraction complete!")
    else:
        st.error("Please provide all inputs.")
