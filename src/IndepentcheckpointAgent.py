from heapq import heappop, heappush

class IndependentCheckpointAgent:
    def __init__(self, start_position, checkpoints):
        """
        Inicializa el agente independiente con una posición inicial y una lista de checkpoints.
        :param start_position: Tupla (fila, columna) inicial del agente.
        :param checkpoints: Lista de checkpoints [(fila, columna), ...] que el agente debe seguir.
        """
        self.position = start_position
        self.checkpoints = checkpoints  # Lista de checkpoints (incluye la salida como último checkpoint)
        self.alive = True
        self.current_goal_index = 0  # Índice del checkpoint actual en la lista de checkpoints

    def move(self, environment):
        """
        Mueve al agente hacia el próximo checkpoint o salida.
        :param environment: Instancia del entorno.
        """
        if not self.alive or self.current_goal_index >= len(self.checkpoints):
            return  # El agente está evacuado o no hay más checkpoints

        # Obtener el checkpoint actual
        current_goal = self.checkpoints[self.current_goal_index]

        # Si el agente llegó al checkpoint actual
        if self.position == current_goal:
            print(f"Agente en {self.position} alcanzó el checkpoint {current_goal}.")
            self.current_goal_index += 1  # Pasar al siguiente checkpoint
            if self.current_goal_index >= len(self.checkpoints):
                print(f"Agente evacuado desde {self.position}.")
                self.alive = False  # El agente ha terminado su recorrido
                return
            current_goal = self.checkpoints[self.current_goal_index]  # Nuevo objetivo

        # Buscar el camino hacia el checkpoint actual usando A*
        path = self.a_star(environment, current_goal)

        # Si se encuentra un camino, moverse al siguiente paso
        if path:
            self.position = path[0]
            print(f"Agente movido a {self.position}. Próximo destino: {current_goal}.")
        else:
            print(f"No se pudo encontrar un camino hacia {current_goal}. Agente atrapado.")
            self.alive = True  # Agente queda atrapado si no puede continuar

    def a_star(self, environment, goal):
        """
        Implementación del algoritmo A* para encontrar el camino hacia el objetivo.
        :param environment: Instancia del entorno.
        :param goal: Tupla (fila, columna) del objetivo.
        :return: Lista de pasos [(fila, columna), ...] o None si no se encuentra un camino.
        """
        start = self.position
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heappop(open_set)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current, environment):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No se encontró un camino

    def get_neighbors(self, position, environment):
        """Obtiene las celdas vecinas válidas desde una posición dada."""
        neighbors = []
        y, x = position
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_y, new_x = y + dy, x + dx
            if environment.is_valid_position((new_y, new_x)):
                neighbors.append((new_y, new_x))
        return neighbors

    def reconstruct_path(self, came_from, current):
        """Reconstruye el camino desde el nodo inicial al nodo objetivo."""
        path = []
        while current in came_from:
            path.insert(0, current)
            current = came_from[current]
        return path

    def heuristic(self, a, b):
        """Calcula la distancia Manhattan entre dos puntos."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
