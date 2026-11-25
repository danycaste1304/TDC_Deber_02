"""Crea láminas de resultados a partir de la ejecución real de los .jff."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from verificar_automatas import ejecutar

BASE = Path(__file__).parent / 'automatas' / 'resultados_visuales'
BASE.mkdir(exist_ok=True)
REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
titulo = ImageFont.truetype(BOLD, 42)
subtitulo = ImageFont.truetype(REGULAR, 25)
cabecera = ImageFont.truetype(BOLD, 25)
celda = ImageFont.truetype(REGULAR, 28)
pie = ImageFont.truetype(REGULAR, 19)

for nombre in ('pedido', 'reserva', 'compra'):
    filas = [fila for fila in ejecutar() if fila[0] == nombre]
    imagen = Image.new('RGB', (1200, 640), '#f5f8fc')
    d = ImageDraw.Draw(imagen)
    d.rounded_rectangle((28, 28, 1172, 612), radius=20, fill='white', outline='#d6e2ee', width=2)
    d.rectangle((28, 28, 1172, 40), fill='#bd2637')
    d.text((62, 74), f'Autómata de {nombre}', font=titulo, fill='#17375e')
    d.text((62, 135), f'Verificación automatizada de {nombre}.jff', font=subtitulo, fill='#49627e')
    columnas = ((76, 'Cadena'), (346, 'Esperado'), (620, 'Observado'), (930, 'Coincide'))
    d.rounded_rectangle((62, 205, 1138, 263), radius=8, fill='#e8f1fa')
    for x, texto in columnas:
        d.text((x, 219), texto, font=cabecera, fill='#17375e')
    for i, (_, cadena, esperado, observado) in enumerate(filas):
        y = 277 + i * 70
        if i % 2 == 0:
            d.rectangle((62, y - 6, 1138, y + 56), fill='#f7f9fc')
        d.text((76, y + 7), cadena, font=celda, fill='#17375e')
        d.text((346, y + 7), esperado, font=celda, fill='#19815a' if esperado == 'Acepta' else '#b72539')
        d.text((620, y + 7), observado, font=celda, fill='#19815a' if observado == 'Acepta' else '#b72539')
        d.text((930, y + 7), 'Sí' if esperado == observado else 'No', font=celda, fill='#19815a' if esperado == observado else '#b72539')
    d.text((62, 579), 'Fuente: archivo JFF leído por verificar_automatas.py · 2 válidas y 2 inválidas', font=pie, fill='#5a7088')
    imagen.save(BASE / f'{nombre}.png', optimize=True)
    print(BASE / f'{nombre}.png')
