import os
import glob
from datetime import datetime
from docx import Document

# Procura qualquer arquivo .docx dentro da pasta 'entrada'
arquivos_docx = glob.glob("entrada/*.docx")

if not arquivos_docx:
    print("Nenhum arquivo .docx encontrado na pasta 'entrada'.")
    exit(0)

# Pega o primeiro arquivo da lista (usando índice 0)
caminho_doc = arquivos_docx[0]
print(f"Lendo arquivo: {caminho_doc}")
doc = Document(caminho_doc)

# Filtra parágrafos vazios
paragrafos = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

if not paragrafos:
    print("O documento está vazio.")
    exit(0)

# Pega o primeiro parágrafo como título e o segundo como subtítulo
titulo = paragrafos[0]
subtitulo = paragrafos[1] if len(paragrafos) > 2 else ""
corpo_paragrafos = paragrafos[2:] if len(paragrafos) > 2 else paragrafos[1:]

# Formata os parágrafos do corpo em HTML
corpo_html = "\n".join([f"<p>{p}</p>" for p in corpo_paragrafos])

# Data atual formatada
data_atual = datetime.now().strftime("%d/%m/%Y • %H:%M")

# Template HTML/CSS inspirado no layout editorial da Bloomberg
html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Inter:wght@400;600;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #ffffff;
            --text-main: #111111;
            --text-muted: #555555;
            --accent-blue: #0047ff;
            --border-color: #e0e0e0;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        header {{
            border-bottom: 1px solid var(--text-main);
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .brand {{
            font-weight: 800;
            font-size: 1.4rem;
            letter-spacing: -0.04em;
            text-transform: uppercase;
        }}
        .category-tag {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--accent-blue);
        }}
        main {{
            max-width: 720px;
            margin: 48px auto;
            padding: 0 20px;
        }}
        .article-header {{
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 24px;
            margin-bottom: 32px;
        }}
        h1 {{
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            font-size: clamp(2rem, 4vw, 3rem);
            line-height: 1.12;
            letter-spacing: -0.03em;
            margin-bottom: 16px;
            color: #000000;
        }}
        .subheadline {{
            font-size: 1.2rem;
            color: var(--text-muted);
            font-weight: 400;
            line-height: 1.45;
            margin-bottom: 20px;
        }}
        .meta {{
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            gap: 16px;
        }}
        .article-body {{
            font-family: 'Newsreader', Georgia, serif;
            font-size: 1.25rem;
            line-height: 1.75;
            color: #1a1a1a;
        }}
        .article-body p {{
            margin-bottom: 24px;
        }}
        .article-body p:first-of-type::first-letter {{
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            font-size: 3.4rem;
            float: left;
            line-height: 0.85;
            margin-right: 12px;
            margin-top: 4px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="brand">MERCADOS & ANÁLISE</div>
        <div class="category-tag">Relatório Especial</div>
    </header>

    <main>
        <article>
            <div class="article-header">
                <h1>{titulo}</h1>
                {f'<p class="subheadline">{subtitulo}</p>' if subtitulo else ''}
                <div class="meta">
                    <span>Publicado em {data_atual}</span>
                </div>
            </div>
            <div class="article-body">
                {corpo_html}
            </div>
        </article>
    </main>
</body>
</html>
"""

# Garante que a pasta de saída existe e salva o arquivo
os.makedirs("saida", exist_ok=True)
with open("saida/index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("HTML gerado com sucesso em saida/index.html!")
