# Fundamentación formal de LOGISTPULSE

**Deber 2 · Teoría de la Computación · USFQ · 22 de noviembre de 2026**  
**Equipo:** Daniela Castellanos · Janneth Cabascango · Alejandro Guamán  
**Repositorio:** https://github.com/danycaste1304/TDC_Deber_02

Este informe modela tres procesos logísticos como autómatas, calcula una ruta de AMR, especifica FEFO y reposición, y fundamenta diez casos del simulador mediante algoritmos, verificadores y reducciones. El código y las pruebas acompañan el informe. Todos los grafos y números usados son los datos didácticos de la consigna o del simulador.

## 1. Modelos de estados

Un autómata por proceso es la quíntupla (Q, Σ, q₀, F, δ). Las tablas completas de Q, Σ, q₀, F, δ y las doce secuencias se encuentran en `automatas/secuencias.md`; los archivos `.jff` abren en JFLAP. Se interpretan como DFA parciales: una transición ausente lleva a un sumidero implícito de rechazo. Un estado de cierre rechazado o cancelado está en F porque la instancia terminó; no significa éxito comercial. La pregunta de aceptación es «¿la secuencia concluye legalmente un proceso?». Si se quisiera aceptar solo el éxito, bastaría cambiar F sin alterar δ.

**Pedido.** Q = {Borrador, Confirmado, Reservado, Preparación, Empacado, Despachado, Entregado, Cancelado}; Σ = {confirmar, reservar, preparar, empacar, despachar, entregar, cancelar}; q₀ = Borrador; F = {Entregado, Cancelado}. δ principal: Borrador --confirmar→ Confirmado --reservar→ Reservado --preparar→ Preparación --empacar→ Empacado --despachar→ Despachado --entregar→ Entregado. Cancelar se permite desde Borrador, Confirmado y Reservado. No se puede despachar antes de empacar.

**Reserva.** Q = {Solicitada, Validada, Reservada, Consumida, Liberada, Rechazada}; Σ = {validar, reservar, consumir, liberar, rechazar}; q₀ = Solicitada; F = {Consumida, Liberada, Rechazada}. δ principal: Solicitada --validar→ Validada --reservar→ Reservada --consumir→ Consumida. Desde Reservada se puede liberar; desde Solicitada o Validada se puede rechazar. Consumir sin reservar carece de transición.

**Compra.** Q = {Borrador, Aprobada, Enviada, Recibida, Cerrada, Rechazada, Cancelada}; Σ = {aprobar, enviar, recibir, cerrar, rechazar, cancelar}; q₀ = Borrador; F = {Cerrada, Rechazada, Cancelada}. δ principal: Borrador --aprobar→ Aprobada --enviar→ Enviada --recibir→ Recibida --cerrar→ Cerrada. Rechazar desde Borrador y cancelar desde Borrador o Aprobada son cierres alternos. Desde Rechazada no se puede enviar.

Los doce resultados se reproducen con `python3 verificar_automatas.py`. Las cadenas en JFLAP usan símbolos de un carácter; cada archivo `*_codigos.json` traduce eventos a símbolos. Las capturas de ejecución en JFLAP (*Input → Multiple Run*) se guardan en `automatas/capturas/`, según la guía de `automatas/secuencias.md`.

## 2. Grafo de planta y ruta del AMR

G = (V,E,w) es dirigido y ponderado. V transitable = {R, B, A, P, E, D}; la zona X está bloqueada y no tiene aristas transitables. E = {(R,B,2), (R,A,8), (B,A,2), (B,P,9), (A,P,3), (P,E,2), (E,D,2)}, con pesos en metros no negativos. Origen R; destino D. El SVG y JSON editables están en `grafo/`. Dijkstra entrega R→B→A→P→E→D con costo 2+2+3+2+2 = **11 m**. La ruta alternativa R→A→P→E→D cuesta 15 m; R→B→P→E→D cuesta 15 m.

