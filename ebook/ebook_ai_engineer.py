# -*- coding: utf-8 -*-
"""
Ebook: AI Engineer Roadmap - André Rizzato
Gerado com reportlab. Preserva capítulos anteriores a cada nova geração.
Versão: v1.4 - Caps 00 a 09 + índice automático (multiBuild)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Preformatted, HRFlowable, Flowable
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.pdfgen import canvas as pdfcanvas

import os
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI_Engineer_Ebook_Semana1.pdf")

# ---------- Cores do tema ----------
NAVY = colors.HexColor("#1B2A4A")
BLUE = colors.HexColor("#2E5EAA")
LIGHT_BLUE = colors.HexColor("#EAF1FB")
GRAY = colors.HexColor("#5A5A5A")
CODE_BG = colors.HexColor("#F4F4F4")
ORANGE = colors.HexColor("#E07A2C")
GREEN = colors.HexColor("#2E8B57")
GREEN_BG = colors.HexColor("#E7F4EC")
ORANGE_BG = colors.HexColor("#FCEFE2")
GRAY_BG = colors.HexColor("#EDEDED")

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="ChapterTitle", fontName="Helvetica-Bold", fontSize=22,
    textColor=NAVY, spaceAfter=18, spaceBefore=6, leading=26
))
styles.add(ParagraphStyle(
    name="ChapterKicker", fontName="Helvetica-Bold", fontSize=11,
    textColor=ORANGE, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="SectionHeading", fontName="Helvetica-Bold", fontSize=14,
    textColor=BLUE, spaceBefore=14, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="BodyPT", fontName="Helvetica", fontSize=10.5, leading=15.5,
    textColor=colors.HexColor("#222222"), spaceAfter=8, alignment=TA_LEFT
))
styles.add(ParagraphStyle(
    name="BulletPT", fontName="Helvetica", fontSize=10.5, leading=15,
    textColor=colors.HexColor("#222222"), leftIndent=14, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="CodeCaption", fontName="Helvetica-Oblique", fontSize=9,
    textColor=GRAY, spaceBefore=2, spaceAfter=10
))
styles.add(ParagraphStyle(
    name="CoverTitle", fontName="Helvetica-Bold", fontSize=30,
    textColor=colors.white, alignment=TA_CENTER, leading=36
))
styles.add(ParagraphStyle(
    name="CoverSubtitle", fontName="Helvetica", fontSize=14,
    textColor=colors.white, alignment=TA_CENTER, spaceBefore=14
))
styles.add(ParagraphStyle(
    name="GlossaryTerm", fontName="Helvetica-Bold", fontSize=10.5,
    textColor=NAVY, spaceBefore=6
))

styles.add(ParagraphStyle(
    name="CellText", fontName="Helvetica", fontSize=8.3, leading=11,
    textColor=colors.HexColor("#222222")
))
styles.add(ParagraphStyle(
    name="CellHeader", fontName="Helvetica-Bold", fontSize=8.6, leading=11,
    textColor=colors.white
))

CODE_STYLE = ParagraphStyle(
    name="Code", fontName="Courier", fontSize=8.6, leading=11.5,
    backColor=CODE_BG, textColor=colors.HexColor("#111111"),
    borderPadding=8, leftIndent=4
)

TOC_STYLE_L0 = ParagraphStyle(
    name="TOCLevel0", fontName="Helvetica-Bold", fontSize=11.5,
    textColor=NAVY, leading=18, leftIndent=0, spaceBefore=4
)


# ---------- Documento com índice automático ----------
class EbookDocTemplate(SimpleDocTemplate):
    """SimpleDocTemplate com hook para popular o índice (TableOfContents).

    afterFlowable é chamado pelo reportlab depois de desenhar cada
    flowable na página - aqui capturamos todo parágrafo no estilo
    ChapterTitle e notificamos o TOC com (nível, texto, página atual).
    Requer doc.multiBuild() em vez de doc.build() - o número de página
    só fica correto na segunda passada, depois que o índice já existe.
    """

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "ChapterTitle":
            texto = flowable.getPlainText()
            self.notify("TOCEntry", (0, texto, self.page))


# ---------- Capa ----------
class CoverPage(Flowable):
    """Desenha fundo e texto da capa juntos, no mesmo Flowable, para evitar
    que o texto branco caia fora da área escura (bug de camadas separadas)."""

    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        # fundo navy
        c.setFillColor(NAVY)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        # faixa superior azul
        c.setFillColor(BLUE)
        c.rect(0, self.height - 6, self.width, 6, fill=1, stroke=0)

        cx = self.width / 2

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(cx, self.height * 0.62, "AI ENGINEER ROADMAP")

        c.setFont("Helvetica", 13)
        c.drawCentredString(cx, self.height * 0.62 - 26, "Curso Personalizado de AI Engineering")

        c.setFillColor(ORANGE)
        c.setLineWidth(1)
        c.line(cx - 60, self.height * 0.48, cx + 60, self.height * 0.48)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 15)
        c.drawCentredString(cx, self.height * 0.40, "André Rizzato")

        c.setFont("Helvetica", 10.5)
        c.drawCentredString(
            cx, self.height * 0.40 - 22,
            "Projeto base: DistributedOrderSystem"
        )
        c.drawCentredString(
            cx, self.height * 0.40 - 38,
            "Volume 1  -  Semana 1"
        )


def build_cover(story, page_w, page_h):
    story.append(CoverPage(page_w - 2 * 2.2 * cm, 20 * cm))
    story.append(PageBreak())


# ---------- Diagrama multi-agente ----------
def multi_agent_diagram():
    d = Drawing(460, 320)

    def box(x, y, w, h, text, fill=LIGHT_BLUE, text_color=NAVY, font_size=8.2):
        d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=BLUE, strokeWidth=1, rx=6, ry=6))
        d.add(String(x + w / 2, y + h / 2 - 3, text, fontName="Helvetica-Bold",
                      fontSize=font_size, fillColor=text_color, textAnchor="middle"))

    # Orchestrator no topo
    box(150, 260, 160, 40, "Order Orchestrator Agent", fill=NAVY, text_color=colors.white, font_size=8.6)

    # Linhas para os agentes worker (desenhadas antes das caixas, para ficarem por baixo)
    workers = [
        (10, "Create Order\nAgent"),
        (110, "Cancel Order\nAgent"),
        (210, "Update Order\nAgent"),
        (310, "Product/Inventory\nInfo Agent"),
        (390, "Order History\nRAG Agent"),
    ]
    for x, label in workers:
        d.add(Line(230, 260, x + 45, 190, strokeColor=GRAY, strokeWidth=0.8))

    # Caixas dos agentes worker, com o texto desenhado por cima (nunca antes do Rect)
    for x, label in workers:
        d.add(Rect(x, 140, 90, 40, fillColor=colors.white, strokeColor=BLUE, strokeWidth=1, rx=5, ry=5))
        lines = label.split("\n")
        start_y = 165 if len(lines) > 1 else 158
        for i, line in enumerate(lines):
            d.add(String(x + 45, start_y - (i * 10), line, fontName="Helvetica",
                          fontSize=7.6, fillColor=NAVY, textAnchor="middle"))

    # Camada de domínio (.NET) embaixo
    d.add(Rect(10, 60, 440, 34, fillColor=colors.HexColor("#FCEFE2"), strokeColor=ORANGE, strokeWidth=1, rx=6, ry=6))
    d.add(String(230, 74, "DistributedOrderSystem (C# / .NET) - Microsservicos de Dominio",
                 fontName="Helvetica-Bold", fontSize=8.4, fillColor=colors.HexColor("#8A4A16"), textAnchor="middle"))

    for x, _ in workers:
        d.add(Line(x + 45, 140, x + 45, 94, strokeColor=GRAY, strokeWidth=0.8))

    d.add(String(230, 20, "Fluxo: usuario -> Orchestrator -> agente especialista -> API .NET do dominio",
                 fontName="Helvetica-Oblique", fontSize=7.6, fillColor=GRAY, textAnchor="middle"))

    return d


# ---------- Construção do documento ----------
def build():
    doc = EbookDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="AI Engineer Roadmap - André Rizzato",
        author="Claude + André Rizzato"
    )
    page_w, page_h = A4
    story = []

    build_cover(story, page_w, page_h)

    # ===================== ÍNDICE =====================
    # Estilo próprio (não "ChapterTitle") para não se auto-listar no índice -
    # afterFlowable() do EbookDocTemplate casa pelo nome do estilo.
    indice_heading_style = ParagraphStyle(name="IndiceHeading", parent=styles["ChapterTitle"])
    story.append(Paragraph("ÍNDICE", indice_heading_style))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))
    toc = TableOfContents()
    toc.levelStyles = [TOC_STYLE_L0]
    story.append(toc)
    story.append(PageBreak())

    # ===================== CAP 00 =====================
    story.append(Paragraph("CAPÍTULO 00", styles["ChapterKicker"]))
    story.append(Paragraph("Setup de Ambiente", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "Antes de escrever qualquer linha de IA, preparamos o terreno. A camada de IA do "
        "DistributedOrderSystem vive dentro de uma pasta <b>ai/</b> separada da solução .NET, "
        "para não misturar responsabilidades: o C# continua sendo a camada de domínio, "
        "o Python entra como camada de inteligência.", styles["BodyPT"]
    ))

    story.append(Paragraph("Passo 1 - Ambiente Python", styles["SectionHeading"]))
    story.append(Paragraph(
        "Confirme a versão instalada e instale as duas dependências iniciais do curso: "
        "o SDK oficial da Anthropic e o utilitário para carregar variáveis de ambiente.",
        styles["BodyPT"]
    ))
    story.append(Preformatted(
        "python --version\npip install anthropic python-dotenv", CODE_STYLE
    ))
    story.append(Paragraph("Comandos de terminal - Semana 1", styles["CodeCaption"]))

    story.append(Paragraph("Passo 2 - Estrutura de pastas", styles["SectionHeading"]))
    story.append(Preformatted(
        "DistributedOrderSystem/\n"
        "  ai/\n"
        "    .env                  <- ANTHROPIC_API_KEY (no .gitignore)\n"
        "    .gitignore\n"
        "    week1/\n"
        "      first_call.py       <- exercicio atual\n"
        "      streaming_call.py   <- proximo passo",
        CODE_STYLE
    ))
    story.append(Paragraph("Estrutura de arquivos da Semana 1", styles["CodeCaption"]))

    story.append(Paragraph("Passo 3 - Chave de API e segurança", styles["SectionHeading"]))
    story.append(Paragraph(
        "A chave é obtida em <b>console.anthropic.com &rarr; API Keys &rarr; Create Key</b>. "
        "Ela nunca vai para o Git: o arquivo <b>.env</b> guarda a chave localmente e o "
        "<b>.gitignore</b> impede que ela seja versionada.", styles["BodyPT"]
    ))
    story.append(Preformatted(
        "# .env\nANTHROPIC_API_KEY=sua_chave_aqui\n\n"
        "# .gitignore\n.env\n__pycache__/\n*.pyc",
        CODE_STYLE
    ))
    story.append(Paragraph("Conteúdo de .env e .gitignore", styles["CodeCaption"]))
    story.append(PageBreak())

    # ===================== CAP 01 =====================
    story.append(Paragraph("CAPÍTULO 01", styles["ChapterKicker"]))
    story.append(Paragraph("Fundamentos de LLM", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "Um <b>LLM</b> (Large Language Model) é um modelo estatístico treinado para prever "
        "a próxima unidade de texto (token) dado o contexto anterior. Isso é suficiente, em "
        "escala, para gerar texto coerente, responder perguntas, escrever código e raciocinar "
        "sobre problemas.", styles["BodyPT"]
    ))

    story.append(Paragraph("Tokens e janela de contexto", styles["SectionHeading"]))
    story.append(Paragraph(
        "Um <b>token</b> é a unidade mínima de texto que o modelo processa - em média, algo "
        "entre 3 e 4 caracteres em português. A <b>context window</b> é o número máximo de "
        "tokens (entrada + saída) que o modelo consegue considerar em uma única chamada. "
        "Todo o histórico de conversa, o system prompt e a pergunta atual competem pelo "
        "mesmo espaço.", styles["BodyPT"]
    ))

    story.append(Paragraph("System prompt vs. user prompt", styles["SectionHeading"]))
    story.append(Paragraph(
        "O <b>system prompt</b> define o papel, as regras e o tom do assistente antes da "
        "conversa começar - é onde configuramos, por exemplo, que o assistente deve responder "
        "sempre em português e conhecer o contexto do DistributedOrderSystem. O <b>user "
        "prompt</b> é a mensagem específica do usuário em cada turno.", styles["BodyPT"]
    ))

    story.append(Paragraph("Temperature", styles["SectionHeading"]))
    story.append(Paragraph(
        "Controla a aleatoriedade da geração: valores baixos (perto de 0) tornam a resposta "
        "mais determinística e previsível - ideal para tarefas de negócio como classificar "
        "um pedido. Valores altos aumentam a criatividade/diversidade, mas também o risco de "
        "respostas menos precisas.", styles["BodyPT"]
    ))

    story.append(Paragraph("Prévia: embeddings", styles["SectionHeading"]))
    story.append(Paragraph(
        "Além de gerar texto, um modelo pode transformar texto em um vetor numérico "
        "(<b>embedding</b>) que representa seu significado. Dois textos com significados "
        "próximos geram vetores próximos no espaço. Essa ideia é a base do RAG, que "
        "construiremos do zero ainda na Fase 1.", styles["BodyPT"]
    ))
    story.append(PageBreak())

    # ===================== CAP 02 =====================
    story.append(Paragraph("CAPÍTULO 02", styles["ChapterKicker"]))
    story.append(Paragraph("Anthropic API na Prática", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "Toda interação com o modelo passa pelo endpoint <b>messages.create</b>. Os "
        "parâmetros centrais são:", styles["BodyPT"]
    ))
    story.append(Paragraph("&bull; <b>model</b> - qual modelo será usado (ex: claude-sonnet-4-6)", styles["BulletPT"]))
    story.append(Paragraph("&bull; <b>max_tokens</b> - limite de tokens de saída", styles["BulletPT"]))
    story.append(Paragraph("&bull; <b>system</b> - o system prompt (papel do assistente)", styles["BulletPT"]))
    story.append(Paragraph("&bull; <b>messages</b> - lista de turnos da conversa (role + content)", styles["BulletPT"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Exercício: first_call.py", styles["SectionHeading"]))
    story.append(Paragraph(
        "Este é o primeiro script que André executa no curso - uma chamada simples, com "
        "system prompt já ancorado no contexto do DistributedOrderSystem.", styles["BodyPT"]
    ))
    story.append(Preformatted(
        "# week1/first_call.py\n"
        "import os\n"
        "from anthropic import Anthropic\n"
        "from dotenv import load_dotenv\n\n"
        "load_dotenv()\n\n"
        "client = Anthropic()\n\n"
        "response = client.messages.create(\n"
        "    model=\"claude-sonnet-4-6\",\n"
        "    max_tokens=1024,\n"
        "    system=\"\"\"Voce e um assistente especializado no sistema DistributedOrderSystem.\n"
        "    Esse sistema gerencia pedidos distribuidos com microservicos em .NET/C#.\n"
        "    Responda sempre em portugues.\"\"\",\n"
        "    messages=[\n"
        "        {\"role\": \"user\", \"content\": \"O que e um sistema de pedidos distribuido e\n"
        "         quais sao os principais desafios?\"}\n"
        "    ]\n"
        ")\n\n"
        "print(response.content[0].text)\n"
        "print(f\"\\n--- Uso de tokens ---\")\n"
        "print(f\"Input:  {response.usage.input_tokens}\")\n"
        "print(f\"Output: {response.usage.output_tokens}\")",
        CODE_STYLE
    ))
    story.append(Paragraph("Código completo - week1/first_call.py", styles["CodeCaption"]))

    story.append(Paragraph("O que observar na resposta", styles["SectionHeading"]))
    story.append(Paragraph("&bull; O modelo respondeu dentro do contexto do system prompt?", styles["BulletPT"]))
    story.append(Paragraph("&bull; Quantos tokens de input foram usados - o system prompt já custa tokens", styles["BulletPT"]))
    story.append(Paragraph("&bull; A latência - tempo até a primeira palavra aparecer", styles["BulletPT"]))
    story.append(PageBreak())

    # ===================== CAP 03 =====================
    story.append(Paragraph("CAPÍTULO 03", styles["ChapterKicker"]))
    story.append(Paragraph("Integração com o Projeto", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "O DistributedOrderSystem não é um projeto de exemplo descartável - é o backbone "
        "técnico de uma futura empresa. A decisão arquitetural central: <b>Python assume a "
        "camada de IA</b> (agentes, RAG, orquestração) e <b>C#/.NET permanece intocado como "
        "camada de domínio</b> (regras de negócio, persistência, APIs).", styles["BodyPT"]
    ))

    story.append(Paragraph("Mapeamento de agentes para o domínio de pedidos", styles["SectionHeading"]))

    def cell1(text, header=False):
        return Paragraph(text, styles["CellHeader"] if header else styles["CellText"])

    table_rows = [
        ["Agente genérico", "Agente no projeto"],
        ["Orchestrator", "Order Orchestrator Agent"],
        ["Booking", "Create Order Agent"],
        ["Cancellation", "Cancel Order Agent"],
        ["Reschedule", "Update Order Agent"],
        ["Information", "Product/Inventory Info Agent"],
        ["RAG/FAQ", "Order History RAG Agent"],
    ]
    table_data = [[cell1(v, header=(i == 0)) for v in row] for i, row in enumerate(table_rows)]
    t = Table(table_data, colWidths=[7.5 * cm, 8.5 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Diagrama multi-agente aplicado ao domínio", styles["SectionHeading"]))
    story.append(multi_agent_diagram())
    story.append(Paragraph(
        "Figura 3.1 - O Orchestrator recebe a intenção do usuário, roteia para o agente "
        "especialista correspondente, que por sua vez chama a API .NET do domínio.",
        styles["CodeCaption"]
    ))
    story.append(PageBreak())

    # ===================== CAP 04 =====================
    story.append(Paragraph("CAPÍTULO 04", styles["ChapterKicker"]))
    story.append(Paragraph("Glossário", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    glossary = [
        ("LLM (Large Language Model)", "Modelo estatístico treinado para prever o próximo token de um texto, usado para gerar respostas, código e raciocínio."),
        ("Token", "Unidade mínima de texto processada pelo modelo; aproximadamente 3-4 caracteres em português."),
        ("Embedding", "Representação numérica (vetor) do significado de um texto, usada para medir similaridade semântica."),
        ("Similaridade de cosseno", "Medida do ângulo entre dois vetores (ignora magnitude); padrão para comparar embeddings de texto."),
        ("Chunking", "Divisão de um texto longo em pedaços menores (chunks) antes de gerar embeddings, para permitir retrieval granular."),
        ("Overlap (chunking)", "Trecho de texto repetido entre chunks consecutivos, para não perder contexto na fronteira do corte."),
        ("Retrieval", "Etapa do RAG que busca, por similaridade vetorial, os chunks mais relevantes para uma pergunta."),
        ("Augmentation", "Etapa do RAG que injeta os chunks recuperados como contexto explícito dentro do prompt enviado ao LLM."),
        ("Grounding", "Instruir o LLM a responder apenas com base no contexto fornecido, reduzindo o risco de alucinação."),
        ("RAG (Retrieval-Augmented Generation)", "Técnica que busca informação relevante em uma base de conhecimento antes de gerar a resposta do modelo."),
        ("Agente", "Sistema que usa um LLM para decidir ações, chamar ferramentas e iterar até cumprir um objetivo."),
        ("Tool Use / Function Calling", "Capacidade do modelo de chamar funções externas (ex: consultar um pedido no .NET) durante a conversa."),
        ("MCP (Model Context Protocol)", "Protocolo aberto para conectar modelos a ferramentas e fontes de dados de forma padronizada."),
        ("Orchestrator", "Agente responsável por rotear a intenção do usuário para o agente especialista correto."),
        ("Fine-tuning", "Processo de re-treinar um modelo pré-existente com dados específicos de um domínio."),
        ("LoRA / QLoRA", "Técnicas eficientes de fine-tuning que ajustam poucos parâmetros extras, reduzindo custo computacional."),
        ("Prompt Engineering", "Prática de estruturar instruções para obter o melhor comportamento possível do modelo."),
        ("Context Window", "Quantidade máxima de tokens (entrada + saída) que o modelo consegue processar em uma chamada."),
        ("Temperature", "Parâmetro que controla a aleatoriedade/criatividade da geração de texto."),
        ("System Prompt", "Instrução inicial que define papel, tom e regras do assistente antes da conversa do usuário."),
    ]
    for term, definition in glossary:
        story.append(Paragraph(term, styles["GlossaryTerm"]))
        story.append(Paragraph(definition, styles["BodyPT"]))
    story.append(PageBreak())

    # ===================== CAP 05 =====================
    story.append(Paragraph("CAPÍTULO 05", styles["ChapterKicker"]))
    story.append(Paragraph("Referência de Arquitetura", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "Visão consolidada do plano de 26 semanas, dividido em 6 fases. Cada fase entrega "
        "capacidades concretas dentro do DistributedOrderSystem, sem abstrair prematuramente "
        "para um template genérico.", styles["BodyPT"]
    ))

    def cell2(text, header=False):
        return Paragraph(text, styles["CellHeader"] if header else styles["CellText"])

    plan_rows = [
        ["Fase", "Semanas", "Foco"],
        ["1 - Fundamentos", "1-4", "Python, API Anthropic, embeddings, RAG do zero"],
        ["2 - Agentes e MCP", "5-10", "Ollama, tool use, MCP server, Semantic Kernel, LangGraph"],
        ["3 - RAG Avançado", "11-16", "Hybrid search, reranking, LlamaIndex, RAGAS, DSPy"],
        ["4 - Fine-tuning", "17-22", "LoRA/QLoRA com Unsloth, DPO, vLLM, MLOps"],
        ["5 - Produção + Negócio", "23-26", "LiteLLM, extração do backbone, instanciação do nicho"],
    ]
    plan_data = [[cell2(v, header=(i == 0)) for v in row] for i, row in enumerate(plan_rows)]
    t2 = Table(plan_data, colWidths=[4.6 * cm, 2.4 * cm, 9.0 * cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Stack consolidada", styles["SectionHeading"]))

    def cell(text, header=False):
        return Paragraph(text, styles["CellHeader"] if header else styles["CellText"])

    stack_rows = [
        ["Camada", "Tecnologia", "Papel"],
        ["IA / Orquestração", "Python (LangGraph, LlamaIndex, FastMCP, Unsloth, RAGAS, DSPy)", "Camada principal de IA"],
        ["Domínio / APIs", "C# / .NET (microsserviços existentes)", "Camada de domínio - não mexer"],
        ["Bridge opcional", "Semantic Kernel (.NET)", "Ponte .NET <-> Python apenas"],
        ["LLM local", "Ollama (Llama 3.2 / Phi-3.5)", "Dev offline, zero custo"],
        ["LLM cloud", "Anthropic API (claude-sonnet-4-6)", "Produção"],
        ["Gateway", "LiteLLM", "Roteamento cloud/local"],
        ["Observabilidade", "LangSmith / Langfuse", "Traces e métricas"],
    ]
    stack_data = [
        [cell(v, header=(i == 0)) for v in row] for i, row in enumerate(stack_rows)
    ]
    t3 = Table(stack_data, colWidths=[2.9 * cm, 8.4 * cm, 4.7 * cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t3)

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "<i>Regra anti-abstração prematura: construir o concreto primeiro (Orders, ponta a "
        "ponta). Generalizar para o template core/ + packs/ só ao instanciar o segundo "
        "domínio, na Fase 5.</i>", styles["BodyPT"]
    ))
    story.append(PageBreak())

    # ===================== CAP 06 =====================
    story.append(Paragraph("CAPÍTULO 06", styles["ChapterKicker"]))
    story.append(Paragraph("Embeddings e Similaridade Semântica", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "Um <b>embedding</b> é um vetor numérico que representa o significado de um texto. "
        "Textos com significados próximos geram vetores próximos no espaço vetorial. A "
        "Anthropic não tem modelo nativo de embeddings - o curso usa a <b>Voyage AI</b> "
        "(<b>voyage-4-large</b> para indexação em nuvem, <b>voyage-4-nano</b> open-weight "
        "para rodar local).", styles["BodyPT"]
    ))

    story.append(Paragraph("Similaridade de cosseno - a fórmula", styles["SectionHeading"]))
    story.append(Paragraph(
        "Dado dois vetores A e B, a similaridade de cosseno é:", styles["BodyPT"]
    ))
    story.append(Preformatted(
        "cos(A, B) = (A . B) / (|A| . |B|)\n\n"
        "  A . B  = produto escalar = soma de (a_i * b_i) termo a termo\n"
        "  |A|    = norma de A = raiz quadrada da soma de a_i ao quadrado\n"
        "  |B|    = norma de B = raiz quadrada da soma de b_i ao quadrado",
        CODE_STYLE
    ))
    story.append(Paragraph(
        "O numerador mede o quanto os vetores apontam na mesma direção; o denominador "
        "normaliza pelo tamanho de cada vetor, deixando o resultado só sobre a direção "
        "(o resultado fica sempre entre -1 e 1).", styles["BodyPT"]
    ))

    story.append(Paragraph("Cosseno vs. distância euclidiana - exemplo numérico", styles["SectionHeading"]))
    story.append(Paragraph(
        "Vetor A = (1, 1) e vetor B = (2, 2). B é literalmente A esticado - mesma direção, "
        "magnitude diferente.", styles["BodyPT"]
    ))
    story.append(Preformatted(
        "Distancia euclidiana:\n"
        "  raiz((2-1)^2 + (2-1)^2) = raiz(2) = 1.41   -> parece \"diferente\"\n\n"
        "Similaridade de cosseno:\n"
        "  (1*2 + 1*2) / (raiz(2) * raiz(8)) = 4 / 4 = 1.0   -> direcao identica",
        CODE_STYLE
    ))
    story.append(Paragraph(
        "Em embeddings de texto, a magnitude do vetor costuma refletir coisas como tamanho "
        "do texto, não o significado. Cosseno ignora isso e compara só a direção - por isso "
        "é o padrão em NLP, e não a distância euclidiana.", styles["BodyPT"]
    ))

    story.append(Paragraph("Aprofundamento: quatro perguntas em aberto (em linguagem simples)", styles["SectionHeading"]))

    story.append(Paragraph("1. Por que cosseno, e não distância euclidiana?", styles["GlossaryTerm"]))
    story.append(Paragraph(
        "Porque distância euclidiana também é afetada pelo <b>tamanho</b> do vetor, não só "
        "pela direção - e o tamanho do embedding costuma refletir coisas como tamanho do "
        "texto, não o significado. Dois textos com o mesmo sentido mas tamanhos diferentes "
        "podem parecer \"distantes\" na euclidiana e \"idênticos\" no cosseno (veja o exemplo "
        "numérico acima: A e B apontam pro mesmo lugar, cosseno = 1.0, mas a distância "
        "euclidiana entre eles não é zero). Cosseno olha só pra direção, por isso é o padrão "
        "em NLP.", styles["BodyPT"]
    ))

    story.append(Paragraph("2. Negação e o estado Cancelled", styles["GlossaryTerm"]))
    story.append(Paragraph(
        "Embeddings não entendem negação como lógica - entendem como padrão de palavras que "
        "aparecem juntas. \"Pedido foi cancelado\" e \"pedido não foi cancelado\" usam quase "
        "as mesmas palavras, no mesmo contexto, e por isso ficam próximos no espaço vetorial "
        "mesmo significando o oposto. Como <b>Cancelled</b> é estado terminal da máquina de "
        "estados do pedido (Pending -&gt; Confirmed -&gt; Shipped -&gt; Delivered / Cancelled), "
        "um fato categórico e exato como esse deve vir de filtro estruturado no banco de "
        "dados, não de busca semântica - busca semântica responde \"sobre o que é o texto\", "
        "não \"isso é verdadeiro ou falso\".", styles["BodyPT"]
    ))

    story.append(Paragraph("3. Cosseno negativo (cos = -1)", styles["GlossaryTerm"]))
    story.append(Paragraph(
        "cos = 1 significa mesma direção (significado quase idêntico); cos = 0 significa "
        "direções perpendiculares (sem relação); cos = -1 significaria direções opostas "
        "(significado oposto). Na prática, com embeddings de texto, valores próximos de -1 "
        "quase não aparecem: textos com significados opostos costumam cair perto de 0 (sem "
        "relação), não perto de -1. Esses modelos são treinados para agrupar textos "
        "parecidos, não para codificar \"oposto lógico\" - o espaço vetorial não tem um "
        "conceito forte de antônimo.", styles["BodyPT"]
    ))

    story.append(Paragraph("4. Códigos de erro internos (ex.: ORD_TIMEOUT_502)", styles["GlossaryTerm"]))
    story.append(Paragraph(
        "O modelo de embedding não sabe que isso é um identificador interno do sistema - ele "
        "quebra o código em pedaços (ORD, TIMEOUT, 502) e gera um vetor a partir de "
        "associações genéricas aprendidas no treino (\"502\" puxa semântica de erro HTTP, "
        "\"TIMEOUT\" puxa semântica genérica de tempo esgotado), sem saber o que o código "
        "significa especificamente no domínio. Por isso não se indexa o código cru - indexa-se "
        "a descrição em linguagem natural (ex.: \"ORD_TIMEOUT_502: tempo excedido aguardando "
        "confirmação do provedor de pagamento\").", styles["BodyPT"]
    ))
    story.append(PageBreak())

    # ===================== CAP 07 =====================
    story.append(Paragraph("CAPÍTULO 07", styles["ChapterKicker"]))
    story.append(Paragraph("RAG do Zero - Chunking e Retrieval", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "Antes de usar um framework (LangChain, LlamaIndex), o curso constrói um RAG mínimo "
        "à mão, para entender o mecanismo por baixo do capô: dividir texto em pedaços "
        "(<b>chunking</b>), transformar cada pedaço em embedding, e recuperar os mais "
        "relevantes para uma pergunta (<b>retrieval</b>).", styles["BodyPT"]
    ))

    story.append(Paragraph("Chunking de tamanho fixo com overlap", styles["SectionHeading"]))
    story.append(Paragraph(
        "A janela desliza sobre o texto em passos menores que o próprio tamanho do chunk, "
        "criando sobreposição entre chunks vizinhos:", styles["BodyPT"]
    ))
    story.append(Preformatted(
        "passo = tamanho_chunk - overlap\n\n"
        "Exemplo: tamanho_chunk=60, overlap=15  ->  passo = 45",
        CODE_STYLE
    ))
    story.append(Preformatted(
        "posicao:  0        45       90       135     151\n"
        "texto:    |--------|--------|--------|--------|\n"
        "chunk 0:  [0.....................60)\n"
        "chunk 1:      [45.....................105)\n"
        "chunk 2:            [90.....................150)\n"
        "chunk 3:                        [135......151)",
        CODE_STYLE
    ))
    story.append(Paragraph(
        "O overlap evita que uma informação seja perdida bem na fronteira do corte - mas não "
        "impede o corte de cair no meio de uma palavra, como aconteceu aqui (\"Motivo\" virou "
        "\"...o:\" no início do chunk 1).", styles["BodyPT"]
    ))

    story.append(Paragraph("Exercício: rag_chunking_retrieval.py", styles["SectionHeading"]))
    story.append(Preformatted(
        "def chunk_text(texto, tamanho_chunk=60, overlap=15):\n"
        "    chunks = []\n"
        "    passo = tamanho_chunk - overlap\n"
        "    inicio = 0\n"
        "    while inicio < len(texto):\n"
        "        chunks.append(texto[inicio:inicio + tamanho_chunk])\n"
        "        inicio += passo\n"
        "    return chunks",
        CODE_STYLE
    ))
    story.append(Paragraph("Código - week3/rag_chunking_retrieval.py (trecho)", styles["CodeCaption"]))

    story.append(Paragraph(
        "Ao embeddar a pergunta, o input_type usado é \"query\" (não \"document\") - a Voyage "
        "gera embeddings ligeiramente diferentes para query vs. documento, uma assimetria "
        "intencional do modelo, não um bug.", styles["BodyPT"]
    ))

    story.append(Paragraph("Resultado real (nota de suporte do pedido 4521)", styles["SectionHeading"]))
    story.append(Preformatted(
        "Pergunta: \"o cliente pediu reembolso?\"\n\n"
        "[0.5493] 'o: item chegou danificado. Cliente pediu dinheiro de volta v'\n"
        "[0.4521] 'eiro de volta via PIX. Reembolso processado em 3 dias uteis.'",
        CODE_STYLE
    ))
    story.append(Paragraph(
        "O chunk vencedor não contém a palavra \"reembolso\" - contém \"Cliente pediu dinheiro "
        "de volta\", com a mesma estrutura sujeito+verbo+objeto da pergunta. O chunk com a "
        "palavra literal \"Reembolso\" fica em segundo porque fala do <b>status</b> do "
        "reembolso (prazo de processamento), não de quem pediu o quê - <b>relevância "
        "tópica</b> (mesma área do assunto) é diferente de <b>relevância proposicional</b> "
        "(responder à mesma pergunta), e é a segunda que o embedding está de fato capturando.",
        styles["BodyPT"]
    ))
    story.append(PageBreak())

    # ===================== CAP 08 =====================
    story.append(Paragraph("CAPÍTULO 08", styles["ChapterKicker"]))
    story.append(Paragraph("RAG do Zero - Augmentation e Generation", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "Chunking e retrieval (Capítulo 07) respondem \"quais pedaços de texto são "
        "relevantes\". Faltam os dois últimos passos do RAG: transformar esses chunks em "
        "resposta em linguagem natural.", styles["BodyPT"]
    ))
    story.append(Preformatted(
        "pergunta -> embed -> retrieve (top-k chunks)\n"
        "                          |\n"
        "                          v\n"
        "                    AUGMENTATION: monta um prompt injetando\n"
        "                    os chunks como contexto explicito\n"
        "                          |\n"
        "                          v\n"
        "                    GENERATION: LLM responde usando\n"
        "                    APENAS esse contexto",
        CODE_STYLE
    ))

    story.append(Paragraph("Augmentation", styles["SectionHeading"]))
    story.append(Paragraph(
        "É literalmente concatenar os chunks recuperados dentro do prompt que vai pro LLM - "
        "\"aumentar\" a pergunta do usuário com informação que ele não tinha antes.",
        styles["BodyPT"]
    ))

    story.append(Paragraph("Generation com grounding", styles["SectionHeading"]))
    story.append(Paragraph(
        "No <b>system prompt</b>, o modelo é instruído a responder <b>só</b> com base no "
        "contexto fornecido, e a dizer que não sabe se a resposta não estiver lá. Sem essa "
        "instrução, o LLM pode completar a resposta com conhecimento geral dele - que pode "
        "estar certo por acaso, mas quebra a garantia de que a resposta vem dos dados reais "
        "do pedido, não da memória do modelo. Essa técnica se chama <b>grounding</b>.",
        styles["BodyPT"]
    ))
    story.append(Preformatted(
        "def generate_answer(pergunta, chunks_recuperados):\n"
        "    contexto = \"\\n\".join(f\"- {texto}\" for _, texto in chunks_recuperados)\n\n"
        "    system = (\n"
        "        \"Voce responde perguntas sobre pedidos do DistributedOrderSystem \"\n"
        "        \"usando APENAS o contexto fornecido. Se a resposta nao estiver \"\n"
        "        \"no contexto, diga que nao ha informacao suficiente.\"\n"
        "    )\n\n"
        "    response = anthropic_client.messages.create(\n"
        "        model=\"claude-sonnet-4-6\", max_tokens=300, system=system,\n"
        "        messages=[{\"role\": \"user\", \"content\": f\"Contexto:\\n{contexto}\\n\\n"
        "Pergunta: {pergunta}\"}],\n"
        "    )\n"
        "    return response.content[0].text",
        CODE_STYLE
    ))
    story.append(Paragraph("Código - week4/rag_generation.py (trecho)", styles["CodeCaption"]))

    story.append(Paragraph("Resultado real - pipeline ponta a ponta", styles["SectionHeading"]))
    story.append(Preformatted(
        "Pergunta: \"o cliente pediu reembolso\"\n\n"
        "Chunks recuperados (contexto que vai para o LLM):\n"
        "  [0.5819] 'o: item chegou danificado. Cliente pediu dinheiro de volta v'\n"
        "  [0.4726] 'eiro de volta via PIX. Reembolso processado em 3 dias uteis.'\n\n"
        "Resposta gerada pelo LLM:\n"
        "  Com base no contexto fornecido, sim - o cliente relatou que o item chegou\n"
        "  danificado e solicitou reembolso via PIX. O reembolso foi processado com\n"
        "  prazo de 3 dias uteis.",
        CODE_STYLE
    ))
    story.append(Paragraph(
        "Resposta corretamente <b>grounded</b>: só usa o que estava nos 2 chunks "
        "recuperados, nada inventado. Detalhe fino: os scores de cosseno ficaram levemente "
        "diferentes do Capítulo 07 (<i>0.5493 &rarr; 0.5819</i>, <i>0.4521 &rarr; 0.4726</i>) "
        "porque a pergunta desta vez não tinha \"?\" no final - o embedding representa o "
        "texto exato enviado, pontuação inclusa. A ordem do ranking não mudou, só o valor "
        "do score - lembrete de que \"similaridade semântica\" ainda é sensível a variações "
        "superficiais do input.", styles["BodyPT"]
    ))
    story.append(PageBreak())

    # ===================== CAP 09 =====================
    story.append(Paragraph("CAPÍTULO 09", styles["ChapterKicker"]))
    story.append(Paragraph("Conteúdo Programático", styles["ChapterTitle"]))
    story.append(HRFlowable(width="100%", color=BLUE, thickness=1.2, spaceAfter=14))

    story.append(Paragraph(
        "As 26 semanas do curso, semana a semana, com o status de cada item no momento "
        "desta geração do ebook.", styles["BodyPT"]
    ))
    story.append(Spacer(1, 6))

    def status_cell(status):
        cor_fundo = {"Concluída": GREEN_BG, "Em andamento": ORANGE_BG, "Pendente": GRAY_BG}[status]
        cor_texto = {"Concluída": GREEN, "Em andamento": ORANGE, "Pendente": GRAY}[status]
        return Paragraph(
            f'<font color="{cor_texto.hexval()}"><b>{status}</b></font>',
            ParagraphStyle(name=f"Status{status}", parent=styles["CellText"], backColor=cor_fundo)
        )

    programa_rows = [
        ["Fase", "Semana", "Item", "Status"],
        ["1 - Fundamentos", "Sem 1", "Python profissional, API Anthropic", "Concluída"],
        ["1 - Fundamentos", "Sem 2", "Embeddings e similaridade semântica (Voyage AI)", "Concluída"],
        ["1 - Fundamentos", "Sem 3-4", "RAG do zero: chunking, retrieval, augmentation e generation ponta a ponta", "Concluída"],
        ["2 - Agentes e MCP", "Sem 5", "Ollama local + docker-compose", "Pendente"],
        ["2 - Agentes e MCP", "Sem 6-7", "Tool use, loop ReAct, primeiro MCP server", "Pendente"],
        ["2 - Agentes e MCP", "Sem 8", "Intent classification (few-shot + Pydantic/Instructor)", "Pendente"],
        ["2 - Agentes e MCP", "Sem 9", "Semantic Kernel como ponte .NET <-> Python", "Pendente"],
        ["2 - Agentes e MCP", "Sem 10", "LangGraph básico, multi-agent orchestrator-worker", "Pendente"],
        ["3 - RAG Avançado", "Sem 11-16", "Hybrid search, reranking, LlamaIndex, RAGAS, DSPy, Qdrant", "Pendente"],
        ["4 - Fine-tuning", "Sem 17-22", "LoRA/QLoRA (Unsloth), DPO, vLLM, MLOps, ML clássico", "Pendente"],
        ["5 - Produção + Negócio", "Sem 23-26", "LiteLLM, extração do backbone, instanciação do nicho", "Pendente"],
    ]
    programa_data = [
        [Paragraph(v, styles["CellHeader"]) for v in programa_rows[0][:3]] + [Paragraph("Status", styles["CellHeader"])]
    ] + [
        [Paragraph(row[0], styles["CellText"]), Paragraph(row[1], styles["CellText"]),
         Paragraph(row[2], styles["CellText"]), status_cell(row[3])]
        for row in programa_rows[1:]
    ]
    t4 = Table(programa_data, colWidths=[3.6 * cm, 2.2 * cm, 7.6 * cm, 2.6 * cm])
    t4.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t4)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "&bull; <font color='#2E8B57'><b>Concluída</b></font> - exercício rodado e "
        "verificado com o André.  "
        "&bull; <font color='#E07A2C'><b>Em andamento</b></font> - parte do trabalho da "
        "semana já entregue.  "
        "&bull; <font color='#5A5A5A'><b>Pendente</b></font> - ainda não iniciada.",
        styles["BodyPT"]
    ))
    story.append(PageBreak())

    doc.multiBuild(story)
    print(f"PDF gerado em: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
