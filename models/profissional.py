# profissional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

# Define a classe do modelo Profissional, que herda de 'Base'.
# Esta classe representa a tabela 'profissionais' no banco de dados.
class Profissional(Base):
    # Define o nome da tabela no banco de dados.
    __tablename__ = "profissionais"

    # Define a coluna 'id' como um inteiro, chave primária e indexada para buscas rápidas.
    id = Column(Integer, primary_key=True, index=True)
    # Define a coluna 'nome' como uma string e não pode ser nula.
    nome = Column(String, nullable=False)
    # Define a coluna 'especialidade' como uma string. Pode ser nula.
    especialidade = Column(String)

    # Define o relacionamento com a tabela 'ProfissionalServico'.
    # 'back_populates' garante que o relacionamento seja bidirecional,
    # onde 'profissional' no modelo 'ProfissionalServico' se refere a este profissional.
    servicos_associados = relationship("ProfissionalServico", back_populates="profissional")