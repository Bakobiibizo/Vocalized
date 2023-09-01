from typing import Optional
import pydantic


class Data(pydantic.BaseModel):
    """
    Validator for the 'text' field.

    Parameters:
        text (str): The text to be validated.

    Raises:
        ValueError: If the text is empty.

    Returns:
        str: The validated text.
    """

    text: str
    voice_id: Optional[str]

    @pydantic.validator("text")
    @classmethod
    def text_valid(cls, text):
        if text == "":
            raise ValueError("Text cannot be empty")
        else:
            return text
