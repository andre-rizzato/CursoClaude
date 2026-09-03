"""
============================================================================
SEMANA 2 - EXERCICIO 3: semantica vence o lexico? (experimento controlado)
DistributedOrderSystem / ai / week2
============================================================================

PROBLEMA QUE ESTE ARQUIVO RESOLVE
---------------------------------
No exercicio anterior, a nota mais parecida SEMANTICAMENTE com a consulta
era tambem a mais parecida LEXICALMENTE (compartilhava "pedido" e "entregue").

As duas hipoteses previam o mesmo resultado:

    H1 (lexical)  : "ganhou porque repete as palavras da consulta"
    H2 (semantica): "ganhou porque significa a mesma coisa"

Um experimento em que duas hipoteses preveem o mesmo resultado nao decide
nada. Chama-se experimento confundido. Este arquivo desconfunde.

COMO
    Item 1 -> responde a consulta SEM compartilhar vocabulario
    Item 2 -> compartilha vocabulario MAS nao responde nada

    Se rank(1) > rank(2)  -> H1 refutada. A semantica manda.
    Se rank(2) > rank(1)  -> o modelo nao sustenta a inferencia.
                             Tambem e resultado: testar voyage-4-large.

Rodamos as duas metricas lado a lado. A tabela e o argumento.
============================================================================
"""

import math
import os

import voyageai
from dotenv import load_dotenv

load_dotenv()

MODELO = "voyage-4-large"


# ===========================================================================
# 1. OS DADOS
# ===========================================================================
# Notas de atendimento ancoradas nos status reais de OrderStatus.cs.
#
# O status NAO entra no embedding. Ele e dado estruturado:
#
#     status -> WHERE status = 'Shipped'    (indice, exato, barato)
#     nota   -> busca por similaridade      (vetor, aproximado, caro)
#
# Embedar a palavra "Shipped" sozinha produziria um vetor numa regiao
# arbitraria do espaco: e um token solto em ingles, sem contexto, e o
# modelo nunca viu pares de treino com ele nesse papel.
#
# Combinar os dois caminhos e hybrid search (Fase 3). O status fica aqui
# so para o dia em que o filtro entrar.
# ===========================================================================

CONSULTA = "Quero acompanhar a entrega do meu pedido"

NOTAS = [
    {
        "id": 1,
        "status": "Shipped",
        "papel": "experimento: responde, zero lexico",
        "texto": "Saiu do centro de distribuicao ontem, previsao de dois a tres dias uteis.",
    },
    {
        "id": 2,
        "status": "Delivered",
        "papel": "experimento: lexico alto, sentido errado",
        "texto": "A entrega do pedido foi feita no endereco errado e quero devolver.",
    },
    {
        "id": 3,
        "status": "Shipped",
        "papel": "parafrase, vocabulario distinto",
        "texto": "Onde esta minha encomenda? Ja faz uma semana.",
    },
    {
        "id": 4,
        "status": "Confirmed",
        "papel": "controle (confundido de proposito)",
        "texto": "O cliente quer saber quando o pedido sera entregue.",
    },
    {
        "id": 5,
        "status": "Pending",
        "papel": "distrator lexical",
        "texto": "O pagamento do pedido foi recusado pelo cartao.",
    },
    {
        "id": 6,
        "status": "Cancelled",
        "papel": "distrator limpo (piso de sanidade)",
        "texto": "Cancelei porque encontrei mais barato em outro site.",
    },
]


# ===========================================================================
# 2. BASELINE LEXICAL: indice de Jaccard
# ===========================================================================
# Precisamos de um numero que represente H1 para poder compara-lo.
# Jaccard mede sobreposicao de conjuntos de palavras:
#
#           |A INTERSECAO B|
#   J(A,B) = ----------------
#           |A UNIAO B|
#
# Termo a termo:
#   |A INTERSECAO B| -> quantas palavras aparecem nos DOIS textos
#   |A UNIAO B|      -> quantas palavras distintas existem no total
#   a divisao        -> normaliza pelo tamanho, senao textos longos ganham
#
# Exemplo minusculo, com a conta a mostra:
#
#   A = "quero cancelar pedido"   -> {quero, cancelar, pedido}
#   B = "quero rastrear pedido"   -> {quero, rastrear, pedido}
#
#   intersecao = {quero, pedido}                  -> 2
#   uniao      = {quero, cancelar, rastrear, pedido} -> 4
#   J = 2 / 4 = 0.50
#
# Repare: 0.50 e ALTO, e os dois textos pedem coisas OPOSTAS.
# Esse e precisamente o buraco que embeddings existem para tapar.
#
# Jaccard e um primo pobre do BM25 do seu Elasticsearch: mesma familia
# (sobreposicao de termos), sem a ponderacao por raridade. Serve aqui
# porque queremos o sinal puramente lexical, sem sofisticacao.
# ===========================================================================

