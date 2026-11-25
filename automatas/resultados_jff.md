# Resultados reproducibles de los archivos JFF

Ejecutado con `python3 verificar_automatas.py`. Este programa lee los `.jff` directamente; no es una captura de JFLAP.

| Autómata | Cadena | Esperado | Observado |
|---|---|---|---|
| pedido | 123456 | Acepta | Acepta |
| pedido | 7 | Acepta | Acepta |
| pedido | 5 | Rechaza | Rechaza |
| pedido | 15 | Rechaza | Rechaza |
| reserva | 123 | Acepta | Acepta |
| reserva | 124 | Acepta | Acepta |
| reserva | 3 | Rechaza | Rechaza |
| reserva | 13 | Rechaza | Rechaza |
| compra | 1234 | Acepta | Acepta |
| compra | 5 | Acepta | Acepta |
| compra | 52 | Rechaza | Rechaza |
| compra | 2 | Rechaza | Rechaza |
