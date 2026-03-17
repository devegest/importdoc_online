from sqlalchemy import Boolean, Column, Date, DateTime, BigInteger, ForeignKey, String, Text, UniqueConstraint
from app.core.database import Base

class TipoDocumento(Base):
    __tablename__ = "tipos_documentos"
    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, unique=True)
    ativo = Column(Boolean, nullable=False, default=True)

class DocumentoObrigatorio(Base):
    __tablename__ = "documentos_obrigatorios"
    __table_args__ = (UniqueConstraint("especialidade_id", "tipo_documento_id", name="uq_doc_esp"),)
    id = Column(BigInteger, primary_key=True, index=True)
    especialidade_id = Column(BigInteger, ForeignKey("especialidades.id", ondelete="CASCADE"), nullable=False)
    tipo_documento_id = Column(BigInteger, ForeignKey("tipos_documentos.id"), nullable=False)
    obrigatorio = Column(Boolean, nullable=False, default=True)

class DocumentoProfissional(Base):
    __tablename__ = "documentos_profissional"
    id = Column(BigInteger, primary_key=True, index=True)
    profissional_id = Column(BigInteger, ForeignKey("profissionais.id", ondelete="CASCADE"), nullable=False)
    tipo_documento_id = Column(BigInteger, ForeignKey("tipos_documentos.id"), nullable=False)
    arquivo_nome = Column(String(255))
    arquivo_url = Column(Text)
    status = Column(String(30), nullable=False, default="NAO_ENVIADO")
    validade = Column(Date)
    observacao = Column(Text)
    enviado_em = Column(DateTime)
    analisado_em = Column(DateTime)
