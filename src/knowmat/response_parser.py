import csv


class ResponseParser:
    """
    A class to parse the LLM response and save it to a CSV file.
    """

    @staticmethod
    def save_to_csv(data: list, output_path: str, file_name: str) -> None:
        """
        Save the extracted data to a CSV file.

        Args:
            data (list): Extracted data.
            output_path (str): Path to save the CSV file.
            file_name (str): Name of the CSV file.
        """
        file_path = f"{output_path}/{file_name}"
        with open(file_path, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "Composition",
                    "Property Name",
                    "Value",
                    "Unit",
                    "Measurement Condition",
                ]
            )

            for entry in data:
                for comp in entry["data"].compositions:
                    for prop in comp.properties_of_composition:
                        writer.writerow(
                            [
                                comp.composition,
                                prop.property_name,
                                prop.value,
                                prop.unit,
                                prop.measurement_condition,
                            ]
                        )

        print(f"Data saved to {file_path}")
