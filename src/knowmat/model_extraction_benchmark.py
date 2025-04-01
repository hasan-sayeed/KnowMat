import os

from src.knowmat.json_extractor import JSONExtractor
from src.knowmat.post_processing import PostProcessor
from src.knowmat.response_parser import ResponseParser


def extract_knowmat_from_pdfs(
    model_name: str,
    pdf_folder_path: str,
    output_csv_path: str,
    output_csv_name: str,
    properties_json_path: str = "src/knowmat/properties.json",
):
    """
    Extracts structured materials science data from PDFs using the KnowMat pipeline.

    Args:
        model_name (str): LLM model name (e.g., 'llama3.2:3b-instruct-fp16').
        pdf_folder_path (str): Path to folder containing PDF files.
        output_csv_path (str): Folder where CSV should be saved.
        output_csv_name (str): Name of the CSV file.
        properties_json_path (str): Path to the properties.json file (default is inside src/knowmat).
    """
    if not os.path.isdir(pdf_folder_path):
        raise ValueError(f"PDF folder not found: {pdf_folder_path}")
    if not os.path.exists(output_csv_path):
        os.makedirs(output_csv_path, exist_ok=True)

    # 1. Extract raw structured data using the PDF parser + pipeline
    print("🔍 Extracting data from PDFs...")
    extracted_result = JSONExtractor.extract(pdf_folder_path, model_name)

    # 2. Save extracted data to CSV
    print("📁 Saving raw extracted data to CSV...")
    ResponseParser.save_to_csv(extracted_result, output_csv_path, output_csv_name)

    # 3. Post-process the CSV file (e.g., match property names to standard ones)
    print("🔧 Post-processing CSV with property mapping...")
    processor = PostProcessor(
        properties_json_path, os.path.join(output_csv_path, output_csv_name)
    )
    processor.process_extracted_data()

    # 4. Update the JSON result as well with post-processed fields
    updated_result = processor.update_extracted_json(extracted_result)

    print("✅ Extraction complete.")
    return updated_result  # You can optionally inspect the structured data returned


def main():
    models_to_test = [
        "llama3.1:8b-instruct-fp16",
        "llama3.2:3b-instruct-fp16",
        "llama3.3:70b-instruct-fp16",
    ]

    pdfs_dir = "data/interim"
    csv_save_path = "data/processed"
    num_runs = 5  # You can change this to test more or fewer times

    for model in models_to_test:
        model_safe_name = model.replace(":", "_").replace(".", "_").replace("-", "_")
        for run in range(1, num_runs + 1):
            csv_file_name = f"extracted_{model_safe_name}_run{run}.csv"
            print(f"\n🚀 Running extraction with model: {model} (Run {run}/{num_runs})")
            extract_knowmat_from_pdfs(model, pdfs_dir, csv_save_path, csv_file_name)


if __name__ == "__main__":
    main()
