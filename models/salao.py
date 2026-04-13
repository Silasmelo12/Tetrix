from sqlalchemy import Column, Integer, String
from db.database import Base

class Salao(Base):
    __tablename__ = "saloes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    endereco = Column(String)