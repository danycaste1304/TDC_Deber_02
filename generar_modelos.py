"""Genera DFA JFLAP y SVG sin bibliotecas externas."""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import html
import json

BASE = Path(__file__).parent
OUT = BASE / 'automatas'
OUT.mkdir(exist_ok=True)
MODELOS = {
 'pedido': (['Borrador','Confirmado','Reservado','Preparación','Empacado','Despachado','Entregado','Cancelado'],
            ['confirmar','reservar','preparar','empacar','despachar','entregar','cancelar'],
            [('Borrador','confirmar','Confirmado'),('Confirmado','reservar','Reservado'),('Reservado','preparar','Preparación'),('Preparación','empacar','Empacado'),('Empacado','despachar','Despachado'),('Despachado','entregar','Entregado'),('Borrador','cancelar','Cancelado'),('Confirmado','cancelar','Cancelado'),('Reservado','cancelar','Cancelado')],
            ['Entregado','Cancelado']),
 'reserva': (['Solicitada','Validada','Reservada','Consumida','Liberada','Rechazada'],
             ['validar','reservar','consumir','liberar','rechazar'],
             [('Solicitada','validar','Validada'),('Validada','reservar','Reservada'),('Reservada','consumir','Consumida'),('Reservada','liberar','Liberada'),('Solicitada','rechazar','Rechazada'),('Validada','rechazar','Rechazada')],
             ['Consumida','Liberada','Rechazada']),
 'compra': (['Borrador','Aprobada','Enviada','Recibida','Cerrada','Rechazada','Cancelada'],
           ['aprobar','enviar','recibir','cerrar','rechazar','cancelar'],
           [('Borrador','aprobar','Aprobada'),('Aprobada','enviar','Enviada'),('Enviada','recibir','Recibida'),('Recibida','cerrar','Cerrada'),('Borrador','rechazar','Rechazada'),('Borrador','cancelar','Cancelada'),('Aprobada','cancelar','Cancelada')],
           ['Cerrada','Rechazada','Cancelada'])
}

for nombre, (estados, alfabeto, aristas, finales) in MODELOS.items():
    # JFLAP usa símbolos de un carácter. El vocabulario semántico se conserva
    # en la tabla y el SVG, y cada evento se codifica con su índice hexadecimal.
    codigos = {evento: format(i + 1, 'X') for i, evento in enumerate(alfabeto)}
    root = Element('structure')
    SubElement(root,'type').text = 'fa'
    automaton = SubElement(root,'automaton')
    for i, estado in enumerate(estados):
        st = SubElement(automaton,'state',id=str(i),name=estado)
        SubElement(st,'x').text = str(90 + 170 * (i % 4))
        SubElement(st,'y').text = str(110 + 180 * (i // 4))
        if i == 0: SubElement(st,'initial')
        if estado in finales: SubElement(st,'final')
    for u, evento, v in aristas:
        t = SubElement(automaton,'transition')
        SubElement(t,'from').text = str(estados.index(u))
        SubElement(t,'to').text = str(estados.index(v))
        SubElement(t,'read').text = codigos[evento]
    ElementTree(root).write(OUT / f'{nombre}.jff', encoding='utf-8', xml_declaration=True)
    # Diagrama SVG claro y editable. La tabla de aristas es la especificación.
    rows = [f'<text x="24" y="{42+i*24}" font-size="16">{html.escape(u)} —{html.escape(e)}→ {html.escape(v)}</text>' for i,(u,e,v) in enumerate(aristas)]
    header = f'<text x="24" y="25" font-size="20" font-weight="bold">{nombre.title()} · q₀={estados[0]} · F={", ".join(finales)}</text>'
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="980" height="'+str(70+len(aristas)*24)+'" viewBox="0 0 980 '+str(70+len(aristas)*24)+'"><rect width="100%" height="100%" fill="#f6f8fb"/>'+header+''.join(rows)+'</svg>'
    (OUT/f'{nombre}.svg').write_text(svg,encoding='utf-8')
    (OUT/f'{nombre}_codigos.json').write_text(json.dumps(codigos,ensure_ascii=False,indent=2),encoding='utf-8')

grafo = {'dirigido':True,'bloqueados':['X'],'origen':'R','destino':'D','unidades':'metros',
         'aristas':[['R','B',2],['R','A',8],['B','A',2],['B','P',9],['A','P',3],['P','E',2],['E','D',2]]}
(BASE/'grafo').mkdir(exist_ok=True)
(BASE/'grafo'/'planta.json').write_text(json.dumps(grafo,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'grafo'/'planta.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="360" viewBox="0 0 1000 360"><defs><marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#216db3"/></marker></defs><rect width="100%" height="100%" fill="#f6f8fb"/><text x="30" y="35" font-size="24" font-weight="bold">Planta AMR · ruta R → B → A → P → E → D · 11 m</text><g stroke="#216db3" stroke-width="4" marker-end="url(#f)"><path d="M120 180L270 180"/><path d="M340 180L455 180"/><path d="M525 180L640 180"/><path d="M710 180L795 180"/><path d="M855 180L940 180"/></g><g stroke="#9aa8b8" stroke-width="2" fill="none"><path d="M120 175Q280 60 455 175"/><path d="M340 185Q500 310 640 185"/></g><g font-size="16" fill="#17375e"><text x="185" y="165">2</text><text x="392" y="165">2</text><text x="580" y="165">3</text><text x="744" y="165">2</text><text x="895" y="165">2</text><text x="245" y="78">8</text><text x="490" y="285">9</text></g><g fill="#17375e" stroke="white" stroke-width="3"><circle cx="95" cy="180" r="29"/><circle cx="305" cy="180" r="29"/><circle cx="490" cy="180" r="29"/><circle cx="675" cy="180" r="29"/><circle cx="825" cy="180" r="29"/><circle cx="965" cy="180" r="29"/></g><g fill="white" text-anchor="middle" font-size="18" font-weight="bold"><text x="95" y="187">R</text><text x="305" y="187">B</text><text x="490" y="187">A</text><text x="675" y="187">P</text><text x="825" y="187">E</text><text x="965" y="187">D</text></g><text x="30" y="335" font-size="16">Aristas dirigidas; pesos no negativos. Zona X bloqueada y excluida de V transitable.</text></svg>''',encoding='utf-8')
