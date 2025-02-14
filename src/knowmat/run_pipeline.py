import json

from src.knowmat.json_extractor import JSONExtractor
from src.knowmat.response_parser import ResponseParser

# # Define paths
# folder_path = "C:/Users/hsayeed/Documents/GitHub/KnowMat/data/processed" # "path_to_your_pdfs"
# properties_file = "src/knowmat/properties.json"
# output_path = "C:/Users/hsayeed/Documents/GitHub/KnowMat/data/processed"
# output_file_name = "extracted_data.csv"

# # Run extraction
# extracted_data = JSONExtractor.extract(folder_path, properties_file)
# print(extracted_data)

# # Save to CSV
# ResponseParser.save_to_csv(extracted_data, output_path, output_file_name)
# print(f"Data saved to {output_path}/{output_file_name}")


# Define paths
folder_path = (
    "C:/Users/hsayeed/Documents/GitHub/KnowMat/data/processed"  # Path to your PDFs
)
properties_file = "src/knowmat/properties.json"
output_path = "C:/Users/hsayeed/Documents/GitHub/KnowMat/data/processed"
output_file_name = "extracted_data.csv"

# Run extraction
extracted_data = JSONExtractor.extract(folder_path, properties_file)

print(extracted_data)

# Print data in a readable JSON format
for file_data in extracted_data:
    file_name = file_data["file_name"]
    compositions = file_data["data"].compositions
    print(f"\nFile: {file_name}")
    for composition in compositions:
        composition_dict = {
            "composition": composition.composition,
            "processing_conditions": composition.processing_conditions,  # Include processing conditions
            "characterization": composition.characterization,  # Include characterization dictionary
            "properties": [
                {
                    "property_name": prop.property_name,
                    "value": prop.value,
                    "unit": prop.unit,
                    "measurement_condition": prop.measurement_condition,
                }
                for prop in composition.properties_of_composition
            ],
        }
        print(json.dumps(composition_dict, indent=4, ensure_ascii=False))

# Save to CSV
ResponseParser.save_to_csv(extracted_data, output_path, output_file_name)
print(f"\nData saved to {output_path}/{output_file_name}")
