from sqlalchemy import Column, Integer, String, true
from db.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    profissional_preferido = Column(String, nullable=False)
    telefone = Column(String, unique=True, nullable=False)
