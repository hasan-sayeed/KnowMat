import csv
import json
import sys


def csv_to_json_records(csv_file_path):
    records = {}
    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comp = row["composition"]
            if comp not in records:
                # Initialize a new record using file_name, composition, processing condition, and characterization.
                records[comp] = {
                    "file_name": row["file name"],
                    "composition": row["composition"],
                    "processing condition": row["processing condition"],
                    "characterization": row["characterization"],
                    "properties": [],
                }
            # Process the property entry.
            try:
                value = float(row["value"])
            except ValueError:
                value = row["value"]
            property_dict = {
                "property_name": row["property name"],
                "value": value,
                "unit": row["unit"],
                "measurement_condition": row["measurement condition"],
                "standard_property_name": row["standard_property_name"],
                "category": row["category"],
                "domain": row["domain"],
            }
            records[comp]["properties"].append(property_dict)
    # Return a list of JSON objects for each composition.
    return list(records.values())


def main():
    if len(sys.argv) != 2:
        print("Usage: {} <csv_file>".format(sys.argv[0]))
        sys.exit(1)
    csv_file = sys.argv[1]
    json_records = csv_to_json_records(csv_file)
    for record in json_records:
        print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
