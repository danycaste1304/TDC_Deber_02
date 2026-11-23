# LOGISTPULSE Deber 2

Entrega reproducible para Teoría de la Computación. El informe en `informe.pdf` reúne los modelos, la clasificación de diez correos y el guion de exposición. Los modelos editables están en `automatas/`; el grafo y sus datos, en `grafo/`.

## Ejecutar

```sh
cd Deber_02
python3 -m unittest discover -s tests -v
python3 demo.py
```

No se requieren paquetes externos para el código ni las pruebas. Abrir los archivos `.jff` en JFLAP y usar *Input → Step* o *Multiple Run* para las secuencias de `automatas/secuencias.md`. La prueba por consola de las mismas cadenas se ejecuta con `python3 verificar_automatas.py`.

## Estructura

- `logistpulse.py`: rutas, inventario, flujo y verificadores/búsquedas de los diez casos.
- `tests/`: pruebas normales, límite e inválidas.
- `automatas/`: tres DFA JFLAP, diagramas SVG y secuencias.
- `grafo/`: grafo de planta ponderado, dirigido y datos JSON.
- `informe.md` y `informe.pdf`: desarrollo completo y versión para entrega.
- `sprints.md`: backlog, revisiones y retrospectivas.
- `presentacion.md`: guion de 8–10 minutos.

Los datos del simulador son ficticios. La clasificación NP indica pertenencia demostrada, sin inferir que el caso quede fuera de P.
