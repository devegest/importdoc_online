from sqlalchemy import Boolean, Column, DateTime, BigInteger, Integer, String, Text, func
from app.core.database import Base

class Perfil(Base):
    __tablename__ = "perfis"
    id = Column(BigInteger, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(Text)
    nivel = Column(Integer, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
