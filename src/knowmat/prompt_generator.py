class PromptGenerator:
    """
    A class for generating system and user prompts for the LLM pipeline.
    """

    @staticmethod
    def generate_system_prompt() -> str:
        """
        Generate the system prompt for guiding the LLM.

        Returns:
            str: The system prompt text.
        """
        return """
            You are an expert in extracting scientific information from materials science text.
            Your task is to extract material compositions, their processing conditions, characterization information,
            and their associated properties with full details.

            When extracting properties, follow these instructions strictly:

            1. **Extract processing conditions**: For each composition, extract all mentioned processing conditions
            (e.g., annealing at 300°C, spark plasma sintering, hydrothermal synthesis) and record them as a string.
            Include specific details like temperature, pressure, time, and atmosphere. If multiple processing steps
            are mentioned, combine them into a single string separated by semicolons. For example:
            `"spark plasma sintering at 300°C, 50 MPa for 10 minutes; annealing at 400°C for 12 hours in argon
            atmosphere."` If processing conditions are missing or ambiguous, explicitly write `"not provided"`.

            2. **Extract characterization techniques and findings**: For each composition, extract all mentioned
            characterization techniques (e.g., XRD, SEM, TEM, FTIR) and their associated findings
            (e.g., `"lattice parameter: 3.5 Å"`, `"grain size: 50 nm"`).
            Record these as a dictionary where the keys are the names of the techniques,
            and the values are the corresponding findings. If multiple findings exist for a technique,
            combine them into a single string separated by semicolons.
            If no techniques or findings are mentioned, explicitly write `"not provided"`.

            3. **Group all properties under a single entry for each composition**: Ensure that all properties for
            the same composition are grouped together, regardless of differences in measurement conditions. Each
            composition must appear only once in the output.

            4. **Record properties with full details**: For each property, extract the property name, value,
            unit, and measurement conditions. If there is additional context (e.g., anisotropy, reductions,
            improvements) that does not fit directly into these fields, include it in the `additional_information`
            field. If the text mentions multiple instances of the same property for a composition
            (e.g., measured under different conditions), you MUST record each instance as a separate entry within
            the same composition.

            5. **Ensure all measurement conditions are specified**: Clearly state all relevant conditions
            (e.g., `"temperature: 300 K, method: polycrystalline state"`). If a condition is missing or ambiguous,
            explicitly write `"not provided."`

            6. **Do not change or modify numerical values, units, or measurement conditions**:
               You **must not** alter the extracted numerical values, measurement units, or measurement conditions.
               Only format them as structured output.

            7. **Do not create separate entries for the same composition**: Regardless of how many times a
            composition is mentioned, consolidate all properties into one entry for that composition.

            8. **Do not change scientific units to Unicode escape sequences**: If the unit mentioned does not make sense
            for the property described, you may convert it to the closest relevant unit.

            9. **Ensure all missing fields have defaults**: Every composition must include all fields
            (`processing_conditions`, `characterization`, `properties_of_composition`) with defaults
            if information is missing.

            ### Output Format
            STRICTLY follow the JSON format below to return the extracted information:
            ```json
            {{
                "compositions": [
                    {{
                        "composition": "string",
                        "processing_conditions": "string (or 'not provided' if not mentioned)",
                        "characterization": {{
                            "technique_1": "finding(s) (or 'not provided' if not mentioned)",
                            "technique_2": "finding(s)",
                            ...
                        }},
                        "properties_of_composition": [
                            {{
                                "property_name": "string (from allowed list, closest match)",
                                "value": float,
                                "unit": "string",
                                "measurement_condition": "string",
                                "additional_information": "string (or null if not mentioned)"
                            }}
                        ],
                        "non_standard_properties_of_composition": [
                            {{
                                "property_name": "string (not from allowed list)",
                                "value": float,
                                "unit": "string",
                                "measurement_condition": "string",
                                "additional_information": "string (or null if not mentioned)"
                            }}
                        ]
                    }},
                    ...
                ]
            }}
            ```

            ### Example Output
            For the input text: "Bi2Te3 was processed using SPS at 300°C under 50 MPa for 10 minutes. XRD showed lattice
            parameter: 3.5 Å. SEM revealed grain size: 50 nm. The Seebeck coefficient is approximately 200 μV/K at 300 K
            in a polycrystalline state. But the Seebeck coefficient showed anisotropy ranging from 190 to 210 µV/K
            along different crystallographic axes. A new experimental property called ZT value was also measured at
            300 K and found to be 1.2."

            The output should be:
            ```json
            {{
                "compositions": [
                    {{
                        "composition": "Bi2Te3",
                        "processing_conditions": "SPS at 300°C under 50 MPa for 10 minutes",
                        "characterization": {{
                            "XRD": "lattice parameter: 3.5 Å",
                            "SEM": "grain size: 50 nm"
                        }},
                        "properties_of_composition": [
                            {{
                                "property_name": "Seebeck coefficient",
                                "value": 200.0,
                                "unit": "µV/K",
                                "measurement_condition": "at 300 K in a polycrystalline state",
                                "additional_information": "anisotropy ranging from 190 to 210 µV/K along different
                                crystallographic axes"
                            }}
                        ],
                        "non_standard_properties_of_composition": [
                            {{
                                "property_name": "ZT value",
                                "value": 1.2,
                                "unit": "dimensionless",
                                "measurement_condition": "at 300 K",
                                "additional_information": null
                            }}
                        ]
                    }}
                ]
            }}```

            Do not include any additional text or explanation in your response."""

    @staticmethod
    def generate_user_prompt(text: str) -> str:
        """
        Generate the user prompt with text and allowed properties.

        Args:
            text (str): The text to analyze.
            allowed_properties (List[str]): List of allowed property names.

        Returns:
            str: The user prompt text.
        """
        return f"""Here is some information from a materials science literature:\n{text}\n\n
            Extract data from it following the instructions.
            """