# Sem esta lista, o baseline mede GRAMATICA, nao vocabulario.
# Descoberto rodando: duas notas sem nenhuma relacao casavam em "do" e "a",
# e o Jaccard saiu invertido em relacao ao esperado.
#
# E exatamente o buraco que o BM25 do Elasticsearch tapa com IDF: termos
# que aparecem em quase todo documento recebem peso proximo de zero
# automaticamente, sem lista manual. Aqui a lista e manual porque o
# objetivo e ver o mecanismo, nao ter o melhor baseline.
STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "de", "do", "da", "dos", "das",
    "no", "na", "nos", "nas", "em", "e", "que", "por", "para", "com",
    "meu", "minha", "seu", "sua", "ao", "aos", "se", "foi",
}


def tokenizar(texto: str) -> set:
    """Minusculas, sem pontuacao, sem stopwords. Devolve conjunto."""
    limpo = "".join(c if c.isalnum() or c.isspace() else " " for c in texto.lower())
    return {p for p in limpo.split() if p not in STOPWORDS}


def jaccard(texto_a: str, texto_b: str) -> float:
    a, b = tokenizar(texto_a), tokenizar(texto_b)
    uniao = a | b
    if not uniao:
        return 0.0
    return len(a & b) / len(uniao)


# ===========================================================================
# 3. SIMILARIDADE DE COSSENO, NA MAO
# ===========================================================================
#                     A . B
#   cos(theta) = ---------------
#                 ||A|| * ||B||
#
# Termo a termo:
#   A . B    -> soma dos produtos coordenada a coordenada. Cresce quando os
#               vetores apontam junto, encolhe quando divergem.
#   ||A||    -> comprimento (norma) de A: raiz da soma dos quadrados.
#   dividir  -> remove o efeito do comprimento. Sobra so a DIRECAO.
#
# Por que direcao e nao comprimento: a norma correlaciona com tamanho do
# texto, nao com significado. Duas frases sobre entrega, uma de 5 e outra
# de 50 palavras, apontam pro mesmo lado com normas diferentes.
#
# Exemplo minusculo, com a conta a mostra:
#
#   A = (1, 0)      B = (1, 1)
#
#   A . B  = 1*1 + 0*1 = 1
#   ||A||  = raiz(1 + 0) = 1
#   ||B||  = raiz(1 + 1) = 1.4142
#
#   cos = 1 / (1 * 1.4142) = 0.7071
#
# Confere pela trigonometria: (1,1) forma 45 graus com o eixo horizontal,
# e cos(45) = 0.7071. E a MESMA funcao do triangulo retangulo. Dois
# vetores sempre definem um plano, mesmo vindo de 1024 dimensoes, e o
# angulo e medido dentro desse plano.
#
# NUMPY faz isso 100x mais rapido com np.dot (BLAS vetorizado).
# Aqui a conta fica visivel de proposito. Em producao, troque - e saiba
# por que trocou.
# ===========================================================================

def produto_escalar(a: list, b: list) -> float:
    return sum(x * y for x, y in zip(a, b))


def norma(v: list) -> float:
    return math.sqrt(sum(x * x for x in v))


def cosseno(a: list, b: list) -> float:
    denominador = norma(a) * norma(b)
    if denominador == 0:
        # O vetor zero nao tem direcao, logo nao tem angulo com nada.
        # E o unico input que quebra esta funcao.
        raise ValueError("Vetor de norma zero: cosseno indefinido.")
    return produto_escalar(a, b) / denominador


# ===========================================================================
# 4. GERACAO DOS EMBEDDINGS
# ===========================================================================
# input_type existe porque RETRIEVAL E ASSIMETRICO.
#
# Uma pergunta e a sua resposta NAO sao textos parecidos:
#
#   pergunta : "Qual o prazo de entrega?"
#   resposta : "Chega em ate tres dias uteis."
#
# Zero palavras em comum, estruturas diferentes. Embedados do mesmo jeito,
# a pergunta se aproxima de OUTRAS PERGUNTAS sobre prazo - nao da resposta.
#
# A Voyage resolve prefixando o texto antes de vetorizar:
#
#   input_type="query"    -> "Represent the query for retrieving supporting
#                             documents: " + seu texto
#   input_type="document" -> "Represent the document for retrieval: "
#                             + seu texto
#
# Mesmo texto, instrucao diferente sobre o PAPEL. Vetores compativeis entre
# si, mas nao identicos. Trocar isso depois da indexacao degrada a busca
# em silencio - sem erro, sem excecao, so resultado pior.
#
# Uma chamada com a lista inteira, nao uma por texto em loop. Latencia e
# quota sao por requisicao.
# ===========================================================================

