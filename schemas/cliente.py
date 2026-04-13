from pydantic import BaseModel


class ClienteCreate(BaseModel):
    nome: str
    profissional_preferido: str
    telefone: str

class ClienteResponse(BaseModel):
    id: int
    nome: str
    profissional_preferido: str
    telefone: str

    class Config:
        from_attributes = True

