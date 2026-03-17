from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.profissional import Profissional
from app.models.profissional_especialidade import ProfissionalEspecialidade
from app.models.especialidade import Especialidade
from app.models.usuario_empresa import UsuarioEmpresa
from app.schemas.profissional import ProfissionalCreate
from app.services.profissional_service import criar_profissional
from app.services.auditoria_service import registrar_auditoria

router = APIRouter()

def validar_empresa_usuario(db: Session, usuario_id: int, empresa_id: int):
    vinculo = db.query(UsuarioEmpresa).filter(
        UsuarioEmpresa.usuario_id == usuario_id,
        UsuarioEmpresa.empresa_id == empresa_id,
        UsuarioEmpresa.ativo == True,
    ).first()
    if not vinculo:
        raise HTTPException(status_code=403, detail="Usuário sem acesso a esta empresa")
    return vinculo

@router.post("")
def novo_profissional(payload: ProfissionalCreate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    validar_empresa_usuario(db, usuario.id, payload.empresa_id)
    profissional, especialidade = criar_profissional(db, payload)
    registrar_auditoria(db, usuario.id, payload.empresa_id, "PROFISSIONAIS", "CRIACAO", "profissionais", str(profissional.id), None, f"cpf={profissional.cpf};nome={profissional.nome};especialidade={especialidade.nome}", "Profissional criado com sucesso")
    return {"id": profissional.id, "message": "Profissional criado com sucesso"}

@router.get("")
def listar_profissionais(empresa_id: int, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    validar_empresa_usuario(db, usuario.id, empresa_id)
    profissionais = db.query(Profissional).filter(Profissional.empresa_id == empresa_id).all()
    resultado = []
    for profissional in profissionais:
        vinculos = (
            db.query(ProfissionalEspecialidade, Especialidade)
            .join(Especialidade, Especialidade.id == ProfissionalEspecialidade.especialidade_id)
            .filter(ProfissionalEspecialidade.profissional_id == profissional.id)
            .all()
        )
        resultado.append({
            "id": profissional.id,
            "empresa_id": profissional.empresa_id,
            "cpf": profissional.cpf,
            "nome": profissional.nome,
            "status": profissional.status,
            "especialidades": [{
                "especialidade_id": esp.id,
                "nome": esp.nome,
                "registro_conselho": pe.registro_conselho,
                "principal": pe.principal,
            } for pe, esp in vinculos],
        })
    return resultado
