from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.documento import DocumentoProfissional, TipoDocumento
from app.models.profissional import Profissional
from app.models.usuario_empresa import UsuarioEmpresa
from app.schemas.documento import DocumentoStatusUpdate
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

@router.get("/profissional/{profissional_id}")
def listar_documentos_profissional(profissional_id: int, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    profissional = db.query(Profissional).filter(Profissional.id == profissional_id).first()
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    validar_empresa_usuario(db, usuario.id, profissional.empresa_id)
    documentos = (
        db.query(DocumentoProfissional, TipoDocumento)
        .join(TipoDocumento, TipoDocumento.id == DocumentoProfissional.tipo_documento_id)
        .filter(DocumentoProfissional.profissional_id == profissional_id)
        .all()
    )
    return [{"id": doc.id, "tipo_documento": tipo.nome, "status": doc.status, "arquivo_nome": doc.arquivo_nome, "arquivo_url": doc.arquivo_url, "observacao": doc.observacao} for doc, tipo in documentos]

@router.put("/{documento_id}/status")
def alterar_status_documento(documento_id: int, payload: DocumentoStatusUpdate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    documento = db.query(DocumentoProfissional).filter(DocumentoProfissional.id == documento_id).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    profissional = db.query(Profissional).filter(Profissional.id == documento.profissional_id).first()
    validar_empresa_usuario(db, usuario.id, profissional.empresa_id)
    status_antigo = documento.status
    documento.status = payload.status
    documento.observacao = payload.observacao
    documento.analisado_em = datetime.now()
    db.commit()
    registrar_auditoria(db, usuario.id, profissional.empresa_id, "DOCUMENTOS", "ALTERACAO_STATUS", "documentos_profissional", str(documento.id), f"status={status_antigo}", f"status={payload.status}", "Status documental alterado")
    return {"message": "Status atualizado com sucesso"}
