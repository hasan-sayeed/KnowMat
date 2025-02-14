from src.knowmat.generate_allowed_properties import AllowedPropertiesGenerator
from src.knowmat.pdf_parser import PDFParser
from src.knowmat.pipeline import Pipeline


class JSONExtractor:
    """
    A class to extract structured data from PDF files and return it as a JSON-compatible format.
    """

    @staticmethod
    def extract(folder_path: str, properties_file: str) -> list:
        """
        Extract data from PDF files in a folder.

        Args:
            folder_path (str): Path to the folder containing PDF files.
            properties_file (str): Path to the JSON properties file.

        Returns:
            list: A list of extracted data in JSON-compatible format.
        """
        allowed_properties = AllowedPropertiesGenerator.generate_allowed_properties(
            properties_file
        )
        parsed_pdfs = PDFParser.parse_folder(folder_path)

        extracted_data = []
        for pdf in parsed_pdfs:
            try:
                data = Pipeline.run_pipeline(pdf["text"], allowed_properties)
                extracted_data.append({"file_name": pdf["file_name"], "data": data})
            except Exception as e:
                print(f"Error extracting data from {pdf['file_name']}: {e}")

        return extracted_data
