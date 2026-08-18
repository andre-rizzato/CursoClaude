# AI Engineer Roadmap — Kit do Projeto (André Rizzato)

Kit para trabalhar o curso de AI Engineering com o **Claude Code** dentro do
VS Code, com contexto do projeto já configurado.

## Como instalar

1. Extraia esta pasta e mescle o conteúdo com o seu clone do
   `DistributedOrderSystem`:
   - `ai/` → mescle com a pasta `ai/` que você já tem (ou copie se ainda
     não existir).
   - `CLAUDE.md` e `.claude/` → coloque na **raiz** do repositório.
   - `ebook/` → pode ficar na raiz ou dentro de `ai/`, como preferir.
2. Renomeie `ai/.env.example` para `ai/.env` e cole sua
   `ANTHROPIC_API_KEY` (console.anthropic.com → API Keys → Create Key).
   Esse arquivo já está no `.gitignore`.
3. Abra a pasta no VS Code.
4. Instale o Claude Code (extensão do VS Code ou `npm install -g
   @anthropic-ai/claude-code` para usar via terminal).
5. Rode `claude` na raiz do projeto. O `CLAUDE.md` carrega automaticamente
   — rode `/context` para confirmar que ele aparece em **Memory files**.

## Comandos do curso

| Comando | O que faz |
|---|---|
| `/status-curso` | Mostra em que semana/fase você está e os próximos passos |
| `/gerar-ebook` | Regenera o PDF do curso com o capítulo da semana concluída |

Esses comandos vêm de `.claude/skills/`. O Claude Code também pode invocar
`/status-curso` automaticamente quando você perguntar algo como "onde eu
parei?" — `/gerar-ebook` só roda quando você pedir explicitamente.

## Estrutura

```text
.
├── CLAUDE.md                      # contexto do projeto para o Claude Code
├── README.md                      # este arquivo
├── .claude/
│   └── skills/
│       ├── status-curso/SKILL.md
│       └── gerar-ebook/SKILL.md
├── ai/
│   ├── .env.example                # renomeie para .env e cole sua chave
│   ├── .gitignore
│   └── week1/
│       └── first_call.py           # exercício da Semana 1
└── ebook/
    ├── ebook_ai_engineer.py        # script reportlab do ebook
    └── AI_Engineer_Ebook_Semana1.pdf
```

## Dependências Python

```bash
cd ai
pip install anthropic python-dotenv
python week1/first_call.py
```

Para regenerar o ebook manualmente (fora do Claude Code):

```bash
pip install reportlab pdf2image
python ebook/ebook_ai_engineer.py
```
