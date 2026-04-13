from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.deps import get_db
from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/cliente", tags=["cliente"])

# CREATE
@router.post("/", response_model=ClienteResponse)
async def criar_cliente(cliente_data: ClienteCreate, db: AsyncSession = Depends(get_db)):
    novo_cliente = Cliente(
        nome=cliente_data.nome,
        profissional_preferido=cliente_data.profissional_preferido,
        telefone=cliente_data.telefone
    )
    db.add(novo_cliente)
    await db.commit()
    await db.refresh(novo_cliente)
    return novo_cliente

# READ (LIST)
@router.get("/", response_model=list[ClienteResponse])
async def listar_clientes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente))
    return result.scalars().all()

# READ (SINGLE)
@router.get("/{cliente_id}", response_model=ClienteResponse)
async def buscar_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente_db = result.scalar_one_or_none()
    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente_db

# UPDATE
@router.put("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(cliente_id: int, cliente_data: ClienteCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente_db = result.scalar_one_or_none()

    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente_db.nome = cliente_data.nome
    cliente_db.profissional_preferido = cliente_data.profissional_preferido
    cliente_db.telefone = cliente_data.telefone

    await db.commit()
    await db.refresh(cliente_db)
    return cliente_db

# DELETE
@router.delete("/{cliente_id}")
async def deletar_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente_db = result.scalar_one_or_none()

    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    await db.delete(cliente_db)
    await db.commit()
    return {"message": "Cliente deletado com sucesso"}
