from queue import PriorityQueue


class Mapa:
    def __init__(self):
        self.tamanho = 10
        self.mapa = [[0] * self.tamanho for i in range(self.tamanho)]        
        self.obstaculos = self.agregar_obstaculos ()
        self.inicio = None
        self.final = None
        
        
    def agregar_obstaculos(self):
        obstaculos = [
        (1, 1), (2, 1), (2, 2), (3, 3), (4, 4), (4, 5), (5, 5), (6, 6), (8, 8), (9, 9),         
        (3, 7), (3, 8), (3, 9), (7, 3), (8, 3), (9, 3), (0, 5), (1, 8), (2, 6), (4, 1), (5, 9)        
            ]
        for obstaculo in obstaculos:
            self.mapa[obstaculo[0]][obstaculo[1]] = 1
        return obstaculos
    
    def agregar_obstaculos_usuario (self):
        obstaculos_usuario = []
        for i in range (2):
            while True:
                x = int(input(f'Ingrese la coordenada x del obstáculo {i + 1}: '))
                y = int(input(f'Ingrese la coordenada y del obstáculo {i + 1}: '))
                if self.coordenada_valida((x, y)):  # Verificar que la coordenada sea válida
                    self.mapa[x][y] = 1
                    obstaculos_usuario.append((x, y))
                    break
                else:
                    print("Coordenada no válida o ya ocupada, intente de nuevo.")
        return obstaculos_usuario  # Devolver la lista de obstáculos del usuario
    
    def coordenadas_inicio_final(self, coordenada_inicio, coordenada_final):
        if self.coordenada_valida(coordenada_inicio) and self.coordenada_valida(coordenada_final):
            self.inicio = coordenada_inicio
            self.final = coordenada_final
        else:
            raise ValueError("Las coordenadas de inicio o final no son válidas.")
        
    
    """ -----------------Validar coordenadas-----------------"""
    
    def coordenada_valida(self, coordenada):
        x, y = coordenada
        xy_valida = 0 <= x < self.tamanho and 0 <= y < self.tamanho and self.mapa[x][y] != 1
        return xy_valida
             
        
        
        
    """ -------------------algoritmo A*------------------------ """
    # El algoritmo A* selecciona la celda con el coste total más bajo como el siguiente nodo a explorar.
    
    # - crear dos listas una abierta y otra cerrada
    # - Añadir el nodo inicial a la lista abierta
    
    def a_star (self, inicio, final, mapa):
        
        # la cola de prioridad nos asegurará que siempre seleccionaremos 
        # la celda con el costo total más bajo como la siguiente a explorar
        lista_abierta = PriorityQueue() 
        lista_abierta.put ((0, inicio)) #añadimos el nodo inicial a la cola con un costo de cero
        
        lista_cerrada = set() #conjunto para nodos evaluados
        nodo_padre = {}
        costo_movimiento  = {inicio : 0} #costo g ---- costo de moverse desde el inicio hasta cada nodo
        
        costo_total = {}
        costo_total [inicio] = self.heuristica(inicio, final) #costo f
        
        
        
    # - mientras que la lista abierta no este vacia... o sea que haya elementos dentro :)    
        while not lista_abierta.empty():
            costo, nodo_actual = lista_abierta.get ()
            
            
            if nodo_actual == final: # si el nodo actual es la meta, termina el ciclo
                return self.reconstruir_camino (nodo_padre, nodo_actual)
            
            lista_cerrada.add(nodo_actual)
            
            
            #si no: evaluar nodo del vecino actual            
            for vecino in self.obtener_vecinos (nodo_actual, mapa):
                if vecino in lista_cerrada:
                    continue
                
                #calcular el costo g tentativo para llegar a este vecino a traves del nodo actual
                costo_mov_tentativo = costo_movimiento [nodo_actual] + 1
                
                if vecino not in costo_movimiento or costo_mov_tentativo < costo_movimiento[vecino]:
                    
                    #actualizar el nodo padre para este vecino
                    nodo_padre [vecino] = nodo_actual
                    
                    #actualizar el costo g para este vecino
                    costo_movimiento[vecino] = costo_mov_tentativo
                    
                    #calcular el costo total f estimado para este vecino
                    costo_total [vecino] = costo_movimiento[vecino] + self.heuristica(vecino, final)
                    
                    #agregar el vecino a la lista abierta con su costo f
                    lista_abierta.put((costo_total[vecino], vecino))
                
        return []
                
                
    """ -------------------distancia manhatan------------------- """    
    def heuristica (self, inicio, final):
        return abs (inicio [0] - final [0]) + (inicio [1] - final [1])
    
    
    
    
    """ -------------------obtener vecinos validos de un nodo------------------- """
    
    def obtener_vecinos (self, nodo, mapa):
        vecinos = []
        
        #evaluar posibles movimientos
        for (dir_x, dir_y) in [(0 , 1), (1 , 0), (0 , -1), (-1 , 0)]:
            x, y = nodo [0] + dir_x, nodo [1]+ dir_y
            
            if 0<=x and x <self.tamanho and 0<=y and y < self.tamanho and mapa[x][y] != 1:
                vecinos.append ((x , y))
        return vecinos
    
    
    
    """ -------------reconstruir el camino desde la meta hacia el inicio------------- """
    
    def reconstruir_camino (self, nodo_padre, nodo_actual):
        camino = []
        while nodo_actual in nodo_padre:
            camino.append(nodo_actual)
            nodo_actual = nodo_padre[nodo_actual]
        camino.reverse()
        return camino
    
    """ -------------imprimir mapa sin resolver------------- """

    def imprimir_mapa_sin_resolver (self):
        
        tablero = self.mapa
        for i in range(self.tamanho):
            
            for j in range(self.tamanho):
                if (i, j) == self.inicio:
                    print('📍', end='')
                elif (i, j) == self.final:
                    print('❗️', end='')
                
                elif tablero[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('.', end=' ')
            print()
            

    


    
    """ -------------imprimir mapa resuelto------------- """

    def imprimir_mapa (self, camino):
        tablero = self.mapa
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if (i, j) == self.inicio:
                    print('📍', end='')
                elif (i, j) == self.final:
                    print('❗️', end='')
                elif (i, j) in camino:
                    print('*', end=' ')
                elif tablero[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('.', end=' ')
            print()
            
mapa = Mapa()

while True:
    try:
        
            # Solicitar coordenadas del usuario
            inicio_x = int(input("Ingrese la coordenada x del punto inicial: "))
            inicio_y = int(input("Ingrese la coordenada y del punto inicial: "))
            final_x = int(input("Ingrese la coordenada x del punto final: "))
            final_y = int(input("Ingrese la coordenada y del punto final: "))
            print ()

            # Configurar el punto inicial y final en el mapa
            mapa.coordenadas_inicio_final((inicio_x, inicio_y), (final_x, final_y))
            print ('Bienvenido a Mapa, intentaremos encontrar la mejor ruta')
            print(f'El punto de partida es {inicio_x},{inicio_y}')
            print(f'El punto de llegada es {final_x},{final_y}')
            
            break

    except ValueError as e:
        print(e)
        
        


camino = mapa.a_star (mapa.inicio, mapa.final, mapa.mapa)
mapa.imprimir_mapa_sin_resolver()
print ()
print ('Puedes poner dos obstaculos indicando sus respectivas coordenadas, los puntos son casillas validas')
mapa.agregar_obstaculos_usuario()  # Llamar al método para agregar obstáculos del usuario
print()

camino = mapa.a_star (mapa.inicio, mapa.final, mapa.mapa) #volver a calcular mapa luego de agregar los obstaculos
mapa.imprimir_mapa(camino)