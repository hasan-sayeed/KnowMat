import os

import fitz  # PyMuPDF


class PDFParser:
    """
    A class for parsing PDFs and removing 'References' sections.
    """

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """
        Parse a PDF, remove the 'References' section, and return the cleaned text.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: The cleaned text from the PDF without the 'References' section.
        """
        doc = fitz.open(file_path)
        references_found = False
        extracted_text = ""

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text()

            # If "References" is found, stop extracting further text
            if "References" in page_text and not references_found:
                references_found = True
                break

            extracted_text += page_text + "\n"

        doc.close()
        return extracted_text.strip()

    @staticmethod
    def parse_folder(folder_path: str) -> list:
        """
        Parse all PDFs in a folder and its subfolders, removing 'References'.

        Args:
            folder_path (str): Path to the folder containing PDFs.

        Returns:
            list: List of dictionaries with file names and cleaned text.
        """
        parsed_papers = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    try:
                        cleaned_text = PDFParser.parse_pdf(file_path)
                        parsed_papers.append({"file_name": file, "text": cleaned_text})
                        # print(f"Processed: {file}")
                    except Exception as e:
                        print(f"Error processing {file}: {e}")
        return parsed_papers
