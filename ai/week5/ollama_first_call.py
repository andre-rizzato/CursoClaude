"""
ollama_first_call.py
Settimana 5 — Ollama locale via docker-compose

Stesso pattern di ai/week1/first_call.py (system + user message), ma
contro un LLM che gira in un container Docker locale (localhost:11434),
non nella API cloud della Anthropic. Nessuna API key, nessun custo per
chiamata, funziona offline.
"""

import requests

# ---------------------------------------------------------------------
# 1. ENDPOINT LOCAL
# ---------------------------------------------------------------------
# O container do docker-compose expõe a porta 11434. /api/chat aceita o
# mesmo formato messages=[{role, content}] da API da Anthropic — é por
# isso que dá pra comparar diretamente com o first_call.py da Semana 1.
# ---------------------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"


def chat(pergunta: str, system: str = "") -> dict:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": pergunta},
        ],
        "stream": False,
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------
# 2. DEMO — mesma pergunta do first_call.py da Semana 1
# ---------------------------------------------------------------------

if __name__ == "__main__":
    system_prompt = (
        "Voce e um assistente especializado no sistema DistributedOrderSystem. "
        "Esse sistema gerencia pedidos distribuidos com microsservicos em .NET/C#. "
        "Responda sempre em portugues."
    )
    pergunta = "O que e um sistema de pedidos distribuido e quais sao os principais desafios?"

    resultado = chat(pergunta, system_prompt)

    print(resultado["message"]["content"])
    print("\n--- Metricas (Ollama expoe isso; a API cloud nao) ---")
    print(f"Tempo total: {resultado['total_duration'] / 1e9:.2f}s")
    print(f"Tempo de load do modelo na memoria: {resultado['load_duration'] / 1e9:.2f}s")
    print(f"Tokens gerados: {resultado['eval_count']}")


# ---------------------------------------------------------------------
# 3. PERGUNTA DE VERIFICACAO
# ---------------------------------------------------------------------
#
# Roda este script DUAS vezes seguidas e compara o "Tempo de load do
# modelo" entre a 1a e a 2a rodada.
#
# O Ollama mantem o modelo carregado na RAM por OLLAMA_KEEP_ALIVE (5min
# por padrao) depois da 1a chamada. O que voce espera que aconteca com o
# load_duration na 2a rodada, e por que isso nao existe (nem faz sentido)
# quando voce chama a API da Anthropic?
# ---------------------------------------------------------------------
