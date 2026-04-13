from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.deps import get_db
from models.servico import Servico
from schemas.servico import ServicoCreate, ServicoResponse

router = APIRouter(prefix="/servico", tags=["servico"])

# CREATE
@router.post("/", response_model=ServicoResponse)
async def criar_servico(servico_data: ServicoCreate, db: AsyncSession = Depends(get_db)):
    novo_servico = Servico(
        nome=servico_data.nome,
        descricao=servico_data.descricao,
        preco=servico_data.preco,
        tempo_estimado_minutos=servico_data.tempo_estimado_minutos,
        custo_insumos=servico_data.custo_insumos,
        score_tetrix=servico_data.score_tetrix,
        classificao_tetrix=servico_data.classificao_tetrix
    )
    db.add(novo_servico)
    await db.commit()
    await db.refresh(novo_servico)
    return novo_servico

# READ (LIST)
@router.get("/", response_model=list[ServicoResponse])
async def listar_servicos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Servico))
    return result.scalars().all()

# READ (SINGLE)
@router.get("/{servico_id}", response_model=ServicoResponse)
async def buscar_servico(servico_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Servico).where(Servico.id == servico_id))
    servico_db = result.scalar_one_or_none()
    if not servico_db:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return servico_db

# UPDATE
@router.put("/{servico_id}", response_model=ServicoResponse)
async def atualizar_servico(servico_id: int, servico_data: ServicoCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Servico).where(Servico.id == servico_id))
    servico_db = result.scalar_one_or_none()

    if not servico_db:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    servico_db.nome = servico_data.nome
    servico_db.descricao = servico_data.descricao
    servico_db.preco = servico_data.preco
    servico_db.tempo_estimado_minutos = servico_data.tempo_estimado_minutos
    servico_db.custo_insumos = servico_data.custo_insumos
    servico_db.score_tetrix = servico_data.score_tetrix
    servico_db.classificao_tetrix = servico_data.classificao_tetrix

    await db.commit()
    await db.refresh(servico_db)
    return servico_db

# DELETE
@router.delete("/{servico_id}")
async def deletar_servico(servico_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Servico).where(Servico.id == servico_id))
    servico_db = result.scalar_one_or_none()

    if not servico_db:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    await db.delete(servico_db)
    await db.commit()
    return {"message": "Serviço deletado com sucesso"}