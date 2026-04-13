from pydantic import BaseModel


# o que a api recebe do usuario
class SalaoCreate(BaseModel):
    nome: str
    endereco: str

# o que a api retorna para o usuario
class SalaoResponse(BaseModel):
    id: int
    nome: str
    endereco: str

    class Config:
            from_attributes = True