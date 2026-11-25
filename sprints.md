# Registro de sprints y trabajo del equipo

**Integrantes:** Daniela Castellanos, Jeanneth Cabascango y Alejandro Guamán. El equipo organizó la entrega en tres hitos durante la última semana, según la aclaración de Daniela. La consigna sugería tres sprints semanales; el historial disponible no acredita tres semanas de ejecución. La asignación de temas y vocerías que sigue fue declarada por el equipo; no se inventan porcentajes ni fechas de revisión.

| Hito | Backlog y resultado | Evidencia verificable | Responsable declarado | Revisión prevista |
|---|---|---|---|---|
| 1 | Tres DFA, doce secuencias y grafo de planta | `python3 verificar_automatas.py`; inspección de `.jff`, SVG y JSON | Daniela Castellanos | Jeanneth Cabascango |
| 2 | Dijkstra, BFS, FEFO, reposición, flujo y pruebas | `python3 -m unittest discover -s tests -v`; contraste de ruta 11 m y posición 23 | Jeanneth Cabascango | Alejandro Guamán |
| 3 | Diez fichas, nota de decidibilidad, PDF y guion | Informe, tabla resumen y reducciones | Alejandro Guamán | Daniela Castellanos |

## Aportes por integrante

| Integrante | Área asignada | Diagrama disponible | Exposición prevista |
|---|---|---|---|
| Daniela Castellanos | Autómatas de pedido, reserva y compra; grafo de planta | Imagen de **Pedido** | 0:00–2:45 |
| Jeanneth Cabascango | Rutas, FEFO, reposición, flujo y pruebas automatizadas | Imagen de **Reserva** | 2:45–5:30 |
| Alejandro Guamán | Fichas de los diez correos, reducciones, decidibilidad, informe PDF | Imagen de **Compra** | 5:30–8:15 |

## Retrospectiva técnica

- Se precisó que el caso c3 cubre **aristas**. Cubrir vértices propios o vecinos sería Dominating Set y no representa la política del correo.
- Se corrigió el ejemplo c2 para sumar también el tramo de regreso al origen.
- La etiqueta «NP» de n1–n4 se interpreta como evidencia de pertenencia, sin afirmar separación respecto de P.
- La validación por consola ahora lee directamente los `.jff`. Las imágenes existentes solo muestran diagramas en otra herramienta; falta la evidencia visual de *Multiple Run* en JFLAP.

## Cierre de release

El historial original contiene cuatro commits hechos el 22 y el 24 de noviembre de 2026. La versión `v1.0.0` corresponde al informe anterior a los nombres del equipo. La versión `v1.0.1` identifica la corrección del nombre, la presentación y las pruebas directas de los `.jff`. Repositorio: https://github.com/danycaste1304/TDC_Deber_02
