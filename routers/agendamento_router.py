from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.deps import get_db
from models.agendamento import Agendamento
from models.profissional import Profissional
from models.servico import Servico
from schemas.agendamento import AgendamentoCreate, AgendamentoResponse
from datetime import timedelta

router = APIRouter(prefix="/agendamento", tags=["agendamento"])

# CREATE
@router.post("/", response_model=AgendamentoResponse)
async def criar_agendamento(agendamento_data: AgendamentoCreate, db: AsyncSession = Depends(get_db)):
    # Buscar o serviço para obter o tempo_estimado_minutos
    servico_result = await db.execute(select(Servico).where(Servico.id == agendamento_data.id_servico))
    servico_db = servico_result.scalar_one_or_none()

    if not servico_db:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    # Buscar o profissional para verificar se existe
    profissional_result = await db.execute(select(Profissional).where(Profissional.id == agendamento_data.id_profissional))
    profissional_db = profissional_result.scalar_one_or_none()

    if not profissional_db:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    # Calcular data_hora_fim
    data_hora_fim = agendamento_data.data_hora_inicio + timedelta(minutes=servico_db.tempo_estimado_minutos)

    novo_agendamento = Agendamento(
        id_cliente=agendamento_data.id_cliente,
        id_servico=agendamento_data.id_servico,
        id_profissional=agendamento_data.id_profissional,
        data_hora_inicio=agendamento_data.data_hora_inicio,
        data_hora_fim=data_hora_fim,
        status=agendamento_data.status,
        sugerido_pelo_tetrix=False # Valor padrão, pode ser alterado se houver lógica para isso
    )
    db.add(novo_agendamento)
    await db.commit()
    await db.refresh(novo_agendamento)
    return novo_agendamento

# READ (LIST)
@router.get("/", response_model=list[AgendamentoResponse])
async def listar_agendamentos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agendamento))
    return result.scalars().all()

# READ (SINGLE)
@router.get("/{agendamento_id}", response_model=AgendamentoResponse)
async def buscar_agendamento(agendamento_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agendamento).where(Agendamento.id == agendamento_id))
    agendamento_db = result.scalar_one_or_none()
    if not agendamento_db:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento_db

# UPDATE
@router.put("/{agendamento_id}", response_model=AgendamentoResponse)
async def atualizar_agendamento(agendamento_id: int, agendamento_data: AgendamentoCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agendamento).where(Agendamento.id == agendamento_id))
    agendamento_db = result.scalar_one_or_none()

    if not agendamento_db:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    # Buscar o serviço para obter o tempo_estimado_minutos, caso o serviço tenha sido alterado
    if agendamento_data.id_servico != agendamento_db.id_servico:
        servico_result = await db.execute(select(Servico).where(Servico.id == agendamento_data.id_servico))
        servico_db = servico_result.scalar_one_or_none()
        if not servico_db:
            raise HTTPException(status_code=404, detail="Novo serviço não encontrado")
        agendamento_db.data_hora_fim = agendamento_data.data_hora_inicio + timedelta(minutes=servico_db.tempo_estimado_minutos)
    elif agendamento_data.data_hora_inicio != agendamento_db.data_hora_inicio:
        # Se a hora de início mudou, mas o serviço não, recalcular data_hora_fim com o serviço atual
        servico_result = await db.execute(select(Servico).where(Servico.id == agendamento_db.id_servico))
        servico_db = servico_result.scalar_one_or_none()
        if servico_db: # Deveria sempre existir, mas é bom verificar
            agendamento_db.data_hora_fim = agendamento_data.data_hora_inicio + timedelta(minutes=servico_db.tempo_estimado_minutos)


    agendamento_db.id_cliente = agendamento_data.id_cliente
    agendamento_db.id_servico = agendamento_data.id_servico
    agendamento_db.id_profissional = agendamento_data.id_profissional
    agendamento_db.data_hora_inicio = agendamento_data.data_hora_inicio
    agendamento_db.status = agendamento_data.status
    # sugerido_pelo_tetrix não é atualizado via PUT, pois é um campo interno

    await db.commit()
    await db.refresh(agendamento_db)
    return agendamento_db

# DELETE
@router.delete("/{agendamento_id}")
async def deletar_agendamento(agendamento_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agendamento).where(Agendamento.id == agendamento_id))
    agendamento_db = result.scalar_one_or_none()

    if not agendamento_db:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    await db.delete(agendamento_db)
    await db.commit()
    return {"message": "Agendamento deletado com sucesso"}
