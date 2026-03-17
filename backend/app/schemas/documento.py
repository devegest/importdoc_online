from typing import Optional
from pydantic import BaseModel

class DocumentoStatusUpdate(BaseModel):
    status: str
    observacao: Optional[str] = None
