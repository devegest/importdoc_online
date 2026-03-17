from datetime import date, datetime
from sqlalchemy.orm import Session
from app.models.auditoria import Auditoria

def registrar_auditoria(db: Session, usuario_id: int, empresa_id: int | None, modulo: str, acao: str,
                        tabela_afetada: str, registro_id: str, valor_antigo: str | None,
                        valor_novo: str | None, descricao: str, ip_origem: str | None = None):
    item = Auditoria(
        usuario_id=usuario_id,
        empresa_id=empresa_id,
        modulo=modulo,
        acao=acao,
        tabela_afetada=tabela_afetada,
        registro_id=registro_id,
        valor_antigo=valor_antigo,
        valor_novo=valor_novo,
        data_alteracao=date.today(),
        hora_alteracao=datetime.now().time().replace(microsecond=0),
        ip_origem=ip_origem,
        descricao=descricao,
    )
    db.add(item)
    db.commit()
