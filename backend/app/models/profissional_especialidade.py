from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, UniqueConstraint
from app.core.database import Base

class ProfissionalEspecialidade(Base):
    __tablename__ = "profissional_especialidades"
    __table_args__ = (UniqueConstraint("profissional_id", "especialidade_id", name="uq_prof_esp"),)
    id = Column(BigInteger, primary_key=True, index=True)
    profissional_id = Column(BigInteger, ForeignKey("profissionais.id", ondelete="CASCADE"), nullable=False)
    especialidade_id = Column(BigInteger, ForeignKey("especialidades.id"), nullable=False)
    registro_conselho = Column(String(50))
    principal = Column(Boolean, nullable=False, default=False)
