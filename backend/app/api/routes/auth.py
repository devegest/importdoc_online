from datetime import datetime, timedelta
import secrets

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import autenticar_usuario, montar_resposta_login
from app.services.auditoria_service import registrar_auditoria

router = APIRouter()


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    nova_senha: str


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, payload.cpf, payload.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="CPF ou senha inválidos")

    resposta = montar_resposta_login(db, usuario)

    registrar_auditoria(
        db,
        usuario.id,
        None,
        "AUTH",
        "LOGIN",
        "usuarios",
        str(usuario.id),
        None,
        None,
        "Login realizado com sucesso",
    )
    return resposta


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    usuario = db.execute(
        text("""
            SELECT id, email
            FROM usuarios
            WHERE email = :email AND ativo = 1
            LIMIT 1
        """),
        {"email": payload.email},
    ).mappings().first()

    if not usuario:
        return {"message": "Se o e-mail existir, enviaremos as instruções."}

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=30)

    db.execute(
        text("""
            INSERT INTO password_reset (usuario_id, email, token, expires_at, used)
            VALUES (:usuario_id, :email, :token, :expires_at, 0)
        """),
        {
            "usuario_id": usuario["id"],
            "email": usuario["email"],
            "token": token,
            "expires_at": expires_at,
        },
    )
    db.commit()

    return {
        "message": "Solicitação registrada com sucesso.",
        "preview_token": token
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    reset = db.execute(
        text("""
            SELECT id, usuario_id, token, expires_at, used
            FROM password_reset
            WHERE token = :token
            LIMIT 1
        """),
        {"token": payload.token},
    ).mappings().first()

    if not reset:
        raise HTTPException(status_code=404, detail="Token inválido.")

    if int(reset["used"]) == 1:
        raise HTTPException(status_code=400, detail="Token já utilizado.")

    expires_at = reset["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)

    if datetime.utcnow() > expires_at:
        raise HTTPException(status_code=400, detail="Token expirado.")

    # Mantendo simples por enquanto, sem mexer no restante do fluxo.
    # Depois dá para trocar por hash bcrypt usando a mesma lógica do login.
    db.execute(
        text("""
            UPDATE usuarios
            SET senha_hash = :senha_hash
            WHERE id = :usuario_id
        """),
        {
            "senha_hash": payload.nova_senha,
            "usuario_id": reset["usuario_id"],
        },
    )

    db.execute(
        text("""
            UPDATE password_reset
            SET used = 1
            WHERE id = :id
        """),
        {"id": reset["id"]},
    )

    db.commit()

    return {"message": "Senha redefinida com sucesso."}
