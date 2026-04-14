from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from routers.whatsapp_service import enviar_mensagem_whatsapp, enviar_mensagem_grupo

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


# Modelo de dados que sua API Tetrix vai receber
class MensagemRequest(BaseModel):
    telefone: str
    mensagem: str
# 2. Depois criamos a classe principal que engloba tudo
class EvolutionMessageRequest(BaseModel):
    number: str
    text: str


@router.post("/notificar-cliente")
def notificar_cliente(dados: MensagemRequest):
    # Chama o Evolution API para fazer o disparo
    resultado = enviar_mensagem_whatsapp(dados.telefone, dados.mensagem)

    if resultado:
        return {"status": "sucesso", "detalhe": "WhatsApp disparado!"}
    else:
        return {"status": "erro", "detalhe": "Falha na comunicação com o WhatsApp"}

@router.post("/notificar-grupo")
def notificar_grupo(dados: EvolutionMessageRequest):
    # Chama o Evolution API para fazer o disparo
    resultado = enviar_mensagem_grupo(dados.number, dados.text)

    if resultado:
        return {"status": "sucesso", "detalhe": "WhatsApp disparado!"}
    else:
        return {"status": "erro", "detalhe": "Falha na comunicação com o WhatsApp"}