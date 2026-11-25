# Especificación y pruebas de autómatas

Los tres modelos son DFA parciales: toda transición no listada va implícitamente a un estado sumidero no aceptante. En JFLAP cada evento semántico se codifica con un símbolo hexadecimal de un carácter, según los archivos `*_codigos.json`. El archivo `.jff` contiene el DFA y el SVG muestra las transiciones con nombres legibles. Estado final significa cierre de una instancia, tanto exitoso como cancelado/rechazado; el resultado de negocio se distingue por el nombre del estado.

| Modelo | Q | Σ | q₀ | F |
|---|---|---|---|---|
| Pedido | Borrador, Confirmado, Reservado, Preparación, Empacado, Despachado, Entregado, Cancelado | confirmar, reservar, preparar, empacar, despachar, entregar, cancelar | Borrador | Entregado, Cancelado |
| Reserva | Solicitada, Validada, Reservada, Consumida, Liberada, Rechazada | validar, reservar, consumir, liberar, rechazar | Solicitada | Consumida, Liberada, Rechazada |
| Compra | Borrador, Aprobada, Enviada, Recibida, Cerrada, Rechazada, Cancelada | aprobar, enviar, recibir, cerrar, rechazar, cancelar | Borrador | Cerrada, Rechazada, Cancelada |

La función δ es exactamente la lista de aristas en `generar_modelos.py`, reproducida en cada SVG. En las entradas siguientes, «acepta» significa que la secuencia termina en F.

| Modelo | Eventos | Estado o bloqueo | Resultado |
|---|---|---|---|
| Pedido | confirmar, reservar, preparar, empacar, despachar, entregar | Entregado | Acepta |
| Pedido | cancelar | Cancelado | Acepta |
| Pedido | despachar | δ(Borrador, despachar) indefinida | Rechaza |
| Pedido | confirmar, despachar | δ(Confirmado, despachar) indefinida | Rechaza |
| Reserva | validar, reservar, consumir | Consumida | Acepta |
| Reserva | validar, reservar, liberar | Liberada | Acepta |
| Reserva | consumir | δ(Solicitada, consumir) indefinida | Rechaza |
| Reserva | validar, consumir | δ(Validada, consumir) indefinida | Rechaza |
| Compra | aprobar, enviar, recibir, cerrar | Cerrada | Acepta |
| Compra | rechazar | Rechazada | Acepta |
| Compra | rechazar, enviar | δ(Rechazada, enviar) indefinida | Rechaza |
| Compra | enviar | δ(Borrador, enviar) indefinida | Rechaza |

Reproducción: `python3 verificar_automatas.py` verifica las doce secuencias con la misma δ que genera los `.jff`.

## Ejecución en JFLAP y capturas

Abrir cada `.jff` en JFLAP → *Input → Multiple Run*, pegar las cuatro cadenas codificadas del modelo y pulsar *Run Inputs*. Guardar la captura de la tabla de resultados en `automatas/capturas/` con el nombre indicado.

| Modelo (responsable) | Cadena | Eventos | Esperado | Captura |
|---|---|---|---|---|
| Pedido (Daniela Castellanos) | `123456` | confirmar…entregar | Accept | `capturas/pedido.png` |
| | `7` | cancelar | Accept | |
| | `5` | despachar | Reject | |
| | `15` | confirmar, despachar | Reject | |
| Reserva (Janneth Cabascango) | `123` | validar, reservar, consumir | Accept | `capturas/reserva.png` |
| | `124` | validar, reservar, liberar | Accept | |
| | `3` | consumir | Reject | |
| | `13` | validar, consumir | Reject | |
| Compra (Alejandro Guamán) | `1234` | aprobar, enviar, recibir, cerrar | Accept | `capturas/compra.png` |
| | `5` | rechazar | Accept | |
| | `52` | rechazar, enviar | Reject | |
| | `2` | enviar | Reject | |
