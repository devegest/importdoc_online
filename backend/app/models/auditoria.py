from sqlalchemy import Column, Date, Time, BigInteger, ForeignKey, String, Text
from app.core.database import Base

class Auditoria(Base):
    __tablename__ = "auditoria"
    id = Column(BigInteger, primary_key=True, index=True)
    usuario_id = Column(BigInteger, ForeignKey("usuarios.id"))
    empresa_id = Column(BigInteger, ForeignKey("empresas.id"))
    modulo = Column(String(100), nullable=False)
    acao = Column(String(100), nullable=False)
    tabela_afetada = Column(String(100))
    registro_id = Column(String(100))
    valor_antigo = Column(Text)
    valor_novo = Column(Text)
    data_alteracao = Column(Date, nullable=False)
    hora_alteracao = Column(Time, nullable=False)
    ip_origem = Column(String(45))
    descricao = Column(Text)