def gerar_embeddings(cliente):
    textos = [n["texto"] for n in NOTAS]

    docs = cliente.embed(texts=textos, model=MODELO, input_type="document").embeddings
    query = cliente.embed(texts=[CONSULTA], model=MODELO, input_type="query").embeddings[0]

    return query, docs


# ===========================================================================
# 5. EXECUCAO
# ===========================================================================

def main():
    if not os.getenv("VOYAGE_API_KEY"):
        raise SystemExit("VOYAGE_API_KEY ausente. Confira o .env em ai/.")

    cliente = voyageai.Client()
    vetor_consulta, vetores_notas = gerar_embeddings(cliente)

    # -----------------------------------------------------------------
    # 5.1 Verificacao da norma
    # -----------------------------------------------------------------
    # A Voyage devolve vetores normalizados. Se ||v|| = 1, os dois
    # denominadores da formula do cosseno valem 1, e o cosseno E o
    # produto escalar puro. As divisoes acima ficam corretas mas
    # redundantes. Meca, nao acredite.
    # -----------------------------------------------------------------
    print(f"Modelo: {MODELO}")
    print(f"Dimensoes: {len(vetor_consulta)}")
    print(f"Norma da consulta: {norma(vetor_consulta):.6f}")
    print(f"Norma da nota 1:   {norma(vetores_notas[0]):.6f}")
    print()
    print(f"Consulta: {CONSULTA}")
    print()

    # -----------------------------------------------------------------
    # 5.2 As duas metricas, lado a lado
    # -----------------------------------------------------------------
    resultados = []
    for nota, vetor in zip(NOTAS, vetores_notas):
        resultados.append({
            "id": nota["id"],
            "status": nota["status"],
            "papel": nota["papel"],
            "texto": nota["texto"],
            "cos": cosseno(vetor_consulta, vetor),
            "jac": jaccard(CONSULTA, nota["texto"]),
        })

    # Ordenacao com chave EXPLICITA.
    # sort(reverse=True) em tuplas cai no segundo elemento em caso de
    # empate e compara strings - ordenacao alfabetica silenciosa. Pior:
    # quebra com TypeError quando o segundo elemento vira dict.
    por_cos = sorted(resultados, key=lambda r: r["cos"], reverse=True)
    por_jac = sorted(resultados, key=lambda r: r["jac"], reverse=True)

    print("RANKING SEMANTICO (cosseno)          RANKING LEXICAL (Jaccard)")
    print("-" * 76)
    for pos, (c, j) in enumerate(zip(por_cos, por_jac), start=1):
        esq = f"{pos}. #{c['id']} {c['cos']:.4f}"
        dir_ = f"{pos}. #{j['id']} {j['jac']:.4f}"
        print(f"{esq:<36} {dir_}")
    print()

    for r in por_cos:
        print(f"  #{r['id']} [{r['status']:<9}] cos={r['cos']:.4f} jac={r['jac']:.4f}")
        print(f"       {r['texto']}")
        print(f"       ({r['papel']})")
    print()

    # -----------------------------------------------------------------
    # 5.3 Veredito do experimento
    # -----------------------------------------------------------------
    posicao = {r["id"]: i for i, r in enumerate(por_cos)}
    pos_1, pos_2 = posicao[1], posicao[2]

    print("=" * 76)
    print("VEREDITO")
    print("=" * 76)
    print(f"Item 1 (responde, zero lexico)     -> posicao {pos_1 + 1}")
    print(f"Item 2 (lexico alto, sentido errado) -> posicao {pos_2 + 1}")
    print()
    if pos_1 < pos_2:
        print("H1 (lexical) REFUTADA: o item sem palavras em comum ficou acima")
        print("do item que repete o vocabulario da consulta.")
    else:
        print("H1 NAO refutada com este modelo. O voyage-4-lite nao sustentou")
        print("a inferencia. Proximo passo: repetir com voyage-4-large e")
        print("comparar. Isso tambem e resultado.")

    ultimo = por_cos[-1]["id"]
    print()
    print(f"Piso de sanidade: item 6 deveria ser o ultimo. Ultimo = #{ultimo}.")


if __name__ == "__main__":
    main()


