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

`python3 verificar_automatas.py` lee directamente los tres `.jff` y verifica las doce secuencias. Los resultados observados están en `resultados_jff.md` y `resultados_visuales/`.

## Cadenas codificadas de prueba

Cada símbolo representa un evento del alfabeto indicado en `*_codigos.json`. La columna «observado» se obtuvo ejecutando el archivo `.jff` con el verificador independiente.

| Modelo | Cadena | Eventos | Esperado | Observado |
|---|---|---|---|---|
| Pedido | `123456` | confirmar…entregar | Acepta | Acepta |
| Pedido | `7` | cancelar | Acepta | Acepta |
| Pedido | `5` | despachar | Rechaza | Rechaza |
| Pedido | `15` | confirmar, despachar | Rechaza | Rechaza |
| Reserva | `123` | validar, reservar, consumir | Acepta | Acepta |
| Reserva | `124` | validar, reservar, liberar | Acepta | Acepta |
| Reserva | `3` | consumir | Rechaza | Rechaza |
| Reserva | `13` | validar, consumir | Rechaza | Rechaza |
| Compra | `1234` | aprobar, enviar, recibir, cerrar | Acepta | Acepta |
| Compra | `5` | rechazar | Acepta | Acepta |
| Compra | `52` | rechazar, enviar | Rechaza | Rechaza |
| Compra | `2` | enviar | Rechaza | Rechaza |
