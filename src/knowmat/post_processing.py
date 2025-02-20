import json
import os

import pandas as pd
from sentence_transformers import SentenceTransformer, util


class PostProcessor:
    """
    A class for post-processing extracted material science data.
    It maps extracted properties to the closest match from a predefined list using SentenceTransformers.
    """

    def __init__(self, properties_file: str, extracted_data_file: str):
        """
        Initializes the PostProcessor with paths to the properties file and extracted data CSV.
        Also loads the sentence transformer model and precomputes embeddings for all standard properties.

        Args:
            properties_file (str): Path to the JSON file containing allowed properties.
            extracted_data_file (str): Path to the CSV file containing extracted property data.
        """
        self.properties_file = properties_file
        self.extracted_data_file = extracted_data_file
        self.property_lookup = self.load_properties()
        self.model = SentenceTransformer(
            "all-distilroberta-v1"
        )  # or any other suitable model
        # Precompute embeddings for the candidate properties (keys of property_lookup)
        self.property_embeddings = {
            prop: self.model.encode(prop, convert_to_tensor=True)
            for prop in self.property_lookup.keys()
        }

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
                    lookup[prop.lower()] = (domain, category, prop)
        return lookup

    def find_closest_property(self, property_name: str):
        """
        Finds the closest matching property from the lookup dictionary using SentenceTransformer embeddings.

        Args:
            property_name (str): The extracted property name.

        Returns:
            tuple: (domain, category, matched_property) if a match above threshold is found,
            otherwise (None, None, None).
        """
        property_name_clean = property_name.lower().strip()
        # Get the embedding for the extracted property
        property_embedding = self.model.encode(
            property_name_clean, convert_to_tensor=True
        )
        best_match = None
        best_score = -1

        # Compare the extracted property's embedding against all candidate embeddings
        for candidate, candidate_embedding in self.property_embeddings.items():
            # Compute cosine similarity (value between -1 and 1)
            score = util.cos_sim(property_embedding, candidate_embedding).item()
            if score > best_score:
                best_score = score
                best_match = candidate

        # You can adjust the threshold based on your validation
        if best_match and best_score > 0.5:
            return self.property_lookup[best_match]
        return None, None, None

    def process_extracted_data(self):
        """
        Reads the extracted data CSV, matches properties using the SentenceTransformer approach,
        updates the DataFrame with new columns: domain, category, and standard_property_name, and
        saves the updated DataFrame back to the same file.
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

        # Apply matching function and update the DataFrame with new columns: domain,
        # category, standard_property_name
        extracted_df[["domain", "category", "standard_property_name"]] = extracted_df[
            "Property Name"
        ].apply(lambda x: pd.Series(self.find_closest_property(x)))

        # Save the updated DataFrame back to the same file
        extracted_df.to_csv(self.extracted_data_file, index=False)
        print(f"Updated extracted data saved to {self.extracted_data_file}")

    def update_extracted_json(self, extracted_result):
        """
        Updates the extracted JSON data by adding 'domain', 'category', and 'standard_property_name'
        keys after each 'property_name' in the properties list for each composition.

        Args:
            extracted_result (list): The extracted result (from JSONExtractor.extract).

        Returns:
            list: The updated extracted result.
        """
        # Assuming extracted_result[0]["data"].compositions is a list of composition objects.
        for composition in extracted_result[0]["data"].compositions:
            for prop in composition.properties_of_composition:
                domain, category, std_property = self.find_closest_property(
                    prop.property_name
                )
                # Convert property object to a dictionary and add new fields
                prop_dict = prop.__dict__
                prop_dict["standard_property_name"] = std_property
                prop_dict["category"] = category
                prop_dict["domain"] = domain

        return extracted_result
