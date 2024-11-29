import random
import heapq

class Agent:
    def __init__(self, position, goal):
        self.position = position  # Posición actual del agente (coordenadas)
        self.goal = goal  # Meta del agente (donde debe llegar)
        self.alive = True  # Estado del agente: vivo o muerto

    def move(self, environment):
        """Mueve al agente hacia su meta utilizando un algoritmo de búsqueda (como A*)"""
        if not self.alive:
            return

        # Movimiento básico: mover al agente hacia su meta
        path = self.a_star(environment, self.goal)
        if path:
            self.position = path[0]

        # Si el agente ha llegado a la meta, se marca como evacuado
        if self.position == self.goal:
            self.alive = False

    def a_star(self, environment, goal):
        """ Implementa una búsqueda A* básica para encontrar la ruta hacia la meta. """
        start = self.position
        goal = self.goal
        open_list = []
        closed_list = set()
        came_from = {}

        # Función heurística (distancia Manhattan)
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Inicializar el open list
        heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start))  # (f_score, g_score, position)
        g_scores = {start: 0}  # El costo desde el inicio hasta el nodo

        while open_list:
            _, g, current = heapq.heappop(open_list)
            
            if current == goal:
                # Reconstruir el camino
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            closed_list.add(current)
            neighbors = [
                (current[0] + dy, current[1] + dx)
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= current[0] + dy < environment.height and 0 <= current[1] + dx < environment.width
            ]

            for neighbor in neighbors:
                if neighbor in closed_list or environment.grid[neighbor[0], neighbor[1]] == 1:  # Obstáculo
                    continue

                # Asegurarse de que el agente no pase cerca del fuego
                if environment.grid[neighbor[0], neighbor[1]] == 2:  # Fuego
                    continue

                tentative_g_score = g + 1
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    came_from[neighbor] = current
                    g_scores[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score, tentative_g_score, neighbor))

        return None  # No se encontró un camino

    def __str__(self):
        return f"Agent at {self.position} aiming for {self.goal}"
