from pydantic import BaseModel

class ProfissionalServicoBase(BaseModel):
    id_profissional: int
    id_servico: int
    tempo_personalizado_minutos: int | None = None

class ProfissionalServicoCreate(ProfissionalServicoBase):
    pass

class ProfissionalServicoResponse(ProfissionalServicoBase):
    id: int

    class Config:
        from_attributes = True
