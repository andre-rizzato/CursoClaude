"""
Semana 2 - Exercício 1: Gerando o primeiro embedding
Objetivo: entender na prática o que é um embedding -
um texto vira um vetor numérico que representa seu significado.
"""

import os

from dotenv import load_dotenv

import voyageai

load_dotenv()

client = voyageai.Client(api_key= os.getenv("VOYAGE_API_KEY"))

texto = "O cliente cancelou o pedido #1234 porque o prazo de entrega estava muito longo."

resultado = client.embed(
 texts = [texto],
 model = "voyage-4-lite",
 input_type = "document", # "document" para textos indexados, "query" para buscas - já adianto esse detalhe, ele importa na Sem 3-4

)

vetor = resultado.embeddings[0]

print(f"Texto: {texto}")
print(f"Dimensões do vetor: {len(vetor)}")
print(f"Primeiros 10 valores: {vetor[:10]}")
print(f"Tokens usados: {resultado.total_tokens}")
      