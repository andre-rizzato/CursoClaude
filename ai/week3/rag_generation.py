"""
rag_generation.py
Settimana 3-4 — RAG da zero: Parte 2 — augmentation + generation ponta a ponta

Completa il pipeline iniziato in rag_chunking_retrieval.py:
chunking -> embedding -> retrieval -> AUGMENTATION -> GENERATION
"""

from anthropic import Anthropic
from dotenv import load_dotenv

from rag_chunking_retrieval import chunk_text, embed_chunks, retrieve

load_dotenv()

anthropic_client = Anthropic()


# ---------------------------------------------------------------------
# 6. AUGMENTATION + GENERATION
# ---------------------------------------------------------------------

def generate_answer(pergunta: str, chunks_recuperados: list[tuple]) -> str:
    """
    Augmentation: monta il prompt finale iniettando i chunk recuperati come
    contesto esplicito.

    Generation: chiama il LLM perché risponda SOLO con base in quel
    contesto — grounding, per ridurre l'allucinazione.
    """
    contexto = "\n".join(f"- {texto}" for _, texto in chunks_recuperados)

    system = (
        "Você responde perguntas sobre pedidos do DistributedOrderSystem "
        "usando APENAS o contexto fornecido pelo usuário. Se a resposta "
        "não estiver no contexto, diga que não há informação suficiente — "
        "nunca invente dados que não apareçam no contexto."
    )

    user_prompt = f"Contexto recuperado:\n{contexto}\n\nPergunta: {pergunta}"

    response = anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=system,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text


# ---------------------------------------------------------------------
# 7. DEMO — pipeline completo, ponta a ponta
# ---------------------------------------------------------------------

if __name__ == "__main__":
    nota_pedido = (
        "Pedido 4521 foi cancelado pelo cliente. Motivo: item chegou danificado. "
        "Cliente pediu dinheiro de volta via PIX. Reembolso processado em 3 dias úteis."
    )

    chunks = chunk_text(nota_pedido, tamanho_chunk=60, overlap=15)
    chunks_com_embeddings = embed_chunks(chunks)

    pergunta = "o cliente pediu reembolso?"
    resultados = retrieve(pergunta, chunks_com_embeddings, k=2)

    print(f"Pergunta: {pergunta}\n")
    print("Chunks recuperados (contexto que vai para o LLM):")
    for score, texto in resultados:
        print(f"  [{score:.4f}] {texto!r}")

    resposta = generate_answer(pergunta, resultados)
    print(f"\nResposta gerada pelo LLM:\n{resposta}")
