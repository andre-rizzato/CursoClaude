# AI Engineer Roadmap (André Rizzato)

Repositório do curso de AI Engineering, com o **Claude Code** configurado
como professor + pair programmer (contexto em `CLAUDE.md`).

Os exercícios usam como contexto real o
[DistributedOrderSystem](https://github.com/andre-rizzato/DistributedOrderSystem),
projeto próprio anterior ao curso — mas esse projeto vive em um repositório
**separado e independente**, não dentro deste.

## Como instalar

1. Clone este repositório e abra a pasta no VS Code.
2. Crie `ai/.env` com sua `ANTHROPIC_API_KEY`
   (console.anthropic.com → API Keys → Create Key). Esse arquivo já está
   no `.gitignore`.
3. Instale o Claude Code (extensão do VS Code ou `npm install -g
   @anthropic-ai/claude-code` para usar via terminal).
4. Rode `claude` na raiz do projeto. O `CLAUDE.md` carrega automaticamente
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
│   ├── .env                        # ANTHROPIC_API_KEY (git-ignorado)
│   ├── .gitignore
│   ├── week1/                      # exercícios da Semana 1
│   └── week2/                      # exercícios da Semana 2
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
