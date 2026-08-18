---
name: gerar-ebook
description: Regenera o ebook do curso (AI_Engineer_Ebook_Semana1.pdf) adicionando o capítulo da semana recém-concluída, preservando os capítulos anteriores.
disable-model-invocation: true
allowed-tools: Bash(python3 ${CLAUDE_PROJECT_DIR}/ebook/ebook_ai_engineer.py) Bash(pip install reportlab*) Bash(pip install pdf2image*)
---

Regenerar o ebook do curso ($ARGUMENTS: descrição opcional do que cobrir no
capítulo novo — se vazio, use o que o André reportou nesta conversa):

1. Abra `${CLAUDE_PROJECT_DIR}/ebook/ebook_ai_engineer.py`.
2. Adicione um novo capítulo cobrindo a semana recém-concluída, seguindo o
   mesmo estilo visual dos capítulos anteriores (mesmas cores, estilos de
   tabela e diagramas quando fizer sentido). Não remova nem reescreva
   capítulos já existentes, exceto para corrigir pendências anotadas no
   `CLAUDE.md` (ex.: Semana 9 = Semantic Kernel como ponte .NET<->Python,
   não alternativa ao LangGraph).
3. Rode `python3 ${CLAUDE_PROJECT_DIR}/ebook/ebook_ai_engineer.py` para gerar
   o PDF atualizado.
4. Renderize 1-2 páginas do capítulo novo com `pdf2image` (dpi~90) para
   conferir visualmente antes de entregar. Erros comuns em reportlab a
   verificar:
   - texto branco sobre fundo claro (ou vice-versa) por camadas desenhadas
     na ordem errada;
   - células de tabela estourando a largura da coluna (usar `Paragraph`
     em vez de string simples para permitir quebra de linha);
   - elementos de `Drawing`/`Rect`/`String` desenhados fora de ordem,
     escondendo texto atrás de formas.
5. Corrija o que encontrar e re-renderize até ficar correto.
6. Apresente o PDF atualizado ao André com um resumo do que mudou.
