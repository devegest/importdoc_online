from sqlalchemy import Column, Date, DateTime, BigInteger, ForeignKey, String, UniqueConstraint, func
from app.core.database import Base

class Profissional(Base):
    __tablename__ = "profissionais"
    __table_args__ = (UniqueConstraint("empresa_id", "cpf", name="uq_profissional_empresa_cpf"),)
    id = Column(BigInteger, primary_key=True, index=True)
    empresa_id = Column(BigInteger, ForeignKey("empresas.id", ondelete="RESTRICT"), nullable=False)
    cpf = Column(String(11), nullable=False, index=True)
    nome = Column(String(200), nullable=False)
    rg = Column(String(20))
    rg_data_expedicao = Column(Date)
    data_nascimento = Column(Date)
    estado_civil = Column(String(50))
    email = Column(String(150))
    telefone_fixo = Column(String(20))
    telefone_celular = Column(String(20))
    cargo = Column(String(100))
    status = Column(String(30), nullable=False, default="CADASTRO")
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
