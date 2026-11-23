import unittest
from datetime import date
from logistpulse import *


class TestLogistpulse(unittest.TestCase):
    def test_rutas(self):
        red = {'Durán':['Quito','Guayaquil'], 'Quito':['Norte'], 'Guayaquil':['Sur'], 'Norte':[], 'Sur':[]}
        self.assertEqual(bfs(red, 'Durán', 'Norte'), ['Durán','Quito','Norte'])
        self.assertIsNone(bfs(red, 'Sur', 'Norte'))
        with self.assertRaises(ValueError): bfs(red, 'X', 'Norte')
        grafo = {'R':[('B',2),('A',8)], 'B':[('A',2),('P',9)], 'A':[('P',3)], 'P':[('E',2)], 'E':[('D',2)], 'D':[]}
        self.assertEqual(dijkstra(grafo, 'R', 'D'), (11, ['R','B','A','P','E','D']))
        self.assertEqual(dijkstra(grafo, 'R', 'R'), (0, ['R']))
        with self.assertRaises(ValueError): dijkstra({'A':[('B',-1)],'B':[]}, 'A', 'B')

    def test_inventario(self):
        lotes = [('B',date(2026,12,1),3),('A',date(2026,12,1),2),('V',date(2026,11,21),9)]
        self.assertEqual(fefo(lotes,4,date(2026,11,22)), [('A',2),('B',2)])
        self.assertEqual(fefo(lotes,0,date(2026,11,22)), [])
        self.assertIsNone(fefo(lotes,6,date(2026,11,22)))
        with self.assertRaises(ValueError): fefo(lotes,-1,date(2026,11,22))
        self.assertEqual(reposicion(18,10,5,30,50),(23,27))
        self.assertEqual(reposicion(40,10,5,30,50),(45,0))
        with self.assertRaises(ValueError): reposicion(1,0,0,10,5)

    def test_certificados_y_busquedas(self):
        vertices, aristas = ['A','B','C'], [('A','B'),('B','C')]
        self.assertTrue(verificar_vertex_cover(vertices,aristas,1,['B']))
        self.assertFalse(verificar_vertex_cover(vertices,aristas,1,['A']))
        self.assertEqual(buscar_vertex_cover(vertices,aristas,1),('B',))
        self.assertIsNone(buscar_vertex_cover(vertices,aristas,0))
        self.assertTrue(verificar_factor(91,10,7))
        self.assertEqual(buscar_factor(91,10),7)
        self.assertEqual(buscar_log_discreto(23,5,8,10),6)
        self.assertTrue(verificar_log_discreto(23,5,8,10,6))
        a=[[0,1,0],[1,0,1],[0,1,0]]
        b=[[0,1,1],[1,0,0],[1,0,0]]
        self.assertTrue(verificar_isomorfismo(a,b,(1,0,2)))
        self.assertIsNotNone(buscar_automorfismo(a))
        clausulas=[[1,-2],[2,3]]
        self.assertTrue(verificar_sat(clausulas,{1:True,2:True,3:False}))
        self.assertIsNotNone(buscar_sat(clausulas,3))
        dist=[[0,4,8],[4,0,3],[8,3,0]]
        self.assertTrue(verificar_tsp(dist,20,(0,1,2,0)))
        self.assertFalse(verificar_tsp(dist,14,(0,1,2,0)))
        self.assertEqual(buscar_tsp(dist,20),(0,1,2,0))
        self.assertEqual(edmonds_karp([('Planta','Quito',7),('Planta','Guayaquil',5),('Quito','Clientes',4),('Guayaquil','Clientes',6),('Quito','Guayaquil',2)],'Planta','Clientes'),10)


if __name__ == '__main__': unittest.main()
