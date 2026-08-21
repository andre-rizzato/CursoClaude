# week1/streaming_call.py
# Objetivo: mesma chamada do first_call.py, mas com streaming —
# o texto aparece aos poucos, palavra por palavra, em vez de tudo de uma vez.

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

with client.messages.stream(
    # client.messages.stream() abre uma conexão de streaming com a API.
    # Diferente do client.messages.create() do first_call.py, que espera
    # a resposta inteira, esse aqui vai entregando pedaços conforme chegam.
    # Usamos "with" porque essa conexão é um recurso que precisa ser
    # aberto e fechado corretamente — o "with" garante o fechamento
    # automático mesmo se der erro no meio do caminho.

    model="claude-sonnet-4-6",
    # Qual modelo vai gerar a resposta. Mesmo modelo do first_call.py.

    max_tokens=1024,
    # Teto máximo de tokens de saída. Lembra do exercício anterior:
    # se a resposta natural for maior que isso, ela é cortada no meio.

    system="""Você é um assistente especializado no sistema DistributedOrderSystem.
    Esse sistema gerencia pedidos distribuídos com microserviços em .NET/C#.
    Responda sempre em português.""",
    # Instrução fixa que define o "papel" do modelo nessa conversa.
    # É reenviada em toda chamada — a API não guarda isso de um lado pro outro.

    messages=[
        {"role": "user", "content": "Explique em poucas linhas o que é o padrão SAGA e por que ele é relevante para o DistributedOrderSystem."}
    ]
    # Lista de mensagens da conversa. Por enquanto só tem uma pergunta do usuário.
    # Na Semana 1 ainda vamos chegar no exercício de manter histórico aqui,
    # acumulando várias mensagens nessa lista a cada rodada.

) as stream:
    # O "as stream" guarda o objeto de streaming numa variável,
    # disponível só dentro deste bloco "with".

    for text in stream.text_stream:
        # stream.text_stream é um iterador: a cada volta do loop,
        # ele entrega o próximo pedacinho de texto que chegou da API,
        # não a resposta inteira de uma vez.

        print(text, end="", flush=True)
        # end="" evita pular linha a cada pedaço (senão o texto ficaria
        # quebrado, um pedaço por linha, em vez de fluir naturalmente).
        # flush=True força o terminal a mostrar o texto na hora,
        # em vez de guardar num buffer interno e só mostrar depois.

    final_message = stream.get_final_message()
    # Só é possível chamar isso DEPOIS que o "for" acima terminou,
    # ou seja, depois que todo o streaming já foi recebido.
    # Ele devolve o objeto de resposta completo, com os metadados
    # que não vêm junto com o texto pedaço a pedaço (usage, stop_reason).

print(f"\n\n--- Uso de tokens ---")
# \n\n pula duas linhas, só pra separar visualmente do texto que
# acabou de ser impresso, sem quebra de linha, lá em cima.

print(f"Input:  {final_message.usage.input_tokens}")
print(f"Output: {final_message.usage.output_tokens}")
# Mesma ideia do first_call.py: quantos tokens entraram e saíram.

print(f"Motivo de parada: {final_message.stop_reason}")
# Novo em relação ao first_call.py: mostra POR QUE o modelo parou.
# "end_turn" = terminou naturalmente.
# "max_tokens" = foi cortado, bateu no teto que configuramos acima.