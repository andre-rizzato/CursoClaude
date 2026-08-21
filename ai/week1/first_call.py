# week1/first_call.py
# Objetivo: primeira chamada à API da Anthropic — chamada "normal",
# sem streaming. Espera a resposta inteira pronta antes de mostrar algo.

import os
# Biblioteca nativa do Python (vem junto com o interpretador, sem instalar nada).
# Aqui ela é usada indiretamente pelo load_dotenv() para ler variáveis de ambiente.

from anthropic import Anthropic
# Importa a classe principal do SDK oficial da Anthropic.
# É essa classe que sabe conversar com api.anthropic.com.

from dotenv import load_dotenv
# Do pacote python-dotenv: função que lê o arquivo .env e injeta
# as variáveis dele no ambiente do processo, como se você tivesse
# exportado ANTHROPIC_API_KEY manualmente no terminal.

load_dotenv()
# Executa a leitura do .env agora. Precisa vir ANTES de criar o client,
# senão a chave ainda não vai estar disponível quando o Anthropic() for criado.

client = Anthropic()
# Cria o cliente da API. Ele procura sozinho a variável de ambiente
# ANTHROPIC_API_KEY (não precisa passar a chave na mão aqui no código —
# é assim que evitamos deixar a chave hardcoded, um risco de segurança).

response = client.messages.create(
    # client.messages.create() faz uma chamada "normal": a chamada só
    # retorna quando a resposta INTEIRA já estiver pronta do lado do
    # servidor. Diferente do streaming, aqui não tem nada aparecendo
    # aos poucos — você espera em silêncio e recebe tudo de uma vez.

    model="claude-sonnet-4-6",
    # Qual modelo vai gerar a resposta.

    max_tokens=1024,
    # Teto máximo de tokens de saída. Se a resposta natural do modelo
    # for maior que isso, ela é cortada no meio, sem aviso no texto —
    # foi exatamente o que aconteceu na primeira vez que você rodou
    # esse script (Output: 1024, resposta cortada em "Sistema pequeno").

    system="""Você é um assistente especializado no sistema DistributedOrderSystem.
    Esse sistema gerencia pedidos distribuídos com microserviços em .NET/C#.
    Responda sempre em português.""",
    # Instrução fixa que define o "papel" do modelo nessa conversa.
    # É reenviada em toda chamada — a API não tem memória própria entre
    # chamadas, então cada requisição carrega o system prompt inteiro de novo.

    messages=[
        {"role": "user", "content": "O que é um sistema de pedidos distribuído e quais são os principais desafios?"}
    ]
    # Lista de mensagens da conversa. Cada item tem um "role" (quem fala:
    # "user" ou "assistant") e um "content" (o texto). Por enquanto só
    # tem uma pergunta do usuário — sem histórico de rodadas anteriores.
)

print(response.content[0].text)
# response.content é uma LISTA de blocos de conteúdo, não um texto direto.
# Isso existe porque uma resposta pode ter mais de um bloco (por exemplo,
# texto + uma chamada de ferramenta, quando chegarmos em tool use).
# Por enquanto, com uma pergunta simples, só existe o bloco [0], de texto,
# e ".text" pega a string de dentro dele.

print(f"\n--- Uso de tokens ---")
# \n pula uma linha, só pra separar visualmente do texto da resposta.

print(f"Input:  {response.usage.input_tokens}")
# Quantos tokens entraram: system prompt + pergunta do usuário somados.

print(f"Output: {response.usage.output_tokens}")
# Quantos tokens o modelo gerou na resposta.

print(f"Motivo de parada: {response.stop_reason}")
# Explica POR QUE o modelo parou de gerar. Mesmo campo que já
# imprimimos no streaming_call.py — aqui ele já vem pronto no
# objeto "response", sem precisar esperar um stream terminar.
# "end_turn"   = terminou naturalmente, respondeu tudo que tinha a dizer.
# "max_tokens" = foi cortado, bateu no teto configurado acima.
# Se você rodar de novo aquela primeira pergunta ampla (desafios de
# sistemas distribuídos), deve ver "max_tokens" aqui — foi o que
# aconteceu na sua primeira execução deste script.