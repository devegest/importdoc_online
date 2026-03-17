from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.models.usuario import Usuario
from app.models.usuario_empresa import UsuarioEmpresa
from app.models.empresa import Empresa
from app.models.perfil import Perfil

def only_digits(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())

def autenticar_usuario(db: Session, cpf: str, senha: str):
    cpf_limpo = only_digits(cpf)
    usuario = db.query(Usuario).filter(Usuario.cpf == cpf_limpo, Usuario.ativo == True).first()
    if not usuario:
        return None
    if not verify_password(senha, usuario.senha_hash):
        return None
    return usuario

def montar_resposta_login(db: Session, usuario: Usuario):
    vinculos = (
        db.query(UsuarioEmpresa, Empresa, Perfil)
        .join(Empresa, Empresa.id == UsuarioEmpresa.empresa_id)
        .join(Perfil, Perfil.id == UsuarioEmpresa.perfil_id)
        .filter(UsuarioEmpresa.usuario_id == usuario.id, UsuarioEmpresa.ativo == True)
        .all()
    )
    empresas = [{"empresa_id": e.id, "nome_fantasia": e.nome_fantasia, "cnpj": e.cnpj, "perfil": p.nome} for _, e, p in vinculos]
    token = create_access_token({"sub": str(usuario.id), "cpf": usuario.cpf})
    return {"access_token": token, "token_type": "bearer", "usuario_id": usuario.id, "nome": usuario.nome, "empresas": empresas}
