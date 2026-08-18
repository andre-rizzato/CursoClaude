---
name: status-curso
description: Mostra o status atual do curso de AI Engineering do André (semana, fase, próximos passos) e o checklist de arquivos esperados. Use quando o André perguntar "onde eu parei", "o que fazer essa semana", "qual o próximo passo", ou pedir um resumo do progresso do curso.
---

Leia o `CLAUDE.md` na raiz do projeto (seções "Estado atual" e "Plano de 26
semanas") e responda de forma direta com:

1. Em qual semana e fase o André está agora.
2. O que já foi concluído nesta semana (com base no que ele reportou na
   conversa até agora).
3. Os próximos 1-3 passos concretos, na ordem em que devem ser feitos.
4. Se a semana foi concluída, pergunte se ele quer rodar `/gerar-ebook`.

Regras:
- Nunca avance a semana sozinho — só quando o André confirmar que o exercício
  anterior funcionou e reportar o output (texto da resposta + tokens, quando
  aplicável).
- Sempre em português (Brasil).
- Seja conciso: isso é um checklist de status, não uma aula.