```text
DIJKSTRA(G,s,t)
  validar vértices y pesos no negativos
  dist[s]=0; dist[otros]=∞; padre[s]=nulo; cola={(0,s)}
  mientras cola no vacía:
    (d,u)=extraer_mínimo(cola)
    si d≠dist[u]: continuar
    si u=t: reconstruir por padre y devolver (d,ruta)
    para cada (u,v,peso):
      si d+peso<dist[v]: dist[v]=d+peso; padre[v]=u; insertar(dist[v],v)
  devolver sin ruta
```

La cola pierde una entrada por iteración; cada relajación exitosa inserta una entrada nueva y hay un número finito de aristas procesadas. Por tanto termina. Con listas y montículo binario: O((|V|+|E|) log |V|) tiempo y O(|V|+|E|) espacio, incluyendo lista, padres y cola. La condición de pesos no negativos garantiza que al extraer la menor distancia se pueda fijar su costo. Para aristas sin peso, BFS encuentra el mínimo número de tramos en O(V+E) tiempo y O(V) espacio adicional.

## 3. Inventario

```text
FEFO(lotes, pedido, hoy)
  validar pedido≥0 y cantidades≥0
  candidatos = lotes con vencimiento≥hoy y disponible>0
  ordenar por (vencimiento ascendente, código ascendente)
  pendiente=pedido; plan=[]
  para cada lote en candidatos:
    toma=min(pendiente, disponible); añadir si toma>0; pendiente-=toma
    si pendiente=0: devolver plan
  devolver fallo por stock insuficiente, sin confirmar el plan parcial
```

La ordenación acaba porque hay L lotes; el recorrido reduce una lista finita y termina. Tiempo O(L log L), espacio O(L). La política es **reserva atómica**: si faltan unidades, no se confirma ninguna. Lotes vencidos, incluso por un día, quedan excluidos; un lote con fecha igual a hoy todavía es elegible. Si dos vencen igual, gana el código lexicográficamente menor. Una reserva real debe ejecutarse en transacción para impedir sobreasignación concurrente.

```text
REPOSICIÓN(productos)
  para cada SKU:
    posición=disponible+en_orden_abierta-reservado
    si posición≤mínimo: sugerencia=max(0,objetivo-posición)
    si no: sugerencia=0
    emitir (SKU,posición,sugerencia)
```

El contador de P productos avanza en cada iteración y termina. Tiempo O(P), espacio O(1) adicional al emitir uno a uno, o O(P) si se guarda toda la salida. La cantidad en órdenes abiertas entra una sola vez en `en_orden_abierta`, lo que evita duplicar una sugerencia por inventario ya pedido. Para evitar dos órdenes nuevas concurrentes, se recalcula y confirma dentro de una transacción por SKU. Ejemplo: 18+10−5 = 23; 23≤30; sugerencia 50−23 = **27**.

## 4. Tabla resumen de los diez correos

Todas las preguntas de decisión sobre entradas finitas válidas son decidibles y computables por un algoritmo efectivo que termina. La columna de espacio indica memoria adicional, salvo que se indique matriz de entrada. P ⊆ NP y «NP» en las cuatro filas intermedias significa **pertenencia demostrada**, sin conclusión de dureza.

| ID | Pregunta de decisión | Evidencia | Algoritmo y estrategia | Tiempo / espacio |
|---|---|---|---|---|
| p1 | ¿Hay camino Durán→Norte? | P | BFS exacto | O(V+E) / O(V) |
| p2 | ¿Existe ruta Quito→Guayaquil de costo ≤K? | P | Dijkstra exacto | O((V+E)log V) / O(V+E) |
| p3 | ¿Flujo máximo ≥K? | P | Edmonds–Karp exacto | O(VE²) / O(V+E) |
| n1 | ¿Dos grafos son isomorfos? | NP, certificado biyección | Permutaciones exactas | O(n!n²) / O(n²) |
| n2 | ¿N tiene divisor entre 2 y B? | NP, certificado d | División exhaustiva exacta | O(B·M(L)) / O(L) |
| n3 | ¿Existe x≤B con gˣ≡h mod p? | NP, certificado x | Enumeración exacta | O(B·M(L)) / O(L) |
| n4 | ¿G tiene automorfismo no identidad? | NP, certificado permutación | Permutaciones exactas | O(n!n²) / O(n²) |
| c1 | ¿3-CNF satisfacible? | NP-completo | Enumeración exacta | O(2ⁿm) / O(n+m) |
| c2 | ¿Ciclo TSP con costo ≤K? | NP-completo | Permutaciones exactas | O(n!n) / O(n²) |
| c3 | ¿Vertex Cover de tamaño ≤k? | NP-completo | Subconjuntos exactos | O(2^V(V+E)) / O(V+E) |

