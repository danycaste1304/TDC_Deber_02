# LOGISTPULSE Deber 2

**Integrantes:** Daniela Castellanos, Jeanneth Cabascango y Alejandro Guamán · Repositorio: https://github.com/danycaste1304/TDC_Deber_02

Entrega reproducible para Teoría de la Computación. El informe en `informe.pdf` reúne los modelos, la clasificación de diez correos y el guion de exposición. Los modelos editables están en `automatas/`; el grafo y sus datos, en `grafo/`.

## Ejecutar

```sh
cd TDC_Deber_02
python3 -m unittest discover -s tests -v
python3 demo.py
```

No se requieren paquetes externos para el código ni las pruebas. `python3 verificar_automatas.py` lee los archivos `.jff` y comprueba las doce cadenas codificadas.

## Estructura

- `logistpulse.py`: rutas, inventario, flujo y verificadores/búsquedas de los diez casos.
- `tests/`: pruebas normales, límite e inválidas.
- `automatas/`: tres DFA `.jff`, diagramas y doce resultados reproducibles en tabla e imágenes.
- `grafo/`: grafo de planta ponderado, dirigido y datos JSON.
- `informe.md` y `informe.pdf`: desarrollo completo y versión para entrega.
- `sprints.md`: tres hitos de la última semana y evidencias verificables.
- `presentacion.html`: ocho diapositivas navegables con las flechas del teclado; `presentacion.md`: guion de 8–10 minutos.

Los datos del simulador son ficticios. La clasificación NP indica pertenencia demostrada, sin inferir que el caso quede fuera de P.

**Evidencia de autómatas:** `automatas/resultados_jff.md` y `automatas/resultados_visuales/` contienen doce pruebas ejecutadas leyendo los `.jff`. Los diagramas están en `automatas/diagramas_referencia/`.
