from typing import List, Optional

from ollama import chat
from pydantic import BaseModel, Field, field_validator

from src.knowmat.generate_allowed_properties import AllowedPropertiesGenerator
from src.knowmat.prompt_generator import PromptGenerator


class Property(BaseModel):
    """Represents a material property extracted from text."""

    property_name: str = Field(description="Name of the material property.")
    value: float = Field(description="Numerical value of the property.")
    unit: str = Field(description="Measurement unit of the property.")
    measurement_condition: Optional[str] = Field(
        default=None,
        description="Conditions under which the property was measured (e.g., temperature, pressure).",
    )
    additional_information: Optional[str] = Field(
        default=None,
        description="Any additional context related to this property, such as anisotropy details.",
    )

    @field_validator("property_name")
    def validate_property_name(cls, value):
        allowed_properties = AllowedPropertiesGenerator.generate_allowed_properties(
            "src/knowmat/properties.json"
        )
        if value.lower() not in allowed_properties:
            raise ValueError(
                f"Invalid property_name: {value}. Allowed properties are: {', '.join(allowed_properties)}"
            )
        return value


class CompositionProperties(BaseModel):
    """Represents the properties, processing conditions, and characterization techniques for a material composition."""

    composition: str = Field(description="The chemical composition of the material.")
    processing_conditions: Optional[str] = Field(
        default="not provided",
        description="Processing conditions applied to the material.",
    )
    characterization: Optional[dict[str, str]] = Field(
        default_factory=dict,
        description="Characterization techniques and their findings.",
    )
    properties_of_composition: List[Property] = Field(
        description="List of standard properties extracted."
    )


class CompositionList(BaseModel):
    """Encapsulates a list of compositions with extracted details."""

    compositions: List[CompositionProperties] = Field(
        description="A list of extracted material compositions."
    )


class Pipeline:
    """
    A class to handle the LLM pipeline for extracting structured data from text.
    """

    @staticmethod
    def run_pipeline(
        text: str, allowed_properties: list, model: str = "llama3.1:8b-instruct-q4_0"
    ) -> CompositionList:
        """
        Run the LLM pipeline with the given text and allowed properties.

        Args:
            text (str): The text to analyze.
            allowed_properties (list): List of allowed property names.
            model (str): The LLM model to use.

        Returns:
            CompositionList: Extracted data validated with Pydantic.
        """
        system_prompt = PromptGenerator.generate_system_prompt(allowed_properties)
        user_prompt = PromptGenerator.generate_user_prompt(text)

        # print("system prompt", system_prompt)
        # print("user prompt", user_prompt)

        response = chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=model,
            format=CompositionList.model_json_schema(),
            options={
                "temperature": 0.0,
                "num_ctx": 10000,
            },  # , "top_p": 0, "top_k": 0},
        )
        print("Raw Response", response.message.content)
        return CompositionList.model_validate_json(response.message.content)
