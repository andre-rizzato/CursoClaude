"""
Semana 2 - Exercício 2: Similaridade semântica
Objetivo: encontrar o pedido mais relacionado a uma consulta usando
similaridade de cosseno entre embeddings.

Teoria em uma frase:
embedding transforma cada texto em um ponto em um espaco com muitas
dimensoes; a similaridade de cosseno mede o angulo entre dois pontos.

Por que medir o angulo?
O tamanho absoluto do vetor pode variar, mas a direcao representa o padrao
semantico aprendido pelo modelo. Dois textos com significado parecido tendem
a apontar para direcoes parecidas, produzindo um score proximo de 1.
"""

# math fornece a raiz quadrada usada para calcular a norma de cada vetor.
import math
# os permite ler a chave da API a partir de uma variavel de ambiente.
import os

# load_dotenv carrega as variaveis definidas no arquivo ai/.env.
from dotenv import load_dotenv

# voyageai e o SDK usado para pedir embeddings ao modelo Voyage.
import voyageai

# Procura o arquivo .env no diretorio atual e nos diretorios pai.
load_dotenv()

# Cria o cliente autenticado. A chave nunca deve ficar escrita no codigo.
client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

# Estes sao os documentos que poderiam estar armazenados em um indice vetorial.
pedidos = [
    "O cliente cancelou o pedido porque o prazo de entrega estava muito longo.",
    "O pagamento do pedido foi recusado pelo gateway.",
    "O cliente quer saber quando o pedido será entregue.",
    "O produto chegou danificado e o cliente solicitou uma troca.",
]

# Esta e a pergunta que queremos comparar com os pedidos armazenados.
consulta = "Quero acompanhar a entrega do meu pedido."

# Gera um vetor para cada pedido. Um embedding e uma lista de numeros reais
# que representa o significado do texto em um espaco de 1024 dimensoes.
embeddings_pedidos = client.embed(
    texts=pedidos,
    model="voyage-4-lite",
    input_type="document",
).embeddings

# Gera o vetor da busca separadamente. "query" informa ao modelo que este
# texto sera usado para procurar documentos, e nao para ser armazenado.
embedding_consulta = client.embed(
    texts=[consulta],
    model="voyage-4-lite",
    input_type="query",
).embeddings[0]


# A similaridade de cosseno e definida por:
#
#   cos(theta) = (A . B) / (||A|| * ||B||)
#
# A . B e o produto escalar: multiplica as coordenadas correspondentes e
# soma os resultados. Ele indica o quanto os vetores apontam na mesma direcao.
# ||A|| e ||B|| sao as normas, isto e, o comprimento de cada vetor.
# Dividir pelas normas remove o efeito do tamanho e deixa a direcao dominar.
def similaridade_cosseno(primeiro_vetor, segundo_vetor):
    # zip junta a coordenada 1 de cada vetor, depois a 2, e assim por diante.
    # Como os vetores tem 1024 coordenadas, o produto usa todas elas.
    produto_escalar = sum(
        primeiro * segundo
        for primeiro, segundo in zip(primeiro_vetor, segundo_vetor)
    )

    # A norma euclidiana e a raiz da soma dos quadrados das coordenadas:
    # ||A|| = sqrt(a1^2 + a2^2 + ... + a1024^2).
    norma_primeiro = math.sqrt(sum(valor * valor for valor in primeiro_vetor))
    norma_segundo = math.sqrt(sum(valor * valor for valor in segundo_vetor))

    # O resultado normalmente fica entre -1 e 1:
    #  1  = mesma direcao, alta semelhanca
    #  0  = pouca relacao direcional
    # -1  = direcoes opostas
    # Em embeddings de texto, scores positivos sao comuns; o valor nao e uma
    # probabilidade, nem significa "61.60% de chance".
    return produto_escalar / (norma_primeiro * norma_segundo)


# Calcula um score para cada par (consulta, pedido) e guarda o texto junto.
resultados = [
    (similaridade_cosseno(embedding_consulta, embedding_pedido), pedido)
    for pedido, embedding_pedido in zip(pedidos, embeddings_pedidos)
]

# Maior score vem primeiro: esse e o ranking da busca semantica.
resultados.sort(reverse=True)

# Exibe a consulta para deixar claro o que foi pesquisado.
print(f"Consulta: {consulta}\n")
# enumerate fornece a posicao humana do resultado: 1, 2, 3 e 4.
for posicao, (score, pedido) in enumerate(resultados, start=1):
    # :.4f mostra exatamente quatro casas decimais para facilitar a leitura.
    print(f"{posicao}. {score:.4f} - {pedido}")