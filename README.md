# LOGISTPULSE Deber 2

**Integrantes:** Daniela Castellanos, Jeanneth Cabascango y Alejandro Guamán · Repositorio: https://github.com/danycaste1304/TDC_Deber_02

Entrega reproducible para Teoría de la Computación. El informe en `informe.pdf` reúne los modelos y la clasificación de diez correos. Está compilado desde `informe.tex` en Times New Roman de 12 puntos. La presentación tiene diez diapositivas.

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
- `informe.tex` y `informe.pdf`: fuente LaTeX y versión compilada para entrega; `informe.md` conserva el contenido en Markdown.
- `sprints.md`: tres hitos de la última semana y evidencias verificables.
- `presentacion_LOGISTPULSE.pptx` y `presentacion_LOGISTPULSE.pdf`: presentación editable y versión PDF; `presentacion.md`: distribución del contenido en 9 minutos.

La clasificación NP indica pertenencia demostrada, sin inferir que el caso quede fuera de P.

**Evidencia de autómatas:** `automatas/resultados_jff.md` y `automatas/resultados_visuales/` contienen doce pruebas ejecutadas leyendo los `.jff`. Los diagramas están en `automatas/diagramas_referencia/`.
