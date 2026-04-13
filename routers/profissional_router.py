from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.deps import get_db
from models.profissional import Profissional
from schemas.profissional import ProfissionalCreate, ProfissionalResponse

router = APIRouter(prefix="/profissionais", tags=["profissionais"])

# CREATE
@router.post("/", response_model=ProfissionalResponse)
async def criar_profissional(profissional_data: ProfissionalCreate, db: AsyncSession = Depends(get_db)):
    novo_profissional = Profissional(
        nome=profissional_data.nome,
        especialidade=profissional_data.especialidade
    )
    db.add(novo_profissional)
    await db.commit()
    await db.refresh(novo_profissional)
    return novo_profissional

# READ (LIST)
@router.get("/", response_model=list[ProfissionalResponse])
async def listar_profissionais(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profissional))
    return result.scalars().all()

# READ (SINGLE)
@router.get("/{profissional_id}", response_model=ProfissionalResponse)
async def buscar_profissional(profissional_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profissional).where(Profissional.id == profissional_id))
    profissional_db = result.scalar_one_or_none()
    if not profissional_db:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return profissional_db

# UPDATE
@router.put("/{profissional_id}", response_model=ProfissionalResponse)
async def atualizar_profissional(profissional_id: int, profissional_data: ProfissionalCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profissional).where(Profissional.id == profissional_id))
    profissional_db = result.scalar_one_or_none()

    if not profissional_db:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    profissional_db.nome = profissional_data.nome
    profissional_db.especialidade = profissional_data.especialidade

    await db.commit()
    await db.refresh(profissional_db)
    return profissional_db

# DELETE
@router.delete("/{profissional_id}")
async def deletar_profissional(profissional_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profissional).where(Profissional.id == profissional_id))
    profissional_db = result.scalar_one_or_none()

    if not profissional_db:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    await db.delete(profissional_db)
    await db.commit()
    return {"message": "Profissional deletado com sucesso"}
