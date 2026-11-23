"""Algoritmos reproducibles del Deber 2 de LOGISTPULSE."""
from collections import deque
from datetime import date
from heapq import heappop, heappush
from itertools import combinations, permutations, product


def bfs(grafo, origen, destino):
    if origen not in grafo or destino not in grafo:
        raise ValueError("origen o destino ausente")
    cola, padre = deque([origen]), {origen: None}
    while cola:
        u = cola.popleft()
        if u == destino:
            ruta = []
            while u is not None:
                ruta.append(u)
                u = padre[u]
            return ruta[::-1]
        for v in grafo[u]:
            if v not in grafo:
                raise ValueError("arista hacia vértice ausente")
            if v not in padre:
                padre[v] = u
                cola.append(v)
    return None


def dijkstra(grafo, origen, destino):
    if origen not in grafo or destino not in grafo:
        raise ValueError("origen o destino ausente")
    for salidas in grafo.values():
        for v, peso in salidas:
            if v not in grafo or not isinstance(peso, (int, float)) or peso < 0:
                raise ValueError("arista inválida o peso negativo")
    distancia, padre = {origen: 0}, {origen: None}
    cola = [(0, origen)]
    while cola:
        costo, u = heappop(cola)
        if costo != distancia[u]:
            continue
        if u == destino:
            ruta = []
            while u is not None:
                ruta.append(u)
                u = padre[u]
            return costo, ruta[::-1]
        for v, peso in grafo[u]:
            nuevo = costo + peso
            if nuevo < distancia.get(v, float("inf")):
                distancia[v], padre[v] = nuevo, u
                heappush(cola, (nuevo, v))
    return None


def fefo(lotes, cantidad, hoy):
    if not isinstance(cantidad, int) or cantidad < 0:
        raise ValueError("cantidad inválida")
    if not isinstance(hoy, date):
        raise ValueError("fecha inválida")
    candidatos = []
    for codigo, vencimiento, disponible in lotes:
        if not isinstance(vencimiento, date) or not isinstance(disponible, int) or disponible < 0:
            raise ValueError("lote inválido")
        if vencimiento >= hoy and disponible > 0:
            candidatos.append((vencimiento, codigo, disponible))
    pendientes, plan = cantidad, []
    for _, codigo, disponible in sorted(candidatos):
        toma = min(pendientes, disponible)
        if toma:
            plan.append((codigo, toma))
            pendientes -= toma
        if pendientes == 0:
            break
    # Política atómica: no se confirma reserva parcial.
    return plan if pendientes == 0 else None


def reposicion(disponible, en_orden, reservado, minimo, objetivo):
    valores = (disponible, en_orden, reservado, minimo, objetivo)
    if any(not isinstance(x, int) or x < 0 for x in valores) or objetivo < minimo:
        raise ValueError("parámetros de reposición inválidos")
    posicion = disponible + en_orden - reservado
    return posicion, max(0, objetivo - posicion) if posicion <= minimo else 0


def verificar_vertex_cover(vertices, aristas, k, certificado):
    vertices, certificado = set(vertices), set(certificado)
    if not isinstance(k, int) or k < 0 or len(certificado) > k or not certificado <= vertices:
        return False
    if any(u not in vertices or v not in vertices for u, v in aristas):
        return False
    return all(u in certificado or v in certificado for u, v in aristas)


def buscar_vertex_cover(vertices, aristas, k):
    vertices = tuple(vertices)
    for r in range(min(k, len(vertices)) + 1):
        for candidato in combinations(vertices, r):
            if verificar_vertex_cover(vertices, aristas, k, candidato):
                return candidato
    return None


def verificar_sat(clausulas, asignacion):
    return all(any(asignacion[abs(l)] == (l > 0) for l in clausula) for clausula in clausulas)


def buscar_sat(clausulas, n):
    for valores in product((False, True), repeat=n):
        candidato = {i + 1: valores[i] for i in range(n)}
        if verificar_sat(clausulas, candidato):
            return candidato
    return None


def verificar_tsp(matriz, limite, ruta):
    n = len(matriz)
    if len(ruta) != n + 1 or ruta[0] != 0 or ruta[-1] != 0:
        return False
    if set(ruta[:-1]) != set(range(n)) or len(set(ruta[:-1])) != n:
        return False
    return sum(matriz[ruta[i]][ruta[i + 1]] for i in range(n)) <= limite


def buscar_tsp(matriz, limite):
    for orden in permutations(range(1, len(matriz))):
        ruta = (0,) + orden + (0,)
        if verificar_tsp(matriz, limite, ruta):
            return ruta
    return None


def verificar_factor(n, b, d):
    return all(isinstance(x, int) for x in (n, b, d)) and n > 1 and 2 <= d <= b and n % d == 0


def buscar_factor(n, b):
    if not isinstance(n, int) or not isinstance(b, int) or n <= 1 or b < 2:
        raise ValueError("N o B inválido")
    return next((d for d in range(2, min(b, n) + 1) if n % d == 0), None)


def verificar_log_discreto(p, g, h, b, x):
    return all(isinstance(v, int) for v in (p, g, h, b, x)) and p > 1 and 0 <= x <= b and pow(g, x, p) == h % p


def buscar_log_discreto(p, g, h, b):
    if any(not isinstance(v, int) for v in (p, g, h, b)) or p <= 1 or b < 0:
        raise ValueError("parámetros inválidos")
    valor = 1
    for x in range(b + 1):
        if valor == h % p:
            return x
        valor = valor * g % p
    return None


def verificar_isomorfismo(a, b, perm):
    n = len(a)
    return len(b) == n and sorted(perm) == list(range(n)) and all(
        a[i][j] == b[perm[i]][perm[j]] for i in range(n) for j in range(n)
    )


def buscar_isomorfismo(a, b):
    return next((p for p in permutations(range(len(a))) if verificar_isomorfismo(a, b, p)), None)


def verificar_automorfismo(a, perm):
    return tuple(perm) != tuple(range(len(a))) and verificar_isomorfismo(a, a, perm)


def buscar_automorfismo(a):
    return next((p for p in permutations(range(len(a))) if verificar_automorfismo(a, p)), None)


def edmonds_karp(aristas, origen, destino):
    if origen == destino:
        raise ValueError("origen y destino iguales")
    residual = {}
    for u, v, capacidad in aristas:
        if not isinstance(capacidad, int) or capacidad < 0:
            raise ValueError("capacidad inválida")
        residual.setdefault(u, {})[v] = residual.setdefault(u, {}).get(v, 0) + capacidad
        residual.setdefault(v, {}).setdefault(u, 0)
    if origen not in residual or destino not in residual:
        raise ValueError("origen o destino ausente")
    flujo = 0
    while True:
        padre, cola = {origen: None}, deque([origen])
        while cola and destino not in padre:
            u = cola.popleft()
            for v, capacidad in residual[u].items():
                if capacidad > 0 and v not in padre:
                    padre[v] = u
                    cola.append(v)
        if destino not in padre:
            return flujo
        cuello, v = float("inf"), destino
        while v != origen:
            u = padre[v]
            cuello = min(cuello, residual[u][v])
            v = u
        v = destino
        while v != origen:
            u = padre[v]
            residual[u][v] -= cuello
            residual[v][u] += cuello
            v = u
        flujo += cuello
