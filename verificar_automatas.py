"""Verifica cadenas leyendo directamente los archivos JFLAP (.jff).

La salida sirve como evidencia reproducible del XML. No sustituye una captura
de la interfaz Input > Multiple Run de JFLAP.
"""
from pathlib import Path
from xml.etree import ElementTree as ET

BASE = Path(__file__).parent / 'automatas'
CASOS = {
    'pedido': [('123456', True), ('7', True), ('5', False), ('15', False)],
    'reserva': [('123', True), ('124', True), ('3', False), ('13', False)],
    'compra': [('1234', True), ('5', True), ('52', False), ('2', False)],
}


def cargar_jff(ruta):
    raiz = ET.parse(ruta).getroot()
    if raiz.findtext('type') != 'fa':
        raise ValueError('El archivo no contiene un autómata finito')
    estados = raiz.findall('./automaton/state')
    iniciales = [e.attrib['id'] for e in estados if e.find('initial') is not None]
    if len(iniciales) != 1:
        raise ValueError('Debe existir exactamente un estado inicial')
    finales = {e.attrib['id'] for e in estados if e.find('final') is not None}
    delta = {}
    for t in raiz.findall('./automaton/transition'):
        clave = (t.findtext('from'), t.findtext('read'))
        if clave in delta:
            raise ValueError('Transición no determinista')
        delta[clave] = t.findtext('to')
    return iniciales[0], finales, delta


def acepta(automata, cadena):
    estado, finales, delta = automata
    for simbolo in cadena:
        estado = delta.get((estado, simbolo))
        if estado is None:
            return False
    return estado in finales


def ejecutar():
    filas = []
    for nombre, casos in CASOS.items():
        automata = cargar_jff(BASE / f'{nombre}.jff')
        for cadena, esperado in casos:
            observado = acepta(automata, cadena)
            assert observado == esperado, (nombre, cadena, esperado, observado)
            filas.append((nombre, cadena, 'Acepta' if esperado else 'Rechaza',
                         'Acepta' if observado else 'Rechaza'))
    return filas


if __name__ == '__main__':
    print('# Resultados reproducibles de los archivos JFF\n')
    print('Ejecutado con `python3 verificar_automatas.py`. Este programa lee los'
          ' `.jff` directamente; no es una captura de JFLAP.\n')
    print('| Autómata | Cadena | Esperado | Observado |')
    print('|---|---|---|---|')
    for fila in ejecutar():
        print('| ' + ' | '.join(fila) + ' |')
