from pydantic import BaseModel
from typing import Optional

class Document(BaseModel):
    id: str
    text: str
    source: str
    title: Optional[str] = None