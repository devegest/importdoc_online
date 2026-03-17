from sqlalchemy import Boolean, Column, DateTime, BigInteger, String, func
from app.core.database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(BigInteger, primary_key=True, index=True)
    razao_social = Column(String(200), nullable=False)
    nome_fantasia = Column(String(200))
    cnpj = Column(String(14), nullable=False, unique=True, index=True)
    email = Column(String(150))
    telefone = Column(String(20))
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
