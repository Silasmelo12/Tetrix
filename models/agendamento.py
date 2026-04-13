from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    id_servico = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    id_profissional = Column(Integer, ForeignKey("profissionais.id"), nullable=False)
    data_hora_inicio = Column(DateTime(timezone=True), nullable=False)
    data_hora_fim = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False)
    sugerido_pelo_tetrix = Column(Boolean, default=False)

    cliente = relationship("Cliente", backref="agendamentos")
    servico = relationship("Servico", backref="agendamentos")
    profissional = relationship("Profissional", backref="agendamentos")
