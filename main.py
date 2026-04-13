from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.deps import get_db
from models.salao import Salao
from schemas.salao import SalaoCreate, SalaoResponse

app = FastAPI()

# CREATE
@app.post("/saloes", response_model=SalaoResponse)
async def criar_salao(salao_data: SalaoCreate, db: AsyncSession = Depends(get_db)):
    novo_salao = Salao(nome=salao_data.nome, endereco=salao_data.endereco)
    db.add(novo_salao)
    await db.flush() 
    return novo_salao

# READ (LIST)
@app.get("/saloes", response_model=list[SalaoResponse])
async def listar_saloes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Salao))
    return result.scalars().all()

# UPDATE
@app.put("/saloes/{salao_id}", response_model=SalaoResponse)
async def atualizar_salao(salao_id: int, salao_data: SalaoCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Salao).where(Salao.id == salao_id))
    salao_db = result.scalar_one_or_none()
    
    if not salao_db:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    salao_db.nome = salao_data.nome
    salao_db.endereco = salao_data.endereco
    return salao_db

# DELETE
@app.delete("/saloes/{salao_id}")
async def deletar_salao(salao_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Salao).where(Salao.id == salao_id))
    salao_db = result.scalar_one_or_none()
    
    if not salao_db:
        raise HTTPException(status_code=404, detail="Salão não encontrado")
    
    await db.delete(salao_db)
    return {"message": "Salão deletado com sucesso"}