# ===========================================================================
# 6. O QUE OBSERVAR AO RODAR
# ===========================================================================
#
# a) A norma. Se der ~1.000000, voce confirmou com o SEU dado que as duas
#    divisoes da formula sao redundantes neste modelo.
#
# b) A coluna Jaccard do item 1. Deve dar 0.0 ou perto: nenhuma palavra
#    da consulta aparece nele. Se o cosseno ainda o colocar no topo, o
#    numero refutou a hipotese - nao a minha opinion.
#
# c) O item 2. Jaccard alto, cosseno que deveria ser medio. E o caso onde
#    o Elasticsearch sozinho erraria.
#
# d) Os dois rankings inteiros. Onde eles DIVERGEM e exatamente o valor
#    que embeddings adicionam ao seu stack atual.
#
# ===========================================================================
# 7. PERGUNTA DE VERIFICACAO
# ===========================================================================
#
# O item 6 ("Cancelei porque encontrei mais barato em outro site") tem
# status Cancelled - terminal na sua maquina de estados.
#
# Suponha que um cliente escreva: "NAO quero cancelar o pedido, quero
# so mudar o endereco."
#
# O que o cosseno vai fazer com o "NAO"? Essa nota vai ficar perto ou
# longe de uma nota sobre cancelamento? Por que?
#
# E a consequencia pratica: se esse agente rodasse em producao no
# DistributedOrderSystem, que erro operacional isso poderia causar,
# dado que Cancelled e um estado TERMINAL?
# ===========================================================================


# ===========================================================================
# 8. APROFUNDAMENTO - respostas objetivas (linguagem simples)
# ===========================================================================
#
# 8.1 Negacao e o estado Cancelled
# ---------------------------------------------------------------------
# Embedding nao entende negacao como logica - entende como PADRAO DE
# PALAVRAS QUE APARECEM JUNTAS. "quero cancelar" e "NAO quero cancelar"
# usam quase o mesmo vocabulario, no mesmo contexto (cancelamento), entao
# ficam PROXIMOS no espaco vetorial mesmo significando o oposto.
#
# Consequencia pratica: Cancelled e estado TERMINAL na maquina de estados
# do pedido (Pending -> Confirmed -> Shipped -> Delivered / Cancelled).
# Se um agente decidisse "isso e sobre cancelamento, vou marcar como
# Cancelled" so com base em similaridade semantica, uma nota do tipo "NAO
# quero cancelar, so mudar o endereco" corre risco de ser tratada como
# pedido de cancelamento - erro operacional grave e IRREVERSIVEL (estado
# terminal). Por isso: status exato SEMPRE vem de filtro estruturado
# (WHERE status = ...), nunca de busca semantica. Busca semantica responde
# "sobre o que e o texto", nao "isso e verdade ou mentira".
#
# 8.2 Por que cosseno, e nao distancia euclidiana
# ---------------------------------------------------------------------
# Distancia euclidiana tambem e afetada pelo TAMANHO (norma) do vetor, nao
# so pela direcao. A norma de um embedding costuma refletir coisas como
# tamanho/intensidade do texto, nao o significado. Exemplo minusculo:
#
#   A = (1, 1)      B = (2, 2)      <- B e A esticado, mesma direcao
#
#   euclidiana = raiz((2-1)^2 + (2-1)^2) = raiz(2) = 1.41   -> "diferente"
#   cosseno    = (1*2 + 1*2) / (raiz(2) * raiz(8)) = 4/4 = 1.0  -> identico
#
# Cosseno ignora o esticamento e compara so a direcao. Por isso e o padrao
# em NLP: significado mora na direcao do vetor, nao no comprimento dele.
#
# 8.3 Cosseno negativo (cos = -1)
# ---------------------------------------------------------------------
# cos=1 -> mesma direcao (significado quase identico)
# cos=0 -> direcoes perpendiculares (sem relacao)
# cos=-1 -> direcoes opostas (significado oposto)
#
# Na pratica, com embeddings de texto, valores perto de -1 quase nunca
# aparecem. Textos com significados opostos tendem a cair perto de 0 (sem
# relacao), nao perto de -1 - porque o modelo foi treinado para AGRUPAR
# textos parecidos, nao para codificar "oposto logico". O espaco vetorial
# nao tem um conceito forte de antonimo.
#
# 8.4 Codigos de erro internos (ex.: ORD_TIMEOUT_502)
# ---------------------------------------------------------------------
# O modelo nao sabe que isso e um identificador interno do seu sistema.
# Ele quebra em pedacos (ORD, TIMEOUT, 502) e gera um vetor a partir de
# associacoes genericas aprendidas no treino ("502" puxa semantica de erro
# HTTP; "TIMEOUT" puxa semantica generica de tempo esgotado) - sem saber o
# que o codigo significa especificamente no DistributedOrderSystem.
#
# Consequencia pratica: nunca indexe o codigo cru. Indexe a descricao em
# linguagem natural (ex.: "ORD_TIMEOUT_502: tempo excedido aguardando
# confirmacao do provedor de pagamento") - ai sim a busca semantica tem
# texto de verdade pra comparar.
# ===========================================================================