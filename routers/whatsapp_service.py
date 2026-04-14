import requests

# Dica: É uma boa prática puxar esses valores do seu arquivo .env usando o os.getenv()
#EVOLUTION_URL = "http://localhost:8080"  # Veja o aviso importante abaixo sobre o localhost!
API_KEY = "12345"
#NOME_INSTANCIA = "nome-da-sua-instancia"  # Substitua pelo nome que você criou no Manager
EVOLUTION_URL='http://localhost:8080'
NOME_INSTANCIA='Tetrix_Bot'

def enviar_mensagem_whatsapp(numero_destino: str, texto: str):
    """
    Envia uma mensagem de texto via WhatsApp usando a Evolution API.
    """
    url = f"{EVOLUTION_URL}/message/sendText/{NOME_INSTANCIA}"

    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "number": numero_destino,
        "options": {
            "delay": 1200,
            "presence": "composing",
            "linkPreview": False
        },
        "text": texto
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        # Levanta um erro se o status code não for 200/201
        response.raise_for_status()

        print("✅ Mensagem enviada com sucesso!")
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        # Se houver uma resposta de erro da Evolution (como aquele erro do "text"), isso ajuda a depurar:
        if hasattr(e, 'response') and e.response is not None:
            print(f"Detalhes do erro: {e.response.text}")
        return None

def enviar_mensagem_grupo(id_grupo: str, texto: str):
    # A rota é a mesma de enviar mensagem normal!
    url = f"{EVOLUTION_URL}/message/sendText/{NOME_INSTANCIA}"
    headers = {"apikey": "12345"}

    payload = {
        # Aqui entra o código gigante que termina em @g.us
        "number": id_grupo,
        "options": {
            "delay": 1500,
            "presence": "composing"  # Vai mostrar "Tetrix está digitando..." no grupo todo
        },
        "text": texto
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


# Testando
meu_grupo_id = "120363123456789012@g.us"
mensagem = "⚠️ *Aviso do Sistema:* Reunião começando em 15 minutos!"
enviar_mensagem_grupo(meu_grupo_id, mensagem)