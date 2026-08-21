# week1/chatbot.py
# Objetivo: fechar a Semana 1 juntando os dois exercícios anteriores —
# streaming (resposta aparecendo aos poucos) + histórico de conversa
# (lista de messages acumulando) — dentro de um loop interativo de verdade.

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

SYSTEM_PROMPT = """Você é o assistente de atendimento do DistributedOrderSystem,
um sistema de pedidos distribuído com microserviços em .NET/C#.
Ajude o usuário com dúvidas sobre pedidos, status, cancelamentos e o
funcionamento do sistema. Responda sempre em português, de forma direta."""

# Mesma ideia do conversation_history.py: essa lista é o "estado" da
# conversa inteira, mantida do lado do CLIENTE (aqui, no seu script),
# não do lado do servidor.
messages = []

print("=== Chatbot de Pedidos — DistributedOrderSystem ===")
print("Digite 'sair' para encerrar.\n")

while True:
    user_input = input("Você: ").strip()

    if user_input.lower() in ("sair", "exit", "quit"):
        print("Até mais!")
        break

    if not user_input:
        # Ignora Enter vazio, não gasta uma chamada de API à toa.
        continue

    # Mesmo padrão do conversation_history.py: adiciona a pergunta
    # ANTES de chamar a API.
    messages.append({"role": "user", "content": user_input})

    print("Assistente: ", end="", flush=True)

    # Mesmo padrão do streaming_call.py: abre o stream, imprime pedaço
    # a pedaço, e só depois do "for" terminar é que pega o objeto final.
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,  # manda o histórico inteiro, não só a pergunta nova
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

        final_message = stream.get_final_message()

    # Pega o texto completo da resposta (já reconstruído pelo SDK a
    # partir dos pedaços do stream) e adiciona no histórico — assim a
    # PRÓXIMA pergunta do usuário já carrega essa resposta como contexto.
    resposta_completa = final_message.content[0].text
    messages.append({"role": "assistant", "content": resposta_completa})

    print(f"\n   (tokens: {final_message.usage.input_tokens} in / {final_message.usage.output_tokens} out | mensagens no histórico: {len(messages)})\n")