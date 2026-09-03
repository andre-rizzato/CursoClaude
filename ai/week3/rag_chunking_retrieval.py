"""
rag_chunking_retrieval.py
Settimana 3-4 — RAG da zero: chunking + retrieval (senza framework)

Ancorato al dominio DistributedOrderSystem: le note di supporto/pedido
sono il "corpus" che vogliamo interrogare.
"""

import os
import math
import voyageai
from dotenv import load_dotenv

load_dotenv()

client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))


# ---------------------------------------------------------------------
# 1. CHUNKING
# ---------------------------------------------------------------------

def chunk_text(texto: str, tamanho_chunk: int = 60, overlap: int = 15) -> list[str]:
    """
    Divide il testo in chunk di tamanho fisso, con overlap tra i chunk
    consecutivi per non perdere contesto sui bordi del taglio.

    passo = tamanho_chunk - overlap  → quanto avanziamo a ogni iterazione
    """
    if overlap >= tamanho_chunk:
        raise ValueError("overlap deve essere minore di tamanho_chunk")

    chunks = []
    passo = tamanho_chunk - overlap
    inicio = 0

    while inicio < len(texto):
        fim = inicio + tamanho_chunk
        chunk = texto[inicio:fim]
        chunks.append(chunk)
        inicio += passo

    return chunks


# ---------------------------------------------------------------------
# 2. EMBEDDING (uguale alla Settimana 2, ma ora per una LISTA di chunk)
# ---------------------------------------------------------------------

def embed_chunks(chunks: list[str]) -> list[dict]:
    """
    Chiama la API Voyage UNA volta per tutti i chunk (batch),
    non un chunk alla volta — più economico e più veloce.
    """
    result = client.embed(chunks, model="voyage-4-large", input_type="document")

    chunks_com_embeddings = []
    for texto, embedding in zip(chunks, result.embeddings):
        chunks_com_embeddings.append({
            "texto": texto,
            "embedding": embedding
        })
    return chunks_com_embeddings


# ---------------------------------------------------------------------
# 3. COSSENO (recuperato dalla Settimana 2 — nessuna modifica)
# ---------------------------------------------------------------------

def cosseno(vetor_a: list[float], vetor_b: list[float]) -> float:
    produto_escalar = sum(a * b for a, b in zip(vetor_a, vetor_b))
    norma_a = math.sqrt(sum(a ** 2 for a in vetor_a))
    norma_b = math.sqrt(sum(b ** 2 for b in vetor_b))
    return produto_escalar / (norma_a * norma_b)


# ---------------------------------------------------------------------
# 4. RETRIEVAL
# ---------------------------------------------------------------------

def retrieve(pergunta: str, chunks_com_embeddings: list[dict], k: int = 3) -> list[tuple]:
    """
    Embedda la domanda con input_type="query" (importante: Voyage usa
    embedding leggermente diversi per query vs document — asimmetria
    intenzionale del modello, non un bug).
    """
    pergunta_embedding = client.embed(
        [pergunta], model="voyage-4-large", input_type="query"
    ).embeddings[0]

    scores = []
    for chunk in chunks_com_embeddings:
        sim = cosseno(pergunta_embedding, chunk["embedding"])
        scores.append((sim, chunk["texto"]))

    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[:k]


# ---------------------------------------------------------------------
# 5. DEMO — nota di supporto reale del DistributedOrderSystem
# ---------------------------------------------------------------------

if __name__ == "__main__":
    nota_pedido = (
        "Pedido 4521 foi cancelado pelo cliente. Motivo: item chegou danificado. "
        "Cliente pediu dinheiro de volta via PIX. Reembolso processado em 3 dias úteis."
    )

    chunks = chunk_text(nota_pedido, tamanho_chunk=60, overlap=15)
    print(f"Total de chunks gerados: {len(chunks)}\n")
    for i, c in enumerate(chunks):
        print(f"Chunk {i}: {c!r}")

    chunks_com_embeddings = embed_chunks(chunks)

    pergunta = "o cliente pediu reembolso?"
    resultados = retrieve(pergunta, chunks_com_embeddings, k=2)

    print(f"\nPergunta: {pergunta}")
    print("Top chunks recuperados:")
    for score, texto in resultados:
        print(f"  [{score:.4f}] {texto!r}")