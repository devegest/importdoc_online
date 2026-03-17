from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import autenticar_usuario, montar_resposta_login
from app.services.auditoria_service import registrar_auditoria

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, payload.cpf, payload.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="CPF ou senha inválidos")
    resposta = montar_resposta_login(db, usuario)
    registrar_auditoria(db, usuario.id, None, "AUTH", "LOGIN", "usuarios", str(usuario.id), None, None, "Login realizado com sucesso")
    return resposta
