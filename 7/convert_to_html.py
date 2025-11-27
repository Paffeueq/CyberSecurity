#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Odczyt markdown
with open('PODSUMOWANIE_ZADAŃ.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Konwersja markdown → HTML (prosty sposób)
html_lines = []
lines = md_content.split('\n')

in_code_block = False
code_lang = ''

for line in lines:
    # Code block
    if line.startswith('```'):
        if in_code_block:
            html_lines.append('</code></pre>')
            in_code_block = False
        else:
            code_lang = line[3:].strip()
            html_lines.append(f'<pre><code class="{code_lang}">')
            in_code_block = True
    elif in_code_block:
        html_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    # Headers
    elif line.startswith('# '):
        html_lines.append(f'<h1>{line[2:]}</h1>')
    elif line.startswith('## '):
        html_lines.append(f'<h2>{line[3:]}</h2>')
    elif line.startswith('### '):
        html_lines.append(f'<h3>{line[4:]}</h3>')
    # Tables
    elif line.startswith('|'):
        html_lines.append(f'<table><tr><td colspan="4">{line}</td></tr></table>')
    # Bold, italic, code inline
    elif line.strip():
        line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
        line = line.replace('*', '<em>', 1).replace('*', '</em>', 1)
        line = line.replace('`', '<code>', 1).replace('`', '</code>', 1)
        
        if line.startswith('- '):
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith('✅'):
            html_lines.append(f'<p style="color: green;">✅ {line[2:]}</p>')
        elif line.startswith('⚠️'):
            html_lines.append(f'<p style="color: orange;">⚠️ {line[2:]}</p>')
        else:
            html_lines.append(f'<p>{line}</p>')
    else:
        html_lines.append('')

html_body = '\n'.join(html_lines)

# Pełny HTML
html_full = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ochrona Danych - Podsumowanie Zadań 1-5</title>
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #2c3e50; padding: 60px 50px; max-width: 1000px; margin: 0 auto; background: #f8f9fa; }}
        
        h1 {{ color: #1a4d7a; font-size: 2.2em; margin-bottom: 10px; border-bottom: 4px solid #3498db; padding-bottom: 15px; text-align: center; }}
        h2 {{ color: #2980b9; font-size: 1.5em; margin-top: 40px; margin-bottom: 20px; border-left: 5px solid #3498db; padding-left: 15px; }}
        h3 {{ color: #34495e; font-size: 1.1em; margin-top: 15px; margin-bottom: 10px; }}
        
        p {{ margin: 15px 0; }}
        li {{ margin: 8px 0; margin-left: 20px; }}
        
        code {{ background: #ecf0f1; padding: 3px 8px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 0.95em; color: #c0392b; }}
        pre {{ background: #2c3e50; color: #ecf0f1; padding: 20px; border-radius: 5px; overflow-x: auto; line-height: 1.5; margin: 15px 0; border-left: 4px solid #e74c3c; }}
        pre code {{ background: none; padding: 0; color: #ecf0f1; font-size: 0.9em; }}
        
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        table th {{ background: #3498db; color: white; padding: 15px; text-align: left; font-weight: bold; }}
        table td {{ border: 1px solid #bdc3c7; padding: 12px 15px; }}
        table tr:hover {{ background: #f0f7ff; }}
        table tr:nth-child(even) {{ background: #f9f9f9; }}
        
        .meta {{ text-align: center; color: #7f8c8d; font-size: 0.95em; margin-bottom: 30px; border-bottom: 1px solid #bdc3c7; padding-bottom: 20px; }}
        .checklist {{ background: #d4edda; padding: 20px; border-left: 5px solid #28a745; margin: 20px 0; border-radius: 4px; }}
        .architecture {{ background: #e3f2fd; padding: 15px; border-left: 5px solid #2196f3; margin: 15px 0; font-family: monospace; line-height: 1.6; }}
        .key-point {{ background: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; margin: 15px 0; border-radius: 4px; }}
        
        .section {{ page-break-inside: avoid; background: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        
        strong {{ color: #c0392b; font-weight: bold; }}
        em {{ color: #8e44ad; font-style: italic; }}
        
        @media print {{ 
            body {{ background: white; }}
            .section {{ page-break-inside: avoid; box-shadow: none; border: 1px solid #ddd; }}
            a {{ color: #2980b9; text-decoration: underline; }}
        }}
    </style>
</head>
<body>

<div class="meta">
    <strong>Ochrona Danych - Praktyka Bezpieczeństwa Sieci</strong><br>
    Podsumowanie Zadań 1-5<br>
    27 listopada 2025 | Paweł
</div>

{html_body}

<div style="text-align: center; margin-top: 60px; padding-top: 20px; border-top: 2px solid #bdc3c7; color: #7f8c8d;">
    <p><strong>✅ Gotowy do rozmowy z prowadzącym!</strong></p>
    <p style="font-size: 0.9em;">Dokument wygenerowany: 27.11.2025 | Wersja: 1.0</p>
</div>

</body>
</html>"""

# Zapis
with open('PODSUMOWANIE_ZADAŃ.html', 'w', encoding='utf-8') as f:
    f.write(html_full)

print("✅ HTML created successfully: PODSUMOWANIE_ZADAŃ.html")
print("📄 To convert to PDF, open the HTML file in browser:")
print("   • Firefox/Chrome: Ctrl+P → Save as PDF")
print("   • Or use: wsl wkhtmltopdf PODSUMOWANIE_ZADAŃ.html PODSUMOWANIE_ZADAŃ.pdf")
