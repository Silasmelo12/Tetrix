from pydantic import BaseModel
from datetime import datetime

class AgendamentoCreate(BaseModel):
    id_cliente: int
    id_servico: int
    id_profissional: int
    data_hora_inicio: datetime
    status: str = "Pendente" # Valor padrão

class AgendamentoResponse(BaseModel):
    id: int
    id_cliente: int
    id_servico: int
    id_profissional: int
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: str
    sugerido_pelo_tetrix: bool

    class Config:
        from_attributes = True
