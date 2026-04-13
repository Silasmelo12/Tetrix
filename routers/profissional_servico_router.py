from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.deps import get_db
from models.profissional_servico import ProfissionalServico
from schemas.profissional_servico import ProfissionalServicoCreate, ProfissionalServicoResponse

router = APIRouter(prefix="/profissional_servico", tags=["profissional_servico"])

# CREATE
@router.post("/", response_model=ProfissionalServicoResponse)
async def criar_profissional_servico(
    profissional_servico_data: ProfissionalServicoCreate,
    db: AsyncSession = Depends(get_db)
):
    # verificar se o vínculo já existe par não dubplicar
    existing_link = await db.execute(
        select(ProfissionalServico).where(
            ProfissionalServico.id_profissional == profissional_servico_data.id_profissional,
            ProfissionalServico.id_servico == profissional_servico_data.id_servico
        )
    )
    if existing_link.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Vínculo entre profissional e serviço já existe.")

    novo_profissional_servico = ProfissionalServico(
        id_profissional=profissional_servico_data.id_profissional,
        id_servico=profissional_servico_data.id_servico,
        tempo_personalizado_minutos=profissional_servico_data.tempo_personalizado_minutos
    )
    db.add(novo_profissional_servico)
    await db.commit()
    await db.refresh(novo_profissional_servico)
    return novo_profissional_servico

# READ (LIST)
@router.get("/", response_model=list[ProfissionalServicoResponse])
async def listar_profissionais_servicos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProfissionalServico))
    return result.scalars().all()

# READ (SINGLE)
@router.get("/{profissional_servico_id}", response_model=ProfissionalServicoResponse)
async def buscar_profissional_servico(
    profissional_servico_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProfissionalServico).where(ProfissionalServico.id == profissional_servico_id)
    )
    profissional_servico_db = result.scalar_one_or_none()
    if not profissional_servico_db:
        raise HTTPException(status_code=404, detail="Associação Profissional-Serviço não encontrada")
    return profissional_servico_db

# UPDATE
@router.put("/{profissional_servico_id}", response_model=ProfissionalServicoResponse)
async def atualizar_profissional_servico(
    profissional_servico_id: int,
    profissional_servico_data: ProfissionalServicoCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProfissionalServico).where(ProfissionalServico.id == profissional_servico_id)
    )
    profissional_servico_db = result.scalar_one_or_none()

    if not profissional_servico_db:
        raise HTTPException(status_code=404, detail="Associação Profissional-Serviço não encontrada")

    profissional_servico_db.id_profissional = profissional_servico_data.id_profissional
    profissional_servico_db.id_servico = profissional_servico_data.id_servico
    profissional_servico_db.tempo_personalizado_minutos = profissional_servico_data.tempo_personalizado_minutos

    await db.commit()
    await db.refresh(profissional_servico_db)
    return profissional_servico_db

# DELETE
@router.delete("/{profissional_servico_id}")
async def deletar_profissional_servico(
    profissional_servico_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProfissionalServico).where(ProfissionalServico.id == profissional_servico_id)
    )
    profissional_servico_db = result.scalar_one_or_none()

    if not profissional_servico_db:
        raise HTTPException(status_code=404, detail="Associação Profissional-Serviço não encontrada")

    await db.delete(profissional_servico_db)
    await db.commit()
    return {"message": "Associação Profissional-Serviço deletada com sucesso"}
