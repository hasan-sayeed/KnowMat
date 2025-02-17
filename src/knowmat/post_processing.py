import json
import os
from difflib import get_close_matches

import pandas as pd


class PostProcessor:
    """
    A class for post-processing extracted material science data.
    It maps extracted properties to the closest match from a predefined list and adds relevant metadata.
    """

    def __init__(self, properties_file: str, extracted_data_file: str):
        """
        Initializes the PostProcessor with paths to the properties file and extracted data CSV.

        Args:
            properties_file (str): Path to the JSON file containing allowed properties.
            extracted_data_file (str): Path to the CSV file containing extracted property data.
        """
        self.properties_file = properties_file
        self.extracted_data_file = extracted_data_file
        self.property_lookup = self.load_properties()

    def load_properties(self) -> dict:
        """
        Loads properties from the JSON file and prepares a lookup dictionary.

        Returns:
            dict: A dictionary where keys are lowercase property names, and values are
            (domain, category, standard property).
        """
        with open(self.properties_file, "r") as file:
            data = json.load(file)

        lookup = {}
        for domain, categories in data.items():
            for category, properties in categories.items():
                for prop in properties:
                    lookup[prop.lower()] = (
                        domain,
                        category,
                        prop,
                    )  # Case-insensitive matching

        return lookup

    def find_closest_property(self, property_name: str):
        """
        Finds the closest matching property from the lookup dictionary.

        Args:
            property_name (str): The extracted property name.

        Returns:
            tuple: (domain, category, matched_property) if found, otherwise (None, None, None).
        """
        property_name = property_name.lower().strip()
        closest_match = get_close_matches(
            property_name, self.property_lookup.keys(), n=1, cutoff=0.4
        )  # Adjust cutoff if needed

        if closest_match:
            return self.property_lookup[closest_match[0]]
        return None, None, None  # If no match is found

    def process_extracted_data(self):
        """
        Reads the extracted data CSV, matches properties, updates metadata, and saves back to the same file.
        """
        if not os.path.exists(self.extracted_data_file):
            raise FileNotFoundError(f"File not found: {self.extracted_data_file}")

        # Load extracted data
        extracted_df = pd.read_csv(self.extracted_data_file)

        # Ensure the necessary column exists
        if "Property Name" not in extracted_df.columns:
            raise ValueError(
                "The 'Property Name' column is missing in extracted_data.csv"
            )

        # Apply matching function and update the DataFrame
        extracted_df[["domain", "category", "property"]] = extracted_df[
            "Property Name"
        ].apply(lambda x: pd.Series(self.find_closest_property(x)))

        # Save the updated DataFrame back to the same file
        extracted_df.to_csv(self.extracted_data_file, index=False)
        print(f"Updated extracted data saved to {self.extracted_data_file}")
