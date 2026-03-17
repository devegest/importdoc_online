from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr

class ProfissionalCreate(BaseModel):
    empresa_id: int
    cpf: str
    nome: str
    rg: Optional[str] = None
    rg_data_expedicao: Optional[date] = None
    data_nascimento: Optional[date] = None
    estado_civil: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone_fixo: Optional[str] = None
    telefone_celular: Optional[str] = None
    cargo: Optional[str] = None
    especialidade_id: int
    registro_conselho: Optional[str] = None
