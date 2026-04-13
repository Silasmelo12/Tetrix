# profissional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String)

    servicos_associados = relationship("ProfissionalServico", back_populates="profissional")