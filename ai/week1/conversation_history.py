# week1/conversation_history.py
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

SYSTEM_PROMPT = """Você é um assistente especializado no sistema DistributedOrderSystem.
Esse sistema gerencia pedidos distribuídos com microserviços em .NET/C#.
Responda sempre em português."""

# Essa lista é o "estado" da conversa. Como a API não guarda nada sozinha,
# somos nós que acumulamos aqui cada mensagem trocada — e reenviamos
# a lista inteira a cada chamada nova.
messages = []


def ask(question: str) -> str:
    # 1) Adiciona a pergunta do usuário na lista ANTES de chamar a API.
    messages.append({"role": "user", "content": question})

    # 2) Manda a lista INTEIRA (não só a pergunta nova) — é isso que
    #    dá a ilusão de "memória", já que o modelo em si não lembra de nada.
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages
    )

    answer = response.content[0].text

    # 3) Adiciona a resposta do modelo na lista também — assim ela entra
    #    no histórico e fica disponível pra próxima rodada.
    messages.append({"role": "assistant", "content": answer})

    print(f"\n🧑 Você: {question}")
    print(f"🤖 Claude: {answer}")
    print(f"   (input: {response.usage.input_tokens} tokens | output: {response.usage.output_tokens} tokens | motivo: {response.stop_reason})")

    return answer


# Primeira pergunta: pede uma lista de serviços.
ask("Quais microserviços fazem parte do DistributedOrderSystem? Liste rapidamente, sem se aprofundar.")

# Segunda pergunta: só faz sentido se o modelo lembrar da resposta anterior.
# Repare que "você citou" só existe porque está na lista de messages agora,
# não porque o modelo "lembrou" sozinho.
ask("Dos serviços que você citou, qual é o responsável por reverter uma transação em caso de falha de pagamento?")

print(f"\n--- Histórico final tem {len(messages)} mensagens ---")