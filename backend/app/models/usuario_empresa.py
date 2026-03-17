from sqlalchemy import Boolean, Column, DateTime, BigInteger, ForeignKey, UniqueConstraint, func
from app.core.database import Base

class UsuarioEmpresa(Base):
    __tablename__ = "usuario_empresas"
    __table_args__ = (UniqueConstraint("usuario_id", "empresa_id", name="uq_usuario_empresa"),)
    id = Column(BigInteger, primary_key=True, index=True)
    usuario_id = Column(BigInteger, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    empresa_id = Column(BigInteger, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    perfil_id = Column(BigInteger, ForeignKey("perfis.id"), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
