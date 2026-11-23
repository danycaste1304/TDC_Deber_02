# Registro de sprints y trabajo del equipo

Este registro identifica artefactos preparados para la entrega. Los nombres de responsables y las revisiones humanas deben completarse con datos reales del equipo; no se atribuyen participaciones ficticias.

| Sprint | Backlog y resultado | Revisión verificable | Responsable del equipo |
|---|---|---|---|
| 1 | Tres DFA, doce secuencias y grafo de planta | `python3 verificar_automatas.py`; inspección de `.jff`, SVG y JSON | Por asignar |
| 2 | Dijkstra, BFS, FEFO, reposición, flujo y pruebas | `python3 -m unittest discover -s tests -v`; contraste de ruta 11 m y posición 23 | Por asignar |
| 3 | Diez fichas, nota de decidibilidad, PDF y guion | Revisión técnica de reducciones y presentación oral | Por asignar |

## Retrospectiva técnica

- Se precisó que el caso c3 cubre **aristas**. Cubrir vértices propios o vecinos sería Dominating Set y no representa la política del correo.
- Se corrigió el ejemplo c2 para sumar también el tramo de regreso al origen.
- La etiqueta «NP» de n1–n4 se interpreta como evidencia de pertenencia, sin afirmar separación respecto de P.
- La validación por consola de los DFA no equivale a una captura de JFLAP. Ese paso visual corresponde a la revisión final del equipo.

## Cierre de release

Versión preparada: `v1.0.0`. Criterio de cierre: pruebas automatizadas verdes, revisión visual del PDF y archivos `.jff` abiertos por el equipo en JFLAP. Registrar fecha, integrantes, revisión por pares y enlace remoto cuando se conozcan.
