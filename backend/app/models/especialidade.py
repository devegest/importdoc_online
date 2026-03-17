from sqlalchemy import Boolean, Column, DateTime, BigInteger, String, func
from app.core.database import Base

class Especialidade(Base):
    __tablename__ = "especialidades"
    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, unique=True)
    codigo_sistema = Column(String(50))
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
