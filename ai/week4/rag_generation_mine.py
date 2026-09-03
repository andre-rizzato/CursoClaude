"""rag_generation.py
Semana 3-4 - RAG do zero: Parte 2 - augmentation + generation + generation ponta a ponta

completa a pipeline iniciado in rag_chunking_retrieval.py
chuncking -> embedding -> retrieval -> AUGUMENTATION -> GENERATION
""" 

import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

# rag_chunking_retrieval.py agora mora em ../week3 (movido pra separar
# Parte 1/Parte 2 em pastas por semana)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "week3"))
from rag_chunking_retrieval import chunk_text, embed_chunks, retrieve

load_dotenv()

anthropic_client = Anthropic()


def generate_answer(pergunta: str, chunks_recuperados: list[tuple]) -> str:

    """
    Augmentation: monta o prompt final injetando os chunks recuperados como
    contexto explícito.

    Generation: chama o LLM pra responder SÓ com base nesse
    contexto — grounding, pra reduzir a alucinação.
    """

    contexto = "\n".join(f"- {texto}" for _, texto in chunks_recuperados)

    system = (
            "Você responde perguntas sobre pedidos do DistributedOrderSystem "
            "usando APENAS o contexto fornecido pelo usuário. Se a resposta "
            "não estiver no contexto, diga que não há informação suficiente — "
            "nunca invente dados que não apareçam no contexto.")

    
    user_prompt = f"Contexto recuperado:\n{contexto}\n\nPergunta: {pergunta}"

    response = anthropic_client.messages.create(model="claude-sonnet-4-6",
                                                max_tokens=300, 
                                                system=system, 
                                                messages=[{"role": "user","content":user_prompt}],
                                                )
    return response.content[0].text

if __name__ == "__main__":
    nota_pedido = (
       "Pedido 4521 foi cancelado pelo cliente. Motivo: item chegou danificado. "
       "Cliente pediu dinheiro de volta via PIX. Reembolso processado em 3 dias úteis."
    )

    chunks = chunk_text(nota_pedido,tamanho_chunk= 60 ,overlap= 15)
    chunks_com_embeddings = embed_chunks(chunks);

    pergunta = "o cliente pediu reembolso"
    resultados = retrieve(pergunta=pergunta, chunks_com_embeddings= chunks_com_embeddings, k=2)

    print(f"Pergunta: {pergunta}\n")
    print(f"Chunks Recuperados (Contexto que vai para o LLM):")
    for score, texto in resultados:
        print(f"[{score:.4f}] {texto!r}")

    resposta = generate_answer(pergunta, resultados)
    print(f"\nResposta gerada pelo LLm: \n{resposta}")

