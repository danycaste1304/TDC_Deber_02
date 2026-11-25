"""Convierte el informe Markdown a un PDF legible para entrega."""
from pathlib import Path
from html import escape
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, KeepTogether, HRFlowable

base = Path(__file__).parent
pdfmetrics.registerFont(TTFont('ArialUnicode','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialUnicodeBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('ArialUnicode',normal='ArialUnicode',bold='ArialUnicodeBold')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TDCBody',fontName='ArialUnicode',fontSize=9.4,leading=13.3,spaceAfter=7,textColor=colors.HexColor('#18314d')))
styles.add(ParagraphStyle(name='TDCTitle',fontName='ArialUnicodeBold',fontSize=20,leading=24,spaceAfter=14,textColor=colors.HexColor('#163958')))
styles.add(ParagraphStyle(name='TDCH1',fontName='ArialUnicodeBold',fontSize=13,leading=17,spaceBefore=15,spaceAfter=8,textColor=colors.HexColor('#1769aa')))
styles.add(ParagraphStyle(name='TDCH2',fontName='ArialUnicodeBold',fontSize=10.5,leading=14,spaceBefore=11,spaceAfter=5,textColor=colors.HexColor('#17375e')))
styles.add(ParagraphStyle(name='TDCCell',fontName='ArialUnicode',fontSize=8.1,leading=11,spaceAfter=3,textColor=colors.HexColor('#18314d')))
styles.add(ParagraphStyle(name='TDCCode',fontName='ArialUnicode',fontSize=8,leading=11,spaceBefore=5,spaceAfter=8,backColor=colors.HexColor('#f2f6fa')))

def inline(s):
    s=escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`(.+?)`',r'<font color="#0f659f">\1</font>',s)
    return s

lines=(base/'informe.md').read_text(encoding='utf-8').splitlines()
story=[]; paragraph=[]; code=[]; table=[]; in_code=False

def flush_paragraph():
    if paragraph:
        story.append(Paragraph(inline(' '.join(paragraph)),styles['TDCBody']))
        paragraph.clear()

def flush_table():
    if table:
        # Cada fila es una ficha compacta; evita reducir cinco columnas a letra ilegible.
        for row in table[2:]:
            cells=[c.strip() for c in row.strip('|').split('|')]
            if len(cells)>=5:
                story.append(Paragraph(f'<b>{inline(cells[0])} · {inline(cells[1])}</b><br/>{inline(cells[2])} · {inline(cells[3])}<br/>{inline(cells[4])}',styles['TDCCell']))
        table.clear()

for line in lines:
    if line.startswith('```'):
        flush_paragraph(); flush_table()
        if in_code:
            story.append(Preformatted('\n'.join(code),styles['TDCCode']))
            code=[]; in_code=False
        else: in_code=True
        continue
    if in_code:
        code.append(line)
        continue
    if line.startswith('|'):
        flush_paragraph(); table.append(line); continue
    if table: flush_table()
    if line.startswith('# '):
        flush_paragraph(); story.append(Paragraph(inline(line[2:]),styles['TDCTitle']))
    elif line.startswith('## '):
        flush_paragraph(); story.append(Paragraph(inline(line[3:]),styles['TDCH1']))
    elif line.startswith('### '):
        flush_paragraph(); story.append(Paragraph(inline(line[4:]),styles['TDCH2']))
    elif not line.strip(): flush_paragraph()
    else: paragraph.append(line.strip())
flush_paragraph(); flush_table()

def footer(canvas,doc):
    canvas.saveState()
    canvas.setFont('ArialUnicode',8)
    canvas.setFillColor(colors.HexColor('#60758a'))
    canvas.drawString(42,28,'LOGISTPULSE · Deber 2 · Teoría de la Computación')
    canvas.drawRightString(A4[0]-42,28,str(doc.page))
    canvas.restoreState()

doc=SimpleDocTemplate(str(base/'informe.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=48,
                      title='Fundamentación formal de LOGISTPULSE',author='Daniela Castellanos, Jeanneth Cabascango, Alejandro Guamán')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(base/'informe.pdf')
