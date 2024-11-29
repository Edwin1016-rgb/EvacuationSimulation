import random
import numpy as np
from data.pseudonumbers import ri

class Environment:
    def __init__(self, width, height):
        """
        Inicializa el entorno con un plano vacío.
        :param width: Ancho del plano (número de columnas).
        :param height: Alto del plano (número de filas).
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)  # 0: espacio vacío, 1: pared, 2: fuego, 3: salida, 4: agente

    def load_layout(self, layout):
        """
        Carga un plano definido (matriz).
        :param layout: Matriz que representa el plano del entorno.
        """
        self.grid = np.array(layout)
        
    def load_checkpoints(self, checkpoints):
        """Carga los puntos de control"""
        self.checkpoints = checkpoints
    

    def update_fire(self, spread_probability):
        """
        Actualiza la propagación del fuego en el entorno.
        :param spread_probability: Probabilidad base de que el fuego se propague a celdas adyacentes.
        """
        new_grid = self.grid.copy()
        fire_spread = []

        # Iterar sobre cada celda del grid
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                if self.grid[y, x] == 2:  # Celda en llamas
                    # Revisar celdas vecinas
                    neighbors = [
                        (y + dy, x + dx)
                        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if 0 <= y + dy < self.grid.shape[0] and 0 <= x + dx < self.grid.shape[1]
                    ]
                    for ny, nx in neighbors:
                        if self.grid[ny, nx] == 0:  # Espacio vacío
                            # Propagación basada en probabilidad
                            if random.choice(ri) < spread_probability:
                                fire_spread.append((ny, nx))

        # Aplicar propagación del fuego
        for fy, fx in fire_spread:
            new_grid[fy, fx] = 2

        self.grid = new_grid
    
    def is_valid_position(self, position):
        """
        Verifica si una posición en el entorno es válida (no es obstáculo ni fuego).
        """
        y, x = position
        return (
            0 <= y < self.grid.shape[0] and
            0 <= x < self.grid.shape[1] and
            self.grid[y, x] in [0, 4]  # 0: espacio vacío, 4: salida
        )


    def display(self, agents=None):
        """
        Muestra el estado actual del entorno en la consola.
        """
        symbols = {
            0: " ",    # Espacio vacío
            1: "*",    # Obstáculo
            2: "fuego",   # Fuego
            3: "salida",   # Salida
            4: "A",    # Agente
            5: "C"     # Punto de control
        }

        # Crear una copia de la cuadrícula para modificarla con los agentes
        display_grid = self.grid.copy()
        # Colocar los checkpoints en la visualización
        if hasattr(self, "checkpoints"):
            for checkpoint in self.checkpoints:
                cy, cx = checkpoint
                display_grid[cy, cx] = 5  # Marca los checkpoints como `5` en el grid

        # Colocar los agentes en la visualización
        if agents:
            for agent in agents:
                display_grid[agent.position[0], agent.position[1]] = 4  # Marca al agente en el grid

        # Mostrar el grid en la consola
        for row in display_grid:
            print("".join(symbols[cell] for cell in row))
        print("\n" + "-" * self.width)
