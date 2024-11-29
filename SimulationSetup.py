import random
import numpy as np
from src.environment import Environment
from src.agent import Agent
from src.IndepentcheckpointAgent import IndependentCheckpointAgent
from src.simulation import Simulation
from data.fire_probabilities import fire_probabilities
from data.pseudonumbers import ri


class SimulationSetup:
    def __init__(self, grid_size=(20, 20)):
        self.grid_size = grid_size
        self.grid = np.zeros(grid_size, dtype=int)
    
    def setup_environment(self):
        """Configura el entorno con obstáculos, fuego y salidas."""
        obstacles = [
            # Contorno de la casa (pared externa)
            *( [(i, 0) for i in range(20)] + [(i, 19) for i in range(20)] ),  # Pared izquierda y derecha
            *( [(0, j) for j in range(20)] + [(19, j) for j in range(20)] ),  # Pared superior e inferior

            # Paredes internas horizontales
            *( [(3, j) for j in range(1, 5)]),
            *( [(3, j) for j in range(12, 15)]),
            *( [(3, j) for j in range(17, 19)]),
            
            *( [(6, j) for j in range(1, 4)]),
            *( [(6, j) for j in range(12, 19)]),
            
            *( [(11, j) for j in range(1, 8)]),
            *( [(11, j) for j in range(16, 19)]),
            
            *( [(14, j) for j in range(1, 8)]),
            *( [(14, j) for j in range(12, 19)]),
            
            *( [(17, j) for j in range(12, 14)]),
            *( [(17, j) for j in range(15, 17)]),
            # Paredes internas verticales
            *( [(i, 4) for i in range(1, 2)]),    
            *( [(i, 4) for i in range(5, 7)]),  
            *( [(i, 4) for i in range(8, 12)]),  
            *( [(i, 4) for i in range(15, 17)]),
            *( [(i, 4) for i in range(18, 19)]),  
            
            *( [(i, 7) for i in range(12, 13)]),    
            *( [(i, 7) for i in range(16, 19)]),  
            
            *( [(i, 8) for i in range(1, 4)]),    
            *( [(i, 8) for i in range(6, 12)]),  
            
            *( [(i, 12) for i in range(1, 2)]),  
            *( [(i, 12) for i in range(5, 7)]),  
            *( [(i, 12) for i in range(8, 13)]), 
            *( [(i, 12) for i in range(15, 18)]), 
            
            *( [(i, 15) for i in range(3, 6)]), 
            *( [(i, 15) for i in range(15, 18)]), 
            
            *( [(i, 16) for i in range(6, 10)]), 
            *( [(i, 16) for i in range(12, 13)]), 
        ]
        
        for pos in obstacles:
            self.grid[pos] = 1  # '1' representa un obstáculo

        # Colocar fuego inicial
        def get_fire_position():
            fx = np.random.randint(1, 18)
            fy = np.random.randint(1, 18)
            
            if random.choice(fire_probabilities) >= 0.8:
                return (fx, fy) 
            return get_fire_position()
        
                
        fx1, fy1 = get_fire_position()
        fx2, fy2 = get_fire_position()
        
        initial_fire_positions = [(fx1, fy1), (fx2, fy2)]
        for pos in initial_fire_positions:
            self.grid[pos] = 2  # '2' representa fuego

        # Salida
        exits = [(19, 9)]
        for exit_pos in exits:
            self.grid[exit_pos] = 4  # '4' representa una salida

        # Crear el entorno
        height, width = self.grid_size
        environment = Environment(height, width)
        environment.load_layout(self.grid)
    
        return environment

    def setup_agents(self):
        """Configura los agentes asegurándose de que sus posiciones sean válidas y no se solapen."""
        
        def get_random_position():
            """Genera una posición aleatoria basada en probabilidad (con ri)."""
            fx = np.random.randint(1, 18)  # Coordenada X
            fy = np.random.randint(1, 18)  # Coordenada Y
            
            # Condición de probabilidad
            if random.choice(ri) >= 0.8:
                return fx, fy  # Si la probabilidad es mayor a 0.8, devolver la posición
            return get_random_position()  # Si no, vuelve a intentar generando otra posición
            
        def get_valid_position():
            """Obtiene una posición válida para un agente (no sobre obstáculos ni fuego ni otros agentes)."""
            while True:
                fx, fy = get_random_position()  # Generar una posición aleatoria
                if self.grid[fx, fy] == 0:  # 0 es una celda vacía
                    return fx, fy
        
        # Crear los agentes
        agents = []
        for _ in range(9):  # Crear 9 agentes
            x, y = get_valid_position()
            agents.append(Agent((x, y), (19, 9)))  # Posición aleatoria para cada agente

        # Agregar un agente independiente con checkpoints
        checkpoint_agents = [
            
            #zona A (Y X)
            IndependentCheckpointAgent((2, 2), [(4, 10),(11, 10),(19, 9)]),
            IndependentCheckpointAgent((5, 2), [(4, 10),(11, 10),(19, 9)]),
            IndependentCheckpointAgent((10, 2), [(4, 10),(11, 10),(19, 9)]),
            IndependentCheckpointAgent((10, 6), [(4, 10),(11, 10),(19, 9)]),   
            
            #zona B
            IndependentCheckpointAgent((5,18), [(4, 10), (11, 10),(19, 9)]),
            IndependentCheckpointAgent((5, 14), [(4, 10), (11, 10),(19, 9)]),
            IndependentCheckpointAgent((2, 16), [(4, 10), (11, 10),(19, 9)]),
            
            #zona c
            IndependentCheckpointAgent((8, 18), [(13, 13),(19, 9)]),
            IndependentCheckpointAgent((13, 18), [(13, 13),(19, 9)]),
            
        ]
        return agents + checkpoint_agents
    
def main():
    # Usar SimulationSetup para configurar la simulación
    setup = SimulationSetup()
    environment = setup.setup_environment()
    agents = setup.setup_agents()

    # Inicializar y ejecutar la simulación
    simulation = Simulation(environment, agents)
    simulation.run(max_steps=33, delay=0.5)
    simulation.save_results()

if __name__ == "__main__":
    main()
