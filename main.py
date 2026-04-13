from fastapi import FastAPI
from routers import cliente_router, agendamento_router, profissional_router, servico_router, salao_router

app = FastAPI()
app.include_router(cliente_router.router)
app.include_router(agendamento_router.router)
app.include_router(profissional_router.router)
app.include_router(servico_router.router)
app.include_router(salao_router.router)