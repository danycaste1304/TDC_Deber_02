from generar_modelos import MODELOS

CASOS = {
 'pedido': [(['confirmar','reservar','preparar','empacar','despachar','entregar'],True),(['cancelar'],True),(['despachar'],False),(['confirmar','despachar'],False)],
 'reserva': [(['validar','reservar','consumir'],True),(['validar','reservar','liberar'],True),(['consumir'],False),(['validar','consumir'],False)],
 'compra': [(['aprobar','enviar','recibir','cerrar'],True),(['rechazar'],True),(['rechazar','enviar'],False),(['enviar'],False)]
}

for nombre, casos in CASOS.items():
    estados, alfabeto, aristas, finales = MODELOS[nombre]
    delta = {(u,e):v for u,e,v in aristas}
    for secuencia, esperado in casos:
        estado = estados[0]
        for evento in secuencia:
            estado = delta.get((estado,evento))
            if estado is None: break
        obtenido = estado in finales
        assert obtenido == esperado, (nombre,secuencia,esperado,obtenido)
        print(nombre, ' → '.join([estados[0]]+secuencia), 'ACEPTA' if obtenido else 'RECHAZA')
