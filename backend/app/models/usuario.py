from sqlalchemy import Boolean, Column, DateTime, BigInteger, String, func
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(BigInteger, primary_key=True, index=True)
    cpf = Column(String(11), nullable=False, unique=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150))
    senha_hash = Column(String, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    ultimo_login_em = Column(DateTime)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
