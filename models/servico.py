from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.database import Base

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    tempo_estimado_minutos = Column(Integer)
    custo_insumos = Column(Float, nullable=False)
    score_tetrix = Column(Integer)
    classificao_tetrix = Column(String) # premium, estratégico, tatico, recuperação

    profissionais_associados = relationship("ProfissionalServico", back_populates="servico")