Aquí L es longitud binaria de los enteros pertinentes y M(L) el costo de multiplicación o división de L bits; con aritmética escolar, M(L)=O(L²). Las cotas O(B·M(L)) son numéricas y pueden ser exponenciales en log B. Para n3 el código usa producto modular incremental, no una exponenciación completa en cada intento. Para p2 el tiempo se refiere a un montículo binario con inserciones repetidas; con la cola de Python la forma rigurosa es O((V+E)log(V+E)), equivalente a O((V+E)log V) para grafos simples. Los algoritmos de búsqueda de la tabla son exactos; no se necesita aproximación en las pequeñas instancias del expediente.

## 5. Fichas de los correos

### p1 Acceso a Zona Norte

Entrada: grafo dirigido de rutas activas, origen Durán y destino Norte. Salida: Sí/No; se reconstruye un camino como evidencia. Restricción: solo aristas activas. BFS marca cada vértice una vez y agota la cola, por lo que decide y computa exactamente la respuesta en O(V+E) tiempo y O(V) espacio. En el expediente, Durán→Quito→Norte da **Sí**; Sur→Norte da **No**. Código y pruebas: `bfs`, `test_rutas`. La infografía de BFS aportada por el usuario concuerda con el camino de dos tramos del simulador.

### p2 Ruta mínima entre centros

Entrada: grafo dirigido con tiempos no negativos, Quito y Guayaquil; decisión asociada: ¿costo mínimo ≤K? La solicitud también pide el valor óptimo y predecesores. Dijkstra resuelve exactamente en O((V+E)log V) tiempo y O(V+E) espacio. Para los datos Quito→Latacunga=2, Quito→Ambato=5, Latacunga→Guayaquil=6 y Ambato→Guayaquil=3, el mínimo es **8** por cualquiera de los dos caminos. La prueba `dijkstra` incluye ruta ponderada de planta, origen=destino y peso negativo inválido. Un peso negativo invalida la precondición de Dijkstra.

### p3 Máximo de camiones

Entrada: red dirigida con capacidades enteras no negativas, fuente Planta y sumidero Clientes. Decisión: ¿el flujo máximo es al menos K? Edmonds–Karp usa BFS sobre la red residual, conserva aristas inversas y termina en O(VE²) tiempo, O(V+E) espacio. Es exacto y computable. En el expediente, la capacidad hacia Clientes es 4+6=10 y existe un flujo de 10: 4 por Quito→Clientes y 6 por Guayaquil→Clientes, con 1 de esos 6 desde Quito→Guayaquil. Por cota superior y construcción, el máximo es **10**. Código: `edmonds_karp`; prueba en `test_certificados_y_busquedas`.

### n1 Isomorfismo de dos redes

Entrada: dos grafos de n vértices; decisión: ¿existe una biyección que preserve adyacencia y no adyacencia? Certificado: permutación de n índices; `verificar_isomorfismo` comprueba biyección y n² pares en O(n²) tiempo y O(n) espacio adicional sobre matrices. Esto prueba pertenencia a NP. La búsqueda exacta enumera n! permutaciones: O(n!n²) tiempo, O(n²) espacio de matrices. Es decidible por agotamiento. Los dos grafos del expediente son isomorfos; la permutación (1,0,2) es válida. No se infiere NP-completitud.

