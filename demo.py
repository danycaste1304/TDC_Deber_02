from datetime import date
from logistpulse import *

red = {'Durán':['Quito','Guayaquil'],'Quito':['Norte'],'Guayaquil':['Sur'],'Norte':[],'Sur':[]}
planta = {'R':[('B',2),('A',8)],'B':[('A',2),('P',9)],'A':[('P',3)],'P':[('E',2)],'E':[('D',2)],'D':[]}
print('BFS:', bfs(red,'Durán','Norte'))
print('AMR:', dijkstra(planta,'R','D'))
print('FEFO:', fefo([('B',date(2026,12,1),3),('A',date(2026,12,1),2)],4,date(2026,11,22)))
print('Reposición:', reposicion(18,10,5,30,50))
print('Vertex Cover:', buscar_vertex_cover(['A','B','C'], [('A','B'),('B','C')], 1))
print('Flujo máximo:', edmonds_karp([('Planta','Quito',7),('Planta','Guayaquil',5),('Quito','Clientes',4),('Guayaquil','Clientes',6),('Quito','Guayaquil',2)],'Planta','Clientes'))
