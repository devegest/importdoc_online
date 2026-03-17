from pydantic import BaseModel, Field
from typing import List

class LoginRequest(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=14)
    senha: str

class EmpresaResumo(BaseModel):
    empresa_id: int
    nome_fantasia: str
    cnpj: str
    perfil: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    nome: str
    empresas: List[EmpresaResumo]
