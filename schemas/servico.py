from pydantic import BaseModel


class ServicoCreate(BaseModel):
    nome: str
    descricao: str = None
    preco: float
    tempo_estimado_minutos: int = None
    custo_insumos: float
    score_tetrix: int = None
    classificao_tetrix: str = None

class ServicoResponse(BaseModel):
    id: int
    nome: str
    descricao: str = None
    preco: float
    tempo_estimado_minutos: int = None
    custo_insumos: float
    score_tetrix: int = None
    classificao_tetrix: str = None

    class Config:
        from_attributes = True