### n2 Factor acotado en binario

Entrada: N>1 y B≥2 codificados en binario; decisión: ¿existe d con 2≤d≤B y d|N? Certificado d, de O(log B) bits; `verificar_factor` comprueba rango y resto en O(M(L)) tiempo y O(L) espacio, demostrando NP. La búsqueda exacta prueba candidatos hasta min(B,N), O(B·M(L)) tiempo en la cota simple y O(L) espacio; termina. Con N=91 y B=10, devuelve **7** y verifica verdadero. La infografía adjunta distingue correctamente buscar de verificar. No se afirma que esta búsqueda sea polinómica en el tamaño binario ni que el problema sea NP-completo.

### n3 Logaritmo discreto acotado

Entrada: p primo, g, h, B en binario; decisión: ¿existe 0≤x≤B con gˣ≡h (mod p)? Certificado x; exponenciación modular por cuadrados verifica en O(log B·M(L)) tiempo y O(L) espacio, por lo que está en NP. La búsqueda exacta incremental multiplica una vez por candidato, O(B·M(L)) tiempo y O(L) espacio; siempre acaba. Con (p,g,h,B)=(23,5,8,10), x=**6**. No se deriva NP-completitud ni separación de P de este certificado.

### n4 Automorfismo no trivial

Entrada: grafo con n vértices; decisión: ¿existe permutación no identidad que preserve todas las adyacencias? Certificado: permutación; `verificar_automorfismo` comprueba no identidad, biyección y n² pares en O(n²) tiempo y O(n) espacio adicional. Enumerar todas las permutaciones es exacto, termina y cuesta O(n!n²) tiempo, O(n²) espacio de matriz. El triángulo del simulador admite, por ejemplo, intercambiar vértices 0 y 1. Se prueba NP, no NP-completitud.

### c1 Restricciones de asignación 3-CNF

Entrada: fórmula de m cláusulas de a lo sumo tres literales sobre n variables; decisión: ¿es satisfacible? Certificado: n bits. `verificar_sat` evalúa cada cláusula en O(m) tiempo y O(n+m) espacio incluyendo entrada. Para dureza, cualquier instancia de **3-SAT** se copia literalmente al formato de restricciones 3-CNF del correo: reducción identidad polinómica, que preserva Sí/No. Como 3-SAT es NP-completo y el caso está en NP, la formulación general es NP-completa. `buscar_sat` enumera 2ⁿ asignaciones, O(2ⁿm) tiempo y O(n+m) espacio, exacto y decidible. El ejemplo (x1∨¬x2)∧(x2∨x3) acepta x1=verdadero, x2=verdadero, x3=falso.

### c2 Recorrido de todos los centros con regreso

Entrada: matriz completa de distancias enteras no negativas y límite K; decisión: ¿existe ciclo que inicia y termina en planta, visita cada centro exactamente una vez y cuesta ≤K? Certificado: permutación de centros. `verificar_tsp` comprueba unicidad y **n tramos, incluido el regreso**, O(n) tiempo y O(n²) espacio de matriz. Para dureza, desde **Hamiltonian Cycle** en un grafo no dirigido de n vértices se construye la matriz con costo 1 si existe arista y 2 si no; K=n. Hay ciclo de costo ≤n si y solo si todas las n aristas del recorrido pertenecen al grafo. La transformación ocupa O(n²) tiempo. Así, la decisión TSP general es NP-completa. La búsqueda exacta enumera (n−1)! recorridos, O(n!n) tiempo y O(n²) espacio. En el ejemplo, 0→1→2→0 cuesta 4+3+8=**15**, que cumple 20. La variante de optimización pediría el mínimo, no solo un Sí/No.

### c3 Cobertura de corredores

