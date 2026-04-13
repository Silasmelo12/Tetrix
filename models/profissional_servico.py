from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class ProfissionalServico(Base):
    __tablename__ = "profissionais_servicos"

    id = Column(Integer, primary_key=True, index=True)
    id_profissional = Column(Integer, ForeignKey("profissionais.id"))
    id_servico = Column(Integer, ForeignKey("servicos.id"))
    tempo_personalizado_minutos = Column(Integer)

    profissional = relationship("Profissional", back_populates="servicos_associados")
    servico = relationship("Servico", back_populates="profissionais_associados")
