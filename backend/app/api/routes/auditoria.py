from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.auditoria import Auditoria
from app.models.usuario_empresa import UsuarioEmpresa

router = APIRouter()

@router.get("")
def listar_auditoria(empresa_id: int | None = None, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    query = db.query(Auditoria)
    if empresa_id is not None:
        vinculo = db.query(UsuarioEmpresa).filter(
            UsuarioEmpresa.usuario_id == usuario.id,
            UsuarioEmpresa.empresa_id == empresa_id,
            UsuarioEmpresa.ativo == True,
        ).first()
        if not vinculo:
            return []
        query = query.filter(Auditoria.empresa_id == empresa_id)
    return query.order_by(Auditoria.id.desc()).all()