Entrada: grafo no dirigido G=(V,E) y entero k; decisión: ¿hay ≤k zonas tales que cada **arista** tenga al menos un extremo elegido? Certificado: subconjunto C; `verificar_vertex_cover` comprueba |C|≤k y cada arista en O(V+E) tiempo, O(V) espacio adicional. El texto operativo define exactamente **Vertex Cover**; la frase del resumen del simulador sobre cubrir una zona propia o vecina describiría otro problema y no se usa. Para dureza, una instancia de Vertex Cover se copia como mapa de corredores y presupuesto k: reducción identidad polinómica. En NP y NP-hard, esta versión es NP-completa. `buscar_vertex_cover` enumera subconjuntos, O(2^V(V+E)) tiempo y O(V+E) espacio, exacto y terminante. En A–B–C, k=1, el certificado {B} cubre ambas aristas.

## 6. Nota de una página sobre decidibilidad y parada

**Decidibilidad** pregunta por la existencia de un algoritmo que, para toda entrada válida de una pregunta Sí/No, termine y responda correctamente. **Computabilidad** se refiere a la función o relación efectiva que se calcula; por ejemplo, devolver una ruta concreta, un número de flujo o una asignación testigo, además de decidir si existe. **Complejidad** mide tiempo y memoria respecto de la longitud de la entrada. Estas nociones no son sinónimas: un procedimiento puede ser computable y terminar siempre, pero requerir un número impracticable de pasos.

Suponemos entradas finitas codificadas en bits, grafos explícitos y una máquina de Turing determinista como modelo. Una instancia de TSP con n centros tiene (n−1)! órdenes posibles si se fija el origen. Enumerarlos, calcular cada costo y comparar con K siempre termina para n finito: la versión de decisión es decidible. Con n grande, el factorial puede impedir usar ese método en el plazo operativo. Un algoritmo exacto más sofisticado, una aproximación para el TSP métrico o una heurística pueden mejorar la práctica, pero sus garantías son distintas y no alteran la decidibilidad.

En cambio, la pregunta general sobre si un programa arbitrario se detiene en una entrada arbitraria es el **problema de la parada**: no existe un decisor que responda correctamente y termine para todos los programas y entradas. La variante «¿este programa termina para toda entrada?» también es indecidible. Allí no basta decir que la búsqueda es enorme; falta un algoritmo general de decisión. Para los diez problemas logísticos aquí formalizados, los conjuntos de candidatos son finitos y efectivamente enumerables, de modo que la preocupación es el costo, no la existencia de un decisor. El certificado de NP aporta verificación polinómica de un Sí, pero por sí solo no garantiza búsqueda polinómica ni prueba NP-completitud.

## 7. Implementación, pruebas y alcance

`logistpulse.py` separa funciones puras de `demo.py`, que presenta resultados. `tests/test_logistpulse.py` incluye casos normales, límite e inválidos: ruta encontrada y ausente, origen=destino, peso negativo, FEFO con empate, demanda cero e insuficiente, reposición con y sin pedido, y certificados válidos y falsos. El comando `python3 -m unittest discover -s tests -v` terminó con tres grupos de pruebas correctos; `python3 verificar_automatas.py` produjo seis aceptaciones y seis rechazos esperados. El demo imprimió AMR 11 m, FEFO A:2/B:2, posición 23/sugerencia 27, Vertex Cover {B} y flujo 10.

El código didáctico de los casos NP-completos usa búsqueda exacta y se limita a instancias pequeñas. Los verificadores presuponen entradas estructuralmente válidas conforme a las restricciones declaradas; las funciones operativas centrales sí rechazan origen inexistente, pesos negativos, cantidades negativas y parámetros de reposición incoherentes. El trabajo se repartió en partes iguales: Daniela Castellanos (autómatas y grafo, Sprint 1), Janneth Cabascango (algoritmos, inventario y pruebas, Sprint 2) y Alejandro Guamán (fichas de complejidad, decidibilidad e informe, Sprint 3); cada integrante revisó el trabajo de otro. Repositorio: https://github.com/danycaste1304/TDC_Deber_02.
