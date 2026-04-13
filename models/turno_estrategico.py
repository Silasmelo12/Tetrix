from sqlalchemy import Column, Integer, String, Time
from db.database import Base

class TurnoEstrategico(Base):
    __tablename__ = "turnos_estrategicos"

    id = Column(Integer, primary_key=True, index=True)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    classificacao = Column(String, nullable=False)
