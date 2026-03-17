from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.profissional import Profissional
from app.models.especialidade import Especialidade
from app.models.profissional_especialidade import ProfissionalEspecialidade
from app.models.documento import DocumentoObrigatorio, DocumentoProfissional

def only_digits(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())

def criar_profissional(db: Session, payload):
    cpf = only_digits(payload.cpf)
    if len(cpf) != 11:
        raise HTTPException(status_code=400, detail="CPF inválido")

    existente = db.query(Profissional).filter(Profissional.empresa_id == payload.empresa_id, Profissional.cpf == cpf).first()
    if existente:
        raise HTTPException(status_code=409, detail="CPF já cadastrado nesta empresa")

    especialidade = db.query(Especialidade).filter(Especialidade.id == payload.especialidade_id, Especialidade.ativo == True).first()
    if not especialidade:
        raise HTTPException(status_code=404, detail="Especialidade não encontrada")

    profissional = Profissional(
        empresa_id=payload.empresa_id,
        cpf=cpf,
        nome=payload.nome,
        rg=payload.rg,
        rg_data_expedicao=payload.rg_data_expedicao,
        data_nascimento=payload.data_nascimento,
        estado_civil=payload.estado_civil,
        email=payload.email,
        telefone_fixo=payload.telefone_fixo,
        telefone_celular=payload.telefone_celular,
        cargo=payload.cargo,
        status="CADASTRO",
    )
    db.add(profissional)
    db.flush()

    db.add(ProfissionalEspecialidade(
        profissional_id=profissional.id,
        especialidade_id=payload.especialidade_id,
        registro_conselho=payload.registro_conselho,
        principal=True,
    ))

    obrigatorios = db.query(DocumentoObrigatorio).filter(DocumentoObrigatorio.especialidade_id == payload.especialidade_id).all()
    for item in obrigatorios:
        db.add(DocumentoProfissional(
            profissional_id=profissional.id,
            tipo_documento_id=item.tipo_documento_id,
            status="NAO_ENVIADO",
        ))

    db.commit()
    db.refresh(profissional)
    return profissional, especialidade
