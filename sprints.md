# Registro de sprints y trabajo del equipo

**Integrantes:** Daniela Castellanos, Janneth Cabascango y Alejandro Guamán. El trabajo se repartió en tres partes iguales (≈33 % cada una): cada integrante lideró un sprint, ejecutó en JFLAP un autómata, revisó el trabajo de otro integrante y expone 2:45 min.

| Sprint | Backlog y resultado | Revisión verificable | Responsable | Revisión por pares |
|---|---|---|---|---|
| 1 | Tres DFA, doce secuencias y grafo de planta | `python3 verificar_automatas.py`; inspección de `.jff`, SVG y JSON | Daniela Castellanos | Janneth Cabascango |
| 2 | Dijkstra, BFS, FEFO, reposición, flujo y pruebas | `python3 -m unittest discover -s tests -v`; contraste de ruta 11 m y posición 23 | Janneth Cabascango | Alejandro Guamán |
| 3 | Diez fichas, nota de decidibilidad, PDF y guion | Revisión técnica de reducciones y presentación oral | Alejandro Guamán | Daniela Castellanos |

## Aportes por integrante

| Integrante | Desarrollo | Evidencia JFLAP | Exposición |
|---|---|---|---|
| Daniela Castellanos | Autómatas de pedido, reserva y compra; grafo de planta | Captura de **Pedido** | 0:00–2:45 |
| Janneth Cabascango | Rutas, FEFO, reposición, flujo y pruebas automatizadas | Captura de **Reserva** | 2:45–5:30 |
| Alejandro Guamán | Fichas de los diez correos, reducciones, decidibilidad, informe PDF | Captura de **Compra** | 5:30–8:15 |

## Retrospectiva técnica

- Se precisó que el caso c3 cubre **aristas**. Cubrir vértices propios o vecinos sería Dominating Set y no representa la política del correo.
- Se corrigió el ejemplo c2 para sumar también el tramo de regreso al origen.
- La etiqueta «NP» de n1–n4 se interpreta como evidencia de pertenencia, sin afirmar separación respecto de P.
- La validación por consola de los DFA se complementa con capturas de JFLAP en `automatas/capturas/`.

## Cierre de release

Versión `v1.0.0`. Criterio de cierre: pruebas automatizadas verdes, revisión visual del PDF y capturas JFLAP de los tres autómatas. Repositorio: https://github.com/danycaste1304/TDC_Deber_02
