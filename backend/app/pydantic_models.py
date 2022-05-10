from pydantic import BaseModel


class ModelBody(BaseModel):
    """Pydantic model used to validate requests against the api"""
    id: str
    readme_text: str
