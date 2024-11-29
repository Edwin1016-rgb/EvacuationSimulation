# src/visualization.py

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from src.IndepentcheckpointAgent import IndependentCheckpointAgent

class Visualization:
    """def __init__(self, environment, agents):
        self.environment = environment
        self.agents = agents
        self.fig, self.ax = plt.subplots()

        # Definir un mapa de colores para las celdas
        self.cmap = mcolors.ListedColormap(["white", "black", "red", "blue", "green", "purple"])  # Agregar un color para CheckpointAgent
        self.bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]  # 6 categorías, incluyendo CheckpointAgent
        self.norm = mcolors.BoundaryNorm(self.bounds, self.cmap.N)
    """ 
    def __init__(self, environment, agents):
        self.environment = environment
        self.agents = agents
        self.fig, self.ax = plt.subplots()

        # Agregar color para los `IndependentCheckpointAgent`
        self.cmap = mcolors.ListedColormap(["white", "black", "red", "blue", "green", "purple" ,"yellow"])  # Agregar un color para CheckpointAgent
        self.bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5 , 6.5]  # Agregar un valor para los checkpoints
        self.norm = mcolors.BoundaryNorm(self.bounds, self.cmap.N)

    def update_plot(self):
        grid = self.environment.grid.copy()

        for agent in self.agents:
            if agent.alive:
                y, x = agent.position
                if isinstance(agent, IndependentCheckpointAgent):
                    grid[y, x] = 5  # Color específico para CheckpointAgent
                else:
                    grid[y, x] = 3  # Color para otros agentes
                    
        # Marcar los checkpoints en la cuadrícula
        if hasattr(self.environment, "checkpoints"):
            for checkpoint in self.environment.checkpoints:
                y, x = checkpoint
                grid[y, x] = 6  # Usa un nuevo valor para los checkpoints

        self.ax.clear()
        self.ax.imshow(grid, cmap=self.cmap, norm=self.norm)
        
        self.ax.set_xticks(np.arange(-0.5, self.environment.width, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, self.environment.height, 1), minor=True)
        self.ax.grid(which="minor", color="gray", linestyle="--", linewidth=0.5)
        self.ax.tick_params(which="minor", size=0) 
        
            
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title("Emergency Evacuation Simulation")
        plt.pause(0.1)


    def show_final(self):
        """Muestra el estado final de la simulación."""
        plt.show()
