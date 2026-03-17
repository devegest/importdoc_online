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
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from app.core.database import get_db
from app.models.usuario import Usuario

router = APIRouter()

# =========================
# MODELS
# =========================

class LoginRequest(BaseModel):
    cpf: str
    senha: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    nova_senha: str


# =========================
# LOGIN (já existente)
# =========================

@router.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.cpf == data.cpf).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    # ⚠️ Aqui você pode validar senha depois (bcrypt)
    return {
        "message": "Login realizado",
        "user": user.nome
    }


# =========================
# ESQUECI SENHA
# =========================

@router.post("/auth/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()

    # sempre retorna sucesso (segurança)
    if not user:
        return {"message": "Se o email existir, enviaremos instruções"}

    # gera token simples
    token = secrets.token_urlsafe(32)

    # 🚀 aqui depois você pode salvar no banco
    return {
        "message": "Link de recuperação gerado",
        "preview_token": token
    }


# =========================
# RESETAR SENHA
# =========================

@router.post("/auth/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    # ⚠️ aqui depois vamos validar token de verdade

    user = db.query(Usuario).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # ⚠️ aqui ideal seria bcrypt
    user.senha_hash = data.nova_senha
    db.commit()

    return {"message": "Senha alterada com sucesso"}
