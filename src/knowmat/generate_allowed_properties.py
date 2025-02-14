import json


class AllowedPropertiesGenerator:
    """
    A class to generate the allowed property names from a JSON properties file.
    """

    @staticmethod
    def generate_allowed_properties(properties_file: str) -> list:
        """
        Generate a list of allowed property names from a JSON properties file.

        Args:
            properties_file (str): Path to the JSON file containing property definitions.

        Returns:
            list: A list of allowed property names.
        """
        with open(properties_file, "r") as file:
            data = json.load(file)

        allowed_properties = []
        for _, properties in data.items():
            for _, aliases in properties.items():
                allowed_properties.extend(aliases)
        allowed_properties.append("")

        return list(allowed_properties)  # Remove duplicates
