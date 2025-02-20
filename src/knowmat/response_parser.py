import os

import pandas as pd


class ResponseParser:
    """
    A class to parse the LLM response and save it to a CSV file.
    """

    @staticmethod
    def save_to_csv(data: list, output_path: str, file_name: str) -> None:
        """
        Save the extracted data to a CSV file. Append extracted data to a CSV file if it
        exists; otherwise, create a new file.

        Args:
            data (list): Extracted data.
            output_path (str): Path to save the CSV file.
            file_name (str): Name of the CSV file.
        """
        file_path = os.path.join(output_path, file_name)
        file_exists = os.path.exists(file_path)

        rows = []
        for entry in data:
            for comp in entry["data"].compositions:
                for prop in comp.properties_of_composition:
                    rows.append(
                        [
                            entry["file_name"],  # Store file name for reference
                            comp.composition,
                            comp.processing_conditions,  # Processing conditions
                            comp.characterization,
                            prop.property_name,
                            prop.value,
                            prop.unit,
                            prop.measurement_condition,
                        ]
                    )

        # Convert to DataFrame
        new_data_df = pd.DataFrame(
            rows,
            columns=[
                "file name",
                "composition",
                "processing condition",
                "characterization",
                "property name",
                "value",
                "unit",
                "measurement condition",
            ],
        )

        # If the file already exists, append new data
        if file_exists:
            existing_df = pd.read_csv(file_path)
            updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)
            updated_df.to_csv(file_path, index=False)
        else:
            # If the file doesn't exist, create it
            new_data_df.to_csv(file_path, index=False)

        print(f"Data appended to {file_path}")
