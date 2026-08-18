# week1/first_call.py
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="""Você é um assistente especializado no sistema DistributedOrderSystem.
    Esse sistema gerencia pedidos distribuídos com microserviços em .NET/C#.
    Responda sempre em português.""",
    messages=[
        {"role": "user", "content": "O que é um sistema de pedidos distribuído e quais são os principais desafios?"}
    ]
)

print(response.content[0].text)
print(f"\n--- Uso de tokens ---")
print(f"Input:  {response.usage.input_tokens}")
print(f"Output: {response.usage.output_tokens}")
