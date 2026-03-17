from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.usuario_empresa import UsuarioEmpresa
from app.models.empresa import Empresa
from app.models.perfil import Perfil

router = APIRouter()

@router.get("/minhas")
def minhas_empresas(db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    vinculos = (
        db.query(UsuarioEmpresa, Empresa, Perfil)
        .join(Empresa, Empresa.id == UsuarioEmpresa.empresa_id)
        .join(Perfil, Perfil.id == UsuarioEmpresa.perfil_id)
        .filter(UsuarioEmpresa.usuario_id == usuario.id, UsuarioEmpresa.ativo == True)
        .all()
    )
    return [{"empresa_id": e.id, "nome_fantasia": e.nome_fantasia, "cnpj": e.cnpj, "perfil": p.nome} for _, e, p in vinculos]
